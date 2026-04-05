# AI Programming Learning

个人 AI 编程学习项目，记录从入门到实战的完整过程。

## 项目结构

### Day01 - Fullstack 全栈留言板
基础全栈应用，实现前后端分离的留言板功能。
- **技术栈**: FastAPI + HTML/JS
- **功能**: 用户留言、消息列表展示

### Day02 - AI 语音助手
智能语音交互助手，集成语音识别、大语言模型和语音合成。
- **技术栈**: FastAPI + Web Speech API + 百度 ASR/TTS + DeepSeek LLM
- **功能**:
  - 🎤 语音输入识别（百度 ASR）
  - 🤖 AI 智能回复（DeepSeek）
  - 🔊 语音播报（百度 TTS）

## 快速开始

### Day01 运行
```bash
cd Day01_Fullstack/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload --port 8001
```

### Day02 运行
```bash
cd Day02_Amallest_Aoice_Assistant/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests pydantic
uvicorn main:app --reload --port 8002
```

然后打开对应项目的 `frontend/index.html` 即可使用。

## 学习记录

- Day 01: 全栈基础搭建，理解前后端交互
- Day 02: AI 能力集成，语音交互全流程
