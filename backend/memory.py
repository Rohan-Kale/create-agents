import sqlite3
import json
from datetime import datetime
from backend.schemas import DailyScheduleFormat

DB_PATH = "agent.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT UNIQUE NOT NULL,
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
            ON CONFLICT(day) DO UPDATE SET
                data = excluded.data,
                created_at = excluded.created_at
            """,
            (
                schedule.day,
                json.dumps(schedule.model_dump()),
                datetime.now().isoformat(),
            )
        )


def load_day(day_str: str) -> DailyScheduleFormat | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT data FROM schedules WHERE day=?",
            (day_str,)
        ).fetchone()

        if row:
            return DailyScheduleFormat.model_validate(json.loads(row[0]))

        return None

def update_completed_tasks(day: str, completed_ids: list[int]):
    schedule = load_day(day)
    if not schedule:
        return None

    for task in schedule.tasks:
        task.completed = task.id in completed_ids

    append_to_memory(schedule)
    return schedule

def save_feedback(day: str, summary: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE schedules SET feedback = ? WHERE day = ?",
            (summary, day)
        )

def load_feedback(day: str) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT feedback FROM schedules WHERE day = ?",
            (day,)
        ).fetchone()

    return row[0] if row and row[0] else None
