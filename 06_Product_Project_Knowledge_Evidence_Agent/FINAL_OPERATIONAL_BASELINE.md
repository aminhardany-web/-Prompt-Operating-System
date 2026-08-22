# PKEA — Final Operational Baseline v1.0

Status: FROZEN OPERATIONAL BASELINE
Date: 2026-08-22

## 1. Purpose

Project Knowledge & Evidence Agent (PKEA) is the executable product layer of the user's lightweight AI Operating System. Its job is to turn project source material into a traceable evidence package that can be reviewed and audited.

PKEA is the operational front door. The user should not need to understand EPKOS, PROMPT-OS, REP, HVS-001 or RA-001 in order to use the product.

## 2. User contract

The user supplies a project folder or supported source file.

The normal operation is:

`python -m pkea.cli run <project-source> --output <workspace>`

The product produces:

- `document_registry.json` — what was ingested and its SHA-256 identity.
- `analysis.json` — claims, evidence, conflicts, dependencies, gaps and controls.
- `report.md` — human-readable audit report.
- `run_summary.json` — execution summary.
- `source_snapshots/` — immutable analysis inputs created at ingestion.

## 3. Integrated system roles

EPKOS is the durable knowledge and governance boundary. It remains the authority boundary and is not silently modified by PKEA.

PROMPT-OS is the prompt and workflow execution-assets layer. Prompt Bank remains its controlled registry of reusable prompt assets.

REP governs research/execution discipline when a research workflow is performed.

HVS-001 governs the quality and traceability expectations for substantive written outputs.

RA-001 remains the reference architecture for the Port Imam Khomeini transformation project and is consumed as project context rather than being redefined by PKEA.

PKEA is the runtime that operates on project evidence. It connects the above layers operationally without merging their responsibilities.

## 4. Evidence authority

Source material is authoritative evidence. Model output is never authoritative merely because a model produced it.

Deterministic extraction is the baseline. Optional LLM extraction is advisory and must pass exact-source grounding validation before a candidate claim is accepted.

Every accepted claim must retain an exact source path and line range.

Human validation is a gate, not an optional cosmetic step.

PKEA does not canonicalize findings into EPKOS in the MVP/baseline.

## 5. Operating flow

`Source → Immutable Snapshot → Registry → Claims → Evidence Validation → Conflicts → Dependencies → Gaps → Human Review → Audit Report`

This is the single operational flow. Additional architecture is not required for normal use.

## 6. Deliberate exclusions

The baseline does not silently add PDF parsing, enterprise connectors, autonomous multi-agent execution, automatic conflict resolution, or automatic promotion into canonical knowledge.

These exclusions are intentional safety and scope controls, not missing documentation tasks.

## 7. Definition of done for the baseline

The baseline is considered operational when the repository CI passes its deterministic unit tests, golden evaluation, Library-corpus evaluation, and canonical production CLI execution. The CI workflow is the executable verification record.

A successful run is not equivalent to saying that all project claims are true. It means that the evidence-processing pipeline completed and preserved the required controls.

## 8. Product principle

Do not optimize for more architecture.

Optimize for fewer user actions, stronger evidence traceability, reproducible execution, and useful project outputs.

The product is successful only when it reduces search, repetition and unsupported conclusions in real project work.
