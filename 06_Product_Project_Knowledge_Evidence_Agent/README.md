# Project Knowledge & Evidence Agent (PKEA)

PKEA is the first executable product extracted from the lightweight AI Operating System connecting EPKOS and PROMPT-OS.

The product turns project sources into a traceable evidence package:

`Documents → Registry → Claims → Evidence → Conflicts → Dependencies → Gaps → Human Review → Audit Report`

## One-command mode

The normal entry point is now one command:

```bash
python -m pkea.cli run ./sample_project --output ./workspace
```

That single command performs, in order:

`Ingest → Immutable Snapshot → Registry → Claim Extraction → Evidence Validation → Conflict Detection → Dependency Mapping → Evidence Gap Register → Audit Report → Run Summary`

For optional LLM-assisted semantic extraction:

```bash
python -m pkea.cli run ./sample_project --output ./workspace --llm openai
```

The command stops on an execution error rather than silently producing a partial success. Results are written to `document_registry.json`, `analysis.json`, `report.md`, and `run_summary.json`.

## Product boundary

PKEA is an evidence-first runtime. It does not silently turn model output into authoritative knowledge.

- Deterministic extraction is the baseline and requires no API key.
- The optional LLM adapter expands semantic claim discovery.
- LLM candidates must cite exact source lines and pass deterministic grounding checks.
- Human decisions are recorded in an append-only validation ledger.
- PKEA never canonicalizes findings into EPKOS in the MVP.

## Current capabilities

1. Ingest Markdown, TXT, JSON, CSV and DOCX project sources.
2. Build a stable document/source registry with SHA-256 content hashes.
3. Create immutable ingestion snapshots before analysis.
4. Extract decisions, requirements, risks, actions and claims deterministically.
5. Optionally extract richer claims with an OpenAI Responses API adapter using structured JSON output.
6. Map every accepted claim to its exact source line range.
7. Detect simple cross-document polarity conflicts.
8. Build document → claim dependency edges.
9. Create evidence gaps for findings awaiting validation.
10. Record human validation decisions without rewriting the original evidence package.
11. Produce JSON and Markdown audit artifacts.
12. Run deterministic golden evaluation plus Library-corpus evaluation in CI.

## Manual subcommands

```bash
python -m pkea.cli ingest ./sample_project --output ./workspace
python -m pkea.cli analyze ./workspace
python -m pkea.cli analyze ./workspace --llm openai
python -m pkea.cli review ./workspace CLM-xxxxxxxxxxxx --decision VALIDATED --reviewer "reviewer-name"
python -m pkea.cli report ./workspace --output ./workspace/report.md
```

## Safety boundary

`LLM extraction → exact-source validation → candidate evidence → human review → downstream canonicalization`

The LLM is not the evidence authority. Source text is.

## Current limitations

- PDF extraction is not yet in the standard-library MVP.
- Connectors for SharePoint, Drive, Jira, ERP and email are deferred.
- Conflict resolution remains human-controlled.
- Autonomous execution and multi-agent orchestration are explicitly deferred until evidence quality is validated on real projects.
- The Library corpus is imported through a controlled manifest; imported sources do not become canonical automatically.

## Architecture position

EPKOS remains the durable, versioned knowledge/governance boundary. PROMPT-OS remains the prompt/workflow execution-assets layer. PKEA is the project knowledge/evidence runtime. Integrations remain adapters rather than hidden runtime dependencies.
