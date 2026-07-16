from fastapi import APIRouter, HTTPException
from models.request import ChatRequest
from models.response import ChatResponse
from services.memory.session import session_store
from services.memory.history import ChatHistory
from services.rag.bg_16 import BG16Pipeline
from services.prompts.system import get_system_prompt
from services.prompts.horoscope import build_horoscope_prompt
from services.prompts.geeta import build_geeta_prompt
from services.llm.factory import LLMFactory

router = APIRouter()

# Instantiate global collection-specific RAG pipeline for Bhagavad Gita Chapter 16
rag_pipeline = BG16Pipeline()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    try:
        session = session_store.get_session(req.session_id)
        chart_data = session.get("chart_data")
        history = session.get("history", [])
        
        # 1. Block if birth chart is not generated yet
        if not chart_data:
            return {
                "response": "🙏 Namaste. Before I can offer specific readings, please provide your birth details (date, time, and city) above so I may calculate your Lagna chart.",
                "session_count": len(history)
            }
            
        # 2. Determine prompt style based on context and history
        system_prompt = get_system_prompt()
        
        # Retrieve relevant Bhagavad Gita verses using RAG
        gita_passages = rag_pipeline.search_wisdom(req.message, top_k=2)
        
        # Is this the initial analysis request?
        is_initial = len(history) == 0 or "explain" in req.message.lower() or "chart" in req.message.lower()
        
        if is_initial:
            user_prompt = build_horoscope_prompt(
                name="Seeker", 
                chart_data=chart_data
            )
        else:
            # Format chat history for context
            history_context = ChatHistory.format_history(history)
            user_prompt = build_geeta_prompt(
                name="Seeker",
                query=req.message,
                chart_data=chart_data,
                passages=gita_passages
            )
            # Append history reference to prompt
            user_prompt += f"\n[Previous Conversation History]\n{history_context}"
            
        # 3. Invoke LLM (Groq or Claude based on setup)
        # Use session-saved API key if provided, else use system environment keys
        api_key = session.get("key")
        
        client = LLMFactory.get_client()
        if api_key:
            client.api_key = api_key # Override client key with session key
            
        response_text = client.generate(system_prompt, user_prompt)
        
        # 4. Save chat turn to session history
        session_store.add_message(req.session_id, "user", req.message)
        session_store.add_message(req.session_id, "assistant", response_text)
        
        return {
            "response": response_text,
            "session_count": len(session_store.get_history(req.session_id))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
