class CharacterChunker:
    """Splits large text documents into fixed-size semantic character chunks with sliding-window overlap."""
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
        """Divide a single text string into character chunks of length chunk_size with overlap."""
        if not text:
            return []
            
        chunks = []
        text_len = len(text)
        start = 0
        
        # Guard against small text
        if text_len <= chunk_size:
            return [text.strip()]
            
        while start < text_len:
            end = min(start + chunk_size, text_len)
            
            # If we're not at the very end, try to align the boundary with a space/word boundary
            if end < text_len:
                # Look back up to 30 characters for a space
                space_idx = text.rfind(' ', end - 30, end)
                if space_idx != -1 and space_idx > start:
                    end = space_idx
                    
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
            # Move start forward, ensuring we always progress to prevent infinite loops
            next_start = end - overlap
            if next_start <= start:
                start = end
            else:
                start = next_start
                
            # Safety checks to prevent infinite loops or redundant small end-chunks
            if start >= text_len - 10:
                break
                
        return chunks

    @staticmethod
    def chunk_documents(documents: list, chunk_size: int = 500, overlap: int = 50) -> tuple:
        """Process a list of page dicts (containing 'content' and 'metadata') and return flattened chunks with metadata."""
        chunked_docs = []
        chunked_metas = []
        
        for doc in documents:
            content = doc.get("content") or doc.get("text") or ""
            metadata = doc.get("metadata") or {}
            
            chunks = CharacterChunker.chunk_text(content, chunk_size, overlap)
            for idx, chunk in enumerate(chunks):
                # Copy original metadata and append chunk index
                meta_copy = metadata.copy()
                meta_copy["chunk_index"] = idx
                
                chunked_docs.append(chunk)
                chunked_metas.append(meta_copy)
                
        return chunked_docs, chunked_metas
