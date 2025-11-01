import os

# 🧠 Project folder structure for AutoMoM (Automated Minutes of Meeting Generator)
project_structure = {
    ".github/workflows": ["main.yaml"],
    "config": ["config.yaml", "params.yaml"],
    "data": ["meeting_transcript.txt"],
    "logs": ["running_logs.log"],
    "notebooks": ["experiments.ipynb"],
    "outputs": [],
    "src/automom/components": [
        "__init__.py",
        "data_ingestion.py",
        "summarizer.py",
        "keyword_extraction.py",
        "intent_extraction.py",
        "mom_generator.py",
        "pdf_generator.py"
    ],
    "src/automom/utils": [
        "__init__.py",
        "logger.py",
        "exception.py",
        "common.py"
    ],
    "src/automom/pipeline": [
        "__init__.py",
        "generate_mom.py"
    ]
}

# 🧾 Root-level files
root_files = ["main.py", "requirements.txt", "setup.py", "README.md"]

# Function to create folders & files
def create_project_structure(base_path="."):
    print("\n🚀 Creating AutoMoM project structure...\n")

    for folder, files in project_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"📁 Created folder: {folder_path}")
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")  # create empty files
            print(f"   📄 Created file: {file_path}")

    for file in root_files:
        with open(os.path.join(base_path, file), "w", encoding="utf-8") as f:
            if file == "README.md":
                f.write("# 🧠 AutoMoM - Automated Minutes of Meeting Generator\n\n")
                f.write("AutoMoM is an NLP-based system that summarizes meeting transcripts, extracts key points, and generates structured minutes of meeting (MoM) reports automatically.\n")
            elif file == "requirements.txt":
                f.write("""torch==2.7.1+cpu
transformers==4.45.2
keybert==0.8.5
sentence-transformers==3.1.1
pyyaml==6.0.1
loguru==0.7.2
fpdf2==2.7.8
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.5.2
streamlit==1.39.0
""")
            elif file == "main.py":
                f.write("""import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from automom.pipeline.generate_mom import run_pipeline

if __name__ == "__main__":
    run_pipeline("data/meeting_transcript.txt")
""")
            elif file == "setup.py":
                f.write("""from setuptools import setup, find_packages

setup(
    name='automom',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').read().splitlines(),
)
""")
        print(f"📄 Created root file: {file}")

    print("\n✅ Project structure created successfully!\n")

if __name__ == "__main__":
    create_project_structure()
