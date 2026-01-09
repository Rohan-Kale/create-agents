import sqlite3
import json
from datetime import datetime
from schedule import DailyScheduleFormat
import os

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
            feedback TEXT,
            created_at TEXT NOT NULL
        )
        """)

def append_to_memory(schedule: DailyScheduleFormat):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO schedules (day, data, feedback, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(day) DO UPDATE SET
                data=excluded.data,
                feedback=excluded.feedback,
                created_at=excluded.created_at
            """,
            (
                schedule.day,
                json.dumps(schedule.model_dump()),
                schedule.feedback if hasattr(schedule, 'feedback') else "",
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

def load_day(day_str):
    '''
    Load the schedule for a specific day.
    '''
    with get_connection() as conn:
        row = conn.execute("SELECT data FROM schedules WHERE day=?", (day_str,)).fetchone()
        print(row)
        if row:
            return DailyScheduleFormat.model_validate(json.loads(row[0]))      
        return None

def get_summary_for_day(day: str) -> dict | None:
    '''
    Get the summary for a specific day.
    '''
    schedule = load_day(day)
    if not schedule:
        return None
    completed = [t for t in schedule.tasks if t.completed]
    missed = [t for t in schedule.tasks if not t.completed]
    total = len(schedule.tasks)
    return {
        "day": day,
        "completed": completed,
        "missed": missed,
        "total": total,
        "completion_rate": len(completed) / total if total > 0 else 0
    }

def load_last_n_days(n: int) -> list[DailyScheduleFormat]:
    """
    Load the last n schedules in chronological order.
    """
    query = "SELECT data FROM schedules ORDER BY created_at DESC LIMIT ?"
    schedules = []
    with get_connection() as conn:
        for (data,) in conn.execute(query, (n,)):
            schedules.append(DailyScheduleFormat.model_validate(json.loads(data)))
    return list(reversed(schedules))  # return oldest first

def save_feedback(day: str, feedback: str):
    """
    Attach feedback to a day's schedule.
    """
    with get_connection() as conn:
        conn.execute(
            "UPDATE schedules SET feedback=? WHERE day=?",
            (feedback, day)
        )
