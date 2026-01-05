import sqlite3
import json
from datetime import datetime
from schedule import DailyScheduleFormat

DB_PATH = "agent.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

def append_to_memory(schedule: DailyScheduleFormat):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO schedules (day, data, created_at)
            VALUES (?, ?, ?)
            """,
            (
                schedule.day,
                json.dumps(schedule.model_dump()),
                datetime.now().isoformat(),
            )
        )

def load_old_conversations(limit: int | None = None) -> list[DailyScheduleFormat]:
    query = """
        SELECT data
        FROM schedules
        ORDER BY created_at ASC
    """
    if limit:
        query += f" LIMIT {limit}"

    schedules = []
    with get_connection() as conn:
        for (data,) in conn.execute(query):
            schedules.append(
                DailyScheduleFormat.model_validate(json.loads(data))
            )

    return schedules
