from fastapi import APIRouter, HTTPException
from models.request import ChatRequest
from models.response import ChatResponse
from services.memory.session import session_store
from services.memory.profile_store import profile_store
from services.memory.history import ChatHistory
from services.rag.bg_16 import BG16Pipeline
from services.prompts.system import get_system_prompt
from services.prompts.horoscope import build_horoscope_prompt
from services.prompts.geeta import build_geeta_prompt, assemble_unified_prompt, classify_intent
from services.prompts.financial import is_financial_query, get_financial_system_prompt
from services.llm.factory import LLMFactory

# New astrology engine imports
from backend.astrology.chart_storage import chart_cache
from backend.astrology.chart_selector import select_charts_for_topic

router = APIRouter()

# Instantiate global collection-specific RAG pipeline for Bhagavad Gita Chapter 16
rag_pipeline = BG16Pipeline()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    try:
        session = session_store.get_session(req.session_id)

        # Enforce strict profile isolation: if session user_id does not match req.user_id, reset session chart_data
        if req.user_id and session.get("user_id") != req.user_id:
            session["chart_data"] = None
            session["user_id"] = req.user_id
            session["history"] = []

        chart_data = session.get("chart_data")
        history = session.get("history", [])

        
        # Fallback: If session has no chart data (e.g. server restart),
        # load from persistent disk profile store
        if not chart_data:
            user_key = req.user_id or req.session_id
            stored = profile_store.load_profile(user_key) if user_key else None
            if not stored and req.session_id:
                stored = profile_store.load_profile(req.session_id)

            if stored and stored.get("natal_chart"):
                natal = stored["natal_chart"]
                chart_data = natal.get("natal", natal)
                session_store.save_chart(req.session_id, chart_data)
                session = session_store.get_session(req.session_id)
                session["profile"] = stored.get("birth_details", {})

        
        # 1. Block if birth chart is not generated yet
        if not chart_data:
            return {
                "response": "🙏 Namaste. Before I can offer specific readings, please provide your birth details (date, time, and city) above so I may calculate your Lagna chart.",
                "session_count": len(history)
            }
            
        # 2. Classify user intent for topic-based chart selection
        detected_intent = classify_intent(req.message)
        
        # 3. Load the full chart bundle from cache (if available)
        cache_key = req.user_id or req.session_id
        chart_bundle = session.get("chart_bundle") or chart_cache.load(cache_key)
        
        # 4. Select topic-specific charts for the LLM
        selected_charts = None
        if chart_bundle:
            selected_charts = select_charts_for_topic(detected_intent, chart_bundle)
            
        # 5. Determine prompt style based on context and history
        # Use specialised financial system prompt when the query is finance-related
        if not (len(history) == 0) and is_financial_query(req.message):
            system_prompt = get_financial_system_prompt()
        else:
            system_prompt = get_system_prompt()
        
        # Retrieve relevant Bhagavad Gita verses using RAG
        gita_passages = rag_pipeline.search_wisdom(req.message, top_k=2)
        
        profile = session.get("profile")
        
        # Is this the initial analysis request?
        is_initial = len(history) == 0
        
        if is_initial:
            user_prompt = build_horoscope_prompt(
                name=profile.get("name") if profile else "Seeker", 
                chart_data=chart_data,
                profile=profile
            )
        else:
            try:
                user_prompt = assemble_unified_prompt(
                    query=req.message,
                    chart_data=chart_data,
                    profile=profile,
                    history=history,
                    passages=gita_passages,
                    intent=detected_intent,
                    selected_charts=selected_charts,
                )
            except TypeError as e:
                if "unexpected keyword argument" in str(e) or "selected_charts" in str(e):
                    user_prompt = assemble_unified_prompt(
                        query=req.message,
                        chart_data=chart_data,
                        profile=profile,
                        history=history,
                        passages=gita_passages,
                        intent=detected_intent,
                    )
                else:
                    raise e
            
        # 6. Invoke LLM (Groq or Claude based on setup)
        # Use session-saved API key if provided, else use system environment keys
        api_key = session.get("key")
        
        client = LLMFactory.get_client()
        if api_key:
            client.api_key = api_key # Override client key with session key
            
        response_text = client.generate(system_prompt, user_prompt, max_tokens=420)
        
        # 7. Save chat turn to session history
        session_store.add_message(req.session_id, "user", req.message)
        session_store.add_message(req.session_id, "assistant", response_text)
        
        return {
            "response": response_text,
            "session_count": len(session_store.get_history(req.session_id))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
