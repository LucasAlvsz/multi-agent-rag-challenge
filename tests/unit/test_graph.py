"""Testes unitários para src/agents/graph.py."""

from unittest.mock import MagicMock, patch

from src.agents.graph import _route_to_specialist


class TestRouteToSpecialist:
    """Testes para _route_to_specialist."""

    def test_routes_to_rh(self):
        state = {"classification": "rh"}
        assert _route_to_specialist(state) == "specialist_rh"

    def test_routes_to_tecnico(self):
        state = {"classification": "tecnico"}
        assert _route_to_specialist(state) == "specialist_tecnico"

    def test_routes_to_both(self):
        state = {"classification": "both"}
        assert _route_to_specialist(state) == "specialist_both"

    def test_unknown_routes_to_both(self):
        state = {"classification": "unknown"}
        assert _route_to_specialist(state) == "specialist_both"


class TestGenerateAnswer:
    """Testes para generate_answer (em agents/generator.py)."""

    def test_empty_context_returns_default(self):
        from src.agents.generator import generate_answer

        state = {"question": "qualquer", "context": "", "sources": []}
        result = generate_answer(state)
        assert "Não encontrei" in result["answer"]

    def test_whitespace_context_returns_default(self):
        from src.agents.generator import generate_answer

        state = {"question": "qualquer", "context": "   \n  ", "sources": []}
        result = generate_answer(state)
        assert "Não encontrei" in result["answer"]

    def test_no_context_key_returns_default(self):
        from src.agents.generator import generate_answer

        state = {"question": "qualquer", "sources": []}
        result = generate_answer(state)
        assert "Não encontrei" in result["answer"]

    @patch("src.agents.generator.get_llm")
    def test_generates_answer_with_context(self, mock_get_llm):
        from src.agents.generator import generate_answer

        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Resposta gerada pelo LLM."
        mock_llm.return_value = mock_response
        mock_get_llm.return_value = mock_llm

        state = {
            "question": "Qual a política?",
            "context": "A política é XYZ.",
            "sources": [],
        }
        result = generate_answer(state)

        assert result["answer"] == "Resposta gerada pelo LLM."


class TestBuildGraph:
    """Testes para build_graph."""

    def test_graph_compiles(self):
        from src.agents.graph import build_graph

        graph = build_graph()
        assert graph is not None

    def test_graph_has_expected_nodes(self):
        from src.agents.graph import build_graph

        graph = build_graph()
        node_names = set(graph.nodes.keys())
        expected = {
            "classify",
            "specialist_rh",
            "specialist_tecnico",
            "specialist_both",
            "generate",
            "__start__",
        }
        assert expected.issubset(node_names)
