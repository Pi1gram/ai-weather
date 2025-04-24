from google.adk.agents import Agent
from tools.say_goodbye import say_goodbye

MODEL = "gemini-2.0-flash"


farewell_agent = None
try:
    farewell_agent = Agent(
        model=MODEL,
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
        "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
        "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
        "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",  # Crucial for delegation
        tools=[say_goodbye],
    )
except Exception as e:
    raise RuntimeError(
        f"Failed to initialize farewell_agent: {e}. "
        "Ensure the model is available and the environment is set up correctly."
    )
