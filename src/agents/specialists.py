"""Nós especialistas: recuperam contexto de coleções específicas do Chroma."""

from langchain_chroma import Chroma

from src.agents.state import AgentState
from src.core.dependencies import get_settings
from src.shared.model_providers import get_embeddings
from src.shared.vectorstore import get_chroma_client


def _query_collection(collection_name: str, question: str, k: int = 5) -> dict:
    """Busca os k chunks mais similares em uma coleção específica."""
    embeddings = get_embeddings()
    client = get_chroma_client()

    resolved_name = get_settings().collection_map.get(collection_name, collection_name)

    vectorstore = Chroma(
        client=client,
        collection_name=resolved_name,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)

    if not docs:
        return {"context": "", "sources": []}

    context = "\n\n".join(doc.page_content for doc in docs)
    sources = [
        {"document": doc.page_content, "metadata": doc.metadata}
        for doc in docs
    ]
    return {"context": context, "sources": sources}


def query_rh(state: AgentState) -> dict:
    """Especialista RH: busca na coleção 'rh'."""
    return _query_collection("rh", state["question"])


def query_tecnico(state: AgentState) -> dict:
    """Especialista Técnico: busca na coleção 'tecnico'."""
    return _query_collection("tecnico", state["question"])


def query_both(state: AgentState) -> dict:
    """Busca em ambas as coleções e mescla os resultados."""
    rh_result = _query_collection("rh", state["question"], k=3)
    tecnico_result = _query_collection("tecnico", state["question"], k=3)

    merged_context = ""
    if rh_result["context"]:
        merged_context += f"[Contexto RH]\n{rh_result['context']}\n\n"
    if tecnico_result["context"]:
        merged_context += f"[Contexto Técnico]\n{tecnico_result['context']}"

    merged_sources = rh_result["sources"] + tecnico_result["sources"]
    return {"context": merged_context.strip(), "sources": merged_sources}
