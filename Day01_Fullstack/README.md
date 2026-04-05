# Day 01 - 全栈留言板

基础全栈应用，实现前后端分离的留言板功能。

## 🎯 项目目标

- 学习 FastAPI 框架基础
- 理解前后端分离架构
- 掌握 RESTful API 设计
- 学会 CORS 跨域处理

## 🏗️ 技术架构

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   Frontend  │ ◄─────────────────► │   Backend   │
│  (HTML/JS)  │                     │  (FastAPI)  │
└─────────────┘                     └─────────────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │  内存存储   │
                                    │  (messages) │
                                    └─────────────┘
```

## 📁 目录结构

```
Day01_Fullstack/
└── backend/
    ├── main.py          # FastAPI 主程序
    ├── requirements.txt # 依赖列表
    └── venv/            # Python 虚拟环境
```

## 🚀 快速开始

### 1. 环境准备

```bash
cd Day01_Fullstack/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn
```

### 2. 启动服务

```bash
uvicorn main:app --reload --port 8001
```

### 3. 访问应用

- API 文档: http://localhost:8001/docs
- 直接访问: http://localhost:8001

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 欢迎信息 |
| `/messages` | GET | 获取所有留言 |
| `/messages` | POST | 发送新留言 |

### 使用示例

```bash
# 发送留言
curl -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{"username": "张三", "content": "你好！"}'

# 获取留言列表
curl "http://localhost:8001/messages"
```

## 🔧 核心代码

### 后端 (main.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 留言数据模型
class Message(BaseModel):
    username: str
    content: str

# 内存存储
messages = []

@app.get("/messages")
def get_messages():
    return messages

@app.post("/messages")
def create_message(msg: Message):
    messages.append(msg)
    return {"status": "ok"}
```

## 📝 学习要点

### FastAPI 核心概念

1. **路径操作装饰器**: `@app.get('/')`, `@app.post('/')`
2. **数据模型**: Pydantic BaseModel 自动验证
3. **自动文档**: 访问 `/docs` 查看 Swagger UI
4. **类型提示**: Python 类型自动转换

### CORS 跨域配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定域名
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎯 作业要求

- [x] 完成 FastAPI 环境搭建
- [x] 实现留言列表接口
- [x] 实现发送留言接口
- [x] 配置 CORS 支持前端访问
- [ ] 添加留言时间戳
- [ ] 实现留言删除功能

## 📚 相关资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)

---

**Day 01 完成！** 🎉

下一步：学习 AI 集成，实现语音助手！
