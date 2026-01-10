from agents.scheduler import Scheduler
from agents.summarizer import SummarizerAgent
from datetime import date
from memory import init_db, append_to_memory, load_day, update_completed_tasks, save_feedback, load_feedback
from fastapi import FastAPI, HTTPException
from backend.schemas import (
    DraftRequest, DraftResponse,
    ConfirmRequest, CompleteTasksRequest, ReflectionResponse,
    DailyScheduleFormat
)


app = FastAPI()
init_db()


scheduler = Scheduler()
summarizer = SummarizerAgent()

@app.post("/draft", response_model=DraftResponse)
def draft_schedule(request: DraftRequest):
    schedule = scheduler.run(", ".join(request.tasks), request.day)
    return DraftResponse(schedule=schedule)

@app.post("/confirm")
def confirm_schedule(request: ConfirmRequest):
    append_to_memory(request.schedule)
    return {"status": "schedule saved"}

@app.get("/schedule/{day}", response_model=DailyScheduleFormat)
def get_schedule(day: str):
    schedule = load_day(day)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@app.post("/complete/{day}", response_model=DailyScheduleFormat)
def complete_tasks(day: str, req: CompleteTasksRequest):
    schedule = update_completed_tasks(day, req.completed_task_ids)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@app.post("/reflect/{day}", response_model=ReflectionResponse)
def reflect(day: str):
    schedule = load_day(day)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    summary = summarizer.reflect_on_day(schedule)
    save_feedback(day, summary)
    return ReflectionResponse(summary=summary)

