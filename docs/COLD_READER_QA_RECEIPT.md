# Cold-Reader QA Receipt Template

Status: blank artifact-QA template; not a completed reader record

Do not record names, contact details, demographic information, or free-form personal observations. Use a study-local pseudonymous reader ID. This receipt evaluates the protocol artifact, not human performance.

## Run Control

| Field | Entry |
| --- | --- |
| QA run ID |  |
| Reader ID |  |
| Oracle custodian ID |  |
| Protocol version/hash |  |
| P0 packet version/hash |  |
| Transfer packet version/hash |  |
| P0 oracle version/hash |  |
| Transfer oracle version/hash |  |
| Packet distribution timestamp |  |
| Locked return timestamp |  |
| Comparison timestamp |  |
| Reader did not draft protocol or packets | yes / no |
| Packet-only distribution confirmed | yes / no |
| Oracle or expected-output exposure before return | none / possible / confirmed |
| Blind-run validity | valid / invalid-practice-only |
| Invalidity reason, if any |  |

Any possible or confirmed pre-return exposure makes the run `invalid-practice-only`. Do not repair validity through reader attestation after exposure.

## Reader Deliverables Received

| Artifact | Received | Complete enough to compare | Notes |
| --- | --- | --- | --- |
| P0 scope receipt |  |  |  |
| P0 assessment profile |  |  |  |
| P0 conclusion and ambiguity log |  |  |  |
| Transfer scope receipt |  |  |  |
| Transfer assessment profile |  |  |  |
| Transfer conclusion and ambiguity log |  |  |  |

## Row-Level Comparison

Create one row for every expected assessment or claim-limit receipt in each packet.

| Packet | Property/helper or claim | Application/evaluation state | Status | Completeness | Located transition | Diagnostic/justification | Claim limit | Diagnostic owner | Intervention owner | Tradeoff | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0 |  |  |  |  |  |  |  |  |  |  | exact / acceptable-variant / mismatch / omitted |
| Transfer |  |  |  |  |  |  |  |  |  |  | exact / acceptable-variant / mismatch / omitted |

An acceptable variant must preserve the same formal status, completeness, mechanism, claim boundary, and required escalation. Wording similarity alone is not sufficient.

## Error-Class Summary

| Error class | P0 count | Transfer count | Blocking ambiguity? | Notes |
| --- | ---: | ---: | --- | --- |
| Wrong application level |  |  |  |  |
| Assessment confused with `omitted_by_claim_limit` |  |  |  |  |
| Wrong status |  |  |  |  |
| Wrong completeness |  |  |  |  |
| Missing sufficient failure |  |  |  |  |
| Unsupported certainty or pass |  |  |  |  |
| Incorrect `not_applicable` |  |  |  |  |
| Diagnostic mismatch |  |  |  |  |
| Located-transition mismatch |  |  |  |  |
| Diagnostic/intervention owner conflation |  |  |  |  |
| Tradeoff omitted |  |  |  |  |
| Prohibited claim made |  |  |  |  |
| Required row omitted |  |  |  |  |

## Ambiguity and Revision Decision

- Reader-reported ambiguities:
- Oracle-custodian comparison notes:
- Protocol wording implicated:
- Packet wording implicated:
- Schema or diagnostic vocabulary implicated:
- Revision required before freeze: yes / no
- Semantic or display-only revision:
- New-reader rerun required: yes / no
- Change-log entry:

Semantic changes always require a new protocol or packet version and a rerun with new readers. Display-only corrections may retain the reader evidence only when they cannot change classification, diagnostic choice, ownership, escalation, or claim boundary; document the rationale.
