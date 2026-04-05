# graph_rag_kimi.py
import requests
from neo4j import GraphDatabase
from openai import OpenAI  # Kimi 兼容 OpenAI SDK

# 从 config.py 导入配置
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, KIMI_API_KEY

# 初始化 Kimi 客户端（兼容 OpenAI SDK）
client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1"
)

def get_graph_context(company_name):
    """从 Neo4j 获取公司关系网络"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    context = []
    
    try:
        with driver.session() as session:
            # 查直接关系（供应、竞争、合作）
            result = session.run("""
                MATCH (c:Company {name: $name})-[r:RELATION]-(other:Company)
                RETURN other.name as other, 
                       r.type as rel_type, 
                       r.product as product
                LIMIT 20
            """, name=company_name)
            
            for record in result:
                rel_desc = f"{record['other']}与{company_name}有{record['rel_type']}关系"
                if record['product']:
                    rel_desc += f"，涉及产品：{record['product']}"
                context.append(rel_desc)
                
            # 查间接关系（二级供应商/客户）
            if len(context) < 3:
                indirect = session.run("""
                    MATCH (c:Company {name: $name})--(mid)--(other:Company)
                    WHERE other.name <> $name AND mid <> c
                    RETURN other.name as other, mid.name as bridge, 
                           '间接关联' as rel_type
                    LIMIT 5
                """, name=company_name)
                for r in indirect:
                    context.append(f"通过{r['bridge']}间接关联：{r['other']}")
                    
    finally:
        driver.close()
    
    return "\n".join(context) if context else "未找到相关供应链信息"

def ask_graph_rag(question: str, model: str = "moonshot-v1-8k") -> dict:
    """
    Graph RAG 主流程
    返回结构化结果，方便 API 使用
    """
    # 简单实体识别（生产环境可用 NLP 库）
    companies = ["宁德时代", "比亚迪", "特斯拉", "小鹏", "蔚来", "蜂巢能源"]
    target = None
    for c in companies:
        if c in question:
            target = c
            break
    
    if not target:
        return {
            "answer": "请提问关于新能源汽车产业链的问题（如宁德时代、比亚迪等）",
            "context_used": 0,
            "company": None
        }
    
    # 1. 检索图谱
    context = get_graph_context(target)
    context_lines = [l for l in context.split('\n') if l.strip()]
    
    # 2. 构建系统提示
    system_prompt = """你是新能源产业链分析专家。严格基于提供的知识图谱数据回答问题：
- 优先使用图谱中的供应/竞争/合作关系
- 如果信息不足，明确说明"根据现有图谱数据..."
- 回答简洁，控制在200字以内"""

    user_prompt = f"""知识图谱信息：
{context}

用户问题：{question}

请基于上述事实回答。"""

    # 3. 调用 Kimi
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # 事实性问题用低温度
            max_tokens=500
        )
        
        return {
            "question": question,
            "company": target,
            "answer": response.choices[0].message.content,
            "context_used": len(context_lines),
            "context_preview": context_lines[:3] if context_lines else [],
            "model": model,
            "tokens": {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens
            } if response.usage else {}
        }
        
    except Exception as e:
        return {
            "question": question,
            "company": target,
            "answer": f"AI 生成失败: {str(e)}",
            "error": str(e),
            "context_used": len(context_lines)
        }

if __name__ == "__main__":
    # 本地测试
    test_questions = [
        "宁德时代的主要供应商是谁？",
        "比亚迪和宁德时代有什么关系？",
        "蜂巢能源的竞争对手有哪些？"
    ]
    
    for q in test_questions:
        print(f"\n❓ {q}")
        result = ask_graph_rag(q)
        print(f"💡 {result['answer']}")
        print(f"📊 使用上下文: {result['context_used']} 条")
