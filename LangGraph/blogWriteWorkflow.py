from langgraph.graph import StateGraph, START, END
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

class BlogWorkflowState(TypedDict):
    topic: str
    outline: str
    content: str
    
def generate_outline(state: BlogWorkflowState) -> BlogWorkflowState:
    title = state['topic']
    
    outline = llm.invoke(f"Generate a detailed outline for {title}")
    
    state['outline'] = outline
    return state
    
def generate_content(state: BlogWorkflowState) -> BlogWorkflowState:
    title = state['topic']
    outline = state['outline']
    
    prompt = f"Write a blog post based on the following outline: {outline}"
    content = llm.invoke(prompt)
    state['content'] = content
    state['outline'] = outline
    return state

graph = StateGraph[BlogWorkflowState]()

graph.add_node('outline_node', generate_outline)
graph.add_node('content_node', generate_content)

graph.add_edge(START, 'outline_node')
graph.add_edge('outline_node', 'content_node')
graph.add_edge('content_node', END)

workflow = graph.compile()

response = workflow.invoke({'topic': 'Rapid growth of AI'})
print(response['content'])