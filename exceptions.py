"""
Custom exceptions for the Weather Risk & Outdoor Activity Planner.

All app-specific exceptions inherit from WeatherAppError, so calling code
can either catch a specific problem (e.g. LocationNotFoundError) or catch
everything the app might raise with a single `except WeatherAppError`.
"""


class WeatherAppError(Exception):
    """Base class for every custom exception this app raises."""
    pass


class LocationNotFoundError(WeatherAppError):
    """Raised when the geocoding API can't find the location the user typed."""
    pass


class WeatherDataError(WeatherAppError):
    """Raised when a weather response is missing fields we need, or is malformed."""
    pass


class NetworkError(WeatherAppError):
    """Raised when a request fails at the network level (timeout, no connection, DNS)."""
    pass


class APIResponseError(WeatherAppError):
    """Raised when an API responds, but with an error status or an unusable payload."""
    pass


class AIServiceError(WeatherAppError):
    """Raised when the Gemini API call fails or returns something we can't use."""
    pass
