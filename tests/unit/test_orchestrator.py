"""Testes unitários para src/agents/orchestrator.py."""

from unittest.mock import MagicMock, patch

from src.agents.orchestrator import ClassificationResult, classify_question


class TestClassifyQuestion:
    """Testes para classify_question."""

    def _make_mock_llm(self, classification_value):
        """Cria um mock LLM que retorna ClassificationResult via with_structured_output.

        LangChain wraps non-Runnable callables in RunnableLambda,
        so it calls mock_structured_llm(input) rather than .invoke(input).
        """
        mock_llm = MagicMock()
        result = ClassificationResult(classification=classification_value)
        mock_structured = MagicMock(return_value=result)
        mock_llm.with_structured_output.return_value = mock_structured
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
    def test_structured_output_called_with_schema(self, mock_get_llm):
        mock_llm = self._make_mock_llm("rh")
        mock_get_llm.return_value = mock_llm

        state = {"question": "Qualquer pergunta"}
        classify_question(state)

        mock_llm.with_structured_output.assert_called_once_with(ClassificationResult)

    @patch("src.agents.orchestrator.get_llm")
    def test_exception_defaults_to_both(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_structured = MagicMock(side_effect=Exception("LLM error"))
        mock_llm.with_structured_output.return_value = mock_structured
        mock_get_llm.return_value = mock_llm

        state = {"question": "Pergunta qualquer"}
        result = classify_question(state)

        assert result["classification"] == "both"
