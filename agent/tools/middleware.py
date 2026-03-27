import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents.middleware import before_model, wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable 
from langchain_core.messages import ToolMessage
from langgraph.types import Command 
from utils.logger_handler import logger
from langchain.agents.middleware.types import AgentState, dynamic_prompt
from langgraph.runtime import Runtime
from langchain.agents.middleware import ModelRequest
from utils.prompt_loader import load_report_prompts, load_system_prompt, load_rag_prompt


@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,   # 请求的数据封装
    handler: Callable[[ToolCallRequest], ToolMessage | Command],   # 处理工具调用的函数
) -> ToolMessage | Command:    # 工具执行的监控
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}被调用，输入参数: {request.tool_call["args"]}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具：{request.tool_call['name']}执行成功")
        
        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True
        
        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具：{request.tool_call['name']}执行失败: {str(e)}")
        raise e

@before_model
def log_before_model(
    state: AgentState,   # 整个Agent的状态封装，包括历史对话、工具调用记录等
    runtime: Runtime,    # 运行时环境封装，可以获取当前模型、工具等信息
): # 模型执行前的日志记录
    logger.info(f"[log_before_model]即将调用模型,带有{len(state['messages'])}条历史消息")
    
    logger.debug(f"[log_before_model]历史消息详情{type(state['messages'][-1]).__name__} : {state['messages'][-1].content.strip()}")
    return None
    
    
@dynamic_prompt    # 每一次在生成提示词前都调用这个函数，根据当前的上下文动态切换提示词    
def report_prompt_switch(request: ModelRequest):    # 根据不同的场景切换不同的提示词 
    runtime_context = getattr(request.runtime, 'context', None) or {}
    is_report = runtime_context.get("report", False)   # 从运行时上下文中获取是否是报告生成的场景
    if is_report:
        logger.info("[report_prompt_switch]检测到报告生成场景，切换到报告提示词")
        return load_report_prompts()   # 返回报告生成的提示词
    
    return load_system_prompt()   # 返回默认的系统提示词




