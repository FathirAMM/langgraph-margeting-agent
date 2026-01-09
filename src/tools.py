from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# Search tool for market research
search_tool = DuckDuckGoSearchRun()

@tool
def headline_creator(topic: str) -> str:
    """Generates catchy headlines for a given topic."""
    return f"5 Ways {topic} Will Change the World", f"Why {topic} Matters Now", f"The Ultimate Guide to {topic}"

tools = [search_tool, headline_creator]
