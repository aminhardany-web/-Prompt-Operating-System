# Prompt Bank / Prompt-OS Deep Execution Audit — 2026-08-27

## Executed scope
Accessible Library/EPKOS archive + Prompt Bank canonical corpus + Deep Structural Candidate corpus + Prompt-OS GitHub repository + current integration contracts.

## Corpus inspected
- Canonical source records: 530
- Structural candidates: 226
- Combined comparison set: 756

## Structural discovery rule
Discovery does not depend on the literal word “prompt”. It identifies reusable engineered instruction artifacts by role, mission, objective, context/input, workflow/decision rules, constraints, output contracts, activation/reuse signals and other behavioral structure. Ordinary chat requests remain excluded unless they form a reusable instruction contract.

## Reconciliation executed
The 226 candidates were compared against all 530 canonical records using character n-gram TF-IDF cosine similarity as an automated first-pass similarity control. This is a screening mechanism, not semantic proof.

Decision counts:
- Exact duplicate candidate ↔ canonical: 30
- High similarity review: 45
- Near duplicate review: 10
- Novel structural candidates requiring semantic classification: 141

## Similarity screening
- Candidate→canonical max similarity: 1.0
- Candidate→canonical mean similarity: 0.142562
- Candidate→canonical pairs ≥0.90: 121
- Candidate→canonical pairs ≥0.80: 167
- Candidate→canonical pairs ≥0.70: 223
- Combined-corpus near-similar pairs ≥0.70 recorded: 635

## Interpretation boundary
Exact similarity 1.0 is suitable for duplicate/occurrence reconciliation, but 0.70–0.99 is only evidence for review. No prompt is merged, replaced or declared “better” solely from a similarity score.

## Current operational truth
- SOURCE_CANONICAL remains immutable.
- Natural-language retrieval contract is defined.
- Automatic intake contract is defined.
- Prompt-vs-Note separation is defined.
- Structural discovery rules are explicitly recorded in the repository.
- 226-candidate reconciliation evidence has been generated.
- Semantic validation of all 530 is NOT completed.
- Runtime evaluation of all 530 is NOT completed.
- Therefore RELEASED/VERIFIED is not claimed.

## Host boundary
The repository contains an active ChatGPT invocation/integration specification, but it explicitly states that automatic loading into every ChatGPT project/page is environment-dependent and must not be falsely represented as native automatic loading.

## User behavior target
The user should be able to state a goal naturally and receive the strongest supported full prompt text. Prompt IDs are optional. When a new structured prompt is supplied in an enabled Prompt Bank context, intake should occur without requiring separate “register/index/archive” commands.
