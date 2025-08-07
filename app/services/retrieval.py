# app/services/retrieval.py
from typing import List, Optional
from ..utils.logging import get_logger
from ..config.settings import settings
import pinecone

logger = get_logger(__name__)

class PineconeRetrieval:
    def __init__(self):
        # Initialize Pinecone client and index
        pinecone.init(api_key=settings.pinecone_api_key.get_secret_value(), environment=settings.pinecone_env)
        self.index = pinecone.Index(settings.pinecone_index_name)

    async def upsert_vectors(self, ids: List[str], vectors: List[List[float]], metadata: Optional[List[dict]] = None):
        """
        Upsert vector embeddings with optional metadata into Pinecone index.
        """
        try:
            # Pinecone upsert accepts list of (id, vector, metadata)
            to_upsert = []
            for i, vec in enumerate(vectors):
                md = metadata[i] if metadata and i < len(metadata) else None
                to_upsert.append((ids[i], vec, md))
            self.index.upsert(vectors=to_upsert)
            logger.info(f"Upserted {len(vectors)} vectors into Pinecone.")
        except Exception as e:
            logger.error(f"Pinecone upsert failed: {e}")

    async def query(self, query_embedding: List[float], top_k: int = 5) -> List[dict]:
        """
        Query Pinecone index for top_k most semantically similar vectors.
        Returns list of matched entries with metadata.
        """
        try:
            result = self.index.query(queries=[query_embedding], top_k=top_k, include_metadata=True)
            matches = result['results'][0]['matches']
            logger.info(f"Retrieved {len(matches)} matches from Pinecone.")
            return matches
        except Exception as e:
            logger.error(f"Pinecone query failed: {e}")
            return []

    def close(self):
        # Gracefully shut down Pinecone client if needed
        self.index.close()
        logger.info("Closed Pinecone index connection.")
