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
    """查询城市天气，使用心知天气免费API
    
    Args:
        city: 用户提到的城市名称，直接传入即可
        user_question: 用户原始问题，用于回复时引用
    """
    try:
        # 心知天气API配置
        SENIVERSE_KEY = os.environ.get("SENIVERSE_KEY", "") or "SIWcWOHZmX77tVKUY"
        if not SENIVERSE_KEY or SENIVERSE_KEY == "你的key":
            # 如果没有配置key，返回友好提示
            return f"【天气信息暂时无法获取，但这不重要，重要的是你今天感觉怎么样？】"
        
        # 构建参考信息
        ref_info = f"根据您的询问（{user_question}），" if user_question else ""
        
        # 心知天气API - 获取当前天气
        url_now = f"https://api.seniverse.com/v3/weather/now.json?key={SENIVERSE_KEY}&location={city}&language=zh-Hans&unit=c"
        with urllib.request.urlopen(url_now, timeout=10) as response:
            data_now = json.loads(response.read().decode('utf-8'))
        
        # 心知天气API - 获取三天预报
        url_daily = f"https://api.seniverse.com/v3/weather/daily.json?key={SENIVERSE_KEY}&location={city}&language=zh-Hans&unit=c&days=3"
        with urllib.request.urlopen(url_daily, timeout=10) as response:
            data_daily = json.loads(response.read().decode('utf-8'))
        
        # 解析当前天气
        results_now = data_now.get('results', [{}])
        now_data = results_now[0].get('now', {}) if results_now else {}
        
        location_data = results_now[0].get('location', {}) if results_now else {}
        display_city = location_data.get('name', city)
        
        # 处理可能为None的字段
        temp_C = now_data.get('temperature') or now_data.get('temp') or '?'
        feels_like = now_data.get('feels_like') or now_data.get('feelsLike') or ''
        weatherDesc = now_data.get('text') or '未知'
        humidity = now_data.get('humidity') or '?'
        wind_dir = now_data.get('wind_direction') or now_data.get('windDir') or ''
        wind_scale = now_data.get('wind_scale') or now_data.get('windSpeed') or ''
        
        # 解析三天预报
        results_daily = data_daily.get('results', [{}])
        daily_data = results_daily[0].get('daily', []) if results_daily else []
        
        forecast_info = ""
        day_names = ['今日', '明日', '后天']
        for i, day in enumerate(daily_data):
            if i < len(day_names):
                text_day = day.get('text_day') or day.get('textDay') or ''
                text_night = day.get('text_night') or day.get('textNight') or ''
                low = day.get('low') or '?'
                high = day.get('high') or '?'
                rain_prob = day.get('rain_prob') or day.get('rainProb') or '0'
                forecast_info += f"\n{day_names[i]}: {text_day}转{text_night} | {low}~{high}°C | 降雨{rain_prob}%"
        
        wind_info = f"{wind_dir}{wind_scale}级" if wind_dir or wind_scale else "微风"
        feels_info = f"（体感{feels_like}°C）" if feels_like else ""
        
        result = f"""{ref_info}你在{display_city}的天气：

🌡️ {temp_C}°C {feels_info}
🌥️ {weatherDesc}
💧 湿度 {humidity}%
🌬️ {wind_info}

【三天预报】{forecast_info}"""
        return result
    except Exception as e:
        logger.error(f"天气查询失败: {e}")
        # 返回友好提示，让AI自然转换成对话
        return f"【天气信息暂时无法获取，但这不重要，重要的是你今天感觉怎么样？】"


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
    情绪历程数据格式：
    {
        "user_id": {
            "month": {
                "情绪状态": xxx,
                "天气场景": xxx,
                "心理活动": xxx,
                "关怀记录": xxx
            }
        }
    }
    """
    if not external_data:
        external_data_pa = get_abs_path(agent_config["external_data_path"])
        if not os.path.exists(external_data_pa):
            raise FileNotFoundError(f"外部数据文件{external_data_pa}不存在")
                    
        with open(external_data_pa,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:  # 跳过表头
                # 处理CSV格式，字段可能包含逗号在引号内
                parts = []
                in_quote = False
                current = ""
                for char in line.strip():
                    if char == '"':
                        in_quote = not in_quote
                    elif char == ',' and not in_quote:
                        parts.append(current.replace('"', ''))
                        current = ""
                    else:
                        current += char
                parts.append(current.replace('"', ''))
                
                if len(parts) >= 6:
                    user_id: str = parts[0]
                    emotion_state: str = parts[1]
                    weather_scene: str = parts[2]
                    mental_activity: str = parts[3]
                    care_record: str = parts[4]
                    time: str = parts[5]
                    
                    if user_id not in external_data:
                        external_data[user_id] = {}
                    
                    external_data[user_id][time] = {
                        "情绪状态": emotion_state,
                        "天气场景": weather_scene,
                        "心理活动": mental_activity,
                        "关怀记录": care_record
                    }


@tool(description="从外部系统中获取用户的情绪历程记录，以纯字符串形式返回，如果未检索到返回空字符串")
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


@tool(description="音乐推荐工具，根据心情和场景推荐音乐。使用酷狗音乐API搜索")
def recommend_music(mood: str = "", genre: str = "") -> str:
    """根据用户的心情和喜好推荐音乐
    
    Args:
        mood: 用户当前的心情或场景描述（如"治愈"、"雨天"、"失眠"、"开心"）
        genre: 音乐风格偏好（如"轻音乐"、"爵士"、"古典"、"民谣"）
    """
    try:
        # 构建搜索关键词
        keyword_parts = []
        if mood:
            keyword_parts.append(mood)
        if genre:
            keyword_parts.append(genre)
        
        if not keyword_parts:
            keyword_parts = ["治愈"]
        
        # 用空格连接，让搜索更准确
        keyword = " ".join(keyword_parts)
        
        logger.info(f"[音乐推荐] 搜索关键词: {keyword}, mood={mood}, genre={genre}")
        
        # 使用酷狗音乐搜索API
        import urllib.parse
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"http://mobilecdn.kugou.com/api/v3/search/song?keyword={encoded_keyword}&page=1&pagesize=5&showtype=1"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X)',
            'Referer': 'http://m.kugou.com/'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        logger.info(f"[音乐推荐] API返回: status={data.get('status')}")
        
        if data.get('status') == 1 and data.get('data', {}).get('info'):
            songs = data['data']['info'][:5]
            song_list = []
            for song in songs:
                name = song.get('songname', '未知')
                artist = song.get('singername', '未知')
                song_list.append(f"{name} - {artist}")
            
            # 直接返回歌曲列表，让AI自己组织语言（不加前缀）
            return "|".join(song_list)
        else:
            logger.warning(f"[音乐推荐] 未获取到数据: {data}")
            return "MUSIC_ERROR:暂时无法获取音乐推荐"
    
    except Exception as e:
        logger.error(f"音乐推荐失败: {e}", exc_info=True)
        return "MUSIC_ERROR:暂时无法获取音乐推荐"


def _get_fallback_music_by_mood(mood: str = "") -> str:
    """根据心情返回定制音乐推荐"""
    fallback_lists = {
        "难过": """🎵 难过的时候，让这些音乐陪陪你：

1. **River Flows in You** - 李闰珉
2. **Sparkle** - 国立优  
3. **Summer** - 久石让
4. **告一段落的情绪** - 纯音乐
5. **夜曲** - 肖邦

音乐是情绪的容器，让它们陪你度过这个时刻 💜""",
        
        "开心": """🎵 开心的时候就要听欢快的歌！

1. **Sunshine After Rain** - 轻快电子
2. **Good Time** - Owl City
3. **The Show** - Lenka
4. **Lemon** - 米津玄師
5. **无条件经典** - 流行精选

让好心情继续蔓延！☀️""",
        
        "失眠": """🎵 夜深了，让这些音乐伴你入睡：

1. **Weightless** - Marconi Union
2. **Gymnopédie No.1** - 萨蒂
3. **River Flows in You** - 李闰珉
4. **雨声** - 白噪音
5. **卡农** - 帕赫贝尔

闭上眼睛，让旋律轻轻拥你入眠 🌙""",
        
        "治愈": """🎵 治愈系音乐清单：

1. **菊次郎的夏天** - 久石让
2. **Rain** - 押尾光太郎
3. **天空之城** - 久石让
4. **Always with Me** - 木村弓
5. **风居住的街道** - 矶村由纪子

这些旋律像温柔的手，轻轻抚平你的心 🌸""",
        
        "放松": """🎵 放松时光，听这些：

1. **Kokoro** - 冈崎律子
2. ** Nils Frahm** - 钢琴曲
3. **天空之城** - 久石让
4. **Summer** - 久石让
5. **流动的城市** - 林海

让音乐像温水一样包裹你 🫖""",
        
        "default": """🎵 治愈系音乐推荐：

1. **菊次郎的夏天** - 久石让
2. **Rain** - 押尾光太郎
3. **River Flows in You** - 李闰珉
4. **天空之城** - 久石让
5. **风居住的街道** - 矶村由纪子

希望这些音乐能温暖你的时光 🎵"""
    }
    
    # 匹配心情关键词
    mood_lower = mood.lower() if mood else ""
    if any(k in mood_lower for k in ["难过", "伤心", "悲伤", "痛"]):
        return fallback_lists["难过"]
    elif any(k in mood_lower for k in ["开心", "高兴", "快乐", "愉快"]):
        return fallback_lists["开心"]
    elif any(k in mood_lower for k in ["失眠", "睡不着", "夜深", "困"]):
        return fallback_lists["失眠"]
    elif any(k in mood_lower for k in ["治愈", "治愈系", "温暖"]):
        return fallback_lists["治愈"]
    elif any(k in mood_lower for k in ["放松", "舒缓", "平静"]):
        return fallback_lists["放松"]
    return fallback_lists["default"]


# if __name__ == '__main__':
#     print(recommend_music("治愈", "轻音乐"))