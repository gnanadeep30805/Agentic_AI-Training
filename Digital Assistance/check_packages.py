import importlib
import sys

packages = ["langchain", "langchain_community", "langchain_core", "langchain_groq", "streamlit", "pypdf", "faiss", "chromadb", "sentence_transformers", "langchain_huggingface", "dotenv"]

print(f"Python version: {sys.version}")
for package in packages:
    try:
        importlib.import_module(package)
        print(f"  {package}: AVAILABLE")
    except ImportError as e:
        print(f"  {package}: NOT AVAILABLE ({e})")
