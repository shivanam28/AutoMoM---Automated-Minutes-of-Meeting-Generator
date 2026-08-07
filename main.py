"""
AutoMoM CLI
------------
Run the pipeline on a single .txt transcript file from the command line.

Usage:
    python main.py path/to/transcript.txt
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from automom.pipeline import generate_mom
from automom.pdf_export import export_to_pdf


def run(transcript_path: str):
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    meeting_id = os.path.splitext(os.path.basename(transcript_path))[0]

    print(f"Running pipeline on: {transcript_path}")
    mom = generate_mom(transcript_text, meeting_id=meeting_id)

    output_path = os.path.join("data/processed/pdfs", f"{meeting_id}_MoM.pdf")
    export_to_pdf(mom, output_path)

    print(f"Summary : {mom['summary'][:120]}...")
    print(f"Keywords: {', '.join(mom['keywords'])}")
    print(f"Intent  : {mom['intent']}")
    print(f"PDF saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/transcript.txt")
        sys.exit(1)
    run(sys.argv[1])
