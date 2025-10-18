# fuzzer/store.py
import sqlite3
import json
from datetime import datetime
from typing import Optional

DB = "vibefuzz.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        endpoint TEXT,
        method TEXT,
        status INTEGER,
        latency_ms INTEGER,
        snippet TEXT,
        payload TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_finding(target, endpoint, method, status, latency_ms, snippet, payload):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    INSERT INTO findings (target, endpoint, method, status, latency_ms, snippet, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (target, endpoint, method, status, latency_ms, snippet[:200], json.dumps(payload), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_findings(limit=100):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT id, target, endpoint, method, status, latency_ms, snippet, payload, created_at FROM findings ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [
        {"id": r[0], "target": r[1], "endpoint": r[2], "method": r[3], "status": r[4], "latency_ms": r[5], "snippet": r[6], "payload": r[7], "created_at": r[8]}
        for r in rows
    ]
