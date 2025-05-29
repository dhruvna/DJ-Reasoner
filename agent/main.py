import os
from dotenv import load_dotenv
load_dotenv()
from graph import build_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":
    workflow = build_graph()
    test_prompt = "Give me some upbeat songs to get me energized for a workout."
    result = workflow.invoke({
        "messages": [HumanMessage(content=test_prompt)]
    })

    print("\n=== DJ Reasoner Response ===\n")
    print(result["final_output"])
