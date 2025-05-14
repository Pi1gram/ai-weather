from httpx import get
import requests
from typing import Dict, Union
import os
import logging
from core.config_utils import get_weather_api_key


_cached_forecast = {}
WEATHER_API_KEY = get_weather_api_key()
API_URL = "http://api.weatherapi.com/v1/forecast.json"


def get_weather(city: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Fetches and caches a week's forecast for the city.
    Returns the raw forecast data.
    """
    global _cached_forecast
    # Removed Gemini model check as it's no longer used in this function

    try:
        # Use cached forecast if available and for the same city
        forecast = _cached_forecast.get(city.lower())
        if not forecast:
            response = requests.get(
                API_URL,
                params={"key": WEATHER_API_KEY, "q": city, "days": 7},
                timeout=10,
            )
            response.raise_for_status()
            forecast_data = response.json()
            if "error" in forecast_data:
                return {
                    "status": "error",
                    "error_message": forecast_data["error"]["message"],
                }
            _cached_forecast[city.lower()] = forecast_data  # Cache the raw data
            forecast = forecast_data

        # Return the relevant part of the forecast data
        return {
            "status": "success",
            "location": forecast.get("location"),
            "current": forecast.get("current"),
            "forecast_data": forecast.get("forecast", {}).get("forecastday"),
        }

    except requests.exceptions.RequestException as e:
        logging.error("API request failed: %s", e)
        return {"status": "error", "error_message": f"API request failed: {str(e)}"}
    except Exception as e:
        logging.exception(
            "Data processing failed"
        )  # Changed from "AI processing failed"
        return {"status": "error", "error_message": f"Data processing failed: {str(e)}"}
