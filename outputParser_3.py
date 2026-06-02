# The demo what we have done in the previous example is old way of doing it and with a more number of lines.
# LandChain provides the parsers that make the same job easy
#  Pydantic will help to parse the data.


import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

class Person(BaseModel):

    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

chain = template | model | parser

final_result = chain.invoke({'place':'sri lankan'})

print(final_result)