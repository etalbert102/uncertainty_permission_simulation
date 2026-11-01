# Reference Profile: Vendor Production-Access Summary

Status: draft reference-profile version `0.1`; consult after the first-pass review

Protocol version: `1.0`

The project lead consults this profile only after recording the first-pass assessment and ambiguities. Prior familiarity is recorded as a limitation but does not invalidate the review.

## Expected Receipt

| Field | Expected entry |
| --- | --- |
| Application level | B: bounded deterministic trace |
| Evaluation unit | Controlled summary-transformation pair |
| Held inputs | Source bundle, summary-stage input, routing rule, process, reviewer resource, clock, and zero random draws |
| Varied inputs | Summary transformation and emitted representation |
| Strongest supported finding | Suppressing a material conflicting restriction changes routing and automatic production-access permission. |
| Non-claims | F1/F2 result, completed review, decision service, capacity effects, contestability, restoration, empirical prevalence, legality, and attackability |

## Expected Assessment Profile

| Property/helper | Conflict-preserving summary | Fluent compressed summary | Required diagnostic or justification |
| --- | --- | --- | --- |
| F0 | `pass/complete` | `fail/complete` | Compressed: `FM_EVIDENCE_TYPE_COLLAPSED`, `FM_LINEAGE_INCOMPLETE`, `FM_POLICY_NOT_INSPECTABLE` |
| F1 | `not_applicable/complete` | `not_applicable/complete` | Frozen scope exclusion: source evidence and summary-stage input do not vary. |
| F2 | `not_applicable/complete` | `not_applicable/complete` | Frozen scope exclusion: no execute-versus-hold intervention. |
| F3 | `unassessable/incomplete` | `not_applicable/complete` | Preserve: `FM_REVIEW_UNRECORDED`; compressed: resolved false antecedent because progression is automatic rather than post-review. |
| F4 | `pass/complete` | `fail/complete` | Compressed: `FM_MATERIAL_ITEM_UNSURFACED` |
| F5 | `unassessable/incomplete` | `unassessable/incomplete` | Both: `FM_APPLICABILITY_UNDETERMINED` |
| GateSafe | `pass/complete` | `not_applicable/complete` | Compressed: resolved false antecedent because no gate is configured; the required missing gate is diagnosed separately. |
| ReviewEffective | `unassessable/incomplete` | `fail/complete` | Preserve: `FM_REVIEW_UNRECORDED`; compressed: `FM_REQUIRED_GATE_MISSING`, `FM_REVIEW_EVIDENCE_MISSING` |
| DecisionServiceEffective | `unassessable/incomplete` | `unassessable/incomplete` | Both: `FM_REQUIRED_INPUT_MISSING` because no service deadline or supported final disposition is supplied. |

The capacity/service boundary uses `evaluation_state = omitted_by_claim_limit` and receives no formal status because Level B cannot support the intended system-capacity estimate. The missing service horizon keeps `DecisionServiceEffective` in scope but `unassessable`; the two conditions must not be conflated.

## Expected Located Transition

The first material failure is `TC-SUMMARY-COMPRESS`: it turns scoped, disputed, source-linked statements into a broad fluent sentence that hides the production restriction and contradictory scan before the shared routing rule executes.

## Expected Interventions and Ownership

| Mechanism | Intervention | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- |
| Evidence-state and scope collapse | Require field-level scope, evidence-state, and source references in summaries consumed by routing. | summary transformation | AI/workflow product owner | More complex summary and validation surface |
| Material conflict unsurfaced | Make unresolved production restrictions a required structured routing field. | evidence/representation contract | security-policy and workflow owners | More cases enter security review |
| Missing gate and review | Enforce a fail-closed production-provisioning dependency until independent verification and recorded authorization. | access workflow | identity-access and security-review owners | Slower provisioning and additional reviewer load |

## Canary Interpretation

Agreement with this profile supports vocabulary-independent application of the protocol to a synthetic contemporary-AI workflow. It does not establish that deployed LLM systems commonly behave this way, that the canary is an empirical case, or that the protocol improves human performance.
