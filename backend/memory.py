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


def save_feedback(day: str, feedback: str):
    """
    Attach feedback to a day's schedule.
    """
    with get_connection() as conn:
        conn.execute(
            "UPDATE schedules SET feedback=? WHERE day=?",
            (feedback, day)
        )

def update_completed_tasks(day: str, completed_ids: list[int]):
    schedule = load_day(day)
    if not schedule:
        return None

    for task in schedule.tasks:
        task.completed = task.id in completed_ids

    append_to_memory(schedule)
    return schedule
