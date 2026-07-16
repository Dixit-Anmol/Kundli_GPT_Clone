from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class TimezoneResponse(BaseModel):
    timezone_name: str
    offset_hours: float

class ChartResponse(BaseModel):
    name: str
    ascendant_sign: str
    moon_sign: str
    nakshatra: str
    pada: int
    yogas: List[Dict[str, Any]]
    doshas: Dict[str, Any]
    raw_positions: Dict[str, Any]

class ChatResponse(BaseModel):
    response: str
    session_count: int
