import requests
import pytz
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.request import TimezoneRequest, ChartRequest
from models.response import TimezoneResponse, ChartResponse
from services.astrology.horoscope import calculate_horoscope_data
from services.memory.session import session_store

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
            "date_of_birth": req.date_str,
            "time_of_birth": req.time_str,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "timezone_offset": offset
        }
        if req.api_key:
            # Save user API key for Anthropic/Groq calls if provided
            sess["key"] = req.api_key
            
        meta = chart_data["metadata"]
        
        return {
            "name": req.name,
            "ascendant_sign": meta["ascendant_sign"],
            "moon_sign": meta["moon_sign"],
            "nakshatra": meta["nakshatra"],
            "pada": meta["pada"],
            "yogas": chart_data["yogas"],
            "doshas": chart_data["doshas"],
            "raw_positions": chart_data["planets"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
