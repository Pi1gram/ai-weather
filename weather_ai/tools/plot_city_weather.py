from tools.get_weather import get_weather
from tools.weather_plotting import plot_max_temperatures
from typing import List


def plot_city_weather_for_dates(city: str, dates: List[str]) -> str:
    """
    Fetches max temperatures for the city and dates, then plots them.
    Args:
        city: The city name (e.g. "Melbourne").
        dates: List of dates in YYYY-MM-DD format (e.g. ["2025-05-15", 
        "2025-05-16"]).
    Returns:
        The file path to the saved PNG plot.
    """
    # Fetch the week's forecast (already cached if called recently)
    weather = get_weather(city)
    if weather.get("status") != "success":
        return None
    forecast_days = weather["forecast_data"]
    # Filter for the requested dates
    date_set = set(dates)
    filtered = [d for d in forecast_days if d["date"] in date_set]
    if not filtered:
        return None
    temps = [d["day"]["maxtemp_c"] for d in filtered]
    plot_path = plot_max_temperatures(dates, temps, city)
    # Return the relative URL for the frontend
    return f"/plots/{city.replace(' ', '_').lower()}_plot.png"
