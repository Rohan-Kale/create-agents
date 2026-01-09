from openai import OpenAI
from backend.schemas import DailyScheduleFormat
import yaml


class Scheduler:
    def __init__(self):
        self.client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])
    
    def run(self, inp, date_str: str) -> DailyScheduleFormat:
        response = self.client.responses.parse(
            model="gpt-5-nano",
            tools=[{"type": "web_search"}],
            input=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps the user create daily schedules based on their tasks for the day."
                    f"TODAYS DAY IS {date_str} DO NOT FORGET TO USE THIS EXACT DATE IN THE SCHEDULE WITH THE FORMAT GIVEN."
                    "It is completely up to you to determine the time frames in which the tasks should be completed, unless specified by the user."
                    "Follow the format strictly and do not add any additional information outside of the format. MAKE SURE TO INCLUDE THINGS SUCH AS LUNCH, BREAKS, ETC."
                    "WHEN ADDING LUNCH BREAKS AND OTHER THINGS MAKE SURE NOT TO HALLUCINATE AND ADD TASKS THAT THE USER DID NOT ASK YOU TO ADD (I.E DIFFERENT TYPES OF HOMEWORK)",
                },
                {"role": "user", "content": inp},
            ],
            text_format=DailyScheduleFormat,
        )

        return response.output_parsed
