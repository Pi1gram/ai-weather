# AI Weather Agent

This project implements a multi-agent system using the Google Agent Development Kit (ADK) to provide weather information and handle simple conversational tasks. It features a web-based chat interface built with Flask.

## Features

- **Weather Information:** Fetches weather data for a specified city using a local API and summarizes it using Google Gemini.
- **Conversational AI:** Handles basic greetings and farewells through dedicated agents.
- **Multi-Agent Architecture:** Uses a root agent (`weather_agent_v2`) to coordinate tasks and delegate to specialized sub-agents (`greeting_agent`, `farewell_agent`).
- **Web Interface:** Provides a simple chat interface using Flask for user interaction.
- **Configurable:** Model names and logging levels can be configured via `config.py` and environment variables.

## Architecture

### Web Frontend (Flask)

    - `weather_ai/app.py`: The main Flask application serving the web interface and handling chat requests.
    - `weather_ai/templates/chat.html`: The HTML structure for the chat interface.
    - `weather_ai/static/`: Contains CSS (`chat.css`) and JavaScript (`chat.js`) for the frontend.

### Google ADK Backend

    - **Agents (`weather_ai/agents/`):**
      - `weather_agent_v1.py`: The root agent that understands user intent and delegates tasks.
      - `greeting_agent.py`: Handles greetings using the `say_hello` tool.
      - `farewell_agent.py`: Handles farewells using the `say_goodbye` tool.
    - **Tools (`weather_ai/tools/`):**
      - `get_weather.py`: Fetches data from the local weather API and uses Google Gemini (`gemini-1.5-flash`) to generate a report.
      - `say_hello.py`: Provides a simple greeting message.
      - `say_goodbye.py`: Provides a simple farewell message.
    - **Runner (`weather_ai/runners/runner_weather.py`):** Manages the execution flow and session state for the root agent (`weather_agent_v2`).
    - **Configuration (`weather_ai/config.py`):** Defines configurable parameters like agent model names and logging levels.

### Local Weather API (Not included in this repo)

    - The `get_weather.py` tool expects a local API server running (default: `http://localhost:5000/api/weather`) to provide raw weather data. You need to run this API separately.

## Setup

### Clone the Repository

    ```bash
    git clone https://gitlab.com/theMarloGroup/training/students/jbhasin/ai_weather.git
    cd ai_weather
    ```

### Create and Activate Virtual Environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.\.venv\Scripts\activate`
    ```

### Install Dependencies

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

### Configure API Keys

    - Create a `.env` file in the `weather_ai` directory (`weather_ai/.env`).
    - Add your Google API key to the `.env` file:
      ```env
      # filepath: /Users/jazzy/Desktop/Marlo/ai_weather/weather_ai/.env
      GOOGLE_API_KEY=AIzaSy...YourGoogleApiKey...
      # Optional: Override model names defined in config.py
      # FAREWELL_AGENT_MODEL=gemini-1.5-flash
      ```
    - **Important:** Ensure `.env` is listed in your `.gitignore` file and **never commit your API keys** to version control.

## Running the Application

### Start the Local Weather API

    - Ensure your separate local weather API server (which provides data to `http://localhost:5000/api/weather`) is running.

### Start the Flask Web Application

    ```bash
    python weather_ai/app.py
    ```

    The application will start, typically on `http://127.0.0.1:5001`.

### Access the Chat Interface

    - Open your web browser and navigate to the URL provided when starting the Flask app (e.g., `http://127.0.0.1:5001`).

## Development

This project uses `ruff` for linting and formatting, and `pytest` for testing. A `Makefile` is provided for common development tasks:

- **Format code:** `make format`
- **Lint code:** `make lint`
- **Run tests:** `make test` (Note: Tests need to be written)
- **Generate reports:** `make report`
- **Clean generated files:** `make clean`

See the `Makefile` for more details (`make help`).
