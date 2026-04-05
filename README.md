# AI Programming Learning

个人 AI 编程学习项目，记录从入门到实战的完整过程。

> 🎯 **目标**: 30天掌握 AI 应用开发核心技能

## 📚 项目结构

| 天数 | 项目名称 | 技术栈 | 核心能力 |
|------|----------|--------|----------|
| [Day 01](./Day01_Fullstack) | 全栈留言板 | FastAPI + HTML/JS | 前后端分离、RESTful API |
| [Day 02](./Day02_Amallest_Aoice_Assistant) | AI 语音助手 | FastAPI + 百度 ASR/TTS + DeepSeek | 语音交互、AI 集成 |
| [Day 03](./Day03_Graph_RAG) | Graph RAG 知识图谱 | Neo4j + Kimi API | 知识图谱、RAG 增强 |

---

## 🚀 快速开始

### Day 01 - 全栈留言板

基础全栈应用，实现前后端分离的留言板功能。

```bash
cd Day01_Fullstack/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload --port 8001
```

**技术要点**: FastAPI 基础、CORS 配置、RESTful API 设计

---

### Day 02 - AI 语音助手

智能语音交互助手，集成语音识别、大语言模型和语音合成。

```bash
cd Day02_Amallest_Aoice_Assistant/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests pydantic python-dotenv

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入百度和 DeepSeek 的 API Key

uvicorn main:app --reload --port 8002
```

打开 `frontend/index.html` 即可使用语音助手。

**功能特性**: 🎤 语音识别 → 🤖 AI 回复 → 🔊 语音播报

---

### Day 03 - Graph RAG 知识图谱

基于 Neo4j + Kimi API 的 Graph RAG 问答系统，实现企业供应链智能问答。

```bash
cd Day03_Graph_RAG
python -m venv venv
source venv/bin/activate
pip install neo4j openai python-dotenv requests

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 Kimi API Key

# 初始化数据并运行
python init_data.py
python graph_rag_kimi.py
```

**功能特性**: 🗃️ 知识图谱 → 🔍 关系检索 → 💡 AI 问答

---

## 📊 学习路线图

```
Day 01 ──→ Day 02 ──→ Day 03 ──→ ...
全栈基础   AI 集成    知识图谱    持续学习
```

### 技能树

- ✅ Web 开发 (FastAPI、前端基础)
- ✅ AI 集成 (LLM API、语音处理)
- ✅ 数据存储 (图数据库 Neo4j)
- ✅ 工程实践 (虚拟环境、Git、环境变量)
- ⬜ 向量数据库 (Milvus / Pinecone)
- ⬜ Agent 开发 (LangChain / AutoGPT)

---

## 📝 学习记录

| 天数 | 主题 | 收获 |
|------|------|------|
| Day 01 | 全栈基础 | 掌握 FastAPI 框架，理解前后端分离架构 |
| Day 02 | AI 集成 | 打通语音交互全流程，学会 API 集成与环境管理 |
| Day 03 | 知识图谱 | 学习 Neo4j 图数据库，理解 Graph RAG 架构 |

---

## 🔧 环境配置

所有项目使用独立虚拟环境和 `.env` 管理配置：

```bash
# 每个子项目目录结构
Day0X_Project/
├── venv/           # 独立虚拟环境
├── .env            # 敏感配置（不提交）
├── .env.example    # 配置模板（可提交）
└── .gitignore      # 忽略 venv/ 和 .env
```

---

## 📄 许可证

MIT License - 自由使用、学习参考

---

> **开始学习**: 进入任意 Day 目录查看详细 README

**🚀 Start Your AI Programming Journey!**
