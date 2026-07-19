import requests
import pytz
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.request import TimezoneRequest, ChartRequest
from models.response import TimezoneResponse, ChartResponse
from services.astrology.horoscope import calculate_horoscope_data
from services.memory.session import session_store
from services.memory.profile_store import profile_store

# New astrology engine imports
from backend.astrology.types import BirthDetails
from backend.astrology.chart_generator import generate_all_charts
from backend.astrology.chart_storage import chart_cache

# Dashboard calculation engine imports
from services.astrology.prakriti import estimate_prakriti
from services.astrology.elements import calculate_element_distribution
from services.astrology.lucky import calculate_lucky_attributes
from services.astrology.planet_ranking import rank_planets
from services.astrology.remedies_calc import generate_remedy_data

router = APIRouter()


def find_timezone_offset(lat: float, lon: float, date_str: str) -> tuple:
    """Resolve the timezone name and historical UTC offset hours (standard or daylight saving time)."""
    # 1. Indian Subcontinent default check (most common Vedic astrology case)
    if 68.0 <= lon <= 89.0 and 8.0 <= lat <= 35.0:
        return "Asia/Kolkata", 5.5
        
    # 2. Attempt online API query
    try:
        url = f"https://timeapi.io/api/TimeZone/coordinate?latitude={lat}&longitude={lon}"
        res = requests.get(url, timeout=3)
        if res.ok:
            data = res.json()
            tz_name = data.get("timeZone", "UTC")
            tz = pytz.timezone(tz_name)
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            offset_seconds = tz.utcoffset(dt).total_seconds()
            return tz_name, offset_seconds / 3600.0
    except Exception as e:
        print(f"Online timezone API failed: {e}. Falling back to astronomical calculation.")
        
    # 3. Astronomical/Longitude based timezone approximation
    # 15 degrees longitude = 1 hour offset
    approx_offset = round((lon / 15.0) * 2.0) / 2.0  # Round to nearest 30 mins
    return "GMT", approx_offset

@router.post("/timezone", response_model=TimezoneResponse)
def get_timezone(req: TimezoneRequest):
    try:
        tz_name, offset = find_timezone_offset(req.latitude, req.longitude, req.date_str)
        return {"timezone_name": tz_name, "offset_hours": offset}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chart", response_model=ChartResponse)
def build_chart(req: ChartRequest):
    try:
        # Resolve timezone offset
        _, offset = find_timezone_offset(req.latitude, req.longitude, req.date_str)
        
        # Parse date and time
        dt = datetime.strptime(req.date_str, "%Y-%m-%d")
        tm = datetime.strptime(req.time_str, "%H:%M:%S")
        
        # Calculate full horoscope data (legacy path, still used for session/response)
        chart_data = calculate_horoscope_data(
            year=dt.year, month=dt.month, day=dt.day,
            hour=tm.hour, minute=tm.minute, second=tm.second,
            lat=req.latitude, lon=req.longitude, timezone_offset=offset
        )
        
        # Store in session memory
        session_store.save_chart(req.session_id, chart_data)
        sess = session_store.get_session(req.session_id)
        sess["profile"] = {
            "name": req.name,
            "date_of_birth": req.date_str,
            "time_of_birth": req.time_str,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "timezone_offset": offset
        }
        if req.api_key:
            # Save user API key for Anthropic/Groq calls if provided
            sess["key"] = req.api_key

        # ---------------------------------------------------------------
        # NEW: Generate ALL divisional charts via the new astrology engine
        # ---------------------------------------------------------------
        birth = BirthDetails(
            name=req.name,
            date_of_birth=req.date_str,
            time_of_birth=req.time_str,
            latitude=req.latitude,
            longitude=req.longitude,
            timezone_offset=offset,
        )

        # Generate all 15 divisional charts + global calculations
        bundle = generate_all_charts(birth)

        # Cache the full bundle (keyed by session_id, or user_id if available)
        cache_key = req.user_id or req.session_id
        chart_cache.store(cache_key, bundle)

        # Store the bundle dict in session for chat access
        sess["chart_bundle"] = bundle.to_dict()
        # ---------------------------------------------------------------
            
        meta = chart_data["metadata"]
        
        # Compute domain-specific dashboard analyses
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
        sess["computed_analyses"] = computed

        # Dynamically calculate current Vimshottari Mahadasha planet
        current_dasha_planet = (
            bundle.dasha.current_mahadasha.planet.capitalize()
            if bundle.dasha and bundle.dasha.current_mahadasha
            else "Jupiter"
        )

        chart_response = {
            "name": req.name,
            "ascendant_sign": meta["ascendant_sign"],
            "moon_sign": meta["moon_sign"],
            "nakshatra": meta["nakshatra"],
            "pada": meta["pada"],
            "current_dasha": current_dasha_planet,
            "metadata": meta,
            "houses": chart_data["houses"],
            "planets": chart_data["planets"],
            "yogas": chart_data["yogas"],
            "doshas": chart_data["doshas"],
            "raw_positions": chart_data["planets"],
            "computed": computed,
        }


        
        # Persist to profile store if user_id is provided (anonymous persistent profile)
        if req.user_id:
            birth_details = {
                "name": req.name,
                "date_of_birth": req.date_str,
                "time_of_birth": req.time_str,
                "latitude": req.latitude,
                "longitude": req.longitude,
                "timezone_offset": offset
            }
            # Save only the natal (static) portion to disk
            natal_doshas = {}
            all_doshas = chart_data.get("doshas", {})
            if "manglik" in all_doshas:
                natal_doshas["manglik"] = all_doshas["manglik"]
            if "kaal_sarp" in all_doshas:
                natal_doshas["kaal_sarp"] = all_doshas["kaal_sarp"]
                
            natal_chart = {
                "natal": {
                    "metadata": chart_data.get("metadata", {}),
                    "planets": chart_data.get("planets", {}),
                    "houses": chart_data.get("houses", {}),
                    "yogas": chart_data.get("yogas", []),
                    "doshas": natal_doshas,
                    "computed": computed,
                }
            }

            profile_store.save_profile(
                user_id=req.user_id,
                birth_details=birth_details,
                natal_chart=natal_chart,
                chart_response=chart_response,
            )
        
        return chart_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
