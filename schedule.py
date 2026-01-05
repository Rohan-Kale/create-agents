from pydantic import BaseModel

class ScheduleItem(BaseModel):
    time: str
    task: str


class DailyScheduleFormat(BaseModel):
    day: str
    tasks: list[str]
    schedule: list[ScheduleItem]        # must create ScheduleItem object since dict is not supported by OpenAI
