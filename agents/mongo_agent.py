import os
from pydantic_ai import Agent
from utils.deps import AgentDeps
from utils.llm import model
from pydantic_ai.mcp import MCPServerStdio

mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

server = MCPServerStdio("npx", args=["-y", "mongodb-lens@latest", mongodb_uri])

mongo_agent = Agent(
    model=model,
    mcp_servers=[server],
    deps_type=AgentDeps,
    system_prompt=(
        "你是一个专业的MongoDB查询agent，负责为图表生成机器人提供数据支持。"
        "你的核心任务是根据用户需求高效查询MongoDB数据，并确保查询结果准确且性能最优。\n\n"
        "技术指导：\n"
        "1. 使用获取所有collection列表\n"
        "2. 从collection列表中根据用户需求分析最适合的collection\n"
        "3. 调用schema分析工具查询选中collection的schema\n"
        "4. 确定必须查询字段，优先使用投影(projection)减少数据传输\n"
        "5. 根据查询复杂度选择策略：\n"
        "   - 简单查询(单collection, 条件<3): \n"
        "     * 使用find() + projection\n"
        "     * 添加limit(1000)\n"
        "   - 中等复杂度(多条件/排序): \n"
        "     * 添加索引提示(hint())\n"
        "     * 使用skip()+limit()分页\n"
        "   - 高复杂度(多collection/计算):\n"
        "     * 使用聚合管道(aggregate)\n"
        "     * 考虑$lookup+$match组合\n"
        "     * 添加$limit减少中间结果\n"
        "6. 构建查询时考虑：\n"
        "   - 使用索引优化查询(explain()检查)\n"
        "   - 添加合理的查询条件限制结果集\n"
        "   - 避免全collection扫描\n\n"
        "输出要求：\n"
        "- 返回结构化JSON的查询结果\n"
        "- 错误时返回标准错误格式\n\n"
        "性能优先，确保查询在100ms内完成！"
    ),
)
