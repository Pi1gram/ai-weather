import os
import asyncio
from google.genai import types
from runners.runner_weather import runner
from dotenv import load_dotenv
load_dotenv()   # <-- this reads your .env into os.environ


USER_ID = "user_team"
SESSION_ID = "session_team"

async def call_agent(query: str):
    print(f"\n>> User: {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            print("<< Agent:", event.content.parts[0].text)
            break

async def main():
    await call_agent("Hello there!")
    await call_agent("Whats the weather in tokyo?")
    await call_agent("Thanks, bye!")

if __name__ == "__main__":
    asyncio.run(main())
