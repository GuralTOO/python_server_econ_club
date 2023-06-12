import weaviate
import os
import dotenv
import json
import openai
from decouple import config

dotenv.load_dotenv()
openai.api_key = config("OPENAI_API_KEY")
OPEN_API_KEY = os.getenv('OPENAI_API_KEY')

print("opening weaviate")

WEAVIATE_URL = "http://157.230.62.148:8080/"

client = weaviate.Client(
    url=WEAVIATE_URL,  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": OPEN_API_KEY,
    }
)

print(client.schema.get())


def search_items(class_name, variables=[""], text_query="", k=10):
    results = client.query.get(class_name=class_name, properties=variables).with_near_text(
        {"concepts": text_query}).with_limit(k).do()
    return results["data"]["Get"][class_name]


def get_answer(question: str):
    context = search_items(class_name="Econ_club_data", variables=[
        "page_text"], text_query=question, k=5)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant that answers questions based on excerpts from the following documents:" + str(context)},
                  {"role": "user", "content": "This is my question: " + question}],
        max_tokens=2500,
        temperature=0.3,
    )
    return response.choices[0].message.content


def get_answer_stream(question: str):
    context = search_items(class_name="Econ_club_data", variables=[
        "page_text"], text_query=question, k=5)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant that answers questions based on excerpts from the following documents:" + str(context)},
                  {"role": "user", "content": "This is my question: " + question}],
        max_tokens=2500,
        temperature=0.3,
        stream=True,
    )
    for part in response:
        print(part)
        # check if part['choices'][0]['delta'] has 'content' key
        if 'content' in part['choices'][0]['delta']:
            yield part['choices'][0]['delta']['content']


# print(get_answer("What is the economic club scholarship program about?"))
# print(response)
# print(response.choices[0].message.content)
# return json.dumps({"answer": response.choices[0].message.content, "sources": context_json['sources']})
