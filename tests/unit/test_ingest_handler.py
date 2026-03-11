"""Testes unitários para src/services/ingest_service.py."""

from unittest.mock import MagicMock, patch

from src.services.ingest_service import handle_ingest


class TestHandleIngest:
    """Testes para handle_ingest."""

    @patch("src.services.ingest_service.Chroma")
    @patch("src.services.ingest_service.get_chroma_client")
    @patch("src.services.ingest_service.get_embeddings")
    @patch("src.services.ingest_service.get_settings")
    @patch("src.services.ingest_service.chunk_text")
    def test_successful_ingest(
        self, mock_chunk, mock_settings, mock_embed, mock_client, mock_chroma_cls
    ):
        mock_chunk.return_value = ["chunk1", "chunk2"]
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_vectorstore = MagicMock()
        mock_chroma_cls.return_value = mock_vectorstore

        result = handle_ingest("conteúdo do documento", "rh")

        assert result["doc_id"] is not None
        assert result["chunks_count"] == 2
        assert result["domain"] == "rh"
        mock_chunk.assert_called_once_with("conteúdo do documento")
        mock_vectorstore.add_texts.assert_called_once()

    @patch("src.services.ingest_service.chunk_text")
    def test_empty_chunks_returns_none_doc_id(self, mock_chunk):
        mock_chunk.return_value = []

        result = handle_ingest("", "tecnico")

        assert result["doc_id"] is None
        assert result["chunks_count"] == 0
        assert result["domain"] == "tecnico"

    @patch("src.services.ingest_service.Chroma")
    @patch("src.services.ingest_service.get_chroma_client")
    @patch("src.services.ingest_service.get_embeddings")
    @patch("src.services.ingest_service.get_settings")
    @patch("src.services.ingest_service.chunk_text")
    def test_passes_domain_to_chroma(
        self, mock_chunk, mock_settings, mock_embed, mock_client, mock_chroma_cls
    ):
        mock_chunk.return_value = ["chunk1"]
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_vectorstore = MagicMock()
        mock_chroma_cls.return_value = mock_vectorstore

        handle_ingest("conteúdo", "tecnico")

        call_kwargs = mock_chroma_cls.call_args.kwargs
        assert call_kwargs["collection_name"] == "col_tecnico"

    @patch("src.services.ingest_service.Chroma")
    @patch("src.services.ingest_service.get_chroma_client")
    @patch("src.services.ingest_service.get_embeddings")
    @patch("src.services.ingest_service.get_settings")
    @patch("src.services.ingest_service.chunk_text")
    def test_generates_unique_doc_ids(
        self, mock_chunk, mock_settings, mock_embed, mock_client, mock_chroma_cls
    ):
        mock_chunk.return_value = ["chunk"]
        mock_settings.return_value = MagicMock(
            collection_map={"rh": "col_rh", "tecnico": "col_tecnico"}
        )
        mock_vectorstore = MagicMock()
        mock_chroma_cls.return_value = mock_vectorstore

        result1 = handle_ingest("doc1", "rh")
        result2 = handle_ingest("doc2", "rh")

        assert result1["doc_id"] != result2["doc_id"]
