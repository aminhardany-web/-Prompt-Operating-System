# Prompt Bank — ChatGPT MCP Runtime

This directory is the real ChatGPT-facing control layer: a tool-only MCP App for natural-language Prompt Bank retrieval.

User examples:

- «بهترین پرامپت برای استخراج و جمع‌بندی کامل پروژه را پیدا کن.»
- «متن کامل بهترین پرامپت ممیزی قرارداد را بده.»
- «این دو پرامپت را مقایسه کن و بگو کدام بهتر است.»
- «این دستور را بررسی کن؛ اگر پرامپت جدید است برای ورود به بانک آماده‌اش کن.»

Tools:

- `search`: field-aware retrieval across title/source/record metadata; returns a suggested operational action (`USE_SOURCE`, `AUDIT_SOURCE`, `DERIVE_OPTIMIZED`, or `TEST_PROMPT`). It is a retrieval aid, not proof of semantic equivalence.
- `fetch`: exact source retrieval with verbatim preservation.
- `compare`: comparison for duplicate/variant/conflict analysis.
- `ingest_prompt`: intake gate for newly supplied structured instructions.
- `health`: corpus readiness check.
- `toolbox`: recommend a reusable Prompt Bank item and the next operational action from a natural-language need, without changing the canonical corpus.

The runtime expects a deployed copy of the current canonical JSONL corpus. The repository currently contains the control-plane code and governance, while the 554-record source corpus remains in the ChatGPT Library workflow. Configure `PROMPT_BANK_SOURCE_PATH` at deployment time.

Defaults: `PROMPT_BANK_CORPUS_VERSION=v3.4`, `PROMPT_BANK_EXPECTED_COUNT=554`, `PORT=3000`.

Run locally:

```bash
npm install
npm run check
npm start
```

Endpoints:

`/mcp` — MCP Streamable HTTP endpoint
`/healthz` — corpus health check

For ChatGPT Developer Mode, the `/mcp` endpoint must be reachable over public HTTPS. No OpenAI API key is required for normal user interaction with the ChatGPT App.

The App is not considered LIVE until a deployed `/healthz` reports the expected corpus and a real ChatGPT call succeeds. This boundary is intentional.
