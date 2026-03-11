"""Factory para LLM e Embeddings via LangChain."""

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from src.core.dependencies import get_settings


def get_llm() -> BaseChatModel:
    """Retorna instância LangChain do LLM conforme LLM_PROVIDER."""
    settings = get_settings()
    provider = settings.llm_provider

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.openai_llm_model,
            api_key=settings.openai_api_key,
        )

    if provider == "bedrock":
        from langchain_aws import ChatBedrock

        return ChatBedrock(
            model_id=settings.bedrock_llm_model,
            region_name=settings.aws_region,
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model=settings.gemini_llm_model,
        google_api_key=settings.google_api_key,
    )


def get_embeddings() -> Embeddings:
    """Retorna instância LangChain de Embeddings conforme LLM_PROVIDER."""
    settings = get_settings()
    provider = settings.llm_provider

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(
            model=settings.openai_embed_model,
            api_key=settings.openai_api_key,
        )

    if provider == "bedrock":
        from langchain_aws import BedrockEmbeddings

        return BedrockEmbeddings(
            model_id=settings.bedrock_embed_model,
            region_name=settings.aws_region,
        )

    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    return GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embed_model,
        google_api_key=settings.google_api_key,
    )
