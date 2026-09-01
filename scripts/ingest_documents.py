from backend.rag.ingestion import build_chunks
from backend.rag.embeddings import EmbeddingModel
from backend.rag.vector_store import VectorStore


def main():
    print("=" * 60)
    print("ShopAssist AI - RAG Document Ingestion")
    print("=" * 60)

    print("\n[1/3] Loading and chunking documents...")

    chunks = build_chunks(
        chunk_size=700,
        chunk_overlap=100,
    )

    print(f"Created {len(chunks)} chunks.")

    if not chunks:
        print("No documents were found.")
        return

    print("\n[2/3] Generating embeddings...")

    embedding_model = EmbeddingModel()

    print(
        f"Embedding model: "
        f"{embedding_model.model_name}"
    )

    print(
        f"Embedding dimension: "
        f"{embedding_model.dimension}"
    )

    embeddings = embedding_model.encode(
        [chunk["text"] for chunk in chunks]
    )

    print(
        f"Generated {len(embeddings)} embeddings."
    )

    print("\n[3/3] Storing vectors in ChromaDB...")

    vector_store = VectorStore()

    stored = vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    print(f"Stored {stored} chunks.")

    print(
        f"Total vectors in database: "
        f"{vector_store.count()}"
    )

    print("\nRAG ingestion completed successfully.")


if __name__ == "__main__":
    main()
