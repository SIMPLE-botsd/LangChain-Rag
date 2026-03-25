import streamlit as st
from agent.react_agent import ReactAgent
import time
from datetime import datetime
import re

# ==================== 消息内容清理函数 ====================
def clean_content(text):
    """清理消息内容，移除HTML标签、代码块和Markdown标记，防止源代码外泄"""
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
    page_title="智扫通智能客服",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式（深色主题） ====================
st.markdown("""
<style>
    /* 深色主题 */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        color: #E2E8F0;
    }
    
    /* 深色主题消息 */
    .stChatMessage {
        background: transparent !important;
    }
    [data-testid="stChatMessage"] {
        background: transparent !important;
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-header p {
        color: #94A3B8;
    }
    
    .welcome-card {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
    }
    .welcome-card h2, .welcome-card p {
        color: #E2E8F0 !important;
    }
    
    .sidebar-item {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
    }
    .sidebar-item h4 { color: #60A5FA !important; }
    .sidebar-item p { color: #94A3B8 !important; }
    
    .quick-card {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
    }
    .quick-card:hover {
        background: #334155 !important;
        border-color: #3B82F6 !important;
    }
    
    .message-time {
        color: #64748B !important;
    }
    
    /* 输入框 */
    .stChatInput input {
        background: #1E293B !important;
        border: 2px solid #334155 !important;
        color: #E2E8F0 !important;
    }
    .stChatInput input::placeholder {
        color: #64748B !important;
    }
    .stChatInput input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* 深色侧边栏 */
    section[data-testid="stSidebar"] {
        background: #0F172A !important;
    }
    
    /* 切换按钮 */
    .theme-btn {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
    }
    
    /* 代码块样式优化 - 防止源代码外泄 */
    pre {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    code {
        color: #E2E8F0 !important;
    }
    
    /* 禁止渲染原始HTML标签 */
    .stMarkdown span[style*="<"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### 💬 关于智扫通")
    
    st.divider()
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>🤖 智能客服</h4>
        <p>基于先进的AI技术，为您提供全天候的智能问答服务</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>📖 使用指南</h4>
        <p>在下方输入您的问题，AI助手会即时为您解答</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-item">
        <h4>💡 提示</h4>
        <p>• 尽量详细描述您的问题<br>
           • 可以输入多轮对话<br>
           • 支持中英文提问</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**🔧 系统状态**")
    st.success("在线")

# ==================== 主界面 ====================
st.markdown("""
<div class="main-header">
    <h1>智扫通智能客服</h1>
    <p>您的专属AI助手，随时为您解答问题</p>
</div>
""", unsafe_allow_html=True)

# ==================== 快捷问题卡片 ====================
if len(st.session_state.get("messages", [])) == 0:
    st.markdown("##### 💬 快捷问题")
    cols = st.columns(2)
    quick_questions = [
        "你好，请介绍一下你自己",
        "你们提供哪些服务？",
        "如何联系客服？",
        "有什么优惠活动吗？"
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

# 处理快捷问题 - 修复点击不发送的问题
if "quick_question" in st.session_state:
    prompt = st.session_state["quick_question"]
    del st.session_state["quick_question"]
    # 将快捷问题当作用户输入来处理
    current_time = datetime.now().strftime("%H:%M")
    
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({
        "role": "user", 
        "content": prompt,
        "time": current_time
    })
    
    response_messages = []
    
    # 打字机效果容器
    typing_placeholder = st.empty()
    full_response = ""
    
    with st.spinner("✨ 正在思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)
        
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                time.sleep(0.01)
                for cha in chunk:
                    yield cha
                
        # 流式输出 + 打字机效果
        response_stream = capture(res_stream, response_messages)
        
        # 实时收集完整响应用于显示（清理HTML标签）
        collected = []
        for char in response_stream:
            collected.append(char)
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
        <h2>👋 欢迎使用智扫通</h2>
        <p>我是您的智能客服助手，有什么可以帮助您的吗？</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 显示聊天历史（带时间戳）====================
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        # 提取时间戳（如果有）
        content = clean_content(message["content"])
        timestamp = message.get("time", "")
        
        if timestamp:
            st.markdown(f'<span class="message-time">{timestamp}</span>', unsafe_allow_html=True)
        st.markdown(content)

# ==================== 用户输入 ====================
prompt = st.chat_input(placeholder="输入您的问题...")

if prompt:
    current_time = datetime.now().strftime("%H:%M")
    
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({
        "role": "user", 
        "content": prompt,
        "time": current_time
    })
    
    response_messages = []
    
    # 打字机效果容器
    typing_placeholder = st.empty()
    full_response = ""
    
    with st.spinner("✨ 正在思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)
        
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                time.sleep(0.01)
                for cha in chunk:
                    yield cha
                
        # 流式输出 + 打字机效果
        response_stream = capture(res_stream, response_messages)
        
        # 实时收集完整响应用于显示（清理HTML标签）
        collected = []
        for char in response_stream:
            collected.append(char)
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
        