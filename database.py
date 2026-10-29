import sqlite3
from datetime import datetime

DB_PATH = "ghostgrid_edge.db"

def init_db():
    """Initializes the local SQLite database for offline-first storage."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for sensor data and hardware logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            value REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            synced INTEGER DEFAULT 0
        )
    """)
    
    # Table for local AI audit logs and actions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("[GhostGrid] Local database initialized successfully.")

def log_sensor_data(sensor_id: str, value: float, status: str):
    """Saves sensor data locally, marking it as unsynced (0) until network returns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    
    cursor.execute(
        "INSERT INTO sensor_logs (sensor_id, value, status, timestamp, synced) VALUES (?, ?, ?, ?, 0)",
        (str(sensor_id), float(value), str(status), timestamp)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()