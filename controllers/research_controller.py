"""
The core orchestration logic coordinates the agents, data cleaning, and PDF generation.
"""
import base64
from typing import Tuple
from services.agents_service import setup_agents_and_tasks
from models.pdf_generator import create_pdf
from utils.markdown_cleaner import clean_markdown

extracted_links = []


def run_deep_research(query: str, breadth: int, depth: int) -> Tuple[str, bytes, str]:
    """
    This initializes a research crew based on a query, breadth, and depth. The agents execute the research, summarize
    findings, and format the final output. The final result is cleaned using a Markdown cleaner and then converted into
    a PDF using a helper function. The PDF is encoded in base64 for API-safe transmission. This function returns both
    the clean text and its base64-encoded PDF version.
    Args:
        query(str): the query to search
        breadth(int): how wide should the AI research agent go on a topic
        depth(int): how deep should the AI research agent get into a topic
    Returns:
        tuple with the cleaned output, PDF data and base64 encoded PDF
    """
    crew, researcher_tool, firecrawl_tool = setup_agents_and_tasks(query, breadth, depth)
    result = crew.kickoff()
    raw_output = result.output if hasattr(result, 'output') else str(result)
    cleaned_output = clean_markdown(raw_output)

    summary_text = f"Summary for research topic: {query}"
    pdf_path = create_pdf(summary_text, cleaned_output, extracted_links)

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')

    return cleaned_output, pdf_data, base64_pdf
