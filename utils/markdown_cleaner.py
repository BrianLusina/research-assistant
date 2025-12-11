"""
Provides utility functions to clean and preprocess markdown text from the agent’s output.
"""
import re

def clean_markdown(md_text: str) -> str:
    """
    Takes md_text as a parameter and removes Markdown syntax such as #, **, *, and backticks ` from the text. This
    ensures the agent’s output is clean, readable, and suitable for display or PDF conversion.

    Note: This modifies the input string in place

    Args:
        md_text(str): Markdown text
    Returns:
        str: cleaned Markdown text
    """
    md_text = re.sub(r'#+ ', '', md_text)  # Remove headings
    md_text = re.sub(r'\\*\\*(.*?)\\*\\*', r'\g<1>', md_text)
    md_text = re.sub(r'\\*(.*?)\\*', r'\g<1>', md_text)
    md_text = re.sub(r'`(.*?)`', r'\g<1>', md_text)
    md_text = re.sub(r'- ', '• ', md_text)
    return md_text.strip()
