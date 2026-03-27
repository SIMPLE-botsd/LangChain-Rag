# 情绪气象台 - 主题改造计划

## TL;DR

> **Quick Summary**: 将智能客服从"扫地机器人"主题改造为"情绪气象台"心理关怀主题，仅修改知识库内容和 app.py 展示层，不改变任何源代码功能。
>
> **Deliverables**:
> - 5个新的情绪关怀知识库文件（替换旧扫地机器人内容）
> - 全新治愈系 UI 的 app.py
>
> **Estimated Effort**: Medium
> **Parallel Execution**: NO - 顺序执行（先知识库后app.py）
> **Critical Path**: 知识库创建 → app.py 改造

---

## Context

### Original Request
用户希望将项目主题从"扫地机器人客服"改变为"情绪气象台"（心理关怀与氛围客服），强调情感连接和治愈系体验。

### 用户明确的需求
1. **核心定位**：弱化商业转化，强调情感连接
2. **天气-情绪映射**：不同天气→不同情绪响应（暖心文案、舒缓音乐等）
3. **位置×时间×天气**：组合场景识别，提供个性化关怀
4. **工作顺序**：先改知识库，最后改 app.py

### 设计方向
- **风格**：治愈系、温柔、放松
- **配色**：温暖柔和（莫兰迪色系/日出日落渐变）
- **图标**：🌤️ 💭 🎵 ☕ 🌙 等治愈系图标

---

## Work Objectives

### Core Objective
将智能客服改造成"情绪气象台"，打造"温柔陪伴"型客服体验

### Concrete Deliverables

#### 知识库文件（data/ 目录）
| 文件名 | 内容描述 | 行数参考 |
|--------|----------|----------|
| `天气情绪映射.txt` | 不同天气类型的情绪响应策略 | ~100行 |
| `心理小贴士.txt` | 正念冥想、情绪调节、压力缓解知识 | ~80行 |
| `氛围推荐.txt` | 音乐/电影/活动推荐（按场景分类） | ~100行 |
| `场景对话库.txt` | 位置×时间×天气组合场景对话 | ~80行 |
| `暖心文案库.txt` | 治愈系文案（早安/晚安/鼓励/安慰） | ~100行 |

#### app.py 改造
| 区域 | 改造内容 |
|------|----------|
| 页面配置 | page_title、page_icon |
| CSS 样式 | 全新温暖治愈系配色方案 |
| 侧边栏 | 情绪气象台介绍、使用指南 |
| 主界面 | 治愈系欢迎语、快捷问题卡片 |
| 快捷问题 | 5个情绪/天气相关问题 |

### Must Have
- [ ] 5个新知识库文件，内容充实（每文件~80-100行）
- [ ] app.py 全新治愈系 UI 主题
- [ ] 删除所有旧扫地机器人相关文件

### Must NOT Have
- [ ] 不修改任何源代码功能（react_agent.py、rag_service.py 等）
- [ ] 不修改任何工具函数（agent_tools.py、middleware.py）
- [ ] 不修改配置和模型工厂

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO（Streamlit 应用，无需单元测试）
- **Automated tests**: NONE
- **QA Policy**: 手动验证

### QA Scenarios (Manual Verification)

```
Scenario: 知识库文件创建验证
  Tool: Bash (ls + wc)
  Steps:
    1. ls data/*.txt 确认新文件存在
    2. wc -l data/*.txt 确认每个文件有足够内容（>50行）
  Expected Result: 5个新文件，每个>50行
  Evidence: 终端输出

Scenario: app.py 语法验证
  Tool: Bash (python -m py_compile)
  Steps:
    1. python -m py_compile app.py
  Expected Result: 无语法错误
  Evidence: 无错误输出

Scenario: Streamlit 页面渲染验证
  Tool: Manual
  Preconditions: 运行 streamlit run app.py
  Steps:
    1. 访问 http://localhost:8501
    2. 检查页面标题显示"情绪气象台"
    3. 检查配色为温暖治愈系
    4. 检查欢迎语符合新主题
    5. 检查快捷问题为情绪相关
  Expected Result: 所有UI元素符合新主题
  Evidence: 截图
```

---

## Execution Strategy

### 顺序执行（知识库 → app.py）

```
Step 1: 知识库改造
├── Task 1: 删除旧扫地机器人知识库文件
├── Task 2: 创建 天气情绪映射.txt
├── Task 3: 创建 心理小贴士.txt
├── Task 4: 创建 氛围推荐.txt
├── Task 5: 创建 场景对话库.txt
└── Task 6: 创建 暖心文案库.txt

Step 2: app.py 改造
└── Task 7: 改造 app.py（UI + 配色 + 文案）

Final: 手动验证
└── Task F1: 整体验证
```

### Agent Dispatch Summary
- **Step 1**: `quick` agent 并行创建知识库文件
- **Step 2**: `quick` agent 修改 app.py
- **Final**: 手动验证

---

## TODOs

---

## Final Verification Wave

- [ ] F1. **整体验证** — `unspecified-high`
  读取 data/ 目录确认 5 个新文件存在且内容充实
  运行 `python -m py_compile app.py` 确认无语法错误
  手动检查 app.py 中的页面标题、欢迎语、配色是否符合新主题
  Output: `知识库 [5/5] | 语法 [PASS/FAIL] | UI [符合/不符合] | VERDICT`

---

## Commit Strategy

- **1**: `refactor(theme): 智扫通 → 情绪气象台` — data/*.txt, app.py

---

## Success Criteria

### Verification Commands
```bash
ls data/*.txt                    # 应显示5个新文件
wc -l data/*.txt                 # 每个文件>50行
python -m py_compile app.py      # 无错误
```

### Final Checklist
- [ ] 所有扫地机器人旧文件已删除
- [ ] 5个新情绪关怀知识库文件已创建
- [ ] app.py 已改造为治愈系 UI
- [ ] 无语法错误