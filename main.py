from agents.scheduler import Scheduler
from memory import init_db, append_to_memory, load_old_conversations, load_day
from agents.summarizer import SummarizerAgent
from datetime import date


def main():
    init_db()
    today_str = date.today().strftime("%A, %B ") + str(date.today().day) + date.today().strftime(", %Y")
    print(today_str)

    #check if there is a schedule for today
    schedule = load_day(today_str)
    print(schedule)

    if schedule is None:
        print("Good morning! Let's create your schedule for today.")
        user_input = input("Enter the tasks you want to complete today: ")

        # Scheduler agent
        scheduler = Scheduler()
        schedule = scheduler.run(user_input, today_str)

        # Store the schedule in memory 
        append_to_memory(schedule)
        print("\nYour schedule for today has been saved:")
        print(schedule.model_dump_json(indent=2))
        print("\nYou can come back later to mark completed tasks and receive feedback.")
    else:
        print("Welcome back! Let's mark which tasks you completed today.")
        # Save updated schedule back to memory
        append_to_memory(schedule)

        # Generate summary
        summarizer = SummarizerAgent()
        summary_text = summarizer.reflect_on_day(today_str)
        print("\nDaily Summary & Feedback:\n")
        print(summary_text)

if __name__ == "__main__":
    main()
