import os
from orchestrator.vector_search import get_vector_matches
from utils.doc_parser import parse_file  # ✅ Add this import

SUPPORTED_EXTENSIONS = (".txt", ".pdf", ".docx", ".md")


def folder_keyword_search(query: str, doc_folder: str = "data", max_results: int = 2):
    if not os.path.isdir(doc_folder):
        return "❗ No documentation available. Please upload or check agent configuration."

    query_words = set(query.lower().split())
    scores = []

    for filename in os.listdir(doc_folder):
        if not filename.endswith(SUPPORTED_EXTENSIONS):
            continue

        full_path = os.path.join(doc_folder, filename)
        content = parse_file(full_path)  # ✅ Handles all file types
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        for para in paragraphs:
            para_words = set(para.lower().split())
            match_score = len(query_words & para_words)
            if match_score > 0:
                scores.append((match_score, para))

    if not scores:
        return "❗ No documentation available. Please upload or check agent configuration."

    top_snippets = [para for _, para in sorted(scores, reverse=True)[:max_results]]
    return "\n\n".join(top_snippets)


def keyword_search(query: str, docs: list[str], max_results: int = 2) -> str:
    matches = [d for d in docs if query.lower() in d.lower()]
    return "\n\n".join(matches[:max_results]) if matches else \
        "❗ No documentation available. Please upload or check agent configuration."


def get_relevant_snippets(
    query: str,
    use_vector: bool = False,
    collection=None,
    doc_folder: str = "data",
    max_results: int = 3
):
    if use_vector and collection:
        try:
            results = get_vector_matches(query, collection, max_results)
            if results:
                return "\n\n".join(results)
        except Exception as e:
            print(f"[WARNING] Vector search failed: {e}")

    return folder_keyword_search(query, doc_folder, max_results)