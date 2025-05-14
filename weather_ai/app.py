from flask import Flask, render_template, request, jsonify, send_from_directory
import asyncio
from google.genai import types
from google.genai import errors as genai_errors
from runners.runner_weather import create_weather_runner
from config import DEFAULT_SESSION_ID, DEFAULT_USER_ID
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

runner = create_weather_runner(user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID)


async def call_agent(query: str):
    """Call the agent asynchronously and return a structured response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])

    agent_final_text = None
    captured_plot_url = None

    try:
        async for event in runner.run_async(
            user_id=DEFAULT_USER_ID, session_id=DEFAULT_SESSION_ID, new_message=content
        ):
            # Check event type by class name
            if event.__class__.__name__ == "ToolOutputEvent" and getattr(
                event, "tool_output", None
            ):
                for part in event.tool_output.outputs:
                    if getattr(part, "function_response", None):
                        response_data = part.function_response.response
                        if (
                            isinstance(response_data, dict)
                            and "plot_url" in response_data
                        ):
                            captured_plot_url = response_data["plot_url"]

            elif event.is_final_response():
                if event.content and event.content.parts:
                    agent_final_text = event.content.parts[0].text
                break

    except genai_errors.ServerError as e:
        error_message = f"The AI model is currently busy or unavailable \
        (Error: {e}). Please try again later."
        app.logger.error(f"Google API ServerError: {e}")
        return {"text": error_message, "error": True}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        app.logger.error(f"Unexpected error in call_agent: {e}", exc_info=True)
        return {"text": error_message, "error": True}

    response_payload = {}
    if agent_final_text:
        response_payload["text"] = agent_final_text
    else:
        if captured_plot_url:
            response_payload["text"] = "Here is the generated plot:"
        else:
            response_payload["text"] = "[Agent did not provide a text response]"

    if captured_plot_url:
        response_payload["plot_url"] = captured_plot_url

    if not response_payload.get("text") and not response_payload.get("plot_url"):
        return {"text": "[No meaningful response processed]"}

    return response_payload


@app.route("/")
def home():
    """Serve the chat interface."""
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from the front end."""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    agent_response_object = asyncio.run(call_agent(user_message))
    return jsonify({"response": agent_response_object})


@app.route("/plots/<filename>")
def plot_file(filename):
    """Serve plot images from the static/plots directory."""
    return send_from_directory("static/plots", filename)


if __name__ == "__main__":
    app.run(port=5001)
