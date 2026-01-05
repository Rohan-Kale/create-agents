from openai import OpenAI
import yaml
from pydantic import BaseModel
import json
from pathlib import Path


class ScheduleItem(BaseModel):
    time: str
    task: str


class DailyScheduleFormat(BaseModel):
    day: str
    tasks: list[str]
    schedule: list[ScheduleItem]        # must create scheduleitem object since dict is not supported by OpenAI

first_run = True

client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])


def append_to_memory(DailyScheduleFormat):
    memory_file = Path("memory.json")
    if memory_file.exists():
        with open("memory.json", "r") as f:
            existing_memory = json.load(f)
    else:
        existing_memory = []

    existing_memory.append(DailyScheduleFormat.model_dump())

    with open("memory.json", "w") as f:
        json.dump(existing_memory, f, indent=2)

def interact_with_ai():
    if first_run:
        inp = input("What tasks do you have to complete today?: ")
    else:
        inp = input("What else would you like me to do for you?: ")
    response = client.responses.parse(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        input=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps the user create daily schedules based on their tasks for the day and the format given. "
                "It is completely up to you to determine the time frames in which the tasks should be completed, unless specified by the user."
                "Follow the format strictly and do not add any additional information outside of the format. MAKE SURE TO INCLUDE THINGS SUCH AS LUNCH, BREAKS, ETC.",
            },
            {"role": "user", "content": inp},
        ],
        text_format=DailyScheduleFormat,
    )

    res =response.output_parsed
    print(res)

    append_to_memory(res)

def main():
    while True:
        interact_with_ai()
        first_run = False
        if input("Do you want to ask another question? (y/n): ").lower() != 'y':
            break

main()
