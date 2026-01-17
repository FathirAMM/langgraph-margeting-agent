from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools import tools, search_tool, web_scraper, seo_analyzer, image_prompt_generator, compliance_check
from src.config import settings

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
# Pydantic SecretStr needs .get_secret_value() to be passed as string
llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key.get_secret_value())

# --- Agent Prompts ---

researcher_prompt = (
    "You are a Senior Market Researcher. Your goal is to uncover deep insights, statistics, and trends. "
    "1. Use 'duckduckgo_search' to find relevant articles and sources. "
    "2. Use 'web_scraper' to read the full content of promising search results to get specific details. "
    "3. Compile a comprehensive report citing your sources. Be factual and detailed."
)

content_prompt = (
    "You are a Content Strategist. Your goal is to craft compelling marketing narratives. "
    "Based on the research provided, draft high-quality content. "
    "Structure your content effectively (MUST include 'Introduction' and 'Conclusion' sections). "
    "Tailor the tone to the audience (Professional yet engaging)."
)

seo_prompt = (
    "You are an SEO Optimizer. Your goal is to ensure content ranks high on search engines. "
    "1. Analyze the draft content using 'seo_analyzer' against relevant keywords. "
    "2. Suggest concrete improvements: changing headings, adding keywords naturally, or adjusting structure. "
    "3. Rewrite sections if necessary to improve the score without sacrificing readability."
)

visual_prompt = (
    "You are a Visual Designer. Your goal is to conceptualize imagery that complements the text. "
    "1. Read the content draft. "
    "2. Use 'image_prompt_generator' to create 3 distinct image prompts that could be used as headers or social media graphics. "
    "3. Describe why each prompt fits the content."
)

compliance_prompt = (
    "You are a Compliance Officer. Your goal is to ensure all content meets strict publication guidelines. "
    "1. Use the 'compliance_check' tool to validate the latest content draft. "
    "2. If the tool reports issues, clearly list them and suggest fixes. "
    "3. If the tool passes, confirm that the content is approved for publication."
)

# --- Create Agents ---

research_agent = create_agent(llm, [search_tool, web_scraper], researcher_prompt)
content_agent = create_agent(llm, [], content_prompt)
seo_agent = create_agent(llm, [seo_analyzer], seo_prompt)
visual_agent = create_agent(llm, [image_prompt_generator], visual_prompt)
compliance_agent = create_agent(llm, [compliance_check], compliance_prompt)

# --- Node Functions ---

def research_node(state):
    return agent_node(state, research_agent, "Senior_Researcher")

def content_node(state):
    return agent_node(state, content_agent, "Content_Strategist")

def seo_node(state):
    return agent_node(state, seo_agent, "SEO_Optimizer")

def visual_node(state):
    return agent_node(state, visual_agent, "Visual_Designer")

def compliance_node(state):
    return agent_node(state, compliance_agent, "Compliance_Officer")
