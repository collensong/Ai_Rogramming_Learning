from db_connector import Neo4jConnector

db = Neo4jConnector()
db.connect()

employees = [
    ("E007", "Grace", "CTO", 6),
    ("E002", "Bob", "Manager", 4),
    ("E003", "Carol", "Tech Lead", 4),
    ("E001", "Alice", "Engineer", 3),
    ("E009", "Henry", "Junior", 2),
]

print("创建节点...")
for emp_id, name, role, level in employees:
    db.run("""
        MERGE (p:Person {emp_id: $id})
        SET p.name = $name, p.role = $role, p.level = $level
    """, {"id": emp_id, "name": name, "role": role, "level": level})

relations = [("E007", "E002"), ("E007", "E003"), ("E002", "E001"), ("E002", "E009")]

print("创建关系...")
for mgr, sub in relations:
    db.run("""
        MATCH (m:Person {emp_id: $mgr}), (s:Person {emp_id: $sub})
        MERGE (m)-[:MANAGES]->(s)
    """, {"mgr": mgr, "sub": sub})

stats = db.get_stats()
print(f"结果：{stats['nodes']} 节点，{stats['relations']} 关系")

db.close()
