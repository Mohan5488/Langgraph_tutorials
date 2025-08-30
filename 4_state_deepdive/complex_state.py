from typing import TypedDict, List, Annotated
from langgraph.graph import END, StateGraph
import operator

class SimpleState(TypedDict):
    count : int
    sum_ : Annotated[int, operator.add]
    history : Annotated[List[int], operator.add]

def increment(state):
    new_value = state["count"] + 1
    return {
        "count" : new_value,
        "sum_" : new_value,
        "history" : [(state["sum_"], state["count"])]
    }

def should_continue(state):
    if state["count"] < 5:
        return "continue"
    else:
        return "stop"
    
graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue": "increment",
        "stop": END
    }
)

app = graph.compile()

print(app.get_graph().draw_mermaid())

state = {
    "count" : 1,
    "sum_" : 1,
    "history" : []
}

res = app.invoke(state)
print(res)