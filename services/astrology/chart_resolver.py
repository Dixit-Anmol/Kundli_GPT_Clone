"""
Robust Chart Resolver Helper.
Ensures chart_data is ALWAYS found or dynamically re-calculated from birth details,
surviving server restarts, container redeploys, and ephemeral disk wipes on cloud hosting (Render).
"""

from typing import Optional, Dict, Any
from services.memory.session import session_store
from services.memory.profile_store import profile_store
from services.astrology.horoscope import calculate_horoscope_data
try:
    from backend.utils.date_parser import parse_date_str, parse_time_str
except ImportError:
    from utils.date_parser import parse_date_str, parse_time_str

try:
    from backend.api.chart import find_timezone_offset
except ImportError:
    try:
        from api.chart import find_timezone_offset
    except ImportError:
        def find_timezone_offset(lat: float, lon: float, date_str: str) -> tuple[float, float]:
            return 5.5, 5.5

def resolve_chart_data(
    session_id: str,
    user_id: Optional[str] = None,
    req_birth_details: Optional[Dict[str, Any]] = None,
    req_chart_data: Optional[Dict[str, Any]] = None,
) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Attempts multi-tiered retrieval and recalculation of chart_data and birth_details.

    Returns (chart_data, birth_details) tuple.
    """
    chart_data = None
    birth_details = None

    # Tier 1: Check session_store for session_id
    if session_id:
        sess = session_store.get_session(session_id)
        chart_data = sess.get("chart_data")
        birth_details = sess.get("profile") or sess.get("birth_details")

    # Tier 2: Check session_store for user_id
    if not chart_data and user_id:
        user_sess = session_store.get_session(user_id)
        chart_data = user_sess.get("chart_data")
        if not birth_details:
            birth_details = user_sess.get("profile") or user_sess.get("birth_details")

    # Tier 3: Check profile_store on disk for user_id or session_id
    stored = None
    if user_id:
        stored = profile_store.load_profile(user_id)
    if not stored and session_id:
        stored = profile_store.load_profile(session_id)

    if stored:
        if not birth_details:
            birth_details = stored.get("birth_details")
        if not chart_data and stored.get("natal_chart"):
            natal = stored["natal_chart"]
            chart_data = natal.get("natal", natal)

    # Tier 4: Check if chart_data passed directly in request
    if not chart_data and req_chart_data and isinstance(req_chart_data, dict):
        chart_data = req_chart_data

    # Tier 5: Check if birth_details passed directly in request
    if req_birth_details and isinstance(req_birth_details, dict):
        if not birth_details:
            birth_details = req_birth_details
        else:
            birth_details.update(req_birth_details)

    # Tier 6: Recalculate on the fly if chart_data is missing or incomplete (lacks planets)
    is_valid_chart = (
        isinstance(chart_data, dict) and
        bool(chart_data.get("planets")) and
        bool(chart_data.get("metadata"))
    )

    if not is_valid_chart and birth_details:
        dob_str = (
            birth_details.get("date_of_birth") or
            birth_details.get("dateOfBirth") or
            birth_details.get("date_str") or
            birth_details.get("dob")
        )
        tob_str = (
            birth_details.get("time_of_birth") or
            birth_details.get("timeOfBirth") or
            birth_details.get("time_str") or
            birth_details.get("tob")
        )
        lat = birth_details.get("latitude") if birth_details.get("latitude") is not None else birth_details.get("lat", 28.6139)
        lon = birth_details.get("longitude") if birth_details.get("longitude") is not None else (
            birth_details.get("lng") if birth_details.get("lng") is not None else birth_details.get("lon", 77.2090)
        )

        if dob_str and tob_str:
            try:
                _, offset = find_timezone_offset(float(lat), float(lon), str(dob_str))
                dt = parse_date_str(str(dob_str))
                tm = parse_time_str(str(tob_str))

                computed_chart = calculate_horoscope_data(
                    year=dt.year, month=dt.month, day=dt.day,
                    hour=tm.hour, minute=tm.minute, second=tm.second,
                    lat=float(lat), lon=float(lon), timezone_offset=float(offset)
                )
                if computed_chart:
                    chart_data = computed_chart
            except Exception as e:
                print(f"[ChartResolver] Error recalculating chart_data on the fly: {e}")

    # Re-hydrate session_store & profile_store if we have valid chart_data
    if chart_data and isinstance(chart_data, dict) and chart_data.get("planets"):
        if session_id:
            session_store.save_chart(session_id, chart_data)
            sess = session_store.get_session(session_id)
            if birth_details:
                sess["profile"] = birth_details
        if user_id:
            session_store.save_chart(user_id, chart_data)
            user_sess = session_store.get_session(user_id)
            if birth_details:
                user_sess["profile"] = birth_details

        # Persist to disk if user_id and birth_details exist
        if user_id and birth_details:
            try:
                profile_store.save_profile(
                    user_id=user_id,
                    birth_details=birth_details,
                    natal_chart={"natal": chart_data},
                    chart_response={"ascendant_sign": chart_data.get("metadata", {}).get("ascendant_sign", "")}
                )
            except Exception as e:
                print(f"[ChartResolver] Failed to persist profile: {e}")

    return chart_data, birth_details
