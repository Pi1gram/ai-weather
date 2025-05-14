import matplotlib.pyplot as plt
import os
from typing import List


def plot_max_temperatures(dates: List[str], temps: List[float], city: str) -> str:
    """
    Plots max temperatures for a city over a list of dates.
    Returns the file path to the saved PNG plot.
    """
    plt.figure(figsize=(8, 4))
    plt.plot(dates, temps, marker="o")
    plt.title(f"Max Temperatures in {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plot_dir = "weather_ai/static/plots"
    os.makedirs(plot_dir, exist_ok=True)
    file_path = os.path.join(plot_dir, f"{city.replace(' ', '_').lower()}_plot.png")
    plt.savefig(file_path)
    plt.close()
    return file_path
