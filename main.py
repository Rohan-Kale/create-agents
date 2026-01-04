from openai import OpenAI
import yaml

client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])

curr_session = []

def store_response(question, answer):
    with open("responses.txt", "a") as f:
        f.write(f"Question: {question}\nAnswer: {answer}\n\n")

def interact_with_ai():
    if not curr_session:
        inp = input("What tasks do you have to complete today?: ")
    else:
        inp = input("What else would you like me to do for you?: ")
    response = client.responses.create(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        input=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps the user create daily schedules based on their tasks for the day."
            },
            {"role": "user", "content": str(curr_session) + inp},
        ]
    )

    res =response.output_text
    print(res + "\n\n")
    curr_session.append((inp, res))

def main():
    while True:
        interact_with_ai()
        if input("Do you want to ask another question? (y/n): ").lower() != 'y':
            break
    store_response(*curr_session)

main()
