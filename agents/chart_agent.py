from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from utils.llm import model

# run mcp server
mcp_server = MCPServerStdio(command="npx", args=["-y", "@antv/mcp-server-chart"])

# Define the chart agent
chart_agent = Agent(
    model=model,
    mcp_servers=[mcp_server],  # Use the MCP server for chart generation
    system_prompt=(
        "你是一名专家级的图表生成智能体。"
        "在分析用户需求后，使用antv的工具生成最合适的图表。"
        "输出一个有效的图表URL字符串。"
        "如果无法满足请求，请清楚说明原因。"
    ),
    output_type=str,  # 输出类型为字符串（生成的图表URL）
)
