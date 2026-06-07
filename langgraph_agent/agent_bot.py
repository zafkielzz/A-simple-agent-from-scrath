import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
# Đổi dòng import sang langchain_groq
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# Khởi tạo mô hình thông qua Groq API
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")

graph= StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent= graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages":[HumanMessage(content= user_input)]})
    user_input = input("Enter: ")

