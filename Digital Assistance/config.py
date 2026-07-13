import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from parent workspace directory
parent_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=parent_env_path)

# Base directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploaded_documents"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# LLM & Embedding configuration
# Default Groq model to use (llama-3.3-70b-specdec is fast and powerful)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-specdec")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Local embeddings model name
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
