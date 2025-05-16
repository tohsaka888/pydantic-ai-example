# 导入日志监控库logfire
import logfire

# 从agents模块导入root_agent
from agents.mongo_agent import mongo_agent
from agents.root_agent import root_agent
from agents.chart_agent import chart_agent
from utils.deps import AgentDeps
import os
from datetime import datetime

# 配置logfire日志监控
logfire.configure()
# 对pydantic_ai进行监控
logfire.instrument_pydantic_ai()

# 初始化输出目录，如果不存在则创建
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


async def main():
    """主入口函数，启动所有agent并处理用户查询"""
    print("Starting agents...")
    async with mongo_agent.run_mcp_servers():
        async with chart_agent.run_mcp_servers():
            # YYYY-MM-DD HH:MM:SS格式的当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Query:")

            # 用户输入查询内容
            query = input()

            # 异步运行root_agent
            result = await root_agent.run(
                query, deps=AgentDeps(current_time=current_time, save_path=output_dir)
            )

            # 打印结果
            print(f"Result: {result.output}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
