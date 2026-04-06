# 🎯 AI综合能力测试框架 - 项目总结

## 📊 项目概览

为你创建了一套**完整的AI综合能力测试系统**，包含20道精心设计的测试题和一套功能完善的测试框架。

### 核心特性

| 特性 | 描述 |
|------|------|
| ✅ 20道测试题 | 涵盖逻辑、语言、数学、常识、创造力、伦理、元认知 |
| ✅ 统一模型接口 | 支持 HuggingFace、OpenAI API 及兼容服务 |
| ✅ 智能评分系统 | 规则评分 + LLM评判双重机制 |
| ✅ 多种报告格式 | 控制台、JSON、Markdown |
| ✅ CLI命令行工具 | 一行命令运行测试 |
| ✅ 可扩展架构 | 易于添加新题目和自定义评分 |

---

## 📁 项目结构

```
ai_test_suite/
├── README.md                   # 使用文档
├── PROJECT_SUMMARY.md          # 本文件
├── requirements.txt            # 依赖列表
├── cli.py                      # 命令行工具
├── quickstart.py               # 快速开始示例
│
├── models/                     # 模型接口模块
│   ├── base.py                # 模型基类（统一接口）
│   ├── openai_model.py        # OpenAI/Kimi/DeepSeek API
│   ├── huggingface_model.py   # HuggingFace本地模型
│   └── dummy_model.py         # 虚拟模型（测试用）
│
├── questions/                  # 题目管理模块
│   ├── base.py                # 题目数据类
│   ├── bank.py                # 题目库管理
│   └── builtin.py             # 20道内置测试题 ⭐
│
├── evaluator/                  # 评分系统
│   ├── base.py                # 评分器基类
│   ├── rule_based.py          # 基于规则的自动评分
│   └── llm_based.py           # LLM作为评判
│
├── reporters/                  # 报告生成
│   ├── base.py                # 报告基类
│   ├── console.py             # 彩色控制台输出
│   ├── json_reporter.py       # JSON格式报告
│   └── markdown.py            # Markdown美观报告
│
├── runner.py                   # 测试运行器（核心协调）
│
└── examples/                   # 使用示例
    ├── test_hf_model.py       # 测试HuggingFace模型
    ├── test_openai_api.py     # 测试API模型
    ├── benchmark_models.py    # 多模型对比
    ├── custom_questions.py    # 自定义题目
    └── advanced_evaluation.py # 高级评分
```

---

## 🧠 20道内置测试题详情

### 第一类：逻辑与推理（5题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| L001 | 序列推理：2,6,15,40,104,? | ★★★ | 模式识别、递推思维 |
| L002 | 条件逻辑陷阱（逆命题） | ★★ | 逻辑严密性 |
| L003 | 空间拓扑（立方体颜色） | ★★★★ | 组合数学、对称性 |
| L004 | 说谎者悖论分析 | ★★★ | 元逻辑、悖论处理 |
| L005 | 爱因斯坦谜题简化版 | ★★★★ | 多约束推理 |

### 第二类：语言理解（5题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| LA001 | 歧义句解析（望远镜） | ★★ | 语境理解、歧义消解 |
| LA002 | 隐喻理解（心的孤岛） | ★★★ | 情感理解、文学分析 |
| LA003 | 反讽检测（专家的"绝佳"主意） | ★★ | 语气分析、语境推理 |
| LA004 | 文化语境（半斤八两） | ★ | 文化知识、历史背景 |
| LA005 | 多语言混合逻辑 | ★ | 跨语言推理 |

### 第三类：数学思维（4题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| M001 | 抽象代数（⊕运算） | ★★★ | 抽象思维、证明能力 |
| M002 | 球面几何直觉 | ★★★★ | 非欧几何、空间直觉 |
| M003 | 条件蒙提霍尔问题 | ★★★★ | 贝叶斯推理、条件概率 |
| M004 | 无限序列求和（Grandi级数） | ★★★★ | 数学哲学、可求和性 |

### 第四类：常识推理（3题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| C001 | 深海塑料瓶物理 | ★★ | 物理直觉、过程推理 |
| C002 | 反常植物生物节律 | ★★★ | 生物学、逆向思维 |
| C003 | 社会常识（养活） | ★★ | 社会理解、隐含前提 |

### 第五类：创造性思维（1题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| CR001 | 概念融合（区块链+光合作用） | ★★★ | 类比推理、创新思维 |

### 第六类：伦理与价值观（1题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| E001 | 自动驾驶伦理困境 | ★★★★ | 道德推理、价值权衡 |

### 第七类：元认知（1题）

| ID | 题目 | 难度 | 关键能力 |
|----|------|------|---------|
| ME001 | 自我反思能力 | ★★★★ | 元认知、自我评估 |

---

## 🚀 快速使用指南

### 方式1：命令行工具

```bash
# 快速测试（虚拟模型演示）
python ai_test_suite/cli.py --quick --num 5

# 测试本地模型
python ai_test_suite/cli.py --model Qwen/Qwen2.5-0.5B-Instruct

# 测试 API 模型
python ai_test_suite/cli.py \
    --api-key $KIMI_API_KEY \
    --base-url https://api.moonshot.cn/v1 \
    --model moonshot-v1-8k \
    --category logic \
    --report md \
    --output report.md
```

### 方式2：Python代码

```python
from ai_test_suite import TestRunner, HuggingFaceModel

# 加载模型
model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct")

# 运行测试
runner = TestRunner(model=model)
result = runner.run()

# 查看结果
print(f"总分: {result.overall_percentage:.1f}%")
```

### 方式3：快速演示

```bash
cd /root/.cache/ai_Code
python ai_test_suite/quickstart.py
```

---

## 🔧 封装好的工具类

### 1. 模型接口（models/）

```python
# 统一接口，支持多种模型
model.generate(prompt, system_prompt, temperature, max_tokens)

# HuggingFace本地模型
model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct", device="cuda")

# OpenAI兼容API
model = OpenAIModel("moonshot-v1-8k", api_key="...", base_url="...")
```

### 2. 题目管理（questions/）

```python
# 创建题目
q = Question(
    id="custom_001",
    category=QuestionCategory.LOGIC,
    difficulty=DifficultyLevel.MEDIUM,
    title="题目名称",
    content="题目内容",
    answer="参考答案",
    keywords=["关键词"],
)

# 管理题目库
bank = QuestionBank()
bank.add(q)
bank.save_to_json("questions.json")
bank.load_from_json("questions.json")
```

### 3. 评分系统（evaluator/）

```python
# 规则评分（自动）
evaluator = RuleBasedEvaluator()

# LLM评分（更准确，需要额外API调用）
judge_model = OpenAIModel("gpt-4", ...)
evaluator = LLMBasedEvaluator(judge_model)

# 评分
result = evaluator.evaluate(answer, question)
print(result.score, result.feedback)
```

### 4. 报告生成（reporters/）

```python
# 控制台报告（彩色）
reporter = ConsoleReporter(verbose=True)
reporter.report(result)

# JSON报告
reporter = JSONReporter()
reporter.report(result, "output.json")

# Markdown报告
reporter = MarkdownReporter()
reporter.report(result, "report.md")
```

### 5. 测试运行器（runner.py）

```python
runner = TestRunner(
    model=model,
    evaluator=evaluator,
    reporter=reporter,
)

# 完整测试
result = runner.run()

# 快速测试
result = runner.run_quick_test(num_questions=5)

# 分类测试
result = runner.run_category_test("logic")

# 多模型对比
results = runner.benchmark([model1, model2, model3])
```

---

## 🎯 评分标准

| 分数段 | 等级 | 能力评估 |
|--------|------|---------|
| 90-100 | 🌟 卓越 | 接近人类专家水平 |
| 70-89 | ✅ 良好 | 强推理与抽象能力 |
| 60-69 | ⚠️ 及格 | 良好推理，抽象有限 |
| 0-59 | ❌ 不及格 | 基础模式匹配 |

---

## 📝 报告示例

运行后会生成包含以下内容的报告：

1. **总体得分**：总分、百分比、等级
2. **分类统计**：各类别的得分分布
3. **详细结果**：每道题的得分、评价、建议
4. **模型统计**：调用次数、延迟、token用量

---

## 🛠️ 扩展开发

### 添加新题目

在 `questions/builtin.py` 中添加新的 Question 对象，或使用：

```python
bank = QuestionBank()
bank.load_from_json("my_questions.json")
```

### 自定义评分

```python
def my_evaluator(answer, question):
    # 自定义评分逻辑
    return score, feedback

question.evaluator = my_evaluator
```

### 添加新模型支持

继承 `ModelInterface` 基类，实现 `generate` 方法。

---

## 📚 文件清单

共 **27** 个Python文件 + **3** 个文档：

- 核心模块：8个
- 模型接口：5个
- 题目管理：3个
- 评分系统：3个
- 报告生成：4个
- 使用示例：5个
- 工具脚本：2个
- 文档：3个

---

## ✨ 特色功能

1. **陷阱题目**：第2题、第12题设计为反常识陷阱，测试AI是否盲目套用模板
2. **开放性问题**：第19-20题无标准答案，关注论证过程
3. **元认知测试**：最后一题要求AI自我反思
4. **多维度评分**：不仅看对错，还看关键词、结构、深度
5. **可视化报告**：彩色控制台输出 + 美观Markdown报告

---

**开始使用**：
```bash
cd /root/.cache/ai_Code
python ai_test_suite/quickstart.py
```

祝你测试愉快！🎉
