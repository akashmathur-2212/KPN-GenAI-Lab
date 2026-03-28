from pathlib import Path
from uuid import uuid4
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from src.logging.logger import get_logger

logger = get_logger()

def get_or_create_vector_store(
    document_name: str,
    embeddings,
    documents,
    number_of_documents: int
):
    GOLD_PATH = Path(f"./data/gold/{document_name}")

    # Check if vector store exists
    if GOLD_PATH.exists() and any(GOLD_PATH.iterdir()):
        logger.info(f"Loading existing vector store from {GOLD_PATH}")

        vector_store = FAISS.load_local(
            str(GOLD_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vector_store

    logger.info(f"Creating new vector store at {GOLD_PATH}")

    # Create vector store
    index = faiss.IndexFlatL2(len(embeddings.embed_query("Hello KPN")))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # Generate IDs
    uuids = [str(uuid4()) for _ in range(len(documents))]

    # Add documents
    vector_store.add_documents(
        documents=documents[:number_of_documents],
        ids=uuids[:number_of_documents]
    )

    # Ensure directory exists
    GOLD_PATH.mkdir(parents=True, exist_ok=True)

    # Save locally
    vector_store.save_local(str(GOLD_PATH))
    logger.info(f"Vector store saved at {GOLD_PATH}")

    return vector_store