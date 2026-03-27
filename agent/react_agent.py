import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import (rag_summarize, fetch_external_data, fill_context_for_report, 
            get_current_month, generate_external_data,get_user_id,get_user_location,get_weather,
            recommend_music
)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,   
            system_prompt= load_system_prompt(),
            tools = [rag_summarize, generate_external_data, fetch_external_data, fill_context_for_report, 
                    get_current_month, get_user_id, get_user_location, get_weather, recommend_music],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )
        
    
    def execute_stream(self, query: str, history: list = None):
        """执行流式输出
        
        Args:
            query: 当前用户输入
            history: 历史消息列表 [{"role": "user/assistant", "content": "..."}]
        """
        # 构建消息列表，包含历史消息
        messages = []
        
        # 添加历史消息
        if history and len(history) > 0:
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": query})
        
        input_dict = {"messages": messages}
        
        # 使用 stream_mode="values" 获取流式输出
        # 每个chunk包含完整的消息历史，我们只取最后一个AI消息的增量内容
        last_content = ""
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            messages_list = chunk.get("messages", [])
            if messages_list:
                latest_message = messages_list[-1]
                if hasattr(latest_message, 'content'):
                    new_content = latest_message.content
                    if new_content and new_content != last_content:
                        # 计算新增的内容
                        if last_content and new_content.startswith(last_content):
                            delta = new_content[len(last_content):]
                            last_content = new_content
                            yield delta
                        elif new_content:
                            # 首次或内容完全不同
                            last_content = new_content
                            yield new_content




if __name__ == '__main__':
    agent = ReactAgent()
    # 测试带历史消息
    history = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好呀，有什么可以帮你的吗？"}
    ]
    for chunk in agent.execute_stream("推荐一首治愈的歌", history=history):
        print(chunk, end="", flush=True)
