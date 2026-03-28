from pathlib import Path
from langchain_docling.loader import DoclingLoader
from src.utils.common import save_docs_to_jsonl, load_docs_from_jsonl
from src.logging.logger import get_logger
from src.utils.paths import BRONZE_PATH, SILVER_PATH

logger = get_logger(__name__)

def load_or_parse_pdf(filename: str):
    """
    Checks if JSONL exists in SILVER using filename.
    If exists then loads it
    Else parses from PDF in BRONZE and saves it
    """

    # Construct full paths
    pdf_path = BRONZE_PATH / filename / ".pdf"
    jsonl_path = SILVER_PATH / (Path(filename).stem + ".jsonl")

    logger.info(f"Checking SILVER for: {jsonl_path.name}")

    # If already exists then load
    if jsonl_path.exists():
        logger.info("JSONL found in SILVER. Loading documents")
        documents = load_docs_from_jsonl(jsonl_path)
        return documents

    # Else parse using Docling
    logger.info("JSONL not found. Parsing PDF with Docling.")

    loader = DoclingLoader(file_path=pdf_path)
    documents = loader.load()

    logger.info(f"Parsed {len(documents)} documents. Saving to SILVER...")

    # Ensure SILVER directory exists
    SILVER_PATH.mkdir(parents=True, exist_ok=True)

    save_docs_to_jsonl(documents=documents, file_path=jsonl_path)

    logger.info("Saved parsed documents to SILVER.")

    return documents
