from typing import TypedDict    # this is used to deifne the state structure state = { "ques" : "...." , "tool" : "... "}
from langgraph.graph import StateGraph, START, END

#StateGraph is used to create Graph 
#START -> graph begin 
#END -> graph finish


#this is flow like how it process phle ques puchega fir tool assign hoga then answer
class AgentState(TypedDict):
    question: str
    tool: str
    answer: str


def process_question(state: AgentState):   # this is node....... and...it recive shared graph memory 
    ques = state["question"]

    if "+" in ques or "-" in ques or "*" in ques:
        state["tool"] = "calculator"
    else:
        state["tool"] = "search"
    
    print(f"Selected Tool: {state['tool']}")

    return state



#execute tool node  
def execute_tool(state: AgentState):
    tool = state["tool"]

    if tool == "calculator":
        state["answer"] = "Math calcualtion completed"
    else: 
        state["answer"] = "Search Completed"


    print(f"Answer: {state['answer']}")

    return state



graph = StateGraph(AgentState) # this create empty graph using upper wale struc se usi way ka empty graphh bna denge  using our state structure


graph.add_node("process_question", process_question)     #"process-question" this is the node name in the graph structure
graph.add_node("execute_tool", execute_tool)

#Connection of nodes
graph.add_edge(START, "process_question")
graph.add_edge("process_question", "execute_tool")
graph.add_edge("execute_tool", END)

app = graph.compile() # this compile the graph  after compile the graph become executable 


result = app.invoke({
    "question": "What is 10+43"
})

print(result)