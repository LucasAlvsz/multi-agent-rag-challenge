"""Agregador de rotas da API."""

from fastapi import APIRouter

from src.api.routes import ask, documents, health

api_router = APIRouter()
api_router.include_router(documents.router)
api_router.include_router(ask.router)
api_router.include_router(health.router)
