"""FastAPI entry point. Run: uvicorn backend.main:app --reload"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from .config import ROOT_DIR, Settings, get_settings
from .rag_pipeline import RAGPipeline
from .services import GroqService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("newgen")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

    @field_validator("question")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("question must not be blank")
        return v


class Source(BaseModel):
    id: int
    source: str
    section: str = ""
    score: float
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    grounded: bool


class HealthResponse(BaseModel):
    status: str
    model: str
    llm_configured: bool
    documents: int
    chunks: int


class IngestResponse(BaseModel):
    documents: int
    chunks: int


def create_app(
    settings: Optional[Settings] = None,
    pipeline: Optional[RAGPipeline] = None,
    llm: Optional[GroqService] = None,
) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if app.state.pipeline is None:
            app.state.pipeline = RAGPipeline(settings)
            app.state.pipeline.ensure_index()
        if app.state.llm is None:
            app.state.llm = GroqService(settings)
        yield

    app = FastAPI(title="NewGen Tech Knowledge Assistant", version="1.0.0", lifespan=lifespan)
    app.state.pipeline = pipeline
    app.state.llm = llm
    if pipeline is not None and llm is None:
        app.state.llm = GroqService(settings)

    @app.get("/api/health", response_model=HealthResponse)
    def health():
        p: RAGPipeline = app.state.pipeline
        return HealthResponse(
            status="ok" if p is not None else "starting",
            model=settings.groq_model,
            llm_configured=bool(settings.groq_api_key) or app.state.llm._client is not None,
            documents=p.document_count if p else 0,
            chunks=p.chunk_count() if p else 0,
        )

    @app.post("/api/query", response_model=QueryResponse)
    def query(req: QueryRequest):
        p: RAGPipeline = app.state.pipeline
        if p is None:
            raise HTTPException(503, "Knowledge base is not ready.")
        chunks = p.retrieve(req.question)
        try:
            answer = app.state.llm.answer(req.question, chunks)
        except RuntimeError as exc:
            raise HTTPException(503, str(exc))
        except Exception as exc:  # noqa: BLE001
            logger.exception("LLM call failed")
            raise HTTPException(502, f"Language model request failed: {exc}")
        sources = [
            Source(id=i, source=c.source, section=c.section, score=c.score,
                   snippet=c.text[:300].replace("\n", " "))
            for i, c in enumerate(chunks, start=1)
        ]
        return QueryResponse(answer=answer, sources=sources, grounded=bool(chunks))

    @app.post("/api/ingest", response_model=IngestResponse)
    def ingest():
        p: RAGPipeline = app.state.pipeline
        if p is None:
            raise HTTPException(503, "Knowledge base is not ready.")
        return IngestResponse(**p.ingest(reset=True))

    frontend = ROOT_DIR / "frontend"
    if frontend.exists():
        app.mount("/", StaticFiles(directory=str(frontend), html=True), name="frontend")
    return app


app = create_app()
