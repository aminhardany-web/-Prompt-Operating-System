# MASTER AUDIT EXECUTION PROTOCOL v1.0

## Purpose
Single operational protocol for reconstructing current project state from primary sources, reconciling historical reports, classifying evidence, and preventing contradictory current-state reports.

## Non-negotiable controls
- Do not treat historical reports as Evidence.
- Do not treat Chat memory or summaries as Sources of Record.
- Do not equate registration with validation.
- Do not equate source linkage with claim verification.
- Do not infer completeness from absence of errors.
- Do not declare CLOSED, ZERO-GAP, FREEZE READY, or PRODUCTION READY without direct evidence.
- Preserve historical versions; separate them from active state.
- Do not redesign frozen architecture.
- When evidence is insufficient, record OPEN or NOT_VERIFIABLE.

## Source precedence
1. Primary/source artifact
2. Frozen baseline/specification
3. Official registry
4. Decision/audit record
5. Historical AI-generated report
6. Memory/summary

## Required execution chain
Source Inventory → Scope Declaration → Claim Extraction → Conflict Detection → Primary-Source Resolution → Evidence Classification → Version/Lineage Check → Dependency Check → Validation Gates → Canonical Current State → User Operating Decision.

## Evidence statuses
VERIFIED | REGISTERED_UNVALIDATED | OPEN | REJECTED | SUPERSEDED | NOT_VERIFIABLE

## Required audit gates
V-001 Registry Integrity
V-002 Canonical Integrity
V-003 Freeze Boundary
V-004 Authority Chain
V-005 Traceability Closure
V-006 Dependency Integrity
V-007 Source Coverage
V-008 Evidence Coverage
V-009 Version Consistency
V-010 Unsupported Claim Detection

## Special rule for corpus counts
Historical counts such as “2,380 evidence records” or “2,264 source-linked records” are not promoted to current validated counts unless the underlying records are directly accessible, enumerated, and dispositioned.

## Final output contract
Produce only:
1. CANONICAL_CURRENT_STATE
2. CLAIM_EVIDENCE_DISPOSITION
3. CONFLICT_REGISTER
4. VALIDATION_AUDIT_RESULT
5. USER_OPERATING_DECISION

## Current limitation rule
If the primary corpus is not accessible in the execution environment, do not simulate full closure. Record the missing corpus as NOT_VERIFIABLE and continue auditing every source that is actually accessible.
