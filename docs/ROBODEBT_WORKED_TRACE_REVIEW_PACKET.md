# Robodebt Worked-Trace Procedure-Review Input

Packet version: `1.0-candidate`

On the first pass, use only this input and the supplied protocol. Consult the reference profile after recording ambiguities.
This is a bounded explanatory trace, not a historical reconstruction or legal conclusion.

Specification: `RB-WORKED-TRACE-001`
Held-input hash: `48bc136d227538bc3ed1e932f7f8047b136a2abb5affe49b0e29fecf52282f37`

## Baseline arm (`U1`)

| Day | Event | Relevant details |
| ---: | --- | --- |
| 0 | `SOURCE_EVIDENCE_INGESTED` | amount=3000; evidence_type=annual_aggregate; provenance=observed_aggregate |
| 0 | `NOTICE_FAILED` | status=not_received_before_deadline |
| 21 | `DEADLINE_REACHED` | deadline_basis=documented_early_profile_21_day_clock |
| 22 | `REPRESENTATION_APPLIED` | inferential_status=imputed; transformation=aggregate_evenly_apportioned_across_periods; uncertainty_surfaced=False |
| 22 | `PROGRESSION_EXECUTED` | action=modeled_debt_assertion; formal_authority_claim=source_attributed_only_not_decided_by_simulation; functional_permission=True; period_specific_support=False |
| 25 | `EXTERNAL_CONSEQUENCE_STARTED` | action=modeled_recovery_exposure |
| 40 | `EVIDENCE_SUBMITTED` | evidence_type=period_specific_records; provenance=stylized_later_recipient_evidence |
| 45 | `REASSESSMENT_COMPLETED` | decision=modeled_debt_reduced_or_zeroed |
| 45 | `CORRECTION_EXECUTED` | decision_state=baseline; recovery_state=baseline |
| 60 | `RESTORATION_EVALUATED` | residual_external_consequence=True; restoration_status=partial |

Apply the protocol and record F0–F5 separately. Do not produce a composite score.

## Repair arm (`U3`)

| Day | Event | Relevant details |
| ---: | --- | --- |
| 0 | `SOURCE_EVIDENCE_INGESTED` | amount=3000; evidence_type=annual_aggregate; provenance=observed_aggregate |
| 0 | `ACCESS_PROBLEM_RECORDED` | notice_received_before_deadline=False |
| 1 | `PROGRESSION_HELD` | reason=period_specific_support_missing |
| 1 | `EVIDENCE_REQUESTED` | evidence_type=period_specific_records; owner=agency |
| 10 | `EXTERNAL_EVIDENCE_RETURNED` | provenance=stylized_third_party_record; retrieval_success=True |
| 15 | `SUPPORTED_DISPOSITION_RECORDED` | action=no_unsupported_progression; period_specific_support=True |
| 15 | `CASE_CLOSED` | external_consequence_started=False |

Apply the protocol and record F0–F5 separately. Do not produce a composite score.

## Required claim boundary

Record application level, evaluation state, status, completeness, located transition, evidence, diagnostic, missing information, diagnostic owner, intervention owner, tradeoff, ambiguity, and claim limit for every row.
Do not infer historical prevalence, legal validity, or adversarial exploitability.
