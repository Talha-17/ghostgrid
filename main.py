
from fastapi import FastAPI
import sqlite3
from database import DB_PATH
from ai_engine import query_local_ai

app = FastAPI(title="GhostGrid Edge Control Center", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "GhostGrid Edge Node",
        "mode": "Fully Offline Capable"
    }

@app.get("/logs")
def get_sensor_logs(limit: int = 10):
    """Retrieves the latest sensor readings saved locally in SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sensor_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"recent_logs": rows}

@app.get("/ask-ai")
async def ask_local_ai(prompt: str):
    """Sends a query to the local AI engine running offline."""
    response = await query_local_ai(prompt)
    return {"prompt": prompt, "ai_response": response}