import sqlite3
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from src.state import AgentState
from src.agents import research_node, content_node, seo_node, visual_node, compliance_node
from src.config import settings

# --- Supervisor Logic ---
members = ["Senior_Researcher", "Content_Strategist", "SEO_Optimizer", "Visual_Designer", "Compliance_Officer"]

system_prompt = (
    "You are the Lead Editor (Supervisor) of a marketing agency. "
    "Your team consists of: {members}. "
    "Your role is to orchestrate the workflow to produce high-quality marketing assets.\n\n"
    "Standard Workflow Guide:\n"
    "1. Start with 'Senior_Researcher' to gather information.\n"
    "2. Pass to 'Content_Strategist' to draft the content.\n"
    "3. Pass to 'SEO_Optimizer' to refine the draft.\n"
    "4. Pass to 'Visual_Designer' to create image assets.\n"
    "5. Pass to 'Compliance_Officer' to check against guardrails.\n"
    "6. If Compliance rejects, send back to 'Content_Strategist' for revisions.\n"
    "7. If Compliance approves, FINISH.\n\n"
    "Given the conversation history, who should act next?"
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

# Pydantic SecretStr needs .get_secret_value() to be passed as string
llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key.get_secret_value())

supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[function_def], function_call="route")
    | JsonOutputFunctionsParser()
)

# --- Graph Construction ---
workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_chain)
workflow.add_node("Senior_Researcher", research_node)
workflow.add_node("Content_Strategist", content_node)
workflow.add_node("SEO_Optimizer", seo_node)
workflow.add_node("Visual_Designer", visual_node)
workflow.add_node("Compliance_Officer", compliance_node)

for member in members:
    workflow.add_edge(member, "Supervisor")

workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x["next"],
    {
        "Senior_Researcher": "Senior_Researcher",
        "Content_Strategist": "Content_Strategist",
        "SEO_Optimizer": "SEO_Optimizer",
        "Visual_Designer": "Visual_Designer",
        "Compliance_Officer": "Compliance_Officer",
        "FINISH": END,
    },
)

workflow.set_entry_point("Supervisor")

# --- Persistence ---
# Use an in-memory db for this example setup to avoid file locks in some envs,
# or a local file 'checkpoints.sqlite' for persistence across runs.
# We will use a local file to demonstrate "production grade" persistence.
memory = SqliteSaver.from_conn_string("checkpoints.sqlite")

graph = workflow.compile(checkpointer=memory)
