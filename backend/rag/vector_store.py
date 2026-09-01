from pathlib import Path
from typing import Dict, List

import chromadb


VECTOR_DB_DIR = Path("models/chroma_db")
COLLECTION_NAME = "shopassist_documents"


class VectorStore:
    """
    Persistent ChromaDB vector store for ShopAssist RAG.
    """

    def __init__(
        self,
        persist_directory: Path = VECTOR_DB_DIR,
        collection_name: str = COLLECTION_NAME,
    ):
        persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "ShopAssist AI knowledge base"
            },
        )

    def add_chunks(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
    ) -> int:
        """
        Add document chunks and their embeddings to ChromaDB.
        """

        if not chunks:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match"
            )

        ids = [chunk["id"] for chunk in chunks]

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "source": chunk["source"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(chunks)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 4,
    ) -> List[Dict]:
        """
        Perform semantic similarity search.
        """

        if not query_embedding:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        matches = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for index, document in enumerate(documents):
            matches.append(
                {
                    "id": ids[index],
                    "text": document,
                    "metadata": metadatas[index],
                    "distance": distances[index],
                }
            )

        return matches

    def count(self) -> int:
        """
        Return number of stored chunks.
        """

        return self.collection.count()

    def clear(self) -> None:
        """
        Remove all vectors from the collection.
        """

        self.client.delete_collection(
            self.collection.name
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={
                "description": "ShopAssist AI knowledge base"
            },
        )
