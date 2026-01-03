from openai import OpenAI
import yaml

client = OpenAI(api_key=yaml.safe_load(open("..\\credentials.yml"))["openai"])

input = input("Enter your question here: ")

response = client.responses.create(
    model="gpt-3.5-turbo",
    input=input
)

print(response)
