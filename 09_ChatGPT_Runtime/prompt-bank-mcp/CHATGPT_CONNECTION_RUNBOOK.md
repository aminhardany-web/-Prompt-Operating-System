# ChatGPT Runtime Connection Runbook

Current implementation state:

- MCP server code: IMPLEMENTED
- Natural-language retrieval: IMPLEMENTED
- Exact source fetch: IMPLEMENTED
- Comparison: IMPLEMENTED
- New-Prompt intake gate: IMPLEMENTED
- Health verification: IMPLEMENTED
- Live ChatGPT connection: NOT YET PROVEN

To make the connection real:

1. Deploy this service to a host with stable public HTTPS.
2. Give the service the current 554-record Prompt Bank JSONL through `PROMPT_BANK_SOURCE_PATH` or an equivalent secure source adapter.
3. Set `PROMPT_BANK_CORPUS_VERSION=v3.4` and `PROMPT_BANK_EXPECTED_COUNT=554`.
4. Confirm `/healthz` returns `ok=true` and `actual_count=554`.
5. Confirm the `/mcp` endpoint with an MCP-compatible inspector/client.
6. In ChatGPT Developer Mode, add an App using the public HTTPS `/mcp` URL.
7. Refresh the App after server descriptor changes.
8. Test natural-language search, exact fetch, compare, and Prompt intake from ChatGPT.

Integrity controls:

- Source text is never silently rewritten.
- Intake does not claim persistence without a writable store confirmation.
- Health fails closed when corpus count differs from the configured expectation.
- Source-Canonical, Semantic-Validated, Runtime-Tested, and Released remain separate states.
- Secrets must remain outside the repository.

After the App is genuinely connected, routine user interaction should require only natural-language requests. The user should not need to know Prompt IDs, code, Python, GitHub, or API keys.
