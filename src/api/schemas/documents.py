"""Schemas Pydantic para o endpoint de ingestão de documentos."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    """Payload para ingestão de documentos."""

    content: str = Field(
        ...,
        description="Texto do documento a ser indexado",
        min_length=1,
        json_schema_extra={
            "examples": [
                "A política de férias da empresa prevê 30 dias corridos após 12 meses de trabalho."
            ]
        },
    )
    domain: Literal["rh", "tecnico"] = Field(
        ...,
        description="Domínio/coleção de destino do documento",
        json_schema_extra={"examples": ["rh"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "A política de férias da empresa prevê 30 dias corridos após 12 meses de trabalho. O colaborador deve solicitar com 30 dias de antecedência.",
                    "domain": "rh",
                },
                {
                    "content": "A API de pagamentos aceita requisições POST no endpoint /v1/payments. O payload deve incluir amount, currency e customer_id. A autenticação é feita via Bearer token.",
                    "domain": "tecnico",
                },
            ]
        }
    }


class DocumentResponse(BaseModel):
    """Resposta da ingestão de documento."""

    doc_id: Optional[str] = Field(
        description="UUID do documento indexado. Null se o conteúdo resultou em zero chunks."
    )
    chunks_count: int = Field(
        description="Número de chunks gerados a partir do documento"
    )
    domain: str = Field(
        description="Domínio/coleção onde o documento foi armazenado"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "doc_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "chunks_count": 3,
                    "domain": "rh",
                }
            ]
        }
    }
