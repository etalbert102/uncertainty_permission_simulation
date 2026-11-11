# P0 Protocol Walkthrough and Expected Profile

Status: draft post-assessment reference and practitioner-facing walkthrough; expected-output projection only

Review order: complete a first pass using `docs/P0_PROCEDURE_REVIEW_PACKET.md` before consulting this walkthrough

Protocol version: `1.0`

Formal fixture: `docs/PRECURSOR_FIDELITY_FIXTURE.md`

## Purpose and Boundary

This walkthrough shows how the process-red-team protocol turns a controlled representation comparison into an inspectable diagnostic profile. It serves as an internal reference profile, not a required human-review return or usability evaluation. It is not an executed trace, a historical Robodebt case, an F1 evidence-refinement test, an F2 system-intervention test, or evidence of prevalence or attackability.

The executable stored-record bundle and canonical hashes remain Slice 1 deliverables. Until then, the IDs and expected classifications below are an oracle projection from the fixture specification, not generated results.

## Application Receipt

| Field | Value |
| --- | --- |
| Evaluation unit | Controlled pair of deterministic trace specifications |
| Application level | B: bounded deterministic trace |
| Core comparison | `P0-E-PRESERVE` versus `P0-E-FALLBACK` |
| Unit held fixed | Case `P0-C1`, model output `P0-M1`, policy, downstream rule `P0-D-ENABLE`, process, resources, clock, baseline, and zero random draws |
| Intended variation | Representation transformation and the representation it emits |
| Claim sought | Whether suppressing a policy-relevant alternative changes routing, scrutiny, and automatic functional permission |
| Prohibited claims | F1 or F2 result; completed review; contestability; restoration; prevalence; historical causation; legality; strategic exploitation |

## Controlled Inputs

The model output contains material alternatives and confidence below the declared fallback threshold. Both arms receive the same output.

| Arm | Transformation | Downstream-visible representation |
| --- | --- | --- |
| Preserve | `P0-Preserve` | Typed alternatives, confidence, provenance, and uncertainty remain visible. |
| Fallback | `P0-Fallback` | The same output is reduced to a broad untyped fallback value that suppresses the material alternative. |

No evidence state, underlying case, model output, policy, decision rule, process state, resource, clock, or random draw changes between arms.

## End-to-End Chain

### Preserve arm

1. `P0-M1` enters `P0-Preserve`.
2. The representation retains the material alternative and its uncertainty.
3. `P0-D-ENABLE` routes the case to `enhanced_scrutiny`.
4. The disposition enables the information action and review operation but does not place the routine progression action in `P_auto_progress`.
5. A fail-closed gate is configured. `GateSafe` is `pass/complete`; review completion is not modeled, so `ReviewEffective` is `unassessable/incomplete`.
6. F0 and F4 pass. F1 and F2 are outside fixture scope. F3 remains unassessable because completed review and execution are absent. F5 is unassessable because obligation scope and horizons are not declared.

### Fallback arm

1. The identical `P0-M1` enters `P0-Fallback`.
2. The representation emits the broad fallback without typed claim lineage or the material alternative.
3. The identical `P0-D-ENABLE` rule routes the case to `routine`.
4. The routine progression action enters `P_auto_progress`; no information action or configured review gate remains.
5. `GateSafe` is `not_applicable` because no gate is configured. The independently required review evidence is absent, so `ReviewEffective` is `fail/complete` rather than silently disappearing.
6. F0 and F4 fail. F1 and F2 remain outside scope, F3 is not applicable because the action is not post-review progression, and F5 remains unassessable.

## Expected Diagnostic Profile

| Step | Property/helper or receipt | Preserve | Fallback | Required diagnostic or justification | Located transition | Intervention and tradeoff |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F0 | `pass/complete` | `fail/complete` | Fallback: `FM_EVIDENCE_TYPE_COLLAPSED`, `FM_LINEAGE_INCOMPLETE`, `FM_POLICY_NOT_INSPECTABLE` | `P0-Fallback` emits an untyped value without the claim-level lineage and inspectability required downstream. | Preserve typed provenance and uncertainty. Increases interface and review information. |
| 1 | F4 | `pass/complete` | `fail/complete` | Fallback: `FM_MATERIAL_ITEM_UNSURFACED` | The material alternative reaches an authorized route only in the preserve arm. | Surface the required meaning before routing. May increase scrutiny volume. |
| 2 | F1 | `not_applicable/complete` | `not_applicable/complete` | Frozen scope exclusion; no failure diagnostic | Evidence and model output are held fixed; this is not an evidence-refinement comparison. | Run a separate certified evidence-refinement fixture before claiming F1. |
| 2 | F2 | `not_applicable/complete` | `not_applicable/complete` | Frozen scope exclusion; no failure diagnostic | The fixture does not compare an added fallback action with an explicit hold over a complete intervention unit. | Run a valid execute-versus-hold pair before claiming F2. |
| 3 | GateSafe | `pass/complete` | `not_applicable/complete` | Fallback: resolved false antecedent because no gate is configured | Preserve configures a fail-closed gate; fallback configures no gate. | Bind material uncertainty to a required fail-closed gate. May delay routine resolution. |
| 3 | ReviewEffective | `unassessable/incomplete` | `fail/complete` | Preserve: `FM_REVIEW_UNRECORDED`; fallback: `FM_REQUIRED_GATE_MISSING`, `FM_REVIEW_EVIDENCE_MISSING` | Preserve lacks modeled completion; fallback definitively lacks required review evidence and dependency. | Complete the review trace; preserve evidence and enforced dependency. Requires review capacity. |
| 3 | F3 | `unassessable/incomplete` | `not_applicable/complete` | Preserve: `FM_REVIEW_UNRECORDED`; fallback: resolved false antecedent | Preserve has post-review progression but no completed review or execution; fallback is automatic progression. | Add execution and authorization records before evaluating preserve-arm F3. |
| 3 | DecisionServiceEffective | `unassessable/incomplete` | `unassessable/incomplete` | Both: `FM_REQUIRED_INPUT_MISSING` because no service deadline or supported final disposition is supplied | P0 cannot establish timely supported decision service. | Extend the bounded trace with a declared service horizon. |
| 4 | Application-level claim-limit receipt | no assessment | no assessment | Level B does not contain a queue-load or service-capacity experiment | P0 cannot locate or estimate a capacity boundary. | Escalate to Level C for capacity or spillover conclusions. |
| 5 | F5 | `unassessable/incomplete` | `unassessable/incomplete` | Both: `FM_APPLICABILITY_UNDETERMINED` | Obligation scope, contestability path, horizons, consequences, and baseline are not declared. | Add a separate contestability/restoration trace. Expands data and modeling burden. |

There is no overall status. The profile establishes a representation-induced routing and permission change, identifies F0 and F4 failures in the fallback arm, and preserves all non-applicable and unassessable boundaries.

## Practitioner-Facing Report Projection

The practitioner report should render the stored assessment graph approximately as follows. This projection is deliberately compact and is not a substitute for the future canonical record bundle.

```yaml
protocol_version: "1.0"
application_level: bounded_deterministic_trace
evaluation_unit: controlled_pair
comparison_id: P0-E-PRESERVE__P0-E-FALLBACK
held_bundle:
  case_id: P0-C1
  model_output_id: P0-M1
  decision_rule_id: P0-D-ENABLE
  random_draw_count: 0
varied:
  - transformation
  - representation
assessment_profile:
  preserve:
    F0: {status: pass, completeness: complete}
    F1: {status: not_applicable, completeness: complete}
    F2: {status: not_applicable, completeness: complete}
    F3: {status: unassessable, completeness: incomplete, diagnostic_codes: [FM_REVIEW_UNRECORDED]}
    F4: {status: pass, completeness: complete}
    F5: {status: unassessable, completeness: incomplete, diagnostic_codes: [FM_APPLICABILITY_UNDETERMINED]}
    GateSafe: {status: pass, completeness: complete, value: true}
    ReviewEffective: {status: unassessable, completeness: incomplete, value: null, diagnostic_codes: [FM_REVIEW_UNRECORDED]}
    DecisionServiceEffective: {status: unassessable, completeness: incomplete, value: null, diagnostic_codes: [FM_REQUIRED_INPUT_MISSING]}
  fallback:
    F0: {status: fail, completeness: complete, diagnostic_codes: [FM_EVIDENCE_TYPE_COLLAPSED, FM_LINEAGE_INCOMPLETE, FM_POLICY_NOT_INSPECTABLE]}
    F1: {status: not_applicable, completeness: complete}
    F2: {status: not_applicable, completeness: complete}
    F3: {status: not_applicable, completeness: complete}
    F4: {status: fail, completeness: complete, diagnostic_codes: [FM_MATERIAL_ITEM_UNSURFACED]}
    F5: {status: unassessable, completeness: incomplete, diagnostic_codes: [FM_APPLICABILITY_UNDETERMINED]}
    GateSafe: {status: not_applicable, completeness: complete, value: null}
    ReviewEffective: {status: fail, completeness: complete, value: false, diagnostic_codes: [FM_REQUIRED_GATE_MISSING, FM_REVIEW_EVIDENCE_MISSING]}
    DecisionServiceEffective: {status: unassessable, completeness: incomplete, value: null, diagnostic_codes: [FM_REQUIRED_INPUT_MISSING]}
conclusion:
  strongest_supported_finding: representation_induced_routing_and_permission_change
  overall_score: prohibited
  escalation_required_for:
    - evidence_refinement_monotonicity
    - fallback_system_effects
    - capacity_boundary
    - contestability_and_restoration
claim_limit_receipts:
  capacity_boundary:
    evaluation_state: omitted_by_claim_limit
    required_level: dynamic_system_simulation
```

## Expected Ownership

| Finding | Diagnostic owner | Intervention owner |
| --- | --- | --- |
| Fallback evidence-state and lineage collapse | representation transformation | interface and workflow product owner |
| Material alternative not surfaced before routing | representation and routing contract | policy and workflow owners jointly |
| Required gate/review evidence absent | operational workflow configuration | workflow and review-resource owners jointly |
| Review, service, capacity, and restoration horizons missing | fixture scope | research-design owner for any expanded fixture |

## Controls

The same-rule semantic null (`P0-S-PRESERVE` versus `P0-S-FALLBACK`) confirms that a representation change need not alter routing or permission when the suppressed distinction is immaterial for that case. The routing-invariance control (`P0-N-PRESERVE` versus `P0-N-FALLBACK`) confirms that a rule can preserve scrutiny and permission across the representation change.

Together, the core pair and controls prevent the protocol from treating every abstraction as a failure. The finding depends on a policy-relevant distinction and a downstream relaxation of safeguards.

## Implementation Acceptance

Slice 1 completes this walkthrough only when the CLI emits the same profile from versioned stored records, all references resolve, canonical hashes reproduce, the held-bundle hash matches across the pair, diagnostics use closed codes, and the rendered report links every row back to the relevant trace, assessment, and diagnostic artifact.
