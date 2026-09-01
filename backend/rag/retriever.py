from typing import Dict, List

from backend.rag.embeddings import EmbeddingModel
from backend.rag.vector_store import VectorStore


class Retriever:
    """
    Semantic retriever for the ShopAssist knowledge base.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel | None = None,
        vector_store: VectorStore | None = None,
    ):
        self.embedding_model = (
            embedding_model
            if embedding_model is not None
            else EmbeddingModel()
        )

        self.vector_store = (
            vector_store
            if vector_store is not None
            else VectorStore()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
    ) -> List[Dict]:
        """
        Retrieve the most relevant document chunks.
        """

        if not query.strip():
            return []

        query_embedding = self.embedding_model.encode_query(
            query
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

    def build_context(
        self,
        query: str,
        top_k: int = 4,
    ) -> tuple[str, List[str]]:
        """
        Retrieve relevant chunks and construct an LLM context.

        Returns:
            context string and source filenames.
        """

        results = self.retrieve(
            query=query,
            top_k=top_k,
        )

        if not results:
            return "", []

        context_parts = []
        sources = []

        for index, result in enumerate(results, start=1):
            metadata = result.get("metadata") or {}

            filename = metadata.get(
                "filename",
                "unknown",
            )

            sources.append(filename)

            context_parts.append(
                f"[Source {index}: {filename}]\n"
                f"{result['text']}"
            )

        unique_sources = list(dict.fromkeys(sources))

        return (
            "\n\n".join(context_parts),
            unique_sources,
        )
