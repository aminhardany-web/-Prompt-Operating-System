# Portfolio Control — Canonical Operating Rule

Status: ACTIVE CONTROL
Effective: 2026-08-23

This is the single control point for portfolio findings that previously remained narrative audit observations.

## Canonical roles

| Asset | Canonical role | Rule |
|---|---|---|
| EPKOS | governance / durable knowledge boundary | no silent promotion; frozen decisions require evidence |
| PKEA | executable evidence-processing runtime | process sources, preserve traceability, require human validation |
| PROMPT-OS | prompt/workflow execution-assets layer | no production release without runtime evaluation |
| Prompt Bank | controlled prompt registry | registration is not validation; runtime evidence is required |
| chat-gpt-amin | Port & Maritime knowledge module | repository/runtime boundary remains explicit |
| RA-001 | frozen reference architecture | change only through controlled change |
| KD-003 / WP2 | strategic project + fact base | fact-base evidence precedes strategic claims |

## Portfolio state machine

Every project or knowledge asset must use exactly one operational state:

`ACTIVE → VALIDATING → PRODUCTION → FROZEN`

or `ACTIVE → BLOCKED` or `ACTIVE → ARCHIVE`.

`REGISTERED` is not a completion state. `FROZEN` is not allowed unless required evidence and validation gates pass.

## Evidence gate

A claim may be treated as validated only when all of the following exist:

1. canonical source identifier;
2. exact source location or line range where applicable;
3. provenance/hash for the source artifact;
4. validation result;
5. reviewer or deterministic gate record;
6. dependency/conflict status where applicable.

## Production gate

Production release is prohibited when runtime testing is zero, required CI checks are absent, or a baseline claims tests passed without an executable verification record.

## Anti-drift rules

- Do not create a second registry for an existing canonical registry.
- Do not create a second product for the same runtime responsibility.
- Do not expand architecture to compensate for missing evidence.
- Do not label a project `COMPLETE` because a README or baseline exists.
- Do not convert an audit finding into a claim of closure without new evidence.

## Controlled decisions

- PKEA is the executable front door for evidence processing.
- EPKOS remains the durable governance/canonicalization boundary.
- EPKBC is specification/compilation logic, not a competing product runtime.
- PROMPT-OS owns prompt/workflow assets; Prompt Bank owns reusable prompt records.
- RA-001 is frozen and is not an active redesign project.
- chat-gpt-amin is a bounded Port & Maritime module; universal ChatGPT loading is not claimed.

Project-specific closure evidence must be stored under `02_Operations/` or the project's canonical evidence repository and linked from the relevant baseline. Narrative status alone is insufficient.
