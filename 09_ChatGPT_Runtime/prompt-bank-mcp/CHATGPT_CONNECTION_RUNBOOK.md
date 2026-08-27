# ChatGPT Runtime Connection Runbook

Implementation in this branch:

`MCP_SERVER = IMPLEMENTED`
`NATURAL_LANGUAGE_RETRIEVAL = IMPLEMENTED`
`SOURCE_FETCH = IMPLEMENTED`
`COMPARE = IMPLEMENTED`
`INTAKE_GATE = IMPLEMENTED`
`HEALTH_CHECK = IMPLEMENTED`
`LIVE_CHATGPT_CONNECTION = NOT_YET_PROVEN`

Final connection procedure:

1. Deploy `09_ChatGPT_Runtime/prompt-bank-mcp` to a service with stable public HTTPS.
2. Provide the current 554-record canonical JSONL to the service via `PROMPT_BANK_SOURCE_PATH` or an equivalent secure source adapter.
3. Keep `PROMPT_BANK_EXPECTED_COUNT=554` and `PROMPT_BANK_CORPUS_VERSION=v3.4` until the corpus is intentionally versioned again.
4. Verify `/healthz` returns `ok=true` and `actual_count=554`.
5. Verify `/mcp` using an MCP-compatible inspector/client.
6. In ChatGPT Developer Mode, add an App using the public HTTPS `/mcp` endpoint.
7. Refresh the App after changes to tool descriptors.
8. Exercise natural-language search, exact fetch, comparison and intake from ChatGPT.

Do not declare the system live before steps 4, 5 and 8 are evidenced.

Integrity rules:

- Source text is never silently rewritten.
- Similarity does not authorize merge or replacement.
- Intake does not claim persistence without a writable persistence adapter.
- Source-Canonical, Semantic-Validated, Runtime-Tested and Released remain independent states.
- Secrets never belong in the repository.

After connection, routine user operation should be natural language only; Prompt IDs, code, Python and API keys are not part of the normal user workflow.
