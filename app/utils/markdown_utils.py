# app/utils/markdown_utils.py
import re
from typing import List


def clean_markdown(md_text: str) -> str:
    """
    Perform cleanup of markdown text.
    - Normalize whitespace
    - Remove excessive blank lines
    - Replace problematic characters if any
    """
    # Normalize line breaks and whitespace
    md_text = re.sub(r'\r\n|\r', '\n', md_text)
    md_text = re.sub(r'\n{3,}', '\n\n', md_text)  # max two consecutive line breaks

    # Strip trailing and leading spaces on each line
    lines = md_text.split('\n')
    lines = [line.rstrip() for line in lines]

    cleaned_text = '\n'.join(lines)
    return cleaned_text


def extract_section_headers(md_text: str) -> List[str]:
    """
    Optionally extract markdown headers to understand document structure.
    E.g., lines starting with #, ##, etc.
    """
    headers = []
    for line in md_text.split('\n'):
        if line.startswith('#'):
            headers.append(line.strip())
    return headers


def markdown_from_pdf_text(pdf_text: str) -> str:
    """
    Convert raw extracted text from PDF into Markdown.
    This is a simplified heuristic example:
      - Treat lines that look like headings as markdown headers
      - Bullet points
      - Preserve paragraphs
    
    Note: Replace this with your actual markdown conversion logic or library.
    """
    lines = pdf_text.split('\n')
    md_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            # Preserve blank lines between paragraphs
            md_lines.append('')
        elif re.match(r'^\d+(\.\d+)*\s', stripped):
            # Example: Numbered clause as header
            md_lines.append(f'### {stripped}')
        elif re.match(r'^[•*-]\s', stripped):
            # Bullet point
            md_lines.append(f'* {stripped[2:]}')
        else:
            md_lines.append(stripped)

    md_text = '\n'.join(md_lines)
    return clean_markdown(md_text)
