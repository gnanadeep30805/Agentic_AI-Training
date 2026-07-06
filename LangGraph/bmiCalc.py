from langgraph.graph import StateGraph, END, START, state
from typing import TypedDict

class BMIState(TypedDict):
    weight: float
    height: float
    bmi: float
    
def calculate_bmi(weight: float, height: float) -> float:
    weight = state['weight']
    height = state['height']
    
    bmi = weight / (height ** 2)
    state['bmi'] = bmi
    return state

bmi_graph = StateGraph[BMIState]()
bmi_graph.add_node('calculate_bmi',calculate_bmi)
    
bmi_graph.add_edge(START, 'calculate_bmi')
bmi_graph.add_edge('calculate_bmi', END)

workflow = bmi_graph.compile()

initial_values = {
    'weight': 70.0,
    'height': 1.75
}

response = workflow.invoke(initial_values)
print(response)