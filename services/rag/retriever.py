class Retriever:
    """Retriever wrapper querying the vector store for semantic matches."""
    
    def __init__(self, store):
        self.store = store
        
    def retrieve(self, query: str, top_k: int = 3) -> list:
        """Retrieve relevant text documents from the store."""
        results = self.store.query(query, top_k=top_k)
        return [r["text"] for r in results]
