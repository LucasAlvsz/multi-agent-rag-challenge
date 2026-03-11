"""Serviço de consulta: invoca o grafo LangGraph."""


def handle_ask(question: str, graph) -> dict:
    """
    Responde à pergunta usando o grafo de agentes:
    classify → specialist (rh/tecnico/both) → generate.

    Args:
        question: Pergunta do usuário.
        graph: Grafo LangGraph compilado (injetado via Depends).

    Returns:
        Dict com answer, classification e sources.
    """
    result = graph.invoke({"question": question})

    return {
        "answer": result.get("answer", ""),
        "classification": result.get("classification", "unknown"),
        "sources": result.get("sources", []),
    }
