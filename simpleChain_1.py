## install -> pip install grandalf

import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=""
)

prompt = PromptTemplate(
    template='Generate 5 interesting facts about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic':'cricket'})

print(result)

chain.get_graph().print_ascii()