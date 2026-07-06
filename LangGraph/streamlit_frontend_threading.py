# pip install langchain_groq
#
#   INPUT  ->  | LLM | -> OUTPUT 
#   


from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key = os.getenv("GROQ_API_KEY")
)

# create a state

class LLMState(TypedDict):

    question: str
    answer: str

def llm_qa(state: LLMState) -> LLMState:

    # extract the question from state
    question = state['question']

    # form a prompt
    prompt = f'Answer the following question {question}'

    # ask that question to the LLM
    answer = llm.invoke(prompt).content

    # update the answer in the state
    state['answer'] = answer

    return state

# create our graph

graph = StateGraph(LLMState)

# add nodes
graph.add_node('llm_qa', llm_qa)

# add edges
graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

# compile
workflow = graph.compile()

# execute

intial_state = {'question': 'what is LangGraph ?'}

final_state = workflow.invoke(intial_state)

print(final_state['answer'])