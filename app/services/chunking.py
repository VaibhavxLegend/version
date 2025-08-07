# app/services/chunking.py
from typing import List
from ..utils.logging import get_logger

logger = get_logger(__name__)

class OllamaChunker:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        # Initialize Ollama client or connection here if needed

    async def semantic_chunk(self, text: str) -> List[str]:
        """
        Use Ollama or similar semantic chunking to split document markdown text
        into semantically coherent overlapping chunks.
        
        For now, a simple heuristic chunker splitting by length.
        """
        tokens = text.split()  # simple token split by whitespace
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = " ".join(chunk_tokens)
            chunks.append(chunk_text)
            start += int(self.chunk_size * 0.75)  # 25% overlap
        logger.info(f"Created {len(chunks)} chunks from document text.")
        return chunks
