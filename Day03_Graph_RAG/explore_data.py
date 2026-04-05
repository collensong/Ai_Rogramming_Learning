from db_connector import Neo4jConnector

db = Neo4jConnector()
db.connect()

# 查看所有人员
print("=== 人员列表 ===")
persons = db.run("MATCH (p:Person) RETURN p.name, p.role, p.department ORDER BY p.level DESC")
for p in persons:
    print(f"{p['p.name']:10} | {p['p.role']:20} | {p['p.department']}")

# 查看项目参与情况（图遍历）
print("\n=== GraphRAG 项目团队 ===")
team = db.run("""
    MATCH (p:Person)-[w:WORKS_ON]->(pr:Project {name: 'GraphRAG Platform'})
    RETURN p.name, w.role, w.allocation
    ORDER BY w.allocation DESC
""")
for t in team:
    print(f"{t['p.name']:10} | {t['w.role']:15} | 投入{t['w.allocation']*100:.0f}%")

# 查看汇报链（路径查询）
print("\n=== Alice 的汇报链 ===")
chain = db.run("""
    MATCH path = shortestPath(
        (alice:Person {name: 'Alice'})-[:MANAGES*0..5]-(boss:Person {name: 'Grace'})
    )
    RETURN [n IN nodes(path) | n.name + '(' + n.role + ')'] AS chain
""")
print(" -> ".join(chain[0]['chain']))

db.close()
