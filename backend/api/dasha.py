import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.memory.session import session_store
from services.memory.profile_store import profile_store
from services.astrology.dasha import calculate_full_dasha_package, lookup_dasha_by_year, PLANET_METADATA
from services.llm.factory import LLMFactory

router = APIRouter()

class DashaTimelineRequest(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    lookup_year: Optional[int] = None

@router.post("/dasha-timeline")
def get_dasha_timeline(req: DashaTimelineRequest):
    try:
        session = session_store.get_session(req.session_id)
        chart_data = session.get("chart_data")

        user_key = req.user_id or req.session_id
        stored = profile_store.load_profile(user_key) if user_key else None
        if not stored and req.session_id:
            stored = profile_store.load_profile(req.session_id)

        # Fallback load from profile_store if backend restarted or session reset
        if not chart_data and stored and stored.get("natal_chart"):
            natal = stored["natal_chart"]
            chart_data = natal.get("natal", natal)
            session_store.save_chart(req.session_id, chart_data)
            session = session_store.get_session(req.session_id)

        if not chart_data:
            raise HTTPException(
                status_code=404,
                detail="Natal chart data not found for session. Please enter birth details first."
            )

        # Extract Moon longitude and birth date
        planets = chart_data.get("planets", {})
        moon_data = planets.get("moon", {})
        moon_long = moon_data.get("longitude", 120.0)

        # Comprehensive birth date parsing across all potential keys
        meta = chart_data.get("metadata", {}) if isinstance(chart_data.get("metadata"), dict) else {}
        sess_bd = session.get("birth_details") or {}
        stored_bd = stored.get("birth_details") if stored else {}

        raw_dob = (
            meta.get("date_of_birth") or
            meta.get("birth_date") or
            meta.get("date_str") or
            chart_data.get("date_of_birth") or
            chart_data.get("birth_date") or
            chart_data.get("date_str") or
            sess_bd.get("date_of_birth") or
            sess_bd.get("date_str") or
            stored_bd.get("date_of_birth") or
            stored_bd.get("date_str")
        )

        birth_dt = None
        if raw_dob:
            try:
                from backend.utils.date_parser import parse_date_str
                birth_dt = parse_date_str(str(raw_dob))
            except Exception:
                try:
                    birth_dt = datetime.date.fromisoformat(str(raw_dob)[:10])
                except Exception:
                    pass

        if not birth_dt:
            birth_dt = datetime.date(1998, 5, 15)

        today_dt = datetime.date.today()

        # Compute full Vimshottari package
        package = calculate_full_dasha_package(moon_long, birth_dt, today_dt)

        # Optional Year Lookup
        lookup_result = None
        if req.lookup_year:
            lookup_result = lookup_dasha_by_year(package["timeline"], req.lookup_year)
        package["year_lookup"] = lookup_result

        # Generate Dynamic AI Interpretation for active Dasha
        curr_maha = package["current_mahadasha"]
        curr_antar = package["current_antardasha"]
        next_maha = package["next_mahadasha"]
        
        user_name = meta.get("name") or "Seeker"
        
        maha_name = curr_maha.get("planet_name", "Rahu")
        antar_name = curr_antar.get("planet_name", "Venus") if curr_antar else "Moon"

        # AI prompt for Dasha Interpretation
        sys_prompt = """You are AstroSutra AI — a master Vedic Dasha & Timing Analyst.

MANDATORY CONVERSATIONAL STYLE:
- Write in 2–3 clean, highly readable prose paragraphs.
- DO NOT use bullet points (- / *), raw asterisks, or markdown section headers.
- Directly address the seeker by their name in sentence 1.
- Synthesize the active Mahadasha and Antardasha themes, emotional shifts, career focus, and spiritual alignment."""

        user_prompt = f"""User: {user_name}
Active Mahadasha: {maha_name} ({curr_maha.get('start_date')} to {curr_maha.get('end_date')})
Active Antardasha: {antar_name} ({curr_antar.get('start_date') if curr_antar else 'N/A'} to {curr_antar.get('end_date') if curr_antar else 'N/A'})
Next Mahadasha: {next_maha.get('planet_name')} (starts {next_maha.get('start_date')})

Explain the core life themes, career focus, relationship dynamics, and strategic opportunities during this active {maha_name}-{antar_name} period. Target length: 150–200 words."""

        try:
            client = LLMFactory.get_client()
            ai_text = client.generate(sys_prompt, user_prompt, max_tokens=380)
        except Exception as e:
            ai_text = (
                f"{user_name}, your active **{maha_name} Mahadasha** brings significant personal transformation and "
                f"strategic movement. Under **{antar_name} Antardasha**, your emotional focus, creative pursuits, "
                f"and key partnerships are heightened. Aligning your daily routine with {maha_name}'s strengths will unlock unexpected growth."
            )

        package["ai_interpretation"] = {
            "summary": ai_text,
            "mahadasha_name": maha_name,
            "antardasha_name": antar_name,
            "focus_areas": {
                "career": f"High potential for growth, expansion, and strategic execution during {maha_name} period.",
                "relationships": f"{antar_name} Antardasha enhances emotional resonance, bonding, and harmony.",
                "health": "Maintain daily discipline, balanced sleep cycles, and mindful vitality management.",
                "spiritual": f"Embrace self-reflection and inner growth aligned with {maha_name}'s karmic lessons."
            },
            "challenges": [
                f"Navigating sudden transition phases during {maha_name} shift",
                "Balancing ambition with emotional stability"
            ],
            "opportunities": [
                f"Favorable windows for relationship & financial growth under {antar_name} Antardasha",
                "New professional networks and expansion"
            ]
        }

        return package

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
