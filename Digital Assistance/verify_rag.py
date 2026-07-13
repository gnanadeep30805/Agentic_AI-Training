import os
import sys
import shutil
from pathlib import Path
import config
import document_processor
import rag_engine

def run_verification():
    print("==================================================")
    print("⚙️ STARTING RAG SYSTEM VERIFICATION")
    print("==================================================")

    # 1. Check API Key
    if not config.GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY is not set. Please set it in your environment or parent folder's .env file.")
        sys.exit(1)
    print(f"✓ GROQ_API_KEY detected. Model to use: {config.GROQ_MODEL}")

    # 2. Reset database and clean up upload folder for testing
    print("\n🧹 Cleaning up old database and uploads...")
    document_processor.clear_vector_store()
    print("✓ DB and uploads cleared successfully.")

    # 3. Locate Sample PDF and copy it
    parent_dir = Path(__file__).resolve().parent.parent
    sample_pdf = parent_dir / "Gnanadeep_Yenneti.pdf"
    
    if not sample_pdf.exists():
        print(f"❌ Error: Sample PDF not found at {sample_pdf}")
        sys.exit(1)
        
    print(f"✓ Found sample PDF: {sample_pdf.name}")
    dest_pdf_path = config.UPLOAD_DIR / sample_pdf.name
    shutil.copy(sample_pdf, dest_pdf_path)
    print(f"✓ Copied to: {dest_pdf_path}")

    # 4. Ingest and Process PDF
    print("\n📦 Processing and Ingesting PDF into FAISS database...")
    try:
        chunks = document_processor.process_pdf(dest_pdf_path)
        print(f"✓ Successfully processed PDF. Generated and stored {chunks} chunks.")
    except Exception as e:
        print(f"❌ Error during PDF processing: {str(e)}")
        sys.exit(1)

    # 5. Retrieve Vector DB Verify
    db = document_processor.get_vector_store()
    if db is None:
        print("❌ Error: FAISS index was not created or failed to load.")
        sys.exit(1)
    print("✓ Vector database is loaded and active.")

    # 6. Test RAG Queries
    # Test Query 1: Information that is present in the document
    # Since Gnanadeep_Yenneti.pdf is likely a resume or bio, let's ask a generic question that would have an answer, like "What is the name in the document?" or "What education details are mentioned?"
    query_in = "What education or projects are listed in the document?"
    print(f"\n🔍 Querying (expecting answer): '{query_in}'")
    
    res_in = rag_engine.query_rag(query_in)
    print(f"Answer:\n{res_in['answer']}")
    print(f"Sources: {res_in['sources']}")
    
    if not res_in['sources']:
        print("⚠️ Warning: No sources were cited for the answer.")
    else:
        print("✓ Sources cited successfully.")

    # Test Query 2: Information that is NOT present in the document
    query_out = "What are the rules about hostel fees and library timings for master students?"
    print(f"\n🔍 Querying (expecting failure): '{query_out}'")
    
    res_out = rag_engine.query_rag(query_out)
    print(f"Answer:\n{res_out['answer']}")
    print(f"Sources: {res_out['sources']}")
    
    expected_failure_msg = "This information was not found in the uploaded documents."
    if expected_failure_msg in res_out['answer']:
        print("✓ Correctly returned the 'Not Found' message.")
    else:
        print(f"❌ Expected answer to contain: '{expected_failure_msg}' but got: '{res_out['answer']}'")

    print("\n==================================================")
    print("🎉 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_verification()
