# Day04 模型竞技场 - 本地 LLM 对比测试

## 📖 项目简介

本项目是在本地 CPU 环境下运行多个开源 LLM 模型进行对比测试的学习项目。通过在边缘设备上部署不同参数规模的模型，深入理解模型大小、推理速度和输出质量之间的权衡关系。

## 🎯 学习目标

- 了解如何在本地 CPU 环境运行大语言模型
- 对比不同参数规模模型的性能差异
- 学习使用 llama.cpp 进行模型量化推理
- 掌握模型评估的基本方法

## 🏗️ 项目结构

```
Day04_Model_Battle/
├── day04_arena_test.py      # 主测试脚本（推荐入口）
├── four_models_battle.py    # 四模型对比快速测试
├── logic_puzzle.py          # 逻辑题专项测试
├── run.sh                   # 快速启动脚本
├── README.md                # 本文件
├── ANALYSIS.md              # 测试结果分析
└── requirements.txt         # 依赖列表
```

## 🔧 环境要求

### 硬件配置
- **CPU**: Intel i9 或同等性能（建议 8 核以上）
- **内存**: 8GB+
- **磁盘**: 4GB+ 用于存放模型文件

### 软件依赖
```bash
pip install llama-cpp-python
```

## 📦 模型准备

本版本专注优化 **TinyLlama-1.1B** 单模型（轻量级部署）：

| 模型 | 参数量 | 文件大小 | 特点 |
|------|--------|----------|------|
| TinyLlama-1.1B | 1.1B | ~638MB | 小巧精悍，速度快 |

> 💡 **提示**: 如需对比多模型，可下载其他 GGUF 模型并修改 `MODELS` 配置

模型存放路径：
```
/home/song/ai/edge_ai/
└── tinyllama-1.1b-chat-q4.gguf
```

## 🚀 快速开始

### 1. 基础对比测试
```bash
# 运行默认测试（逻辑题对比）
python day04_arena_test.py

# 或使用脚本
bash run.sh
```

### 2. 交互式模式
```bash
# 选择特定模型，输入自定义问题
python day04_arena_test.py --interactive
```

### 3. 全面测试
```bash
# 运行多个类别的问题测试
python day04_arena_test.py --test
```

### 4. 专项测试
```bash
# 逻辑题测试
python logic_puzzle.py

# 四模型快速对比
python four_models_battle.py
```

## 📊 测试结果示例

### 性能对比（Intel i9 环境）

| 模型 | 加载时间 | 生成速度 | 质量评分 |
|------|----------|----------|----------|
| Qwen0.5B | ~1s | ~62 tok/s | ⭐⭐⭐ |
| Qwen1.5B | ~3s | ~25 tok/s | ⭐⭐⭐⭐ |
| Phi-2 | ~4s | ~15 tok/s | ⭐⭐⭐⭐ |
| TinyLlama | ~2s | ~35 tok/s | ⭐⭐⭐ |

### 逻辑题测试案例

**问题**: "如果我昨天是明天，那么今天就是周五。请问今天实际上是周几？"

- **正确答案**: 周日 或 周三（取决于理解方式）
- **测试目的**: 考察模型的逻辑推理能力

详见 [ANALYSIS.md](./ANALYSIS.md)

## 🔍 核心代码解析

### 模型加载
```python
from llama_cpp import Llama

llm = Llama(
    model_path="path/to/model.gguf",
    n_threads=16,        # 使用 16 线程
    n_ctx=2048,          # 上下文长度
    verbose=False        # 关闭详细日志
)
```

### 生成回复
```python
response = llm.create_chat_completion(
    messages=[{"role": "user", "content": "你的问题"}],
    max_tokens=200,      # 最大生成 token 数
    temperature=0.7      # 温度参数
)
answer = response['choices'][0]['message']['content']
```

## 📝 学习笔记

### 1. 模型量化
- GGUF 格式支持 4-bit 量化，大幅减少内存占用（638MB 即可运行 1.1B 模型）
- 量化后模型质量会有一定损失，但对于简单任务影响较小

### 2. 参数优化
```python
llm = Llama(
    model_path="...",
    n_threads=8,    # 根据 CPU 核心数调整
    n_ctx=1024,     # 1024 足够日常对话，可节省内存
)
```

### 2. 推理优化
- 增加 `n_threads` 可提升 CPU 利用率
- 根据任务调整 `n_ctx` 避免不必要的内存开销

### 3. 模型选择建议
- **快速原型验证**: Qwen0.5B（速度最快）
- **中文任务**: Qwen 系列（针对中文优化）
- **英文任务**: Phi-2（微软训练质量高）
- **资源受限**: TinyLlama（体积小功能全）

## 🐛 常见问题

### 1. 模型加载失败
```
FileNotFoundError: 模型文件不存在
```
**解决**: 检查 `MODELS` 配置中的路径是否正确

### 2. 内存不足
```
RuntimeError: 无法分配内存
```
**解决**: 
- 减少同时加载的模型数量
- 降低 `n_ctx` 值
- 使用更小的模型

### 3. llama-cpp 安装失败
```bash
# macOS
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# Linux (CPU only)
pip install llama-cpp-python --no-cache-dir
```

## 🚀 扩展方向

1. **增加更多模型**: 尝试 Gemma、Mistral 等
2. **GPU 加速**: 使用 CUDA 或 Metal 后端
3. **Web UI**: 搭建 Gradio 界面
4. **批量测试**: 设计标准化评测集
5. **API 服务**: 使用 llama-cpp-python 的 server 模式

## 📚 参考资源

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Qwen2.5](https://huggingface.co/Qwen)
- [Phi-2](https://huggingface.co/microsoft/phi-2)

## 📄 许可证

本项目仅用于学习研究目的。模型使用遵循各自原始许可证。

---

**Day04 完成目标**: ✅ 在本地 CPU 运行多模型对比，理解模型规模与性能的权衡
