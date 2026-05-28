from typing import TypedDict    # this is used to deifne the state structure state = { "ques" : "...." , "tool" : "... "}
from langgraph.graph import StateGraph, START, END
from my_tools.calculator import calculator
from my_tools.search import search


#StateGraph is used to create Graph 
#START -> graph begin 
#END -> graph finish


#this is flow like how it process phle ques puchega fir tool assign hoga then answer
class AgentState(TypedDict):
    question: str
    tool: str
    answer: str
    reflection: str
    retry_count: int

def process_question(state: AgentState):   # this is node....... and...it recive shared graph memory 
    ques = state["question"]

    if "+" in ques or "-" in ques or "*" in ques:
        state["tool"] = "calculator"
    else:
        state["tool"] = "search"
    
    print(f"Selected Tool: {state['tool']}")

    return state



# #execute tool node  
# def execute_tool(state: AgentState):
#     tool = state["tool"]

#     if tool == "calculator":
#         state["answer"] = "Math calcualtion completed"
#     else: 
#         state["answer"] = "Search Completed"


#     print(f"Answer: {state['answer']}")

#     return state


#node for Execute calculator
def execute_calculator(state: AgentState):

    question = state["question"]
    expression = (
        question.replace("What is", "").replace("Calculate", "").strip()
    )

    result = calculator(expression)   # function callled from calculator file from tools folder
    state["answer"] = result

    print(f"calculate result {state['answer']}")
    return state

#node for search executin
def execute_search(state: AgentState):
    question = state["question"]
    result = search(question)
    state["answer"] = result

    print(f"search result is {state['answer']}")
    return state


# node for the reflectin meand now agent retry its output and rethink and regenreat the output if not correct
def reflect_on_answer(state: AgentState):

    answer = state["answer"]

    if "Error" in answer:
        state["retry_count"] += 1

        if state["retry_count"] >= 3:
            state["reflection"] = "good"
            state["answer"] = "Failed after 3 retries"

        else:
            state["reflection"] = "retry"

    else:
        state["reflection"] = "good"

    print(f"Reflection is : {state['reflection']}")
    return state




# for reflection router
def reflection_router(state: AgentState):
    reflection = state["reflection"]

    if reflection == "good":
        return "finish"

    return "retry"

# now this will decide which one of above func or node will run
def route_tool(state: AgentState):
    tool = state["tool"]
    if tool == "calculator":
        return "calculator_path"

    return "search_path"


graph = StateGraph(AgentState) # this create empty graph using upper wale struc se usi way ka empty graphh bna denge  using our state structure


graph.add_node("process_question", process_question)     #"process-question" this is the node name in the graph structure
graph.add_node("execute_calculator", execute_calculator)
graph.add_node("execute_search", execute_search)
graph.add_node("reflect_on_answer", reflect_on_answer)




#Connection of nodes

graph.add_edge(START, "process_question")
# graph.add_edge("process_question", "execute_tool")
# graph.add_edge("execute_tool", END)

#based on condition the nodes will connect ->The graph itself decides path dynamically.
graph.add_conditional_edges(
    "process_question",
    route_tool,
    {
        "calculator_path": "execute_calculator",
        "search_path": "execute_search"
    }
)

# now connecting both final node


# graph.add_edge("execute_calculator", END)
# graph.add_edge("execute_search", END)

graph.add_edge("execute_calculator", "reflect_on_answer")
graph.add_edge("execute_search", "reflect_on_answer")


#addition of conditional edges for the reflect answer
graph.add_conditional_edges(
    "reflect_on_answer",
    reflection_router,
    {
        "finish": END,
        "retry": "process_question"
    }
)







app = graph.compile() # this compile the graph  after compile the graph become executable 


# result = app.invoke({
#     "question": "Latest AI news"
# })

# print(result)


questions = [
    "What is 13 + 43",
    "What is 10 + ",
    "Calculate 5*12",
    "Latest Ai news",
    "Search about india"
]

for q in questions:
    print(f"\n ---------Ans BROO - {q}--------\n")

    result = app.invoke({
        "question": q,
        "retry_count": 0
    })

    print(result)