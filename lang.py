import weaviate
import os
import dotenv
from langchain.vectorstores import Weaviate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
dotenv.load_dotenv()

WEAVIATE_URL = "http://172.22.48.1:8080/"

client = weaviate.Client(
    url=WEAVIATE_URL,  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"],
    }
)











# set-up chat model
chat = ChatOpenAI(temperature=0.6)
template = "You are a helpful assistant that answers questions based on excerpts from documents {input_documents}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt])
chain = LLMChain(llm=chat, prompt=chat_prompt)

# get documents from database

vector_store = Weaviate(client, "Econ_club_data", "page_text")
user_input = "What is the economic club scholarship program about?"
documents = vector_store.similarity_search_by_text(user_input, k=3)
string_documents = ""
for doc in documents:
    # convert doc to string
    string_documents = string_documents + str(doc) + "\n"


print(chain.run(input_documents=string_documents, text=user_input))
# print(chat(chat_prompt.format_prompt(input_language="English",
#       output_language="Russian", text="I love programming.").to_messages()).content)


# qa = RetrievalQA.from_chain_type(
#     llm=OpenAI(), chain_type="stuff", retriever=vector_store.as_retriever())
# query = "What is the objective of the economic club?"
# print(qa.run(query))
# chain(
#     {"question": "Explain the concept of retirement consumption puzzle"},
#     return_only_outputs=True,
# )
