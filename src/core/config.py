"""Configuração centralizada da aplicação via Pydantic BaseSettings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente e/ou arquivo .env."""

    # Provider
    llm_provider: str = "openai"

    # OpenAI
    openai_api_key: str = ""
    openai_llm_model: str = "gpt-4o-mini"
    openai_embed_model: str = "text-embedding-3-small"

    # AWS Bedrock
    aws_region: str = "us-east-1"
    bedrock_llm_model: str = "anthropic.claude-3-haiku-20240307-v1:0"
    bedrock_embed_model: str = "amazon.titan-embed-text-v2:0"

    # Google Gemini
    google_api_key: str = ""
    gemini_llm_model: str = "gemini-2.5-flash-lite"
    gemini_embed_model: str = "gemini-embedding-001"

    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    # Collection mapping (domain -> ChromaDB collection name)
    collection_map: dict = {"rh": "col_rh", "tecnico": "col_tecnico"}

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
