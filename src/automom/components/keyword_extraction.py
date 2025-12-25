from keybert import KeyBERT
import pandas as pd
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException
import sys

class KeywordExtractor:
    def __init__(self):
        logger.info("🔍 Initializing Keyword Extractor using KeyBERT...")
        self.model = KeyBERT('sentence-transformers/all-MiniLM-L6-v2')

    def extract_keywords(self, df):
        """Extract keywords for each meeting transcript."""
        try:
            logger.info("🧩 Extracting keywords from transcripts...")

            keywords_list = []
            for i, row in df.iterrows():
                text = str(row.get("transcript_text", ""))  # ✅ get text safely as string
                if not text.strip():  # ✅ check only if it's a string
                    keywords_list.append("No transcript text available.")
                    continue

                # ✅ Extract top 5 keywords
                keywords = self.model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
                keywords_text = ", ".join([kw[0] for kw in keywords])
                keywords_list.append(keywords_text)

                if (i + 1) % 5 == 0:
                    logger.info(f"✅ Processed {i + 1}/{len(df)} transcripts")

            df["keywords"] = keywords_list

            output_path = "data/processed/meeting_keywords.csv"
            df.to_csv(output_path, index=False)
            logger.success(f"💾 Keywords saved to: {output_path}")

            return df

        except Exception as e:
            raise AutoMoMException(e, sys)
