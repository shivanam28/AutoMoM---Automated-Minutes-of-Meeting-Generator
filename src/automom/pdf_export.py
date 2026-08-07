"""
AutoMoM PDF Export
-------------------
Takes the dict returned by pipeline.generate_mom() and writes a
formatted Minutes-of-Meeting PDF using reportlab.
"""


import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def export_to_pdf(mom: dict, output_path: str) -> str:
    """
    Write a Minutes-of-Meeting PDF from a result dict.

    mom is expected to have: meeting_id, summary, keywords, intent.
    Returns the path the PDF was written to.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 80

    def new_page_if_needed(min_y=100):
        nonlocal y
        if y < min_y:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 10)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(80, y, "AutoMoM — Minutes of Meeting")
    y -= 35

    # Meeting ID
    c.setFont("Helvetica", 11)
    c.drawString(80, y, f"Meeting: {mom.get('meeting_id', 'Unknown')}")
    y -= 30

    # Summary
    c.setFont("Helvetica-Bold", 13)
    c.drawString(80, y, "Summary")
    y -= 20
    c.setFont("Helvetica", 10)
    for line in _wrap_text(mom.get("summary", "No summary available."), width=95):
        c.drawString(80, y, line)
        y -= 14
        new_page_if_needed()

    # Keywords
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(80, y, "Keywords")
    y -= 20
    c.setFont("Helvetica", 10)
    keywords = mom.get("keywords", [])
    c.drawString(80, y, ", ".join(keywords) if keywords else "None found")
    y -= 20
    new_page_if_needed()

    # Intent
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(80, y, "Intent")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(80, y, mom.get("intent", "Unknown"))

    c.save()
    return output_path


def _wrap_text(text: str, width: int = 95):
    """Simple word-wrap so long summary lines don't run off the page."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = f"{current} {word}".strip()
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
