import os
import chromadb
from services.rag.embeddings import Embedder

class ChromaStore:
    """Persistent Vector Store implementing standard CRUD interfaces wrapping the official ChromaDB client."""
    
    def __init__(self, collection_name: str = "gita_ch16", db_path: str = "backend/chroma_db"):
        self.collection_name = collection_name
        # Keep path absolute to prevent directory resolution conflicts
        self.db_path = os.path.abspath(db_path)
        self.embedder = Embedder()
        
        # Ensure base directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize Persistent Client (saves vectors and sqlite metadata to disk)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        
    def add_documents(self, documents: list, metadatas: list = None, ids: list = None):
        """Insert/update text chunks along with metadata and custom pre-computed embeddings into the database."""
        if not ids:
            ids = [f"doc_{idx}" for idx in range(len(documents))]
        if not metadatas:
            metadatas = [{} for _ in documents]
            
        # Calculate embeddings using our custom Embedder
        embeddings = [self.embedder.get_embedding(doc) for doc in documents]
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
    def query(self, query_text: str, top_k: int = 3) -> list:
        """Query ChromaDB for top_k most similar text chunks using cosine-similarity distance."""
        query_vector = self.embedder.get_embedding(query_text)
        
        # Perform query using pre-computed vector to avoid heavy local torch dependencies
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )
        
        # Parse query output lists
        formatted = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else [{} for _ in docs]
            ids = results["ids"][0] if "ids" in results and results["ids"] else [f"doc_{i}" for i in range(len(docs))]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0 for _ in docs]
            
            for i in range(len(docs)):
                formatted.append({
                    "id": ids[i],
                    "text": docs[i],
                    "metadata": metas[i],
                    "score": 1.0 - distances[i]  # Convert distance to similarity score
                })
                
        return formatted
        
    def delete(self, ids: list):
        """Remove documents by ID list from the collection."""
        self.collection.delete(ids=ids)
        
    def reset(self):
        """Reset the vector database collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def count(self) -> int:
        """Return total number of documents in the collection."""
        return self.collection.count()
