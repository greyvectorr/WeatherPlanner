"""
Forecast - wraps the raw JSON that Open-Meteo returns into a clean object
with proper Python types (datetimes instead of ISO strings, etc.) and
convenient methods for reading it hour by hour or day by day.
"""

from datetime import datetime

from config import describe_weather_code
from exceptions import WeatherDataError


class Forecast:
    """A parsed, structured weather forecast for one location."""
    
    def __init__(self, raw_data, location_name="", country=""):
        """Build a Forecast from the raw dict returned by WeatherClient.

        Args:
            raw_data: The JSON dict from WeatherClient.get_forecast_raw().
            location_name, country: Optional display info to attach.

        Raises:
            WeatherDataError: the raw data doesn't have the shape we expect
                (missing arrays, or hourly arrays of mismatched length).
        """
        
        self.location_name = location_name
        self.country = country
        
        try:
            hourly = raw_data["hourly"]
            daily = raw_data["daily"]
            
            self.hourly_times = [
                datetime.strptime(
                    t,
                    "%Y-%m-%dT%H:%M" 
                    # "%Y-%m-%dT%H:%M" is a date-time format string representing a 
                    # year, month, day, hour, and minute in ISO 8601 style.
                )
                for t in hourly["time"]
            ]
            
            self.hourly_temperature = hourly["temperature_2m"]
            self.hourly_precip_probability = hourly["precipitation_probability"]
            self.hourly_precipitation = hourly["precipitation"]
            self.hourly_wind_speed = hourly["wind_speed_10m"]
            self.hourly_weather_code = hourly["weather_code"]
            self.hourly_humidity = hourly["relative_humidity_2m"]
            self.hourly_uv_index = hourly["uv_index"]

            self.daily_times = [
                datetime.strptime(
                    t,
                    "%Y-%m-%d"
                )
                for t in daily["time"]
            ]
            
            self.daily_temp_max = daily["temperature_2m_max"]
            self.daily_temp_min = daily["temperature_2m_min"]
            self.daily_precip_probability_max = daily["precipitation_probability_max"]
            self.daily_weather_code = daily["weather_code"]
            self.daily_sunrise = daily["sunrise"]
            self.daily_sunset = daily["sunset"]
            
        except KeyError as missing_field:
            raise WeatherDataError(f"Forecast data was missing expected field: {missing_field}")
        except (ValueError, TypeError) as parse_error:
            raise WeatherDataError(f"Forecast data could not be parsed: {parse_error}")
        
        
        # Every hourly list should be the same length (one entry per hour).
        # If they're not, something is badly wrong with the response and we
        # should not silently proceed with mismatched data.
        
        hourly_lengths = {
            len(self.hourly_times),
            len(self.hourly_temperature),
            len(self.hourly_precip_probability),
            len(self.hourly_wind_speed),
            len(self.hourly_weather_code),
        }
        
        if len(hourly_lengths) > 1:
            raise WeatherDataError("Hourly forecast arrays have mismatched lengths.")
        

def get_hourly_entries(self, day_index=0):
    """Return one day's worth of hourly readings as a list of dicts.

        Args:
            day_index: 0 for today, 1 for tomorrow, etc. (forecast_days=3
                is requested by WeatherClient, so 0-2 are valid).

        Returns:
            A list of dicts, one per hour of that day, each containing:
            time, temperature, precip_probability, wind_speed, weather_code,
            weather_description, humidity, uv_index.
    """
    
    start = day_index * 24
    end = start + 24
    entries = []
    for i in range(start, min(end, len(self.hourl_times))):
        entries.append({
            "time": self.hourly_times[i],
            "temperature": self.hourly_temperature[i],
            "precip_probability": self.hourly_precip_probability[i],
            "wind_speed": self.hourly_wind_speed[i],
            "weather_code": self.hourly_weather_code[i],
            "weather_description": describe_weather_code(self.hourly_weather_code[i]),
            "humidity": self.hourly_humidity[i],
            "uv_index": self.hourly_uv_index[i],
        })
        
    return entries


def get_daily_summary(self, day_index=0):
    """Return a single day's daily-aggregate weather as a dict.

        Args:
            day_index: 0 for today, 1 for tomorrow, etc.

        Returns:
            A dict with date, temp_max, temp_min, precip_probability_max,
            weather_code, weather_description, sunrise, sunset.

        Raises:
            WeatherDataError: day_index is out of range for the data we have.
    """
    
    if day_index >= len(self.daily_times):
        raise WeatherDataError(f"No daily data available for day index {day_index}.")
    
    return {
        "date": self.daily_times[day_index],
        "temp_max": self.daily_temp_max[day_index],
        "temp_min": self.daily_temp_min[day_index],
        "precip_probability_max": self.daily_precip_probability_max[day_index],
        "weather_code": self.daily_weather_code[day_index],
        "weather_description": describe_weather_code(self.daily_weather_code[day_index]),
        "sunrise": self.daily_sunrise[day_index],
        "sunset": self.daily_sunset[day_index],
    }
    
    
def number_of_days(self):
    """How many days of daily-aggregate data this forecast has."""
    return len(self.daily_times)