# Plan Completion Receipt

Date: 2026-10-31

Status: execution-ready study plan; simulation and research results not yet implemented

## Completion Boundary

This receipt closes planning, not the study. The repository now specifies the formal model, generic configuration boundary, Robodebt application boundary, dynamic experiment, validation sequence, pilot decisions, confirmatory freeze, analysis, evidence packet, and 10,000-word manuscript. Slices 1–6 must still be executed. No simulation, pilot, confirmatory result, or empirical manuscript claim is certified here.

## Planning Requirements and Evidence

| Requirement | Canonical evidence | Closure test |
| --- | --- | --- |
| Standalone research contribution and 10,000-word contract | `docs/STUDY_PLAN.md`, `docs/ARTICLE_OUTLINE.md` | 9,400-word core plus 600-word contingency; full conducted study required |
| Formal constructs and proposition boundaries | `docs/FORMAL_MODEL.md`, `docs/PRECURSOR_FIDELITY_FIXTURE.md` | F0–F5, three headline propositions, scope exclusions, and no-change falsifier specified |
| Case-neutral execution architecture | `docs/CONFIGURATION_COMPILATION.md`, `data/model/schema_manifest_v1.yaml` | only a validated compiled configuration executes; every runtime slot has exactly one owner |
| Documented institutional application | `docs/ROBODEBT_CASE_STUDY.md`, `data/sources/robodebt/` | dated early/enhanced profiles, three-axis validity, no silent historical defaults |
| Dynamic simulation and analysis design | `docs/STUDY_PLAN.md`, `docs/PREREGISTRATION.md` | policies, factors, estimands, controls, horizon, keyed pairing, precision, and extension rule specified |
| Practical process-red-team output | `docs/PROCESS_RED_TEAM_PROTOCOL.md`, blinded packets, withheld profiles, QA receipt | application levels, closed statuses, escalation, non-composite report, and independent QA gate specified |
| Execution order and ownership | Work Slices 0–7 and file/mutation contract in `docs/STUDY_PLAN.md` | each slice has purpose, owned outputs, forbidden work, commands, done conditions, and commit rule |
| Failure handling and runtime feasibility | Execution Protocol and Verification Tiers in `docs/STUDY_PLAN.md` | stable diagnostic envelope, escalation order, measured runtime ceilings, and stop rule specified |
| External and future dependencies | `docs/DEFERRED.md` | nine items have an owner, risk, next action, and due gate |
| Final study completion standard | 39-question Final Completion Audit in `docs/STUDY_PLAN.md` | every answer must cite stored evidence before the study is declared complete |

## Decisions Left to Execution, Not to Implementer Discretion

The pilot must measure and freeze cohort size, final replication bounds within the stated cap, MCSE targets, scenario validity, censoring treatment, and the confirmatory runtime ceiling. These are controlled empirical decisions with predeclared inputs and decision rules, not missing plan choices. The project lead must close the baseline commit and environment receipt before Slice 1 mutation, and must close independent reader QA, invitation verification, literature chaining, and source-byte identity at their registered pre-freeze gates.

An implementer may choose ordinary internal code structure only where it does not alter schemas, fact ownership, event semantics, random-stream allocation, formal properties, estimands, diagnostics, or frozen outputs. Any semantic change requires a ledger entry and rerun of the owning gate.

## Verification

The plan-completeness command is:

```bash
python3 scripts/validate_plan.py
```

The source-and-specification command is:

```bash
python3 scripts/validate_slice0.py
```

Both must pass before Slice 1 begins and after any edit to the canonical plan, preregistration, architecture, source/application boundary, protocol, deferred register, or execution controls.

Expected plan receipt:

```text
PLAN_VALID slices=8 primary_hypotheses=3 policies=5 audit_questions=39 deferred_items=9 word_ceiling=10000
```

## Entry Decision

Slice 1 may begin after both validators pass and `D-009` records the approved baseline commit and environment receipt. Independent reader QA may run in parallel, but protocol `1.0` and Slice 4 remain blocked until the required locked reader returns and all other pre-freeze dependencies are closed. Exact Robodebt population calibration is neither required nor permitted as a silent prerequisite for the generic kernel.
