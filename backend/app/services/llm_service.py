"""Groq wrapper. The LLM never touches the database; it only receives schema text."""
import re
from pathlib import Path

from groq import Groq

from app.core.config import settings
from app.schemas.schema_models import DatabaseSchema

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


class LLMService:
    def __init__(self) -> None:
        self._client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None

    def _chat(self, system: str, user: str) -> str:
        if not self._client:
            raise RuntimeError("GROQ_API_KEY is not configured")
        resp = self._client.chat.completions.create(
            model=settings.groq_model,
            temperature=0,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content.strip()

    def generate_sql(self, question: str, schema: DatabaseSchema) -> str:
        system = (PROMPTS / "nl_to_sql.txt").read_text().replace("{schema}", schema.to_prompt())
        raw = self._chat(system, question)
        return re.sub(r"^```(?:sql)?|```$", "", raw, flags=re.MULTILINE).strip()

    def summarize(self, sql: str, ir: dict) -> str:
        system = (PROMPTS / "sql_to_nl.txt").read_text()
        return self._chat(system, f"SQL:\n{sql}\n\nBreakdown:\n{ir}")


llm_service = LLMService()
