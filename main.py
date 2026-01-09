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

        scheduler = Scheduler()

        schedule = None

        while True:
            # Generate or regenerate schedule
            schedule = scheduler.run(user_input, today_str)

            print("\n📅 Draft schedule:\n")
            print(schedule.model_dump_json(indent=2))

            print("\nWhat would you like to do?")
            print("1. Accept and save schedule")
            print("2. Edit tasks")
            print("3. Cancel")

            choice = input("Choose an option (1–3): ").strip()

            if choice == "1":
                append_to_memory(schedule)
                print("\nSchedule saved successfully!")
                print("You can come back later to mark completed tasks and receive feedback.")
                break

            elif choice == "2":
                user_input = input(
                    "\nEnter your updated tasks or instructions "
                    "(e.g., 'shorter gym session', 'no work after 8pm'): "
                )
                print("\nUpdating schedule...")
                continue

            elif choice == "3":
                print("\nSchedule creation canceled.")
                schedule = None
                break

            else:
                print("Invalid option. Please choose 1–3.")
    else:
        print("Welcome back! Let's mark which tasks you completed today.")

        # Generate summary
        summarizer = SummarizerAgent()
        summary_text = summarizer.reflect_on_day(today_str)
        print("\nDaily Summary & Feedback:\n")
        print(summary_text)

if __name__ == "__main__":
    main()
