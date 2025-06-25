import os
import time
from llm.ollama_client import query_llm
from orchestrator.vector_search import init_chroma_index, get_vector_matches
from orchestrator.loader import load_agent_config, load_agent_docs
from utils.context_retriever import keyword_search

# --- Agent metadata ---
AGENT_NAME = os.path.basename(os.path.dirname(__file__))

# --- Load config and docs ---
CONFIG = load_agent_config(AGENT_NAME)
USE_VECTOR = CONFIG.get("use_vector", False)
MODEL = CONFIG.get("model", "mistral")
DOCS = load_agent_docs(AGENT_NAME)
print(f"[DEBUG] Loaded {len(DOCS)} documents for {AGENT_NAME}")

# --- Initialize vector index if enabled ---
chroma = None
if USE_VECTOR:
    chroma = init_chroma_index(AGENT_NAME)
    if chroma.count() < len(DOCS):  # Avoid re-embedding if already exists
        print(f"[Chroma] Embedding {len(DOCS)} documents for {AGENT_NAME}...")
        for i, chunk in enumerate(DOCS):
            chroma.add(documents=[chunk], ids=[f"chunk-{i}"])
    else:
        print(f"[Chroma] Found existing vector index with {chroma.count()} items.")

# --- Context Retriever ---
def get_relevant_snippets(query: str) -> str:
    if USE_VECTOR and chroma:
        try:
            return "\n\n".join(get_vector_matches(chroma, query, n_results=3))
        except Exception as e:
            print(f"[WARNING] Vector search failed, falling back. Reason: {e}")
    return keyword_search(query, DOCS, max_results=2)

# --- Main agent interface ---
def handle_task(input_text: str) -> dict:
    if not DOCS or len(DOCS) == 0:
        return {
            "agent": AGENT_NAME,
            "response": "❗ No documentation available. Please upload or check agent configuration.",
            "model": MODEL,
            "duration": 0,
            "load_time": 0,
            "inference_time": 0
        }
    
    t0 = time.time()
    context = get_relevant_snippets(input_text)
    load_time = time.time() - t0

    prompt = f"""
You are a helpful assistant. Based on the following documentation:
\"\"\"
{context}
\"\"\"
Answer the question: {input_text}
""".strip()

    t1 = time.time()
    response = query_llm(prompt, model=MODEL)
    inference_time = time.time() - t1

    return {
        "agent": AGENT_NAME,
        "response": response,
        "model": MODEL,
        "duration": round(load_time + inference_time, 2),
        "load_time": round(load_time, 2),
        "inference_time": round(inference_time, 2),
    }