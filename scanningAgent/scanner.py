import os
from smolagents import OpenAIServerModel, ToolCallingAgent

# Configure the model to use LM Studio's local API endpoint
model = OpenAIServerModel(
    model_id="local-model",  # This can be any name, LM Studio will use whatever model you have loaded
    api_base="http://localhost:1234/v1",  # Default LM Studio API endpoint
    api_key="not-needed",  # LM Studio doesn't require an API key by default
)

# Create a simple agent using the local model
agent = ToolCallingAgent(
    name="LocalLLMAgent",
    model=model,
    tools=[],  # Empty list of tools
    # You can also add the default toolbox with add_base_tools=True
)

# Example conversation with the agent
# response = agent.run("Hello! Can you tell me what you are and how you're running?")
# print(f"Agent response: {response}")


with open("../demo_target/lovable/demo_target/app.py", "r") as file:
    content = file.read()
    print(content)

scanResponse = agent.run(f"Here is a FastAPI app code:\n\n{content}\n\nCan you Generate a list of API interfaces offered by this app and what inputs they accept? Specify the types of inputs and input fields clearly")


print("Scan Response:")
print(scanResponse)

with open("testable-interfaces.txt", "w") as f:
  f.write(scanResponse)