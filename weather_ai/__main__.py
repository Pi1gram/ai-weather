import logging
import asyncio
from google.genai import types
from runners.runner_weather import create_weather_runner
from dotenv import load_dotenv
from config import DEFAULT_SESSION_ID, DEFAULT_USER_ID
import warnings  # Import the warnings module

# -------------------------------------------------------------------------------------------------
# Silence all GenAI/ADK warnings about function‐calling internals
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)
logging.getLogger("google.adk").setLevel(logging.ERROR)
# -------------------------------------------------------------------------------------------------

load_dotenv()  # <-- this reads your .env into os.environ

warnings.filterwarnings("ignore")

runner = create_weather_runner()


async def call_agent(query: str):
    logging.info("\n>> User: %s", query)
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None  # Variable to store the final text

    async for event in runner.run_async(
        user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID, new_message=content
    ):
        # Check if this event is the final response from the agent
        if event.is_final_response():
            # Extract the text part of the final response
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            else:
                final_response_text = "[Agent did not provide a text response]"
            break  # Exit the loop once the final response is found

    if final_response_text is not None:
        logging.info("<< Agent: %s", final_response_text)
    else:
        logging.warning("<< Agent: [No final response received]")


async def main():
    await call_agent("how are you")
    await call_agent("Whats the weather in melbourne?")
    await call_agent("Thanks, bye!")


if __name__ == "__main__":
    asyncio.run(main())
