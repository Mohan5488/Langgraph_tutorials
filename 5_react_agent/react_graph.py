from langgraph.graph import StateGraph, END
from langchain_core.agents import AgentAction, AgentFinish
from dotenv import load_dotenv
load_dotenv()
from react_state import AgentState
from nodes import reason_node, act_node

graph = StateGraph(AgentState)
REASON_NODE = "reason_node"
ACT_NODE = "act_node"

def should_continue(state):
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT_NODE
    
graph.add_node(REASON_NODE, reason_node)
graph.add_node(ACT_NODE, act_node)
graph.set_entry_point(REASON_NODE)

graph.add_conditional_edges(REASON_NODE, should_continue)
graph.add_edge(ACT_NODE, REASON_NODE)

app = graph.compile()

state = {
     "input": "How many days ago was the latest SpaceX launch?", 
    "agent_outcome": None, 
    "intermediate_steps": []
}

res = app.invoke(state)
print(res)

print(res['agent_outcome'].return_values["output"])