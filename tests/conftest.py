"""Fixtures e configurações compartilhadas para os testes."""

import os
from unittest.mock import MagicMock

import pytest

os.environ.setdefault("LLM_PROVIDER", "openai")
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake-key-for-testing")
os.environ.setdefault("CHROMA_HOST", "localhost")
os.environ.setdefault("CHROMA_PORT", "8000")


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    """Limpa o cache do get_settings entre testes para evitar state leaking."""
    from src.core.dependencies import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def sample_text():
    """Texto de exemplo para testes de chunking e ingestão."""
    return (
        "Este é um documento de teste para o sistema RAG. "
        "Ele contém informações sobre políticas de recursos humanos. "
        "Os colaboradores devem seguir as diretrizes estabelecidas pela empresa. "
        "O horário de trabalho é das 9h às 18h, com intervalo de 1 hora para almoço. "
        "As férias são de 30 dias corridos após 12 meses de trabalho."
    )


@pytest.fixture
def sample_chunks():
    """Lista de chunks de exemplo."""
    return [
        "Este é o primeiro chunk do documento.",
        "Este é o segundo chunk do documento.",
        "Este é o terceiro chunk do documento.",
    ]


@pytest.fixture
def sample_embeddings():
    """Lista de embeddings fake para testes."""
    return [
        [0.1] * 256,
        [0.2] * 256,
        [0.3] * 256,
    ]


@pytest.fixture
def mock_chroma_collection():
    """Mock de uma coleção do ChromaDB."""
    collection = MagicMock()
    collection.count.return_value = 3
    collection.query.return_value = {
        "documents": [["chunk 1", "chunk 2"]],
        "metadatas": [[{"doc_id": "doc-1"}, {"doc_id": "doc-1"}]],
        "distances": [[0.1, 0.2]],
    }
    return collection


@pytest.fixture
def mock_chroma_client(mock_chroma_collection):
    """Mock do cliente ChromaDB."""
    client = MagicMock()
    client.get_or_create_collection.return_value = mock_chroma_collection
    return client
