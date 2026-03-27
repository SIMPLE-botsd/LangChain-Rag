# 情绪气象台

> 心理关怀与氛围陪伴AI助手

基于 AI 大模型的情感陪伴智能客服系统，支持情绪识别、天气共情、暖心文案、氛围推荐、音乐推荐、心理报告生成等功能。

## 功能特性

- *知识库检索增强生成 (RAG)*：基于 Chroma 向量数据库与 DashScope Text Embedding 构建心理关怀知识向量空间，支持 TXT/PDF 文档自动向量化，采用混合检索策略实现语义匹配，通过 ReAct (Reasoning + Acting) Agent 框架实现精准的工具调用与上下文推理
- *天气-情绪映射系统*：根据用户所在位置的天气状况，结合时间、场景，智能匹配情绪关怀策略，提供个性化的温暖回复（基于心知天气 API）
- *智能多工具编排*：基于 LangChain Agent 与中间件（Middleware）机制实现动态工具链编排，支持工具监控、日志增强、上下文注入；Tool Calling 覆盖 RAG 检索、天气 API、地理位置服务、情绪记录查询、音乐推荐等
- *自适应提示词系统*：通过中间件实现的动态提示词切换机制，根据对话场景（情绪陪伴/报告生成）自动注入不同 system prompt，支持上下文感知的少样本学习
- *流式生成与打字机效果*：基于 LangChain 的流式输出 (stream_mode="values")，配合前端增量渲染实现
- *音乐推荐*：集成酷狗音乐 API，根据用户心情和场景推荐治愈系音乐

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端框架 | Streamlit |
| Agent 框架 | LangChain + LangGraph |
| 大模型 | 通义千问 (Qwen3-max) |
| 嵌入模型 | DashScope Text Embedding (text-embedding-v4) |
| 向量数据库 | Chroma DB |
| 天气 API | 心知天气 (Seniverse) |
| 音乐 API | 酷狗音乐 |
| 配置管理 | PyYAML |

## 项目结构

```
AiAgent_copy/
├── app.py                      # Streamlit 主界面入口（情绪气象台UI）
├── agent/
│   ├── __init__.py
│   ├── react_agent.py          # ReAct Agent 核心实现
│   └── tools/
│       ├── __init__.py
│       ├── agent_tools.py      # Agent 工具函数
│       └── middleware.py       # 中间件（日志、动态提示词）
├── model/
│   ├── __init__.py
│   └── factory.py              # 模型工厂（LLM、Embedding）
├── rag/
│   ├── __init__.py
│   ├── rag_service.py          # RAG 检索增强服务
│   └── vector_store.py         # Chroma 向量库管理
├── utils/
│   ├── __init__.py
│   ├── config_handler.py       # YAML 配置加载
│   ├── logger_handler.py       # 日志工具
│   ├── file_handler.py         # 文件处理工具（MD5、PDF/TXT加载）
│   ├── prompt_loader.py        # 提示词加载
│   └── path_tool.py            # 路径工具
├── config/                     # 配置文件
│   ├── rag.yml                 # RAG 配置（模型名称）
│   ├── chroma.yml              # 向量库配置
│   ├── agent.yml               # Agent 配置
│   └── prompt.yml              # 提示词路径配置
├── prompts/                    # 提示词模板
│   ├── main_prompt.txt         # 主系统提示词（情绪陪伴角色）
│   ├── rag_summarize.txt       # RAG 检索提示词
│   └── report_prompt.txt       # 报告生成提示词（心理关怀报告）
├── data/                       # 知识库数据
│   ├── *.txt                   # 心理关怀知识文档
│   ├── *.pdf                   # PDF 文档支持
│   └── external/
│       └── records.csv         # 用户情绪历程记录
├── chroma_db/                   # Chroma 向量数据库持久化目录
├── logs/                        # 日志文件目录
└── README.md
```

## 知识库内容

| 文件 | 内容 |
|------|------|
| 天气情绪映射.txt | 不同天气状况对应的情绪响应策略 |
| 心理小贴士.txt | 正念冥想、情绪调节、压力缓解技巧 |
| 氛围推荐.txt | 音乐、电影、活动推荐（按场景分类） |
| 场景对话库.txt | 位置×时间×天气组合场景对话 |
| 暖心文案库.txt | 早安、晚安、鼓励、安慰等治愈系文案 |

## 快速开始

### 环境要求

- Python 3.10+
- DashScope API Key（通义千问）
- 心知天气 API Key（天气预报，默认可用测试 Key）

### 安装依赖

```bash
pip install streamlit langchain langchain-community langchain-chroma langchain-text-splitters dashscope pyyaml
```

### 配置 API Key

在心知天气官网申请免费 API Key，Linux/macOS：

```bash
export SENIVERSE_KEY="your-seniverse-key"
export DASHSCOPE_API_KEY="your-dashscope-key"
```

Windows：

```powershell
set SENIVERSE_KEY=your-seniverse-key
set DASHSCOPE_API_KEY=your-dashscope-key
```

或直接在代码中修改 `agent/tools/agent_tools.py` 中的默认 Key。

### 启动服务

```bash
streamlit run app.py
```

服务启动后访问 `http://localhost:8501` 即可使用。

## Agent 工具

| 工具 | 功能 | 触发场景 |
|------|------|----------|
| `rag_summarize` | 心理知识库检索 | 需要情绪调节建议、心理小贴士 |
| `get_weather` | 天气查询（心知天气） | 询问天气或需要结合天气给情绪回应 |
| `get_user_location` | 获取用户位置（IP定位） | 自动获取用户所在城市 |
| `get_user_id` | 获取用户 ID | 生成情绪报告 |
| `get_current_month` | 获取当前月份 | 生成情绪报告 |
| `fetch_external_data` | 查询情绪历程记录 | 生成情绪关怀报告 |
| `fill_context_for_report` | 切换报告模式 | 明确要求生成报告 |
| `recommend_music` | 音乐推荐（酷狗音乐） | 询问音乐推荐或说"推荐首歌" |
| `generate_external_data` | 加载外部数据 | 内部工具，初始化情绪历程数据 |

## 核心场景

### 天气-情绪映射

| 天气 | 情绪响应 |
|------|----------|
| 晴天 | 愉悦、振奋、推荐户外活动 |
| 阴天 | 平静、沉思、适合室内活动 |
| 雨天 | 惆怅、浪漫、适合陪伴倾听 |
| 雪天 | 宁静、童趣、适合温暖相聚 |
| 高温 | 烦躁、疲惫、推荐消暑和冥想 |
| 深夜+雨天 | 孤独、敏感、需要温暖陪伴 |

### 特色功能

- 🌧️ **天气情绪映射**：根据天气状况提供对应的情绪关怀
- 💭 **正念冥想引导**：提供呼吸练习、身体扫描等减压技巧
- 🎵 **音乐推荐**：根据心情推荐治愈系音乐（酷狗音乐）
- 🎬 **氛围推荐**：根据场景推荐音乐、电影、活动
- 📝 **情绪报告**：生成个人情绪历程与关怀建议
- 🌙 **深夜陪伴**：为深夜失眠的用户提供温暖陪伴

## 架构设计

```
┌─────────────────────────────────────┐
│      Streamlit UI (app.py)          │
│   情绪气象台界面 / 消息管理 / 流式输出  │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│     ReactAgent (react_agent.py)    │
│   LangChain Agent + 中间件           │
└───────┬─────────────────┬───────────┘
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────────┐
│   模型工厂     │  │    工具函数       │
│ ChatTongyi    │  │ rag_summarize    │
│ DashScope     │  │ get_weather      │
│ Embeddings    │  │ recommend_music │
│               │  │ fetch_external   │
└───────────────┘  └──────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│      RAG Service (rag_service.py)  │
│   检索 → 增强 → 生成 链路             │
└───────┬─────────────────┬───────────┘
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────────┐
│  VectorStore  │  │   Prompt 模板     │
│   (Chroma)    │  │ 情绪角色+报告生成  │
└───────────────┘  └──────────────────┘
```

## 中间件机制

项目实现了灵活的中间件系统，用于：

1. **工具监控** (`monitor_tool`)：记录工具调用日志，切换报告上下文
2. **模型日志** (`log_before_model`)：模型调用前的日志记录
3. **动态提示词** (`report_prompt_switch`)：根据场景（情绪陪伴/报告生成）动态切换系统提示词

## 许可证

MIT License
