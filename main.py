from openai import OpenAI
import yaml


session_mem = []
first_run = True
client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])
with open("responses.txt", "r") as f:
    session_mem = [f.read()]

def store_response(question, answer):
    with open("responses.txt", "a") as f:
        f.write(f"Question: {question}\nAnswer: {answer}\n\n")

def interact_with_ai():
    if first_run:
        inp = input("What tasks do you have to complete today?: ")
    else:
        inp = input("What else would you like me to do for you?: ")
    response = client.responses.create(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        input=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps the user create daily schedules based on their tasks for the day. Save "
                "the previous conversation history and use it to inform your responses.",
            },
            {"role": "user", "content": str(session_mem) + inp},
        ]
    )

    res =response.output_text
    print(res + "\n\n")
    session_mem.append((inp, res))

def main():
    while True:
        interact_with_ai()
        first_run = False
        if input("Do you want to ask another question? (y/n): ").lower() != 'y':
            break
        store_response(*session_mem[-1])
    store_response(*session_mem[-1])

main()
