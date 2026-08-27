# Prompt Bank — Discovery Rule Set v1.0

STATUS: ACTIVE / CONTROLLED

## Core decision
A reusable engineered instruction is a Prompt candidate regardless of whether its source text contains the word «prompt».

## Positive evidence
Consider an artifact Prompt-like when it contains a meaningful combination of:
1. role/persona or explicit model behavior;
2. mission/task/objective;
3. scoped context or inputs;
4. ordered procedure/workflow or decision rules;
5. constraints/guardrails;
6. expected output structure, format or acceptance criteria;
7. reuse/activation language, variables or placeholders.

The strongest candidates are those with at least three independent structural families and a coherent reusable purpose.

## Candidate boundaries
The system must also consider as discovery candidates:
- legal/advisory instructions;
- research/review instructions;
- book author/editor instructions;
- audit/judging instructions;
- consultant/advisor/council/team instructions;
- extraction/recovery instructions;
- project operating protocols;
- writing/translation/localization standards;
- templates that prescribe AI behavior;
- assistant-authored prompt architectures and master protocols.

## Exclusions
Do not promote:
- ordinary one-off questions;
- simple conversational requests;
- factual lookup requests without reusable behavior;
- narrative reports or completed outputs;
- notes that contain no executable instruction contract.

An excluded artifact may still be stored as NOTE/EVIDENCE and linked to a Prompt.

## Required handling of compound artifacts
When a large artifact contains both a Prompt and supporting knowledge, preserve the full source artifact and register the executable Prompt boundary separately with a source span/locator. Never discard context that is necessary to reproduce the source faithfully.

## Required handling of assistant-authored artifacts
Assistant-generated instruction text is a valid discovery candidate. Its source role remains ASSISTANT. It may become canonical only through the same evidence and quality gates as any other source.

## Similarity decision ladder
EXACT_DUPLICATE → NEAR_DUPLICATE → SAME_JOB → SPECIALIZATION → REFINEMENT → COMPLEMENT → CONFLICT → INDEPENDENT

No merge is allowed from similarity score alone.

## User-facing default
The operator can state a goal in natural language. The retrieval layer must search by job/goal and return the strongest supported full prompt text first. Metadata can follow.

## Automatic intake
When a new structured instruction appears within an enabled Prompt Bank context, the expected system behavior is automatic capture, hashing, provenance, classification, duplicate/similarity check, registration and validation queueing. Separate user commands such as «ثبت کن» should not be required for the normal intake path.

## Truth rule
A discovery result is not automatically validated, tested, optimized or released. Statuses are independent and evidence-backed.
