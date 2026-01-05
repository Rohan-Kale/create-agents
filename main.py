from agents.scheduler import Scheduler
from memory import init_db, append_to_memory, load_old_conversations

def main():
    init_db()
    
    agent = Scheduler()

    past_memory = load_old_conversations()

    first_run = True

    while True:
        if first_run:
            user_input = input("What tasks do you have to complete today?: ")
        else:
            user_input = input("What else would you like me to do for you?: ")

        schedule = agent.run(user_input, past_memory)
        print("\nGenerated schedule:\n")
        print(schedule.model_dump_json(indent=2))

        append_to_memory(schedule)
        past_memory.append(schedule)

        first_run = False

        if input("\nDo you want to ask another question? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    main()
