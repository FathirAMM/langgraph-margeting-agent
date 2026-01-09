from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools import tools, search_tool, headline_creator

def create_agent(llm, tools, system_prompt):
    """Helper function to create an agent with tools."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o")

# Define Agent System Prompts
researcher_prompt = (
    "You are a Market Researcher. Your job is to find the latest trends, statistics, and information "
    "about a given topic. Use the search tool to find accurate and up-to-date information. "
    "Summarize your findings clearly."
)

content_prompt = (
    "You are a Content Creator. Your job is to write engaging marketing copy (blog posts, social media posts, etc.) "
    "based on the research provided. Make it punchy, professional, and tailored to the target audience. "
    "Use the headline_creator tool if you need ideas for titles."
)

seo_prompt = (
    "You are an SEO Specialist. Your job is to review content and optimize it for search engines. "
    "Suggest keywords, meta descriptions, and improvements to headings to maximize reach."
)

# Create Agents
research_agent = create_agent(llm, [search_tool], researcher_prompt)
content_agent = create_agent(llm, [headline_creator], content_prompt)
seo_agent = create_agent(llm, [], seo_prompt)

# Node functions for the graph
def research_node(state):
    return agent_node(state, research_agent, "Market_Researcher")

def content_node(state):
    return agent_node(state, content_agent, "Content_Creator")

def seo_node(state):
    return agent_node(state, seo_agent, "SEO_Specialist")
