import sys
import pandas as pd
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException
from automom.components.summarizer import Summarizer
from automom.components.keyword_extraction import KeywordExtractor
from automom.components.intent_extraction import IntentExtractor
from automom.components.pdf_generator import PDFGenerator

def run_automom_pipeline():
    try:
        logger.info("🚀 Starting AutoMoM - Automated Minutes of Meeting Generator...")

        # -------------------- FILE PATH --------------------
        input_csv = "data/processed/test_transcripts.csv"

        # Load transcripts
        logger.info(f"📄 Loading meeting transcripts from: {input_csv}")
        transcripts_df = pd.read_csv(input_csv)
        logger.info(f"✅ Loaded {len(transcripts_df)} transcripts for processing")

        # -------------------- SUMMARIZATION --------------------
        logger.info("🧠 Starting summarization process using BART model...")
        summarizer = Summarizer(model_name="facebook/bart-large-cnn")
        transcripts_df = summarizer.generate_summaries(transcripts_df)
        logger.success("💾 Summaries saved successfully!")

        # -------------------- KEYWORD EXTRACTION --------------------
        logger.info("🧩 Starting keyword extraction using KeyBERT...")
        keyword_extractor = KeywordExtractor()
        transcripts_df = keyword_extractor.extract_keywords(transcripts_df)
        logger.success("💾 Keywords extracted successfully!")

        # -------------------- INTENT EXTRACTION --------------------
        logger.info("🎯 Starting intent extraction using BART MNLI model...")
        intent_extractor = IntentExtractor()

        # Handles both method names
        if hasattr(intent_extractor, "extract_intent"):
            transcripts_df = intent_extractor.extract_intent(transcripts_df)
        elif hasattr(intent_extractor, "extract_intents"):
            transcripts_df = intent_extractor.extract_intents(transcripts_df)
        else:
            raise AttributeError("IntentExtractor missing both 'extract_intent' and 'extract_intents' methods!")

        logger.success("💾 Intents extracted successfully!")

        # -------------------- PDF GENERATION --------------------
        logger.info("📝 Generating final MoM PDF reports...")
        pdf_generator = PDFGenerator()
        pdf_generator.generate_pdf(transcripts_df)
        logger.success("🎉 All MoM PDFs generated successfully!")

        # -------------------- DONE --------------------
        logger.success("✅ AutoMoM Pipeline Completed Successfully!")

    except Exception as e:
        raise AutoMoMException(e, sys)

if __name__ == "__main__":
    run_automom_pipeline()
