"""
使用配置文件的示例代码
"""

# 方式1：从 config 模块导入
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, KIMI_API_KEY

print(f"Neo4j 地址: {NEO4J_URI}")
print(f"Neo4j 用户: {NEO4J_USER}")
print(f"Kimi API Key: {KIMI_API_KEY[:10]}...")

# 方式2：直接在代码中使用
from neo4j import GraphDatabase
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 方式3：调用 Kimi API
import requests

headers = {
    "Authorization": f"Bearer {KIMI_API_KEY}",
    "Content-Type": "application/json"
}

# 示例：发送请求到 Kimi
# response = requests.post(
#     "https://api.moonshot.cn/v1/chat/completions",
#     headers=headers,
#     json={
#         "model": "moonshot-v1-8k",
#         "messages": [{"role": "user", "content": "你好"}]
#     }
# )
