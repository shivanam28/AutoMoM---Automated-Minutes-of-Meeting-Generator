# 📝 AutoMoM – Automated Minutes of Meeting Generator

AutoMoM is an **AI-powered system** that automatically generates **professional Minutes of Meeting (MoM)** from raw meeting transcripts. The project leverages **Natural Language Processing (NLP)** and **Transformer-based models** to summarize discussions, extract key topics, identify meeting intents, and generate a well-structured **PDF MoM report** — all in a single pipeline.

---

## Key Features

- **Automatic Meeting Summarization**  
  Converts long meeting transcripts (1000–8000 words) into concise summaries using Transformer models.

- **Keyword Extraction**  
  Identifies important discussion points and themes using semantic embeddings.

- **Intent Extraction**  
  Detects meeting intents such as decisions, actions, updates, and discussions.

- 🧾 **Professional PDF MoM Generation**  
  Generates a structured and readable Minutes of Meeting PDF.

- 🖥 **User-Friendly GUI (Streamlit)**  
  Upload `.txt` or `.csv` transcript files and download the MoM report easily.

---

## Project Workflow

1. User uploads meeting transcript (Text / CSV)
2. Transcript is summarized using an NLP model
3. Keywords are extracted from the meeting
4. Intents are classified from discussions
5. Final **Minutes of Meeting PDF** is generated

---

## Technologies Used

- Python  
- HuggingFace Transformers (BART)  
- KeyBERT  
- Sentence-Transformers  
- Pandas & NumPy  
- ReportLab (PDF Generation)  
- Streamlit (GUI)  
- Git & GitHub  

---

## How to Run the Project

### 1️⃣ Create Virtual Environment
conda create -n automom python=3.10
conda activate automom

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Run Streamlit App
streamlit run app.py

---

## Future Enhancements

- Audio-to-text transcription support
- Cloud deployment  
- Speaker-wise segmentation  

---

## Author & Partners

Shivani Singh <br>
B.Tech Data Science <br>
J.C.Bose University of Science and Technology

Mehak Rana <br>
B.Tech Data Science <br>
J.C.Bose University of Science and Technology

---

## License

This project is developed for **academic and learning puposes**.


