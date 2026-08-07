"""
AutoMoM Core Pipeline
----------------------
A sequential NLP pipeline: transcript text -> summary -> keywords -> intent.
Uses only pretrained models (no training, no dataset required).

Models used:
- Summarization : facebook/bart-large-cnn
- Keywords      : KeyBERT (all-MiniLM-L6-v2 embeddings)
- Intent        : facebook/bart-large-mnli (zero-shot classification)
"""

from transformers import pipeline
from keybert import KeyBERT

# ---------------------------------------------------------------------
# Fixed candidate labels for zero-shot intent classification.
# Edit this list to change what categories the pipeline can detect.
# ---------------------------------------------------------------------
INTENT_LABELS = [
    "Policy Discussion",
    "Budget Meeting",
    "Action Items",
    "Project Update",
    "Technical Discussion",
    "Client Feedback",
    "General Announcement",
]

# ---------------------------------------------------------------------
# Models are loaded lazily (only once, on first use) and cached here.
# This avoids reloading a multi-hundred-MB model on every function call.
# ---------------------------------------------------------------------
_summarizer = None
_keyword_model = None
_intent_classifier = None


def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer


def _get_keyword_model():
    global _keyword_model
    if _keyword_model is None:
        _keyword_model = KeyBERT("sentence-transformers/all-MiniLM-L6-v2")
    return _keyword_model


def _get_intent_classifier():
    global _intent_classifier
    if _intent_classifier is None:
        _intent_classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
    return _intent_classifier


# ---------------------------------------------------------------------
# Stage 1: Summarization
# ---------------------------------------------------------------------
def summarize(text: str, max_length: int = 300, min_length: int = 80) -> str:
    """Condense transcript text into a short summary using BART."""
    if not text.strip():
        return "No transcript text available."

    # BART's encoder has a hard 1024-TOKEN limit (not word limit). English
    # averages ~1.3 tokens/word, so we chunk at 600 words to stay safely
    # under that ceiling. truncation=True below is a hard safety net in
    # case any single chunk still tokenizes longer than expected.
    chunks = _chunk_text(text, max_words=600)
    summarizer = _get_summarizer()

    partial_summaries = []
    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True,
        )
        partial_summaries.append(result[0]["summary_text"])

    combined = " ".join(partial_summaries)

    # If we had multiple chunks, do one more pass to summarize the summary.
    # The combined text can itself exceed the token limit on very long
    # transcripts, so it gets the same chunking treatment recursively.
    if len(partial_summaries) > 1:
        return summarize(combined, max_length=max_length, min_length=min_length)

    return combined


def _chunk_text(text: str, max_words: int = 600):
    """Split long text into word-count-limited chunks so BART never truncates silently."""
    words = text.split()
    if len(words) <= max_words:
        return [text]
    return [
        " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
    ]


# ---------------------------------------------------------------------
# Stage 2: Keyword extraction
# ---------------------------------------------------------------------
def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """Pull the top-N keyphrases from the transcript using KeyBERT."""
    if not text.strip():
        return []

    model = _get_keyword_model()
    keywords = model.extract_keywords(
        text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=top_n
    )
    return [kw for kw, score in keywords]


# ---------------------------------------------------------------------
# Stage 3: Intent classification
# ---------------------------------------------------------------------
def extract_intent(text: str) -> str:
    """Classify the transcript's primary intent via zero-shot classification."""
    if not text.strip():
        return "Unknown"

    classifier = _get_intent_classifier()
    # Zero-shot models have their own length limits; keep the input reasonable
    # AND pass truncation=True as a hard safety net against token overflow.
    result = classifier(text[:2000], INTENT_LABELS, truncation=True)
    return result["labels"][0] if result.get("labels") else "Unknown"


# ---------------------------------------------------------------------
# Orchestrator: runs all three stages and returns one clean result dict.
# This is the single function app.py and main.py both call.
# ---------------------------------------------------------------------
def generate_mom(transcript_text: str, meeting_id: str = "Meeting") -> dict:
    """Run the full pipeline on one transcript and return structured MoM data."""
    return {
        "meeting_id": meeting_id,
        "summary": summarize(transcript_text),
        "keywords": extract_keywords(transcript_text),
        "intent": extract_intent(transcript_text),
    }