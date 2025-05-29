import os
from dotenv import load_dotenv
load_dotenv()
from graph import build_graph
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
if __name__ == "__main__":

    workflow = build_graph()

    prompt = "Give me songs songs by Maroon 5 from the album 'Songs about Jane'"
    result = workflow.invoke({
        "messages": [HumanMessage(content=prompt)]
    })

    print("\n=== DJ Reasoner Says ===\n")
    print(result["final_output"])
