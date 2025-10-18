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


with open("../scanningAgent/testable-interfaces.txt", "r") as file:
    content = file.read()
    print(content)

testResponse = agent.run(f"Here is a list of testable interfaces for an app:\n\n{content}\n\nCan you  Generate 5 random fuzz test cases for each of these interfaces? Provide the test cases in a structured format, specifying the input values and the expected outputs for each test case. Try to intentionally generate bad inputs to test the robustness of the interfaces. ")

print("Test Response:")
print(testResponse)




# with open("test-cases.txt", "w") as f:
#   f.write(testResponse)