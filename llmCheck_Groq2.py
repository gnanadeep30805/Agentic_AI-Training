from langchain_groq import ChatGroq
from langchain.messages import HumanMessage

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=""
    )

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]

response = llm.invoke(messages)
print(response.content)