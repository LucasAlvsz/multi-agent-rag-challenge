"""API FastAPI para RAG — app factory com lifespan e routers."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.agents.graph import build_graph
from src.api.router import api_router
from src.core.dependencies import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa recursos no startup (graph) e limpa no shutdown."""
    app.state.graph = build_graph()
    yield


def create_app() -> FastAPI:
    """Factory que cria e configura a aplicação FastAPI."""
    settings = get_settings()

    application = FastAPI(
        title="RAG Multi-Agent API",
        description=(
            "API para ingestão de documentos e consultas com RAG multi-agente.\n\n"
            "## Funcionalidades\n\n"
            "- **Ingestão**: recebe documentos, divide em chunks, gera embeddings e armazena "
            "no ChromaDB em coleções separadas por domínio (RH ou Técnico).\n"
            "- **Consulta**: usa um orquestrador multi-agente (LangGraph) que classifica a pergunta, "
            "roteia para o agente especialista correto e gera uma resposta baseada no contexto recuperado.\n\n"
            "## Providers suportados\n\n"
            "LLM e Embeddings: **OpenAI**, **AWS Bedrock** e **Google Gemini** — "
            "configurável via variável de ambiente `LLM_PROVIDER`."
        ),
        version="1.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router)

    @application.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=503,
            content={"detail": str(exc)},
        )

    return application


app = create_app()
