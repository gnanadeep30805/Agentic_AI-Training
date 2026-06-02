import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key="",
)


# 1st prompt -> detailed report
template1 = PromptTemplate(
    template='Write a detailed report on {topic} in 100 words.',
    input_variables=['topic']
)

# 2nd prompt -> summary
template2 = PromptTemplate(
    template='Write a 5 line summary on the following text. /n {text}',
    input_variables=['text']
)

prompt1 = template1.invoke({'topic':'black hole'})

result = model.invoke(prompt1)

prompt2 = template2.invoke({'text':result.content})

result1 = model.invoke(prompt2)

print(result1.content)
