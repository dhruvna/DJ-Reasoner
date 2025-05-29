# agent/graph.py

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from tools import spotify_tool

def receive_prompt(state):
    return {"user_input": state["messages"][-1].content}

def parse_intent(state):
    return {"query": state["user_input"]}

def call_spotify(state):
    query = state["query"]
    result = spotify_tool.run(query)
    return {
        "search_results": result,
        "query": query
    }

def reason_about_results(state):
    explanation = f"I'm recommending these songs based on your prompt: '{state['query']}'.\n\n"
    return {"final_output": explanation + state["search_results"]}

def build_graph():
    builder = StateGraph(state_schema=dict)

    builder.add_node("ReceivePrompt", RunnableLambda(receive_prompt))
    builder.add_node("ParseIntent", RunnableLambda(parse_intent))
    builder.add_node("SearchSpotify", RunnableLambda(call_spotify))
    builder.add_node("Reason", RunnableLambda(reason_about_results))

    # Graph flow
    builder.set_entry_point("ReceivePrompt")
    builder.add_edge("ReceivePrompt", "ParseIntent")
    builder.add_edge("ParseIntent", "SearchSpotify")
    builder.add_edge("SearchSpotify", "Reason")
    builder.set_finish_point("Reason")

    return builder.compile()