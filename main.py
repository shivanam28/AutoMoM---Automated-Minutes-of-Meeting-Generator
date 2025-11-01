import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from automom.pipeline.generate_mom import run_pipeline

if __name__ == "__main__":
    run_pipeline("data/meeting_transcript.txt")
