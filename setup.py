from setuptools import setup, find_packages

setup(
    name="automom",
    version="1.0.0",
    author="Shivani Singh",
    author_email="23001016511@jcboseust.ac.in",
    description="AutoMoM - An NLP-based system that summarizes meeting transcripts and generates Minutes of Meeting (MoM) automatically.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shivanam28/AutoMoM---Automated-Minutes-of-Meeting-Generator",  
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=open("requirements.txt", encoding="utf-8").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
)
