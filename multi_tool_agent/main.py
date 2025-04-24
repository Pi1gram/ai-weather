import os
import asyncio
from google.genai import types
from runners.runner_weather import runner
from dotenv import load_dotenv
load_dotenv()   # <-- this reads your .env into os.environ


USER_ID = "user_1"
SESSION_ID = "session_001"

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
    await call_agent("What is the weather in London?")
    await call_agent("How about Paris?")
    await call_agent("Tell me the weather in New York")

if __name__ == "__main__":
    asyncio.run(main())
