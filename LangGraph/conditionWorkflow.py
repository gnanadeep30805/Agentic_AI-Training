from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    category: str
    response:str

def classify_query(state:AgentState):
    query = state['query']

    if any(word in query for word in ["error", "bug", "issue", "help","fault"]):
        state["category"] = "Technical Support"
    elif any(word in query for word in ["billing", "invoice", "payment","sub"]):
        state["category"] = "Billing"
    elif any(word in query for word in ["login", "password", "account"]):
        state["category"] = "Account"
    
    return {"category":state["category"]}


def tech_support(state: AgentState):
    return {
        "response": "Handling technical issue"
    }

def billing(state: AgentState):
    return {
        "response": "Handling billing issue"
    }

def account(state: AgentState):
    return {
        "response": "Handling account issue"
    }


def route_query(state: AgentState):
    category = state["category"]
    
    if category == "Technical Support":
        return "tech_support"
    elif category == "Billing":
        return "billing"
    elif category == "Account":
        return "account"

graph = StateGraph(AgentState)

graph.add_node("classify_query", classify_query)
graph.add_node("tech_support", tech_support)
graph.add_node("billing", billing)
graph.add_node("account", account)

graph.add_edge(START, "classify_query")
graph.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "tech_support": "tech_support",
        "billing": "billing",
        "account": "account"
    }
)

graph.add_edge("tech_support", END)
graph.add_edge("billing", END)
graph.add_edge("account", END)

workflow = graph.compile()

print(workflow.invoke({"query": "facing issue with billing"}))