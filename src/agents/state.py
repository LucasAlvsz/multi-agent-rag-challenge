"""Estado compartilhado do grafo LangGraph."""

from typing import TypedDict, Literal


class AgentState(TypedDict):
    """Estado que flui entre os nós do grafo.

    Cada nó lê o que precisa e escreve apenas os campos que produz.
    O LangGraph faz merge automático do retorno parcial no estado corrente.
    """

    question: str
    classification: Literal["rh", "tecnico", "both"]
    context: str
    sources: list[dict]
    answer: str
