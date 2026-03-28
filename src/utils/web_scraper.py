import requests
from bs4 import BeautifulSoup
from typing import List
from pathlib import Path

from langchain_core.documents import Document
from src.logging.logger import get_logger
from src.utils.paths import BRONZE_PATH

logger = get_logger(__name__)

def load_urls_from_txt(file_path: str = BRONZE_PATH / "urls.txt") -> List[str]:
    """
    Reads URLs from a .txt file (one URL per line)
    """
    path = Path(file_path)

    if not path.exists():
        logger.error(f"URL file not found: {file_path}")
        return []

    logger.info(f"Loading URLs from {file_path}")

    with path.open("r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    logger.info(f"Loaded {len(urls)} URLs")

    return urls

def create_documents_from_urls() -> List[Document]:
    """
    Fetches URLs and converts them into LangChain Document objects for embeddings.
    """

    urls = load_urls_from_txt()

    documents = []

    for idx, url in enumerate(urls):
        try:
            logger.info(f"[{idx}] Processing URL: {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            # Extract main content (you can improve this later)
            content = soup.get_text(separator=" ", strip=True)

            logger.debug(f"[{idx}] Title extracted: {title}")
            logger.debug(f"[{idx}] Content length: {len(content)} characters")

            doc = Document(
                page_content=content,
                metadata={
                    "source": url,
                    "title": title,
                },
            )

            documents.append(doc)

        except Exception as e:
            logger.error(f"[{idx}] Failed to process {url}: {e}")

    logger.info(f"Successfully created {len(documents)} documents")

    return documents