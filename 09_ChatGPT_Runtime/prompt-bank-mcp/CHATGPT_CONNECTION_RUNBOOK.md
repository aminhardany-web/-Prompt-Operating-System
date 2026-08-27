# ChatGPT Runtime Connection Runbook

## Current status

`MCP_SERVER_CODE`: IMPLEMENTED
`NATURAL_LANGUAGE_RETRIEVAL`: IMPLEMENTED
`SOURCE_FETCH`: IMPLEMENTED
`COMPARE`: IMPLEMENTED
`NEW_PROMPT_INTAKE`: IMPLEMENTED AS A READ-ONLY GATE
`CHATGPT_RUNTIME_CONNECTION`: NOT YET LIVE
`REASON`: the repository does not contain a public HTTPS deployment and the complete 554-record corpus is not stored in the repository.

## Required final connection path

1. Deploy this service to a host that provides stable public HTTPS.
2. Provide the 554-record Prompt Bank JSONL to the service through `PROMPT_BANK_SOURCE_PATH` or a secure equivalent.
3. Set `PROMPT_BANK_CORPUS_VERSION=v3.4` and `PROMPT_BANK_EXPECTED_COUNT=554` for the current Library corpus.
4. Verify `GET /healthz` returns `ok=true` and `actual_count=554`.
5. Verify `POST /mcp` with an MCP Inspector or equivalent client.
6. In ChatGPT Developer Mode, add the App using the public `/mcp` URL.
7. Refresh the App after descriptor changes.
8. Test natural-language retrieval, exact source fetch, comparison, and new-Prompt intake in ChatGPT.

## Safety and integrity controls

- The server does not rewrite stored source text.
- The server does not claim persistence for `ingest_prompt`; a writable persistence adapter is intentionally separate.
- Health checks fail when the loaded corpus count differs from the expected count.
- Production release of a Prompt remains separate from Source-Canonical registration and runtime evaluation.
- API keys must never be committed to Git or placed in Prompt Bank files.

## User-side burden

After the App is actually connected, normal use should require only natural-language requests. The user should not need Prompt IDs for discovery and should not need to manage Python, GitHub, or API keys for routine retrieval.
