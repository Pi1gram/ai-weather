import os
from google.adk.agents import Agent
from tools.get_weather import get_weather

# You can use a string model name (Gemini) or a LiteLlm wrapper here.
MODEL = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "gemini-2.0-flash")

weather_agent_v1 = Agent(
    name="weather_agent_v1",
    model=MODEL,
    description="Provides weather information for specific cities.",
    instruction=(
        "You are a weather assistant. "
        "When asked about a city's weather, call the get_weather tool. "
        "If it returns an error, apologize and say you don’t have the data. "
        "Otherwise, read back the report."
    ),
    tools=[get_weather],
)
