import sqlite3, json
from pathlib import Path
DB = Path(__file__).parents[3] / "growthpilot.db"
def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("CREATE TABLE IF NOT EXISTS audit_events (id INTEGER PRIMARY KEY, ts DATETIME DEFAULT CURRENT_TIMESTAMP, event TEXT, action TEXT, status TEXT, explanation TEXT, payload TEXT)")
def log(event, action, status, explanation, payload=None):
    init_db()
    with sqlite3.connect(DB) as c:
        c.execute("INSERT INTO audit_events(event,action,status,explanation,payload) VALUES (?,?,?,?,?)", (event, action, status, explanation, json.dumps(payload or {})))
def recent(limit=100):
    init_db()
    with sqlite3.connect(DB) as c:
        rows=c.execute("SELECT id,ts,event,action,status,explanation,payload FROM audit_events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(zip(["id","timestamp","event","action","status","explanation","payload"], r)) for r in rows]
