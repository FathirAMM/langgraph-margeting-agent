from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents import research_node, content_node, seo_node

# Supervisor Logic
members = ["Market_Researcher", "Content_Creator", "SEO_Specialist"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When the work is "
    "complete and you are satisfied with the final output (ensure it has been optimized by SEO), "
    "respond with FINISH."
)

options = ["FINISH"] + members

function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next? "
            "Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = ChatOpenAI(model="gpt-4o")

supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[function_def], function_call="route")
    | JsonOutputFunctionsParser()
)

# Graph Construction
workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_chain)
workflow.add_node("Market_Researcher", research_node)
workflow.add_node("Content_Creator", content_node)
workflow.add_node("SEO_Specialist", seo_node)

for member in members:
    workflow.add_edge(member, "Supervisor")

# Conditional edges from Supervisor
workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x["next"],
    {
        "Market_Researcher": "Market_Researcher",
        "Content_Creator": "Content_Creator",
        "SEO_Specialist": "SEO_Specialist",
        "FINISH": END,
    },
)

workflow.set_entry_point("Supervisor")

graph = workflow.compile()
