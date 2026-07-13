import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import config
import document_processor
import prompt_templates

# Initialize ChatGroq model
def get_llm():
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in the environment or .env file.")
    return ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=0.0  # Zero temperature for precise, fact-based RAG
    )

def format_history(history):
    """
    Formats the streamlit conversation history into LangChain messages.
    """
    formatted = []
    for msg in history:
        if msg["role"] == "user":
            formatted.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            formatted.append(AIMessage(content=msg["content"]))
    return formatted

def query_rag(question: str, chat_history: list = [], similarity_threshold: float = 0.35, k: int = 5) -> dict:
    """
    Retrieves context from FAISS and generates an answer using Groq ChatGroq.
    
    Args:
        question (str): User's question.
        chat_history (list): List of chat messages (dicts with "role" and "content").
        similarity_threshold (float): Minimum relevance score threshold to include a chunk.
        k (int): Number of chunks to retrieve.
        
    Returns:
        dict: Contains "answer" (str) and "sources" (list of dicts).
    """
    db = document_processor.get_vector_store()
    
    # If no documents have been uploaded/processed yet
    if db is None:
        return {
            "answer": "This information was not found in the uploaded documents. Please upload document PDFs first.",
            "sources": []
        }
    
    # 1. Similarity Search with Relevance Scores
    try:
        docs_and_scores = db.similarity_search_with_relevance_scores(question, k=k)
    except Exception as e:
        # Fallback to standard similarity search if scores aren't supported by the distance metric
        docs_and_scores = [(doc, 1.0) for doc in db.similarity_search(question, k=k)]

    # 2. Context Engineering: Filter, Rank, and Deduplicate Chems
    filtered_chunks = []
    seen_contents = set()
    sources = []
    
    for doc, score in docs_and_scores:
        # Filter out chunks below relevance threshold
        if score < similarity_threshold:
            continue
            
        # Deduplicate identical contents
        content_hash = hash(doc.page_content.strip())
        if content_hash in seen_contents:
            continue
            
        seen_contents.add(content_hash)
        filtered_chunks.append(doc)
        
        # Add metadata for citation
        source_info = {
            "source_name": doc.metadata.get("source_name", "Unknown Document"),
            "page_number": doc.metadata.get("page_number", "Unknown Page")
        }
        if source_info not in sources:
            sources.append(source_info)

    # 3. Assemble Context
    if not filtered_chunks:
        return {
            "answer": "This information was not found in the uploaded documents.",
            "sources": []
        }
        
    context_str = ""
    for i, doc in enumerate(filtered_chunks):
        context_str += f"[Doc {i+1} - Source: {doc.metadata.get('source_name')} - Page: {doc.metadata.get('page_number')}]\n"
        context_str += f"{doc.page_content}\n\n"
        
    # 4. Invoke LLM with Prompts and Conversation History
    try:
        llm = get_llm()
        formatted_msgs = format_history(chat_history)
        
        # Format the RAG prompt template
        prompt_val = prompt_templates.RAG_PROMPT.format_messages(
            context=context_str,
            history=formatted_msgs,
            question=question
        )
        
        response = llm.invoke(prompt_val)
        answer = response.content.strip()
        
        # Safety Check: If LLM claims information is not found despite formatting
        if "not found in the uploaded documents" in answer.lower():
            # Standardize output
            return {
                "answer": "This information was not found in the uploaded documents.",
                "sources": []
            }
            
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        return {
            "answer": f"Error communicating with LLM: {str(e)}",
            "sources": []
        }
