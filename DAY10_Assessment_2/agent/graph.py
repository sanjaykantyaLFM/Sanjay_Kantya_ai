from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.state import AgentState
from agent.retriever import retrieve_documents
from my_tools.calculator import calculator

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash"
)



def agent_node(state: AgentState):
    question = state["question"]

    if any(char.isdigit() for char in question):
        state["route"] = "tool"
    else:
        state["route"] = "retrieve"

    return state

def retrieve_node(state: AgentState):
    docs = retrieve_documents(
        state["question"]
    )
    state["retrieved_docs"] = docs


    return state



def tool_node(state: AgentState):

    result = calculator.invoke(
        {"expression": state["question"]}
    )


    state["answer"] = str(result)

    return state



def answer_node(state: AgentState):

    docs = state["retrieved_docs"]

    context = "\n\n".join(
        [doc["content"] for doc in docs]
    )


    citations = "\n".join(
        [
            f"{doc['source']} (chunk {doc['chunk_id']})"
            for doc in docs
        ]
    )
    # yha pr ab prompt denge

    prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{state['question']}

Also provide source citations.
"""

    # llm ko invoke kiya hia
    response = llm.invoke(prompt)

    final_answer = (
        response.content
        + "\n\nSources:\n"
        + citations
    )

    state["answer"] = final_answer

    return state



def router(state: AgentState):
    return state["route"]


# Build Graph abhi empty hai graph
builder = StateGraph(AgentState)

#nodes assign kiya
builder.add_node("agent", agent_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("tool", tool_node)
builder.add_node("answer", answer_node)


#edges
builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    router,
    {
        "retrieve": "retrieve",
        "tool": "tool"
    }
)

builder.add_edge(
    "retrieve",
    "answer"
)

builder.add_edge(
    "answer",
    END
)

builder.add_edge(
    "tool",
    END
)


graph = builder.compile()


if __name__ == "__main__":

    result = graph.invoke(
        {
            "question": "What is RAG?",
            "retrieved_docs": [],
            "answer": "",
            "route": ""
        }
    )

    print(result["answer"])