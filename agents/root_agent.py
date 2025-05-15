# 从pydantic_ai导入Agent和RunContext类
from typing import Literal
from pydantic_ai import Agent, RunContext

# 从utils.llm导入模型
from agents.chart_agent import chart_agent
from agents.mongo_agent import mongo_agent
from utils.llm import model
from utils.deps import AgentDeps

# 定义root_agent主agent
root_agent = Agent(
    model=model,  # 使用的LLM模型
    output_type=object,  # 输出类型为任意对象
    deps_type=AgentDeps,
    system_prompt=(
        "你是一个图表生成机器人中的主agent,"
        "现在你需要根据用户的需求选择合适的agent来完成任务,"
        "你可以选择MongoDB查询agent来获取数据,"
        "也可以选择图表生成agent来生成图表.\n\n"
        "请根据用户的需求进行选择.\n\n"
        "使用MongoDB查询agent时, 要先将用户的需求转化为语意化的查询语句"
    ),
)


@root_agent.tool
async def search_data(ctx: RunContext[AgentDeps], question: str) -> object:
    """搜索数据"""
    result = await mongo_agent.run(question, deps=ctx.deps)
    return result.output


@root_agent.tool
async def generate_chart(
    ctx: RunContext[AgentDeps],
    result: object,
    chart_type: Literal["柱状图", "折线图", "饼图"],
) -> str:
    """生成图表"""
    query = (
        f"根据查询出的结果生成{chart_type}，以下是查询出的结果",
        f"```json\n{result}\n```",
    )
    result = await chart_agent.run(query, deps=None)
    return result.output
