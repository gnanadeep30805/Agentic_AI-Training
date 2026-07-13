import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader
import re
import config

# Initialize local HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL_NAME,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

def process_pdf(pdf_path: Path) -> int:
    """
    Loads a PDF file, splits it into chunks with metadata (source & page),
    generates embeddings, and adds them to the FAISS vector database.
    
    Args:
        pdf_path (Path): Path to the PDF file.
        
    Returns:
        int: Number of chunks added.
    """
    # 1. Load document
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    
    # 2. Split document
    # Recommended: Chunk Size 500-1000, Overlap 100-200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    
    # 3. Enhance Metadata
    for chunk in chunks:
        # Get base filename
        filename = Path(chunk.metadata.get("source", pdf_path.name)).name
        chunk.metadata["source_name"] = filename
        
        # Ensure page number is 1-indexed (PyPDFLoader is 0-indexed, let's keep page info)
        page_num = chunk.metadata.get("page", 0) + 1
        chunk.metadata["page_number"] = page_num
        
    # 4. Save/Update Vector Store
    if not chunks:
        return 0
        
    index_path = config.VECTOR_STORE_DIR / "faiss_index"
    
    if index_path.exists():
        # Load existing database
        db = FAISS.load_local(
            folder_path=str(config.VECTOR_STORE_DIR),
            embeddings=embeddings,
            index_name="faiss_index",
            allow_dangerous_deserialization=True  # Required for loading local FAISS binary safely
        )
        # Add new documents
        db.add_documents(chunks)
    else:
        # Create new database
        db = FAISS.from_documents(chunks, embeddings)
        
    # Save the updated database
    db.save_local(folder_path=str(config.VECTOR_STORE_DIR), index_name="faiss_index")
    
    return len(chunks)


def extract_pdf_topics(pdf_path: Path, max_pages: int = 5) -> list[str]:
    """Extract candidate headings or table-of-contents topics from a PDF."""
    reader = PdfReader(str(pdf_path))
    topics: list[str] = []

    for page_index in range(min(max_pages, len(reader.pages))):
        text = reader.pages[page_index].extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            if re.search(r'\btable of contents\b', line, re.I):
                if line not in topics:
                    topics.append(line)
                continue

            if re.match(r'^(Chapter\s+\d+|Section\s+\d+|\d+\.\d+|\d+\.\d+\.\d+)', line, re.I):
                if line not in topics:
                    topics.append(line)
                continue

            if len(line) < 120 and re.search(r'^[A-Z][A-Za-z0-9\s:\-\(\)]+$', line) and sum(1 for c in line if c.isupper()) >= max(3, len(line) // 8):
                if line not in topics:
                    topics.append(line)

        if len(topics) >= 40:
            break

    return topics[:40]


def load_all_document_topics(max_pages: int = 5) -> dict[str, list[str]]:
    """Load extracted topics for all PDFs in the upload folder."""
    topics_by_file: dict[str, list[str]] = {}
    for pdf_path in config.UPLOAD_DIR.glob("*.pdf"):
        topics_by_file[pdf_path.name] = extract_pdf_topics(pdf_path, max_pages=max_pages)
    return topics_by_file


def get_vector_store():
    """
    Loads and returns the FAISS vector store if it exists, otherwise None.
    """
    index_path = config.VECTOR_STORE_DIR / "faiss_index"
    if not index_path.exists():
        return None
    try:
        return FAISS.load_local(
            folder_path=str(config.VECTOR_STORE_DIR),
            embeddings=embeddings,
            index_name="faiss_index",
            allow_dangerous_deserialization=True
        )
    except Exception:
        return None

def clear_vector_store():
    """
    Deletes the FAISS index files and uploaded documents.
    """
    # Clear index files
    for filename in ["faiss_index.faiss", "faiss_index.pkl"]:
        file_path = config.VECTOR_STORE_DIR / filename
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception:
                pass
                
    # Clear uploaded documents
    for file_path in config.UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            try:
                os.remove(file_path)
            except Exception:
                pass
