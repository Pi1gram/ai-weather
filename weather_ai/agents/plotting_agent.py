from google.adk.agents import Agent
from tools.weather_plotting import plot_max_temperatures
from config import MODEL

plotting_agent = Agent(
    name="plotting_agent",
    model=MODEL,
    instruction="""You are the Plotting Agent. Your ONLY task is to generate weather plots using the 'plot_max_temperatures' tool. 
Provide a plot of max temperatures for a city over a list of dates when requested. Do not answer general weather or greeting/farewell questions.""",
    description="Handles plotting of weather data using matplotlib.",
    tools=[plot_max_temperatures],
)
