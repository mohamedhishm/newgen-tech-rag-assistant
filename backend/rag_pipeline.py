"""Ingestion, chunking, embedding, vector store and retrieval."""
from __future__ import annotations

import logging
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from html.parser import HTMLParser

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import Settings

logger = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".docx", ".csv", ".json", ".html"
}


@dataclass
class RetrievedChunk:
    text: str
    source: str
    section: str
    score: float

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {"script", "style"}
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())

def read_file(path: Path) -> str:
    ext = path.suffix.lower()

    if ext == ".pdf":
        from pypdf import PdfReader
        return "\n".join(
            (p.extract_text() or "")
            for p in PdfReader(str(path)).pages
        )

    if ext == ".docx":
        import docx
        return "\n".join(
            p.text for p in docx.Document(str(path)).paragraphs
        )

    if ext == ".html":
        parser = HTMLTextExtractor()
        parser.feed(
            path.read_text(encoding="utf-8", errors="ignore")
        )
        return "\n".join(parser.text)

    return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(data_dir: Path) -> List[Document]:
    """Load every supported file in data_dir (recursively) as one Document each."""
    docs: List[Document] = []
    if not data_dir.exists():
        return docs
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            text = read_file(path).strip()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Skipping %s: %s", path.name, exc)
            continue
        if text:
            docs.append(Document(page_content=text, metadata={"source": path.name}))
    return docs


def _nearest_heading(full_text: str, chunk: str) -> str:
    idx = full_text.find(chunk[:80])
    if idx < 0:
        return ""
    headings = re.findall(r"^(#{1,4}\s+.+)$", full_text[: idx + 1], flags=re.M)
    return headings[-1].lstrip("# ").strip() if headings else ""


def split_documents(docs: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )
    chunks: List[Document] = []
    for doc in docs:
        for i, piece in enumerate(splitter.split_text(doc.page_content)):
            meta = {
                "source": doc.metadata["source"],
                "chunk_index": i,
                "section": _nearest_heading(doc.page_content, piece),
            }
            chunks.append(Document(page_content=piece, metadata=meta))
    return chunks


def build_embeddings(model_name: str) -> Embeddings:
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=model_name, encode_kwargs={"normalize_embeddings": True}
    )


class RAGPipeline:
    def __init__(self, settings: Settings, embeddings: Optional[Embeddings] = None):
        self.settings = settings
        self.embeddings = embeddings or build_embeddings(settings.embedding_model)
        self._store = None
        self.document_count = 0

    # ---- vector store ----
    def _open_store(self):
        from langchain_chroma import Chroma

        return Chroma(
            collection_name=self.settings.collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(self.settings.vector_store_dir),
            collection_metadata={"hnsw:space": "cosine"},
        )

    @property
    def store(self):
        if self._store is None:
            self._store = self._open_store()
        return self._store

    def chunk_count(self) -> int:
        return self.store._collection.count()

    def source_files(self) -> List[str]:
        metas = self.store.get(include=["metadatas"]).get("metadatas") or []
        return sorted({m["source"] for m in metas if m and "source" in m})

    # ---- ingestion ----
    def ingest(self, reset: bool = True) -> dict:
        if reset:
            try:
                self.store.delete_collection()
            except Exception:  # noqa: BLE001
                pass
            self._store = None
            if self.settings.vector_store_dir.exists():
                shutil.rmtree(self.settings.vector_store_dir, ignore_errors=True)
        docs = load_documents(self.settings.data_dir)
        chunks = split_documents(docs, self.settings.chunk_size, self.settings.chunk_overlap)
        if chunks:
            for start in range(0, len(chunks), 128):
                self.store.add_documents(chunks[start : start + 128])
        self.document_count = len(docs)
        logger.info("Ingested %d documents into %d chunks", len(docs), len(chunks))
        return {"documents": len(docs), "chunks": len(chunks)}

    def ensure_index(self) -> None:
        if self.chunk_count() == 0:
            self.ingest(reset=False)
        else:
            self.document_count = len(self.source_files())

    # ---- retrieval ----
    def retrieve(self, question: str, k: Optional[int] = None) -> List[RetrievedChunk]:
        k = k or self.settings.top_k
        results = self.store.similarity_search_with_score(question, k=k)
        out: List[RetrievedChunk] = []
        for doc, distance in results:
            score = 1.0 - float(distance)  # cosine distance -> similarity
            if score >= self.settings.min_relevance:
                out.append(
                    RetrievedChunk(
                        text=doc.page_content,
                        source=doc.metadata.get("source", "unknown"),
                        section=doc.metadata.get("section", ""),
                        score=round(score, 4),
                    )
                )
        return out
