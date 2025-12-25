import os
import sys
import pandas as pd
from automom.components.summarizer import Summarizer
from automom.components.keyword_extraction import KeywordExtractor
from automom.components.intent_extraction import IntentExtractor
from automom.components.pdf_generator import PDFGenerator
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException


class MoMGenerator:
    def __init__(self, input_file="data/processed/test_transcripts.csv"):
        """
        Initializes the AutoMoM pipeline starting from summarization.
        Assumes data ingestion is already completed.
        """
        self.input_file = input_file
        self.output_dir = "data/processed"
        self.pdf_dir = os.path.join(self.output_dir, "mom_reports")
        os.makedirs(self.pdf_dir, exist_ok=True)

        self.summarizer = Summarizer()
        self.keyword_extractor = KeywordExtractor()
        self.intent_extractor = IntentExtractor()
        self.pdf_generator = PDFGenerator()

    def generate_mom(self):
        """
        Runs the MoM generation pipeline:
        Summarizer -> Keyword Extractor -> Intent Extractor -> PDF Generator
        """
        try:
            logger.info("🚀 Starting AutoMoM - Summarization to PDF pipeline...")

            # Step 1: Load transcript data
            if not os.path.exists(self.input_file):
                raise FileNotFoundError(f"Input file not found: {self.input_file}")

            transcripts_df = pd.read_csv(self.input_file)
            if transcripts_df.empty:
                logger.warning("⚠️ No transcripts found in input file.")
                return

            logger.success(f"✅ Loaded {len(transcripts_df)} transcripts for processing.")

            # Step 2: Summarization
            transcripts_df = self.summarizer.summarize_meetings(transcripts_df)
            summary_path = os.path.join(self.output_dir, "meeting_summaries.csv")
            transcripts_df.to_csv(summary_path, index=False)
            logger.success(f"💾 Summaries saved to: {summary_path}")

            # Step 3: Keyword Extraction
            transcripts_df = self.keyword_extractor.extract_keywords(transcripts_df)
            keywords_path = os.path.join(self.output_dir, "meeting_keywords.csv")
            transcripts_df.to_csv(keywords_path, index=False)
            logger.success(f"💾 Keywords saved to: {keywords_path}")

            # Step 4: Intent Extraction
            transcripts_df = self.intent_extractor.extract_intent(transcripts_df)
            intent_path = os.path.join(self.output_dir, "meeting_intents.csv")
            transcripts_df.to_csv(intent_path, index=False)
            logger.success(f"💾 Intents saved to: {intent_path}")

            # Step 5: PDF Generation
            self.pdf_generator.generate_pdfs(transcripts_df, self.pdf_dir)
            logger.success(f"🎉 All Minutes of Meeting PDFs generated successfully in {self.pdf_dir}")

            logger.success("✅ AutoMoM Pipeline (Summarizer → PDF) Completed Successfully!")

        except Exception as e:
            raise AutoMoMException(e, sys)
