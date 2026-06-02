# https://docs.langchain.com/oss/python/integrations/chat/anthropic

import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

import os
from langchain_openrouter import ChatOpenRouter

os.environ["OPENROUTER_API_KEY"] = "sk-or-v1-"

# Initialize model
llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0.7,
    max_tokens=200
)

# Invoke model
response = llm.invoke("Explain Agentic AI in simple terms in 15 words.")

print(response.content)