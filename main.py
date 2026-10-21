import json
from openai import OpenAI


client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "gemma4:e2b"

# 1. A real Python function; the model cannot run this, only your code can
def get_weather(city: str) -> str:
    fake_data = {"london": "12C and drizzling", "paris": "16C and sunny"}
    return fake_data.get(city.lower(), "no data for that city")


TOOLS = {"get_weather": get_weather}  # name -> function, so we can dispatch

# 2. A description of the defined function (JSON Schema). This is all the model ever sees.
tool_schemas = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}]


messages = [{"role": "user", "content": "Do I need an umbrella in London today?"}]

# 3. The (famous, agentic) *"loop"*
while True:
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tool_schemas)
    msg = response.choices[0].message
    messages.append(msg.model_dump(exclude_none=True))  # remember what the model said

    if not msg.tool_calls:  # if no tool requested -> final answer
        print("\nAgent:", msg.content)
        break

    for call in msg.tool_calls:  # model asked for tool(s): so WE run them!
        args = json.loads(call.function.arguments)
        print(f"→ model requested {call.function.name}({args})")
        result = TOOLS[call.function.name](**args)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})


print(json.dumps(messages, indent=2))

