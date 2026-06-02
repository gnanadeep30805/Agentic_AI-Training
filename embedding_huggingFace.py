# pip install -U langchain langchain-openai

import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key="or-v1-",
    check_embedding_ctx_length=False
)

vector = embeddings.embed_query(
    "What is Retrieval Augmented Generation?"
)

print(vector[:10])