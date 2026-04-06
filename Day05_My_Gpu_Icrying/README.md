# 🤖 AI综合能力测试框架

一套完整的AI模型能力评估系统，涵盖逻辑、语言、数学、常识和创造性思维等维度。

## 📦 项目结构

```
ai_test_suite/
├── __init__.py           # 包入口
├── runner.py             # 测试运行器（核心）
├── models/               # 模型接口
│   ├── base.py          # 模型基类
│   ├── openai_model.py  # OpenAI API 封装
│   ├── huggingface_model.py  # HuggingFace 模型封装
│   └── dummy_model.py   # 虚拟模型（测试用）
├── questions/            # 题目管理
│   ├── base.py          # 题目数据类
│   ├── bank.py          # 题目库
│   └── builtin.py       # 内置20道测试题
├── evaluator/            # 评分系统
│   ├── base.py          # 评分器基类
│   ├── rule_based.py    # 规则评分
│   └── llm_based.py     # LLM评分
├── reporters/            # 报告生成
│   ├── console.py       # 控制台报告
│   ├── json_reporter.py # JSON报告
│   └── markdown.py      # Markdown报告
└── examples/             # 使用示例
    ├── test_hf_model.py
    ├── test_openai_api.py
    ├── benchmark_models.py
    ├── custom_questions.py
    └── advanced_evaluation.py
```

## 🚀 快速开始

### 1. 最简单的方式（虚拟模型演示）

```python
from ai_test_suite import TestRunner, DummyModel

# 创建虚拟模型
model = DummyModel("demo")

# 运行测试
runner = TestRunner(model=model)
result = runner.run_quick_test(num_questions=5)
```

### 2. 测试本地 HuggingFace 模型

```python
from ai_test_suite import TestRunner, HuggingFaceModel

# 加载模型
model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct")

# 运行完整测试
runner = TestRunner(model=model)
result = runner.run()
```

### 3. 测试 API 模型（OpenAI/Kimi/DeepSeek）

```python
from ai_test_suite import TestRunner, OpenAIModel

# 配置API模型
model = OpenAIModel(
    model_name="moonshot-v1-8k",
    api_key="your-api-key",
    base_url="https://api.moonshot.cn/v1",
)

runner = TestRunner(model=model)
result = runner.run()
```

## 📋 内置测试题目

包含20道精心设计的测试题：

| 类别 | 数量 | 题目示例 |
|------|------|---------|
| 逻辑与推理 | 5 | 序列推理、逻辑陷阱、悖论识别、爱因斯坦谜题 |
| 语言理解 | 5 | 歧义消解、隐喻理解、反讽检测、文化语境 |
| 数学思维 | 4 | 抽象代数、几何直觉、概率悖论、无限序列 |
| 常识推理 | 3 | 物理常识、生物推理、社会常识 |
| 创造性思维 | 1 | 概念融合（区块链+光合作用） |
| 伦理与价值观 | 1 | 自动驾驶伦理困境 |
| 元认知 | 1 | 自我反思能力 |

## 🛠️ 核心功能

### 模型接口

统一封装了多种模型调用方式：

- **HuggingFaceModel**: 本地加载 transformers 模型
- **OpenAIModel**: OpenAI API 及兼容服务
- **DummyModel**: 虚拟模型（框架测试用）

### 评分系统

- **RuleBasedEvaluator**: 基于关键词和规则的自动评分
- **LLMBasedEvaluator**: 使用更强的LLM作为评判

### 报告输出

- **ConsoleReporter**: 彩色控制台输出
- **JSONReporter**: 结构化JSON数据
- **MarkdownReporter**: 美观的Markdown报告

## 📊 使用示例

### 多模型对比

```python
from ai_test_suite import TestRunner

models = [model1, model2, model3]
runner = TestRunner(model=models[0])

# 自动对比所有模型
results = runner.benchmark(models, limit=10)
```

### 自定义题目

```python
from ai_test_suite import Question, QuestionBank

# 创建自定义题目
q = Question(
    id="custom_001",
    category=QuestionCategory.LOGIC,
    difficulty=DifficultyLevel.MEDIUM,
    title="自定义题目",
    content="题目内容...",
    answer="参考答案",
    keywords=["关键词1", "关键词2"],
)

# 添加到题库
bank = QuestionBank()
bank.add(q)
bank.save_to_json("my_questions.json")
```

### 高级筛选

```python
# 按类别筛选
result = runner.run(categories=["logic", "math"])

# 按难度筛选
result = runner.run(difficulties=[3, 4])  # 高难度

# 指定题目
result = runner.run(question_ids=["L001", "L002"])
```

## 🔧 安装依赖

```bash
# 基础依赖
pip install torch transformers

# API 调用
pip install openai

# 报告生成（可选）
pip install markdown
```

## 📝 评分标准

| 分数段 | 能力评估 |
|--------|---------|
| 0-40分 | 基础模式匹配，逻辑链短 |
| 41-70分 | 良好推理，能处理标准逻辑 |
| 71-90分 | 强推理，能识别悖论和隐喻 |
| 91-100分 | 接近人类专家水平 |

## 🎯 使用建议

1. **混合提问**：打乱题目顺序，防止模型"预热"
2. **追问细节**：对回答追问"为什么"测试深度理解
3. **设置陷阱**：如第2题、第12题包含反常识陷阱
4. **开放性问题**：第19-20题无标准答案，关注论证过程

## 📄 生成报告示例

运行测试后会输出：

```
======================================================================
🤖 AI 综合能力测试报告
======================================================================

模型名称: Qwen/Qwen2.5-0.5B-Instruct
测试时间: 2024-01-15T10:30:00 ~ 2024-01-15T10:35:00
总用时: 300.00秒

----------------------------------------------------------------------
📊 总体得分
----------------------------------------------------------------------

总分: 156.5 / 200.0
百分比: 78.2%
等级: ✅ 良好

----------------------------------------------------------------------
📈 分类统计
----------------------------------------------------------------------

logic        ████████████████░░░░ 78.5%
             题目数: 5, 平均响应: 12.50s

language     ███████████████░░░░░ 75.0%
             题目数: 5, 平均响应: 8.30s
...
```

## 📚 更多信息

查看 `examples/` 目录获取更多使用示例！

## 🏷️ License

MIT License



标题：4090玩家的AI祛魅实录
一句话总结：
花了3天测试本地大模型，发现7B只比0.5B聪明10%，决定不再折腾本地部署，转而学Python。
章节1：迷茫（Day 1-2）
 
背景：学完FastAPI/Graph RAG后不知道干嘛
 
症状："一个人学无聊"、"等模型下载时不知道干嘛"
 
决定：用AI测试框架测测本地模型智商
章节2：漫长的等待（Day 3）
 
戏剧性细节：93%卡顿，三个.incomplete文件
 
心理描写：从"期待"到"不等了"的转折
 
关键决定：后台挂着下载，前台开始写Python
章节3：集体翻车（实测数据）
表格对比：
表格
模型
参数
体积
分数
每GB智商
表现
Qwen2.5-0.5B
0.5B
1GB
32.2%
32.2%/GB
学渣，但快
DeepSeek-R1-7B
7B
15GB
39.5%
2.6%/GB
话痨，纠结26秒
Qwen2.5-7B
7B
15GB
42.9%
2.9%/GB
沉默，但依然懵
核心发现：
 
性价比暴死：为了10%提升，多等20分钟下载+占用14GB显存
 
全军覆没：数学/逻辑/文化题集体不及格
 
话痨税：DeepSeek思维链写了3929 token，只比0.5B高7分
章节4：觉醒（收获）
给后来者的建议：
1. 
别折腾本地7B了：简单任务用0.5B，复杂推理直接调API
2. 
测试的价值：不是看模型多聪明，是知道它什么时候会胡说（禁区清单）
3. 
动手比等待重要：等15GB下载的焦虑 > 写Python分析的快乐
章节5：代码（你的产出）
 
 analyze_deepseek.py ：话痨分析器（统计模型废话量）
 
 download_calculator.py ：下载时间计算器（实用工具）
 
 test_results/ ：原始测试日志（JSON/Markdown）