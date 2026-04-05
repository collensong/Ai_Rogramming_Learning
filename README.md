# AI Programming Learning

个人 AI 编程学习项目，记录从入门到实战的完整过程。

> 🎯 **目标**: 30天掌握 AI 应用开发核心技能

## 📚 项目结构

| 天数 | 项目名称 | 技术栈 | 核心能力 |
|------|----------|--------|----------|
| Day 01 | [全栈留言板](./Day01_Fullstack) | FastAPI + HTML/JS | 前后端分离、RESTful API |
| Day 02 | [AI 语音助手](./Day02_Amallest_Aoice_Assistant) | FastAPI + 百度 ASR/TTS + DeepSeek | 语音交互、AI 集成 |
| Day 03 | [Graph RAG 知识图谱](./Day03_Graph_RAG) | Neo4j + Kimi API | 知识图谱、RAG 增强 |

---

## 🚀 快速开始

### 环境准备

```bash
# 克隆项目
git clone https://github.com/collensong/Ai_Rogramming_Learning.git
cd Ai_Rogramming_Learning

# 每个子项目都有独立的虚拟环境，按需激活
```

### Day01 - 全栈留言板

基础全栈应用，实现前后端分离的留言板功能。

```bash
cd Day01_Fullstack/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload --port 8001
```

访问 http://localhost:8001/docs 查看 API 文档

**技术要点**: FastAPI 基础、CORS 配置、静态文件服务

---

### Day02 - AI 语音助手

智能语音交互助手，集成语音识别、大语言模型和语音合成。

```bash
cd Day02_Amallest_Aoice_Assistant/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests pydantic python-dotenv

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入百度 API Key 和 DeepSeek API Key

uvicorn main:app --reload --port 8002
```

然后打开 `frontend/index.html` 使用语音助手。

**功能特性**:
- 🎤 语音输入识别（百度 ASR）
- 🤖 AI 智能回复（DeepSeek）
- 🔊 语音播报（百度 TTS）

**技术要点**: 语音处理流程、API 集成、环境变量管理

---

### Day03 - Graph RAG 知识图谱

基于 Neo4j + Kimi API 的 Graph RAG 问答系统，实现企业供应链智能问答。

```bash
cd Day03_Graph_RAG
python -m venv venv
source venv/bin/activate
pip install neo4j openai python-dotenv requests

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 Kimi API Key

# 初始化 Neo4j 数据
python init_data.py

# 运行测试
python test_neo4j.py
python graph_rag_kimi.py
```

**功能特性**:
- 🗃️ 知识图谱构建（Neo4j）
- 🔍 结构化关系检索
- 💡 AI 增强问答（Kimi）

**技术要点**: 图数据库、Cypher 查询、Graph RAG 架构

---

## 📊 学习路线图

```
Day 01 ──→ Day 02 ──→ Day 03 ──→ ...
全栈基础   AI 集成    知识图谱    持续学习
           ↑          ↑
        语音交互    智能检索
```

### 技能树

- [x] **Web 开发**: FastAPI、RESTful API、前端基础
- [x] **AI 集成**: LLM API、语音识别、语音合成
- [x] **数据存储**: 图数据库（Neo4j）
- [x] **工程实践**: 虚拟环境、环境变量、Git 管理
- [ ] **向量数据库**: Milvus / Pinecone（待学习）
- [ ] **Agent 开发**: LangChain / AutoGPT（待学习）

---

## 🔧 环境配置指南

### 统一依赖管理

每个子项目都有独立的 `venv`，避免依赖冲突：

```
Ai_Rogramming_Learning/
├── Day01_Fullstack/
│   └── backend/venv/
├── Day02_Amallest_Aoice_Assistant/
│   └── backend/venv/
└── Day03_Graph_RAG/
    └── venv/
```

### API Key 管理

所有项目都使用 `.env` 文件管理敏感信息：

```env
# 模板文件：.env.example（可提交到 Git）
API_KEY=your_api_key_here

# 真实配置：.env（已添加到 .gitignore，不提交）
API_KEY=sk-xxxxxxxxx
```

---

## 📝 学习记录

### Day 01: 全栈基础
- 掌握 FastAPI 框架基础
- 理解前后端分离架构
- 学会 CORS 配置处理跨域

### Day 02: AI 能力集成
- 打通语音交互全流程（ASR → LLM → TTS）
- 掌握环境变量配置管理
- 理解异步 API 调用

### Day 03: 知识图谱
- 学习 Neo4j 图数据库基础
- 掌握 Cypher 查询语言
- 理解 Graph RAG vs 传统 RAG 的差异

---

## 🤝 参与贡献

这是一个个人学习项目，欢迎提出建议和问题！

**问题反馈**: 通过 GitHub Issues 提交

---

## 📄 许可证

MIT License - 自由使用、学习参考

---

> 💡 **学习建议**: 建议按顺序学习，每个项目都包含完整的 README.md 说明文档。

**开始你的 AI 编程之旅吧！** 🚀
