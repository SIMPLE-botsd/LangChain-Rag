# 智扫通智能客服系统

> 基于大语言模型的领域知识问答与个性化服务系统

基于 AI 大模型的智能客服系统，支持知识库检索、天气查询、用户报告生成等功能。

## 功能特性
- *知识库检索增强生成 (RAG)*：基于 Chroma 向量数据库与 DashScope Text Embedding 构建领域知识向量空间，采用混合检索策略（dense + sparse）实现语义匹配，通过 ReAct (Reasoning + Acting) Agent 框架实现精准的工具调用与上下文推理
- *智能多工具编排*：基于 LangChain Agent 与中间件（Middleware）机制实现动态工具链编排，支持工具监控、日志增强、上下文注入；Tool Calling 覆盖 RAG 检索、天气 API、地理位置服务、外部数据查询等
- *自适应提示词系统*：通过中间件实现的动态提示词切换机制，根据对话场景（闲聊问答/报告生成）自动注入不同 system prompt，支持上下文感知的少样本学习
- *流式生成与打字机效果*·：基于 LangChain 的流式输出 (stream_mode="values")，配合前端增量渲染实现

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端框架 | Streamlit |
| Agent 框架 | LangChain + LangGraph |
| 大模型 | 通义千问 (Qwen3-max) |
| 嵌入模型 | DashScope Text Embedding |
| 向量数据库 | Chroma DB |
| 配置管理 | PyYAML |

## 项目结构

```
AiAgent_copy/
├── app.py                      # Streamlit 主界面入口
├── agent/
│   ├── react_agent.py          # ReAct Agent 核心实现
│   └── tools/
│       ├── agent_tools.py      # Agent 工具函数
│       └── middleware.py       # 中间件（日志、动态提示词）
├── model/
│   └── factory.py              # 模型工厂（LLM、Embedding）
├── rag/
│   ├── rag_service.py          # RAG 检索增强服务
│   └── vector_store.py         # Chroma 向量库管理
├── utils/
│   ├── config_handler.py       # YAML 配置加载
│   ├── logger_handler.py       # 日志工具
│   ├── prompt_loader.py        # 提示词加载
│   └── path_tool.py            # 路径工具
├── config/                     # 配置文件
│   ├── rag.yml                 # RAG 配置（模型名称）
│   ├── chroma.yml              # 向量库配置
│   ├── agent.yml               # Agent 配置
│   └── prompt.yml              # 提示词路径配置
├── prompts/                    # 提示词模板
│   ├── main_prompt.txt         # 主系统提示词
│   ├── rag_summarize.txt       # RAG 检索提示词
│   └── report_prompt.txt       # 报告生成提示词
└── data/                       # 知识库数据
    ├── *.txt                   # 知识文档
    ├── *.pdf                   # PDF 文档
    └── external/
        └── records.csv         # 用户使用记录
```

## 快速开始

### 环境要求

- Python 3.10+
- DashScope API Key（通义千问）

### 安装依赖

```bash
pip install streamlit langchain langchain-community langchain-chroma pyyaml
```

### 配置 API Key

在环境变量中设置 DashScope API Key：

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

或在使用前在代码中配置（参考 `model/factory.py`）。

### 启动服务

```bash
streamlit run app.py
```

服务启动后访问 `http://localhost:8501` 即可使用。

## Agent 工具

| 工具 | 功能 | 触发场景 |
|------|------|----------|
| `rag_summarize` | 知识库检索 | 专业知识问答 |
| `get_weather` | 天气查询 | 询问天气或环境影响 |
| `get_user_location` | 获取用户位置 | 自动定位 |
| `get_user_id` | 获取用户 ID | 生成报告 |
| `get_current_month` | 获取当前月份 | 生成报告 |
| `fetch_external_data` | 查询使用记录 | 生成报告 |
| `fill_context_for_report` | 切换报告模式 | 明确要求生成报告 |

## 架构设计

```
┌─────────────────────────────────────┐
│      Streamlit UI (app.py)          │
│   聊天界面 / 消息管理 / 流式输出      │
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
│ Embeddings    │  │ fetch_external   │
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
│   (Chroma)    │  │ 动态提示词切换     │
└───────────────┘  └──────────────────┘
```

## 中间件机制

项目实现了灵活的中间件系统，用于：

1. **工具监控** (`monitor_tool`)：记录工具调用日志，切换报告上下文
2. **模型日志** (`log_before_model`)：模型调用前的日志记录
3. **动态提示词** (`report_prompt_switch`)：根据场景（普通问答/报告生成）动态切换系统提示词

## 知识库管理

将知识文档（`.txt`、`.pdf`）放入 `data/` 目录，系统会自动：

1. 加载并解析文档
2. 按配置分块（chunk_size=200, overlap=20）
3. 生成向量存入 Chroma 数据库
4. 检索时返回最相关的 Top-K 文档

## 配置文件说明

### config/rag.yml
```yaml
chat_model_name: qwen3-max       # 聊天模型名称
embedding_model_name: text-embedding-v4  # 嵌入模型名称
```

### config/chroma.yml
```yaml
collection_name: agent           # 向量集合名
persist_directory: chroma_db     # 向量库持久化路径
k: 3                             # 检索返回数量
chunk_size: 200                  # 分块大小
chunk_overlap: 20                # 分块重叠
```

## 扩展开发

### 添加新工具

1. 在 `agent/tools/agent_tools.py` 中使用 `@tool` 装饰器定义
2. 在 `agent/react_agent.py` 的 `create_agent` 中注册

### 添加新提示词

1. 在 `prompts/` 目录创建 `.txt` 文件
2. 在 `config/prompt.yml` 中注册路径
3. 通过 `utils/prompt_loader.py` 加载

## 许可证

MIT License
