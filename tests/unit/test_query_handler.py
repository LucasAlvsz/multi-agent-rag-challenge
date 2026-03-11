"""Testes unitários para src/services/query_service.py."""

from unittest.mock import MagicMock

from src.services.query_service import handle_ask


class TestHandleAsk:
    """Testes para handle_ask."""

    def test_returns_answer_and_sources(self):
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {
            "answer": "Resposta teste",
            "classification": "rh",
            "sources": [{"document": "doc1", "metadata": {}}],
        }

        result = handle_ask("Pergunta?", mock_graph)

        assert result["answer"] == "Resposta teste"
        assert result["classification"] == "rh"
        assert len(result["sources"]) == 1

    def test_handles_missing_answer(self):
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {}

        result = handle_ask("Pergunta?", mock_graph)

        assert result["answer"] == ""
        assert result["classification"] == "unknown"
        assert result["sources"] == []

    def test_passes_question_to_graph(self):
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {"answer": "ok", "sources": []}

        handle_ask("Qual a política de férias?", mock_graph)

        mock_graph.invoke.assert_called_once_with(
            {"question": "Qual a política de férias?"}
        )
