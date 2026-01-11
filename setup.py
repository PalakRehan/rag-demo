from setuptools import setup, find_packages

setup(
    name="rag-demo",
    version="0.1.0",
    description="Working mini chatbot based on RAG",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.7.0",
        "tqdm>=4.60.0",
        "numpy>=1.21.0",
        "pandas>=2.0.0",
        "sentence-transformers>=2.2.0",
        "transformers>=4.30.0",
        "accelerate>=0.20.0",
        "faiss-cpu>=1.7.0",
        "torch>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
)