# ChatGPT Runtime Connection Runbook

## Current source authority — revalidated 2026-09-29

The current authoritative Prompt Bank source is:

`/02_PROMPT_BANK/00_CURRENT_CONTROL/01_CANONICAL/PROMPT_BANK_CANONICAL_SOURCE_v3.4.jsonl`

Current companion index:

`/02_PROMPT_BANK/00_CURRENT_CONTROL/01_CANONICAL/PROMPT_BANK_MASTER_INDEX_v3.4.csv`

Current evaluation/runtime gate:

`/02_PROMPT_BANK/00_CURRENT_CONTROL/02_EVALUATION/PROMPT_EVALUATION_RUNTIME_GATE_v3.5.md`

Authority meaning:

- **v3.4 / 554 records** = immutable Source-Canonical corpus.
- **v3.5** = evaluation/runtime gate for the v3.4 corpus; it is not a replacement corpus.
- The runtime server code in this directory is **implementation v0.1.0**. It is not itself the source corpus.
- Deployment must mount/copy the exact current v3.4 source into `PROMPT_BANK_SOURCE_PATH`; changing the runtime location must not create a second source of truth.

Current implementation state:

`MCP_SERVER = IMPLEMENTED`
`NATURAL_LANGUAGE_RETRIEVAL = IMPLEMENTED`
`SOURCE_FETCH = IMPLEMENTED`
`COMPARE = IMPLEMENTED`
`INTAKE_GATE = IMPLEMENTED`
`HEALTH_CHECK = IMPLEMENTED`
`LIVE_CHATGPT_CONNECTION = NOT_YET_PROVEN`

Important retrieval boundary:

The existing runtime server in `src/server.ts` uses its current lexical search implementation. A separate repaired Retrieval v4 implementation was not found as executable runtime code on the current `main` branch during the 2026-09-29 source-first recheck. Therefore Retrieval v4 must not be described as already connected to this MCP server.

## Connection procedure

1. Deploy `09_ChatGPT_Runtime/prompt-bank-mcp` to a service with stable public HTTPS.
2. Provide the exact current v3.4 canonical JSONL to the service via `PROMPT_BANK_SOURCE_PATH` or an equivalent secure source adapter.
3. Keep `PROMPT_BANK_EXPECTED_COUNT=554` and `PROMPT_BANK_CORPUS_VERSION=v3.4` until the source corpus is intentionally versioned again.
4. Verify `/healthz` returns `ok=true` and `actual_count=554`.
5. Verify `/mcp` using an MCP-compatible inspector/client.
6. In ChatGPT Developer Mode, add an App using the public HTTPS `/mcp` endpoint.
7. Refresh the App after changes to tool descriptors.
8. Exercise natural-language search, exact fetch, comparison and intake from ChatGPT.

Do not declare the system live before steps 4, 5 and 8 are evidenced.

## Integrity rules

- Source text is never silently rewritten.
- Similarity does not authorize merge or replacement.
- Intake does not claim persistence without a writable persistence adapter.
- Source-Canonical, Semantic-Validated, Runtime-Tested and Released remain independent states.
- Secrets never belong in the repository.
- Historical/superseded Prompt Bank generations remain lineage artifacts and are not substitutes for v3.4.
- Discovery candidates are not promoted without independent validation.
- A retrieval abstention is not proof that no related asset exists elsewhere in the authorized project/library/archive scope.

After connection, routine user operation should be natural language only; Prompt IDs, code, Python and API keys are not part of the normal user workflow.
