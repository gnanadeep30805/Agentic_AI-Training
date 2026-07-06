from langgraph.graph import START, END, StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

class LLMWorkflowState(TypedDict):
    question: str
    answer: str
    
def ask_question(state: LLMWorkflowState) -> LLMWorkflowState:
    question = state['question']
    
    messages = [
        (
            "system",
            "You are a helpful assistant.",
        ),
        (
            "human", 
            question,
        ),
    ]

    response = llm.invoke(messages)
    state['answer'] = response
    return state

llm_workflow = StateGraph[LLMWorkflowState]()
llm_workflow.add_node('ask_question', ask_question)

llm_workflow.add_edge(START, 'ask_question')
llm_workflow.add_edge('ask_question', END)

workflow = llm_workflow.compile()

response = workflow.invoke({'question': 'What is Agentic AI?'})
print(response)