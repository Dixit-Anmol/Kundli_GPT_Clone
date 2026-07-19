"""
Tab-scoped Chat Endpoint.

Handles domain-specific chat by selecting the appropriate system prompt
and context builder based on the active tab.
"""
from fastapi import APIRouter, HTTPException
from models.request import TabChatRequest
from models.response import ChatResponse
from services.memory.session import session_store
from services.memory.profile_store import profile_store
from services.rag.bg_16 import BG16Pipeline
from services.prompts.tabs import get_tab_system_prompt, build_tab_context
from services.llm.factory import LLMFactory

router = APIRouter()

# RAG pipeline (reused for spiritual tab)
rag_pipeline = BG16Pipeline()


@router.post("/tab-chat", response_model=ChatResponse)
def handle_tab_chat(req: TabChatRequest):
    try:
        session = session_store.get_session(req.session_id)
        chart_data = session.get("chart_data")
        history = session.get("history", [])

        # Fallback: load from profile store if session has no chart data
        if not chart_data and req.user_id:
            stored = profile_store.load_profile(req.user_id)
            if stored and stored.get("natal_chart"):
                natal = stored["natal_chart"]
                chart_data = natal.get("natal", natal)
                session_store.save_chart(req.session_id, chart_data)
                session["profile"] = stored.get("birth_details", {})

        if not chart_data:
            return {
                "response": "🙏 Please provide your birth details first so I can generate your chart.",
                "session_count": 0,
            }

        profile = session.get("profile")
        computed = session.get("computed_analyses") or chart_data.get("computed")
        if not computed:
            from services.astrology.prakriti import estimate_prakriti
            from services.astrology.elements import calculate_element_distribution
            from services.astrology.lucky import calculate_lucky_attributes
            from services.astrology.planet_ranking import rank_planets
            from services.astrology.remedies_calc import generate_remedy_data

            prakriti = estimate_prakriti(chart_data)
            elements = calculate_element_distribution(chart_data)
            lucky = calculate_lucky_attributes(chart_data)
            rankings = rank_planets(chart_data)
            remedies = generate_remedy_data(chart_data, rankings)
            computed = {
                "prakriti": prakriti,
                "elements": elements,
                "lucky": lucky,
                "planet_rankings": rankings,
                "remedy_data": remedies,
            }
            session["computed_analyses"] = computed


        # Determine if this is the initial tab overview reading or a follow-up user chat question
        is_initial = bool(
            req.is_initial
            or req.message.startswith("Provide a detailed")
            or len(history) == 0
        )

        # Get domain-specific system prompt (Initial Overview vs Focused Chat Q&A)
        system_prompt = get_tab_system_prompt(req.tab, is_initial=is_initial)


        # Build domain-specific user context
        # For spiritual tab, include Bhagavad Gita RAG
        passages = None
        if req.tab == "spiritual":
            passages = rag_pipeline.search_wisdom(req.message, top_k=2)

        user_prompt = build_tab_context(
            tab=req.tab,
            query=req.message,
            chart_data=chart_data,
            profile=profile,
            history=history,
            computed=computed,
            passages=passages,
        )

        # Invoke LLM
        client = LLMFactory.get_client()
        api_key = session.get("key")
        if api_key:
            client.api_key = api_key

        response_text = client.generate(system_prompt, user_prompt)

        # Save chat turn to session history
        session_store.add_message(req.session_id, "user", req.message)
        session_store.add_message(req.session_id, "assistant", response_text)

        return {
            "response": response_text,
            "session_count": len(session_store.get_history(req.session_id)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
