import os

import logging


def get_google_api_key() -> str | None:
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        logging.warning(
            "GOOGLE_API_KEY not found in environment variables. Ensure .env is loaded by the application entry point."
        )
    return key


def get_weather_api_key() -> str | None:
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        logging.warning(
            "WEATHER_API_KEY not found in environment variables. Ensure .env is loaded by the application entry point."
        )
    return key


def get_model_name() -> str:
    return os.getenv("AGENT_MODEL_NAME", "gemini-1.5-flash")
