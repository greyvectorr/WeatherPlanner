"""
Weather Risk & Outdoor Activity Planner - Streamlit UI.

Run with:  streamlit run app.py

This module is intentionally "thin" - it doesn't contain any weather
logic, risk-scoring logic, or AI-prompting logic itself. Its only job is
to collect input, call the classes in weather_client.py / forecast.py /
risk_analyzer.py / recommendation_engine.py, and render the results.
"""


from datetime import date, datetime

import pandas as pd
import streamlit as st

import storage
from config import ACTIVITIES
from exceptions import WeatherAppError
from forecast import Forecast
from recommendation_engine import RecommendationEngine
from risk_analyzer import ActivityRiskAnalyzer
from validators import extract_numbers, is_valid_date_format
from weather_client import WeatherClient


