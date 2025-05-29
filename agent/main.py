# agent/main.py

from dotenv import load_dotenv
load_dotenv()
from graph import build_graph
from langchain_core.messages import HumanMessage

def save_workflow_graph(workflow):
    graph = workflow.get_graph()
    png_bytes = graph.draw_mermaid_png()
    with open("workflow_graph.png", "wb") as f:
        f.write(png_bytes)
    print("Workflow graph saved as 'workflow_graph.png'.")

if __name__ == "__main__":

    user_input = input("What kind of music are you in the mood for? ")

    workflow = build_graph()
    save_workflow_graph(workflow)
    result = workflow.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    print("\n=== DJ Reasoner Says ===\n")
    print(result["final_output"])
