"""
配置文件加载模块
使用方式:
    from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, KIMI_API_KEY
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件（如果存在）
load_dotenv()

# Neo4j 配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://192.168.10.17:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Kimi API 配置
KIMI_API_KEY = os.getenv("KIMI_API_KEY")

# 验证配置
if not KIMI_API_KEY:
    raise ValueError("""
❌ 缺少 KIMI_API_KEY 环境变量！

请按以下步骤配置：
1. 在 .env 文件中添加：KIMI_API_KEY=你的真实API密钥
2. 或在命令行设置：export KIMI_API_KEY="你的真实API密钥"
""")

# 打印配置（调试用，生产环境请删除）
if __name__ == "__main__":
    print(f"✅ Neo4j 配置: {NEO4J_URI} (用户: {NEO4J_USER})")
    print(f"✅ Kimi API Key: {'已配置' if KIMI_API_KEY else '未配置'}")
