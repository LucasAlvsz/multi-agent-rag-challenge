"""Serviço de ingestão de documentos: chunking → embeddings → ChromaDB."""

import uuid

from langchain_chroma import Chroma

from src.core.dependencies import get_settings
from src.shared.chunking import chunk_text
from src.shared.model_providers import get_embeddings
from src.shared.vectorstore import get_chroma_client


def handle_ingest(content: str, domain: str) -> dict:
    """
    Processa o documento: chunking, embeddings e armazenamento no Chroma.

    Args:
        content: Texto do documento.
        domain: Coleção de destino (rh ou tecnico).

    Returns:
        Dict com doc_id, chunks_count e domain.
    """
    chunks = chunk_text(content)
    if not chunks:
        return {"doc_id": None, "chunks_count": 0, "domain": domain}

    settings = get_settings()
    embeddings = get_embeddings()
    client = get_chroma_client()
    collection_name = settings.collection_map.get(domain, domain)

    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    doc_id = str(uuid.uuid4())
    metadatas = [{"doc_id": doc_id} for _ in chunks]
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    vectorstore.add_texts(texts=chunks, metadatas=metadatas, ids=ids)

    return {"doc_id": doc_id, "chunks_count": len(chunks), "domain": domain}
