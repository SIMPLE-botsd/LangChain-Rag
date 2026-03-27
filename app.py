import streamlit as st
from agent.react_agent import ReactAgent
import time
from datetime import datetime
import re

# ==================== 消息内容清理函数 ====================
def clean_content(text):
    """清理消息内容，移除HTML标签、代码块和Markdown标记"""
    if not text:
        return text
    # 移除HTML标签如 <span class="xxx">xxx</span>
    text = re.sub(r'<[^>]+>', '', text)
    # 移除代码块标记
    text = re.sub(r'```[\s\S]*?```', '', text)  # 多行代码块
    text = re.sub(r'`([^`]+)`', r'\1', text)    # 单行代码
    # 移除Markdown标题标记（如 # 标题）
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # 移除Markdown加粗标记（如 **文字**）
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # 移除Markdown斜体标记（如 *文字*）
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # 移除Markdown链接标记（如 [文字](url)）
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.strip()

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="情绪气象台",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式（暗色主题-紫色渐变） ====================
st.markdown("""
<style>
    /* 暗色主题 - 紫色渐变 */
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #1A1A2E 100%);
        color: #E2E8F0;
        min-height: 100vh;
    }
    
    /* 消息样式透明 */
    .stChatMessage {
        background: transparent !important;
    }
    [data-testid="stChatMessage"] {
        background: transparent !important;
    }
    
    /* 主标题 */
    .main-header h1 {
        background: linear-gradient(135deg, #A855F7 0%, #EC4899 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .main-header .subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
    }
    
    /* 欢迎卡片 */
    .welcome-card {
        background: rgba(30, 30, 50, 0.8) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.1) !important;
    }
    .welcome-card h2, .welcome-card p {
        color: #E2E8F0 !important;
    }
    .welcome-card h2 {
        background: linear-gradient(135deg, #A855F7, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    /* 侧边栏项目 */
    .sidebar-item {
        background: rgba(30, 30, 50, 0.6) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }
    .sidebar-item h4 { 
        background: linear-gradient(135deg, #A855F7, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .sidebar-item p { 
        color: #94A3B8 !important;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* 快捷问题卡片 */
    .quick-card {
        background: rgba(30, 30, 50, 0.6) !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 15px !important;
        color: #E2E8F0 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .quick-card:hover {
        background: rgba(50, 40, 80, 0.6) !important;
        border-color: #A855F7 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2) !important;
    }
    
    /* 消息时间戳 */
    .message-time {
        color: #64748B !important;
        font-size: 0.8rem;
    }
    
    /* 输入框 */
    .stChatInput input {
        background: rgba(30, 30, 50, 0.8) !important;
        border: 2px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 25px !important;
        color: #E2E8F0 !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
    }
    .stChatInput input::placeholder {
        color: #64748B !important;
    }
    .stChatInput input:focus {
        border-color: #A855F7 !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
    }
    
    /* 侧边栏 - 暗色 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F0F1A 0%, #1A1A2E 100%) !important;
    }
    
    /* 分割线 */
    .stDivider {
        border-color: rgba(168, 85, 247, 0.2) !important;
    }
    
    /* 按钮样式 - 渐变紫粉 */
    .stButton > button {
        background: linear-gradient(135deg, #A855F7 0%, #EC4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* spinner */
    .stSpinner > div {
        border-color: #A855F7 !important;
    }
    
    /* 代码块 */
    pre {
        background: rgba(15, 15, 26, 0.9) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    code {
        color: #E2E8F0 !important;
    }
    
    /* 禁止渲染原始HTML标签 */
    .stMarkdown span[style*="<"] {
        display: none !important;
    }
    
    /* 选中文字颜色 */
    ::selection {
        background: rgba(168, 85, 247, 0.4);
    }
    
    /* 标签样式 */
    .stStatus {
        background: rgba(168, 85, 247, 0.1) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### 🌤️ 关于情绪气象台")
    
    st.divider()
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>💭 心理陪伴</h4>
        <p>根据天气与你的状态，提供温暖的陪伴与关怀</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>🎵 音乐推荐</h4>
        <p>根据心情推荐治愈系音乐，支持说"推荐音乐"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>💝 使用提示</h4>
        <p>• 分享你现在的感受<br>
           • 告诉我你那边的天气<br>
           • 想聊天或只是陪伴</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>🌙 深夜关怀</h4>
        <p>夜深了也睡不着吗？我在这里陪你</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**🌡️ 此刻状态**")
    st.success("温暖在线")

# ==================== 主界面 ====================
st.markdown("""
<div class="main-header">
    <h1>情绪气象台</h1>
    <p class="subtitle">你的温暖心事伙伴，随时为你守候</p>
</div>
""", unsafe_allow_html=True)

# ==================== 快捷问题卡片 ====================
if len(st.session_state.get("messages", [])) == 0:
    st.markdown("##### 💭 今日心情")
    cols = st.columns(2)
    quick_questions = [
        "今天天气怎么样？你感觉如何？",
        "心情有点低落，能陪我说说话吗",
        "推荐一首治愈系的音乐吧",
        "睡不着，能给我讲个晚安故事吗"
    ]
    
    for i, q in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(f"💬 {q}", key=f"quick_{i}", use_container_width=True):
                st.session_state["quick_question"] = q

# ==================== 初始化 ====================
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()
    
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 处理快捷问题
if "quick_question" in st.session_state:
    prompt = st.session_state["quick_question"]
    del st.session_state["quick_question"]
    
    current_time = datetime.now().strftime("%H:%M")
    
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({
        "role": "user", 
        "content": prompt,
        "time": current_time
    })
    
    # 打字机效果容器
    typing_placeholder = st.empty()
    full_response = ""
    
    with st.spinner("✨ 正在倾听..."):
        # 获取历史消息
        history = st.session_state["messages"][:-1] if len(st.session_state["messages"]) > 0 else []
        
        # 传递历史消息给agent
        res_stream = st.session_state["agent"].execute_stream(prompt, history=history)
        
        # 流式输出 + 打字机效果
        collected = []
        for chunk in res_stream:
            collected.append(chunk)
            full_response = ''.join(collected)
            typing_placeholder.markdown(clean_content(full_response))
        
        # 最终显示
        typing_placeholder.empty()
        with st.chat_message("assistant"):
            st.markdown(clean_content(full_response))
            
        assistant_time = datetime.now().strftime("%H:%M")
        st.session_state["messages"].append({
            "role": "assistant", 
            "content": full_response,
            "time": assistant_time
        })
    
    st.rerun()

# 显示欢迎信息
if len(st.session_state["messages"]) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h2>🌸 你好呀，很高兴遇见你</h2>
        <p>我是情绪气象台，一个只想好好陪伴你的AI伙伴。</p>
        <p>不管外面是晴天还是雨天，不管你现在开心还是难过，我都在这里。</p>
        <p>今天感觉怎么样？想说说话吗？</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 显示聊天历史（带时间戳）====================
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        content = clean_content(message["content"])
        timestamp = message.get("time", "")
        
        if timestamp:
            st.markdown(f'<span class="message-time">{timestamp}</span>', unsafe_allow_html=True)
        st.markdown(content)

# ==================== 用户输入 ====================
prompt = st.chat_input(placeholder="说点什么吧... 我在听 🎧")

if prompt:
    current_time = datetime.now().strftime("%H:%M")
    
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({
        "role": "user", 
        "content": prompt,
        "time": current_time
    })
    
    # 打字机效果容器
    typing_placeholder = st.empty()
    full_response = ""
    
    with st.spinner("✨ 正在倾听..."):
        # 获取历史消息（排除当前这条）
        history = st.session_state["messages"][:-1] if len(st.session_state["messages"]) > 0 else []
        
        # 传递历史消息给agent
        res_stream = st.session_state["agent"].execute_stream(prompt, history=history)
        
        # 流式输出 + 打字机效果
        collected = []
        for chunk in res_stream:
            collected.append(chunk)
            full_response = ''.join(collected)
            typing_placeholder.markdown(clean_content(full_response))
        
        # 最终显示
        typing_placeholder.empty()
        with st.chat_message("assistant"):
            st.markdown(clean_content(full_response))
            
        assistant_time = datetime.now().strftime("%H:%M")
        st.session_state["messages"].append({
            "role": "assistant", 
            "content": full_response,
            "time": assistant_time
        })
    
    st.rerun()
