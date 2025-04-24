from google.adk.agents import Agent
from tools.say_hello import say_hello
from google.adk.models.lite_llm import LiteLlm
import os

MODEL = "gemini-2.0-flash"
greeting_agent = None
try:
    greeting_agent = Agent(
        model = MODEL,
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
except Exception as e:
    raise RuntimeError(
        f"Failed to initialize greeting_agent: {e}. "
        "Ensure the model is available and the environment is set up correctly."
    )
