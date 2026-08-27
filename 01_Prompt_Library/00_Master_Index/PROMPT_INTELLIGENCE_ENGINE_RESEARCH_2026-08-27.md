# Prompt Intelligence Engine — Deep Research & Implementation Baseline

Date: 2026-08-27
Status: RESEARCH-COMPLETE / IMPLEMENTATION-NOT-YET-VERIFIED
Branch: research/prompt-intelligence-2026-08-27

## 1. Verified starting state

The current Prompt Bank baseline is ACTIVE / CONTROLLED / RETRIEVAL-READY, with 530 canonical records, 509 legacy exact-source records, 21 structural promotions, 205 discovery candidates outside canonical, zero exact canonical duplicate hashes, zero runtime-tested canonical records, and zero fully semantic-validated canonical records. Production release remains NOT AUTHORIZED. Historical recall remains OPEN.

Source: PROMPT_BANK_OPERATIONAL_BASELINE_v3.2 and PROMPT_BANK_MASTER_MANIFEST_v3.1.

## 2. Objective

Extend the existing bank without replacing its governance model so that the system can:

1. detect exact and near duplicates;
2. detect same-job / same-goal prompts even when wording differs;
3. identify structural and semantic defects;
4. compare competing prompts for the same job;
5. select a best current candidate without rewriting source text;
6. generate derived optimized variants with explicit lineage;
7. evaluate prompts against task-specific test cases;
8. prevent regression before a derived prompt is released;
9. continuously ingest new prompts through the same controls.

## 3. Required decision pipeline

NEW_OR_RECALLED_PROMPT
→ SOURCE_CAPTURE
→ EXACT_HASH_CHECK
→ STRUCTURAL_FINGERPRINT
→ NEAR_DUPLICATE_CANDIDATES
→ SAME_JOB_CLUSTERING
→ SEMANTIC_REVIEW
→ DEFECT_SCAN
→ QUALITY_SCORE
→ RUNTIME_EVAL
→ REGRESSION_EVAL
→ VERSION_RANKING
→ RELEASE_DECISION

No stage may silently overwrite SOURCE_CANONICAL.

## 4. Similarity controls

Similarity must be multi-layered rather than keyword-only:

A. Exact identity: normalized-safe hash comparison while preserving the immutable original text.
B. Structural similarity: role/context/task/constraints/process/output-schema fingerprints.
C. Lexical similarity: token/phrase overlap for fast candidate generation.
D. Semantic similarity: model-assisted comparison of job-to-be-done, intended behavior, constraints and output contract.
E. Functional equivalence: whether two prompts are expected to produce materially interchangeable results for the same task.

Similarity must never by itself authorize merging. A similar prompt can be a specialized variant, a better version, a complementary prompt, or an independent prompt.

## 5. Defect detection

The defect scanner should test at minimum:

- ambiguous objective;
- missing role/context where required;
- missing inputs/placeholders;
- contradictory instructions;
- impossible or unverifiable requirements;
- missing output contract;
- missing decision rules;
- missing evidence/verification requirements for evidence-sensitive tasks;
- excessive or redundant instructions;
- hidden dependency on unavailable context;
- unsafe or disallowed operational assumptions;
- claims of certainty unsupported by evidence;
- prompt injection / instruction-conflict exposure when external content is consumed;
- evaluation criteria that cannot actually be measured.

A defect finding is an observation, not an automatic rejection. Severity must be recorded.

## 6. Quality model

A prompt quality score should not be a single opaque number. Record component scores and evidence:

- Task clarity
- Input completeness
- Constraint precision
- Process executability
- Output contract quality
- Evidence / verification controls
- Failure handling
- Reusability
- Maintainability
- Runtime effectiveness
- Regression stability

A release score must be task-specific. Runtime performance cannot be inferred from textual quality alone.

## 7. OpenAI evaluation alignment

OpenAI's current API supports Evals with datasets and testing criteria, and graders including string checks, text similarity, Python graders, model-based score graders, label graders, and multi-graders. This supports a layered evaluation architecture rather than relying on subjective review alone.

Recommended mapping:

- deterministic structural checks → Python grader / local validator;
- exact expected output where appropriate → string check;
- similarity-oriented tasks → text similarity grader;
- qualitative quality dimensions → score-model grader;
- categorical failure modes → label-model grader;
- composite release score → multi-grader.

Official OpenAI references reviewed on 2026-08-27:
- Evals API reference
- Graders API reference
- API quickstart

The external API must be treated as an evaluation service, not as the authority for source provenance or canonical text.

## 8. Best-version selection

For each same-job cluster, produce a ranked comparison:

1. task fit;
2. evidence integrity;
3. output-contract completeness;
4. defect severity;
5. runtime score;
6. regression score;
7. maintainability;
8. specialization fit.

Possible decisions:

KEEP_CANONICAL
KEEP_AS_SPECIALIZED
PREFER_AS_BEST_CURRENT
DERIVE_OPTIMIZED
KEEP_BOTH_COMPLEMENTARY
REJECT_FOR_USE
NEEDS_HUMAN_REVIEW

No automatic REPLACE decision is permitted solely from semantic similarity.

## 9. Continuous intake

Every new prompt should enter the same intake pipeline automatically when the source surface is accessible. User-facing retrieval should remain simple: the user can ask for the best prompt for a goal, while the engine performs discovery, comparison, validation and ranking behind the scenes.

The system must distinguish:

- source registration;
- quality validation;
- runtime validation;
- release status.

Registration never implies verification.

## 10. Current implementation gap

The repository already defines retrieval, provenance, lifecycle, recall and optimization controls, but the audited baseline explicitly reports zero runtime-tested canonical prompts and zero fully semantic-validated canonical prompts. Therefore this research document does NOT claim that the 530 canonical records have now been semantically or runtime validated.

The 205 discovery candidates and the open historical recall queue remain upstream work for the intelligence layer.

## 11. Execution order

P0 — reconcile and classify the 205 discovery candidates.
P1 — close accessible historical recall gaps.
P2 — build deterministic structural/defect scanner and near-duplicate candidate generator.
P3 — create representative evaluation sets by prompt job family.
P4 — connect OpenAI Evals/graders for semantic and runtime assessment.
P5 — run evaluations on prioritized high-value clusters first.
P6 — establish regression baselines.
P7 — enable best-version ranking and controlled derived optimization.
P8 — enable continuous intake and release gating.

## 12. Evidence rule

Until execution artifacts exist, status must remain:

DESIGNED / IMPLEMENTATION-PENDING / TEST-PENDING

and never:

VERIFIED / RELEASED / PRODUCTION-READY.

## 13. Research conclusion

The correct next step is not another architecture rewrite. The repository has enough governance structure to add a Prompt Intelligence and Evaluation layer. The missing proof is execution: candidate clustering, semantic comparison, defect detection, runtime evaluation, regression and release evidence.
