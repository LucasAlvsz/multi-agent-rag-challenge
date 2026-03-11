"""Nó gerador: produz a resposta final usando LLM com contexto recuperado."""

from src.agents.prompts.loader import load_prompt
from src.agents.state import AgentState
from src.shared.model_providers import get_llm

ANSWER_PROMPT = load_prompt("answer")


def generate_answer(state: AgentState) -> dict:
    """Gera resposta final usando LLM com o contexto recuperado."""
    if not state.get("context", "").strip():
        return {
            "answer": "Não encontrei documentos relevantes para responder à sua pergunta."
        }

    llm = get_llm()
    chain = ANSWER_PROMPT | llm
    result = chain.invoke(
        {"question": state["question"], "context": state["context"]}
    )
    return {"answer": result.content}
