from neo4j import GraphDatabase

URI = "bolt://192.168.10.17:7687"
USER = "neo4j"
PASSWORD = "password"

def query_suppliers(company_name):
    """查询某公司的供应商"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    with driver.session() as session:
        # 查询供应关系（谁供应给该公司）
        result = session.run("""
            MATCH (supplier:Company)-[r:RELATION {type: '供应'}]->(c:Company {name: $name})
            RETURN supplier.name as supplier_name, r.product as product
        """, name=company_name)
        
        suppliers = []
        for record in result:
            suppliers.append(f"{record['supplier_name']}（供应{record['product']}）")
        
        # 查询合作关系
        result = session.run("""
            MATCH (partner:Company)-[r:RELATION {type: '合作'}]->(c:Company {name: $name})
            RETURN partner.name as partner_name, r.product as product
        """, name=company_name)
        
        partners = []
        for record in result:
            partners.append(f"{record['partner_name']}（合作{record['product']}）")
        
        # 查询竞争对手
        result = session.run("""
            MATCH (c:Company {name: $name})-[r:RELATION {type: '竞争'}]->(competitor:Company)
            RETURN competitor.name as competitor_name, r.product as market
        """, name=company_name)
        
        competitors = []
        for record in result:
            competitors.append(f"{record['competitor_name']}（{record['market']}）")
    
    driver.close()
    
    return {
        "suppliers": suppliers,
        "partners": partners,
        "competitors": competitors
    }

if __name__ == "__main__":
    # 测试查询
    company = "宁德时代"
    result = query_suppliers(company)
    
    print(f"🔍 {company} 的供应链分析：")
    print(f"   供应商：{result['suppliers'] or '无'}")
    print(f"   合作伙伴：{result['partners'] or '无'}")
    print(f"   竞争对手：{result['competitors'] or '无'}")
