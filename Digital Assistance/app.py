import streamlit as st
import os
from pathlib import Path
import config
import document_processor
import rag_engine

# Set Page Config
st.set_page_config(
    page_title="EduRetrieve - College digital assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling / CSS for Premium Aesthetics
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Apply Font */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0e1117;
    }
    
    /* Header decoration */
    .title-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #30363d;
    }
    .title-emoji {
        font-size: 2.5rem;
        margin-right: 15px;
    }
    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Custom status indicators */
    .document-card {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    .document-card:hover {
        border-color: #60a5fa;
        transform: translateY(-2px);
    }
    
    /* Quick Tips */
    .tips-container {
        background-color: #111827;
        border-left: 4px solid #3b82f6;
        padding: 12px;
        border-radius: 4px;
        margin-top: 20px;
        font-size: 0.9rem;
    }
    
    /* Source badges */
    .source-badge {
        display: inline-block;
        background-color: #1e3a8a;
        color: #93c5fd;
        border: 1px solid #2563eb;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        margin-right: 6px;
        margin-top: 4px;
    }
    
    /* Welcome banner */
    .welcome-banner {
        padding: 30px;
        background: linear-gradient(135deg, #1e1b4b, #0f172a);
        border: 1px solid #312e81;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE SETUP -----------------
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

# Helper to get currently uploaded documents in directory
def get_existing_documents():
    return [f.name for f in config.UPLOAD_DIR.glob("*.pdf")]


def make_unique_upload_path(file_path):
    """Return a unique file path, appending a number if the name already exists."""
    if not file_path.exists():
        return file_path

    base = file_path.stem
    suffix = file_path.suffix
    i = 1
    while True:
        candidate = file_path.with_name(f"{base}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


active_docs = get_existing_documents()
document_topics = document_processor.load_all_document_topics()

# ----------------- SIDEBAR UI -----------------
with st.sidebar:
    st.markdown('<div class="title-container"><span class="title-emoji">🎓</span><span class="title-text">EduRetrieve</span></div>', unsafe_allow_html=True)
    st.caption("RAG-Based College digital assistant")
    
    st.markdown("---")
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload college PDF documents (e.g. Academic Policy, handbook)",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Process uploaded files
    if uploaded_files:
        new_uploads = []
        for uploaded_file in uploaded_files:
            file_path = config.UPLOAD_DIR / uploaded_file.name
            file_path = make_unique_upload_path(file_path)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            new_uploads.append(file_path)
        
        if new_uploads:
            with st.spinner("Processing & Ingesting documents into vector database..."):
                total_chunks = 0
                for path in new_uploads:
                    chunks = document_processor.process_pdf(path)
                    total_chunks += chunks
                st.success(f"Successfully processed {len(new_uploads)} document(s) ({total_chunks} chunks added)!")
                document_topics = document_processor.load_all_document_topics()
                # Refresh document list
                active_docs = get_existing_documents()
                st.rerun()

    # Database Status and Actions
    st.markdown("---")
    st.subheader("📚 Loaded Documents")
    
    if active_docs:
        for idx, doc_name in enumerate(active_docs):
            topics = document_topics.get(doc_name, [])
            topic_lines = "<br>".join(topics[:5]) if topics else "No extracted topics available."
            st.markdown(f"""
            <div class="document-card">
                <div>
                    <strong>📄 {doc_name}</strong><br>
                    <small style='color:#cbd5e1;'>{topic_lines}</small>
                </div>
                <div style="font-size: 0.8rem; color: #10b981;">● Active</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Database & Files", use_container_width=True, type="secondary"):
            document_processor.clear_vector_store()
            st.success("Vector database and uploaded files cleared!")
            st.rerun()
    else:
        st.info("No documents uploaded yet. Please upload policy documents to begin.")

    # Practical Guide / Tips
    st.markdown("""
    <div class="tips-container">
        <strong>💡 Suggested Questions:</strong>
        <ul style="padding-left: 20px; margin-top: 5px;">
            <li>What is the attendance policy?</li>
            <li>How many internal exams are conducted?</li>
            <li>What is the fee refund policy?</li>
            <li>What are the library timings?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN UI -----------------
# Header
st.markdown("## 💬 College Information Assistant")
st.markdown("Ask any questions about attendance rules, exam policies, hostel guides, or refund schemes.")

# Welcome Banner if Chat is Empty
if len(st.session_state['messages']) == 0:
    st.markdown(f"""
    <div class="welcome-banner">
        <h3>Welcome to EduRetrieve!</h3>
        <p>I am a secure digital assistant trained to answer questions using only the official documents uploaded by your college.</p>
        <p style="font-size: 0.9rem; color: #9ca3af;">Currently indexing: <strong>{len(active_docs)} document(s)</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Display Chat History
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If assistant message contains sources, show them
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
            for src in message["sources"]:
                st.markdown(f'<span class="source-badge">📖 {src["source_name"]} - Page {src["page_number"]}</span>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# User Chat Input
user_query = st.chat_input("Ask a question about the college policies...")

if user_query:
    # 1. Add User message to chat history
    st.session_state['messages'].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # 2. Query RAG Engine with Spinner
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Searching documents & generating answer..."):
            # Pass conversation history (excluding the current query)
            result = rag_engine.query_rag(
                question=user_query,
                chat_history=st.session_state['messages'][:-1]
            )
            
            answer = result["answer"]
            sources = result["sources"]
            
            # Display answer
            response_placeholder.markdown(answer)
            
            if sources:
                st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
                for src in sources:
                    st.markdown(f'<span class="source-badge">📖 {src["source_name"]} - Page {src["page_number"]}</span>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
        # 3. Add Assistant answer to chat history
        st.session_state['messages'].append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
