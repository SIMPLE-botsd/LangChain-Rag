# 智扫通智能客服 - Docker部署与开源计划

## TL;DR
为项目添加 Docker 支持，核心代码开源，用户一条命令即可部署

## 用户需求
- **部署方式**: Docker一键部署
- **开源范围**: 核心代码开源（prompt单独处理）

---

## 一、项目结构规划

```
zhisaotong/
├── Dockerfile              # 容器构建文件
├── docker-compose.yml     # 编排文件（含ChromaDB）
├── .env.example           # 环境变量示例（API Key）
├── .gitignore             # Git忽略文件
├── README.md              # 项目说明
├── LICENSE                # 开源协议（MIT）
├── requirements.txt       # Python依赖
└── src/                  # 核心代码（开源）
    ├── app.py
    ├── agent/
    ├── rag/
    ├── model/
    ├── utils/
    └── config/
```

---

## 二、Docker相关文件

### 2.1 Dockerfile
- 基于 python:3.11-slim
- 安装系统依赖
- 复制代码
- 安装Python依赖
- 暴露 8501 端口（Streamlit默认）
- 启动命令

### 2.2 docker-compose.yml
- streamlit 服务（主应用）
- chromadb 服务（向量数据库）
- 环境变量配置
- 卷挂载（持久化数据）

### 2.3 .env.example
```
DASHSCOPE_API_KEY=your_api_key_here
```

---

## 三、开源准备

### 3.1 README.md 内容
- 项目介绍
- 功能特性
- 快速开始（Docker方式）
- 环境变量说明
- 演示截图
- 贡献指南

### 3.2 .gitignore
- __pycache__/
- *.pyc
- .env
- chroma_db/
- logs/

### 3.3 核心代码 vs 闭源
| 内容 | 开源 | 说明 |
|------|------|------|
| Agent代码 | ✅ | react_agent.py, agent_tools.py, middleware.py |
| RAG代码 | ✅ | rag_service.py, vector_store.py |
| 前端代码 | ✅ | app.py |
| 工具函数 | ✅ | utils/*.py |
| 配置文件 | ✅ | config/*.yml |
| prompts | ❌ | prompts/*.txt（核心业务逻辑） |
| 数据文件 | ❌ | data/*（知识库） |
| API Key | ❌ | 不上传 |

---

## 四、执行任务清单

### Wave 1: Docker支持
- [ ] 创建 Dockerfile
- [ ] 创建 docker-compose.yml
- [ ] 创建 .env.example
- [ ] 创建 .dockerignore
- [ ] 创建 requirements.txt

### Wave 2: 开源准备
- [ ] 创建 README.md
- [ ] 创建 LICENSE (MIT)
- [ ] 创建 .gitignore
- [ ] 整理目录结构（src/ 分离）

### Wave 3: 部署验证
- [ ] 本地 Docker 构建测试
- [ ] docker-compose up 验证
- [ ] API Key 配置验证

---

## 五、快速部署命令（用户侧）

```bash
# 1. 克隆项目
git clone https://github.com/yourname/zhisaotong.git
cd zhisaotong

# 2. 配置API Key
cp .env.example .env
vim .env  # 填入你的DashScope API Key

# 3. 一键启动
docker-compose up -d

# 4. 访问
open http://localhost:8501
```

---

## 六、技术要点

1. **API Key 隔离**: 通过环境变量注入，不写入代码
2. **数据持久化**: ChromaDB 数据通过卷挂载
3. **端口**: 8501 (Streamlit)
4. **依赖**: python:3.11-slim + chromadb + streamlit

---

## 七、Success Criteria
- [ ] `docker build` 成功
- [ ] `docker-compose up` 启动无报错
- [ ] 浏览器访问 localhost:8501 显示界面
- [ ] GitHub 仓库创建并上传代码
