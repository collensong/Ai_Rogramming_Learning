from neo4j import GraphDatabase

URI = "bolt://192.168.10.17:7687"
USER = "neo4j"
PASSWORD = "password"  # 如果不对，改成你实际设的密码

try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"✅ 连接成功！图谱中有 {count} 个节点")
    driver.close()
except Exception as e:
    print(f"❌ 连接失败: {e}")