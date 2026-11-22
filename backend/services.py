"""Groq LLM integration and prompt templating."""
from __future__ import annotations

from typing import List

from .config import Settings
from .rag_pipeline import RetrievedChunk

SYSTEM_PROMPT = (
    "You are the official NewGen Tech Knowledge Assistant. Answer the user's question "
    "strictly using the provided context. If the answer cannot be found in the context, "
    "state clearly that the information is not available in company records. "
    "Never hallucinate or use external general knowledge. "
    "Be concise and precise, and reference sources by their bracketed number, e.g. [1]."
)

NOT_FOUND_MESSAGE = "This information is not available in company records."


def format_context(chunks: List[RetrievedChunk]) -> str:
    return "\n\n".join(
        f"[{i}] Source: {c.source}" + (f" | Section: {c.section}" if c.section else "") + f"\n{c.text}"
        for i, c in enumerate(chunks, start=1)
    )


def build_messages(question: str, chunks: List[RetrievedChunk]) -> list[dict]:
    user = f"Context:\n{format_context(chunks)}\n\nQuestion: {question}\n\nAnswer using only the context above."
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}]


class GroqService:
    def __init__(self, settings: Settings, client=None):
        self.settings = settings
        self._client = client

    @property
    def client(self):
        if self._client is None:
            if not self.settings.groq_api_key:
                raise RuntimeError("GROQ_API_KEY is not configured. Set it in .env.")
            from groq import Groq

            self._client = Groq(api_key=self.settings.groq_api_key)
        return self._client

    def answer(self, question: str, chunks: List[RetrievedChunk]) -> str:
        # Strict grounding: with no relevant context the LLM is never called.
        if not chunks:
            return NOT_FOUND_MESSAGE
        resp = self.client.chat.completions.create(
            model=self.settings.groq_model,
            messages=build_messages(question, chunks),
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
        )
        return (resp.choices[0].message.content or "").strip() or NOT_FOUND_MESSAGE
