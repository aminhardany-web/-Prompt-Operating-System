# Prompt Runtime Gate

Status: ACTIVE CONTROL
Effective: 2026-08-23

Prompt Bank registration is an inventory operation, not a production authorization.

## Required states

`REGISTERED → STRUCTURAL_VALIDATED → RUNTIME_TESTED → PRODUCTION`

A prompt may move to `PRODUCTION` only when:

- the exact canonical prompt text is preserved;
- source/message traceability is present;
- input/output contract is defined;
- at least one deterministic runtime test exists;
- expected behavior and failure behavior are recorded;
- the test result is reproducible in CI or an attached execution record;
- no unresolved critical defect remains.

## Batch policy

Existing Prompt Bank records must not be silently marked production merely because they are canonical. Untested records remain `REGISTERED` or `STRUCTURAL_VALIDATED`.

Runtime evaluation should be performed in batches and recorded under `02_Operations/prompt_runtime/`. Each record must contain prompt ID, test case, input fixture, expected criteria, observed result, verdict, timestamp, model/runtime identifier, and source trace.

## Release rule

`Runtime Test = 0` means `Production Release = NOT AUTHORIZED`.

This gate exists to close the previous gap between prompt registration and demonstrated behavior without generating new prompt variants merely to increase inventory.
