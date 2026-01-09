from pydantic import BaseModel

class ScheduleItem(BaseModel):
    time: str
    task: str

class TaskItem(BaseModel):
    name: str
    completed: bool = False


class DailyScheduleFormat(BaseModel):
    day: str
    tasks: list[TaskItem]
    schedule: list[ScheduleItem]        # must create ScheduleItem object since dict is not supported by OpenAI
