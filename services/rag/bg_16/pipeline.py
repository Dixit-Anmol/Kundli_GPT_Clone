from services.rag.pipeline import RAGPipeline

class BG16Pipeline(RAGPipeline):
    """Concrete RAG pipeline subclass bound specifically to the Bhagavad Gita Chapter 16 PDF collection."""
    
    def __init__(self):
        super().__init__(
            collection_name="gita_chapter_16",
            data_file_path="backend/data/knowledge/bhagavad_gita/BG_16_Geeta.pdf"
        )
