import requests
from typing import Dict, Union
import os
import logging
from dotenv import load_dotenv  # Make sure dotenv is loaded
import google.generativeai as genai  # Import Google AI library

# Load environment variables (ensure this runs)
load_dotenv()

_cached_forecast = {}
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    logging.error("Error: WEATHER_API_KEY not found in environment variables.")
    raise ValueError("WEATHER_API_KEY not found in environment variables.")

API_URL = "http://api.weatherapi.com/v1/forecast.json"

# Configure Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logging.error("Error: GOOGLE_API_KEY not found in environment variables.")
    gemini_model = None
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        logging.error("Error initializing Google Gemini model: %s", e)
        gemini_model = None


def get_weather(city: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Fetches and caches a week's forecast for the city.
    Returns today's weather summary by default.
    """
    global _cached_forecast
    if gemini_model is None:
        return {
            "status": "error",
            "error_message": "Google Gemini model failed to initialize.",
        }
    try:
        # Use cached forecast if available and for the same city
        forecast = _cached_forecast.get(city.lower())
        if not forecast:
            response = requests.get(
                API_URL,
                params={"key": WEATHER_API_KEY, "q": city, "days": 7},
                timeout=20,
            )
            response.raise_for_status()
            forecast = response.json()
            if "error" in forecast:
                return {"status": "error", "error_message": forecast["error"]}
            _cached_forecast[city.lower()] = forecast

        # Default: summarize today's weather
        today = forecast["forecast"]["forecastday"][0]
        condition = today["day"]["condition"]["text"]
        temp_c = today["day"]["maxtemp_c"]
        temp_f = today["day"]["maxtemp_f"]
        wind_kph = today["day"]["maxwind_kph"]
        wind_mph = today["day"]["maxwind_mph"]
        date_str = today["date"]

        prompt = (
            f"Generate a brief, human-readable weather report for {city} on {date_str} based on this data:\n"
            f"- Condition: {condition}\n"
            f"- Max Temperature: {temp_c}°C / {temp_f}°F\n"
            f"- Max Wind: {wind_kph} kph ({wind_mph} mph)\n"
            f"Report:"
        )

        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=100,
        )
        gemini_response = gemini_model.generate_content(
            prompt, generation_config=generation_config
        )

        if not gemini_response.parts:
            block_reason = (
                gemini_response.prompt_feedback.block_reason
                if gemini_response.prompt_feedback
                else "Unknown"
            )
            safety_ratings = (
                gemini_response.prompt_feedback.safety_ratings
                if gemini_response.prompt_feedback
                else "N/A"
            )
            logging.warning(
                f"Gemini response blocked. Reason: {block_reason}. "
                f"Safety Ratings: {safety_ratings}"
            )
            return {
                "status": "error",
                "error_message": f"AI response generation blocked (Reason: {block_reason}).",
            }

        ai_response = gemini_response.text.strip()
        return {
            "status": "success",
            "report": ai_response,
            "forecast_data": forecast["forecast"]["forecastday"],  # for follow-up use
        }

    except requests.exceptions.RequestException as e:
        logging.error("API request failed: %s", e)
        return {"status": "error", "error_message": f"API request failed: {str(e)}"}
    except Exception as e:
        logging.exception("AI processing failed")
        return {"status": "error", "error_message": f"AI processing failed: {str(e)}"}
