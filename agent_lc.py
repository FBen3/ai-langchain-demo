from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


model = ChatOllama(model="gemma4:e2b")

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    fake_data = {"london": "12C and drizzling", "paris": "16C and sunny"}
    return fake_data.get(city.lower(), "no data for that city")


# the "agent" / 'agentic loop' being created for you
agent = create_agent(model=model, tools=[get_weather])

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Do I need an umbrella in London today?"}]}
)


for m in result["messages"]:
    m.pretty_print()

print(type(agent))

