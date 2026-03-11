"""Testes unitários para src/agents/orchestrator.py."""

from unittest.mock import MagicMock, patch

from src.agents.orchestrator import classify_question


class TestClassifyQuestion:
    """Testes para classify_question."""

    def _make_mock_llm(self, content_text):
        """Cria um mock LLM que retorna content_text quando usado em chain.

        LangChain wraps non-Runnable callables in RunnableLambda,
        so it calls mock_llm(input) rather than mock_llm.invoke(input).
        """
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = content_text
        mock_llm.return_value = mock_response
        return mock_llm

    @patch("src.agents.orchestrator.get_llm")
    def test_classifies_rh(self, mock_get_llm):
        mock_get_llm.return_value = self._make_mock_llm("rh")

        state = {"question": "Qual a política de férias?"}
        result = classify_question(state)

        assert result["classification"] == "rh"

    @patch("src.agents.orchestrator.get_llm")
    def test_classifies_tecnico(self, mock_get_llm):
        mock_get_llm.return_value = self._make_mock_llm("tecnico")

        state = {"question": "Como funciona a API de autenticação?"}
        result = classify_question(state)

        assert result["classification"] == "tecnico"

    @patch("src.agents.orchestrator.get_llm")
    def test_classifies_both(self, mock_get_llm):
        mock_get_llm.return_value = self._make_mock_llm("both")

        state = {"question": "Quais APIs os colaboradores usam?"}
        result = classify_question(state)

        assert result["classification"] == "both"

    @patch("src.agents.orchestrator.get_llm")
    def test_invalid_classification_defaults_to_both(self, mock_get_llm):
        mock_get_llm.return_value = self._make_mock_llm("invalid_response")

        state = {"question": "Pergunta qualquer"}
        result = classify_question(state)

        assert result["classification"] == "both"

    @patch("src.agents.orchestrator.get_llm")
    def test_strips_and_lowercases(self, mock_get_llm):
        mock_get_llm.return_value = self._make_mock_llm("  RH  \n")

        state = {"question": "Qualquer pergunta"}
        result = classify_question(state)

        assert result["classification"] == "rh"
