# The demo what we have done in the previous example is old way of doing it and with a more number of lines.
# LandChain provides the parsers that make the same job easy
#  JSON will help to parse the data.


from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key="",
)

parser = JsonOutputParser()

template = PromptTemplate(
    template='Give me 5 facts about {topic} \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

result = chain.invoke({'topic':'Agentic AI'})

print(result)