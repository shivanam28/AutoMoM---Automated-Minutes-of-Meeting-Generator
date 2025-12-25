from transformers import pipeline
import pandas as pd
from automom.utils.logger import logger

class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        logger.info(f"🧠 Loading summarization model: {model_name}")
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_text(self, text, min_length=80, max_length=300):
        """Generate a summary for a single text block."""
        try:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            logger.warning(f"⚠️ Summarization failed for text: {e}")
            return "Summary not generated due to error."

    def generate_summaries(self, df):
        """Generate summaries for all meeting transcripts in the DataFrame."""
        logger.info("📝 Generating summaries for all meeting transcripts...")

        summaries = []
        for i, row in df.iterrows():
            text = str(row.get("transcript_text", ""))
            if not text.strip():
                summaries.append("No transcript text available.")
                continue

            summary = self.summarize_text(text)
            summaries.append(summary)

            if (i + 1) % 5 == 0:
                logger.info(f"✅ Processed {i + 1}/{len(df)} transcripts")

        df["summary"] = summaries

        output_path = "data/processed/meeting_summaries.csv"
        df.to_csv(output_path, index=False)
        logger.success(f"💾 Summaries saved to: {output_path}")
        return df
