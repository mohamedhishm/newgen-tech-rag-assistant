"""Pytest suite. Uses deterministic fake embeddings and a fake LLM: no network or model downloads."""
import pytest
from fastapi.testclient import TestClient
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from pydantic import ValidationError

from backend.config import Settings
from backend.main import create_app
from backend.rag_pipeline import RAGPipeline, load_documents, split_documents
from backend.services import NOT_FOUND_MESSAGE, SYSTEM_PROMPT, GroqService, build_messages


@pytest.fixture
def data_dir(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    (d / "hr_policy.md").write_text(
        "# Remote Work\n\nEmployees may work remotely. Core hours are 10:00 to 15:00.\n\n"
        "## Leave\n\nEmployees receive 25 days of annual leave.\n", encoding="utf-8")
    (d / "it_support.txt").write_text("Submit IT tickets through the service desk portal.", encoding="utf-8")
    (d / "ignore.exe").write_text("binary", encoding="utf-8")
    return d


@pytest.fixture
def settings(tmp_path, data_dir):
    return Settings(data_dir=data_dir, vector_store_dir=tmp_path / "vs", groq_api_key="test",
                    min_relevance=-10.0, chunk_size=200, chunk_overlap=20, _env_file=None)


@pytest.fixture
def pipeline(settings):
    p = RAGPipeline(settings, embeddings=DeterministicFakeEmbedding(size=32))
    p.ingest(reset=False)
    return p


class FakeClient:
    class _Msg:
        content = "Core hours are 10:00 to 15:00 [1]."
    class _Choice:
        message = None
    def __init__(self):
        self.calls = 0
        self.chat = self
        self.completions = self
    def create(self, **kwargs):
        self.calls += 1
        choice = self._Choice(); choice.message = self._Msg()
        return type("R", (), {"choices": [choice]})()


# ---- config ----
def test_settings_defaults_and_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "abc")
    monkeypatch.setenv("TOP_K", "3")
    s = Settings(_env_file=None)
    assert s.groq_api_key == "abc" and s.top_k == 3
    assert s.data_dir.is_absolute()


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValidationError):
        Settings(chunk_size=200, chunk_overlap=300, _env_file=None)


# ---- ingestion ----
def test_load_documents_filters_extensions(data_dir):
    docs = load_documents(data_dir)
    assert {d.metadata["source"] for d in docs} == {"hr_policy.md", "it_support.txt"}


def test_load_documents_missing_dir(tmp_path):
    assert load_documents(tmp_path / "nope") == []


def test_split_documents_metadata_and_size():
    doc = Document(page_content="# Title\n\n" + ("Sentence about policy. " * 60), metadata={"source": "a.md"})
    chunks = split_documents([doc], 200, 20)
    assert len(chunks) > 1
    assert all(c.metadata["source"] == "a.md" for c in chunks)
    assert all(len(c.page_content) <= 200 for c in chunks)
    assert chunks[0].metadata["section"] == "Title"


# ---- retrieval ----
def test_ingest_counts(pipeline):
    assert pipeline.document_count == 2
    assert pipeline.chunk_count() >= 2
    assert pipeline.source_files() == ["hr_policy.md", "it_support.txt"]


def test_retrieve_returns_ranked_chunks(pipeline):
    res = pipeline.retrieve("Employees receive 25 days of annual leave.", k=2)
    assert len(res) == 2
    assert res[0].score >= res[1].score
    assert res[0].source in {"hr_policy.md", "it_support.txt"}


def test_retrieve_threshold_filters_everything(pipeline):
    pipeline.settings.min_relevance = 5.0
    assert pipeline.retrieve("anything") == []


# ---- prompt / LLM ----
def test_prompt_contains_grounding_rules_and_context(pipeline):
    chunks = pipeline.retrieve("leave", k=1)
    msgs = build_messages("leave?", chunks)
    assert msgs[0]["content"] == SYSTEM_PROMPT
    assert "Never hallucinate" in SYSTEM_PROMPT
    assert chunks[0].text in msgs[1]["content"]


def test_llm_not_called_without_context(settings):
    client = FakeClient()
    svc = GroqService(settings, client=client)
    assert svc.answer("q", []) == NOT_FOUND_MESSAGE
    assert client.calls == 0


def test_llm_missing_key_raises(settings):
    settings.groq_api_key = ""
    with pytest.raises(RuntimeError):
        GroqService(settings).client


# ---- API ----
@pytest.fixture
def client(settings, pipeline):
    app = create_app(settings=settings, pipeline=pipeline, llm=GroqService(settings, client=FakeClient()))
    return TestClient(app)


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["documents"] == 2 and body["llm_configured"] is True


def test_query_returns_answer_and_sources(client):
    r = client.post("/api/query", json={"question": "What are the core hours?"})
    assert r.status_code == 200
    body = r.json()
    assert "10:00" in body["answer"]
    assert body["grounded"] is True and body["sources"]
    assert {"id", "source", "score", "snippet"} <= set(body["sources"][0])


@pytest.mark.parametrize("payload", [{}, {"question": ""}, {"question": "   "}, {"question": "x" * 2001}])
def test_query_validation(client, payload):
    assert client.post("/api/query", json=payload).status_code == 422


def test_query_ungrounded_when_nothing_relevant(client, pipeline):
    pipeline.settings.min_relevance = 5.0
    body = client.post("/api/query", json={"question": "Who won the world cup?"}).json()
    assert body["answer"] == NOT_FOUND_MESSAGE and body["grounded"] is False


def test_ingest_endpoint(client):
    r = client.post("/api/ingest")
    assert r.status_code == 200 and r.json()["documents"] == 2
