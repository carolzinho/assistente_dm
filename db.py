import sqlite3
import json
from typing import Dict

DB_NAME = "assistant.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            user_id TEXT PRIMARY KEY,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_conversation_db(user_id: str) -> Dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT data FROM conversations WHERE user_id = ?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row[0])


def save_conversation_db(user_id: str, data: Dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (user_id, data)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET data=excluded.data
    """, (user_id, json.dumps(data)))

    conn.commit()
    conn.close()


def delete_conversation_db(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM conversations WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()
