# Robodebt Worked-Trace Reference Profile

Reference-profile version: `1.0-candidate`

Artifact hash: `79ef8f7c8ff7e9af4863a591afd80f38a563e609e3f9f0d655c2d156bd2318d1`

## Baseline arm

| Property | Status | Completeness | Diagnostics | Located transition | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F0 | `fail` | `complete` | `FM_EVIDENCE_TYPE_COLLAPSED` | B-04 | representation owner | interface and policy owner | surfacing may slow progression |
| F1 | `fail` | `complete` | `FM_ROBUST_PERMISSION_VIOLATION` | B-05 | permission-rule owner | gate owner | holding action delays disposition |
| F2 | `unassessable` | `incomplete` | `FM_REQUIRED_INPUT_MISSING` | paired intervention boundary | simulation owner | simulation owner | cohort spillovers are outside this one-case trace |
| F3 | `fail` | `complete` | `FM_REQUIRED_GATE_MISSING` | B-05 | process owner | review and gate owner | pre-action review consumes capacity |
| F4 | `fail` | `complete` | `FM_MATERIAL_ITEM_UNSURFACED` | B-04 | representation owner | interface owner | additional context may increase reviewer burden |
| F5 | `fail` | `complete` | `FM_RESTORATION_PARTIAL` | B-10 | reassessment owner | restoration owner | complete restoration may require broader remediation |

## Repair arm

| Property | Status | Completeness | Diagnostics | Located transition | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F0 | `pass` | `complete` | `none` | R-05 | evidence owner | information-service owner | evidence acquisition adds workload |
| F1 | `pass` | `complete` | `none` | R-06 | permission-rule owner | gate owner | supported disposition takes longer |
| F2 | `unassessable` | `incomplete` | `FM_REQUIRED_INPUT_MISSING` | paired intervention boundary | simulation owner | simulation owner | cohort spillovers are outside this one-case trace |
| F3 | `not_applicable` | `complete` | `none` | R-06 | process owner | policy owner | a different progression path could require review |
| F4 | `pass` | `complete` | `none` | R-05 | representation owner | interface owner | surfacing requires provenance maintenance |
| F5 | `not_applicable` | `complete` | `none` | R-07 | process owner | policy owner | avoidance is not evidence of restoration capability |

## Shared claim limit

bounded explanatory trace; not representative, historical calibration, legal conclusion, or attackability evidence
