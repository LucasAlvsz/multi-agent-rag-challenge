"""Rota para consulta RAG multi-agente."""

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas.ask import AskRequest, AskResponse
from src.api.schemas.common import ErrorResponse
from src.core.dependencies import get_graph
from src.services.query_service import handle_ask

router = APIRouter(tags=["Consulta"])


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Consultar com RAG multi-agente",
    description=(
        "Recebe uma pergunta em linguagem natural. O orquestrador classifica a intenção "
        "(rh, tecnico ou ambos), roteia para o agente especialista apropriado que busca "
        "contexto no ChromaDB, e gera uma resposta via LLM."
    ),
    responses={
        200: {"description": "Resposta gerada com sucesso"},
        400: {
            "description": "Pergunta contém apenas espaços em branco",
            "model": ErrorResponse,
        },
        422: {
            "description": "Payload inválido (pergunta vazia ou campo ausente)"
        },
        503: {
            "description": "Provider LLM/Embeddings não disponível",
            "model": ErrorResponse,
        },
    },
)
def post_ask(request: AskRequest, graph=Depends(get_graph)) -> AskResponse:
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400, detail="O campo 'question' não pode estar vazio"
        )

    result = handle_ask(request.question, graph)
    return AskResponse(**result)
