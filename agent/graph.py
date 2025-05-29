# agent/graph.py

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from tools import spotify_tool
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

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
    query = state["query"]
    results = state["search_results"]

    prompt = f"""You are a music-savvy assistant. The user asked for music like: "{query}".

    Here are the songs you found:
    {results}

    Format your response as a **numbered list**, where each entry includes:
    1. The song title in quotes
    2. The artist name
    3. A short explanation of why this song fits the user's request

    Make sure the formatting looks like this:

    1. "Title" by Artist — explanation
    2. "..." ...

    For example:
    1. "Chasing Cars" by Snow Patrol — This song has a melancholic yet uplifting vibe, perfect for rainy days.

    Keep your tone friendly and insightful, like a DJ recommending tracks to a friend.
    """

    response = llm.invoke(prompt)
    return {"final_output": response.content}

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
