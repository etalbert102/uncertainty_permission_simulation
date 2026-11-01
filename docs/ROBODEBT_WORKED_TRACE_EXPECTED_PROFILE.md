# Robodebt Worked-Trace Withheld Expected Profile

Oracle version: `1.0-candidate`

Artifact hash: `8a37755cd17cbfccd38a51d266599cf38d9975a8d6a89b2302b69c2b6216ef43`

## Baseline arm

| Property | Status | Completeness | Diagnostic | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- |
| F0 | `fail` | `complete` | `IMPUTATION_PROVENANCE_SUPPRESSED` | representation owner | interface and policy owner | surfacing may slow progression |
| F1 | `fail` | `complete` | `ROBUST_PERMISSION_VIOLATION` | permission-rule owner | gate owner | holding action delays disposition |
| F2 | `unassessable` | `partial` | `INTERVENTION_SCOPE_INCOMPLETE` | simulation owner | simulation owner | cohort spillovers are outside this one-case trace |
| F3 | `fail` | `complete` | `EFFECTIVE_REVIEW_ABSENT` | process owner | review and gate owner | pre-action review consumes capacity |
| F4 | `fail` | `complete` | `MATERIAL_UNCERTAINTY_NOT_SURFACED` | representation owner | interface owner | additional context may increase reviewer burden |
| F5 | `fail` | `complete` | `RESTORATION_PARTIAL` | reassessment owner | restoration owner | complete restoration may require broader remediation |

## Repair arm

| Property | Status | Completeness | Diagnostic | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- |
| F0 | `pass` | `complete` | `EVIDENCE_STATUS_PRESERVED` | evidence owner | information-service owner | evidence acquisition adds workload |
| F1 | `pass` | `complete` | `PROGRESSION_WITHHELD_UNTIL_SUPPORTED` | permission-rule owner | gate owner | supported disposition takes longer |
| F2 | `unassessable` | `partial` | `INTERVENTION_SCOPE_INCOMPLETE` | simulation owner | simulation owner | cohort spillovers are outside this one-case trace |
| F3 | `not_applicable` | `complete` | `NO_PRE_ACTION_PROGRESSION_REQUIRING_REVIEW` | process owner | policy owner | a different progression path could require review |
| F4 | `pass` | `complete` | `ACTION_RELEVANT_EVIDENCE_SURFACED` | representation owner | interface owner | surfacing requires provenance maintenance |
| F5 | `not_applicable` | `complete` | `NO_ADVERSE_ACTION_OR_RESTORATION_DUE` | process owner | policy owner | avoidance is not evidence of restoration capability |

## Shared claim limit

bounded explanatory trace; not representative, historical calibration, legal conclusion, or attackability evidence
