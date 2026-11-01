# Post-Simulation Procedure Comprehensibility Review

Status: required project-lead review after Slice 5 analysis and before Slice 6 completion

## Purpose and evidentiary boundary

This review asks whether the five-step process-red-team procedure is understandable and practically usable when read alongside the completed simulation and worked examples. It is performed by the project lead after the dynamic simulation and confirmatory analysis are complete.

The review is not independent validation, an inter-rater reliability study, evidence about human performance, or a test of the simulation's empirical validity. It cannot establish that a new practitioner will reproduce every classification. Its function is to identify unclear wording, missing instructions, unusable worksheets, and places where the article or repository fails to connect an assessment to its evidence and claim limit.

## Review control

| Field | Entry |
| --- | --- |
| Review date |  |
| Reviewer | project lead |
| Protocol version and hash |  |
| Confirmatory analysis receipt and hash |  |
| Evidence-packet version and hash |  |
| P0 review-input version |  |
| Robodebt worked-trace review-input version |  |
| Transfer-canary version |  |
| Prior familiarity with reference profiles | none / partial / substantial |
| Review conclusion | understandable / understandable with editorial fixes / semantic revision required |

Prior familiarity is a limitation to record, not a reason to invalidate this review.

## Staged review procedure

1. Read the main-text five-step method and `docs/PROCESS_RED_TEAM_PROTOCOL.md` without consulting the reference profiles.
2. Apply the procedure first to `docs/P0_PROCEDURE_REVIEW_PACKET.md`, then to `docs/ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md`, and finally to `docs/TRANSFER_CANARY.md`.
3. For each input, record the application level, evaluation state, property/helper status, completeness, located transition, evidence, diagnostics, missing information, owners, intervention, tradeoff, and claim limits.
4. Record every point where the next step, required input, vocabulary, output field, or claim boundary is unclear.
5. Consult `docs/P0_USABILITY_WALKTHROUGH.md`, `docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md`, and `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`; distinguish genuine procedural ambiguity from an ordinary classification disagreement.
6. Trace the main-text Robodebt example and each reported simulation claim to its stored evidence without relying on the precursor essay.
7. Classify every proposed correction as editorial or semantic and apply the change-control rule below.

## Comprehensibility checklist

Record `yes`, `no`, or `unclear`, with an artifact and section reference for every non-`yes` response.

| Question | Result | Evidence or issue |
| --- | --- | --- |
| Can the intended decision question and application level be selected without hidden author knowledge? |  |  |
| Are the minimum inputs and mandatory escalation rules explicit? |  |  |
| Is the distinction between `assessed` and `omitted_by_claim_limit` clear? |  |  |
| Are `pass`, `fail`, `unassessable`, and `not_applicable` distinguishable? |  |  |
| Can the first material evidence-to-action transition be located? |  |  |
| Can evidentiary support, simulated operational outcomes, and legal status be kept separate? |  |  |
| Can formal authority, functional permission, and operational action be kept separate? |  |  |
| Are diagnostic owner, intervention owner, and tradeoff recorded separately? |  |  |
| Does each worked-example row trace to a stored event, assessment, or diagnostic artifact? |  |  |
| Is it clear what the Robodebt example and simulation do not establish? |  |  |
| Can the procedure be summarized in the article without requiring repository access? |  |  |
| Can the repository materials be used without reading the 1,500-word precursor essay? |  |  |

## Issue and disposition log

| Issue ID | Artifact and location | What was unclear | Severity | Proposed correction | Editorial or semantic | Disposition | Rerun required |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | blocking / material / minor |  |  |  |  |

## Change-control rule

An editorial change may improve navigation, define an already-frozen term more plainly, add a cross-reference, or correct wording without changing application level, required input, status, completeness, diagnostic, property meaning, ownership, intervention logic, claim limit, scenario, metric, or result interpretation. Record and verify editorial changes, but they do not invalidate confirmatory artifacts.

A semantic change alters any frozen construct, classification rule, required input, protocol step, application mapping, intervention, scenario, metric, analysis, worked-trace selection rule, or supported conclusion. A semantic change requires a new protocol and freeze version, invalidation of affected confirmatory artifacts, rerunning the affected simulation or analysis, and repeating this review on the new evidence packet. It must not be disguised as editorial clarification.

## Completion decision

Slice 6 may complete only when:

- every blocking or material comprehensibility issue has a recorded disposition;
- all accepted editorial corrections are reflected in the protocol, article, and evidence packet;
- no unresolved issue prevents the project lead from following the five steps and tracing the examples to evidence;
- any semantic revision has followed the new-freeze and rerun rule; and
- the review conclusion and limitations are recorded without claiming independent validation.
