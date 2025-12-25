import sys
import pandas as pd
from transformers import pipeline
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException


class IntentExtractor:
    """
    Uses a zero-shot classification model (BART MNLI)
    to infer the main intent or topic of each meeting transcript.
    """

    def __init__(self):
        try:
            logger.info("🎯 Initializing Intent Extractor using BART MNLI model...")
            self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            self.labels = [
                "Policy Discussion",
                "Budget Meeting",
                "Community Issue",
                "Infrastructure Planning",
                "Environmental Concerns",
                "Public Health",
                "Education",
                "Administrative Updates",
            ]
        except Exception as e:
            raise AutoMoMException(e, sys)

    def extract_intent(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes a dataframe with 'transcript_text' column and returns
        a new dataframe with an added 'intent' column.
        """
        try:
            intents = []
            for _, row in df.iterrows():
                text = str(row["transcript_text"])[:1000]  # limit input length
                result = self.classifier(text, self.labels)
                top_intent = result["labels"][0] if result and "labels" in result else "General Discussion"
                intents.append(top_intent)

            df["intent"] = intents
            output_path = "data/processed/meeting_intents.csv"
            df.to_csv(output_path, index=False)
            logger.success(f"💾 Meeting intents saved to: {output_path}")
            return df

        except Exception as e:
            raise AutoMoMException(e, sys)
































# import sys
# from transformers import pipeline
# from automom.utils.logger import logger
# from automom.utils.exception import AutoMoMException
# import pandas as pd

# class IntentExtractor:
#     def __init__(self):
#         logger.info("🎯 Initializing Intent Extractor using BART MNLI model...")
#         self.intent_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

#     def extract_intents(self, df):  # ✅ fixed name
#         """Extract meeting intent (main discussion category) for each transcript."""
#         try:
#             candidate_labels = [
#                 "budget discussion", "policy decision", "public announcement", 
#                 "infrastructure planning", "environmental issue", "housing", 
#                 "transportation", "public safety", "education", "general discussion"
#             ]

#             intents = []
#             for i, row in df.iterrows():
#                 text = str(row.get("transcript_text", ""))[:3000]  # trim long texts
#                 if not text.strip():
#                     intents.append("unknown")
#                     continue

#                 result = self.intent_model(text, candidate_labels)
#                 intent = result["labels"][0] if result["labels"] else "unknown"
#                 intents.append(intent)

#                 if (i + 1) % 5 == 0:
#                     logger.info(f"🧭 Processed {i + 1}/{len(df)} transcripts")

#             df["intent"] = intents
#             output_path = "data/processed/meeting_intents.csv"
#             df.to_csv(output_path, index=False)
#             logger.success(f"💾 Meeting intents saved to: {output_path}")
#             return df

#         except Exception as e:
#             raise AutoMoMException(e, sys)
