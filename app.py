"""
AutoMoM Streamlit App
----------------------
Upload a .txt meeting transcript -> get back a PDF Minutes-of-Meeting.
This file only handles UI. All logic lives in src/automom/pipeline.py
and src/automom/pdf_export.py.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
import streamlit as st

from automom.pipeline import generate_mom
from automom.pdf_export import export_to_pdf

st.set_page_config(page_title="AutoMoM", page_icon="🧠", layout="centered")

st.title("🧠 AutoMoM — Automated Minutes of Meeting Generator")
st.markdown("Upload a `.txt` meeting transcript and generate a Minutes-of-Meeting PDF.")

uploaded_file = st.file_uploader("📂 Upload transcript (.txt)", type=["txt"])

if uploaded_file:
    transcript_text = uploaded_file.read().decode("utf-8")
    meeting_id = os.path.splitext(uploaded_file.name)[0]

    st.success(f"File '{uploaded_file.name}' loaded — {len(transcript_text.split())} words.")

    if st.button("🚀 Generate Minutes of Meeting"):
        with st.spinner("Running pipeline: summarizing → extracting keywords → detecting intent..."):
            try:
                mom = generate_mom(transcript_text, meeting_id=meeting_id)

                output_dir = "data/processed/pdfs"
                pdf_path = os.path.join(output_dir, f"{meeting_id}_MoM.pdf")
                export_to_pdf(mom, pdf_path)

                st.subheader("📝 Summary")
                st.write(mom["summary"])

                st.subheader("🔑 Keywords")
                st.write(", ".join(mom["keywords"]))

                st.subheader("🎯 Intent")
                st.write(mom["intent"])

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Minutes of Meeting (PDF)",
                        data=f,
                        file_name=f"{meeting_id}_MoM.pdf",
                        mime="application/pdf",
                    )

            except Exception as e:
                st.error(f"❌ Pipeline failed: {e}")
