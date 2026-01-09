from openai import OpenAI
from schemas import DailyScheduleFormat
import yaml

class SummarizerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])

    def reflect_on_day(self, schedule: DailyScheduleFormat) -> str:
        """
        Generate a reflection/feedback for the day based on completed tasks.
        """
        # Convert schedule to readable string for the model
        tasks_summary = "\n".join(
            [
                f"- [{ 'X' if task.completed else ' ' }] {task.name}"
                for task in schedule.tasks
            ]
        )

        system_prompt = (
            "You are an AI assistant that helps the user reflect on their day. "
            "Given a schedule with tasks and whether each task was completed, "
            "ask questions about how the day went, give feedback, "
            "and provide suggestions for improvement. "
            "Focus on what the user completed, what was missed, and how they can improve tomorrow. "
            "Do NOT add or remove any tasks. IGNORE TASKS SUCH AS BREAKS OR LUNCH. "
        )

        user_prompt = f"Schedule for {schedule.day}:\n{tasks_summary}"

        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        return response.output_text 
