# app/db/pinecone.py

import pinecone
from ..config.settings import settings

def init_pinecone():
    pinecone.init(
        api_key=settings.pinecone_api_key.get_secret_value(),
        environment=settings.pinecone_env
    )
    index = pinecone.Index(settings.pinecone_index_name)
    return index
