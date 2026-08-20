# Project Knowledge & Evidence Agent (PKEA)

PKEA is the first executable product extracted from the AI Operating System layer connecting EPKOS and PROMPT-OS.

The MVP turns project documents into a traceable evidence package:

`Documents → Registry → Claims → Evidence → Conflicts → Dependencies → Gaps → Report`

## Design boundary

- Evidence-first. No unsupported claim is promoted to canonical knowledge.
- Deterministic by default. No model/API key is required for the baseline pipeline.
- Human approval is required before a finding becomes authoritative project knowledge.
- Every document and extracted claim receives a stable content hash.
- Historical inputs are preserved; supersession is explicit.

## MVP capabilities

1. Ingest Markdown, TXT, JSON and CSV files.
2. Build a document/source registry.
3. Extract candidate claims, decisions, requirements, risks and actions using deterministic rules.
4. Map claims to their source document and source line range.
5. Detect simple cross-document conflicts for normalized claim subjects.
6. Build lightweight document/claim dependency edges.
7. Detect evidence gaps and unsupported candidates.
8. Produce a machine-readable JSON audit package and a human-readable Markdown report.

## Run

```bash
python -m pkea.cli ingest ./sample_project --output ./workspace
python -m pkea.cli analyze ./workspace
python -m pkea.cli report ./workspace --output ./workspace/report.md
```

The implementation intentionally uses only the Python standard library in the MVP.

## Architecture position

EPKOS remains the durable, versioned knowledge/governance layer. PROMPT-OS remains the prompt/workflow execution layer. PKEA is the product runtime that consumes project sources and produces evidence-backed project knowledge artifacts.
