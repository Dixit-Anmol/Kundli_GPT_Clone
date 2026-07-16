from pydantic import BaseModel
from typing import Optional

class TimezoneRequest(BaseModel):
    latitude: float
    longitude: float
    date_str: str  # YYYY-MM-DD format

class ChartRequest(BaseModel):
    name: str
    date_str: str  # YYYY-MM-DD
    time_str: str  # HH:MM:SS
    latitude: float
    longitude: float
    session_id: str
    api_key: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str
