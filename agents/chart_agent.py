from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent, RunContext
from utils.deps import AgentDeps
from utils.llm import model
import requests

# run mcp server
mcp_server = MCPServerStdio(command="npx", args=["-y", "@antv/mcp-server-chart"])

# Define the chart agent
chart_agent = Agent(
    model=model,
    mcp_servers=[mcp_server],  # Use the MCP server for chart generation
    system_prompt=(
        "你是一名专家级的图表生成智能体。"
        "在分析用户需求后，使用antv的工具生成最合适的图表。"
        "将生成的图表保存在本地，并返回图表的URL。"
        "如果无法满足请求，请清楚说明原因。"
    ),
    output_type=str,  # 输出类型为字符串（生成的图表URL）
    deps_type=AgentDeps,
)


@chart_agent.tool
def save_chart(ctx: RunContext[AgentDeps], url: str, chart_name: str) -> str:
    """
    保存图表的URL
    """
    result = requests.get(url)
    with open(f"{ctx.deps.save_path}/{chart_name}.png", "wb") as f:
        f.write(result.content)
    return f"图表已保存为{chart_name}.png"