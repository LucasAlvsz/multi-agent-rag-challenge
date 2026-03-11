"""Divisão de texto em chunks com overlap via LangChain."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """
    Divide o texto em chunks com overlap usando RecursiveCharacterTextSplitter.

    Args:
        text: Texto a ser dividido.
        chunk_size: Tamanho máximo de cada chunk em caracteres.
        overlap: Número de caracteres de sobreposição entre chunks.

    Returns:
        Lista de chunks.
    """
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        strip_whitespace=True,
    )

    return splitter.split_text(text.strip())
