"""
Contains the CrewAI agent definitions and their task flow setup using LangChain tools and OpenAI.
"""
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import os
import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_KEY")

extracted_links = []

def firecrawl_search(query: str):
    response = requests.get(f"https://api.firecrawl.dev/v1/search?query={query}", headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"})

    if response.status_code == 200:
        try:
            json_data = response.json()
            results = json_data.get("results", [])
            if results:
                for result in results:
                    url = result.get("url")
                    if url:
                        extracted_links.append(url)
                return response.text
        except Exception:
            # TODO: log exception
            pass

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.3)
    fallback_response = llm.invoke([
        HumanMessage(content=f"Please provide a clear explanation about: {query}. Include definition, features, and common use cases.")
    ])
    return fallback_response.content

# Register firecrawl search as a tool
firecrawl_tool = Tool(
    name="FirecrawlSearch",
    description="Search the web using Firecrawl API and return HTML content or fallback LLM answer.",
    func=firecrawl_search,
)
