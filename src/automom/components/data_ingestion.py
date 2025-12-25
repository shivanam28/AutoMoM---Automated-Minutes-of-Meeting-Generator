"""
Robust Data Ingestion for MeetingBank / AutoMoM
- Scans all subfolders under data/MeetingBank/Audio&Transcripts
- Loads each .json transcript file
- Extracts: meeting_id, region, meeting_type, meeting_date, transcript_text, raw_json_path
- Saves a CSV: data/processed/meeting_transcripts_all.csv
"""

import os
import json
import pandas as pd
from typing import Any, Dict, List, Optional
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException
import sys

# optional date parsing - pandas includes dateutil; try import directly
try:
    from dateutil.parser import parse as parse_date
except Exception:
    parse_date = None  # fallback to raw string if not available


class DataIngestion:
    def __init__(self, base_dir: str = "data/MeetingBank/Audio&Transcripts"):
        self.base_dir = base_dir
        self.processed_dir = "data/processed"
        os.makedirs(self.processed_dir, exist_ok=True)

    # ---------- helpers ----------
    def _safe_get(self, d: Dict[str, Any], keys: List[str]) -> Optional[Any]:
        """Return first non-empty value for keys in dict d."""
        for k in keys:
            if k in d and d[k] not in (None, "", [], {}):
                return d[k]
        return None

    def _parse_date(self, date_val: Any) -> str:
        """Try to parse the date into ISO format, otherwise return original string."""
        if date_val is None:
            return "unknown"
        if isinstance(date_val, (int, float)):
            try:
                # timestamp
                return pd.to_datetime(date_val, unit="s").isoformat()
            except Exception:
                return str(date_val)
        if isinstance(date_val, str):
            if parse_date:
                try:
                    dt = parse_date(date_val)
                    return dt.isoformat()
                except Exception:
                    return date_val
            else:
                # fallback: let pandas try
                try:
                    return pd.to_datetime(date_val).isoformat()
                except Exception:
                    return date_val
        return str(date_val)

    def _extract_transcript_from_obj(self, obj: Any) -> str:
        """
        Given various possible structures, return combined transcript text.
        obj may be:
          - list of dicts (utterances) with speaker/text keys
          - dict containing 'transcript', 'Utterances', 'results', 'items', etc.
          - plain string
        """
        texts: List[str] = []

        # If it's a string, return directly
        if isinstance(obj, str):
            return obj.strip()

        # If it's a list, iterate entries
        if isinstance(obj, list):
            for entry in obj:
                if isinstance(entry, str):
                    texts.append(entry.strip())
                elif isinstance(entry, dict):
                    # common text keys
                    text_val = self._safe_get(entry, ["text", "content", "transcript", "utterance", "utteranceText", "utterances"])
                    if isinstance(text_val, list):
                        # nested list - recurse
                        texts.append(self._extract_transcript_from_obj(text_val))
                        continue
                    # look for nested 'results' structure
                    if text_val is None:
                        # maybe the dict contains 'items' or 'alternatives' or 'speaker' + 'words'
                        # try to join words
                        if "items" in entry and isinstance(entry["items"], list):
                            word_parts = []
                            for it in entry["items"]:
                                w = self._safe_get(it, ["content", "text", "word"])
                                if w:
                                    word_parts.append(str(w))
                            if word_parts:
                                texts.append(" ".join(word_parts))
                                continue
                        # fallback to joining all string values
                        values = [str(v) for v in entry.values() if isinstance(v, str)]
                        if values:
                            texts.append(" ".join(values))
                            continue
                    else:
                        # If text_val is dict or list, recurse; else treat as string
                        if isinstance(text_val, (dict, list)):
                            texts.append(self._extract_transcript_from_obj(text_val))
                        else:
                            # include speaker if available
                            speaker = self._safe_get(entry, ["speaker", "spk", "participant", "speaker_id", "speakerName"])
                            if speaker:
                                texts.append(f"{speaker}: {str(text_val).strip()}")
                            else:
                                texts.append(str(text_val).strip())
                else:
                    # unknown entry type - stringify
                    texts.append(str(entry))
            return "\n".join([t for t in texts if t])

        # If it's a dict, try typical keys or nested objects
        if isinstance(obj, dict):
            # keys that may hold the transcript segments
            for key in ["transcript", "Transcript", "Utterances", "utterances", "results", "items", "segments", "alternatives"]:
                if key in obj and obj[key] not in (None, "", []):
                    return self._extract_transcript_from_obj(obj[key])
            # maybe dict keys are speakers mapping to lists
            # join all string values
            for k, v in obj.items():
                if isinstance(v, str) and len(v) > 20:  # heuristic
                    texts.append(v.strip())
                elif isinstance(v, (list, dict)):
                    texts.append(self._extract_transcript_from_obj(v))
            return "\n".join([t for t in texts if t])

        # fallback: stringify
        return str(obj)

    def load_single_transcript(self, file_path: str) -> Dict[str, str]:
        """Load a single JSON transcript and extract fields robustly."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise AutoMoMException(f"Failed to load JSON: {file_path} ; {e}", sys) from e

        try:
            # meeting id candidates
            meeting_id = self._safe_get(data, ["id", "meeting_id", "file", "filename", "meetingName"]) or os.path.splitext(os.path.basename(file_path))[0]

            # meeting type/category
            meeting_type = self._safe_get(data, ["meeting_type", "type", "category", "meetingName", "title"]) or "unknown"

            # meeting date candidates
            date_val = self._safe_get(data, ["meeting_date", "date", "meetingDate", "recorded_on", "start_time", "startTime", "meeting_start"])
            meeting_date = self._parse_date(date_val) if date_val else "unknown"

            # region inferred from directory name relative to base_dir
            try:
                rel = os.path.relpath(file_path, self.base_dir)
                parts = rel.split(os.sep)
                region = parts[0] if len(parts) > 1 else "unknown"
            except Exception:
                region = "unknown"

            # transcript contents - try many keys first
            transcript_candidate = self._safe_get(data, ["transcript", "Transcript", "utterances", "Utterances", "content", "results", "items", "segments", "alternatives"])
            if transcript_candidate is None:
                # maybe file itself is just a dict with speaker entries or nested under other keys
                transcript_text = self._extract_transcript_from_obj(data)
            else:
                transcript_text = self._extract_transcript_from_obj(transcript_candidate)

            # clean up whitespace
            transcript_text = transcript_text.strip()
            if not transcript_text:
                logger.warning(f"Empty transcript text extracted for {file_path}; trying to join all text-like fields.")
                # last resort: join all string fields
                parts = []
                def collect_strings(obj):
                    if isinstance(obj, str):
                        parts.append(obj.strip())
                    elif isinstance(obj, list):
                        for it in obj:
                            collect_strings(it)
                    elif isinstance(obj, dict):
                        for v in obj.values():
                            collect_strings(v)
                collect_strings(data)
                transcript_text = "\n".join([p for p in parts if len(p) > 10])[:20000]  # limit size
                if not transcript_text:
                    transcript_text = "unknown"

            # final fallbacks
            if meeting_type in (None, "", "unknown"):
                meeting_type = "unknown"
            if meeting_date in (None, "", "unknown"):
                meeting_date = "unknown"
            if transcript_text in (None, "", "unknown"):
                transcript_text = "unknown"

            return {
                "region": region,
                "meeting_id": meeting_id,
                "meeting_type": meeting_type,
                "meeting_date": meeting_date,
                "transcript_text": transcript_text,
                "raw_json_path": file_path,
            }

        except Exception as e:
            raise AutoMoMException(f"Error extracting data from {file_path}: {e}", sys) from e

    def load_all_transcripts(self) -> pd.DataFrame:
        """Walk base_dir and ingest all .json transcript files."""
        try:
            logger.info(f"🔍 Scanning all transcript folders under: {self.base_dir}")
            all_meetings = []
            for root, _, files in os.walk(self.base_dir):
                for file in files:
                    if file.lower().endswith(".json"):
                        file_path = os.path.join(root, file)
                        try:
                            record = self.load_single_transcript(file_path)
                            all_meetings.append(record)
                        except Exception as e:
                            # log file-level errors and continue
                            logger.error(f"Failed to process {file_path}: {e}")
                            continue
            df = pd.DataFrame(all_meetings)
            logger.success(f"✅ Loaded {len(df)} transcripts from all regions.")
            return df
        except Exception as e:
            raise AutoMoMException(e, sys) from e

    def save_processed_data(self, df: pd.DataFrame, output_path: Optional[str] = None):
        try:
            if output_path is None:
                output_path = os.path.join(self.processed_dir, "meeting_transcripts_all.csv")
            df.to_csv(output_path, index=False, encoding="utf-8")
            logger.success(f"💾 Processed transcripts saved to: {output_path}")
        except Exception as e:
            raise AutoMoMException(e, sys) from e


# # quick-run support
# if __name__ == "__main__":
#     ingestion = DataIngestion(base_dir="data/MeetingBank/Audio&Transcripts")
#     df = ingestion.load_all_transcripts()
#     print(df.head(10).to_string(index=False))
#     ingestion.save_processed_data(df)

#     # ✅ Optional: Create a smaller version of the dataset for testing/summarization
#     try:
#         small_sample_size = 20  # <-- change this number if needed
#         if len(df) > small_sample_size:
#             small_df = df.sample(small_sample_size, random_state=42)
#             small_output_path = os.path.join("data", "processed", "meeting_transcripts_small.csv")
#             small_df.to_csv(small_output_path, index=False, encoding="utf-8")
#             logger.success(f"📉 Small sample CSV created: {small_output_path} ({len(small_df)} records)")
#         else:
#             logger.info("Dataset is already small — skipping sample creation.")
#     except Exception as e:
#         logger.error(f"⚠️ Could not create small dataset sample: {e}")
