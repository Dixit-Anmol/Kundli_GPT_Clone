import os
import json

# Pre-packaged key verses from Bhagavad Gita for immediate seeding if files are missing
FALLBACK_VERSES = [
    {
        "chapter": 16,
        "verse": 21,
        "text": "trividham narakasyedam dvaaram naashanam aatmanah kaamah krodhas tathaa lobhas tasmaad etat trayam tyajet",
        "translation": "There are three gates leading to this hell, destructive of the soul—Lust, Anger, and Greed. Therefore, one must abandon these three.",
        "significance": "The three gateway keys to hell: Lust (Kama), Anger (Krodha), and Greed (Lobha)."
    },
    {
        "chapter": 16,
        "verse": 22,
        "text": "etaih vimuktah kaunteya tamo-dvaaraih tribhih narah aacharati aatmanah shreyas tato yaanti paraam gatim",
        "translation": "A person who is liberated from these three gates to darkness, O son of Kunti, strives for the welfare of the soul and thereby attains the supreme goal.",
        "significance": "Turning towards the light and beginning self-improvement (Sadhana)."
    }
]

class JSONDocumentLoader:
    """Generic JSON document loader for indexing different collections/books in RAG pipelines."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load_documents(self) -> list:
        """Load documents from JSON array of objects, with a structured fallback if file is missing."""
        if not self.file_path:
            return FALLBACK_VERSES
            
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading JSON documents from {self.file_path}: {e}")
                
        # If absolute path not found, try relative to project root
        proj_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', self.file_path))
        if os.path.exists(proj_root_path):
            try:
                with open(proj_root_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading JSON documents from relative path: {e}")
                
        return FALLBACK_VERSES

class PDFDocumentLoader:
    """PDF document loader extracting text page-by-page using pypdf."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load_documents(self) -> list:
        """Extract text from each page of the PDF and return a list of page dicts."""
        documents = []
        target_path = self.file_path
        
        if not os.path.exists(target_path):
            # Try relative path
            alt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', self.file_path))
            if os.path.exists(alt_path):
                target_path = alt_path
            else:
                print(f"PDF file not found at {self.file_path} or relative {alt_path}")
                return []
                
        try:
            from pypdf import PdfReader
            reader = PdfReader(target_path)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    documents.append({
                        "content": text.strip(),
                        "metadata": {
                            "source": os.path.basename(target_path),
                            "page": idx + 1
                        }
                    })
        except Exception as e:
            print(f"Error loading PDF from {target_path}: {e}")
            
        return documents

