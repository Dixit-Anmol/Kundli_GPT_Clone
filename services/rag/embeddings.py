import math

class Embedder:
    """Lightweight text embedder utilizing TF-IDF keyword vectorization fallback for maximum stability."""
    
    def __init__(self):
        # List of prominent spiritual & astrological keywords to build our vector space
        self.vocabulary = [
            "karma", "dharma", "gita", "krishna", "arjuna", "yoga", "astrology", "horoscope",
            "planet", "star", "nakshatra", "house", "dasha", "transit", "remedy", "mantra",
            "gemstone", "saturn", "jupiter", "sun", "moon", "mars", "mercury", "venus",
            "ascendant", "lagna", "rashi", "manglik", "sade sati", "wisdom", "soul", "duty",
            "action", "attachment", "devotion", "peace", "mind", "control", "meditation"
        ]
        self.vocab_size = len(self.vocabulary)
        
    def get_embedding(self, text: str) -> list:
        """Generate a normalized feature vector for text using vocabulary term frequency."""
        text_lower = text.lower()
        vector = [0.0] * self.vocab_size
        
        # Word counts
        for i, word in enumerate(self.vocabulary):
            vector[i] = float(text_lower.count(word))
            
        # Add slight noise for diversity
        for i in range(self.vocab_size):
            vector[i] += 0.01 * (len(text_lower) % (i + 3))
            
        # Normalize vector
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0.0:
            vector = [v / magnitude for v in vector]
            
        return vector

def cosine_similarity(v1: list, v2: list) -> float:
    """Calculate the cosine similarity between two numeric lists."""
    if len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
    return dot_product / (mag1 * mag2)
