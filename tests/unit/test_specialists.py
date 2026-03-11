"""Testes unitários para src/agents/specialists.py."""

from unittest.mock import MagicMock, patch

from src.agents.specialists import query_both, query_rh, query_tecnico


class TestQueryCollection:
    """Testes para _query_collection via funções públicas."""

    @patch("src.agents.specialists.get_settings")
    @patch("src.agents.specialists.get_chroma_client")
    @patch("src.agents.specialists.get_embeddings")
    @patch("src.agents.specialists.Chroma")
    def test_query_rh(self, mock_chroma_cls, mock_embeddings, mock_client, mock_settings):
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_doc = MagicMock()
        mock_doc.page_content = "Política de férias"
        mock_doc.metadata = {"doc_id": "doc-1"}

        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = [mock_doc]

        mock_vectorstore = MagicMock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma_cls.return_value = mock_vectorstore

        state = {"question": "Qual a política de férias?"}
        result = query_rh(state)

        assert result["context"] == "Política de férias"
        assert len(result["sources"]) == 1
        assert result["sources"][0]["document"] == "Política de férias"
        mock_chroma_cls.assert_called_once()

    @patch("src.agents.specialists.get_settings")
    @patch("src.agents.specialists.get_chroma_client")
    @patch("src.agents.specialists.get_embeddings")
    @patch("src.agents.specialists.Chroma")
    def test_query_tecnico(self, mock_chroma_cls, mock_embeddings, mock_client, mock_settings):
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_doc = MagicMock()
        mock_doc.page_content = "Documentação da API"
        mock_doc.metadata = {"doc_id": "doc-2"}

        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = [mock_doc]

        mock_vectorstore = MagicMock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma_cls.return_value = mock_vectorstore

        state = {"question": "Como funciona a API?"}
        result = query_tecnico(state)

        assert result["context"] == "Documentação da API"
        assert len(result["sources"]) == 1

    @patch("src.agents.specialists.get_settings")
    @patch("src.agents.specialists.get_chroma_client")
    @patch("src.agents.specialists.get_embeddings")
    @patch("src.agents.specialists.Chroma")
    def test_query_returns_empty_when_no_docs(self, mock_chroma_cls, mock_embeddings, mock_client, mock_settings):
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = []

        mock_vectorstore = MagicMock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_chroma_cls.return_value = mock_vectorstore

        state = {"question": "Pergunta sem resultado?"}
        result = query_rh(state)

        assert result["context"] == ""
        assert result["sources"] == []


class TestQueryBoth:
    """Testes para query_both."""

    @patch("src.agents.specialists.get_settings")
    @patch("src.agents.specialists.get_chroma_client")
    @patch("src.agents.specialists.get_embeddings")
    @patch("src.agents.specialists.Chroma")
    def test_merges_both_collections(self, mock_chroma_cls, mock_embeddings, mock_client, mock_settings):
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_doc_rh = MagicMock()
        mock_doc_rh.page_content = "Info RH"
        mock_doc_rh.metadata = {"doc_id": "rh-1"}

        mock_doc_tec = MagicMock()
        mock_doc_tec.page_content = "Info Técnica"
        mock_doc_tec.metadata = {"doc_id": "tec-1"}

        call_count = 0

        def create_vectorstore(**kwargs):
            nonlocal call_count
            mock_retriever = MagicMock()
            if call_count == 0:
                mock_retriever.invoke.return_value = [mock_doc_rh]
            else:
                mock_retriever.invoke.return_value = [mock_doc_tec]
            call_count += 1
            vs = MagicMock()
            vs.as_retriever.return_value = mock_retriever
            return vs

        mock_chroma_cls.side_effect = create_vectorstore

        state = {"question": "Pergunta mista?"}
        result = query_both(state)

        assert "[Contexto RH]" in result["context"]
        assert "[Contexto Técnico]" in result["context"]
        assert len(result["sources"]) == 2

    @patch("src.agents.specialists.get_settings")
    @patch("src.agents.specialists.get_chroma_client")
    @patch("src.agents.specialists.get_embeddings")
    @patch("src.agents.specialists.Chroma")
    def test_handles_empty_rh(self, mock_chroma_cls, mock_embeddings, mock_client, mock_settings):
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_doc_tec = MagicMock()
        mock_doc_tec.page_content = "Info Técnica"
        mock_doc_tec.metadata = {"doc_id": "tec-1"}

        call_count = 0

        def create_vectorstore(**kwargs):
            nonlocal call_count
            mock_retriever = MagicMock()
            if call_count == 0:
                mock_retriever.invoke.return_value = []
            else:
                mock_retriever.invoke.return_value = [mock_doc_tec]
            call_count += 1
            vs = MagicMock()
            vs.as_retriever.return_value = mock_retriever
            return vs

        mock_chroma_cls.side_effect = create_vectorstore

        state = {"question": "Pergunta apenas técnica?"}
        result = query_both(state)

        assert "[Contexto RH]" not in result["context"]
        assert "[Contexto Técnico]" in result["context"]
        assert len(result["sources"]) == 1
