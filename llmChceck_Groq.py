
##  pip install groq
##  pip install langchain langchain-groq
##  https://docs.langchain.com/oss/python/integrations/chat/groq

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=""
)

messages = [
    (
        "system",
        "You are a helpful assistant,,,.",
    ),
    (
        "human", 
        " write something about Agentic AI."),
    ]


# Invoke model
response = llm.invoke(messages)

print(response)