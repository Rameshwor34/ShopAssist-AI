from pathlib import Path
from typing import List, Dict


DOCUMENTS_DIR = Path("data/documents")


def load_documents(directory: Path = DOCUMENTS_DIR) -> List[Dict[str, str]]:
    """
    Load supported text documents from the document directory.

    Returns:
        A list of dictionaries containing document text and metadata.
    """

    documents = []

    directory.mkdir(parents=True, exist_ok=True)

    supported_extensions = {".txt", ".md"}

    for file_path in sorted(directory.iterdir()):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        try:
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).strip()
        except OSError as exc:
            print(f"Could not read {file_path}: {exc}")
            continue

        if not text:
            continue

        documents.append(
            {
                "text": text,
                "source": str(file_path),
                "filename": file_path.name,
            }
        )

    return documents


def chunk_text(
    text: str,
    chunk_size: int = 700,
    chunk_overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping word-based chunks.

    Args:
        text: Input document text.
        chunk_size: Maximum approximate number of words per chunk.
        chunk_overlap: Number of overlapping words between chunks.

    Returns:
        List of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0
    step = chunk_size - chunk_overlap

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start += step

    return chunks


def build_chunks(
    directory: Path = DOCUMENTS_DIR,
    chunk_size: int = 700,
    chunk_overlap: int = 100,
) -> List[Dict[str, str]]:
    """
    Load all documents and convert them into retrieval chunks.
    """

    documents = load_documents(directory)

    chunks = []

    for document in documents:
        document_chunks = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for index, chunk in enumerate(document_chunks):
            chunks.append(
                {
                    "id": f'{document["filename"]}:{index}',
                    "text": chunk,
                    "source": document["source"],
                    "filename": document["filename"],
                    "chunk_index": str(index),
                }
            )

    return chunks


if __name__ == "__main__":
    chunks = build_chunks()

    print(f"Documents loaded: {len(load_documents())}")
    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks[:3]:
        print(
            f'\n[{chunk["id"]}]\n'
            f'{chunk["text"][:300]}...'
        )
