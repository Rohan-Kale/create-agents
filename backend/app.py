from agents.scheduler import Scheduler
from agents.summarizer import SummarizerAgent
from datetime import date
from memory import init_db, append_to_memory, load_day
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

@app.post("/schedule/draft", response_model=DraftResponse)
def draft_schedule(request: DraftRequest):
    schedule = scheduler.run(", ".join(request.tasks), request.day)
    return DraftResponse(schedule=schedule)

@app.post("/schedule/confirm")
def confirm_schedule(request: ConfirmRequest):
    append_to_memory(request.schedule)
    return {"status": "schedule saved"}

@app.post("/schedule/complete")
def complete_tasks(request: CompleteTasksRequest):
    schedule = load_day(request.day)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule found for this day")

    for task in schedule.tasks:
        if task.id in request.completed_task_ids:
            task.completed = True

    append_to_memory(schedule)
    return {"status": "tasks updated"}

@app.get("/reflect/{day}", response_model=ReflectionResponse)
def reflect_on_day(day: str):
    schedule = load_day(day)
    if not schedule:
        raise HTTPException(status_code=404, detail="No schedule found for this day")
    
    summary = summarizer.reflect_on_day(day)
    return ReflectionResponse(summary=summary)
