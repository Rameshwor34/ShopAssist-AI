from typing import List, Dict

from backend.rag.embeddings import EmbeddingModel
from backend.rag.vector_store import VectorStore


_embedding_model = None
_vector_store = None


def _get_resources():
    global _embedding_model, _vector_store

    if _embedding_model is None:
        _embedding_model = EmbeddingModel()

    if _vector_store is None:
        _vector_store = VectorStore()

    return _embedding_model, _vector_store


def retrieve(query: str, top_k: int = 4) -> List[Dict]:
    """
    Retrieve the most relevant document chunks for a user query.

    Args:
        query: User's natural-language question.
        top_k: Maximum number of chunks to retrieve.

    Returns:
        A list of matching chunks containing text, metadata,
        source information, and similarity distance.
    """

    if not query or not query.strip():
        return []

    embedding_model, vector_store = _get_resources()

    if vector_store.count() == 0:
        return []

    query_embedding = embedding_model.encode([query])[0]

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=min(top_k, vector_store.count()),
    )

    return results


def format_context(results: List[Dict]) -> str:
    """
    Convert retrieved chunks into context suitable for an LLM prompt.
    """

    if not results:
        return "No relevant information was found in the knowledge base."

    context_parts = []

    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        source = metadata.get("filename", "unknown source")

        context_parts.append(
            f"[Source {index}: {source}]\n"
            f"{result.get('text', '').strip()}"
        )

    return "\n\n".join(context_parts)
