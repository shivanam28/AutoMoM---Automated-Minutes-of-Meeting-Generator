import streamlit as st
import pandas as pd
import os
from automom.components.summarizer import Summarizer
from automom.components.keyword_extraction import KeywordExtractor
from automom.components.intent_extraction import IntentExtractor
from automom.components.pdf_generator import PDFGenerator
from automom.utils.logger import logger

st.set_page_config(page_title="AutoMoM - Meeting Summarizer", page_icon="🧠", layout="centered")

# Title
st.title("🧠 AutoMoM - Automated Minutes of Meeting Generator")
st.markdown("Upload your meeting transcript (.txt or .csv) and generate summarized minutes automatically!")

# File uploader
uploaded_file = st.file_uploader("📂 Upload Meeting Transcript File", type=["txt", "csv"])

if uploaded_file:
    # Read input file
    if uploaded_file.name.endswith(".txt"):
        transcript_text = uploaded_file.read().decode("utf-8")
        data = pd.DataFrame([{"region": "Unknown", "meeting_id": uploaded_file.name, "transcript_text": transcript_text}])
    else:
        data = pd.read_csv(uploaded_file)

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # Generate MoM button
    if st.button("🚀 Generate Minutes of Meeting"):
        with st.spinner("Processing... This may take a few seconds ⏳"):
            try:
                # Summarization
                st.info("🧠 Summarizing transcript using BART...")
                summarizer = Summarizer(model_name="facebook/bart-large-cnn")
                data = summarizer.generate_summaries(data)

                # Keyword extraction
                st.info("🔑 Extracting keywords using KeyBERT...")
                keyword_extractor = KeywordExtractor()
                data = keyword_extractor.extract_keywords(data)

                # Intent extraction
                st.info("🎯 Identifying intents using BART MNLI...")
                intent_extractor = IntentExtractor()
                data = intent_extractor.extract_intent(data)

                # Save PDFs
                st.info("📝 Generating final PDF report...")
                output_dir = "data/processed/pdfs"
                os.makedirs(output_dir, exist_ok=True)
                pdf_generator = PDFGenerator(output_dir=output_dir)
                pdf_generator.generate_pdf(data)

                pdf_file = os.path.join(output_dir, f"{data.iloc[0]['meeting_id']}_MoM.pdf")
                if os.path.exists(pdf_file):
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📥 Download Minutes of Meeting (PDF)",
                            data=f,
                            file_name=f"{data.iloc[0]['meeting_id']}_MoM.pdf",
                            mime="application/pdf"
                        )
                    st.success("🎉 Minutes of Meeting generated successfully!")
                else:
                    st.error("⚠️ PDF generation failed. Please check logs.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
