import dotenv
dotenv.load_dotenv()

from src.graph import graph
from langchain_core.messages import HumanMessage

def main():
    print("Welcome to the Multi-Agent Marketing System!")
    print("--------------------------------------------")
    user_input = input("Enter your marketing request (e.g., 'Write a blog post about AI in Marketing'): ")

    if not user_input:
        print("No input provided. Exiting.")
        return

    inputs = {"messages": [HumanMessage(content=user_input)]}
    print("\nProcessing... (This may take a moment)\n")

    for s in graph.stream(inputs):
        if "__end__" not in s:
            for key, value in s.items():
                print(f"--- Agent: {key} ---")
                # Handle supervisor output which is a dict with 'next' key
                if key == "Supervisor":
                    print(f"Supervisor decided next step: {value.get('next')}")
                # Handle agent output which contains messages
                elif "messages" in value:
                    print(value["messages"][0].content)
                else:
                    print(value)
                print("\n")
        else:
            print("--- Finished ---")

if __name__ == "__main__":
    main()
