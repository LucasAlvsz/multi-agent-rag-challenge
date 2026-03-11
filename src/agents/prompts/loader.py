"""Carrega prompts de arquivos YAML como ChatPromptTemplate."""

from pathlib import Path

import yaml
from langchain_core.prompts import ChatPromptTemplate

_PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> ChatPromptTemplate:
    """Carrega um prompt YAML pelo nome (sem extensão) e retorna ChatPromptTemplate."""
    path = _PROMPTS_DIR / f"{name}.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)

    messages = [(msg["role"], msg["content"]) for msg in data["messages"]]
    return ChatPromptTemplate.from_messages(messages)
