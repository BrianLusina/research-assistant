"""
Contains the CrewAI agent definitions and their task flow setup using LangChain tools and OpenAI.
"""
import os
from typing import Tuple
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage
import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_KEY")

extracted_links = []

@tool
def firecrawl_search(query: str) -> str:
    """
    Search the web using Firecrawl API and return HTML content or fallback LLM answer.
    Args:
        query(str): the query to use to perform a search
    Returns:
        str: Response from a query search
    """
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

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.3)
    fallback_response = llm.invoke([
        HumanMessage(content=f"Please provide a clear explanation about: {query}. Include definition, features, and common use cases.")
    ])
    return fallback_response.content


def setup_agents_and_tasks(query: str, breadth: int, depth: int) -> Tuple[Crew, Agent]:
    """
    This function sets up a multi-stage AI workflow involving three specialized agents, Researcher, Summarizer, and
    Presenter, to conduct deep web research, summarize the findings, and generate a polished final report.
    Args:
        query(str): represents the research topic the agents will explore
        breadth(int): indicates how wide-ranging the research should be across different sources or subtopics
        depth(int): indicates how thoroughly agents should explore each source or branch of the topic
    Returns:

    """
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.3)

    researcher = Agent(
        name="Research Agent",
        role="Web searcher and data collector",
        goal="Conduct deep recursive web research",
        backstory="Expert in online information mining and query generation",
        tools=[firecrawl_search],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    summarizer = Agent(
        name="Summarization Agent",
        role="Content summarizer",
        goal="Condense detailed findings into concise summaries",
        backstory="Skilled in summarizing complex texts for better understanding",
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    presenter = Agent(
        name="Presentation Agent",
        role="Report formatter",
        goal="Create readable and well-structured reports",
        backstory="Experienced in generating polished documents for readers",
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    task_research = Task(
        description=f"Perform deep research on: {query}.",
        expected_output="Raw web content, source links, and extracted notes",
        agent=researcher
    )

    task_summarize = Task(
        description="Summarize the research findings into structured points.",
        expected_output="Summarized bullets categorized by topic",
        agent=summarizer
    )

    task_present = Task(
        description="Format all summaries into a professional report.",
        expected_output="A final human-readable report",
        agent=presenter
    )

    crew = Crew(
        agents=[researcher, summarizer, presenter],
        tasks=[task_research, task_summarize, task_present],
        verbose=True,
        max_steps=20,
        max_time=300
    )

    return crew, researcher
