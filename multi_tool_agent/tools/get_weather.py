import requests
from typing import Dict, Union
import os
import logging
import warnings
from dotenv import load_dotenv  # Make sure dotenv is loaded
import google.generativeai as genai  # Import Google AI library

# Load environment variables (ensure this runs)
load_dotenv()

# Suppress specific warnings if needed (optional)
warnings.filterwarnings(
    "ignore",
    message="Some weights of the model checkpoint at distilbert-base-uncased were not used when initializing DistilBertForCausalLM.",
)
warnings.filterwarnings(
    "ignore",
    message="The model 'DistilBertForCausalLM' is not supported for text-generation.",
)

API_URL = "http://localhost:5000/api/weather"  # Your Flask API endpoint

# Configure Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    gemini_model = None
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"Error initializing Google Gemini model: {e}")
        gemini_model = None


def get_weather(city: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """Fetches weather from Flask API and processes with Google Gemini."""
    if gemini_model is None:
        return {
            "status": "error",
            "error_message": "Google Gemini model failed to initialize.",
        }
    try:
        response = requests.get(API_URL, params={"city": city}, timeout=20)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return {"status": "error", "error_message": data["error"]}

        raw_data = {
            "description": data.get("description", "No description available."),
            "temperature": data.get("temperature", "Unknown"),
            "wind": data.get("wind", "Unknown"),
        }
        prompt = (
            f"Generate a brief, human-readable weather report for {city} based on this data:\n"
            f"- Current conditions: {raw_data['description']}\n"
            f"- Temperature: {raw_data['temperature']}\n"
            f"- Wind: {raw_data['wind']}\n\n"
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
                f"Gemini response blocked. Reason: {block_reason}. \
                Safety Ratings: {safety_ratings}"
            )
            return {
                "status": "error",
                "error_message": f"AI response generation \
                blocked (Reason: {block_reason}).",
            }

        ai_response = gemini_response.text.strip()
        return {"status": "success", "report": ai_response}

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {"status": "error", "error_message": f"API request failed: {str(e)}"}
    except Exception as e:
        # Log the full traceback for AI errors
        logging.exception("AI processing failed")
        return {"status": "error", "error_message": f"AI processing failed: {str(e)}"}

