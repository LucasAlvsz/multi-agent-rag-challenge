"""Testes unitários para src/agents/prompts/loader.py."""

import pytest
from langchain_core.prompts import ChatPromptTemplate

from src.agents.prompts.loader import load_prompt


class TestLoadPrompt:
    """Testes para load_prompt."""

    def test_load_answer_prompt(self):
        prompt = load_prompt("answer")
        assert isinstance(prompt, ChatPromptTemplate)

    def test_load_classification_prompt(self):
        prompt = load_prompt("classification")
        assert isinstance(prompt, ChatPromptTemplate)

    def test_answer_prompt_has_two_messages(self):
        prompt = load_prompt("answer")
        assert len(prompt.messages) == 2

    def test_classification_prompt_has_two_messages(self):
        prompt = load_prompt("classification")
        assert len(prompt.messages) == 2

    def test_answer_prompt_has_expected_variables(self):
        prompt = load_prompt("answer")
        assert "context" in prompt.input_variables
        assert "question" in prompt.input_variables

    def test_classification_prompt_has_expected_variables(self):
        prompt = load_prompt("classification")
        assert "question" in prompt.input_variables

    def test_load_nonexistent_raises(self):
        with pytest.raises(FileNotFoundError):
            load_prompt("nonexistent_prompt")
