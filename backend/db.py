import sqlite3
import json
from datetime import datetime
from backend.schemas import DailyScheduleFormat

conn = sqlite3.connect('schedules.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    day TEXT,
                    schedule TEXT,
                    created_at TEXT,
                )""")

def save_schedule_to_db(schedule: DailyScheduleFormat):
    cursor.execute("INSERT INTO schedules (day, schedule, created_at) VALUES (?, ?, ?)",
                   (schedule.day, json.dumps(schedule.model_dump()), datetime.now().isoformat()))
    conn.commit()

