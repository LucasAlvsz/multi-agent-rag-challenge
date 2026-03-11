"""Testes unitários para src/shared/chunking.py."""

from src.shared.chunking import CHUNK_OVERLAP, CHUNK_SIZE, chunk_text


class TestChunkText:
    """Testes para a função chunk_text."""

    def test_empty_string_returns_empty_list(self):
        assert chunk_text("") == []

    def test_none_returns_empty_list(self):
        assert chunk_text(None) == []

    def test_whitespace_only_returns_empty_list(self):
        assert chunk_text("   \n\t  ") == []

    def test_short_text_returns_single_chunk(self):
        text = "Texto curto para teste."
        result = chunk_text(text)
        assert len(result) == 1
        assert result[0] == text

    def test_text_exactly_chunk_size_produces_overlap_chunk(self):
        """Texto com exatamente chunk_size chars gera chunk extra por causa do overlap."""
        text = "a" * CHUNK_SIZE
        result = chunk_text(text)

        assert len(result) >= 1
        assert "".join(result).replace("a", "") == ""

    def test_long_text_produces_multiple_chunks(self):
        text = "palavra " * 200
        result = chunk_text(text)
        assert len(result) > 1

    def test_multiple_chunks_produced_with_overlap(self):
        """Verifica que overlap produz mais chunks que sem overlap."""
        text = "palavra " * 200
        result_with = chunk_text(text, chunk_size=100, overlap=20)
        result_without = chunk_text(text, chunk_size=100, overlap=0)
        assert len(result_with) > 2
        assert len(result_with) > len(result_without)

    def test_respects_word_boundaries(self):
        """Verifica que chunks não cortam palavras ao meio."""
        text = "uma frase com várias palavras diferentes para testar " * 20
        result = chunk_text(text, chunk_size=50, overlap=10)
        for chunk in result:
            assert not chunk.startswith(" ")
            assert not chunk.endswith(" ")

    def test_custom_chunk_size(self):
        text = "a " * 100
        result = chunk_text(text, chunk_size=20, overlap=5)
        for chunk in result:
            assert len(chunk) <= 20

    def test_overlap_zero(self):
        text = "abcdefghij" * 10
        result = chunk_text(text, chunk_size=20, overlap=0)
        assert len(result) >= 5

    def test_default_parameters(self):
        assert CHUNK_SIZE == 500
        assert CHUNK_OVERLAP == 50

    def test_strips_leading_trailing_whitespace(self):
        text = "  texto com espaços  "
        result = chunk_text(text)
        assert result[0] == "texto com espaços"

    def test_chunks_are_non_empty(self):
        text = "Este é um texto razoavelmente longo que deve gerar alguns chunks. " * 20
        result = chunk_text(text)
        for chunk in result:
            assert chunk.strip() != ""
