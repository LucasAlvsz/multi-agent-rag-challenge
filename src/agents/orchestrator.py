"""Nó orquestrador: classifica a pergunta do usuário por domínio."""

from src.agents.prompts.loader import load_prompt
from src.agents.state import AgentState
from src.shared.model_providers import get_llm

CLASSIFICATION_PROMPT = load_prompt("classification")


def classify_question(state: AgentState) -> dict:
    """Classifica a pergunta e retorna a classificação no estado."""
    llm = get_llm()
    chain = CLASSIFICATION_PROMPT | llm
    result = chain.invoke({"question": state["question"]})

    classification = result.content.strip().lower()

    if classification not in ("rh", "tecnico", "both"):
        classification = "both"

    return {"classification": classification}
