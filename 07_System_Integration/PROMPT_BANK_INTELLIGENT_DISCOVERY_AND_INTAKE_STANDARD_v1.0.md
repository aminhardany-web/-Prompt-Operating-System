# Prompt Bank — Intelligent Discovery & Intake Standard v1.0

Status: ACTIVE / CONTROLLED / SOURCE-PRESERVING
Purpose: define the mandatory discovery boundary for Prompt Bank. A prompt is identified by structure and operational function, not by the literal presence of the word «prompt».

## 1. Discovery principle
The system MUST search for engineered instruction-bearing artifacts, including:
- system-like instructions;
- role/persona definitions;
- missions/objectives;
- execution workflows and staged procedures;
- decision protocols;
- expert/advisor/council/team operating instructions;
- legal/advisory/research/writing/editing/audit/judging instructions;
- output contracts and schemas;
- reusable templates with behavioral instructions;
- task modules that define how the model must behave;
- composite or master instructions created through aggregation or iterative refinement.

The literal words «prompt», «پرامپت», «system prompt» or similar are neither necessary nor sufficient.

## 2. Exclusion principle
Do NOT register ordinary chat requests merely because they are imperative. Conversational requests are promoted only when they contain sufficient reusable operational structure, such as role + objective + rules/process + expected output, or a reusable behavioral contract.

## 3. Candidate classes
Every discovered artifact is classified as one of:
PROMPT
PROMPT_FRAGMENT
WORKFLOW_SPEC
GOVERNANCE_SPEC
ROLE_SPEC
NOTE
EVIDENCE
REPORT_OUTPUT
ORDINARY_REQUEST
OTHER

Classification must use the artifact's function and structure, not its title alone.

## 4. Deep discovery signals
Strong positive signals include combinations of:
role/persona, mission, objective, scope, inputs, outputs, constraints, rules, stages, decision logic, evaluation criteria, fallback behavior, examples, variables/placeholders, activation conditions, commands, reusable instructions, or explicit behavioral requirements.

## 5. Composite prompt discovery
If a prompt is assembled from several previous prompts, notes, decisions or framework files, discover the resulting structured artifact as a candidate and preserve links to all source components. Do not flatten away component lineage.

## 6. User and assistant authored artifacts
Both user-authored and assistant-authored instruction artifacts may be candidates. The source_role must remain explicit. An assistant-generated instruction becomes canonical only after evidence and classification gates; it is not treated as user-authored merely because it appears in a project.

## 7. Intake behavior
When a user supplies an engineered instruction artifact in a Prompt Bank context, the default action is automatic intake:
CAPTURE → EXACT SOURCE → HASH → PROVENANCE → CLASSIFY → DUPLICATE/NEAR-DUPLICATE → SAME-JOB/FAMILY → CONFLICT/VARIANT → REGISTER/CANDIDATE → VALIDATION QUEUE → INDEX

The user should not need separate commands for registration, indexing or archiving.

## 8. Historical recall
Discovery must cover all accessible corpus layers: conversation archive, project artifacts, Library, Prompt Bank datasets, Prompt-OS registries, EPKOS extraction corpus and related derived packages. No claim of universal recall is allowed where the host does not expose the underlying source.

## 9. Source preservation
SOURCE_CANONICAL is immutable. No discovery or optimization process may silently rewrite, summarize, normalize or merge source text.

## 10. Optimization separation
A historical source may receive a DERIVED_OPTIMIZED sibling containing improved clarity, scope, context boundaries, output contract, examples, uncertainty handling, variables and other improvements. The derivative MUST include parent Prompt ID, change record, rationale and evaluation status.

## 11. Similarity and conflict
The engine must distinguish exact duplicates from near duplicates, same-job variants, refinements, specializations, complements and conflicts. Similarity alone never authorizes merge or replacement.

## 12. Quality defects
The audit layer should flag, where evidenced:
- unclear task or success criteria;
- excessive scope / monolithic instructions;
- missing or ambiguous context boundary;
- vague output requirements;
- contradictory rules;
- excessive negative-only constraints;
- missing uncertainty/error handling;
- redundant repeated instructions;
- hidden dependency on prior chat context;
- unsupported claims or invented authority;
- conflict with parent/source/version;
- poor reuse due to hard-coded values that should be variables.

A defect flag is an audit result, not an automatic rejection.

## 13. Retrieval behavior
Natural-language retrieval is the preferred user interface. The user describes the desired result; the runtime searches by semantic job/goal, domain, title, category, keywords, provenance and lifecycle, then returns the best supported full text first.

## 14. Notes integration
Notes are first-class records but distinct from prompts. Notes can be linked to prompts, projects, evidence and decisions without being silently promoted to Prompt.

## 15. Release gates
Discovery, registration, source verification, semantic validation, runtime testing, regression and release are independent states. No higher state may be inferred from a lower state.
