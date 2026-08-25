# Unified Repository Integration — Adapter Contract

## Purpose

Provide one controlled interoperability contract for repositories that remain separate from the primary PKEA runtime.

## Required adapter outputs

Every adapter must emit a deterministic record containing:

- repository
- source_ref
- source_path
- source_sha256
- extraction_status
- evidence_status
- authority_status
- dependency_refs
- conflict_refs
- last_validated_at

## Processing order

`SOURCE DISCOVERY → IMMUTABLE EXTRACTION → REGISTRATION → EVIDENCE MAPPING → DEPENDENCY MAPPING → VALIDATION → PKEA → HUMAN REVIEW → EPKOS`

## Fail-closed rules

1. Missing source evidence means `NOT_PROVEN`.
2. Missing SHA-256 means `NOT_REGISTERED`.
3. Unresolved authority means `NOT_AUTHORITATIVE`.
4. Unresolved conflicts block canonicalization.
5. Integration never overwrites the source repository.
6. Integration never deletes a repository.
7. A link or registry entry alone is not evidence of integration.

## Current boundary decisions

- `-Prompt-Operating-System`: active PKEA runtime and integration hub.
- `EPKOS-Final-`: governance/knowledge boundary; adapter required.
- `AI-Prompt-OS`: prompt asset boundary; adapter required.
- `data`: preserved data source; extraction and adapter required.
- `chat-gpt-amin`, `001-HUM-INT-`, `OmniRoute`: remain isolated until their adapters produce evidence-backed records.
- Empty or incomplete repositories are not deleted during integration; they remain explicit workstreams until evidence establishes redundancy.

## Completion criterion

The portfolio is not considered fully integrated until every non-primary repository is either:

`INTEGRATED` with evidence, or `EXPLICITLY_ISOLATED` with a documented reason.
