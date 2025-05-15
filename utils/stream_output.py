# 导入Agent和依赖类型
from pydantic_ai import Agent
from pydantic_ai.tools import AgentDepsT

# 导入流式处理相关事件类型
from pydantic_ai.messages import (
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
    ToolCallPartDelta,
)

async def stream_output(agent: Agent, user_prompt: str, deps: AgentDepsT) -> None:
    """流式处理Agent输出
    
    Args:
        agent: 要运行的Agent实例
        user_prompt: 用户输入的提示词
        deps: Agent依赖参数
    """
    output_messages = []  # 存储输出消息的列表
    
    # 开始节点级别的流式迭代
    async with agent.iter(user_prompt, deps=deps) as run: # type: ignore
        async for node in run:
            # 处理用户提示节点
            if Agent.is_user_prompt_node(node):
                output_messages.append(f"=== UserPromptNode: {node.user_prompt} ===")
            
            # 处理模型请求节点
            elif Agent.is_model_request_node(node):
                output_messages.append(
                    "=== ModelRequestNode: streaming partial request tokens ==="
                )
                # 流式处理模型请求
                async with node.stream(run.ctx) as request_stream:
                    async for event in request_stream:
                        # 处理部分开始事件
                        if isinstance(event, PartStartEvent):
                            output_messages.append(
                                f"[Request] Starting part {event.index}: {event.part!r}"
                            )
                        # 处理部分增量事件
                        elif isinstance(event, PartDeltaEvent):
                            if isinstance(event.delta, TextPartDelta):
                                output_messages.append(
                                    f"[Request] Part {event.index} text delta: {event.delta.content_delta!r}"
                                )
                            elif isinstance(event.delta, ToolCallPartDelta):
                                output_messages.append(
                                    f"[Request] Part {event.index} args_delta={event.delta.args_delta}"
                                )
                        # 处理最终结果事件
                        elif isinstance(event, FinalResultEvent):
                            output_messages.append(
                                f"[Result] The model produced a final output (tool_name={event.tool_name})"
                            )
            
            # 处理工具调用节点
            elif Agent.is_call_tools_node(node):
                output_messages.append(
                    "=== CallToolsNode: streaming partial response & tool usage ==="
                )
                # 流式处理工具调用
                async with node.stream(run.ctx) as handle_stream:
                    async for event in handle_stream:
                        # 处理工具调用事件
                        if isinstance(event, FunctionToolCallEvent):
                            output_messages.append(
                                f"[Tools] The LLM calls tool={event.part.tool_name!r} with args={event.part.args} (tool_call_id={event.part.tool_call_id!r})"
                            )
                        # 处理工具结果事件
                        elif isinstance(event, FunctionToolResultEvent):
                            output_messages.append(
                                f"[Tools] Tool call {event.tool_call_id!r} returned => {event.result.content}"
                            )
            
            # 处理结束节点
            elif Agent.is_end_node(node):
                assert run.result.output == node.data.output # type: ignore
                output_messages.append(
                    f"=== Final Agent Output: {run.result.output} ===" # type: ignore
                )