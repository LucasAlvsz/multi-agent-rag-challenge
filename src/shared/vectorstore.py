"""Factory para cliente ChromaDB."""

import chromadb

from src.core.dependencies import get_settings


def get_chroma_client() -> chromadb.HttpClient:
    """Retorna cliente HTTP do Chroma."""
    settings = get_settings()
    return chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
