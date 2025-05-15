from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from utils.llm import model

# run mcp server
mcp_server = MCPServerStdio(
    command="npx", args=["-y", "@gongrzhe/quickchart-mcp-server"]
)

# Define the chart agent
chart_agent = Agent(
    model=model,
    mcp_servers=[mcp_server],  # Use the MCP server for chart generation
    system_prompt=(
        "You are a chart generation agent. "
        "Your task is to generate charts based on user requirements. "
        "You can use the QuickChart API to create various types of charts. "
        "Please ensure that the generated chart is accurate and meets the user's needs."
    ),
    output_type=str,  # The output type is a string (URL of the generated chart)
)
