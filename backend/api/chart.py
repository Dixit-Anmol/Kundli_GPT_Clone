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

from services.astrology.prashna_engine import calculate_prashna_chart
from services.astrology.partial_horoscope_engine import calculate_partial_horoscope

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
        mode = (req.mode or "exact").lower()

        # ---------------------------------------------------------------
        # Option 3: Prashna Kundli (Horary)
        # ---------------------------------------------------------------
        if mode == "prashna":
            _, offset = find_timezone_offset(req.latitude, req.longitude, datetime.now().strftime("%Y-%m-%d"))
            chart_data = calculate_prashna_chart(
                question=req.question or "General Guidance",
                category=req.category or "general",
                lat=req.latitude,
                lon=req.longitude,
                timezone_offset=offset
            )

            # Store in session memory
            session_store.save_chart(req.session_id, chart_data)
            sess = session_store.get_session(req.session_id)
            sess["profile"] = {
                "name": req.name,
                "mode": "prashna",
                "question": req.question,
                "category": req.category,
                "latitude": req.latitude,
                "longitude": req.longitude,
                "timezone_offset": offset
            }
            if req.api_key:
                sess["key"] = req.api_key

            return {
                "name": req.name,
                "ascendant_sign": chart_data["prashna_lagna"]["sign"],
                "moon_sign": chart_data["planets"]["moon"]["sign"],
                "nakshatra": chart_data["panchanga"]["nakshatra"],
                "pada": chart_data["panchanga"]["pada"],
                "yogas": [],
                "doshas": {},
                "raw_positions": chart_data["raw_positions"],
                "mode": "prashna",
                "chart_type": chart_data["chart_type"],
                "question": chart_data["question"],
                "category": chart_data["category"],
                "location": chart_data["location"],
                "prashna_time": chart_data["prashna_time"],
                "prashna_lagna": chart_data["prashna_lagna"],
                "panchanga": chart_data["panchanga"],
                "disclaimer": chart_data["disclaimer"],
                "planets": chart_data["planets"]
            }

        # ---------------------------------------------------------------
        # Option 2: Partial Birth Details (Estimated Horoscope)
        # ---------------------------------------------------------------
        elif mode == "partial":
            date_parts = (req.date_str or "2000-01-01").split("-")
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
            _, offset = find_timezone_offset(req.latitude, req.longitude, req.date_str or "2000-01-01")

            chart_data = calculate_partial_horoscope(
                year=year, month=month, day=day,
                time_slot=req.time_slot or "unknown",
                exact_time=req.time_str,
                lat=req.latitude, lon=req.longitude, timezone_offset=offset
            )

            # Store in session memory
            session_store.save_chart(req.session_id, chart_data)
            sess = session_store.get_session(req.session_id)
            sess["profile"] = {
                "name": req.name,
                "mode": "partial",
                "date_of_birth": req.date_str,
                "time_slot": req.time_slot,
                "latitude": req.latitude,
                "longitude": req.longitude,
                "timezone_offset": offset
            }
            if req.api_key:
                sess["key"] = req.api_key

            return {
                "name": req.name,
                "ascendant_sign": "Estimated (Lagna Excluded)",
                "moon_sign": chart_data["moon_sign"],
                "nakshatra": chart_data["nakshatra"],
                "pada": 1,
                "yogas": [],
                "doshas": {},
                "raw_positions": chart_data["raw_positions"],
                "mode": "partial",
                "chart_type": chart_data["chart_type"],
                "confidence_level": chart_data["confidence_level"],
                "birth_date": chart_data["birth_date"],
                "time_slot": chart_data["time_slot"],
                "has_exact_time": chart_data["has_exact_time"],
                "moon_stable": chart_data["moon_stable"],
                "exact_calculations": chart_data["exact_calculations"],
                "estimated_calculations": chart_data["estimated_calculations"],
                "excluded_calculations": chart_data["excluded_calculations"],
                "disclaimer": chart_data["disclaimer"],
                "planets": chart_data["planets"],
                "transits": chart_data["transits"]
            }


        # ---------------------------------------------------------------
        # Option 1: Complete Janma Kundli (Exact Birth Details)
        # ---------------------------------------------------------------
        # Resolve timezone offset
        _, offset = find_timezone_offset(req.latitude, req.longitude, req.date_str)
        
        # Parse date and time
        dt = datetime.strptime(req.date_str, "%Y-%m-%d")
        tm = datetime.strptime(req.time_str, "%H:%M:%S")
        
        # Calculate full horoscope data
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
            "mode": "exact",
            "date_of_birth": req.date_str,
            "time_of_birth": req.time_str,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "timezone_offset": offset
        }
        if req.api_key:
            sess["key"] = req.api_key

        birth = BirthDetails(
            name=req.name,
            date_of_birth=req.date_str,
            time_of_birth=req.time_str,
            latitude=req.latitude,
            longitude=req.longitude,
            timezone_offset=offset,
        )

        bundle = generate_all_charts(birth)
        cache_key = req.user_id or req.session_id
        chart_cache.store(cache_key, bundle)
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
