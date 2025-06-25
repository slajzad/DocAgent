import chromadb
import os

def init_chroma_index(agent_name: str):
    """
    Initialize a persistent ChromaDB collection for a specific agent.
    Creates a local directory for the vector index if it doesn't exist.
    """
    persist_path = f"agents/{agent_name}/chroma_index"
    os.makedirs(persist_path, exist_ok=True)

    client = chromadb.PersistentClient(path=persist_path)
    collection = client.get_or_create_collection(name=agent_name)

    print(f"[Chroma] Initialized collection for agent: {agent_name}")
    return collection


def get_vector_matches(collection, query_text: str, n_results=3, min_score=0.5):
    """
    Query ChromaDB collection and return matching documents below a distance threshold.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances"]
    )
    docs = results["documents"][0]
    scores = results["distances"][0]

    print(f"[Chroma] Match scores: {scores}")

    # Filter based on distance (lower is better)
    return [doc for doc, score in zip(docs, scores) if score < min_score]