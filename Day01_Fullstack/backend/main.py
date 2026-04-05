from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# 数据库设置
DB_FILE = "messages.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY, name TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# 启动时初始化
@app.on_event("startup")
async def startup():
    init_db()

class Message(BaseModel):
    name: str
    content: str

@app.get("/messages")
def get_messages():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    rows = c.fetchall()
    db.close()
    return [{"id": r["id"], "name": r["name"], "content": r["content"]} for r in rows]

@app.post("/submit")
def submit_message(msg: Message):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO messages (name, content) VALUES (?, ?)", 
              (msg.name, msg.content))
    db.commit()
    db.close()
    return {"status": "ok"}

@app.delete("/delete/{message_id}")
def delete_message(message_id: int):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    db.commit()
    db.close()
    return {"status": "ok"}

@app.get("/")
def health():
    return {"message": "后端运行中！", "db": "sqlite"}

@app.put("/messages/{msg_id}")
def update_message(msg_id: int, msg: Message):
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE messages SET name=?, content=? WHERE id=?", 
              (msg.name, msg.content, msg_id))
    db.commit()
    rows_affected = c.rowcount
    db.close()
    
    if rows_affected == 0:
        return {"status": "error", "message": "留言不存在"}
    return {"status": "ok", "updated_id": msg_id}
