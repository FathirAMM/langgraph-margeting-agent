import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from src.config import settings
from src.guardrails import ContentValidator

# --- Base Search Tool ---
search_tool = DuckDuckGoSearchRun()

# --- Specialized Tools ---

@tool
def web_scraper(url: str) -> str:
    """
    Scrapes the text content from a given URL.
    Useful for reading full articles or blog posts found during search.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text[:5000] + "..." if len(text) > 5000 else text # Truncate if too long
    except Exception as e:
        return f"Error scraping {url}: {e}"

@tool
def seo_analyzer(content: str, keywords: str) -> str:
    """
    Analyzes the SEO quality of the content based on provided keywords.
    Returns a brief report on keyword density and basic readability.
    keywords should be a comma-separated string.
    """
    keyword_list = [k.strip().lower() for k in keywords.split(",")]
    content_lower = content.lower()
    word_count = len(content.split())

    report = [f"SEO Analysis Report (Word Count: {word_count})"]
    report.append("-" * 30)

    for k in keyword_list:
        count = content_lower.count(k)
        density = (count / word_count) * 100 if word_count > 0 else 0
        report.append(f"Keyword '{k}': Found {count} times ({density:.2f}%)")

    if word_count < 300:
        report.append("WARNING: Content is too short for good SEO (aim for >300 words).")

    return "\n".join(report)

@tool
def image_prompt_generator(topic: str, tone: str = "professional") -> str:
    """
    Generates a detailed prompt for an AI image generator (like DALL-E) based on a topic.
    """
    return (
        f"A high-quality, {tone} digital illustration representing '{topic}'. "
        "Clean lines, modern style, suitable for a corporate blog or marketing material. "
        "Bright and engaging colors."
    )

@tool
def compliance_check(content: str) -> str:
    """
    Validates content against safety and policy guardrails.
    Returns a status report.
    """
    result = ContentValidator.validate(content)
    return result["feedback"]

tools = [search_tool, web_scraper, seo_analyzer, image_prompt_generator, compliance_check]
