"""
Configuration and reference data for the Weather Risk & Outdoor Activity Planner.

Nothing in here talks to the network - it's just constants, thresholds, and
lookup tables used by the rest of the app.
"""

import os

# ---------------------------------------------------------------------------
# Open-Meteo API endpoints (no API key required => https://open-meteo.com)
# ---------------------------------------------------------------------------
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# The specific hourly and daily variables we ask Open-Meteo for. Keeping this
# in one place means every part of the app agrees on what fields to expect.

HOURLY_VARIABLES = [
    "temperature_2m",
    "precipitation_probability",
    "precipitation",
    "wind_speed_10m",
    "weather_code",
    "relative_humidity_2m",
    "uv_index",
]

DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max"
    "weather_code",
    "sunrise",
    "sunset",
    "uv_index_max",
]

REQUEST_TIMEOUT_SECONDS = 10


# ---------------------------------------------------------------------------
# Gemini API (requires a free API key from https://aistudio.google.com)
# ---------------------------------------------------------------------------
GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)


def get_gemini_api_key():
    """
    Look up the Gemini API key from wherever the user configured it.

    Checks, in order:
      1. Streamlit's secrets manager (.streamlit/secrets.toml) - the
         recommended way to store secrets in a Streamlit app.
      2. A plain GEMINI_API_KEY environment variable, as a fallback for
         running the underlying classes outside of Streamlit (e.g. in tests).

    Returns:
        The API key as a string, or None if it isn't configured anywhere.
        None is a valid, expected return value - callers must handle it,
        since the app should degrade gracefully without a key rather than
        crash.
    """
    
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
         # No secrets.toml file, not running inside Streamlit, or any other
        # problem reading secrets - fall through to the environment variable.
        pass
    
    return os.environ.get("GEMINI_API_KEY")


# ---------------------------------------------------------------------------
# Local storage locations (JSON files => storage.py)
# ---------------------------------------------------------------------------

DATA_DIR = "data"
FAVOURITES_FILE = os.path.join(DATA_DIR, "favourites.json")
HISTORY_FILE = os.path.join(DATA_DIR, "search_history.json")
MAX_HISTORY_ENTRIES = 50


# ---------------------------------------------------------------------------
# WMO weather codes -> human-readable description.
# Source: https://open-meteo.com/en/docs (WMO Weather interpretation codes)
# 
# WMO stands for the World Meteorological Organization, a specialized agency 
# of the United Nations focused on weather, climate, and water resources.
# ---------------------------------------------------------------------------

WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


# Weather codes that represent a thunderstorm - treated as a hard safety
# concern for every outdoor activity, regardless of other conditions.

THUNDERSTORM_CODES = {95, 96, 99}


def describe_weather_code(code):
    """Turn a raw WMO weather code into a human-readable description.

    Returns "Unknown conditions" for any code not in our lookup table,
    rather than raising an error - a forecast with an unrecognised code
    should never crash the app.
    """
    
    return WMO_WEATHER_CODES.get(code, "Unknown conditions")


# ---------------------------------------------------------------------------
# Activities and their weather sensitivity profiles.
#
# These thresholds drive ActivityRiskAnalyzer's scoring. They are reasonable
# general-purpose defaults, not official safety standards - documented here
# so they're easy to find and adjust as a group if you want to tune them.
# ---------------------------------------------------------------------------

ACTIVITIES = {
    "Football": {
        "icon": "⚽",
        "max_wind_kmh": 40,
        "max_precip_probability": 60,
        "ideal_temp_c": (15, 30),
        "extreme_temp_c": (5, 38),
        "base_packing": ["Football boots", "Shin guards", "Water bottle", "Team kit"],
    },
    
    "Jogging": {
        "icon": "🏃",
        "max_wind_kmh": 45,
        "max_precip_probability": 65,
        "ideal_temp_c": (10, 25),
        "extreme_temp_c": (2, 35),
        "base_packing": ["Running shoes", "Moisture-wicking clothing", "Water bottle"],
    },
    
    "Farming": {
        "icon": "🌾",
        "max_wind_kmh": 50,
        "max_precip_probability": 70,
        "ideal_temp_c": (12, 32),
        "extreme_temp_c": (5, 40),
        "base_packing": ["Farm boots", "Gloves", "Wide-brim hat", "Hydration pack"],
    },
    
    "Picnic": {
        "icon": "🧺",
        "max_wind_kmh": 30,
        "max_precip_probability": 30,
        "ideal_temp_c": (18, 30),
        "extreme_temp_c": (10, 35),
        "base_packing": ["Picnic blanket", "Cooler bag", "Sunscreen", "Insect repellent"],
    },
    
    "Travelling": {
        "icon": "🧳",
        "max_wind_kmh": 55,
        "max_precip_probability": 70,
        "ideal_temp_c": (10, 35),
        "extreme_temp_c": (0, 42),
        "base_packing": ["Travel documents", "Phone charger", "Comfortable shoes"],
    },
    
    "Outdoor Event": {
        "icon": "🎪",
        "max_wind_kmh": 35,
        "max_precip_probability": 40,
        "ideal_temp_c": (15, 30),
        "extreme_temp_c": (5, 38),
        "base_packing": ["Tickets/pass", "Portable chair", "Sunscreen", "Rain poncho"],
    },
}


# The hours of the day we consider when recommending a "best time" - keeps
# suggestions to a sensible waking window rather than, say, 3am.

DAYTIME_HOURS_WINDOW = (6, 20) 
# 6:00 in the morning to 20:00 at night