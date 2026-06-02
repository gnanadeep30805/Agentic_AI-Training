# The demo what we have done in the previous example is old way of doing it and with a more number of lines.
# LandChain provides the parsers that make the same job easy
# StrOutputParser will help to parse the data.

import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key="",
)

# 1st prompt -> detailed report
template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

# 2nd prompt -> summary
template2 = PromptTemplate(
    template='Write a 5 line summary on the following text. /n {text}',
    input_variables=['text']
)

# Parser 
parser = StrOutputParser()

# Template1 (Prompt Engineering) → LLM Model → Output Parser → Template2 (Second Prompt) → LLM Model → Output Parser → Final Response.

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic':'black hole'})

print(result)
