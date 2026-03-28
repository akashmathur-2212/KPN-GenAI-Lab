import typing as t
import jsonlines
from langchain_core.documents import Document

def save_docs_to_jsonl(documents: t.Iterable[Document], file_path: str) -> None:
    with jsonlines.open(file_path, mode="w") as writer:
        for idx, doc in enumerate(documents):
            doc_dict = doc.model_dump()
            doc_dict["id"] = idx
            writer.write(doc_dict)

def load_docs_from_jsonl(file_path) -> t.Iterable[Document]:
    documents = []
    with jsonlines.open(file_path, mode="r") as reader:
        for doc in reader:
            documents.append(Document(**doc))
    return documents