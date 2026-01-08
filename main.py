from agents.scheduler import Scheduler
from memory import init_db, append_to_memory, load_old_conversations, load_day
from agents.summarizer import SummarizerAgent
from datetime import date

def mark_tasks(schedule):
    """
    Ask user which tasks were completed and which were missed.
    Returns updated schedule with completion info.
    """
    print("\nMark your tasks as completed or missed:")
    for task in schedule.tasks:
        response = input(f"Did you complete '{task.name}'? (y/n): ").lower()
        task.completed = response == "y"
    return schedule

def main():
    init_db()
    today_str = date.today().strftime("%A, %B %d, %Y")

    #check if there is a schedule for today
    schedule = load_day(today_str)

    print(" ---------------SCHEDULE FOR TODAY---------------", schedule)
    if schedule is None:
        print("Good morning! Let's create your schedule for today.")
        user_input = input("Enter the tasks you want to complete today: ")

        # Scheduler agent
        scheduler = Scheduler()
        schedule = scheduler.run(user_input, load_old_conversations())

        # Store the schedule in memory 
        append_to_memory(schedule)
        print("\nYour schedule for today has been saved:")
        print(schedule.model_dump_json(indent=2))
        print("\nYou can come back later to mark completed tasks and receive feedback.")
    else:
        print("Welcome back! Let's mark which tasks you completed today.")

        schedule = mark_tasks(schedule)

        # Save updated schedule back to memory
        append_to_memory(schedule)

        # Generate summary
        summarizer = SummarizerAgent(memory=None)
        summary_text = summarizer.reflect_on_day(today_str)
        print("\nDaily Summary & Feedback:\n")
        print(summary_text)

if __name__ == "__main__":
    main()
