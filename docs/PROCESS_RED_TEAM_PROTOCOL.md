# Process Red-Team Protocol

Status: draft version `0.2`; pre-freeze and pre-confirmatory

Protocol owner: process-red-team method

Formal basis: `docs/FORMAL_MODEL.md`

Blinded compatibility packet: `docs/P0_COLD_READER_PACKET.md`

Post-assessment compatibility oracle: `docs/P0_USABILITY_WALKTHROUGH.md`

Blinded transfer packet: `docs/TRANSFER_CANARY.md`

Post-assessment transfer oracle: `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`

## Purpose

This protocol diagnoses when a workflow turns incomplete, uncertain, disputed, or aggregate evidence into consequential action without preserving the safeguards that the evidence state requires. It follows one evidence-to-action path across representation, routing, review, action, contestability, and restoration.

The protocol is usable at three levels. A practitioner should use the least demanding level that can support the intended conclusion and must escalate when the process contains shared resources, feedback, timeouts, or system spillovers that the current level cannot resolve.

This is a diagnostic method, not a legal-compliance standard, a risk score, or a claim that every workflow requires simulation.

## Output Contract

The output is a **diagnostic profile**, not one overall `pass` or `fail`. Preserve every assessed property or helper separately, including:

- status: `pass`, `fail`, `unassessable`, or `not_applicable`;
- completeness: `complete`, `incomplete`, or `invalid`;
- the located evidence-to-action transition;
- evaluated inputs and their roles;
- observable evidence and trace references;
- stable diagnostic codes;
- unresolved information;
- a mechanism-specific intervention, its owner, and its tradeoff; and
- the application level and resulting claim limit.

A known sufficient failure remains a failure even if another conjunct is unresolved; completeness records the unresolved material. Missing documentation is normally `unassessable`, not `not_applicable`. An overall score, weighted ranking, traffic-light average, or statement that the complete workflow “passes” is prohibited unless a separately frozen decision rule is introduced and justified outside this protocol.

## Application Levels

| Level | Use when | Minimum inputs | Supported conclusions | Prohibited conclusions |
| --- | --- | --- | --- | --- |
| **A. Document audit** | The immediate question concerns declared transformations, permission rules, configured gates, roles, deadlines, or correction paths. | One bounded process map; evidence-type inventory; representation and routing rules; action taxonomy; gate and review rules; deadlines and timeout behavior; correction path; source and owner for each claim. | Structural findings about evidence lineage, declared permission changes, configured gate semantics, formal authority, and existence of correction paths. Explicit missing-documentation findings. | Realized review effectiveness, probability of access or correction, queue-capacity boundaries, causal spillovers, prevalence, or system-level F2 pass. |
| **B. Bounded deterministic trace** | A case path, controlled pair, or explicitly bounded trace prefix can be reconstructed without stochastic system interaction. A trace may end before review, execution, contestability, or restoration completes if the missing horizon is declared. | Level A inputs plus versioned case inputs, ordered events through the declared boundary, pre/post states, exact action instances, available decision and review records, declared completed and incomplete horizons, and any certified refinement set needed for F1. | Case- or pair-specific F0–F5 findings where the required inputs and horizons exist; exact gate, review, permission, timing, contestability, and restoration failures on the observed prefix. Unfinished conditions remain `unassessable`. | Population frequency, stochastic reliability, shared-capacity effects, completed-horizon claims beyond the trace boundary, or cohort-level F2 claims without a valid noninterference certificate. |
| **C. Dynamic system simulation** | Shared queues, endogenous response, feedback, deadlines, timeout rules, resource competition, or spillovers can change outcomes. | Level B contracts plus a complete initial system state, cohort membership, queue and resource models, keyed exogenous draws, event priorities and bounds, scenario validity rules, and paired intervention policies. | Designed-parameter-space estimates, capacity boundaries, tradeoffs, and system-level execute-versus-hold F2 results for focal and spillover cases. | Historical prevalence or causal estimates, unmodeled real-world behavior, legality inferred from simulation, or generalization beyond declared scenarios. |

Machine-facing application-level IDs are `document_audit`, `bounded_deterministic_trace`, and `dynamic_system_simulation`.

### Mandatory escalation

Escalate from Level A to Level B when a conclusion depends on event order, whether review completed in time, whether an exact action remained authorized at execution, or whether correction occurred by a horizon.

Escalate from Level B to Level C when an action can change a shared queue, service capacity, another case's deadline or timeout, cohort composition, or later endogenous behavior. A case-local F2 comparison is permitted only with a valid noninterference certificate and supports only a within-case conclusion.

If the required higher-level inputs cannot be obtained, return `unassessable` with the missing inputs and the unsupported claim explicitly named. Do not silently approximate a higher-level conclusion at a lower level.

### Assessment versus claim-limit receipt

`status` is assigned only when a property or helper is evaluated. A report also carries `evaluation_state = assessed | omitted_by_claim_limit` outside the formal assessment envelope. `omitted_by_claim_limit` means the selected application level cannot support the sought conclusion and no property evaluation was attempted; it is not a fifth status and cannot be counted as `not_applicable` or `unassessable`.

Use `unassessable` when the property is in or potentially in scope but required information or valid specification is missing. Use `omitted_by_claim_limit` when, for example, a bounded deterministic trace deliberately makes no system-capacity estimate. Every omission names the unsupported claim, the higher level required, and the missing input class.

## Intake Worksheet

Complete this worksheet before assigning statuses.

### 1. Scope and decision question

| Field | Required entry |
| --- | --- |
| Workflow and version | Stable workflow or profile ID and effective dates |
| Evaluation unit | Case, controlled pair, or cohort system |
| Application level | A, B, or C, with rationale |
| Consequential progression | Exact action instances or action classes under review |
| Comparison | Baseline, alternative representation, evidence refinement, hold intervention, or policy contrast |
| Claim sought | Structural, trace-specific, prospective, realized, or simulation-estimated |
| Explicit non-claims | Conclusions the selected level cannot support |

### 2. Evidence and representation

For every handoff, record the source, value, evidence type (`observed`, `derived`, `imputed`, `disputed`, or `missing`), transformation, assumptions, compatible-state meaning, representation visible downstream, owner, and provenance visibility.

### 3. Permission and action

List automatic progression, post-review progression, constraint, information, and restoration actions separately. Record the exact rule, target, parameters, prerequisites, authorization requirement, timeout behavior, and independent support rule for each material action.

### 4. Review and timing

Record who receives the case, what they see, whether they can stop or modify the exact action, whether the workflow waits, queue/resource dependencies, review deadline, action deadline, timeout semantics, and the versioned review decision where one exists.

### 5. Contestability and restoration

Record the structural correction path, access requirements, capacity dependencies, contestability horizon, restoration obligations, consequence dimensions, baseline, and any residual effects after correction.

### 6. Evidence quality and ownership

For each material assertion, identify whether it is documented, hypothetical, simulated, or derived; name the source or synthetic root; identify the owning layer; and state whether the input is complete, missing, disputed, or structurally invalid.

Record ownership in two separate fields. `diagnostic_owner` is the layer responsible for the failed or missing fact, such as evidence transformation, process configuration, or simulation execution. `intervention_owner` is the role empowered to change the representation, rule, gate, resource, deadline, or restoration process. Do not infer one from the other.

## Assessment Semantics

Use one assessment envelope per property or helper.

| Status | Meaning |
| --- | --- |
| `pass` | The applicable condition is established from complete valid inputs under a conclusion-valid method. |
| `fail` | A sufficient valid counterexample or failed necessary condition is established. |
| `unassessable` | The condition applies or may apply, but no sufficient pass or failure conclusion is available. |
| `not_applicable` | A frozen scope exclusion or fully resolved false antecedent establishes that the condition does not apply. |

| Completeness | Meaning |
| --- | --- |
| `complete` | Every required input is available and valid. |
| `incomplete` | Required information, a horizon, or precision remains unavailable, but the available structure is valid. |
| `invalid` | A required schema, reference, specification, rule binding, or aggregation contract is malformed or inconsistent. |

For the standard conjunctive rule, `fail` dominates `unassessable`, then `pass`, then an all-`not_applicable` result. Completeness is reported independently and takes the worst applicable component value under `invalid > incomplete > complete`. Contextual helpers never determine aggregate truth.

### Ordered status procedure

For every property or helper:

1. Confirm that the selected application level permits the sought conclusion. If not, emit an `omitted_by_claim_limit` receipt and stop; do not create an assessment.
2. Read the frozen scope declaration. Missing or undetermined scope is `unassessable`; explicit exclusion is `not_applicable`.
3. Validate the inputs needed to decide the antecedent. Missing input is `unassessable/incomplete`; structurally invalid input is `unassessable/invalid`.
4. Evaluate the antecedent. A demonstrably false antecedent is `not_applicable/complete`.
5. Evaluate every independently decidable condition and retain every sufficient failure witness.
6. If a sufficient valid failure witness exists, return `fail`; unresolved material is retained through `incomplete` or `invalid` completeness.
7. If no sufficient failure exists but required material is missing or invalid, return `unassessable` with the applicable completeness.
8. Return `pass/complete` only when every required condition is validly established.

An absent configured gate is `not_applicable` for `GateSafe`, because there is no gate whose behavior can be evaluated. If a gate was independently required, record `FM_REQUIRED_GATE_MISSING` under the affected review or progression assessment; do not relabel the nonexistent gate itself as unsafe.

### Compact property glossary

| Property/helper | Plain-language question | Typical application level | Key boundary |
| --- | --- | --- | --- |
| F0 — evidentiary fidelity | Are material claims supported, traceable, distinguishable as observed/derived/imputed/disputed/missing, and inspectable downstream? | A or B | A truthful broad label can still fail by hiding lineage, assumptions, or material distinctions. |
| F1 — robust automatic permission | Does weaker evidence avoid introducing automatic progression that an independent support rule excludes under any certified admissible refinement? | B; C if system state affects permission | A found counterexample can fail; search without a counterexample cannot establish universal pass. |
| F2 — safe fallback allowance | Does executing an added constraint or information fallback, compared with explicitly holding it, avoid releasing unsupported progression for focal or spillover cases? | C; B only with valid case-local noninterference | Shared queues, deadlines, or capacity require a cohort-system pair. |
| F3 — review-preserved progression | Was the exact progression action withheld until effective, current authorization, and did it remain eligible and independently supported at execution? | B or C | A review label, notice, or stale authorization is insufficient. |
| F4 — surfacing preservation | Did every independently material meaning reach a role able to intervene before progression or expiry? | A for configured structural surfacing; B/C for realized timely surfacing | Structural policy visibility must not be reported as realized timely delivery. |
| F5 — contestability and restoration | Is correction structurally reachable, prospectively reliable or realized by the declared horizon, and are all required consequences restored? | A for structural path only; B/C for prospective or realized results | Correction of the decision coordinate alone does not establish complete restoration. |
| GateSafe | Did a configured gate actually block the action while prerequisites were unmet? | B or C | No configured gate means `not_applicable`; a separately required missing gate is diagnosed elsewhere. |
| ReviewEffective | Did an authorized reviewer receive the required evidence and complete an enforceable intervention in time? | B or C | Any observably false necessary condition can establish failure. |
| DecisionServiceEffective | Did the workflow reach a supported disposition by the declared service deadline? | B or C | A safe fail-closed gate can coexist with failed decision service. |

## Five-Step Diagnostic

### Step 1: Map evidence transformations and ownership

**Required inputs:** evidence/representation worksheet, transformation rules, provenance, ownership, visibility, and independently defined material meaning.

**Checks:** classify every material value; verify lineage and assumptions; locate dropped alternatives or uncertainty; test F0 evidentiary fidelity and F4 surfacing preservation.

**Output:** the first transition where relevant evidence or uncertainty becomes unsupported, relabeled, or unavailable to an authorized role.

**Typical interventions:** preserve typed provenance; surface alternatives; prohibit relabeling; bind transformations to source records; expose uncertainty to the role that can intervene.

### Step 2: Test what weaker evidence newly permits

**Required inputs:** action inventory, total decision rule, independent support rule, comparison baseline, and—where F1 is claimed—a conclusion-valid refinement certificate.

**Checks:** separate progression from constraint and information acquisition; compare exact automatic action instances; treat defaults and fail-open timeouts as permission rules; test F1 on evidence refinements and F2 on valid execute-versus-hold intervention pairs.

**Output:** the exact evidence-to-permission edge that is supported, unsupported, outside scope, or unresolved.

**Typical interventions:** restrict automatic progression; acquire evidence; use reversible constraint; require effective review; change timeout behavior; remove unsupported defaults.

### Step 3: Verify that review is operationally effective

**Required inputs:** gate state, review state, evidence visible to the reviewer, authority, dependency, timing, exact review decision, and execution pre-state.

**Checks:** report configured review, gate safety, review effectiveness, and decision service separately; verify the workflow waits; bind authorization to the exact action and versions; recheck eligibility and support immediately before execution.

**Output:** whether review blocks unsupported progression, merely labels it, is incomplete, or preserves safety while losing timely service.

**Typical interventions:** enforce a fail-closed dependency; give the reviewer stopping authority; expose the missing evidence; revalidate at execution; add capacity or admission control.

### Step 4: Stress access, workload, and deadlines

**Required inputs:** notice and access conditions, workload, service capacity, deadlines, queue disciplines, timeout behavior, and the selected application level's timing model.

**Checks:** use hand traces for deterministic failures, queue calculations for simple capacity questions, and Level C simulation for feedback or shared-resource effects; identify the boundary at which effective review or timely supported service fails.

**Output:** the operating region, boundary, overload behavior, and separate safety, delay, agency-workload, recipient-burden, and unresolved-case effects.

**Typical interventions:** increase or reserve capacity; meter arrivals; extend or pause deadlines; prioritize material uncertainty; acquire evidence before queueing; keep timeout behavior fail closed.

### Step 5: Test contestability and restoration

**Required inputs:** correction path, access and capacity dependencies, horizons, reliability rule, consequence vector, restoration obligation, and baseline.

**Checks:** separate structural path existence, prospective reliability, realized opportunity, uptake, correction, and restoration; test whether all modeled consequence dimensions return to baseline when restoration is due.

**Output:** whether correction is reachable and timely, whether it occurred, and which consequences remain after correction.

**Typical interventions:** pause recovery during contest; make evidence acquisition feasible; extend correction windows; reserve reassessment capacity; restore monetary and nonmonetary consequences separately.

## Practitioner Report Template

### Scope receipt

- Workflow/profile and version:
- Evaluation unit:
- Application level and rationale:
- Comparison and baseline:
- Claim sought:
- Explicit non-claims:
- Source cutoff and assessor:

### Assessment profile

| Step | Property/helper | Evaluation state | Status | Completeness | Located transition | Evidence/trace | Diagnostic | Missing information or claim limit | Intervention | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | F0 |  |  |  |  |  |  |  |  |  |  |  |
| 1 | F4 |  |  |  |  |  |  |  |  |  |  |  |
| 2 | F1 |  |  |  |  |  |  |  |  |  |  |  |
| 2 | F2 |  |  |  |  |  |  |  |  |  |  |  |
| 3 | GateSafe |  |  |  |  |  |  |  |  |  |  |  |
| 3 | ReviewEffective |  |  |  |  |  |  |  |  |  |  |  |
| 3 | F3 |  |  |  |  |  |  |  |  |  |  |  |
| 3 | DecisionServiceEffective |  |  |  |  |  |  |  |  |  |  |  |
| 4 | capacity/service boundary |  |  |  |  |  |  |  |  |  |  |  |
| 5 | F5 structural |  |  |  |  |  |  |  |  |  |  |  |
| 5 | F5 prospective |  |  |  |  |  |  |  |  |  |  |  |
| 5 | F5 realized/restoration |  |  |  |  |  |  |  |  |  |  |  |

Add rows rather than combining incompatible statuses. Preserve component-level results beneath every aggregate. For `evaluation_state = omitted_by_claim_limit`, leave status and completeness blank and complete only the claim-limit, escalation, and ownership fields.

### Conclusion receipt

State:

1. the strongest supported finding;
2. every known failure, including failures with incomplete completeness;
3. every unassessable issue and the exact missing input;
4. the selected intervention and its expected mechanism;
5. safety, delay, burden, workload, and restoration tradeoffs separately;
6. whether a higher application level is required; and
7. the conclusions that remain prohibited.

Do not produce a weighted “best policy,” overall compliance score, or aggregate workflow pass.

## Diagnostic Resolution Standard

Every `fail` or `unassessable` result must use a closed diagnostic code and record the category, owning layer, property/helper, source and target identifiers, expected and observed values where meaningful, artifact path, severity, and suggested next action. The suggested action must address the diagnosed mechanism; it must not be a generic request to “review the model.”

When multiple interventions are plausible, report each intervention's owner and tradeoff. Do not imply that preserving safety automatically preserves timely decision service or that correction automatically restores all consequences.

### Compact diagnostic lookup

| Situation | Code |
| --- | --- |
| Scope is missing, ambiguous, or deliberately undetermined | `FM_APPLICABILITY_UNDETERMINED` |
| Required evaluation input is missing or invalid | `FM_REQUIRED_INPUT_MISSING` |
| Independent evaluation specification is missing or invalid | `FM_EVALUATION_SPEC_INVALID` |
| Known evidence state is relabeled or collapsed | `FM_EVIDENCE_TYPE_COLLAPSED` |
| Source, transformation, assumption, or version lineage is incomplete | `FM_LINEAGE_INCOMPLETE` |
| Required provenance or typing is unavailable downstream | `FM_POLICY_NOT_INSPECTABLE` |
| Independently material meaning does not reach an authorized role in time | `FM_MATERIAL_ITEM_UNSURFACED` |
| Required gate is absent | `FM_REQUIRED_GATE_MISSING` |
| Reviewer lacks required evidence | `FM_REVIEW_EVIDENCE_MISSING` |
| Reviewer lacks stopping, delaying, or modifying authority | `FM_REVIEW_AUTHORITY_MISSING` |
| Required review was not completed and recorded | `FM_REVIEW_UNRECORDED` |
| Review completed too late | `FM_REVIEW_LATE` |
| Realized contestability or restoration horizon remains pending | `FM_EVALUATION_HORIZON_PENDING` |
| Correction leaves a modeled consequence unrestored | `FM_RESTORATION_PARTIAL` |

The complete closed registry remains in `data/model/schema_manifest_v1.yaml`. If no listed code accurately describes the finding, return the relevant property `unassessable/invalid` and escalate the vocabulary gap; do not invent a code in the reader packet.

## Cold-Reader QA

Cold-reader QA occurs in two stages. During Slice 0, at least two readers who did not draft the protocol independently apply it without coaching to:

1. the blinded fixed representation-preservation packet in `docs/P0_COLD_READER_PACKET.md`; and
2. the blinded contemporary-AI packet in `docs/TRANSFER_CANARY.md`.

This first stage tests construct readability and continuity before implementation. P0 is synthetic and is not a Robodebt trace. Slice 3 now provides the executable prespecified Robodebt worked-trace packet rendered from `RB-WORKED-TRACE-001` and its separately withheld expected profile. Before version `1.0` is frozen, new eligible readers must apply the protocol to that packet and the transfer canary. This second stage tests the operational protocol before confirmatory freeze; the artifacts exist, but valid independent returns remain pending.

Each reader records the application level, located transition, assessment statuses and completeness, evidence used, missing information, intervention, and ambiguity. Reconcile disagreements by revising the protocol or returning `unassessable`; do not settle them through undocumented coaching. This is artifact QA, not evidence about human performance.

The reader receives packet-only copies and the protocol. They must not have access to the applicable withheld profiles, fixture expected-result tables, or executable expected outputs until their assessment is locked. For Slice 0 these include `docs/P0_USABILITY_WALKTHROUGH.md` and `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`; for Slice 3 they include the generated Robodebt expected profile and the transfer profile. An oracle custodian records packet version and hashes, distributes the packets, timestamps the returned reports, and only then compares each row with the withheld profiles. Repository access that exposes the oracles invalidates the blind run and must be logged as a practice run rather than QA evidence.

The custodian uses `docs/COLD_READER_QA_RECEIPT.md` to record exposure validity, versions and hashes, returned artifacts, row-level differences, error classes, ambiguities, and any revision/rerun decision.

Agreement is not the sole criterion. Record omitted rows, unsupported certainty, wrong application level, incorrect `not_applicable` use, diagnostic mismatch, and failure to state claim limits. Revise version `0.2` before freeze, retain the original reports and change log, and rerun the affected QA stage with new readers after any semantic change. Distribution follows `docs/COLD_READER_DISTRIBUTION.md`.

## Version and Freeze Rule

Version `0.2` may change only before confirmatory freeze. Version `1.0` freezes the five steps, application-level rules, assessment-versus-claim-limit distinction, status/completeness semantics, prohibited composite score, intake fields, diagnostic fields, blinded packets, withheld oracles, canary, and worked-trace selection rule. Results may illustrate the frozen protocol but may not redefine it.
