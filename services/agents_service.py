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

# Task 3: Add Firecrawl Search function here


# Task 5: Implement Researcher, Summarizer, and presenter Agents
