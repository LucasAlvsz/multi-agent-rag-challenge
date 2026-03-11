"""Definição e compilação do grafo LangGraph."""

from langgraph.graph import END, StateGraph

from src.agents.generator import generate_answer
from src.agents.orchestrator import classify_question
from src.agents.specialists import query_both, query_rh, query_tecnico
from src.agents.state import AgentState


def _route_to_specialist(state: AgentState) -> str:
    """Decide qual nó especialista executar com base na classificação."""
    classification = state["classification"]
    if classification == "rh":
        return "specialist_rh"
    elif classification == "tecnico":
        return "specialist_tecnico"
    return "specialist_both"


def build_graph() -> StateGraph:
    """Monta e compila o grafo de agentes."""
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_question)
    graph.add_node("specialist_rh", query_rh)
    graph.add_node("specialist_tecnico", query_tecnico)
    graph.add_node("specialist_both", query_both)
    graph.add_node("generate", generate_answer)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        _route_to_specialist,
        {
            "specialist_rh": "specialist_rh",
            "specialist_tecnico": "specialist_tecnico",
            "specialist_both": "specialist_both",
        },
    )

    graph.add_edge("specialist_rh", "generate")
    graph.add_edge("specialist_tecnico", "generate")
    graph.add_edge("specialist_both", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
