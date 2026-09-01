from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Local sentence-transformer embedding model.

    The model runs locally, so document embeddings do not need
    to be sent to an external embedding API.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Convert text into dense embedding vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def encode_query(self, text: str) -> List[float]:
        """
        Generate an embedding for a user query.
        """

        return self.encode([text])[0]

    @property
    def dimension(self) -> int:
        """
        Return the embedding vector dimension.
        """

        return self.model.get_sentence_embedding_dimension()
