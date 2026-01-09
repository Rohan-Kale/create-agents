from pydantic import BaseModel
from typing import List

class ScheduleItem(BaseModel):
    time: str
    task_id: int

class TaskItem(BaseModel):
    id: int
    name: str
    completed: bool = False

class DailyScheduleFormat(BaseModel):
    day: str
    tasks: list[TaskItem]
    schedule: list[ScheduleItem]        # must create ScheduleItem object since dict is not supported by OpenAI

class DraftRequest(BaseModel):
    tasks: List[str]
    day: str

class DraftResponse(BaseModel):
    schedule: DailyScheduleFormat

class ConfirmRequest(BaseModel):
    schedule: DailyScheduleFormat

class CompleteTasksRequest(BaseModel):
    day: str
    completed_task_ids: List[int]   # marks the task complete given task.ids

class ReflectionResponse(BaseModel):
    summary: str

