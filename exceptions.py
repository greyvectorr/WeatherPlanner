"""
Custom exceptions for the Weather Risk & Outdoor Activity Planner.

All app-specific exceptions inherit from WeatherAppError, so calling code
can either catch a specific problem (e.g. LocationNotFoundError) or catch
everything the app might raise with a single `except WeatherAppError`.
"""