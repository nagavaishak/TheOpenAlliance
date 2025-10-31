from strands import Agent
from strands_tools import calculator, current_time

# Create agent with Claude Sonnet 4.5
agent = Agent(
    tools=[calculator, current_time],
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0"  # ✅ US inference profile
)

print("Testing Strands Agent with Claude Sonnet 4.5...\n")

# Test it
response = agent("What time is it right now? And calculate 42 * 137 for me.")
print(response)