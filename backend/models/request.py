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
    user_id: Optional[str] = None   # Anonymous persistent UUID from localStorage
    api_key: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_id: Optional[str] = None   # For profile-store fallback loading

class TabChatRequest(BaseModel):
    session_id: str
    message: str
    tab: str  # "overview" | "career" | "marriage" | "health" | "food" | "remedies" | "finance" | "personality" | "spiritual"
    user_id: Optional[str] = None
    is_initial: Optional[bool] = False
    relationship_type: Optional[str] = "spouse"  # father, mother, siblings, spouse, children, friends, boss, mentors, inlaws
    sub_tab: Optional[str] = "overview"  # "overview" | "kala_vidya"




