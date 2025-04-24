from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agents.weather_agent_v1 import weather_agent_v2

# Session service setup
session_service = InMemorySessionService()

# Define constants for session
APP_NAME = "weather_tutorial_app"
USER_ID = "user_team"
SESSION_ID = "session_team"

# Create the session
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# Create the runner
runner = Runner(
    agent=weather_agent_v2,
    app_name=APP_NAME,
    session_service=session_service
)

print(f"Runner created for agent '{runner.agent.name}'.")