# Optional Online Technical Appendix: Process Red-Team Protocol and Worked Trace

This optional technical appendix accompanies *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*. The article contains the complete five-step argument, method, worked-example conclusion, and claim boundaries needed to interpret the study. This appendix supplies implementation-level protocol machinery and worked-trace receipts for readers who want to apply or inspect the procedure. It may be distributed through the project repository or submitted separately if a venue permits supplementary material; the article does not depend on its acceptance.

The confirmatory protocol is version `1.0`. The canonical technical specification remains [PROCESS_RED_TEAM_PROTOCOL.md](PROCESS_RED_TEAM_PROTOCOL.md), and the formal definitions remain [FORMAL_MODEL.md](FORMAL_MODEL.md). This appendix is an optional publication-facing rendering of those frozen materials, not part of the article's 10,000-word submission count.

## S1. Application levels and escalation

Use the least demanding level that can support the intended conclusion.

| Level | Use when | Minimum inputs | Supported conclusions | Prohibited conclusions |
| --- | --- | --- | --- | --- |
| **A. Document audit** | The question concerns declared transformations, permission rules, configured gates, roles, deadlines, or correction paths. | A bounded process map; evidence-type inventory; representation and routing rules; action taxonomy; gate and review rules; deadlines and timeout behavior; correction path; source and owner for each claim. | Structural findings about evidence lineage, declared permission changes, configured gate semantics, formal authority, and the existence of correction paths; explicit missing-documentation findings. | Realized review effectiveness, probability of access or correction, queue-capacity boundaries, causal spillovers, prevalence, or a system-level F2 pass. |
| **B. Bounded deterministic trace** | A case path, controlled pair, or bounded trace prefix can be reconstructed without stochastic system interaction. | Level A inputs plus versioned case inputs, ordered events through the declared boundary, pre/post states, exact action instances, available decision and review records, completed and incomplete horizons, and any refinement certificate needed for F1. | Case- or pair-specific F0–F5 findings where the required inputs and horizons exist; exact gate, review, permission, timing, contestability, and restoration findings on the observed prefix. | Population frequency, stochastic reliability, shared-capacity effects, completed-horizon claims beyond the trace boundary, or cohort-level F2 claims without a valid noninterference certificate. |
| **C. Dynamic system simulation** | Shared queues, endogenous response, feedback, deadlines, timeout rules, resource competition, or spillovers can change outcomes. | Level B contracts plus a complete initial system state, cohort membership, queue and resource models, keyed exogenous draws, event priorities and bounds, scenario-validity rules, and paired intervention policies. | Designed-parameter-space estimates, capacity tradeoffs, and system-level execute-versus-hold F2 results for focal and spillover cases. | Historical prevalence or causal estimates, unmodeled real-world behavior, legality inferred from simulation, or generalization beyond the declared scenarios. |

Escalate from Level A to Level B when a conclusion depends on event order, timely review, action-specific authorization at execution, or correction by a horizon. Escalate from Level B to Level C when an action can change a shared queue, service capacity, another case's deadline or timeout, cohort composition, or later endogenous behavior. If the required higher-level inputs are unavailable, return `unassessable`, name the missing inputs, and identify the unsupported claim.

A controlled pair compares two arms while holding the declared case or system inputs fixed and changing only the named representation, rule, or intervention.

## S2. Assessment and completeness semantics

The protocol produces a diagnostic profile, not an overall workflow score.

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

Status and completeness are separate. A known sufficient counterexample may yield `fail` while unresolved material remains recorded as `incomplete`. Missing documentation normally yields `unassessable`, not `not_applicable`.

The report-level field `evaluation_state` is either `assessed` or `omitted_by_claim_limit`. An item marked `omitted_by_claim_limit` receives no status or completeness value; instead, the receipt names the unsupported claim, required higher level, and missing input class. It is not a fifth status.

## S3. Required receipt fields

Each assessed property or helper records:

- application level and claim limit;
- evaluated inputs and their roles;
- evidence source and trace reference;
- located evidence-to-action transition;
- evaluation state, status, and completeness;
- stable diagnostic code and unresolved information;
- diagnostic owner and intervention owner as separate fields;
- mechanism-specific intervention and tradeoff; and
- any ambiguity, unsupported conclusion, or escalation requirement.

The intake worksheet records the workflow and version, evaluation unit, consequential progression, comparison, claim sought, explicit nonclaims, evidence types, transformations, representations, permission and action rules, review and timeout behavior, contestability horizon, restoration obligations, and consequence baseline.

## S4. Five-step reference worksheet

| Step | Core question | Required record | Escalation trigger |
| --- | --- | --- | --- |
| **1. Map transformations and ownership** | Where does a policy-material distinction disappear or become unavailable to an empowered role? | Source value and evidence type; transformation; assumptions; downstream representation; provenance; F0 and F4 result; diagnostic and intervention owners. | Use a trace when the finding depends on event order or realized surfacing. |
| **2. Test what weaker evidence permits** | Does weaker evidence permit progression excluded by an admissible refinement, or does a purported fallback create progression or spillovers? | Exact actions; target and parameters; prerequisites; independent support rule; default and timeout; refinement certificate or failure witness; F1 and F2 result. | Use Level C when the intervention changes shared resources, another case, or a cohort path. |
| **3. Test whether review is operational** | Is a configured gate blocking, action-bound, current, adequately informed, and timely? | Gate safety, effective-review conditions, F3, and timely supported service separately; reviewer evidence, authority, dependency, timing, decision, and execution-state revalidation. | Escalate when queueing or capacity determines timely completion. |
| **4. Stress access, workload, and deadlines** | How do access, arrivals, service demand, capacity, deadlines, and defaults alter outcomes? | Gate safety, timely completion, unresolved cases, interaction events, workload, recovery-path entry, correction, and restoration as separate outcomes. | Use dynamic simulation for feedback, resource competition, or spillovers. |
| **5. Test contestability and restoration** | Does a correction path exist, can it be used in time, and are all declared consequences restored? | Structural path, access, use, correction, consequence vector, baseline, restoration status, residual effects, horizon, and owner. | Treat an unfinished horizon as `unassessable`; do not infer restoration from record correction alone. |

## S5. Fixed Robodebt bounded trace

The worked trace is an inspectable scripted illustration, not a representative or independently derived result. It holds the case, evidence, access, later evidence, process, clocks, evaluation rules, resources, and draws fixed. Only the policy changes: impute and progress versus agency-assisted information first. F0–F4 describe what follows from those declared inputs. Capacity/service and the substantive recovery/restoration endpoints are `omitted_by_claim_limit` because the fixture does not independently derive the inputs needed to establish them.

### Table S1. Assessment profile

| Step/property | Baseline assessment | Repair assessment | Evidence and claim limit |
| --- | --- | --- | --- |
| 1/F0 | `fail/complete`: aggregate evidence becomes an unflagged imputed period value. | `pass/complete`: retrieved period records retain their evidentiary type and provenance. | Day-22 imputation versus day-10 evidence return; trace-specific fidelity only. |
| 1/F4 | `fail/complete`: imputation and its uncertainty are not surfaced before action. | `pass/complete`: retrieved evidence is surfaced before disposition. | Same representation transition; trace-specific surfacing only. |
| 2/F1 | `fail/complete`: the imputed value automatically permits unsupported modeled debt progression. | `pass/complete`: progression is held until period-specific support is obtained. | Day-22 progression versus day-15 supported disposition; no population or legal inference. |
| 2/F2 | `unassessable/incomplete`: the trace cannot test spillovers. | Same. | No cohort, shared queue, or noninterference evidence; Level C required. |
| 3/F3 | `fail/complete`: a required pre-action gate is absent. | `not_applicable/complete`: the supported disposition does not require review in this trace. | No general review-reliability estimate. |
| 4/capacity-service | `omitted_by_claim_limit`; no status. | Same. | No arrivals or shared queues; Level C required. |
| 5/F5 | `omitted_by_claim_limit`; no status. | Same. | Recovery and restoration outcomes require acquired records and the resulting disposition, a recovery-entry rule, correction timing, restoration events and dependencies, a consequence baseline, and a day-60 observation rule. The fixture scripts rather than independently derives those inputs. |

### Table S2. Ownership and intervention receipt

Entries appear as baseline; repair.

| Step/property | Diagnostic owner | Intervention — empowered owner | Tradeoff |
| --- | --- | --- | --- |
| 1/F0 | representation; evidence | Preserve provenance — interface and policy; acquire evidence — information service | Slower progression; acquisition workload. |
| 1/F4 | representation; representation | Surface material meaning — interface; maintain surfacing — interface | Reviewer context; provenance maintenance. |
| 2/F1 | permission rule; permission rule | Hold unsupported action — gate; require support — gate | Delayed disposition; longer supported disposition. |
| 2/F2 | simulation; simulation | Build Level C cohort pair — simulation; same | Cohort spillovers remain unresolved; same. |
| 3/F3 | process; process | Bind fail-closed review — review and gate; none in trace — policy if scope changes | Review consumes capacity; another progression path could require review. |
| 4/capacity-service | simulation; simulation | Add queues, resources, and paired policies — simulation; same | Modeling assumptions and computation; same. |
| 5/F5 | reassessment; process | Specify and test recovery and restoration endpoints before assigning an intervention — restoration and policy | Broader remediation and any endpoint effects remain unresolved. |

The trace does not establish that every historical Robodebt case followed this path, that the modeled debt was legally or monetarily invalid, that either arm entered or avoided recovery, that restoration succeeded or failed, or that information-first handling is costless or generally superior. Its scripted recovery and restoration events remain useful for testing software contracts, but they do not independently establish the article's substantive worked-example endpoints.

## S6. Executable representation fixture

The article uses domain-neutral language for the deterministic representation pair. The executable fixture retains its original safety-specific labels so that readers can reproduce the exact frozen test rather than infer that the example was rewritten after results were known.

A low-resolution sensor output records a pickup-like silhouette at confidence 0.42, typed alternatives that include an armed technical, and the broad class `vehicle`. The preservation arm keeps confidence, alternatives, unresolved status, and provenance visible. A fixed rule then requires added observation and fail-closed review before routine administrative disposition. The fallback arm emits only the defensible broad label `vehicle`; every listed alternative remains compatible with that label, but the policy-material distinction disappears and the same rule permits routine disposition. The fixture concerns routing of a synthetic organizational case. It does not authorize action against a physical object, estimate prevalence, or model an operational deployment.

Two negative controls delimit the mechanism. When no policy-material alternative is present, both representations route identically. When scrutiny is representation-independent, both arms retain it. The canonical specification is [PRECURSOR_FIDELITY_FIXTURE.md](PRECURSOR_FIDELITY_FIXTURE.md), and the publication review packet is [P0_PROCEDURE_REVIEW_PACKET.md](P0_PROCEDURE_REVIEW_PACKET.md).

## S7. Freeze 5 reporting details and sensitivity

The core U3 conditional-review denominator contains 44,381 requests and 42,098 timely completions. Twenty of 3,240 family-replications generated no request and are treated as not applicable; all 108 families have a positive denominator after aggregation. A completed review of unresolved evidence produces an evidence-request state rather than progression, so completion does not imply resolution or supported service.

The fail-open progression union is 0.476211 of initiated cases. Its exclusive components are 0 evidence-only, 0.104603 authorization-only, and 0.371609 joint evidence-and-authorization failure. The evidence-only zero is rule-implied rather than estimated: completed review cannot authorize unsupported progression. The authorization-only component prevents authorization failure from being mislabeled as evidentiary failure, while the joint component identifies cases with both defects. These components partition the timeout-activation result and are not separate policy effects.

| U3 sequential stage | Core rate per initiated case | Sensitivity rate |
| --- | ---: | ---: |
| Adequate response evidence before retrieval | 0.573248 | 0.573962 |
| Retrieval requested | 0.426752 | 0.426038 |
| Evidence retrieved and progression supported | 0.255529 | 0.254722 |
| Unresolved after acquisition; entered review | 0.171223 | 0.171316 |
| Evidence requested after timely review | 0.162415 | 0.162863 |
| Held after review timeout | 0.008808 | 0.008453 |

The stage rows are sequential rates, not additive quantities or independent component effects. Adequate response evidence plus unresolved response evidence sent to retrieval partitions initiated U3 cases; retrieved evidence plus unresolved evidence partitions retrieval requests. Unresolved evidence then enters review, where timely completion changes its recorded state to evidence requested and timeout leaves it held. The model has no post-request response cycle, so neither review branch resolves evidence.

The latency sensitivity doubled the retrieval-time scale from 10 to 20 days. Its stage rates differ from the core by less than 0.001. U3 generated 44,405 review requests, of which 42,214 completed on time; 24 family-replications generated no request. The sensitivity changes routing and queue phasing only. It does not test retrieval failure, abandonment, deadline expiry, or historical calibration.

Complete machine-readable evidence is in the Freeze 5 core and sensitivity analysis receipts under `outputs/`, [FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json](FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json), and the prior [FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json](FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json).

## S8. Reference artifacts

- Confirmatory protocol: [PROCESS_RED_TEAM_PROTOCOL.md](PROCESS_RED_TEAM_PROTOCOL.md)
- Formal definitions and executable contracts: [FORMAL_MODEL.md](FORMAL_MODEL.md)
- Worked-trace selection rule: [WORKED_TRACE_SELECTION.md](WORKED_TRACE_SELECTION.md)
- Worked-trace expected profile: [ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md](ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md)
- Worked-trace review packet: [ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md](ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md)
- Stored bounded trace: [`../data/golden_traces/robodebt_worked_trace_v1.json`](../data/golden_traces/robodebt_worked_trace_v1.json)
- Transfer canary and expected profile: [TRANSFER_CANARY.md](TRANSFER_CANARY.md) and [TRANSFER_CANARY_EXPECTED_PROFILE.md](TRANSFER_CANARY_EXPECTED_PROFILE.md)

These artifacts make the protocol inspectable and replayable. They do not establish practitioner usability, inter-rater reliability, adoption, field efficacy, or transfer performance.
