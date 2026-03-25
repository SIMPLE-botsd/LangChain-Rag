import sys
import os,random
import urllib.request
import json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService 
from utils.config_handler import agent_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]

external_data = {}

@tool(description="这是一个RAG工具，可以根据用户的查询，从知识库中检索相关信息并返回给用户")
def rag_summarize(query: str):
    return rag.rag_summarize(query)

@tool(description="这是一个天气查询工具，可以根据用户输入的城市名称返回该城市的天气信息。city参数直接传入用户说的城市名即可，user_question参数传入用户原始问题（如果有的话），工具会结合用户问题给出更贴切的回复")
def get_weather(city: str, user_question: str = "") -> str:
    """查询城市天气，使用wttr.in免费API
    
    Args:
        city: 用户提到的城市名称，直接传入即可
        user_question: 用户原始问题，用于回复时引用
    """
    try:
        # 构建参考信息
        ref_info = f"根据您的询问（{user_question}），" if user_question else ""
        
        # wttr.in API - 完全免费，无需注册
        url = f"http://wttr.in/{city}?format=j1"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # 获取实际城市名（nearest_area是列表，areaName也是列表）
        nearest_area = data.get('nearest_area', [])
        if nearest_area and isinstance(nearest_area, list):
            area_info = nearest_area[0]
            area_name_list = area_info.get('areaName', [])
            if area_name_list and isinstance(area_name_list, list) and len(area_name_list) > 0:
                actual_city = area_name_list[0].get('value', city)
            else:
                actual_city = city
        else:
            actual_city = city
        display_city = actual_city if actual_city else city
        
        # 解析当前天气数据
        current_condition = data.get('current_condition', [])
        if current_condition and isinstance(current_condition, list):
            current = current_condition[0]
        else:
            current = {}
        
        temp_C = current.get('temp_C', '未知')
        feels_like = current.get('FeelsLikeC', '未知')
        humidity = current.get('humidity', '未知')
        windspeedKmph = current.get('windspeedKmph', '未知')
        weather_desc_list = current.get('weatherDesc', [])
        if weather_desc_list and isinstance(weather_desc_list, list) and len(weather_desc_list) > 0:
            weatherDesc = weather_desc_list[0].get('value', '未知')
        else:
            weatherDesc = '未知'
        localObsDateTime = current.get('localObsDateTime', '未知')
        uvIndex = current.get('uvIndex', '未知')
        visibility = current.get('visibility', '未知')
        
        # 获取未来几天预报
        weather_forecast = data.get('weather', [])
        forecast_info = ""
        if weather_forecast and isinstance(weather_forecast, list):
            day_names = ['今日', '明日', '后日']
            for i, day in enumerate(weather_forecast[:3]):
                if not isinstance(day, dict):
                    continue
                maxTemp = day.get('maxtempC', '')
                minTemp = day.get('mintempC', '')
                hourly_list = day.get('hourly', [])
                if hourly_list and isinstance(hourly_list, list) and len(hourly_list) > 0:
                    hourly = hourly_list[0]
                    if isinstance(hourly, dict):
                        desc_list = hourly.get('weatherDesc', [])
                        if desc_list and isinstance(desc_list, list) and len(desc_list) > 0:
                            desc = desc_list[0].get('value', '')
                        else:
                            desc = ''
                        chance_of_rain = hourly.get('chanceofrain', '')
                    else:
                        desc = ''
                        chance_of_rain = ''
                else:
                    desc = ''
                    chance_of_rain = ''
                
                day_label = day_names[i] if i < len(day_names) else f'第{i+1}天'
                forecast_info += f"\n{day_label}预报: {desc}, 最高{maxTemp}°C, 最低{minTemp}°C, 降雨概率{chance_of_rain}%"
        
        result = f"""{ref_info}查询到{display_city}的天气信息如下：

【实时天气】
🌡️ 温度: {temp_C}°C（体感温度 {feels_like}°C）
🌥️ 天气状况: {weatherDesc}
💧 湿度: {humidity}%
🌬️ 风速: {windspeedKmph}公里/小时
☀️ 紫外线指数: {uvIndex}
👁️ 能见度: {visibility}公里
⏰ 观测时间: {localObsDateTime}

【未来三天预报】{forecast_info}

以上天气信息仅供参考，具体以实际为准。"""
        return result
    except Exception as e:
        logger.error(f"天气查询失败: {e}")
        return f"抱歉，无法获取{city}的天气信息，请稍后重试。原因：{str(e)}"


@tool(description = "获取用户所在位置的工具函数,返回用户所在城市的名称")
def get_user_location() -> str:
    """获取用户位置，使用ip-api.com免费API"""
    try:
        # ip-api.com - 完全免费，无需注册，返回用户真实IP所在城市
        url = "http://ip-api.com/json/?fields=status,country,city"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('status') == 'success':
            city = data.get('city', '')
            country = data.get('country', '')
            if city and country:
                return f"{city}"
            elif city:
                return city
        # 如果API失败，返回默认城市
        return "北京"
    except Exception as e:
        logger.error(f"获取用户位置失败: {e}")
        return "北京"

@tool(description = "获取用户ID的工具函数,返回一个唯一的用户ID字符串")
def get_user_id() -> str:
    # 这里是一个示例工具函数,可以根据需要进行修改
    return random.choice(user_ids)

@tool(description = "获取当前月份的工具函数,返回当前月份的名称，格式如2025-03")
def get_current_month() -> str:
    """获取当前月份，使用Python datetime本地实现"""
    return datetime.now().strftime("%Y-%m")


def generate_external_data():
    """
    {
        "user_id": {
            "month":{"特征": xxx, "效率": xxx},
            "month":{"特征": xxx, "效率": xxx},
            "month":{"特征": xxx, "效率": xxx},
            "month":{"特征": xxx, "效率": xxx},
        },
    }
    :return:
    """
    if not external_data:
        external_data_pa = get_abs_path(agent_config["external_data_path"])
        if not os.path.exists(external_data_pa):
            raise FileNotFoundError(f"外部数据文件{external_data_pa}不存在")
                    
        with open(external_data_pa,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:  # 跳过表头
                arr: list[str] = line.strip().split(",")
                
                user_id: str = arr[0].replace('"',"")  # 去掉可能存在的引号
                feature: str = arr[1].replace('"',"")
                efficiency: str = arr[2].replace('"',"")
                consumables: str = arr[3].replace('"',"")
                comparison: str = arr[4].replace('"',"")
                time: str = arr[5].replace('"',"")
                
                if user_id not in external_data:
                    external_data[user_id] = {}
                
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }
        
    

@tool(description="从外部系统中获取用户的使用记录，以纯存符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str,month: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:    
        logger.warning(f"{fetch_external_data}未检索到用户{user_id}在{month}的使用记录")
        return ""           
        

@tool(description="无参数，无返回值，调用后除法中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文支持")
def fill_context_for_report():
    return "fill_context_for_report工具被调用，返回报告生成所需的上下文信息"

# if __name__ == '__main__':
#     print(fetch_external_data("1002","2025-01"))