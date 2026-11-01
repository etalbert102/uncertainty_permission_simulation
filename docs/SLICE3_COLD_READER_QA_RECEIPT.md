# Slice 3 Cold-Reader QA Receipt

Status: blank pre-freeze artifact-QA template; not a completed reader record

Do not record names, contact details, demographics, or free-form personal observations. This exercise evaluates the protocol artifacts, not reader performance.

## Run control

| Field | Entry |
| --- | --- |
| QA run ID |  |
| Reader ID |  |
| Oracle custodian ID |  |
| Protocol version/hash |  |
| Robodebt packet version/hash |  |
| Transfer packet version/hash |  |
| Robodebt oracle version/hash |  |
| Transfer oracle version/hash |  |
| Distribution timestamp |  |
| Locked return timestamp |  |
| Comparison timestamp |  |
| Reader did not draft protocol or packets | yes / no |
| Packet-only distribution confirmed | yes / no |
| Pre-return oracle or repository exposure | none / possible / confirmed |
| Blind-run validity | valid / invalid-practice-only |
| Invalidity reason |  |

Possible or confirmed pre-return exposure makes the run `invalid-practice-only`.

## Row-level comparison

Enter one row for every expected property/helper or claim-limit receipt in both packets.

| Packet | Arm/claim | Application level | Evaluation state | Property/helper | Status | Completeness | Located transition | Evidence | Diagnostic | Missing information/claim limit | Diagnostic owner | Intervention owner | Tradeoff | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Robodebt / Transfer |  |  |  |  |  |  |  |  |  |  |  |  |  | exact / acceptable-variant / mismatch / omitted |

An acceptable variant preserves formal status, completeness, mechanism, ownership, required escalation, tradeoff, and claim boundary. Wording similarity is insufficient.

## Error-class summary

| Error class | Robodebt count | Transfer count | Blocking ambiguity? | Notes |
| --- | ---: | ---: | --- | --- |
| Wrong application level or evaluation state |  |  |  |  |
| Wrong status or completeness |  |  |  |  |
| Missing sufficient failure |  |  |  |  |
| Unsupported certainty/pass |  |  |  |  |
| Incorrect `not_applicable` |  |  |  |  |
| Located-transition or diagnostic mismatch |  |  |  |  |
| Diagnostic/intervention owner conflation |  |  |  |  |
| Tradeoff omitted |  |  |  |  |
| Prohibited claim made |  |  |  |  |
| Required row omitted |  |  |  |  |

## Revision decision

- Reader-reported ambiguity:
- Oracle-custodian comparison:
- Protocol, packet, schema, or vocabulary implicated:
- Revision required before freeze: yes / no
- Semantic or display-only revision:
- New-reader rerun required: yes / no
- Change-log entry:

Semantic changes require a version increment and a new-reader rerun. Display-only changes may retain evidence only when they cannot change classification, diagnosis, ownership, escalation, tradeoff, or claim boundary.
