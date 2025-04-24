import logging
import asyncio
from google.genai import types
from runners.runner_weather import runner
from dotenv import load_dotenv
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

# Configure logging to suppress lower-level messages from libraries if desired
# logging.basicConfig(level=logging.ERROR) # Example: Show only ERROR and above
# Or keep default logging level

USER_ID = "user_team"
SESSION_ID = "session_team"


async def call_agent(query: str):
    print(f"\n>> User: {query}")  # Print the user query
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None  # Variable to store the final text

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        # Check if this event is the final response from the agent
        if event.is_final_response():
            # Extract the text part of the final response
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            else:
                final_response_text = "[Agent did not provide a text response]"
            break  # Exit the loop once the final response is found

    # Print the final agent response after the loop finishes
    if final_response_text is not None:
        print(f"<< Agent: {final_response_text}")
    else:
        # This case might happen if the agent stream ends without a final response event
        print("<< Agent: [No final response received]")


async def main():
    await call_agent("Hello there!")
    await call_agent("Whats the weather in tokyo?")
    await call_agent("Thanks, bye!")


if __name__ == "__main__":
    asyncio.run(main())
