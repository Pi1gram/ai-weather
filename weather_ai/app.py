from flask import Flask, render_template, request, jsonify
import asyncio
from google.genai import types
from runners.runner_weather import runner
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

USER_ID = "user_team"
SESSION_ID = "session_team"


async def call_agent(query: str):
    """Call the agent asynchronously and return the response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            else:
                final_response_text = "[Agent did not provide a text response]"
            break

    return final_response_text or "[No response received]"


@app.route("/")
def index():
    """Serve the chat interface."""
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from the front end."""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call the agent asynchronously
    response = asyncio.run(call_agent(user_message))
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(port=5001) 
