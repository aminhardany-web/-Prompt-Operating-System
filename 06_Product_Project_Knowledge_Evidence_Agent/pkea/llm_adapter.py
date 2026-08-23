from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol


class ClaimExtractionAdapter(Protocol):
    def extract_claims(self, *, document_id: str, path: str, numbered_text: str) -> list[dict[str, Any]]: ...


SYSTEM_PROMPT = """You extract candidate project claims from source text.
Return only claims that are explicitly supported by the supplied source lines.
Allowed type values: decision, requirement, risk, action, claim.
Never invent evidence. line_start/line_end must point to the supplied numbered source lines and quote must be copied exactly from those lines.
These are CANDIDATE findings only; do not mark them validated or canonical."""

CLAIM_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "type": {"type": "string", "enum": ["decision", "requirement", "risk", "action", "claim"]},
                    "text": {"type": "string"},
                    "line_start": {"type": "integer", "minimum": 1},
                    "line_end": {"type": "integer", "minimum": 1},
                    "quote": {"type": "string"},
                },
                "required": ["type", "text", "line_start", "line_end", "quote"],
            },
        }
    },
    "required": ["claims"],
}

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


@dataclass
class OpenAIResponsesAdapter:
    api_key: str
    model: str = "gpt-5.6-luna"
    endpoint: str = "https://api.openai.com/v1/responses"
    timeout: int = 60
    max_retries: int = 2

    @classmethod
    def from_env(cls) -> "OpenAIResponsesAdapter":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required for the OpenAI adapter")
        return cls(
            api_key=key,
            model=os.getenv("PKEA_LLM_MODEL", "gpt-5.6-luna"),
            endpoint=os.getenv("OPENAI_RESPONSES_ENDPOINT", "https://api.openai.com/v1/responses"),
            timeout=int(os.getenv("PKEA_LLM_TIMEOUT", "60")),
            max_retries=int(os.getenv("PKEA_LLM_MAX_RETRIES", "2")),
        )

    def extract_claims(self, *, document_id: str, path: str, numbered_text: str) -> list[dict[str, Any]]:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Document ID: {document_id}\nPath: {path}\n\n{numbered_text}"},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "pkea_claim_extraction",
                    "strict": True,
                    "schema": CLAIM_SCHEMA,
                }
            },
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = json.loads(response.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = RuntimeError(f"OpenAI adapter request failed ({exc.code}): {detail}")
                if exc.code not in RETRYABLE_STATUS_CODES or attempt >= self.max_retries:
                    raise last_error from exc
                retry_after = exc.headers.get("Retry-After")
                try:
                    delay = min(float(retry_after), 30.0) if retry_after else 2.0 ** attempt
                except ValueError:
                    delay = 2.0 ** attempt
                time.sleep(max(0.0, delay))
            except urllib.error.URLError as exc:
                last_error = RuntimeError(f"OpenAI adapter connection failed: {exc.reason}")
                if attempt >= self.max_retries:
                    raise last_error from exc
                time.sleep(min(2.0 ** attempt, 10.0))
        else:
            raise last_error or RuntimeError("OpenAI adapter request failed without a response")

        output_text = raw.get("output_text")
        if not output_text:
            parts: list[str] = []
            for item in raw.get("output", []):
                for content in item.get("content", []):
                    if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                        parts.append(content.get("text", ""))
            output_text = "".join(parts)
        if not output_text:
            raise RuntimeError("OpenAI adapter returned no output_text")
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("OpenAI adapter returned non-JSON structured output") from exc
        claims = parsed.get("claims", [])
        if not isinstance(claims, list):
            raise RuntimeError("OpenAI adapter returned an invalid claims payload")
        return claims
