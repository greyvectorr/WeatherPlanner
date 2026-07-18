"""
Custom exceptions for the Weather Risk & Outdoor Activity Planner.

All app-specific exceptions inherit from WeatherAppError, so calling code
can either catch a specific problem (e.g. LocationNotFoundError) or catch
everything the app might raise with a single `except WeatherAppError`.
"""


class WeatherAppError(Exception):
    pass


class LocationNotFoundError(WeatherAppError):
    pass


class WeatherDataError(WeatherAppError):
    pass


class NetworkError(WeatherAppError):
    pass


class APIResponseError(WeatherAppError):
    pass


class AIServiceError(WeatherAppError):
    pass