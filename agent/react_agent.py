import sys
import os,random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import (rag_summarize, fetch_external_data, fill_context_for_report, 
            get_current_month, generate_external_data,get_user_id,get_user_location,get_weather
)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,   
            system_prompt= load_system_prompt(),   # 这里的系统提示词由中间件动态注入
            tools = [rag_summarize, generate_external_data, fetch_external_data, fill_context_for_report, get_current_month, get_user_id, get_user_location, get_weather],   # 工具函数列表
            middleware=[monitor_tool, log_before_model, report_prompt_switch  ]
        )
        
    
    def execute_stream(self,query: str):
        input_dict ={
            "messages":[
            {"role": "user", "content": query}
            ]
        }
        
        # 这里的上下文信息由工具函数动态注入,context={"report": False}表示默认不是报告生成的场景,当fill_context_for_report工具被调用后,中间件会将context["report"]切换为True,从而触发提示词的切换
        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + '\n'
        
        
        
if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告") :
        print(chunk, end="",flush=True)