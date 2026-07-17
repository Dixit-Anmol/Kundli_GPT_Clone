"""
Divisional Chart (Varga) computation for Vedic Astrology.

Given a planet's sidereal longitude (0-360), each function returns the
sign index (0-11) where the planet lands in that particular division.

All formulas follow standard Parashari rules from Brihat Parashara
Hora Shastra (BPHS).
"""

from services.astrology.planets import ZODIAC_SIGNS


# ---------------------------------------------------------------------------
# Generic regular-division helper
# ---------------------------------------------------------------------------

def _regular_varga(longitude: float, division: int) -> int:
    """
    For a regular Varga where each sign is divided into `division` equal
    parts, compute the resulting sign index (0-11).

    The sub-division index within the sign determines how many signs
    forward from the natal sign the planet moves:

        sub = int((degree_in_sign / 30) * division)
        result_sign = (natal_sign + sub) % 12
    """
    sign_idx = int(longitude // 30)
    degree_in_sign = longitude % 30.0
    sub = int((degree_in_sign / 30.0) * division)
    return (sign_idx + sub) % 12


# ---------------------------------------------------------------------------
# D1 — Rashi (identity; no transformation)
# ---------------------------------------------------------------------------

def compute_d1(longitude: float) -> int:
    """D1 Rashi chart — planet stays in its natal sign."""
    return int(longitude // 30) % 12


# ---------------------------------------------------------------------------
# D2 — Hora
# ---------------------------------------------------------------------------

def compute_d2(longitude: float) -> int:
    """
    D2 Hora chart.
    First half (0-15°) of odd signs → Leo (4), second half → Cancer (3).
    First half of even signs → Cancer (3), second half → Leo (4).
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    is_odd_sign = (sign_idx % 2 == 0)  # 0-indexed: Aries=0 is odd sign
    first_half = degree < 15.0

    if is_odd_sign:
        return 4 if first_half else 3   # Leo / Cancer
    else:
        return 3 if first_half else 4   # Cancer / Leo


# ---------------------------------------------------------------------------
# D4 — Chaturthamsa (Property / Fortune)
# ---------------------------------------------------------------------------

def compute_d4(longitude: float) -> int:
    """D4 Chaturthamsa — regular 4-division."""
    return _regular_varga(longitude, 4)


# ---------------------------------------------------------------------------
# D7 — Saptamsa (Children / Progeny)
# ---------------------------------------------------------------------------

def compute_d7(longitude: float) -> int:
    """
    D7 Saptamsa.
    Odd signs: count from the same sign.
    Even signs: count from the 7th sign.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 7)
    is_odd = (sign_idx % 2 == 0)  # 0-indexed
    if is_odd:
        return (sign_idx + sub) % 12
    else:
        return (sign_idx + 6 + sub) % 12


# ---------------------------------------------------------------------------
# D9 — Navamsa (Spouse / Dharma)
# ---------------------------------------------------------------------------

def compute_d9(longitude: float) -> int:
    """
    D9 Navamsa — the most important divisional chart.
    Fire signs start from Aries, Earth from Capricorn,
    Air from Libra, Water from Cancer.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    navamsa_num = int(degree / (30.0 / 9.0))  # 0-8

    # Element of the natal sign determines the starting sign
    element = sign_idx % 4   # 0=Fire, 1=Earth, 2=Air, 3=Water
    start_signs = {0: 0, 1: 9, 2: 6, 3: 3}  # Aries, Capricorn, Libra, Cancer
    return (start_signs[element] + navamsa_num) % 12


# ---------------------------------------------------------------------------
# D10 — Dasamsa (Career / Profession)
# ---------------------------------------------------------------------------

def compute_d10(longitude: float) -> int:
    """
    D10 Dasamsa.
    Odd signs: count from the same sign.
    Even signs: count from the 9th sign from it.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 10)
    is_odd = (sign_idx % 2 == 0)
    if is_odd:
        return (sign_idx + sub) % 12
    else:
        return (sign_idx + 8 + sub) % 12


# ---------------------------------------------------------------------------
# D12 — Dwadasamsa (Parents)
# ---------------------------------------------------------------------------

def compute_d12(longitude: float) -> int:
    """D12 Dwadasamsa — regular 12-division (cycles through all 12 signs)."""
    return _regular_varga(longitude, 12)


# ---------------------------------------------------------------------------
# D16 — Shodasamsa (Vehicles / Luxury / Happiness)
# ---------------------------------------------------------------------------

def compute_d16(longitude: float) -> int:
    """
    D16 Shodasamsa.
    Moveable signs start from Aries, Fixed from Leo, Dual from Sagittarius.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 16)

    modality = sign_idx % 3   # 0=Moveable, 1=Fixed, 2=Dual
    start_signs = {0: 0, 1: 4, 2: 8}  # Aries, Leo, Sagittarius
    return (start_signs[modality] + sub) % 12


# ---------------------------------------------------------------------------
# D20 — Vimsamsa (Spirituality / Upasana)
# ---------------------------------------------------------------------------

def compute_d20(longitude: float) -> int:
    """
    D20 Vimsamsa.
    Moveable signs start from Aries, Fixed from Sagittarius, Dual from Leo.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 20)

    modality = sign_idx % 3
    start_signs = {0: 0, 1: 8, 2: 4}  # Aries, Sagittarius, Leo
    return (start_signs[modality] + sub) % 12


# ---------------------------------------------------------------------------
# D24 — Chaturvimsamsa (Education / Learning)
# ---------------------------------------------------------------------------

def compute_d24(longitude: float) -> int:
    """
    D24 Chaturvimsamsa.
    Odd signs start from Leo, Even signs start from Cancer.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 24)
    is_odd = (sign_idx % 2 == 0)

    start = 4 if is_odd else 3  # Leo / Cancer
    return (start + sub) % 12


# ---------------------------------------------------------------------------
# D27 — Saptavimsamsa (Strength / Stamina)
# ---------------------------------------------------------------------------

def compute_d27(longitude: float) -> int:
    """
    D27 Saptavimsamsa.
    Fire signs start from Aries, Earth from Cancer, Air from Libra,
    Water from Capricorn.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 27)

    element = sign_idx % 4
    start_signs = {0: 0, 1: 3, 2: 6, 3: 9}
    return (start_signs[element] + sub) % 12


# ---------------------------------------------------------------------------
# D30 — Trimsamsa (Misfortune / Health)
# ---------------------------------------------------------------------------

def compute_d30(longitude: float) -> int:
    """
    D30 Trimsamsa — irregular division for odd and even signs.

    Odd signs: 0-5° Mars, 5-10° Saturn, 10-18° Jupiter, 18-25° Mercury, 25-30° Venus
    Even signs: 0-5° Venus, 5-12° Mercury, 12-20° Jupiter, 20-25° Saturn, 25-30° Mars

    Returns the sign ruled by the Trimsamsa lord (Aries for Mars, etc.).
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    is_odd = (sign_idx % 2 == 0)

    lord_to_sign = {
        "mars": 0,      # Aries
        "saturn": 10,   # Aquarius
        "jupiter": 8,   # Sagittarius
        "mercury": 2,   # Gemini
        "venus": 1,     # Taurus
    }

    if is_odd:
        if degree < 5:
            lord = "mars"
        elif degree < 10:
            lord = "saturn"
        elif degree < 18:
            lord = "jupiter"
        elif degree < 25:
            lord = "mercury"
        else:
            lord = "venus"
    else:
        if degree < 5:
            lord = "venus"
        elif degree < 12:
            lord = "mercury"
        elif degree < 20:
            lord = "jupiter"
        elif degree < 25:
            lord = "saturn"
        else:
            lord = "mars"

    return lord_to_sign[lord]


# ---------------------------------------------------------------------------
# D40 — Khavedamsa (Auspicious / Inauspicious Effects)
# ---------------------------------------------------------------------------

def compute_d40(longitude: float) -> int:
    """
    D40 Khavedamsa.
    Odd signs start from Aries, Even signs start from Libra.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 40)
    is_odd = (sign_idx % 2 == 0)

    start = 0 if is_odd else 6  # Aries / Libra
    return (start + sub) % 12


# ---------------------------------------------------------------------------
# D45 — Akshavedamsa (General Indications)
# ---------------------------------------------------------------------------

def compute_d45(longitude: float) -> int:
    """
    D45 Akshavedamsa.
    Moveable signs start from Aries, Fixed from Leo, Dual from Sagittarius.
    """
    sign_idx = int(longitude // 30)
    degree = longitude % 30.0
    sub = int((degree / 30.0) * 45)

    modality = sign_idx % 3
    start_signs = {0: 0, 1: 4, 2: 8}
    return (start_signs[modality] + sub) % 12


# ---------------------------------------------------------------------------
# D60 — Shashtiamsa (Past Life Karma / Very Fine Tuning)
# ---------------------------------------------------------------------------

def compute_d60(longitude: float) -> int:
    """D60 Shashtiamsa — regular 60-division."""
    return _regular_varga(longitude, 60)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

VARGA_FUNCTIONS = {
    "D1": compute_d1,
    "D2": compute_d2,
    "D4": compute_d4,
    "D7": compute_d7,
    "D9": compute_d9,
    "D10": compute_d10,
    "D12": compute_d12,
    "D16": compute_d16,
    "D20": compute_d20,
    "D24": compute_d24,
    "D27": compute_d27,
    "D30": compute_d30,
    "D40": compute_d40,
    "D45": compute_d45,
    "D60": compute_d60,
}

ALL_VARGA_NAMES = list(VARGA_FUNCTIONS.keys())


def compute_varga_position(longitude: float, varga_name: str) -> int:
    """
    Compute the sign index (0-11) for a planet in the given Varga chart.
    Raises KeyError if varga_name is not recognised.
    """
    return VARGA_FUNCTIONS[varga_name](longitude)


def get_varga_sign_name(longitude: float, varga_name: str) -> str:
    """Return the zodiac sign name for the planet in the given Varga."""
    idx = compute_varga_position(longitude, varga_name)
    return ZODIAC_SIGNS[idx]
