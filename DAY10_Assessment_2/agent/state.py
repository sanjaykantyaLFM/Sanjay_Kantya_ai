from typing import TypedDict

class AgentState(TypedDict):
    question: str
    retrieved_docs: list
    answer: str
    route: str