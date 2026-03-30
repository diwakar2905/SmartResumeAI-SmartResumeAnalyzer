import re

# Define regex patterns for each section header
# Patterns are anchored to the start of a line and are case-insensitive
SECTION_KEYWORDS = {
    "summary": r"^\s*(professional\s+)?summary\b",
    "experience": r"^\s*(work\s+)?experience\b|^\s*professional\s+experience\b",
    "education": r"^\s*education\b",
    "projects": r"^\s*projects\b",
    "certifications": r"^\s*certifications\b|^\s*licenses\s*(?:&\s*certifications)?\b"
}

def extract_sections(text):
    """
    Scans the resume text to detect the presence of standard resume sections.

    Args:
        text (str): Full resume text extracted from PDF or DOCX.

    Returns:
        dict: Mapping of section names to boolean values indicating presence.
    """
    sections_found = {section: False for section in SECTION_KEYWORDS}

    for section, pattern in SECTION_KEYWORDS.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            sections_found[section] = True

    return sections_found
