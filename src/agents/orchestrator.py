"""Nó orquestrador: classifica a pergunta do usuário por domínio."""

from typing import Literal

from pydantic import BaseModel, Field

from src.agents.prompts.loader import load_prompt
from src.agents.state import AgentState
from src.shared.model_providers import get_llm

CLASSIFICATION_PROMPT = load_prompt("classification")


class ClassificationResult(BaseModel):
    """Schema para saída estruturada do classificador."""

    classification: Literal["rh", "tecnico", "both"] = Field(
        description="Domínio da pergunta: rh, tecnico ou both",
    )


def classify_question(state: AgentState) -> dict:
    """Classifica a pergunta e retorna a classificação no estado."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(ClassificationResult)
    chain = CLASSIFICATION_PROMPT | structured_llm

    try:
        result = chain.invoke({"question": state["question"]})
        return {"classification": result.classification}
    except Exception:
        return {"classification": "both"}
