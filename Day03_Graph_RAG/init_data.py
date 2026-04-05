from neo4j import GraphDatabase

URI = "bolt://192.168.10.17:7687"
USER = "neo4j"
PASSWORD = "password"  # 如果不对，改成你实际设的密码

def init_data():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    with driver.session() as session:
        # 清空旧数据（可选）
        session.run("MATCH (n) DETACH DELETE n")
        
        # 创建公司节点
        companies = [
            ("宁德时代", "电池制造", 10000),
            ("天齐锂业", "锂矿开采", 5000),
            ("比亚迪", "汽车制造", 80000),
            ("特斯拉", "汽车制造", 120000),
            ("江西铜业", "铜矿开采", 3000)
        ]
        
        for name, industry, employees in companies:
            session.run("""
                CREATE (c:Company {
                    name: $name, 
                    industry: $industry, 
                    employees: $employees
                })
            """, name=name, industry=industry, employees=employees)
        
        # 创建供应关系
        relations = [
            ("天齐锂业", "宁德时代", "供应", "电池级碳酸锂"),
            ("江西铜业", "宁德时代", "合作", "铜箔材料"),
            ("宁德时代", "特斯拉", "供应", "动力电池"),
            ("宁德时代", "比亚迪", "竞争", "动力电池市场")
        ]
        
        for from_company, to_company, rel_type, product in relations:
            session.run("""
                MATCH (a:Company {name: $from_name}), (b:Company {name: $to_name})
                CREATE (a)-[r:RELATION {
                    type: $rel_type,
                    product: $product
                }]->(b)
            """, from_name=from_company, to_name=to_company, rel_type=rel_type, product=product)
        
        # 验证数据
        result = session.run("MATCH (n) RETURN count(n) as count")
        count = result.single()["count"]
        
        result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
        rel_count = result.single()["rel_count"]
        
        print(f"✅ 数据初始化完成！")
        print(f"   节点数: {count}")
        print(f"   关系数: {rel_count}")
    
    driver.close()

if __name__ == "__main__":
    init_data()
