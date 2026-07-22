from pydantic import BaseModel
from typing import Optional

class TimezoneRequest(BaseModel):
    latitude: float
    longitude: float
    date_str: str  # YYYY-MM-DD format

class ChartRequest(BaseModel):
    name: str
    date_str: Optional[str] = "2000-01-01"  # YYYY-MM-DD
    time_str: Optional[str] = "12:00:00"  # HH:MM:SS
    latitude: float
    longitude: float
    session_id: str
    user_id: Optional[str] = None   # Anonymous persistent UUID from localStorage
    api_key: Optional[str] = None
    mode: Optional[str] = "exact"  # "exact" | "partial" | "prashna"
    time_slot: Optional[str] = "unknown" # "morning" | "afternoon" | "evening" | "night" | "sunrise" | "sunset" | "unknown"
    question: Optional[str] = None
    category: Optional[str] = "general"

class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_id: Optional[str] = None   # For profile-store fallback loading

class TabChatRequest(BaseModel):
    session_id: str
    message: str
    tab: str  # "overview" | "career" | "marriage" | "health" | "food" | "remedies" | "finance" | "personality" | "spiritual" | "matching"
    user_id: Optional[str] = None
    is_initial: Optional[bool] = False
    relationship_type: Optional[str] = "spouse"  # father, mother, siblings, spouse, children, friends, boss, mentors, inlaws
    sub_tab: Optional[str] = "overview"  # "overview" | "kala_vidya"
    mode: Optional[str] = "exact"
    time_slot: Optional[str] = "unknown"
    question: Optional[str] = None
    category: Optional[str] = "general"
    tier: Optional[str] = "free"

class PersonMatchInput(BaseModel):
    profile_id: Optional[str] = None
    name: Optional[str] = "Partner"
    date_str: Optional[str] = "2000-01-01"
    time_str: Optional[str] = "12:00:00"
    latitude: Optional[float] = 28.6139
    longitude: Optional[float] = 77.2090
    timezone_offset: Optional[float] = 5.5

class KundliMatchRequest(BaseModel):
    session_id: str
    person_a: PersonMatchInput
    person_b: PersonMatchInput
