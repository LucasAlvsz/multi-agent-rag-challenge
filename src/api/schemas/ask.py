"""Schemas Pydantic para o endpoint de consulta RAG."""

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    """Documento fonte recuperado pela busca vetorial."""

    document: str = Field(description="Conteúdo do chunk recuperado")
    metadata: dict = Field(description="Metadados do chunk (ex: doc_id)")


class AskRequest(BaseModel):
    """Payload para consulta ao sistema RAG."""

    question: str = Field(
        ...,
        description="Pergunta do usuário em linguagem natural",
        min_length=1,
        json_schema_extra={"examples": ["Qual é a política de férias?"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"question": "Qual é a política de férias?"},
                {"question": "Como integrar a API de pagamentos?"},
            ]
        }
    }


class AskResponse(BaseModel):
    """Resposta da consulta RAG."""

    answer: str = Field(
        description="Resposta gerada pelo LLM com base no contexto recuperado"
    )
    classification: str = Field(
        description="Classificação da pergunta pelo orquestrador: rh, tecnico ou both"
    )
    sources: list[SourceDocument] = Field(
        description="Lista de chunks usados como contexto para gerar a resposta"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "A política de férias da empresa prevê 30 dias corridos após 12 meses de trabalho.",
                    "classification": "rh",
                    "sources": [
                        {
                            "document": "A política de férias da empresa prevê 30 dias corridos após 12 meses de trabalho. O colaborador deve solicitar com 30 dias de antecedência.",
                            "metadata": {
                                "doc_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
                            },
                        }
                    ],
                }
            ]
        }
    }
