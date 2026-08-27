# Prompt Bank — ChatGPT MCP Runtime

This is the first real ChatGPT-facing runtime layer for Prompt Bank. It is a **tool-only** MCP App: no custom widget is required for the core user flow.

## User experience

The model can call the tools from natural language. Users do not need to know Prompt IDs.

Examples:

- "Find the best prompt for extracting and summarizing a whole project."
- "Show me the full source text for PB-0554."
- "Compare PB-0100 and PB-0200 and tell me whether they are duplicates or variants."
- "I have a new structured instruction. Check whether it belongs in Prompt Bank."

## Tools

- `search`: natural-language retrieval across the configured Prompt corpus.
- `fetch`: exact source retrieval by Prompt ID; source text is returned verbatim.
- `compare`: exact-text and status/lineage comparison for a set of Prompt IDs.
- `ingest_prompt`: intake gate for a new user-supplied Prompt; it detects exact duplicates and likely related items but does not falsely claim persistence.
- `health`: verifies corpus reachability and expected record count.

## Source of truth

The runtime is deliberately source-preserving. The deployed service must be given a readable copy of the current Prompt Bank corpus through `PROMPT_BANK_SOURCE_PATH` or a deployment-specific adapter. It must not treat repository documentation as a substitute for the Prompt text corpus.

Required environment values:

- `PROMPT_BANK_SOURCE_PATH`: filesystem path to the canonical JSONL corpus.
- `PROMPT_BANK_CORPUS_VERSION`: expected corpus version, default `v3.4`.
- `PROMPT_BANK_EXPECTED_COUNT`: expected number of records, default `554`.
- `PORT`: HTTP port, default `3000`.

## Local run

```bash
npm install
npm run check
npm start
```

The MCP endpoint is:

`http://localhost:3000/mcp`

Health check:

`http://localhost:3000/healthz`

For a real ChatGPT connection the MCP endpoint must be exposed over public HTTPS. In ChatGPT Developer Mode, add an App using the public `/mcp` URL. Refresh the App after tool descriptor changes.

## Important limitation

This repository currently does **not** contain the complete 554-record Prompt corpus. The canonical corpus is maintained in ChatGPT Library in the existing project workflow. Therefore the runtime code is connected to a configurable corpus adapter, but the full ChatGPT retrieval loop is not honestly declared live until a deployed service has access to the 554-record corpus and ChatGPT can reach its HTTPS `/mcp` endpoint.

No OpenAI API key is required for ordinary ChatGPT users invoking this App. A separate OpenAI API key is only needed for programmatic batch evaluation outside normal ChatGPT App usage.
