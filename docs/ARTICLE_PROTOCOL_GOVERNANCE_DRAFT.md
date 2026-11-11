# Article Draft: Process-Red-Team Protocol and Governance Implications

Status: first publication-facing draft from protocol `1.0`, the fixed Robodebt worked trace, and the transfer canary

Working title: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

The section number follows `ARTICLE_OUTLINE.md`. Usability is a design objective, not an evaluated outcome, and no formal comprehensibility review is required.

## 7. Process-Red-Team Protocol and Governance Implications

### 7.1 What the protocol produces

Usability is a design objective, not an evaluated result. The protocol examines an evidence-to-action path through representation, routing, review, action, contestability, and restoration. It returns separate findings, missing information, located transitions, interventions, owners, and tradeoffs—not an overall score.

Use the least demanding adequate level. **Level A, document audit**, maps evidence, actions, rules, roles, deadlines, and correction paths; it supports structural findings only. **Level B, bounded deterministic trace**, adds versioned case inputs, ordered events, states, actions, and horizons; it supports trace-specific conclusions only. **Level C, dynamic system simulation**, adds cohorts, queues, resources, keyed draws, event rules, and paired policies; it supports estimates only within the designed parameter space.

Escalate from A to B when conclusions depend on event order or realized timing, and from B to C when shared resources, spillovers, or endogenous behavior matter. If higher-level inputs are unavailable, return `unassessable` and name them.

Level choice belongs in the receipt; it does not license inference about missing operational facts.

A **controlled pair** compares two arms while holding the declared case or system inputs fixed and changing only the named representation, rule, or intervention.

An evaluated property is `assessed` and receives `pass`, `fail`, `unassessable`, or `not_applicable`. A conclusion beyond the selected level is `omitted_by_claim_limit` and receives no status. Completeness—`complete`, `incomplete`, or `invalid`—is separate: a sufficient failure can coexist with unresolved material.

Each step records the evaluated inputs, evidence source, located transition, trace reference, evaluation state, status, completeness, diagnostic, unresolved information, intervention, diagnostic and intervention owners, tradeoff, level, and claim limit.

### 7.2 Step 1: map transformations and ownership

For each handoff, record the source value and type (observed, derived, imputed, disputed, or missing), transformation, assumptions, downstream representation, provenance, and diagnostic owner. Locate the first transition where a policy-relevant distinction disappears or becomes unavailable to an empowered role.

This tests evidentiary fidelity (F0) and surfacing preservation (F4). A broad label may fail by hiding imputation, conflicting evidence, lineage, or action-relevant scope. Interventions retain typed provenance, expose material disputes, prohibit unsupported relabeling, and bind transformations to sources. Record the intervention owner separately; it may be the interface or workflow owner rather than the evidence producer.

### 7.3 Step 2: test what weaker evidence permits

Inventory exact progression, constraint, information-acquisition, and restoration actions. For each automatic progression, record its target, parameters, prerequisites, support rule, default, and timeout consequence. F1 asks whether weaker evidence permits an action excluded by the support rule under an admissible refinement. One valid counterexample fails F1; passage requires a conclusion-valid certificate covering the frozen refinement set.

F2 compares executing a fallback with holding it over the **complete intervention unit**: the focal case and every affected queue, resource, deadline, and case. Without noninterference, a case-local trace is insufficient. Defaults and fail-open timeouts are permission rules. Locate failures at the evidence-to-permission edge; responses include narrower authority, evidence acquisition, reversible constraint, effective review, or fail-closed timeout.

### 7.4 Step 3: test whether review is operational

Decompose “human review”: Is a gate configured and blocking? Does an authorized reviewer receive material evidence and control the exact action? Does the workflow wait? Is authorization current at execution? Is a supported disposition reached by the service deadline?

Report `GateSafe`, `ReviewEffective`, F3, and `DecisionServiceEffective` separately. A fail-closed gate may be safe while service fails; completed review may be stale or nonbinding. With no configured gate, `GateSafe` is not applicable, although a required missing gate is diagnosed under progression or review. The excluded simulation service output is invalid because its numerator failed semantic audit. Target visibility, stopping authority, dependency, timing, execution-state revalidation, or capacity—not a reviewer label.

### 7.5 Step 4: stress access, workload, and deadlines

Use the simplest adequate level: documents for timeout rules, traces for event order, queue calculations for simple capacity questions, and Level C for shared resources, feedback, or spillovers. If the question concerns a boundary rather than a sampled operating region, state how that boundary was located and with what resolution.

Stress access, evidence, arrivals, service demand, capacity, deadlines, and timeouts. Report gate safety, timely completion, unresolved cases, recipient interactions or burden, workload, exposure, and restoration separately. Do not equate delay with safety or backlog reduction with resolution. Matched fail-open and fail-closed policies had identical timely-review completion but opposite permission consequences. Interaction events cannot establish subjective burden or welfare. Recommendations must identify improvement, deterioration, and what remains unmeasured.

### 7.6 Step 5: test contestability and restoration

Separate six questions hidden by “appeal available”: does a structural path exist; is access reliable; was an opportunity available and used; did correction occur; were all required consequences restored? Documents support structural findings; realized and timely conclusions require a trace or system model with declared horizons.

Declare the consequence vector and baseline before claiming restoration. Correcting a decision or balance does not restore recovery status, time, access, or other external consequences. Pending horizons are unassessable, not failed. Interventions can pause recovery, enable evidence acquisition, reserve reassessment capacity, extend windows, and separate correction from restoration ownership. Keep their costs and delays visible. Explicitly name every consequence outside the model.

### 7.7 Fixed Robodebt worked example

The fixed Level B controlled pair is explanatory, not representative. It holds the case, evidence, access, later evidence, process, clocks, evaluation rules, resources, and draws fixed. Only policy changes: impute and progress versus agency-assisted information first.

In the baseline, a notice fails, the 21-day deadline expires, and aggregate income becomes an imputed period representation without surfaced uncertainty. Unsupported modeled debt progression and recovery exposure follow; later correction leaves a residual consequence. The repair holds progression, obtains records, records a supported disposition, and avoids modeled exposure. This trace does not establish that information first is costless, generally superior, or historically typical.

A component-local check might confirm that averaging ran as specified or that notice issued. Only the process trace shows how failed access, imputation, deadline expiry, and the permission rule combine to permit unsupported progression.

**Table 3. Five-step diagnostic applied to the fixed Robodebt trace.** All F0–F5 rows are `assessed`; capacity/service is `omitted_by_claim_limit`. Rows follow diagnostic order. In Panel B, entries appear as baseline; repair.

**A. Assessment profile**

| Step/property | Baseline assessment | Repair assessment | Evidence and claim limit |
| --- | --- | --- | --- |
| 1/F0 | `fail/complete`; `FM_EVIDENCE_TYPE_COLLAPSED` | `pass/complete` | B-04/R-05; trace-specific fidelity. |
| 1/F4 | `fail/complete`; `FM_MATERIAL_ITEM_UNSURFACED` | `pass/complete` | B-04/R-05; trace-specific surfacing. |
| 2/F1 | `fail/complete`; `FM_ROBUST_PERMISSION_VIOLATION` | `pass/complete` | B-05/R-06; no population or legal inference. |
| 2/F2 | `unassessable/incomplete`; `FM_REQUIRED_INPUT_MISSING` | Same | No cohort pair or spillover conclusion. |
| 3/F3 | `fail/complete`; `FM_REQUIRED_GATE_MISSING` | `not_applicable/complete` | B-05/R-06; no general review-reliability estimate. |
| 4/capacity-service | `omitted_by_claim_limit`; no status | Same | No arrivals or shared queues; Level C required. |
| 5/F5 | `fail/complete`; `FM_RESTORATION_PARTIAL` | `not_applicable/complete` | B-10/R-07; no legal, frequency, or attackability finding. |

**B. Ownership and intervention receipt**

| Step/property | Diagnostic owner | Intervention — empowered owner | Tradeoff |
| --- | --- | --- | --- |
| 1/F0 | representation; evidence | Preserve provenance — interface and policy; acquire evidence — information service | Slower progression; acquisition workload. |
| 1/F4 | representation; representation | Surface material meaning — interface; maintain surfacing — interface | Reviewer context; provenance maintenance. |
| 2/F1 | permission rule; permission rule | Hold unsupported action — gate; require support — gate | Delayed disposition; longer supported disposition. |
| 2/F2 | simulation; simulation | Build Level C cohort pair — simulation; same | Cohort spillovers remain unresolved; same. |
| 3/F3 | process; process | Bind fail-closed review — review and gate; none in trace — policy if scope changes | Review consumes capacity; another progression path could require review. |
| 4/capacity-service | simulation; simulation | Add queues, resources, and paired policies — simulation; same | Modeling assumptions and computation; same. |
| 5/F5 | reassessment; process | Restore every consequence — restoration; none in trace — policy if progression occurs | Broader remediation; avoidance proves no restoration capability. |

### 7.8 Governance interventions and bounded transfer

Transformation and interface owners can preserve evidence state, provenance, and material disputes. Information-service owners can acquire missing evidence, while policy owners can pause or extend deadlines. Gate owners can make review fail closed; operational owners can reserve capacity, meter arrivals, or prioritize material uncertainty. Recovery owners can pause external action during contest, and restoration owners can repair consequences beyond the decision record. These controls are not interchangeable. Provenance increases interface complexity; evidence acquisition adds interactions and workload; fail-closed review accumulates unresolved cases; added capacity consumes resources; longer deadlines delay disposition; recovery pauses defer collection and prolong open cases; and restoration may require remediation outside the decision system.

The frozen transfer canary illustrates the same Level B procedure on a hypothetical LLM-generated vendor-access summary. The source bundle, routing rule, resources, and clock remain fixed while only the summary transformation changes. Its expected profile locates the first material failure where a fluent summary hides a disputed production restriction and contradictory scan, causing the common rule to omit verification and review and permit automatic provisioning. This author-constructed example demonstrates how the protocol represents a different vocabulary; it does not validate transfer, deployed-LLM prevalence, legality, strategic exploitation, or practitioner performance.

The protocol and examples are inspectable design artifacts, not evaluated usability interventions. The study does not assess adoption, efficiency, inter-rater reliability, or reproducible classification by unfamiliar users. Authors may use the worksheets and reference profiles for ordinary editorial checking, but no completed reader or project-lead return is treated as evidence or required for the paper. These materials support inspection, not evidence of human performance.

## Draft Traceability Notes (Not Article Prose)

| Draft element | Frozen or stored artifact |
| --- | --- |
| Levels, statuses, completeness, five steps, and report contract | `docs/PROCESS_RED_TEAM_PROTOCOL.md`, version `1.0` |
| Fixed worked-trace inputs and events | `docs/ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md`; `data/golden_traces/robodebt_worked_trace_v1.json` |
| Table 3 classifications, diagnostics, ownership, and tradeoffs | `docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md` |
| Prespecified trace selection and claim boundary | `docs/WORKED_TRACE_SELECTION.md` |
| LLM-summary transfer canary | `docs/TRANSFER_CANARY.md`; `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md` |
| Optional author editorial notes; not an article dependency | `docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md` |
