def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary with keys:
              - 'status': 'success' or 'error'
              - 'report': (if success) a human-readable weather string
              - 'error_message': (if error) why we failed
    """
    # Simple normalization
    key = city.lower().replace(" ", "")
    mock = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny, 25°C."},
        "london":  {"status": "success", "report": "Cloudy in London, 15°C."},
        "tokyo":   {"status": "success", "report": "Light rain in Tokyo, 18°C."},
    }
    return mock.get(key, {
        "status": "error",
        "error_message": f"Sorry, no data for '{city}'."
    })
