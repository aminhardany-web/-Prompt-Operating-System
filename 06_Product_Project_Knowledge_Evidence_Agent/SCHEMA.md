# PKEA Evidence Object Model v0.2

PKEA keeps five primary artifact families.

## Document

A source document is identified by a stable `document_id` derived from its relative path and content. The registry preserves format, SHA-256, size, line count and ingestion status.

## Claim

A claim is a candidate finding. It contains:

- `claim_id`
- `document_id`
- `type`
- `text`
- `subject`
- `polarity`
- `evidence.path`
- `evidence.line_start`
- `evidence.line_end`
- `evidence.quote`
- `validation_status`

A claim is not authoritative merely because it exists in `analysis.json`.

## Conflict

A conflict links claims with the same normalized subject but opposite polarity. Conflict status is `UNRESOLVED` until a human-controlled downstream process resolves it.

## Dependency

The MVP records `document → claim` support edges. Future releases can add claim → decision, requirement → risk, decision → action and project-level dependency types without changing the evidence contract.

## Validation event

Human review is an append-only JSONL event containing reviewer, decision, timestamp, claim ID and optional note. The original claim and source evidence are never rewritten by the review command.

## Authority boundary

`source → candidate → deterministic evidence validation → human review → EPKOS canonicalization`

The MVP deliberately stops before canonicalization. This prevents PKEA from becoming an uncontrolled second system of record.
