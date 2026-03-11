"""Rota para ingestão de documentos."""

import asyncio

from fastapi import APIRouter, HTTPException

from src.api.schemas.common import ErrorResponse
from src.api.schemas.documents import DocumentRequest, DocumentResponse
from src.services.ingest_service import handle_ingest

router = APIRouter(tags=["Ingestão"])


@router.post(
    "/documents",
    response_model=DocumentResponse,
    summary="Ingerir documento",
    description=(
        "Recebe um documento de texto, divide em chunks com overlap, "
        "gera embeddings e armazena no ChromaDB na coleção correspondente ao domínio."
    ),
    responses={
        200: {"description": "Documento indexado com sucesso"},
        400: {
            "description": "Conteúdo contém apenas espaços em branco",
            "model": ErrorResponse,
        },
        422: {
            "description": "Payload inválido (conteúdo vazio, campo ausente ou domínio inválido)"
        },
        503: {
            "description": "Provider LLM/Embeddings não disponível",
            "model": ErrorResponse,
        },
    },
)
async def post_documents(request: DocumentRequest) -> DocumentResponse:
    if not request.content or not request.content.strip():
        raise HTTPException(
            status_code=400, detail="O campo 'content' não pode estar vazio"
        )

    result = await asyncio.to_thread(handle_ingest, request.content, request.domain)
    return DocumentResponse(**result)
