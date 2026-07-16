class Reranker:
    """Reranker stub returning retrieved results sorted by relevance scores."""
    
    @staticmethod
    def rerank(results: list) -> list:
        # Results are already sorted by cosine similarity in the vector store query.
        return results
