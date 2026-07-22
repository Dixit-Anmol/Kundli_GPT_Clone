import datetime
from typing import Dict, List, Any, Optional

DASHA_ORDER = ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"]

DASHA_YEARS = {
    "ketu": 7,
    "venus": 20,
    "sun": 6,
    "moon": 10,
    "mars": 7,
    "rahu": 18,
    "jupiter": 16,
    "saturn": 19,
    "mercury": 17
}

PLANET_METADATA = {
    "sun": {
        "name": "Sun",
        "sanskrit": "Surya",
        "color": "#EAB308", # Gold
        "bg": "rgba(234, 179, 8, 0.15)",
        "border": "#CA8A04",
        "icon": "wb_sunny",
        "themes": ["Leadership & Recognition", "Authority & Power", "Self-Realization", "Career Elevation", "Vitality & Health"]
    },
    "moon": {
        "name": "Moon",
        "sanskrit": "Chandra",
        "color": "#38BDF8", # Silver/Sky
        "bg": "rgba(56, 189, 248, 0.15)",
        "border": "#0284C7",
        "icon": "bedtime",
        "themes": ["Emotional Peace & Mind", "Home & Family Bonding", "Intuition & Creativity", "Public Reputation", "Travel & Relocation"]
    },
    "mars": {
        "name": "Mars",
        "sanskrit": "Mangal",
        "color": "#EF4444", # Red
        "bg": "rgba(239, 68, 68, 0.15)",
        "border": "#DC2626",
        "icon": "local_fire_department",
        "themes": ["Energy & Ambition", "Property & Real Estate", "Courage & Initiative", "Technical Skills", "Competitive Mastery"]
    },
    "mercury": {
        "name": "Mercury",
        "sanskrit": "Budha",
        "color": "#10B981", # Emerald
        "bg": "rgba(16, 185, 129, 0.15)",
        "border": "#059669",
        "icon": "menu_book",
        "themes": ["Business & Commerce", "Communication & Writing", "Intellectual Growth", "Trading & Networking", "Skill Development"]
    },
    "jupiter": {
        "name": "Jupiter",
        "sanskrit": "Guru",
        "color": "#F59E0B", # Yellow/Amber
        "bg": "rgba(245, 158, 11, 0.15)",
        "border": "#B45309",
        "icon": "auto_awesome",
        "themes": ["Wisdom & Higher Education", "Marriage & Relationship Security", "Children & Progeny Growth", "Career Elevation", "Spiritual Realization"]
    },
    "venus": {
        "name": "Venus",
        "sanskrit": "Shukra",
        "color": "#EC4899", # Pink/Rose
        "bg": "rgba(236, 72, 153, 0.15)",
        "border": "#E11D48",
        "icon": "favorite",
        "themes": ["Relationships & Love", "Luxury & Material Comforts", "Arts & Creative Design", "Financial Prosperity", "Harmonious Bonds"]
    },
    "saturn": {
        "name": "Saturn",
        "sanskrit": "Shani",
        "color": "#6366F1", # Indigo
        "bg": "rgba(99, 102, 241, 0.15)",
        "border": "#4338CA",
        "icon": "hourglass_empty",
        "themes": ["Discipline & Hard Work", "Long-term Security", "Karmic Lessons", "Structure & Endurance", "Patience & Perseverance"]
    },
    "rahu": {
        "name": "Rahu",
        "sanskrit": "Rahu",
        "color": "#8B5CF6", # Purple
        "bg": "rgba(139, 92, 246, 0.15)",
        "border": "#7C3AED",
        "icon": "blur_on",
        "themes": ["Transformation & Innovation", "Foreign Opportunities", "Unconventional Success", "Ambition & Scaling", "Tech Mastery"]
    },
    "ketu": {
        "name": "Ketu",
        "sanskrit": "Ketu",
        "color": "#6B7280", # Slate Gray
        "bg": "rgba(107, 114, 128, 0.15)",
        "border": "#4B5563",
        "icon": "psychology",
        "themes": ["Spiritual Awakening", "Detachment & Research", "Intuitive Depth", "Inner Mastery", "Karmic Resolution"]
    }
}


def _format_remaining_time(days: int) -> str:
    """Format remaining days into years and months string."""
    if days <= 0:
        return "Completed"
    years = days // 365
    rem_days = days % 365
    months = rem_days // 30
    
    parts = []
    if years > 0:
        parts.append(f"{years} Yr{'s' if years > 1 else ''}")
    if months > 0 or years == 0:
        parts.append(f"{months} Mo{'s' if months != 1 else ''}")
    return " ".join(parts)


def calculate_antardashas(
    maha_planet: str,
    maha_start: datetime.date,
    maha_end: datetime.date,
    today_date: datetime.date
) -> List[Dict[str, Any]]:
    """Calculate all 9 Antardashas within a Mahadasha."""
    maha_planet = maha_planet.lower()
    start_idx = DASHA_ORDER.index(maha_planet)
    
    current_date = maha_start
    antardashas = []
    maha_years = DASHA_YEARS[maha_planet]

    for i in range(9):
        antar_planet = DASHA_ORDER[(start_idx + i) % 9]
        antar_years = (maha_years * DASHA_YEARS[antar_planet]) / 120.0
        days = int(round(antar_years * 365.25))
        
        antar_end = current_date + datetime.timedelta(days=days)
        
        # Status determination
        if today_date > antar_end:
            status = "completed"
            progress = 1.0
            days_rem = 0
        elif today_date < current_date:
            status = "upcoming"
            progress = 0.0
            days_rem = (antar_end - current_date).days
        else:
            status = "current"
            elapsed = (today_date - current_date).days
            total = (antar_end - current_date).days or 1
            progress = min(1.0, max(0.0, elapsed / total))
            days_rem = (antar_end - today_date).days

        meta = PLANET_METADATA.get(antar_planet, PLANET_METADATA["jupiter"])

        antardashas.append({
            "planet": antar_planet,
            "planet_name": meta["name"],
            "combination": f"{PLANET_METADATA.get(maha_planet, {}).get('name', maha_planet.capitalize())} / {meta['name']}",
            "start_date": current_date.isoformat(),
            "end_date": antar_end.isoformat(),
            "duration_years": round(antar_years, 2),
            "progress": round(progress, 2),
            "days_remaining": days_rem,
            "remaining_formatted": _format_remaining_time(days_rem),
            "status": status,
            "color": meta["color"],
            "icon": meta["icon"],
        })
        current_date = antar_end

    return antardashas


def calculate_pratyantardashas(
    maha_planet: str,
    antar_planet: str,
    antar_start: datetime.date,
    antar_end: datetime.date,
    today_date: datetime.date
) -> List[Dict[str, Any]]:
    """Calculate Pratyantardashas for a specific Antardasha."""
    maha_planet = maha_planet.lower()
    antar_planet = antar_planet.lower()
    start_idx = DASHA_ORDER.index(antar_planet)
    
    current_date = antar_start
    pratyantardashas = []
    maha_years = DASHA_YEARS[maha_planet]
    antar_years = DASHA_YEARS[antar_planet]

    for i in range(9):
        praty_planet = DASHA_ORDER[(start_idx + i) % 9]
        praty_years = (maha_years * antar_years * DASHA_YEARS[praty_planet]) / 14400.0
        days = int(round(praty_years * 365.25))
        praty_end = current_date + datetime.timedelta(days=days)
        
        if today_date > praty_end:
            status = "completed"
        elif today_date < current_date:
            status = "upcoming"
        else:
            status = "current"

        meta = PLANET_METADATA.get(praty_planet, PLANET_METADATA["jupiter"])

        pratyantardashas.append({
            "planet": praty_planet,
            "planet_name": meta["name"],
            "start_date": current_date.isoformat(),
            "end_date": praty_end.isoformat(),
            "duration_days": days,
            "status": status,
            "color": meta["color"],
        })
        current_date = praty_end

    return pratyantardashas


def calculate_full_dasha_package(
    moon_longitude: float,
    birth_date: datetime.date,
    today_date: Optional[datetime.date] = None
) -> Dict[str, Any]:
    """
    Computes complete Vimshottari Dasha Package for natal chart:
    - Chronological Mahadasha Timeline (with nested Antardashas)
    - Active Mahadasha, Antardasha, and Pratyantardasha
    - Timeline Statistics & Year Lookup Engine
    - Next Mahadasha Focus Card
    """
    if not today_date:
        today_date = datetime.date.today()

    nak_width = 360.0 / 27.0
    nak_idx = int(moon_longitude // nak_width)
    
    start_long = nak_idx * nak_width
    progress_frac = (moon_longitude - start_long) / nak_width
    
    start_lord_idx = nak_idx % 9
    start_lord = DASHA_ORDER[start_lord_idx]
    
    start_lord_years = DASHA_YEARS[start_lord]
    years_remaining_at_birth = start_lord_years * (1.0 - progress_frac)
    
    current_date = birth_date
    timeline = []
    
    # First Mahadasha (partial)
    first_days = int(round(years_remaining_at_birth * 365.25))
    first_end = current_date + datetime.timedelta(days=first_days)
    
    first_meta = PLANET_METADATA[start_lord]
    first_antars = calculate_antardashas(start_lord, current_date, first_end, today_date)
    
    timeline.append({
        "planet": start_lord,
        "planet_name": first_meta["name"],
        "sanskrit_name": first_meta["sanskrit"],
        "start_date": current_date.isoformat(),
        "end_date": first_end.isoformat(),
        "duration_years": round(years_remaining_at_birth, 2),
        "total_mahadasha_years": start_lord_years,
        "color": first_meta["color"],
        "bg": first_meta["bg"],
        "border": first_meta["border"],
        "icon": first_meta["icon"],
        "themes": first_meta["themes"],
        "antardashas": first_antars,
    })
    current_date = first_end
    
    # Remaining 8 Mahadashas
    curr_idx = (start_lord_idx + 1) % 9
    for _ in range(8):
        lord = DASHA_ORDER[curr_idx]
        years = DASHA_YEARS[lord]
        days = int(round(years * 365.25))
        end_date = current_date + datetime.timedelta(days=days)
        meta = PLANET_METADATA[lord]
        
        antars = calculate_antardashas(lord, current_date, end_date, today_date)
        
        timeline.append({
            "planet": lord,
            "planet_name": meta["name"],
            "sanskrit_name": meta["sanskrit"],
            "start_date": current_date.isoformat(),
            "end_date": end_date.isoformat(),
            "duration_years": years,
            "total_mahadasha_years": years,
            "color": meta["color"],
            "bg": meta["bg"],
            "border": meta["border"],
            "icon": meta["icon"],
            "themes": meta["themes"],
            "antardashas": antars,
        })
        current_date = end_date
        curr_idx = (curr_idx + 1) % 9

    # Determine status & progress for each Mahadasha
    current_maha = None
    next_maha = None
    completed_count = 0
    upcoming_count = 0

    for idx, item in enumerate(timeline):
        s_dt = datetime.date.fromisoformat(item["start_date"])
        e_dt = datetime.date.fromisoformat(item["end_date"])
        
        if today_date > e_dt:
            item["status"] = "completed"
            item["progress"] = 1.0
            completed_count += 1
        elif today_date < s_dt:
            item["status"] = "upcoming"
            item["progress"] = 0.0
            upcoming_count += 1
            if current_maha and not next_maha:
                next_maha = item
        else:
            item["status"] = "current"
            elapsed = (today_date - s_dt).days
            total = (e_dt - s_dt).days or 1
            item["progress"] = round(min(1.0, max(0.0, elapsed / total)), 2)
            item["days_remaining"] = (e_dt - today_date).days
            item["remaining_formatted"] = _format_remaining_time(item["days_remaining"])
            current_maha = item

    if not current_maha:
        current_maha = timeline[-1]
        current_maha["status"] = "current"

    if not next_maha and len(timeline) > 1:
        curr_idx = timeline.index(current_maha)
        if curr_idx + 1 < len(timeline):
            next_maha = timeline[curr_idx + 1]

    # Find active Antardasha
    current_antar = None
    for a in current_maha.get("antardashas", []):
        if a["status"] == "current":
            current_antar = a
            break
    if not current_antar and current_maha.get("antardashas"):
        current_antar = current_maha["antardashas"][0]

    # Find active Pratyantardasha
    current_praty = None
    if current_maha and current_antar:
        a_s = datetime.date.fromisoformat(current_antar["start_date"])
        a_e = datetime.date.fromisoformat(current_antar["end_date"])
        pratys = calculate_pratyantardashas(current_maha["planet"], current_antar["planet"], a_s, a_e, today_date)
        for p in pratys:
            if p["status"] == "current":
                current_praty = p
                break

    # Age calculation
    age = today_date.year - birth_date.year - ((today_date.month, today_date.day) < (birth_date.month, birth_date.day))
    years_rem_maha = round(current_maha.get("days_remaining", 0) / 365.25, 1)

    return {
        "current_mahadasha": {
            "planet": current_maha["planet"],
            "planet_name": current_maha["planet_name"],
            "start_date": current_maha["start_date"],
            "end_date": current_maha["end_date"],
            "duration_years": current_maha["duration_years"],
            "progress": current_maha["progress"],
            "days_remaining": current_maha.get("days_remaining", 0),
            "remaining_formatted": current_maha.get("remaining_formatted", ""),
            "color": current_maha["color"],
            "icon": current_maha["icon"],
        },
        "current_antardasha": current_antar,
        "current_pratyantardasha": current_praty,
        "next_mahadasha": {
            "planet": next_maha["planet"] if next_maha else "N/A",
            "planet_name": next_maha["planet_name"] if next_maha else "N/A",
            "start_date": next_maha["start_date"] if next_maha else "N/A",
            "end_date": next_maha["end_date"] if next_maha else "N/A",
            "duration_years": next_maha["duration_years"] if next_maha else 0,
            "color": next_maha["color"] if next_maha else "#F59E0B",
            "icon": next_maha["icon"] if next_maha else "auto_awesome",
            "themes": next_maha["themes"] if next_maha else [],
        },
        "statistics": {
            "completed_count": completed_count,
            "current_mahadasha_name": current_maha["planet_name"],
            "upcoming_count": upcoming_count,
            "current_age": age,
            "years_remaining_current": years_rem_maha,
        },
        "timeline": timeline,
    }


def lookup_dasha_by_year(timeline: List[Dict[str, Any]], target_year: int) -> Dict[str, Any]:
    """Find which Mahadasha and Antardasha are active in a specific target year."""
    target_dt = datetime.date(target_year, 6, 15)
    target_iso = target_dt.isoformat()
    
    found_maha = None
    for m in timeline:
        if m["start_date"][:4] <= str(target_year) <= m["end_date"][:4] or (m["start_date"] <= target_iso <= m["end_date"]):
            found_maha = m
            break

    if not found_maha:
        found_maha = timeline[-1] if target_year > int(timeline[-1]["end_date"][:4]) else timeline[0]

    found_antar = None
    for a in found_maha.get("antardashas", []):
        if a["start_date"][:4] <= str(target_year) <= a["end_date"][:4] or (a["start_date"] <= target_iso <= a["end_date"]):
            found_antar = a
            break
            
    if not found_antar and found_maha.get("antardashas"):
        found_antar = found_maha["antardashas"][0]

    return {
        "target_year": target_year,
        "mahadasha": {
            "planet": found_maha["planet"],
            "planet_name": found_maha["planet_name"],
            "start_date": found_maha["start_date"],
            "end_date": found_maha["end_date"],
            "color": found_maha["color"],
        },
        "antardasha": {
            "planet": found_antar["planet"] if found_antar else "N/A",
            "planet_name": found_antar["planet_name"] if found_antar else "N/A",
            "combination": found_antar["combination"] if found_antar else "N/A",
            "start_date": found_antar["start_date"] if found_antar else "N/A",
            "end_date": found_antar["end_date"] if found_antar else "N/A",
            "color": found_antar["color"] if found_antar else "#F59E0B",
        } if found_antar else None
    }
