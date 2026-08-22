# PKEA Integration Contract

PKEA is the product runtime, not a replacement for the two existing systems.

## EPKOS

EPKOS is the durable knowledge/governance system of record. PKEA may read EPKOS source registries, baselines and validation artifacts. PKEA must not silently promote its own candidates into an EPKOS frozen baseline.

Boundary:

`PKEA findings → human/validation gate → EPKOS canonicalization`

## PROMPT-OS

PROMPT-OS supplies reusable prompt/workflow assets and execution records. PKEA can invoke a registered extraction/evaluation workflow in later releases, but the MVP keeps deterministic extraction as the baseline so evidence behavior is testable without an LLM dependency.

Boundary:

`Project source → PKEA intake → optional PROMPT-OS workflow → evidence result → validation`

## Product principle

The two systems become layers of one lightweight AI Operating System:

`PROMPT-OS = execution assets`

`PKEA = project knowledge/evidence runtime`

`EPKOS = durable knowledge, governance and audit boundary`

The product must remain usable when either upstream system is unavailable; integrations are adapters, not hidden runtime dependencies.
