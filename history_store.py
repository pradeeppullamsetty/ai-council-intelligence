"""Local SQLite storage for AI Council sessions."""
import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).with_name("council_history.db")

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            topic TEXT NOT NULL,
            verdict TEXT NOT NULL,
            payload TEXT NOT NULL
        )""")

def save_session(data: dict):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO sessions(created_at, topic, verdict, payload) VALUES(?,?,?,?)",
                    (data.get("generated_at", datetime.now().isoformat(timespec="seconds")),
                     data.get("topic", "Untitled"), data.get("verdict", ""),
                     json.dumps(data, ensure_ascii=False)))

def list_sessions(limit: int = 50):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        rows = con.execute("SELECT id, created_at, topic, verdict, payload FROM sessions ORDER BY id DESC LIMIT ?",
                           (limit,)).fetchall()
    return [{"id": r[0], "created_at": r[1], "topic": r[2], "verdict": r[3],
             "payload": json.loads(r[4])} for r in rows]
