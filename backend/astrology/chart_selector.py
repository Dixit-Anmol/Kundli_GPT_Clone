"""
Topic-Based Chart Selector.

Never sends all charts to the LLM. Instead, selects the minimum
required divisional charts, dasha, gochar, and strength data
based on the user's query topic.
"""

from typing import Dict, Any, Optional


# ---------------------------------------------------------------------------
# Helper to extract a chart dict from the bundle
# ---------------------------------------------------------------------------

def _extract_chart(bundle: dict, chart_key: str) -> dict:
    """Safely extract a divisional chart from the bundle dict."""
    return bundle.get(chart_key, {})


def _extract_dasha_current(bundle: dict) -> dict:
    """Extract only the current Maha/Antar/Pratyantar periods (not the full timeline)."""
    dasha = bundle.get("dasha", {})
    return {
        "current_mahadasha": dasha.get("current_mahadasha"),
        "current_antardasha": dasha.get("current_antardasha"),
        "current_pratyantar": dasha.get("current_pratyantar"),
    }


def _extract_gochar(bundle: dict) -> dict:
    """Extract current transit data."""
    return bundle.get("gochar", {})


def _extract_yogas(bundle: dict, chart_keys: list = None) -> list:
    """Extract yogas from specified charts (defaults to D1)."""
    if chart_keys is None:
        chart_keys = ["D1"]

    all_yogas = []
    for key in chart_keys:
        chart = bundle.get(key, {})
        yogas = chart.get("yogas", [])
        for y in yogas:
            if y not in all_yogas:
                all_yogas.append(y)
    return all_yogas


def _extract_strengths(bundle: dict) -> dict:
    """Extract shadbala and planet strength from D1."""
    d1 = bundle.get("D1", {})
    return {
        "planet_strength": d1.get("planet_strength", {}),
        "shadbala": bundle.get("shadbala", []),
    }


def _extract_global_metadata(bundle: dict) -> dict:
    """Extract lagna, moon sign, sun sign, karakas, nakshatra."""
    return {
        "lagna": bundle.get("lagna", ""),
        "moon_sign": bundle.get("moon_sign", ""),
        "sun_sign": bundle.get("sun_sign", ""),
        "karakas": bundle.get("karakas", {}),
        "nakshatra": bundle.get("nakshatra", {}),
        "dignity": bundle.get("dignity", {}),
        "ashtakavarga": bundle.get("ashtakavarga", {}),
    }


# ===================================================================
# Topic-specific selectors
# ===================================================================

def get_finance_charts(bundle: dict) -> dict:
    """Finance: D1, D2, D9, D10 + Dasha + Gochar + Yogas + Strengths."""
    return {
        "topic": "Finance",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D2": _extract_chart(bundle, "D2"),
            "D9": _extract_chart(bundle, "D9"),
            "D10": _extract_chart(bundle, "D10"),
        },
        "dasha": _extract_dasha_current(bundle),
        "gochar": _extract_gochar(bundle),
        "yogas": _extract_yogas(bundle, ["D1", "D9"]),
        "strengths": _extract_strengths(bundle),
        **_extract_global_metadata(bundle),
    }


def get_career_charts(bundle: dict) -> dict:
    """Career: D1, D10, D9 + Dasha + Gochar."""
    return {
        "topic": "Career",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D10": _extract_chart(bundle, "D10"),
            "D9": _extract_chart(bundle, "D9"),
        },
        "dasha": _extract_dasha_current(bundle),
        "gochar": _extract_gochar(bundle),
        "yogas": _extract_yogas(bundle, ["D1", "D9"]),
        "strengths": _extract_strengths(bundle),
        **_extract_global_metadata(bundle),
    }


def get_marriage_charts(bundle: dict) -> dict:
    """Marriage: D1, D9 + Dasha + Yogas."""
    return {
        "topic": "Marriage",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D9": _extract_chart(bundle, "D9"),
        },
        "dasha": _extract_dasha_current(bundle),
        "yogas": _extract_yogas(bundle, ["D1", "D9"]),
        "strengths": _extract_strengths(bundle),
        **_extract_global_metadata(bundle),
    }


def get_health_charts(bundle: dict) -> dict:
    """Health: D1, D30, D9 + Dasha + Gochar."""
    return {
        "topic": "Health",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D30": _extract_chart(bundle, "D30"),
            "D9": _extract_chart(bundle, "D9"),
        },
        "dasha": _extract_dasha_current(bundle),
        "gochar": _extract_gochar(bundle),
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_education_charts(bundle: dict) -> dict:
    """Education: D1, D24 + Dasha."""
    return {
        "topic": "Education",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D24": _extract_chart(bundle, "D24"),
        },
        "dasha": _extract_dasha_current(bundle),
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_children_charts(bundle: dict) -> dict:
    """Children: D1, D7 + Dasha."""
    return {
        "topic": "Children",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D7": _extract_chart(bundle, "D7"),
        },
        "dasha": _extract_dasha_current(bundle),
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_property_charts(bundle: dict) -> dict:
    """Property: D1, D4 + Dasha."""
    return {
        "topic": "Property",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D4": _extract_chart(bundle, "D4"),
        },
        "dasha": _extract_dasha_current(bundle),
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_luxury_charts(bundle: dict) -> dict:
    """Luxury: D1, D16."""
    return {
        "topic": "Luxury",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D16": _extract_chart(bundle, "D16"),
        },
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_spirituality_charts(bundle: dict) -> dict:
    """Spirituality: D1, D20."""
    return {
        "topic": "Spirituality",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D20": _extract_chart(bundle, "D20"),
        },
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_parents_charts(bundle: dict) -> dict:
    """Parents: D1, D12."""
    return {
        "topic": "Parents",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D12": _extract_chart(bundle, "D12"),
        },
        "dasha": _extract_dasha_current(bundle),
        "yogas": _extract_yogas(bundle, ["D1"]),
        **_extract_global_metadata(bundle),
    }


def get_general_charts(bundle: dict) -> dict:
    """General Horoscope: D1, D9 + Dasha + Gochar."""
    return {
        "topic": "General Horoscope",
        "charts": {
            "D1": _extract_chart(bundle, "D1"),
            "D9": _extract_chart(bundle, "D9"),
        },
        "dasha": _extract_dasha_current(bundle),
        "gochar": _extract_gochar(bundle),
        "yogas": _extract_yogas(bundle, ["D1", "D9"]),
        "strengths": _extract_strengths(bundle),
        **_extract_global_metadata(bundle),
    }


# ===================================================================
# Dispatcher
# ===================================================================

# Topic → selector function mapping
_TOPIC_MAP = {
    "Finance":             get_finance_charts,
    "Wealth":              get_finance_charts,
    "Career":              get_career_charts,
    "Marriage":            get_marriage_charts,
    "Health":              get_health_charts,
    "Education":           get_education_charts,
    "Children":            get_children_charts,
    "Property":            get_property_charts,
    "Luxury":              get_luxury_charts,
    "Spirituality":        get_spirituality_charts,
    "Parents":             get_parents_charts,
    "Family":              get_parents_charts,
    "General Horoscope":   get_general_charts,
    "Relationships":       get_marriage_charts,
    "Mental Wellbeing":    get_health_charts,
    "Remedies":            get_general_charts,
    "Bhagavad Gita Discussion": get_general_charts,
    "Astrology Explanation":    get_general_charts,
}


def select_charts_for_topic(topic: str, bundle: dict) -> dict:
    """
    Master dispatcher: given a classified topic and a FullChartBundle dict,
    return only the minimum required astrology data for that topic.
    """
    selector = _TOPIC_MAP.get(topic, get_general_charts)
    return selector(bundle)
