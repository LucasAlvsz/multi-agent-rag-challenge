"""Rota de health check."""

from fastapi import APIRouter

from src.api.schemas.common import HealthResponse

router = APIRouter(tags=["Sistema"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Verifica se a API está respondendo.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
