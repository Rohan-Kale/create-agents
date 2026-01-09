# summarizer_agent.py
from openai import OpenAI
from memory import load_day, save_feedback
from schedule import DailyScheduleFormat
import yaml

class SummarizerAgent:
    def __init__(self):
         self.client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])

    def reflect_on_day(self, day: str) -> str:
        """
        Collect reflections on today's tasks, optionally generate LLM summary.
        """
        schedule: DailyScheduleFormat = load_day(day)
        if not schedule:
            return f"No schedule found for {day}."

        # Collect feedback on each task
        task_feedback = {}
        print(f"\n--- Reflection for {day} ---\n")
        for task in schedule.tasks:
            completed = input(f"Did you complete '{task.name}'? (y/n): ").lower() == "y"
            task.completed = completed
            feedback = input(f"What did you like or dislike about '{task.name}'? (optional): ")
            task_feedback[task.name] = {
                "completed": completed,
                "feedback": feedback
            }

        # generate summary using LLM
        prompt = f"You are an AI coach. Summarize the user's reflections on their daily tasks,"
        " providing constructive advice for improvement."

        user_input = f"Todays tasks and reflections:\n{task_feedback}"

        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )

        summary_text = response.output_text.strip()

        # Save updated schedule back to memory
        save_feedback(day, feedback=summary_text)

        return summary_text
