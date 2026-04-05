from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        # 场景B：代码在服务器上，直接连容器映射的端口
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "dev123")  # 你的实际密码
        self.driver = None
    
    def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self.driver.verify_connectivity()
        print(f"✅ 已连接: {self.uri}")
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def run(self, query: str, parameters: Dict = None) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def get_stats(self) -> Dict:
        result = self.run("MATCH (n) RETURN count(n) as nodes")
        rel_result = self.run("MATCH ()-[r]->() RETURN count(r) as relations")
        return {
            "nodes": result[0]["nodes"] if result else 0,
            "relations": rel_result[0]["relations"] if rel_result else 0
        }

if __name__ == "__main__":
    db = Neo4jConnector()
    db.connect()
    print(db.get_stats())
    db.close()
