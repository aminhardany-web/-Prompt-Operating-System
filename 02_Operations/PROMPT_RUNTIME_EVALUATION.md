# Prompt Runtime Evaluation Gate

Status: ACTIVE — PRODUCTION RELEASE BLOCKED UNTIL EVALUATED
Effective: 2026-08-23

A prompt record is not considered tested merely because it is registered, canonical, deduplicated, or source-traceable.

## Required evidence per tested prompt

1. Exact prompt text and stable Prompt ID.
2. Test input or fixture.
3. Expected behavioral criteria.
4. Actual output.
5. Pass/fail decision.
6. Evaluator and date.
7. Version/commit reference.
8. Regression status when the prompt changes.

## Release rule

A prompt may enter `05_Tested_Prompts` only after a recorded runtime evaluation passes. Missing runtime evidence means `UNTESTED`, not `PASS`.

Bulk registration must never be used as a substitute for runtime evaluation.
