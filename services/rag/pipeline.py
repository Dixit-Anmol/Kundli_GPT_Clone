from services.rag.loader import JSONDocumentLoader, PDFDocumentLoader
from services.rag.chunker import CharacterChunker
from services.rag.chroma_store import ChromaStore
from services.rag.retriever import Retriever
from services.rag.query_engine import QueryEngine

class RAGPipeline:
    """Generic modular RAG pipeline orchestrating document loading, splitting, indexing, and retrieval for a specific collection."""
    
    def __init__(self, collection_name: str, data_file_path: str):
        self.collection_name = collection_name
        self.data_file_path = data_file_path
        
        self.store = ChromaStore(collection_name=self.collection_name)
        self.retriever = Retriever(self.store)
        self.query_engine = QueryEngine()
        
        # Automatically load and seed the vector store for this collection
        self._seed_database()
        
    def _seed_database(self):
        """Load and index documents from the target file (JSON or PDF) if database is empty."""
        # Avoid re-embedding on every startup if already populated
        try:
            if self.store.count() > 0:
                print(f"Collection '{self.collection_name}' already seeded. Skipping document extraction.")
                return
        except Exception as e:
            print(f"Failed to check collection count: {e}. Attempting seeding.")
            
        if self.data_file_path.lower().endswith('.pdf'):
            loader = PDFDocumentLoader(self.data_file_path)
        else:
            loader = JSONDocumentLoader(self.data_file_path)
            
        raw_docs = loader.load_documents()
        
        # Chunk using the sliding character chunker
        docs, metas = CharacterChunker.chunk_documents(raw_docs, chunk_size=500, overlap=50)
        
        # Generate unique IDs based on the collection name and index
        ids = [f"{self.collection_name}_chunk_{idx}" for idx in range(len(docs))]
        
        # Seed the document store
        self.store.add_documents(docs, metadatas=metas, ids=ids)
        
    def search_wisdom(self, query: str, top_k: int = 2) -> list:
        """Query the vector database and retrieve the most semantically relevant text chunks."""
        clean_query = self.query_engine.preprocess_query(query)
        return self.retriever.retrieve(clean_query, top_k=top_k)
