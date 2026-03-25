"""
yaml库 用于处理yaml格式的配置文件
：param yaml_path: yaml配置文件的路径
k : v 的形式存储在yaml文件中
:return: 返回一个字典，包含yaml文件中的配置信息 
"""
import yaml
from utils.path_tool import get_abs_path
# 定义rag的配置文件
def load_rag_config(config_path: str = get_abs_path("config/rag.yml"),encoding = "utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)
    
    
# 定义chroma的配置文件
def load_chroma_config(config_path: str = get_abs_path("config/chroma.yml"),encoding = "utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)
    
    
# 定义prompt的配置文件
def load_prompt_config(config_path: str = get_abs_path("config/prompt.yml"),encoding = "utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)
    
    
# 定义agent的配置文件
def load_agent_config(config_path: str = get_abs_path("config/agent.yml"),encoding = "utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)
    
    
rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompt_config = load_prompt_config()
agent_config = load_agent_config()


if __name__ == '__main__':
    print(agent_config["chat_model_name"])