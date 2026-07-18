"""
storage.py - local persistence for favourite locations and search history,
using plain JSON files on disk (no database needed for this app).

Every read function is defensive: a missing file, an empty file, or a
corrupted file all result in an empty list being returned rather than a
crash - a broken data file should never stop the app from starting.
"""

import json
import os
from datetime import datetime

from config import DATA_DIR, FAVOURITES_FILE, HISTORY_FILE, MAX_HISTORY_ENTRIES


def _ensure_data_dir():
    """Create the data directory if it doesn't already exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    
def _load_json_list(path):
    """Load a JSON file that should contain a list.

    Returns an empty list if the file doesn't exist, isn't valid JSON, or
    doesn't contain a list - callers never need to handle those cases
    themselves.
    """
    
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    
    if not isinstance(data, list):
        return []
    return data


def _save_json_list(path, data):
    """Write a list to a JSON file, creating the data directory if needed."""
    _ensure_data_dir()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        


# ---------------------------------------------------------------------------
# Favourite locations
# ---------------------------------------------------------------------------

def load_favourites():
    """Return every saved favourite location as a list of dicts."""
    return _load_json_list(FAVOURITES_FILE)


def save_favourite(name, country, latitude, longitude):
    """Add a location to favourites, unless it's already saved.

    Args:
        name, country: Location identifiers, typically from WeatherClient.geocode().
        latitude, longitude: Coordinates, so a favourite can be re-fetched
            without geocoding it again.

    Returns:
        The updated list of favourites.
    """
    
    favourites = load_favourites()
    for favourite in favourites:
        if favourite["name"] == name and favourite["country"] == country:
            return favourites # already saved - nothing to save again
        
    favourites.append({
        "name": name,
        "country": country, 
        "latitude": latitude,
        "longitude": longitude,
    })
    
    _save_json_list(FAVOURITES_FILE, favourites)
    return favourites


def remove_favourite(name, country):
    """Remove a location from favourites by name and country.

    Returns:
        The updated list of favourites.
    """
    
    favourites = load_favourites()
    updated = [
        f for f in favourites if not (f["name"] == name and f["country"] == country)
    ]
    
    _save_json_list(FAVOURITES_FILE, updated)
    return updated



# ---------------------------------------------------------------------------
# Search history
# ---------------------------------------------------------------------------

def load_history():
    """Return past searches as a list of dicts, most recent first."""
    return _load_json_list(HISTORY_FILE)


def save_search(location_name, country, activity, risk_level):
    """Record a search in the history file.

    Keeps only the most recent MAX_HISTORY_ENTRIES searches, so the file
    doesn't grow forever.

    Returns:
        The updated history list.
    """
    
    history = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "location": location_name,
        "country": country,
        "activity": activity,
        "risk_level": risk_level,
    }
    
    history.insert(0, entry) # most recent search first
    history = history[:MAX_HISTORY_ENTRIES]
    _save_json_list(HISTORY_FILE, history)
    return history
    