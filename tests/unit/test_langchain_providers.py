"""Testes unitários para src/shared/model_providers.py e src/shared/vectorstore.py."""

from unittest.mock import MagicMock, patch


class TestGetLlm:
    """Testes para get_llm."""

    @patch("src.shared.model_providers.get_settings")
    def test_openai_returns_chat_model(self, mock_settings):
        mock_settings.return_value = MagicMock(
            llm_provider="openai",
            openai_llm_model="gpt-4o-mini",
            openai_api_key="sk-test",
        )
        from src.shared.model_providers import get_llm

        result = get_llm()
        assert result is not None

    @patch("src.shared.model_providers.get_settings")
    def test_gemini_fallback_for_unknown_provider(self, mock_settings):
        mock_settings.return_value = MagicMock(
            llm_provider="invalid",
            gemini_llm_model="gemini-pro",
            google_api_key="fake-key",
        )
        from src.shared.model_providers import get_llm

        result = get_llm()
        assert result is not None


class TestGetEmbeddings:
    """Testes para get_embeddings."""

    @patch("src.shared.model_providers.get_settings")
    def test_openai_returns_embeddings(self, mock_settings):
        mock_settings.return_value = MagicMock(
            llm_provider="openai",
            openai_embed_model="text-embedding-3-small",
            openai_api_key="sk-test",
        )
        from langchain_core.embeddings import Embeddings
        from src.shared.model_providers import get_embeddings

        result = get_embeddings()
        assert isinstance(result, Embeddings)

    @patch("src.shared.model_providers.get_settings")
    def test_gemini_fallback_for_unknown_provider(self, mock_settings):
        mock_settings.return_value = MagicMock(
            llm_provider="invalid",
            gemini_embed_model="models/embedding-001",
            google_api_key="fake-key",
        )
        from langchain_core.embeddings import Embeddings
        from src.shared.model_providers import get_embeddings

        result = get_embeddings()
        assert isinstance(result, Embeddings)


class TestGetChromaClient:
    """Testes para get_chroma_client."""

    @patch("src.shared.vectorstore.chromadb.HttpClient")
    @patch("src.shared.vectorstore.get_settings")
    def test_creates_client_with_settings(self, mock_settings, mock_http_client):
        mock_settings.return_value = MagicMock(
            chroma_host="testhost", chroma_port=9999
        )
        from src.shared.vectorstore import get_chroma_client

        get_chroma_client()
        mock_http_client.assert_called_once_with(host="testhost", port=9999)

    @patch("src.shared.vectorstore.chromadb.HttpClient")
    @patch("src.shared.vectorstore.get_settings")
    def test_default_host_and_port(self, mock_settings, mock_http_client):
        mock_settings.return_value = MagicMock(
            chroma_host="localhost", chroma_port=8000
        )
        from src.shared.vectorstore import get_chroma_client

        get_chroma_client()
        mock_http_client.assert_called_once_with(host="localhost", port=8000)
