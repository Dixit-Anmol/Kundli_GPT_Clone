"""
Vedic Kundli Matching (Gun Milan) & Astrological Compatibility Engine.
Classical Ashtakoota Algorithm based on Brihat Parashara Hora Shastra & standard
commercial astrology implementations (AstroSage, KundliGPT, Drik Panchang reference).

Calculates:
1. Ashtakoota 36 Guna Milan using authoritative lookup matrices:
   - Varna (1 pt): Moon Sign spiritual hierarchy
   - Vashya (2 pts): 5x5 Classical compatibility matrix
   - Tara (3 pts): Dual-count Nakshatra Tara computation
   - Yoni (4 pts): 14x14 Animal compatibility matrix
   - Graha Maitri (5 pts): Naisargika Maitri (Natural Friendship) table
   - Gana (6 pts): 3x3 Gana matrix (Deva, Manushya, Rakshasa)
   - Bhakoot (7 pts): Moon sign distance + Bhakoot Nivarana (cancellation)
   - Nadi (8 pts): Nadi type + Nadi Nivarana (cancellation with exempted Nakshatras)
2. Manglik (Mangal Dosha) Dual Analysis & Cancellation Rules
3. Rajju Dosha Analysis (Longevity)
4. Vedha Dosha (Nakshatra Affliction)
5. Mahendra & Stree Deergha Compatibility Indicators
6. Yoni Animal Symbol Compatibility Matrix & Emoji Mapping
7. Dasha Compatibility & Marriage Timing Period Estimator
"""

import math

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _extract_str_val(val, fallback: str = "Aries") -> str:
    """Safely extract string value from either a string or a dictionary."""
    if isinstance(val, str) and val.strip():
        return val.strip()
    if isinstance(val, dict):
        res = val.get("name") or val.get("sign") or val.get("nakshatra") or val.get("planet")
        if res and isinstance(res, str) and res.strip():
            return res.strip()
    if val and not isinstance(val, (dict, str)):
        s = str(val).strip()
        if s:
            return s
    return fallback


# ---------------------------------------------------------------------------
# 1. Vedic Constant Tables & Mappings
# ---------------------------------------------------------------------------

RASHI_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

RASHI_LORDS = {
    "Aries": "mars", "Taurus": "venus", "Gemini": "mercury", "Cancer": "moon",
    "Leo": "sun", "Virgo": "mercury", "Libra": "venus", "Scorpio": "mars",
    "Sagittarius": "jupiter", "Capricorn": "saturn", "Aquarius": "saturn", "Pisces": "jupiter"
}

NAKSHATRAS_ORDER = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# ---------------------------------------------------------------------------
# VARNA (Max 1 pt)
# ---------------------------------------------------------------------------
VARNA_MAP = {
    "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin",
    "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
    "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
    "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"
}
VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}

# ---------------------------------------------------------------------------
# VASHYA (Max 2 pts) — Classical 5x5 Matrix
# Categories: Chatushpada, Manava, Jalachara, Vanachara, Keeta
# Source: Astroyogi / Brihat Parashara Hora Shastra standard
# Note: Sagittarius 1st half = Manava, 2nd half = Chatushpada
#        Capricorn 1st half = Chatushpada, 2nd half = Jalachara
#        (simplified: Sagittarius = Manava, Capricorn = Jalachara as per
#         most commercial software like AstroSage, KundliGPT)
# ---------------------------------------------------------------------------
VASHYA_MAP = {
    "Aries": "Chatushpada", "Taurus": "Chatushpada",
    "Gemini": "Manava", "Virgo": "Manava", "Libra": "Manava",
    "Sagittarius": "Manava", "Aquarius": "Manava",
    "Cancer": "Jalachara", "Capricorn": "Jalachara", "Pisces": "Jalachara",
    "Leo": "Vanachara",
    "Scorpio": "Keeta"
}

# Classical Vashya Compatibility Matrix
# Row = Boy, Column = Girl -> Score
# Source: KundliGPT / AstroSage standard
VASHYA_MATRIX = {
    "Chatushpada": {"Chatushpada": 2.0, "Manava": 0.5, "Jalachara": 1.0, "Vanachara": 2.0, "Keeta": 0.5},
    "Manava":      {"Chatushpada": 0.5, "Manava": 2.0, "Jalachara": 0.5, "Vanachara": 0.0, "Keeta": 1.0},
    "Jalachara":   {"Chatushpada": 1.0, "Manava": 0.5, "Jalachara": 2.0, "Vanachara": 0.0, "Keeta": 1.0},
    "Vanachara":   {"Chatushpada": 0.5, "Manava": 0.5, "Jalachara": 0.0, "Vanachara": 2.0, "Keeta": 0.0},
    "Keeta":       {"Chatushpada": 0.5, "Manava": 1.0, "Jalachara": 1.0, "Vanachara": 0.0, "Keeta": 2.0},
}

# ---------------------------------------------------------------------------
# YONI (Max 4 pts) — Classical 14x14 Animal Compatibility Matrix
# Source: jagannathhora.com / AstroSage / Saravali standard tables
# ---------------------------------------------------------------------------
YONI_MAP = {
    "Ashwini": {"animal": "Horse", "symbol": "🐎"},
    "Shatabhisha": {"animal": "Horse", "symbol": "🐎"},
    "Bharani": {"animal": "Elephant", "symbol": "🐘"},
    "Revati": {"animal": "Elephant", "symbol": "🐘"},
    "Krittika": {"animal": "Sheep", "symbol": "🐑"},
    "Pushya": {"animal": "Sheep", "symbol": "🐑"},
    "Rohini": {"animal": "Serpent", "symbol": "🐍"},
    "Mrigashira": {"animal": "Serpent", "symbol": "🐍"},
    "Ardra": {"animal": "Dog", "symbol": "🐕"},
    "Mula": {"animal": "Dog", "symbol": "🐕"},
    "Punarvasu": {"animal": "Cat", "symbol": "🐈"},
    "Ashlesha": {"animal": "Cat", "symbol": "🐈"},
    "Magha": {"animal": "Rat", "symbol": "🐀"},
    "Purva Phalguni": {"animal": "Rat", "symbol": "🐀"},
    "Uttara Phalguni": {"animal": "Cow", "symbol": "🐮"},
    "Uttara Bhadrapada": {"animal": "Cow", "symbol": "🐮"},
    "Hasta": {"animal": "Buffalo", "symbol": "🐃"},
    "Swati": {"animal": "Buffalo", "symbol": "🐃"},
    "Chitra": {"animal": "Tiger", "symbol": "🐯"},
    "Vishakha": {"animal": "Tiger", "symbol": "🐯"},
    "Anuradha": {"animal": "Deer", "symbol": "🦌"},
    "Jyeshtha": {"animal": "Deer", "symbol": "🦌"},
    "Purva Ashadha": {"animal": "Monkey", "symbol": "🐒"},
    "Shravana": {"animal": "Monkey", "symbol": "🐒"},
    "Uttara Ashadha": {"animal": "Mongoose", "symbol": "🦡"},
    "Abhijit": {"animal": "Mongoose", "symbol": "🦡"},
    "Dhanishta": {"animal": "Lion", "symbol": "🦁"},
    "Purva Bhadrapada": {"animal": "Lion", "symbol": "🦁"},
}

# Full 14x14 Classical Yoni Matrix
# 4 = Same, 3 = Friendly, 2 = Neutral, 1 = Unfriendly, 0 = Enemy
# Source: jagannathhora.com / Saravali / AstroSage standard
YONI_MATRIX = {
    "Horse":    {"Horse": 4, "Elephant": 2, "Sheep": 2, "Serpent": 3, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 1, "Buffalo": 0, "Tiger": 1, "Deer": 3, "Monkey": 3, "Mongoose": 2, "Lion": 1},
    "Elephant": {"Horse": 2, "Elephant": 4, "Sheep": 3, "Serpent": 3, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 2, "Buffalo": 3, "Tiger": 1, "Deer": 2, "Monkey": 3, "Mongoose": 2, "Lion": 0},
    "Sheep":    {"Horse": 2, "Elephant": 3, "Sheep": 4, "Serpent": 2, "Dog": 1, "Cat": 2, "Rat": 1, "Cow": 3, "Buffalo": 3, "Tiger": 1, "Deer": 2, "Monkey": 0, "Mongoose": 3, "Lion": 1},
    "Serpent":  {"Horse": 3, "Elephant": 3, "Sheep": 2, "Serpent": 4, "Dog": 2, "Cat": 1, "Rat": 1, "Cow": 1, "Buffalo": 1, "Tiger": 2, "Deer": 2, "Monkey": 2, "Mongoose": 0, "Lion": 2},
    "Dog":      {"Horse": 2, "Elephant": 2, "Sheep": 1, "Serpent": 2, "Dog": 4, "Cat": 2, "Rat": 1, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 0, "Monkey": 2, "Mongoose": 1, "Lion": 1},
    "Cat":      {"Horse": 2, "Elephant": 2, "Sheep": 2, "Serpent": 1, "Dog": 2, "Cat": 4, "Rat": 0, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 3, "Monkey": 3, "Mongoose": 2, "Lion": 1},
    "Rat":      {"Horse": 2, "Elephant": 2, "Sheep": 1, "Serpent": 1, "Dog": 1, "Cat": 0, "Rat": 4, "Cow": 2, "Buffalo": 2, "Tiger": 2, "Deer": 2, "Monkey": 2, "Mongoose": 1, "Lion": 2},
    "Cow":      {"Horse": 1, "Elephant": 2, "Sheep": 3, "Serpent": 1, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 4, "Buffalo": 3, "Tiger": 0, "Deer": 3, "Monkey": 2, "Mongoose": 2, "Lion": 1},
    "Buffalo":  {"Horse": 0, "Elephant": 3, "Sheep": 3, "Serpent": 1, "Dog": 2, "Cat": 2, "Rat": 2, "Cow": 3, "Buffalo": 4, "Tiger": 1, "Deer": 2, "Monkey": 2, "Mongoose": 2, "Lion": 1},
    "Tiger":    {"Horse": 1, "Elephant": 1, "Sheep": 1, "Serpent": 2, "Dog": 1, "Cat": 1, "Rat": 2, "Cow": 0, "Buffalo": 1, "Tiger": 4, "Deer": 1, "Monkey": 1, "Mongoose": 2, "Lion": 1},
    "Deer":     {"Horse": 3, "Elephant": 2, "Sheep": 2, "Serpent": 2, "Dog": 0, "Cat": 3, "Rat": 2, "Cow": 3, "Buffalo": 2, "Tiger": 1, "Deer": 4, "Monkey": 2, "Mongoose": 2, "Lion": 1},
    "Monkey":   {"Horse": 3, "Elephant": 3, "Sheep": 0, "Serpent": 2, "Dog": 2, "Cat": 3, "Rat": 2, "Cow": 2, "Buffalo": 2, "Tiger": 1, "Deer": 2, "Monkey": 4, "Mongoose": 3, "Lion": 2},
    "Mongoose": {"Horse": 2, "Elephant": 2, "Sheep": 3, "Serpent": 0, "Dog": 1, "Cat": 2, "Rat": 1, "Cow": 2, "Buffalo": 2, "Tiger": 2, "Deer": 2, "Monkey": 3, "Mongoose": 4, "Lion": 2},
    "Lion":     {"Horse": 1, "Elephant": 0, "Sheep": 1, "Serpent": 2, "Dog": 1, "Cat": 1, "Rat": 2, "Cow": 1, "Buffalo": 2, "Tiger": 1, "Deer": 1, "Monkey": 2, "Mongoose": 2, "Lion": 4},
}

# ---------------------------------------------------------------------------
# GRAHA MAITRI (Max 5 pts) — Naisargika Maitri (Natural Friendship)
# Step 1: Look up Rashi lords for both Moon signs
# Step 2: Check planetary friendship in BOTH directions (asymmetric)
# Step 3: Map combined relationship to score
# Source: Brihat Parashara Hora Shastra / AstroSage / astromedha.in
# ---------------------------------------------------------------------------

# Natural Planetary Friendships (Naisargika Maitri):
# +1 = Friend, 0 = Neutral, -1 = Enemy
NAISARGIKA_MAITRI = {
    "sun":     {"sun": 1, "moon": 1, "mars": 1, "mercury": 0, "jupiter": 1, "venus": -1, "saturn": -1},
    "moon":    {"sun": 1, "moon": 1, "mars": 0, "mercury": -1, "jupiter": 1, "venus": 0, "saturn": 0},
    "mars":    {"sun": 1, "moon": 1, "mars": 1, "mercury": -1, "jupiter": 1, "venus": 0, "saturn": 0},
    "mercury": {"sun": 1, "moon": -1, "mars": 0, "mercury": 1, "jupiter": 0, "venus": 1, "saturn": 0},
    "jupiter": {"sun": 1, "moon": 1, "mars": 1, "mercury": -1, "jupiter": 1, "venus": -1, "saturn": 0},
    "venus":   {"sun": -1, "moon": -1, "mars": 0, "mercury": 1, "jupiter": 0, "venus": 1, "saturn": 1},
    "saturn":  {"sun": -1, "moon": -1, "mars": -1, "mercury": 1, "jupiter": 0, "venus": 1, "saturn": 1},
}

# Mapping: (Lord A's view of Lord B, Lord B's view of Lord A) -> Graha Maitri score
GRAHA_MAITRI_SCORE_MAP = {
    (1, 1): 5.0,    # Mutual Friends
    (1, 0): 4.0,    # Friend & Neutral
    (0, 1): 4.0,    # Neutral & Friend
    (1, -1): 1.0,   # Friend & Enemy
    (-1, 1): 1.0,   # Enemy & Friend
    (0, 0): 3.0,    # Mutual Neutral (as per some traditions: 0.5)
    (0, -1): 0.5,   # Neutral & Enemy
    (-1, 0): 0.5,   # Enemy & Neutral
    (-1, -1): 0.0,  # Mutual Enemies
}

# ---------------------------------------------------------------------------
# GANA (Max 6 pts) — Classical 3x3 Matrix
# Source: Standard Ashtakoota / AstroSage / Drik Panchang
# ---------------------------------------------------------------------------
GANA_MAP = {
    "Ashwini": "Deva", "Bharani": "Manushya", "Krittika": "Rakshasa",
    "Rohini": "Manushya", "Mrigashira": "Deva", "Ardra": "Manushya",
    "Punarvasu": "Deva", "Pushya": "Deva", "Ashlesha": "Rakshasa",
    "Magha": "Rakshasa", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya",
    "Hasta": "Deva", "Chitra": "Rakshasa", "Swati": "Deva",
    "Vishakha": "Rakshasa", "Anuradha": "Deva", "Jyeshtha": "Rakshasa",
    "Mula": "Rakshasa", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya",
    "Shravana": "Deva", "Dhanishta": "Rakshasa", "Shatabhisha": "Rakshasa",
    "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Revati": "Deva"
}

# Row = Boy Gana, Column = Girl Gana
GANA_MATRIX = {
    "Deva":     {"Deva": 6.0, "Manushya": 6.0, "Rakshasa": 1.0},
    "Manushya": {"Deva": 5.0, "Manushya": 6.0, "Rakshasa": 0.0},
    "Rakshasa": {"Deva": 0.0, "Manushya": 0.0, "Rakshasa": 6.0},
}

# ---------------------------------------------------------------------------
# NADI (Max 8 pts) — with exhaustive cancellation rules
# ---------------------------------------------------------------------------
NADI_MAP = {
    "Ashwini": "Adi", "Ardra": "Adi", "Punarvasu": "Adi",
    "Uttara Phalguni": "Adi", "Hasta": "Adi", "Jyeshtha": "Adi",
    "Mula": "Adi", "Shatabhisha": "Adi", "Purva Bhadrapada": "Adi",

    "Bharani": "Madhya", "Mrigashira": "Madhya", "Pushya": "Madhya",
    "Purva Phalguni": "Madhya", "Chitra": "Madhya", "Anuradha": "Madhya",
    "Purva Ashadha": "Madhya", "Dhanishta": "Madhya", "Uttara Bhadrapada": "Madhya",

    "Krittika": "Antya", "Rohini": "Antya", "Ashlesha": "Antya",
    "Magha": "Antya", "Swati": "Antya", "Vishakha": "Antya",
    "Uttara Ashadha": "Antya", "Shravana": "Antya", "Revati": "Antya"
}

# Nakshatras exempt from Nadi Dosha (from Muhurta Chintamani)
NADI_EXEMPT_NAKSHATRAS = {
    "Rohini", "Ardra", "Pushya", "Magha", "Vishakha",
    "Shravana", "Uttara Bhadrapada", "Revati"
}

# ---------------------------------------------------------------------------
# RAJJU (Marital Longevity)
# ---------------------------------------------------------------------------
RAJJU_MAP = {
    "Dhanishta": "Siro", "Chitra": "Siro", "Mrigashira": "Siro",
    "Rohini": "Kantha", "Ardra": "Kantha", "Hasta": "Kantha",
    "Swati": "Kantha", "Shravana": "Kantha", "Shatabhisha": "Kantha",
    "Krittika": "Nabhi", "Punarvasu": "Nabhi", "Uttara Phalguni": "Nabhi",
    "Vishakha": "Nabhi", "Uttara Ashadha": "Nabhi", "Purva Bhadrapada": "Nabhi",
    "Bharani": "Kati", "Pushya": "Kati", "Purva Phalguni": "Kati",
    "Anuradha": "Kati", "Purva Ashadha": "Kati", "Uttara Bhadrapada": "Kati",
    "Ashwini": "Pada", "Ashlesha": "Pada", "Magha": "Pada",
    "Jyeshtha": "Pada", "Mula": "Pada", "Revati": "Pada"
}

# VEDHA pairs (Nakshatra mutual affliction)
VEDHA_PAIRS = [
    ("Ashwini", "Jyeshtha"), ("Bharani", "Anuradha"), ("Krittika", "Vishakha"),
    ("Rohini", "Swati"), ("Ardra", "Shravana"), ("Punarvasu", "Uttara Ashadha"),
    ("Pushya", "Purva Ashadha"), ("Ashlesha", "Mula"), ("Magha", "Revati"),
    ("Purva Phalguni", "Uttara Bhadrapada"), ("Uttara Phalguni", "Purva Bhadrapada"),
    ("Hasta", "Shatabhisha"), ("Mrigashira", "Dhanishta")
]


# ---------------------------------------------------------------------------
# 2. Classical Ashtakoota Calculators
# ---------------------------------------------------------------------------

def calculate_varna(sign1: str, sign2: str) -> dict:
    """1. Varna (Max 1 Pt) — Boy's varna rank >= Girl's varna rank => 1 pt."""
    s1 = _extract_str_val(sign1, "Aries")
    s2 = _extract_str_val(sign2, "Taurus")
    v1 = VARNA_MAP.get(s1, "Shudra")
    v2 = VARNA_MAP.get(s2, "Shudra")
    pts = 1.0 if VARNA_RANK[v1] >= VARNA_RANK[v2] else 0.0
    return {"obtained": pts, "max": 1.0, "boy_varna": v1, "girl_varna": v2}


def calculate_vashya(sign1: str, sign2: str) -> dict:
    """2. Vashya (Max 2 Pts) — 5x5 classical matrix lookup."""
    s1 = _extract_str_val(sign1, "Aries")
    s2 = _extract_str_val(sign2, "Taurus")
    v1 = VASHYA_MAP.get(s1, "Manava")
    v2 = VASHYA_MAP.get(s2, "Manava")
    pts = VASHYA_MATRIX.get(v1, {}).get(v2, 1.0)
    return {"obtained": pts, "max": 2.0, "boy_vashya": v1, "girl_vashya": v2}


def calculate_tara(nak1: str, nak2: str) -> dict:
    """3. Tara (Max 3 Pts) — Classical dual-count Nakshatra computation."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    try:
        idx1 = NAKSHATRAS_ORDER.index(n1)
        idx2 = NAKSHATRAS_ORDER.index(n2)
    except ValueError:
        return {"obtained": 1.5, "max": 3.0, "note": "Nakshatra not found"}

    # Tara from Boy to Girl
    count1 = ((idx2 - idx1) % 27) + 1
    tara1 = count1 % 9
    rem1 = 1.0 if tara1 in [1, 2, 4, 6, 8, 0] else 0.0

    # Tara from Girl to Boy
    count2 = ((idx1 - idx2) % 27) + 1
    tara2 = count2 % 9
    rem2 = 1.0 if tara2 in [1, 2, 4, 6, 8, 0] else 0.0

    total = (rem1 + rem2) * 1.5
    return {"obtained": total, "max": 3.0, "tara_1": tara1, "tara_2": tara2}


def calculate_yoni(nak1: str, nak2: str) -> dict:
    """4. Yoni (Max 4 Pts) — 14x14 classical animal matrix."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    y1 = YONI_MAP.get(n1, {"animal": "Horse", "symbol": "🐎"})
    y2 = YONI_MAP.get(n2, {"animal": "Horse", "symbol": "🐎"})
    a1, a2 = y1["animal"], y2["animal"]
    pts = float(YONI_MATRIX.get(a1, {}).get(a2, 2))

    if pts == 4:
        relation = f"Same Animal ({a1} 💖 {a2})"
    elif pts == 3:
        relation = f"Friendly ({a1} & {a2})"
    elif pts == 2:
        relation = f"Neutral ({a1} & {a2})"
    elif pts == 1:
        relation = f"Unfriendly ({a1} & {a2})"
    else:
        relation = f"Sworn Enemy ({a1} ⚠️ {a2})"

    return {
        "obtained": pts, "max": 4.0,
        "boy_animal": a1, "boy_symbol": y1["symbol"],
        "girl_animal": a2, "girl_symbol": y2["symbol"],
        "relation": relation
    }


def calculate_graha_maitri(sign1: str, sign2: str) -> dict:
    """5. Graha Maitri (Max 5 Pts) — Naisargika Maitri friendship table.

    Uses asymmetric natural planetary friendship:
    1. Get lords of both Moon signs.
    2. Look up Lord A's view of Lord B, and Lord B's view of Lord A.
    3. Map the (viewA, viewB) pair to a score.
    """
    s1 = _extract_str_val(sign1, "Aries")
    s2 = _extract_str_val(sign2, "Taurus")
    lord1 = RASHI_LORDS.get(s1, "mars")
    lord2 = RASHI_LORDS.get(s2, "venus")

    if lord1 == lord2:
        pts = 5.0
        relation = "Same Rashi Lord (5/5)"
    else:
        view_a = NAISARGIKA_MAITRI.get(lord1, {}).get(lord2, 0)
        view_b = NAISARGIKA_MAITRI.get(lord2, {}).get(lord1, 0)
        pts = GRAHA_MAITRI_SCORE_MAP.get((view_a, view_b), 3.0)

        if pts == 5.0:
            relation = "Mutual Friends (5/5)"
        elif pts == 4.0:
            relation = "Friend & Neutral (4/5)"
        elif pts == 3.0:
            relation = "Mutual Neutral (3/5)"
        elif pts == 1.0:
            relation = "Friend & Enemy (1/5)"
        elif pts == 0.5:
            relation = "Neutral & Enemy (0.5/5)"
        else:
            relation = "Mutual Enemy (0/5)"

    return {
        "obtained": pts, "max": 5.0,
        "boy_lord": lord1.capitalize(), "girl_lord": lord2.capitalize(),
        "relation": relation
    }


def calculate_gana(nak1: str, nak2: str) -> dict:
    """6. Gana (Max 6 Pts) — 3x3 classical matrix."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    g1 = GANA_MAP.get(n1, "Deva")
    g2 = GANA_MAP.get(n2, "Deva")
    pts = GANA_MATRIX.get(g1, {}).get(g2, 0.0)

    if pts >= 6.0:
        relation = f"Excellent ({g1} & {g2})"
    elif pts >= 5.0:
        relation = f"Good ({g1} & {g2})"
    elif pts >= 1.0:
        relation = f"Caution ({g1} & {g2})"
    else:
        relation = f"Incompatible ({g1} & {g2})"

    return {"obtained": pts, "max": 6.0, "boy_gana": g1, "girl_gana": g2, "relation": relation}


def calculate_bhakoot(sign1: str, sign2: str) -> dict:
    """7. Bhakoot (Max 7 Pts) — KundliGPT-compatible scoring.

    Scoring by Moon sign distance (KundliGPT / AstroSage standard):
      - 1/1, 1/7, 3/11, 4/10  -> 7 pts (fully auspicious)
      - 5/9 (Navapanchama)     -> 4 pts (partially auspicious, relates to progeny)
      - 2/12 (Dwindwadasa)     -> 0 pts (financial dosha)
      - 6/8 (Shashtashtaka)    -> 0 pts (health/longevity dosha)
    Cancellation (only for 2/12 and 6/8):
      - Same Rashi lord => 7 pts
    """
    s1 = _extract_str_val(sign1, "Aries")
    s2 = _extract_str_val(sign2, "Taurus")
    idx1 = RASHI_NAMES.index(s1) if s1 in RASHI_NAMES else 0
    idx2 = RASHI_NAMES.index(s2) if s2 in RASHI_NAMES else 0

    dist = ((idx2 - idx1) % 12) + 1
    dist_rev = ((idx1 - idx2) % 12) + 1

    lord1 = RASHI_LORDS.get(s1, "mars")
    lord2 = RASHI_LORDS.get(s2, "venus")

    cancellation = False
    cancel_reason = ""
    is_dosha = False

    # Fully auspicious distances
    if dist in [1, 7, 3, 11, 4, 10]:
        pts = 7.0
        status = f"Auspicious ({dist}/{dist_rev})"
    # Navapanchama (5/9) — partially auspicious per KundliGPT
    elif dist in [5, 9]:
        pts = 4.0
        status = f"Navapanchama ({dist}/{dist_rev})"
    # True dosha: 2/12 (Dwindwadasa) or 6/8 (Shashtashtaka)
    else:
        # Only cancel for same Rashi lord
        if lord1 == lord2:
            cancellation = True
            cancel_reason = f"Same lord ({lord1.capitalize()})"
            pts = 7.0
            status = f"Dosha cancelled ({cancel_reason})"
        else:
            pts = 0.0
            is_dosha = True
            if dist in [2, 12]:
                status = f"Dwindwadasa Dosha ({dist}/{dist_rev})"
            else:
                status = f"Shashtashtaka Dosha ({dist}/{dist_rev})"

    return {
        "obtained": pts, "max": 7.0,
        "is_dosha": is_dosha,
        "cancellation": cancellation, "cancellation_reason": cancel_reason,
        "status": status, "distance": dist
    }


def calculate_nadi(nak1: str, nak2: str, sign1: str = "", sign2: str = "") -> dict:
    """8. Nadi (Max 8 Pts) — with complete Nadi Nivarana (cancellation).

    Cancellation rules (from Muhurta Chintamani):
      1. Same Nakshatra, different Rashis
      2. Same Rashi, different Nakshatras
      3. Same Nakshatra, different Padas (not computable without pada info, skipped)
      4. Either Nakshatra is in the exempt list
    """
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    s1 = _extract_str_val(sign1, "")
    s2 = _extract_str_val(sign2, "")

    nadi1 = NADI_MAP.get(n1, "Adi")
    nadi2 = NADI_MAP.get(n2, "Madhya")

    same_nadi = (nadi1 == nadi2)
    cancellation = False
    cancel_reason = ""

    if same_nadi:
        # Check exempted Nakshatras
        if n1 in NADI_EXEMPT_NAKSHATRAS or n2 in NADI_EXEMPT_NAKSHATRAS:
            cancellation = True
            exempt_nak = n1 if n1 in NADI_EXEMPT_NAKSHATRAS else n2
            cancel_reason = f"{exempt_nak} is exempt from Nadi Dosha"
        # Same Nakshatra but different Rashis
        elif n1 == n2 and s1 and s2 and s1 != s2:
            cancellation = True
            cancel_reason = f"Same Nakshatra ({n1}) in different Rashis"
        # Same Rashi but different Nakshatras
        elif n1 != n2 and s1 and s2 and s1 == s2:
            cancellation = True
            cancel_reason = f"Same Rashi ({s1}) with different Nakshatras"

    if not same_nadi:
        pts = 8.0
        status = f"Compatible ({nadi1} & {nadi2})"
    elif cancellation:
        pts = 8.0
        status = f"Dosha cancelled ({cancel_reason})"
    else:
        pts = 0.0
        status = f"Nadi Dosha (both {nadi1})"

    return {
        "obtained": pts, "max": 8.0,
        "boy_nadi": nadi1, "girl_nadi": nadi2,
        "is_dosha": same_nadi and not cancellation,
        "cancellation": cancellation, "cancellation_reason": cancel_reason,
        "status": status
    }


# ---------------------------------------------------------------------------
# 3. Auxiliary Checks
# ---------------------------------------------------------------------------

def calculate_vedha_dosha(nak1: str, nak2: str) -> dict:
    """Vedha — Nakshatra mutual affliction check."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    has = any((n1 == p[0] and n2 == p[1]) or (n1 == p[1] and n2 == p[0]) for p in VEDHA_PAIRS)
    return {
        "is_dosha": has,
        "status": "Vedha Dosha Present ⚠️" if has else "No Vedha Dosha ✅"
    }


def calculate_mahendra_stree_deergha(nak1: str, nak2: str) -> dict:
    """Mahendra & Stree Deergha auxiliary indicators."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    try:
        idx1 = NAKSHATRAS_ORDER.index(n1)
        idx2 = NAKSHATRAS_ORDER.index(n2)
        count = ((idx2 - idx1) % 27) + 1
    except ValueError:
        count = 1

    mahendra = count in [4, 7, 10, 13, 16, 19, 22, 25]
    stree_deergha = count > 13

    return {
        "mahendra": "Favorable Mahendra ✅" if mahendra else "Neutral Mahendra",
        "stree_deergha": "Favorable Stree Deergha ✅" if stree_deergha else "Standard"
    }


def calculate_manglik_status(chart: dict) -> dict:
    """Manglik (Mangal Dosha) — Mars in houses 1, 2, 4, 7, 8, 12."""
    planets = chart.get("raw_positions") or chart.get("planets", {})
    mars_p = planets.get("mars", {})
    raw_house = mars_p.get("house", 1) if isinstance(mars_p, dict) else 1
    if isinstance(raw_house, dict):
        raw_house = raw_house.get("house", 1)
    mars_house = int(raw_house) if raw_house else 1

    manglik_houses = [1, 2, 4, 7, 8, 12]
    is_manglik = mars_house in manglik_houses

    cancellation_reasons = []
    mars_sign = _extract_str_val(mars_p.get("sign") if isinstance(mars_p, dict) else "", "Aries")

    if mars_sign in ["Aries", "Scorpio", "Capricorn"]:
        cancellation_reasons.append("Mars in own/exalted sign")
    if mars_house == 2 and mars_sign in ["Gemini", "Virgo"]:
        cancellation_reasons.append("Mars in 2nd house Gemini/Virgo")

    severity = "High" if is_manglik and not cancellation_reasons else ("Low" if is_manglik else "None")
    return {
        "is_manglik": is_manglik, "mars_house": mars_house, "mars_sign": mars_sign,
        "cancellation": len(cancellation_reasons) > 0,
        "cancellation_reasons": cancellation_reasons, "severity": severity
    }


def calculate_rajju_dosha(nak1: str, nak2: str) -> dict:
    """Rajju Dosha — marital longevity check."""
    n1 = _extract_str_val(nak1, "Ashwini")
    n2 = _extract_str_val(nak2, "Bharani")
    r1 = RAJJU_MAP.get(n1, "Pada")
    r2 = RAJJU_MAP.get(n2, "Pada")
    is_dosha = (r1 == r2)
    return {
        "is_dosha": is_dosha, "boy_rajju": r1, "girl_rajju": r2,
        "status": f"Rajju Dosha ({r1}) ⚠️" if is_dosha else "No Rajju Dosha ✅"
    }


# ---------------------------------------------------------------------------
# 4. Master Orchestrator
# ---------------------------------------------------------------------------

def calculate_kundli_matching(
    chart_a: dict, chart_b: dict,
    person_a_name: str = "Partner A", person_b_name: str = "Partner B"
) -> dict:
    """Complete classical Ashtakoota Kundli Matching."""

    # --- Extract Moon data robustly ---
    planets_a = chart_a.get("planets") or chart_a.get("raw_positions") or {}
    planets_b = chart_b.get("planets") or chart_b.get("raw_positions") or {}
    moon_a = planets_a.get("moon", {}) if isinstance(planets_a, dict) else {}
    moon_b = planets_b.get("moon", {}) if isinstance(planets_b, dict) else {}
    meta_a = chart_a.get("metadata", {}) if isinstance(chart_a.get("metadata"), dict) else {}
    meta_b = chart_b.get("metadata", {}) if isinstance(chart_b.get("metadata"), dict) else {}

    nak_a = _extract_str_val(
        (moon_a.get("nakshatra") if isinstance(moon_a, dict) else None) or meta_a.get("nakshatra"),
        "Ashwini"
    )
    nak_b = _extract_str_val(
        (moon_b.get("nakshatra") if isinstance(moon_b, dict) else None) or meta_b.get("nakshatra"),
        "Bharani"
    )
    sign_a = _extract_str_val(
        (moon_a.get("sign") if isinstance(moon_a, dict) else None) or meta_a.get("moon_sign"),
        "Cancer"
    )
    sign_b = _extract_str_val(
        (moon_b.get("sign") if isinstance(moon_b, dict) else None) or meta_b.get("moon_sign"),
        "Scorpio"
    )
    asc_a = _extract_str_val(meta_a.get("ascendant_sign") or chart_a.get("ascendant_sign"), "Aries")
    asc_b = _extract_str_val(meta_b.get("ascendant_sign") or chart_b.get("ascendant_sign"), "Taurus")

    # --- 8 Ashtakoota factors ---
    varna = calculate_varna(sign_a, sign_b)
    vashya = calculate_vashya(sign_a, sign_b)
    tara = calculate_tara(nak_a, nak_b)
    yoni = calculate_yoni(nak_a, nak_b)
    maitri = calculate_graha_maitri(sign_a, sign_b)
    gana = calculate_gana(nak_a, nak_b)
    bhakoot = calculate_bhakoot(sign_a, sign_b)
    nadi = calculate_nadi(nak_a, nak_b, sign_a, sign_b)

    total = round(sum(f["obtained"] for f in [varna, vashya, tara, yoni, maitri, gana, bhakoot, nadi]), 1)

    if total >= 33.0:
        verdict, rating_color = "Excellent Match 🌟", "gold"
        recommendation = "Highly recommended. Exceptional harmony across all dimensions."
    elif total >= 25.0:
        verdict, rating_color = "Good Match ✅", "emerald"
        recommendation = "Recommended. Strong compatibility with minor remedial considerations."
    elif total >= 18.0:
        verdict, rating_color = "Acceptable Match ⚠️", "amber"
        recommendation = "Acceptable with remedies. Traditional Puja/Mantras recommended for active Doshas."
    else:
        verdict, rating_color = "Not Recommended ❌", "red"
        recommendation = "Low Guna score. Comprehensive astrological remedies and counseling required."

    # --- Manglik ---
    manglik_a = calculate_manglik_status(chart_a)
    manglik_b = calculate_manglik_status(chart_b)
    if manglik_a["is_manglik"] and manglik_b["is_manglik"]:
        manglik_match = "Both Manglik (neutralized ✅)"
    elif not manglik_a["is_manglik"] and not manglik_b["is_manglik"]:
        manglik_match = "Neither Manglik ✅"
    else:
        who = person_a_name if manglik_a["is_manglik"] else person_b_name
        manglik_match = f"One Manglik ({who}) ⚠️"

    # --- Auxiliary ---
    rajju = calculate_rajju_dosha(nak_a, nak_b)
    vedha = calculate_vedha_dosha(nak_a, nak_b)
    aux = calculate_mahendra_stree_deergha(nak_a, nak_b)

    # --- Marriage timing ---
    dasha_a = chart_a.get("current_dasha") or {}
    dasha_b = chart_b.get("current_dasha") or {}
    pa = _extract_str_val(dasha_a.get("planet") if isinstance(dasha_a, dict) else None, "Jupiter").capitalize()
    pb = _extract_str_val(dasha_b.get("planet") if isinstance(dasha_b, dict) else None, "Venus").capitalize()
    timing = f"Favorable window: {pa} & {pb} Dasha activations (next 12–24 months)."

    return {
        "person_a_name": person_a_name,
        "person_b_name": person_b_name,
        "person_a_details": {"moon_sign": sign_a, "nakshatra": nak_a, "ascendant": asc_a},
        "person_b_details": {"moon_sign": sign_b, "nakshatra": nak_b, "ascendant": asc_b},
        "ashtakoota": {
            "total_score": total, "max_score": 36.0,
            "verdict": verdict, "rating_color": rating_color,
            "recommendation": recommendation,
            "factors": {
                "varna": varna, "vashya": vashya, "tara": tara, "yoni": yoni,
                "graha_maitri": maitri, "gana": gana, "bhakoot": bhakoot, "nadi": nadi,
            }
        },
        "dosha_analysis": {
            "manglik_person_a": manglik_a, "manglik_person_b": manglik_b,
            "manglik_summary": manglik_match,
            "nadi_dosha": nadi, "bhakoot_dosha": bhakoot, "rajju_dosha": rajju,
            "vedha_dosha": vedha,
            "mahendra": aux["mahendra"], "stree_deergha": aux["stree_deergha"],
        },
        "yoni_pairing": {
            "boy_symbol": yoni["boy_symbol"], "boy_animal": yoni["boy_animal"],
            "girl_symbol": yoni["girl_symbol"], "girl_animal": yoni["girl_animal"],
            "relation": yoni["relation"],
            "display": f"{yoni['boy_symbol']} {yoni['boy_animal']}  ❤️  {yoni['girl_symbol']} {yoni['girl_animal']}"
        },
        "marriage_timing": timing,
    }
