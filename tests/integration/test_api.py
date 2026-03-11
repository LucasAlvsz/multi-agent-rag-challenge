"""Testes de integração para os endpoints da API FastAPI."""

from unittest.mock import ANY, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Cria um TestClient para a aplicação FastAPI (com lifespan)."""
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    """Testes para GET /health."""

    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestDocumentsEndpoint:
    """Testes para POST /documents."""

    @patch("src.api.routes.documents.handle_ingest")
    def test_ingest_rh_document(self, mock_ingest, client):
        mock_ingest.return_value = {
            "doc_id": "abc-123",
            "chunks_count": 3,
            "domain": "rh",
        }

        response = client.post(
            "/documents",
            json={"content": "Documento de RH sobre férias", "domain": "rh"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["doc_id"] == "abc-123"
        assert data["chunks_count"] == 3
        assert data["domain"] == "rh"
        mock_ingest.assert_called_once_with("Documento de RH sobre férias", "rh")

    @patch("src.api.routes.documents.handle_ingest")
    def test_ingest_tecnico_document(self, mock_ingest, client):
        mock_ingest.return_value = {
            "doc_id": "def-456",
            "chunks_count": 5,
            "domain": "tecnico",
        }

        response = client.post(
            "/documents",
            json={"content": "Documentação da API REST", "domain": "tecnico"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["domain"] == "tecnico"

    def test_empty_content_returns_422(self, client):
        """Empty string is rejected by Pydantic min_length=1 validation."""
        response = client.post(
            "/documents",
            json={"content": "", "domain": "rh"},
        )
        assert response.status_code == 422

    def test_whitespace_content_returns_400(self, client):
        """Whitespace-only passes Pydantic but is caught by endpoint logic."""
        response = client.post(
            "/documents",
            json={"content": "   ", "domain": "rh"},
        )
        assert response.status_code == 400

    def test_invalid_domain_returns_422(self, client):
        response = client.post(
            "/documents",
            json={"content": "conteúdo", "domain": "invalido"},
        )
        assert response.status_code == 422

    def test_missing_content_returns_422(self, client):
        response = client.post(
            "/documents",
            json={"domain": "rh"},
        )
        assert response.status_code == 422

    def test_missing_domain_returns_422(self, client):
        response = client.post(
            "/documents",
            json={"content": "conteúdo"},
        )
        assert response.status_code == 422

    @patch("src.api.routes.documents.handle_ingest")
    def test_value_error_returns_503(self, mock_ingest, client):
        mock_ingest.side_effect = ValueError("Provider não configurado")

        response = client.post(
            "/documents",
            json={"content": "conteúdo válido", "domain": "rh"},
        )

        assert response.status_code == 503
        assert "Provider não configurado" in response.json()["detail"]


class TestAskEndpoint:
    """Testes para POST /ask."""

    @patch("src.api.routes.ask.handle_ask")
    def test_ask_returns_answer(self, mock_ask, client):
        mock_ask.return_value = {
            "answer": "A política de férias é de 30 dias.",
            "classification": "rh",
            "sources": [{"document": "doc sobre férias", "metadata": {"doc_id": "1"}}],
        }

        response = client.post(
            "/ask",
            json={"question": "Qual a política de férias?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "A política de férias é de 30 dias."
        assert len(data["sources"]) == 1

    def test_empty_question_returns_422(self, client):
        """Empty string is rejected by Pydantic min_length=1 validation."""
        response = client.post(
            "/ask",
            json={"question": ""},
        )
        assert response.status_code == 422

    def test_whitespace_question_returns_400(self, client):
        """Whitespace-only passes Pydantic but is caught by endpoint logic."""
        response = client.post(
            "/ask",
            json={"question": "   "},
        )
        assert response.status_code == 400

    def test_missing_question_returns_422(self, client):
        response = client.post(
            "/ask",
            json={},
        )
        assert response.status_code == 422

    @patch("src.api.routes.ask.handle_ask")
    def test_value_error_returns_503(self, mock_ask, client):
        mock_ask.side_effect = ValueError("LLM não disponível")

        response = client.post(
            "/ask",
            json={"question": "pergunta válida"},
        )

        assert response.status_code == 503
        assert "LLM não disponível" in response.json()["detail"]

    @patch("src.api.routes.ask.handle_ask")
    def test_ask_passes_question(self, mock_ask, client):
        mock_ask.return_value = {"answer": "ok", "classification": "rh", "sources": []}

        client.post(
            "/ask",
            json={"question": "Minha pergunta específica"},
        )

        mock_ask.assert_called_once_with("Minha pergunta específica", ANY)
