"""Dependency injection para FastAPI (Depends)."""

from functools import lru_cache

from fastapi import Request

from src.core.config import Settings


@lru_cache
def get_settings() -> Settings:
    """Retorna instância singleton de Settings (cacheada)."""
    return Settings()


def get_graph(request: Request):
    """Retorna o grafo LangGraph inicializado no lifespan da aplicação."""
    return request.app.state.graph
