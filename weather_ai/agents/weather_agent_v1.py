from google.adk.agents import Agent
from tools.get_weather import get_weather
from agents.greeting_agent import greeting_agent
from agents.farewell_agent import farewell_agent
from agents.plotting_agent import plotting_agent
from config import MODEL


weather_agent_v2 = Agent(
    name="weather_agent_v2",
    model=MODEL,
    description="""The main coordinator agent. Handles weather 
requests and delegates greetings/farewells to specialists.""",
    instruction="""You are the main Weather Agent coordinating a team. 
Your primary responsibility is to provide weather information. 
Use the 'get_weather' tool ONLY for specific weather 
requests (e.g., 'weather in London'). 
You have specialized sub-agents: 
1. 'greeting_agent': Handles simple greetings like 'Hi', 
'Hello'. Delegate to it for these. 
2. 'farewell_agent': Handles simple farewells like 'Bye', 
'See you'. Delegate to it for these. 
3. 'plotting_agent': Handles plotting of weather data.
Analyze the user's query. If it's a greeting, 
delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. 
If it's a weather request, handle it yourself 
using 'get_weather'. and plot the data using 'plotting_agent'.
If the user asks for a plot, delegate to 'plotting_agent'.
For anything else, respond appropriately or state 
you cannot handle it.""",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent, plotting_agent],
)
