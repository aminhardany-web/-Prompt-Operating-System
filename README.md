# AI-Prompt-Operating-System

A controlled operating system for project knowledge, evidence, prompts and AI-assisted workflows.

## Operational product

The repository's primary executable product is **Project Knowledge & Evidence Agent (PKEA)**.

PKEA is the user-facing runtime that turns project sources into a traceable evidence package:

`Documents → Registry → Claims → Evidence → Conflicts → Dependencies → Gaps → Human Review → Audit Report`

Normal command:

```bash
python -m pkea.cli run ./sample_project --output ./workspace
```

The final operational baseline is documented in `06_Product_Project_Knowledge_Evidence_Agent/FINAL_OPERATIONAL_BASELINE.md`.

## System roles

- **EPKOS** — durable knowledge and governance boundary.
- **PROMPT-OS** — prompt/workflow execution-assets layer.
- **Prompt Bank** — controlled registry of reusable prompt assets inside PROMPT-OS.
- **REP** — research/execution discipline.
- **HVS-001** — output quality and evidence-traceability standard.
- **RA-001** — reference architecture for the Port Imam Khomeini transformation project.
- **PKEA** — executable evidence-processing runtime connecting these layers without merging their responsibilities.

## Repository structure

- **00_Governance** — constitutional and governance frameworks
- **01_Prompt_Library** — controlled prompt assets
- **02_Operations** — testing, evaluation and execution records
- **03_Knowledge_Recovery** — knowledge recovery systems
- **04_Projects** — project workspaces
- **05_Outputs** — generated outputs and deliverables
- **06_Product_Project_Knowledge_Evidence_Agent** — executable PKEA product
- **99_Archive** — historical material

## Evidence rule

Source material is the evidence authority. LLM output is advisory and must pass deterministic grounding checks. Human validation remains a required gate. PKEA does not silently promote findings into canonical EPKOS knowledge.

## Verification

The repository CI verifies unit tests, golden evaluation, Library-corpus evaluation and canonical production CLI execution for PKEA.
