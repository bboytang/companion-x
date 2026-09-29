import hashlib
import math
import re

class EmbeddingProvider:
    """Provider boundary for memory embeddings."""
    dimensions = 1536

    def embed(self, text: str) -> list[float]:
        tokens = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
        vector = [0.0] * self.dimensions
        if not tokens:
            return vector
        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0 if digest[4] & 1 else -1.0
        norm = math.sqrt(sum(x * x for x in vector))
        return [x / norm for x in vector] if norm else vector
