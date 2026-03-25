# 代码质量优化计划

## TL;DR
修复7个简单代码问题，提升项目质量

## 待处理项

- [ ] 1. 修复 `agent ` 空格bug — `app.py:271, 297` 变量名多了一个空格
- [ ] 2. 删除未使用的 `month_arr` — `agent_tools.py:13` 已用datetime替代
- [ ] 3. 统一变量命名规范 — 修复拼音/混合风格变量名
- [ ] 4. 简化 `import` 语句 — 删除未使用的 `random`
- [ ] 5. 统一时间格式输出 — 消息时间戳显示格式
- [ ] 6. 添加 API 超时友好提示 — 天气/定位失败时
- [ ] 7. 修复日志冗余输出 — middleware 去掉多余分隔线

## 具体修改

### 1. app.py: 修复 agent 空格bug
```python
# 改
st.session_state["agent "] = ReactAgent()
st.session_state["agent "].execute_stream(prompt)
# 为
st.session_state["agent"] = ReactAgent()
st.session_state["agent"].execute_stream(prompt)
```

### 2. agent_tools.py: 删除 month_arr
```python
# 删除
month_arr = ["2025-01", ..., "2025-12"]
```

### 3. 统一变量命名
- `user_ids= ` → `user_ids = ` (空格规范化)
- 检查其他混合命名风格

### 4. 简化 import
```python
# app.py: 删除未使用的
import random

# agent_tools.py: 删除未使用的  
import random
```

### 5. 统一时间格式
```python
# app.py 中时间戳统一为 %H:%M 格式
```

### 6. API 超时提示
```python
# agent_tools.py: 增强错误信息
except Exception as e:
    return f"天气服务暂时不可用，请稍后重试"
```

### 7. 修复日志冗余
```python
# middleware.py: 删除 print("="*50)
```

## 执行命令
```
/start-work code-cleanup
```
