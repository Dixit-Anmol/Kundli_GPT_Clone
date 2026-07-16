class QueryEngine:
    """Pre-processes search queries to extract semantic intent before retrieval."""
    
    @staticmethod
    def preprocess_query(query: str) -> str:
        # Standardize and clean query
        return query.strip().lower()
