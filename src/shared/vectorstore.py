"""Factory para cliente ChromaDB (singleton)."""

from functools import lru_cache

import chromadb

from src.core.dependencies import get_settings


@lru_cache
def get_chroma_client() -> chromadb.HttpClient:
    """Retorna cliente HTTP do Chroma (cacheado como singleton)."""
    settings = get_settings()
    return chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
