# Day 03 - Graph RAG 知识图谱问答系统

基于 Neo4j 知识图谱 + Kimi AI 的 Graph RAG（检索增强生成）系统，实现企业供应链关系智能问答。

## 🎯 项目目标

- 学习 Neo4j 图数据库基础操作
- 掌握知识图谱构建方法
- 实现 Graph RAG 增强问答
- 理解向量检索 vs 图谱检索的差异

## 🏗️ 系统架构

```
用户问题
    ↓
实体识别（简单关键词匹配）
    ↓
Neo4j 图谱检索（关系查询）
    ↓
上下文组装
    ↓
Kimi AI 生成回答
    ↓
返回结果
```

## 📁 文件说明

| 文件 | 功能 |
|------|------|
| `config.py` | 统一配置管理，加载 .env 环境变量 |
| `graph_rag_kimi.py` | Graph RAG 主程序，问答入口 |
| `init_data.py` | 初始化 Neo4j 数据（公司节点和关系） |
| `query_test.py` | 查询测试工具 |
| `test_neo4j.py` | Neo4j 连接测试 |
| `explore_data.py` | 数据探索工具 |
| `db_connector.py` | 数据库连接封装 |
| `.env.example` | 环境变量模板 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install neo4j openai python-dotenv requests

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 Kimi API Key
```

### 2. 配置 .env

```env
# Neo4j 数据库配置
NEO4J_URI=bolt://192.168.10.17:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Kimi API 密钥（从 https://platform.moonshot.cn 获取）
KIMI_API_KEY=sk-your-api-key-here
```

### 3. 初始化数据

```bash
python init_data.py
```

会创建以下测试数据：
- **公司节点**：宁德时代、比亚迪、特斯拉、天齐锂业、江西铜业
- **关系类型**：供应、竞争、合作

### 4. 运行测试

```bash
# 测试 Neo4j 连接
python test_neo4j.py

# 运行 Graph RAG 问答
python graph_rag_kimi.py
```

## 💡 使用示例

### 方式一：命令行直接运行

```bash
python graph_rag_kimi.py
```

输出示例：
```
❓ 宁德时代的主要供应商是谁？
💡 宁德时代的主要供应商包括江西铜业和天齐锂业。江西铜业为宁德时代提供铜箔材料，而天齐锂业则供应电池级碳酸锂。
📊 使用上下文: 4 条
```

### 方式二：在代码中调用

```python
from graph_rag_kimi import ask_graph_rag

result = ask_graph_rag("特斯拉的电池是谁供应的？")
print(result["answer"])
print(f"使用了 {result['context_used']} 条图谱数据")
```

### 方式三：交互式提问

```python
from graph_rag_kimi import ask_graph_rag

while True:
    question = input("\n请输入问题（或 q 退出）：")
    if question.lower() == 'q':
        break
    
    result = ask_graph_rag(question)
    print(f"\n💡 {result['answer']}")
    print(f"📊 使用上下文: {result['context_used']} 条")
```

## 🧪 支持的问答类型

| 问题类型 | 示例 |
|----------|------|
| 供应商查询 | "宁德时代的主要供应商是谁？" |
| 客户关系 | "特斯拉的电池是谁供应的？" |
| 竞争关系 | "比亚迪和宁德时代有什么关系？" |
| 合作关系 | "江西铜业和哪些公司有合作？" |

## 🗃️ 数据结构

### 节点（Company）

```cypher
(:Company {
    name: "宁德时代",
    industry: "电池制造",
    employees: 10000
})
```

### 关系（RELATION）

```cypher
(:Company)-[:RELATION {
    type: "供应",        // 关系类型：供应/竞争/合作
    product: "动力电池"  // 涉及产品
}]->(:Company)
```

## 📊 查询示例

### 查看所有公司

```cypher
MATCH (n:Company) RETURN n.name, n.industry
```

### 查看某公司的所有关系

```cypher
MATCH (c:Company {name: "宁德时代"})-[r:RELATION]-(other)
RETURN other.name, r.type, r.product
```

### 查找供应商

```cypher
MATCH (supplier:Company)-[r:RELATION {type: "供应"}]->(c:Company {name: "宁德时代"})
RETURN supplier.name, r.product
```

## 🔧 常见问题

### 1. 连接 Neo4j 失败

- 检查 Neo4j 服务是否启动
- 确认 `NEO4J_URI`、`NEO4J_USER`、`NEO4J_PASSWORD` 配置正确
- 测试连接：`python test_neo4j.py`

### 2. Kimi API 401 错误

- 检查 `.env` 文件中的 `KIMI_API_KEY` 是否已替换为真实密钥
- 确认 API Key 有效且未过期
- 从 https://platform.moonshot.cn 获取新 Key

### 3. 找不到实体

当前使用简单关键词匹配，支持的公司列表：
```python
companies = ["宁德时代", "比亚迪", "特斯拉", "小鹏", "蔚来", "蜂巢能源"]
```

如需支持更多公司，修改 `graph_rag_kimi.py` 中的 `companies` 列表。

## 📚 学习要点

### Graph RAG 优势

1. **可解释性**：能展示答案来源的图谱关系
2. **精确性**：结构化查询避免向量检索的语义漂移
3. **关系推理**：支持多跳推理（A→B→C）

### vs 传统 RAG

| 特性 | 传统 RAG（向量） | Graph RAG（图谱） |
|------|-----------------|------------------|
| 检索方式 | 语义相似度 | 结构化查询 |
| 关系表达 | 弱 | 强（显式关系） |
| 可解释性 | 低 | 高（可追溯） |
| 适合场景 | 文档问答 | 关系推理 |

## 🔗 相关资源

- [Neo4j 官方文档](https://neo4j.com/docs/)
- [Kimi API 文档](https://platform.moonshot.cn/docs)
- [Graph RAG 论文](https://arxiv.org/abs/2404.16130)

## 📝 作业要求

1. ✅ 完成 Neo4j 环境搭建
2. ✅ 导入示例数据（5家公司，4条关系）
3. ✅ 实现 Graph RAG 问答
4. ✅ 测试至少 3 个不同问题
5. ⭐ 进阶：添加更多公司和关系
6. ⭐ 进阶：实现多跳推理查询

## 🏆 成果展示

运行成功后的输出示例：

```
❓ 宁德时代的主要供应商是谁？
💡 宁德时代的主要供应商包括江西铜业和天齐锂业。江西铜业为宁德时代提供铜箔材料，而天齐锂业则供应电池级碳酸锂。
📊 使用上下文: 4 条

❓ 比亚迪和宁德时代有什么关系？
💡 比亚迪与宁德时代在动力电池市场上存在竞争关系。根据知识图谱信息，两家公司都在争夺同一市场，即动力电池领域。
📊 使用上下文: 4 条
```

---

**Day 03 完成！** 🎉

下一步：尝试添加更多企业数据，构建更完整的供应链知识图谱！
