# Prompt Bank — ChatGPT MCP Runtime

This directory is the real ChatGPT-facing control layer: a tool-only MCP App for natural-language Prompt Bank retrieval.

User examples:

- «بهترین پرامپت برای استخراج و جمع‌بندی کامل پروژه را پیدا کن.»
- «متن کامل بهترین پرامپت ممیزی قرارداد را بده.»
- «این دو پرامپت را مقایسه کن و بگو کدام بهتر است.»
- «این دستور را بررسی کن؛ اگر پرامپت جدید است برای ورود به بانک آماده‌اش کن.»

Tools:

- `search`: intent-first retrieval; the user does not need a Prompt ID or the word Prompt.
- `fetch`: exact source retrieval with verbatim preservation.
- `compare`: comparison for duplicate/variant/conflict analysis.
- `ingest_prompt`: intake gate for newly supplied structured instructions.
- `health`: corpus readiness check.

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
