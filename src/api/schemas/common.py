"""Schemas Pydantic compartilhados (health, erros)."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Resposta do health check."""

    status: str = Field(description="Status da API", examples=["ok"])


class ErrorResponse(BaseModel):
    """Resposta de erro."""

    detail: str = Field(description="Mensagem de erro")
