# 📝 AutoMoM – Automated Minutes of Meeting Generator

AutoMoM is an **AI-powered system** that automatically generates **professional Minutes of Meeting (MoM)** from raw meeting transcripts. The project leverages **Natural Language Processing (NLP)** and **Transformer-based pretrained models** to summarize discussions, extract key topics, identify meeting intent, and generate a well-structured **PDF MoM report** — all in a single, lightweight pipeline.

No training or custom dataset is required — the entire pipeline runs on pretrained models via inference only.

---

## Key Features

- **Automatic Meeting Summarization**
  Converts long meeting transcripts (tested up to ~8000 words) into concise summaries using BART, with automatic chunking so long transcripts are never silently truncated.
- **Keyword Extraction**
  Identifies important discussion points and themes using KeyBERT with sentence-transformer embeddings.
- **Intent Extraction**
  Classifies each meeting's primary intent (e.g. Policy Discussion, Budget Meeting, Action Items) using zero-shot classification — no labeled training data needed.
- 🧾 **Professional PDF MoM Generation**
  Generates a structured, readable Minutes of Meeting PDF from the pipeline's output.
- 🖥 **User-Friendly GUI (Streamlit)**
  Upload a `.txt` transcript and download the finished MoM report directly from the browser.
- 🖲 **CLI Support**
  Run the exact same pipeline from the command line — useful for batch processing, scripting, and testing without launching the UI.

---

## Project Workflow

1. User uploads a `.txt` meeting transcript (via Streamlit UI or as a CLI argument)
2. Transcript is summarized using BART (`facebook/bart-large-cnn`)
3. Keywords are extracted using KeyBERT + MiniLM embeddings
4. Meeting intent is classified using zero-shot classification (`facebook/bart-large-mnli`)
5. Final **Minutes of Meeting PDF** is generated and made available to download

---

## Project Structure

```
AutoMoM/
├── app.py                      # Streamlit UI — thin wrapper around the pipeline
├── main.py                     # CLI entry point — same pipeline, no browser needed
├── requirements.txt
└── src/
    └── automom/
        ├── __init__.py
        ├── pipeline.py         # Core NLP stages: summarize, extract_keywords, extract_intent
        └── pdf_export.py       # PDF generation from pipeline output
```

Both `app.py` and `main.py` call the same `generate_mom()` function in `pipeline.py` — the core pipeline logic is fully decoupled from the interface used to run it.

---

## Technologies Used

- Python
- HuggingFace Transformers (BART, BART-MNLI)
- KeyBERT
- Sentence-Transformers (MiniLM)
- ReportLab (PDF generation)
- Streamlit (GUI)
- Git & GitHub

---

## How to Run the Project

### 1️⃣ Create a Virtual Environment

```bash
conda create -n automom python=3.10
conda activate automom
```

### 2️⃣ Install PyTorch (CPU build)

PyTorch's CPU wheel must be installed from PyTorch's own index — it isn't resolvable via a plain `pip install`:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 3️⃣ Install Remaining Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

**Or, run it from the command line instead:**

```bash
python main.py path/to/transcript.txt
```

> ℹ️ The first run will download the pretrained models (~1GB combined) from HuggingFace. This only happens once — subsequent runs load instantly from the local cache.

---

## Future Enhancements

- Audio-to-text transcription support
- Cloud deployment
- Speaker-wise segmentation
- CSV/batch upload support in the Streamlit UI

---

## Author

Shivani Singh <br>
B.Tech Data Science <br>
J.C. Bose University of Science and Technology


---

## License

This project is developed for **academic and learning purposes**.
