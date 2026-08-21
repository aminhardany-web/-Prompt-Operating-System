# Project Knowledge & Evidence Agent (PKEA)

PKEA is the first executable product extracted from the lightweight AI Operating System connecting EPKOS and PROMPT-OS.

The product turns project sources into a traceable evidence package:

`Documents → Registry → Claims → Evidence → Conflicts → Dependencies → Gaps → Human Review → Audit Report`

## Product boundary

PKEA is an evidence-first runtime. It does not silently turn model output into authoritative knowledge.

- Deterministic extraction is the baseline and requires no API key.
- The optional LLM adapter expands semantic claim discovery.
- LLM candidates must cite exact source lines.
- A deterministic validator rejects fabricated or out-of-range evidence.
- Human decisions are recorded in an append-only validation ledger.
- PKEA never canonicalizes findings into EPKOS in the MVP.

## Current capabilities

1. Ingest Markdown, TXT, JSON and CSV project sources.
2. Build a stable document/source registry with SHA-256 content hashes.
3. Extract decisions, requirements, risks, actions and claims deterministically.
4. Optionally extract richer claims with an OpenAI Responses API adapter using structured JSON output.
5. Map every accepted claim to its exact source line range.
6. Detect simple cross-document polarity conflicts.
7. Build document → claim dependency edges.
8. Create evidence gaps for findings awaiting validation.
9. Record human validation decisions without rewriting the original evidence package.
10. Produce JSON and Markdown audit artifacts.
11. Run deterministic golden evaluation plus unit tests in CI.

## CLI

```bash
python -m pkea.cli ingest ./sample_project --output ./workspace
python -m pkea.cli analyze ./workspace
python -m pkea.cli analyze ./workspace --llm openai
python -m pkea.cli review ./workspace CLM-xxxxxxxxxxxx --decision VALIDATED --reviewer "reviewer-name"
python -m pkea.cli report ./workspace --output ./workspace/report.md
```

For the OpenAI adapter:

```bash
export OPENAI_API_KEY="..."
export PKEA_LLM_MODEL="gpt-5.6-luna"
```

The API key is read only from the environment and is never written to the project workspace.

## Safety boundary

`LLM extraction → exact-source validation → candidate evidence → human review → downstream canonicalization`

The LLM is not the evidence authority. Source text is.

## Evaluation

The golden project verifies document count, claim count, claim types, conflict detection, source traceability and the human-gate control. Unit tests additionally verify that fabricated LLM quotes are rejected and that the validation ledger is append-only.

## Current limitations

- PDF/DOCX extraction is not yet in the standard-library MVP.
- Connectors for SharePoint, Drive, Jira, ERP and email are deferred.
- Conflict resolution remains human-controlled.
- Autonomous execution and multi-agent orchestration are explicitly deferred until evidence quality is validated on real projects.

## Architecture position

EPKOS remains the durable, versioned knowledge/governance boundary. PROMPT-OS remains the prompt/workflow execution-assets layer. PKEA is the project knowledge/evidence runtime. Integrations remain adapters rather than hidden runtime dependencies.
