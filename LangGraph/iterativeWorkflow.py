#  START -> Take Quiz -> Evaluate_Score -> pass/fail -> if(pass -> END) -> if(fail -> Return to take quiz)


from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random

class QuizState(TypedDict):
    score:int
    quiz_taken:bool
    attempt:int

def take_quiz(state: QuizState):
    score = random.randint(40,100)
    print("You scored", score)
    return {
        "score": score,
        "quiz_taken": True,
        "attempt": state.get("attempt", 0) + 1
    }

def study_material(state):
    print("Study well")
    return{}

def evaluate_score(state: QuizState):
    score = state["score"]
    if score >= 50:
        return "PASS"
    else:
        return "RETRY"

builder = StateGraph(QuizState)

builder.add_node("take_quiz", take_quiz)
builder.add_node("study_material", study_material)

builder.add_edge(START, "take_quiz")
builder.add_conditional_edges(
    "take_quiz",   
    evaluate_score,
    {
        "PASS": END,
        "RETRY": "study_material"
    }
)

builder.add_edge("study_material", "take_quiz")

workflow = builder.compile()

result = workflow.invoke({"attempt":0})

print(result)
