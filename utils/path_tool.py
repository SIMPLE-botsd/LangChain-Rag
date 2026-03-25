"""
为整个工程提供统一的绝对路径
"""
import os

def get_project_root() -> str:
    """获取项目根目录的绝对路径
    return: 字符串的绝对路径""" 
    """获取项目根目录的绝对路径（Agent_project）"""
    # 当前文件（path_tool.py）所在目录 -> utils
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 再取上一级目录 -> Agent_project
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    """将相对路径转换为绝对路径
    relative_path: 相对于项目根目录的路径
    return: 字符串的绝对路径""" 
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path 



# if __name__ == "__main__":
#     # 测试函数
#     print(get_project_root())
#     print(get_abs_path("config.yaml"))
