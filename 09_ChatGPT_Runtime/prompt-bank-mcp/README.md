# Prompt Bank — ChatGPT MCP Runtime

Tool-only ChatGPT App runtime for the Prompt Bank. The user experience is natural-language retrieval; Prompt IDs, GitHub, Python, and API keys are implementation details.

## Tools

`search` finds Prompt Bank records by goal, task, role, topic, wording, or natural-language need. It does not require the user to say "prompt".

`fetch` returns the exact stored source record and preserves the source text verbatim.

`compare` compares multiple records for exact duplication, variants, lineage and status differences. Topic similarity alone is not treated as duplication.

`ingest_prompt` is the intake gate for a newly supplied structured instruction. It detects exact duplicates and likely related items. Persistence is deliberately not claimed by this read-only adapter.

`health` verifies that the expected corpus is actually loaded.

## Source integrity

The deployed runtime must have a readable copy of the current canonical JSONL corpus. The repository currently stores the governance and runtime code, while the full 554-record source corpus remains maintained in the ChatGPT Library workflow. Configure `PROMPT_BANK_SOURCE_PATH` to a deployed corpus copy.

Defaults:

- `PROMPT_BANK_CORPUS_VERSION=v3.4`
- `PROMPT_BANK_EXPECTED_COUNT=554`
- `PORT=3000`

## Run

```bash
npm install
npm run check
npm start
```

MCP endpoint: `/mcp`
Health endpoint: `/healthz`

## ChatGPT connection

The MCP endpoint must be available over public HTTPS. In ChatGPT Developer Mode, add the App using the public `/mcp` URL and refresh the App after descriptor changes.

## Important boundary

This code makes the ChatGPT-facing MCP layer real, but it does not by itself make the App live inside ChatGPT. A public HTTPS deployment and access to the 554-record corpus are still required. No claim of a live ChatGPT connection should be made until `/healthz` is verified and a real ChatGPT tool call succeeds.
