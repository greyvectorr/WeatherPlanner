"""
Forecast - wraps the raw JSON that Open-Meteo returns into a clean object
with proper Python types (datetimes instead of ISO strings, etc.) and
convenient methods for reading it hour by hour or day by day.
"""