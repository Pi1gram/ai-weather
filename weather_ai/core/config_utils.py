# filepath: /Users/jazzy/Desktop/Marlo/ai_weather/weather_ai/core/config_utils.py
import os
from dotenv import load_dotenv
import logging

_ENV_LOADED = False


def load_app_env():
    global _ENV_LOADED
    if not _ENV_LOADED:
        load_dotenv(
            dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env")
        )  # Adjust path to .env
        _ENV_LOADED = True


def get_google_api_key() -> str | None:
    load_app_env()
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        logging.error("GOOGLE_API_KEY not found in environment variables.")
    return key


def get_weather_api_key() -> str | None:
    load_app_env()
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        logging.error("WEATHER_API_KEY not found in environment variables.")
    return key


def get_model_name() -> str:
    load_app_env()
    return os.getenv("AGENT_MODEL_NAME", "gemini-1.5-flash")
