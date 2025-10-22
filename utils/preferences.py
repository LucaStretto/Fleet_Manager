# utils/preferences.py

"""User Preferences Management"""
import json
import os

PREFERENCES_FILE = "user_preferences.json"

DEFAULT_PREFERENCES = {
    "theme": "light",
    "language": "el",
    "window_size": [1400, 900],
    "window_position": [100, 100]
}

def load_preferences():
    """Load user preferences from file."""
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return DEFAULT_PREFERENCES.copy()
    return DEFAULT_PREFERENCES.copy()

def save_preferences(preferences):
    """Save user preferences to file."""
    try:
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving preferences: {e}")

def get_preference(key, default=None):
    """Get a specific preference value."""
    prefs = load_preferences()
    return prefs.get(key, default)

def set_preference(key, value):
    """Set a specific preference value."""
    prefs = load_preferences()
    prefs[key] = value
    save_preferences(prefs)
