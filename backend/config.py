"""Application settings loaded from environment / .env via Pydantic."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    groq_api_key: str = Field(default="", description="Groq API key")
    groq_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    data_dir: Path = ROOT_DIR / "data"
    vector_store_dir: Path = ROOT_DIR / "vector_store"
    collection_name: str = "newgen_knowledge"
    chunk_size: int = Field(default=900, ge=100, le=4000)
    chunk_overlap: int = Field(default=150, ge=0)
    top_k: int = Field(default=5, ge=1, le=20)
    min_relevance: float = Field(default=0.25, description="Minimum cosine similarity to use a chunk")
    max_question_length: int = 1000
    temperature: float = 0.0
    max_tokens: int = 700

    @field_validator("data_dir", "vector_store_dir", mode="after")
    @classmethod
    def _absolute(cls, v: Path) -> Path:
        return v if v.is_absolute() else (ROOT_DIR / v)

    @field_validator("chunk_overlap")
    @classmethod
    def _overlap_lt_size(cls, v: int, info) -> int:
        size = info.data.get("chunk_size", 900)
        if v >= size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
