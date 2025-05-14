from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agents.weather_agent_v1 import weather_agent_v1
from config import DEFAULT_SESSION_ID, DEFAULT_USER_ID

# Store the session service instance globally within this module to ensure it's a singleton
_session_service_instance = None


def get_session_service():
    """Returns a singleton InMemorySessionService instance."""
    global _session_service_instance
    if _session_service_instance is None:
        _session_service_instance = InMemorySessionService()
    return _session_service_instance


# Define constants for the application and default session
APP_NAME = "weather_tutorial_app"


def create_weather_runner(
    app_name: str = APP_NAME,
    user_id: str = DEFAULT_USER_ID,
    session_id: str = DEFAULT_SESSION_ID,
    agent_instance=None,
):
    """
    Creates and returns a configured Runner instance.

    This function initializes a shared InMemorySessionService and ensures a session
    for the given app_name, user_id, and session_id is created.

    Args:
        app_name: The name of the application.
        user_id: The user ID for the session.
        session_id: The session ID.
        agent_instance: An optional pre-configured agent instance. If None,
                        the default weather_agent_v1 will be used.

    Returns:
        A configured Runner instance.
    """
    session_service = get_session_service()

    # Ensure the session is created.
    # InMemorySessionService.create_session will overwrite if it already exists.
    session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    if agent_instance is None:
        agent_instance = weather_agent_v1  # Use the default imported agent

    runner = Runner(
        agent=agent_instance,
        app_name=app_name,  # Runner is configured with an app_name
        session_service=session_service,
    )
    return runner


