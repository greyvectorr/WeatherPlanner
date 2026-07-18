import os



# ---------------------------------------------------------------------------
# Local storage locations (JSON files => storage.py)
# ---------------------------------------------------------------------------

DATA_DIR = "data"
FAVOURITES_FILE = os.path.join(DATA_DIR, "favourites.json")
HISTORY_FILE = os.path.join(DATA_DIR, "search_history.json")
MAX_HISTORY_ENTRIES = 50


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