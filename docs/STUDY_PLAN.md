# Study Plan: Flexible Dynamic Uncertainty-to-Permission Kernel — Robodebt Application

Status: Slices 0-2 complete; Slice 3 engineering/design-freeze candidate complete; external pre-freeze gates pending; no confirmatory results exist

Working article title: *When Uncertainty Expands Authority: Formalizing and Stress-Testing Automated Decision Workflows Through Robodebt*

Target submission: Stanford CISAC/GTG edited volume, *Emerging Technologies and the Future of Decision-Making*

Deliverable: a 10,000-word extended research paper reporting a completed formal, computational, and case-grounded study—not a research-design essay or proposal

Completed precursor: the 1,500-word essay *When Uncertainty Expands Authority: How AI Workflows Can Reduce Scrutiny*, preserved in `../in_progress/uncertainty_expands_authority/when-uncertainty-expands-authority-final-revision.md`

Verified full-article deadline: 2026-12-18. `D-007` is closed; `docs/VENUE_CONTRACT.md` records the authoritative call, source hash, and word-count rule. The deadline does not alter hypotheses, estimands, or evidence standards.

## Extended-Paper Contract

This repository owns the 10,000-word paper. It does not reopen, replace, or silently rewrite the completed 1,500-word essay. The precursor supplies the motivating mechanism, bounded hypothesis, workflow-level unit of analysis, and initial two-phase test. The extended paper must preserve that intellectual continuity while making a substantially new contribution through formalization, documented institutional application, dynamic simulation, and reported results.

The precursor contains two nested claims that must remain distinct. The **base vulnerability** exists when a defensible representation suppresses a policy-relevant distinction and relaxes a safeguard. The vulnerability becomes **adversarially exploitable** only when an actor can induce the ambiguity, observe the resulting response, repeat the condition, and benefit. This paper formalizes and tests the base vulnerability and its operational safeguards. Robodebt grounds the institutional mechanism; it is not evidence that a strategic actor exploited the process. Process red-teaming is the evaluation method, not proof of a historical attack.

The 10,000-word paper is a completed research article. A formal model plus a proposed simulation design is insufficient. Submission requires executed confirmatory runs, uncertainty-aware results, negative controls, boundary analysis, limitations, and traceable support for every material claim. Robodebt is the source-grounded application through which the model and process-red-team method are instantiated and stress-tested; it is neither an engine dependency, a substitute thesis, nor a claim that the original essay was about Robodebt.

The extension must retain and sharpen four claims from the precursor:

1. Uncertainty does not inherently expand authority; representation and routing can make it do so.
2. The relevant unit of assurance is the evidence-to-action workflow, not model accuracy in isolation.
3. Weaker evidence should not, by itself, reduce safeguards or expand consequential automatic action.
4. Nominal human review is not meaningful control unless relevant uncertainty is visible and a reviewer can intervene in time.

The new paper must add four forms of evidence that the essay did not claim to provide:

1. a formal information order, action taxonomy, and robust-permission condition with scoped propositions and counterexamples;
2. a citation-level mapping of those constructs onto separate early and enhanced OCI application profiles, with every value distinguished as documented, inferred, stylized, or unsupported;
3. a validated finite-cohort discrete-event simulation that reveals queue, timing, access, burden, and restoration dynamics; and
4. reproducible empirical-demonstration results showing where safeguards hold, fail, or exchange one form of harm for another.

Before generalizing to Robodebt, the formal verification layer must reproduce the essay's exact held-output comparison in a **precursor-fidelity fixture**: keep the underlying case, uncertain model output, downstream rule, and process state fixed; vary only whether the interface preserves policy-relevant confidence and alternatives or emits the broad fallback representation; then compare surfacing, routing, scrutiny, review, and automatic permission. This fixture proves continuity of the construct, not empirical prevalence or attack.

### Working article architecture and word budget

Use the following 9,400-word article allocation as the drafting target and hold 600 words unassigned. The verified call sets a 10,000-word ceiling including endnotes and excluding bibliography. The reserve absorbs counted abstract text, captions, transitions, qualifications, and reviewer-required clarification without displacing a core evidence section. Treat tables, captions, and appendices as counted unless the publisher later states otherwise. Do not treat the reserve as a ninth section or spend it merely to reach the ceiling.

| Article function | Working words | Required job |
| --- | ---: | --- |
| Introduction and contribution | 700 | State the problem, thesis, completed-study design, findings, and contribution. |
| Mechanism, literature, and originality | 800 | State the bounded hypothesis from first principles and locate the formal and empirical contribution. |
| Formal model and propositions | 1,250 | Define only the constructs and three headline propositions needed to use and interpret the method. |
| Robodebt case and process mapping | 1,100 | Establish the documented early/enhanced OCI application and inference limits. |
| Dynamic simulation methods | 1,200 | Specify the design, policies, primary estimands, validation, freezing, and interpretation boundary. |
| Results | 1,850 | Report the three primary contrasts, queue boundaries, controls, uncertainty, and operational meaning. |
| Practical protocol and governance implications | 1,750 | Give the prespecified five-step protocol, fixed worked trace, diagnostic table, interventions, canary, and bounded AI transfer. |
| Limitations and conclusion | 750 | Bound the claims, identify residual uncertainty, and state the transferable result. |
| **Drafting subtotal** | **9,400** | **The planned main text before contingency is used.** |
| **Unallocated contingency** | **600** | **Reserved for counted abstract text, captions, transitions, and necessary qualification.** |
| **Submission ceiling** | **10,000** | **A full research paper whose practical method is usable from the main text.** |

## Objective

Develop and demonstrate an invariant-based process-red-team method for detecting when incomplete evidence, representation policy, administrative burden, review capacity, and deadlines permit an automated workflow to impose consequential action without robust evidentiary support.

The completed study will contain four connected contributions:

1. **Formal model:** define compatible latent states, evidentiary fidelity, formal authority, functional permission, operational action, effective review, surfacing, reversibility, and robust permission monotonicity.
2. **Executable verification layer:** check the formal properties on constrained structural examples and generate minimal counterexamples.
3. **Dynamic process-red-team simulation:** perturb evidence availability, notice and access conditions, provenance visibility, workload, deadlines, gate semantics, and restoration pathways in a finite-cohort organizational process.
4. **Document-grounded application:** load early and repaired Online Compliance Intervention profiles from the Australian Robodebt program through the same case-neutral configuration boundary used by synthetic profiles, compare them with declared counterfactual safeguards, and derive concrete governance implications for current automation and AI assurance.

The central computational result is not that an authored permissive rule behaves permissively. It is the boundary at which review ceases to deliver timely decisions, and whether that service failure becomes external harm depends on gate semantics, evidence acquisition, administrative access, and restoration design. A fail-closed gate may preserve safety while losing decision service; a fail-open gate may convert the same queue pressure into unsupported action.

The required end state is a reviewable formal specification, documented process map, validated discrete-event simulator, frozen scenario design, reproducible Monte Carlo results, boundary and tradeoff analyses, evidence packet, and submission-ready 10,000-word article.

## Revision Decision

This plan replaces an exhaustive static Cartesian grid as the primary computational result.

The static model remains valuable for:

- checking definitions;
- validating named policy profiles;
- proving or illustrating structural propositions;
- generating minimal counterexamples; and
- catching implementation errors.

It is not presented as an empirical discovery or as the main simulation. The main computational study is a stochastic discrete-event simulation of an organizational decision process under varying workload, evidentiary incompleteness, recipient response, record availability, and review design.

The simulation itself is the core red-team method. It systematically mutates the process and checks formal invariants under load. The prior three-way LLM protocol comparison is no longer a core contribution. A small audit-checklist ablation may run only after the formal, dynamic, and document-grounded evidence packet is complete.

## Flexible-Kernel Decision

The simulator is a **case-neutral study kernel with closed, versioned configuration contracts**. It is flexible enough to represent another evidence-to-action workflow without changing event-engine code, but it is not a general-purpose simulation platform, plugin system, or historical digital twin.

The architecture separates five owners:

1. **Kernel:** deterministic event ordering, finite-cohort execution, resources and queues, deadlines, evidence-state changes, action execution, keyed random draws, trace storage, and metrics.
2. **Formal evaluation specification:** compatible-state sets, support rules, materiality, review requirements, restoration obligations, and F0-F5 assessment. It remains independent of the operational profile.
3. **Process profile:** roles, stages, resources, queue disciplines, notice and access paths, deadline types, transition topology, and available action classes.
4. **Policy profile:** representation, routing, permission, gate, timeout, evidence-acquisition, correction, and restoration rules.
5. **Application adapter:** source references, dated terminology, documented transition bindings, provenance labels, and explicit mappings from an institutional case to the process and policy contracts.

Robodebt is the primary application adapter, not the source of kernel semantics. Canonical synthetic profiles establish the mechanism and exercise every core path before a Robodebt adapter is loaded. The same policy implementation IDs must behave identically under any semantically equivalent profile regardless of domain labels.

### Minimum defensible case threshold

An application is sufficient for implementation and eventual publication when authoritative or otherwise justified sources support:

- the evidence distinction and transformation being modeled;
- the consequential action and its routing or permission path;
- the relevant notice, access, review, deadline, correction, and restoration structure;
- the organizational roles and stopping authority needed for the claimed mechanism; and
- explicit boundaries around unresolved dates, transitions, quantities, and causal claims.

Exact historical rates, staffing, service-time distributions, engagement probabilities, and caseload reconstruction are not required. A historical profile may retain those fields as `unsupported`; it may not silently fill them. Executable experiments combine the historical structural adapter with a separate stylized scenario overlay whose values and sensitivity ranges are study-owned and visibly labeled.

### Case change and freeze rule

Before confirmatory freeze, the Robodebt mapping may be corrected, narrowed, or versioned if the source audit, application-sufficiency review, or executable trace checks reveal a material weakness. Such a change must be logged and must not require a kernel-code change unless it exposes a genuinely general missing construct. Replacing Robodebt as the selected primary application requires an explicit new plan and preregistration version; it is not an ordinary mapping edit. Before confirmatory execution, the selected application, source manifest, adapter version, parameter-provenance table, stylized overlays, worked-trace rule, and inference limits are frozen and hashed. Post-freeze case changes invalidate the affected confirmatory run.

This design permits implementation before every case detail is confirmed while preserving a strong publication boundary: the empirical demonstration is about declared mechanisms over declared parameter spaces, and the case establishes structural relevance rather than historical numerical estimation.

### Deterministic configuration compilation

The binding and precedence rules are canonical in `docs/CONFIGURATION_COMPILATION.md`. The simulator executes only a `CompiledConfiguration` produced from exact references to a process profile, active policy profile, independent evaluation specification, application mapping where applicable, and scenario overlay. Compilation emits a receipt for every runtime parameter slot. Documented values cannot be overwritten; fields marked `unsupported` contribute no executable value; stylized or sensitivity overlays may fill only declared unbound slots; duplicate owners, undeclared targets, and unresolved slots invalidate the configuration before trace execution.

Application source fixtures may describe topology and behavior together, but compilation separates them. `ProcessProfile` owns the capability graph. `PolicyProfile` owns active transformation, routing, permission, gate, timeout, correction, and restoration behavior. Counterfactual policies may select only capabilities declared by the process profile; a policy that needs new topology must select a separately versioned counterfactual process profile.

## Contribution And Evidence Hierarchy

### Primary theoretical contribution

A formal safety condition preventing weaker evidence from expanding automatic functional permission unless the action is robust across compatible refinements or passes an effective review, while still allowing precautionary, containment, and information-seeking actions.

Evidence: definitions, assumptions, characterization results, proof sketches, satisfying cases, and counterexamples.

### Primary computational contribution

A finite-cohort process-red-team simulation showing how evidentiary transformation policies interact with notice delivery, administrative access, endogenous recipient response, staff review, deadlines, evidence acquisition, debt action, recovery exposure, and reassessment.

Evidence: validated event traces, paired Monte Carlo experiments, queue and outcome metrics, sensitivity analyses, and boundary maps.

### Primary institutional contribution

A process-level mapping from the formal model to a documented early-OCI baseline and a documented enhanced-OCI repair profile, including roles, transitions, review points, authority, timing, and failure consequences.

Evidence: authoritative public sources, a source-anchored process map, a model-to-process crosswalk, and explicit limits on what is inferred.

### Optional audit contribution

An ablation testing whether adding the formal checklist to an otherwise identical system-audit prompt improves detection and localization of simulated failures.

Evidence: evaluator outputs and blinded semantic scoring. This optional component is not required for the article's central claims.

## Venue-Fit Contract

The study must illuminate concrete organizational or institutional consequences, not merely a theoretical possibility. It must also remain recognizably responsive to the accepted 1,500-word uncertainty-to-permission essay and to the venue's emphasis on emerging technology. Continuity means extending the essay's mechanism with new theory and evidence, not merely repeating its examples at greater length.

The article must therefore identify, for the documented workflow:

- which organizational role receives or loses information;
- which process transition changes;
- which action becomes automatic, review-gated, delayed, or unavailable;
- who retains stopping or override authority;
- how workload and deadlines affect that authority;
- where accountability is recorded; and
- which policy or system-design intervention follows.

The documented application does not reproduce the historical program, estimate unreported field quantities, or treat stylized simulation outputs as estimates of Robodebt outcomes. It uses the public record to anchor process structure and tests counterfactual governance designs under declared assumptions.

The article's emerging-technology contribution is the formal invariant and process-red-team method, not a claim that Robodebt used modern AI. The forward-looking policy analysis tests whether transparency, inspectable business rules, review, contestability, accountable ownership, and recovery pauses are sufficient once workload and access constraints are included. Services Australia's current automation and AI strategy supplies institutional continuity, not evidence that a current AI system reproduces Robodebt.

## Canonical Research Basis

The canonical precursor is the completed essay:

- `../in_progress/uncertainty_expands_authority/when-uncertainty-expands-authority-final-revision.md`

Treat its mechanism, bounded hypothesis, test logic, and stated limitations as the upstream claim contract. This repository may refine definitions or narrow claims when the formalization, sources, or results require it, but every material departure must be identified in the claim-boundary memo. Do not edit the precursor as part of this study.

The study operationalizes source material in the sibling `decision_space_writing` repository, especially:

- `../decision_space_writing/context/source-docs-md/paywall-writing-drafts-when-uncertainty-becomes-permission-aa1af0.md`
- `../decision_space_writing/context/source-docs-md/ideas-and-outlines-adversarial-manipulation-of-the-decision-space-stanford-ee91ba.md`
- `../decision_space_writing/context/source-docs-md/ideas-and-outlines-ied-spec-99319c.md`
- `../decision_space_writing/context/mechanisms/adversarial-decision-space-manipulation.md`
- `../decision_space_writing/context/mechanisms/red-team-review.md`
- `../decision_space_writing/context/concepts/decision-space-construction.md`
- `../decision_space_writing/context/concepts/decision-space-erosion.md`

Canonical mechanism:

> incomplete or aggregate evidence -> uncertainty-laundering representation -> routing or permission change -> burden and review-capacity interaction -> action and organizational outcome

Canonical design principle:

> Declining decision-relevant information must not expand automatic authority, although it may expand precautionary, containment, reversible information-seeking, or effectively review-gated action.

The study preserves the distinction between:

- **Decision-space erosion:** an option, case, warning, or review opportunity disappears before an authorized person can act on it.
- **Behavioral compression:** a person sees relevant alternatives but defers, anchors, or conforms.

The simulation models decision-space erosion and structural review opportunity. It does not model human cognitive deference.

## Research Questions

### RQ1: Robust formal conditions

When can an automatic consequential action be justified from incomplete evidence across every compatible refinement, and when does imputation instead create unsupported functional permission?

### RQ2: Operational review

When does a formally required review gate provide effective review and timely decision service once finite cohorts, queueing, deadlines, evidence access, and timeout semantics are included?

### RQ3: Organizational tradeoffs

How do claimant-led hold, impute-and-progress, fail-closed review, fail-open review, and agency-assisted information-first policies differ in evidentiary support, numerical error, delay, agency workload, recipient burden, recovery exposure, and correction?

### RQ4: Boundary conditions

At what combinations of evidentiary incompleteness, initiation load, administrative-access barriers, third-party record availability, and staff evidence access do review-preserving policies become overloaded, ineffective, or operationally costly?

### RQ5: Institutional application

Which roles, transitions, and authority relationships in the early and enhanced OCI processes can be defensibly mapped into the case-neutral contracts, which elements remain stylized or unsupported, and does the mapping require any case-specific engine behavior?

### RQ6: Process-red-team value

Which process mutations reveal violations that component accuracy checks or nominal human-review labels would miss, and which interventions prevent those violations under stress?

### Optional RQ7: Auditability

Does adding the formal permission-and-review checklist to the same generic audit protocol improve detection and causal localization of simulated failures?

## Formal Model

### Information states

Let `Theta` be the latent state space and `E` the evidence-state space.

For each evidence state `e`, define `Gamma(e) subset_of Theta` as the latent states compatible with that evidence under declared source and measurement assumptions. Evidence state `e_more` refines `e_less` only when:

```text
Gamma(e_more) subset_of Gamma(e_less)
```

and the relationship is produced by an explicit coarsening or garbling operation independent of the downstream permission rule. For Robodebt, `e_more` can contain fortnight-specific income and working dates while `e_less` contains an annual employer-income total and a broad employment period. In the finite reference model, use one or both of:

- hypothesis-set or partition refinement; and
- a declared many-to-one coarsening map `g` where `e_less = g(e_more)`.

If probabilistic states are included, the formal specification must state whether the relation is support refinement, calibrated distributional coarsening, or Blackwell-style garbling. Confidence scores alone do not establish the information order.

`Ref(e_less)` is the declared set of admissible finer evidence states compatible with `e_less`. Incomparable states and refinements excluded after observing the desired action are not used for monotonicity claims. Freezing alone is insufficient: each tested coarse state also requires an independently owned refinement-coverage certificate recording the generator or constraints, admissibility assumptions, exclusions, coverage argument, and constructive mode. Accepted modes are exact finite enumeration, symbolic exact constraints, a conservative outer approximation, or witness search. Witness search can prove failure from a validated admissible counterexample but cannot establish universal pass; a conservative-outer pass is sound, while its failure requires an independently validated admissible witness.

### Representations and decision rules

- Every stored formal, process, fixture, event, and result object uses a common versioned envelope containing object and schema identities and versions, owner, provenance status, versioned source references, and a canonical content hash.
- `rho(e)` produces the representation visible to downstream components. Every conforming material claim is typed as `observed`, `derived`, `imputed`, `disputed`, or `missing` and carries versioned source and assumption references. An explicitly represented untyped candidate field remains evaluable only so F0 can diagnose the failure rather than losing it during artifact parsing.
- `D(r, q, t)` maps representation `r`, process state `q`, and time `t` to routing and permission decisions.
- `Surfaced(r, q, u)` identifies the case, options, warnings, and uncertainty visible to role `u`.
- `Corresponds_sigma(v, m, a, e, q)` establishes, independently of the workflow, whether surfaced item `v` preserves the action-relevant meaning required by material item `m`. Accepted modes are exact ID with matching semantic fields, a frozen versioned mapping with an independently reviewable preservation rationale, or reproducible symbolic entailment in the forward direction from the surfaced semantics to the required meaning. Reverse implication, satisfiable overlap, display-text similarity, and the workflow's own materiality map are insufficient.
- `sigma` is an evaluation specification owned independently of `rho` and `D`. It supplies source-grounded or explicitly hypothetical action-support rules, evaluation materiality, required-meaning records, semantic correspondence, refinement coverage, baseline criteria, action-comparison fields, and F2 hold-intervention and alignment rules. The operational policy map remains a separate record of what the workflow actually implements.

Every event trace records a complete pre-event and post-event state, including evidence, representation, process state, time, policy, transformation, rule, evaluation-specification versions, and enabled and selected action instances. Any material state or version change requires support and permission to be reevaluated. Snapshot results are never carried across a transition by default.

Representation and decision rules are separate. A coarse label or imputed value is not intrinsically permissive; permission depends on how the downstream rule treats it. The Robodebt application therefore distinguishes observed fortnightly income from fortnightly income imputed by averaging aggregate annual data.

### Formal authority, functional permission, and operational action

Keep three concepts distinct:

- `L(q)`: actions legally or formally authorized in process state `q`, as established only by an authoritative source or a declared hypothetical rule;
- `P_auto(e, q)`: actions the workflow functionally permits to execute automatically given evidence `e`; and
- `X(case, t)`: actions actually executed in the simulated trace.

The simulator can establish a functional-permission or execution violation relative to the declared model. It does not determine historical legality. In the Robodebt application, legal conclusions and evidentiary requirements are source-attributed fields, not outputs inferred from numerical oracle error.

### Action classes and authority order

Do not classify actions only as consequential or nonconsequential. Each action is a fully instantiated instance with a stable instance ID that changes whenever a behaviorally material target, amount, scope, timing, authority condition, or consequence changes. Action sets use a declared finite-explicit, symbolic-constraint, or ordered-family representation. Ordered families require a frozen partial order and closure rule; no downward closure or substitutability is inferred. Each action has:

- actor;
- target;
- resource commitment;
- external consequence;
- reversibility window;
- authorization requirement;
- versioned source-rule references; and
- an authority-direction class.

Required authority-direction classes:

1. `progression`: advances mission or operational execution, commits resources, or imposes external effects;
2. `constraint`: pauses, blocks, contains, quarantines, or safely shuts down progression;
3. `information`: obtains additional evidence without independently creating the consequential outcome; and
4. `restoration`: reverses or repairs a prior state when still feasible.

Define `P_auto_progress(e, q)` as automatic progression actions that increase external commitment relative to the declared baseline. Precautionary braking, containment, and safe shutdown do not belong in this set merely because they are consequential.

### Effective review

A configured review gate and an effective review opportunity are distinct.

`ReviewEffective(case, action, t)` is true only when:

- the case is surfaced before automatic progression;
- relevant evidence and uncertainty are available to the reviewer;
- an identified reviewer has stopping, delaying, or modifying authority;
- the workflow enforces the dependency;
- review begins and completes before the action or deadline forecloses intervention; and
- the decision and any override are recorded.

The simulator records why a configured gate failed to become effective: queue delay, deadline expiry, missing evidence, missing authority, fail-open timeout, or process suppression. A review decision must bind the exact action instance, evidence and rule versions, authorization conditions, and expiry; changed material parameters or stale versions require recorded revalidation or a new review. At execution, the exact action must still belong to the current post-review action set and satisfy the independent support rule. A documented discretionary override counts only when its evidence, authority, reasons, and scope are encoded in `sigma`.

Also distinguish:

- `GateSafe`: the gate blocks automatic progression while its prerequisites remain unmet;
- `ReviewEffective`: an authorized reviewer can actually inspect and change the result in time; and
- `DecisionServiceEffective`: the process reaches a supported disposition within the declared service window.

A fail-closed overloaded gate may remain safe while both review and decision service become ineffective. A fail-open overloaded gate can lose all three.

### Base vulnerability and adversarial exploitability

Do not use “adversarial” as a synonym for harmful, automated, or red-teamed. The formal and simulation results establish the base uncertainty-to-permission vulnerability when representation or routing causes weaker evidence to relax a safeguard or expand unsupported automatic progression.

Classify the vulnerability as adversarially exploitable only when all four additional conditions are supported:

1. **Inducibility:** an actor can influence whether the workflow receives or produces the relevant ambiguity or coarse representation.
2. **Observability:** the actor can infer the downstream routing, scrutiny, delay, or permission response with enough reliability to adapt.
3. **Repeatability:** the actor can reproduce the condition or apply the learned strategy to relevant future cases.
4. **Benefit:** the resulting authority or scrutiny change advances the actor's objective.

These are claim-boundary fields, not assumed simulation parameters. The Robodebt application may establish the base vulnerability and organizational consequences without establishing any of the four attackability conditions. Red-team mutations test whether a process is structurally susceptible; they do not establish that a historical actor induced or exploited it.

### Precursor-fidelity fixture

`P0-Precursor` is the stable repository ID for a required executable compatibility fixture reproducing the short paper's exact counterfactual logic. In the manuscript, define it entirely from first principles as the **representation-preservation fixture**; reserve the repository ID for internal and supplementary artifacts:

- hold the underlying case, uncertain model output, downstream decision rule, and process state fixed;
- in `P0-Preserve`, retain confidence, policy-relevant alternatives, and provenance in the interface representation;
- in `P0-Fallback`, expose only the defensible broad fallback label;
- compare the surfaced alternatives, routing, scrutiny, review opportunity, and `P_auto_progress`; and
- include a negative-control rule under which both representations produce identical safeguards and permissions.

The fixture passes when the formal model can represent both the hypothesized authority expansion and the falsifying no-change case without changing the held model output. It is a continuity and regression check, not an empirical finding and not evidence of adversarial exploitation.

### Formal properties

#### F0: Evidentiary fidelity

A representation satisfies evidentiary fidelity only when:

- every claim typed `observed` is supplied by its declared source and retains source identity and version;
- every `derived` or `imputed` claim preserves its source evidence, transformation, assumptions, and compatible-state set;
- disputed and missing values remain distinguishable from zero or observed values; and
- downstream rules can inspect these types rather than receiving an untyped point value.

F0 identifies an uncertainty-laundering transformation. Whether that transformation creates a prohibited outcome depends on the downstream authority rule and the remaining properties.

#### F1: Robust automatic-permission monotonicity

For an evidence-sensitive progression action, automatic permission under `e_less` must be independently supported under every certified admissible refinement. Let `J_progress_sigma` be the progression actions supported by `sigma`, not the actions enabled or selected by the workflow:

```text
P_auto_progress(e_less, q)
    subset_of intersection(
        J_progress_sigma(e_more, q)
        for e_more in Ref(e_less)
    )
```

Weaker information must not introduce an automatic progression action that the independent support rule excludes under at least one compatible finer state. The refinement set is frozen and its coverage certified before policy outcomes are inspected. A uniformly permissive workflow cannot certify itself merely by permitting the action under every state.

#### F2: Safe fallback allowance

Declining information may introduce constraint, containment, and information-seeking actions when an explicit execute-versus-hold intervention pair over a complete frozen intervention unit, under identical cohort membership and keyed exogenous inputs, shows that they cannot newly release a progression action outside the robust support envelope recomputed at the later action's own pre-state. The two arms share one intervention-pair ID. The hold intervention applies none of the tested fallback's direct effects or action-rooted descendants and cannot be replaced by another active policy. A case-local pair supports only a within-case result and requires a frozen noninterference certificate; any action that can change shared queues, capacity, deadline service, timeouts, or another case requires a cohort-system pair. Paired system states align on the sorted union of branch-independent causal cuts derived from relative time, event priority, and stable causal-event keys, never on event index. The causal comparison ends for each affected case immediately before its earliest frozen new-evidence, review, authorization, separate-intervention, or horizon boundary.

#### F3: Review-preserved progression

A newly available progression action is outside F1 when it is unavailable automatically and can occur only after an effective prior review event applying a declared evidence rule. It belongs to the post-review action set. F3 additionally requires the recorded review to authorize the exact current action instance and versions, the action to remain in the current post-review set at execution, and independent support to remain true in that execution state. A reviewer who merely confirms an imputed value without the required evidence, reviews a different amount or stale rule version, authorizes an action whose current eligibility has lapsed, or authorizes an action unsupported in the execution state does not satisfy this property.

#### F4: Surfacing preservation

Abstraction or operational policy must not remove an item designated material by the independent evaluation specification from every authorized reviewer before progression or deadline expiry. A surfaced item counts only when exact semantic IDs and fields agree, a frozen mapping supplies an independently reviewable preservation rationale, or the surfaced semantics directionally entail the required action-relevant meaning. Reverse implication or semantic overlap is insufficient. `sigma` owns the required intervention-capability type and surfacing deadline; the process model supplies actual role assignment, authority possession, and event timing. Operational and evaluation materiality are compared explicitly so the workflow cannot pass by omitting an inconvenient item from its own map or by substituting a semantically inadequate broad label.

#### F5: Contestability and restoration

An action described as reviewable or reversible must have a feasible operation that can halt or modify it within its declared time window. Report structural path existence, prospective probability of operational access and completion against a frozen reliability threshold, realized path availability, correction uptake, and restoration separately. Before a realized contestability or restoration horizon expires, an unresolved component returns `status = unassessable` with `FM_EVALUATION_HORIZON_PENDING`, not failure. `RestorationComplete` is true only when the relevant decision state, monetary state, recovery status, and other modeled external consequences are restored. Debt reduction or zeroing alone may be only partial restoration.

Every F0–F5 evaluator uses the common typed assessment envelope and the property contract matrix in `docs/FORMAL_MODEL.md`. It first reads the frozen scope declaration, then validates the inputs and `sigma` components needed to resolve a conditional antecedent, then—only when the property applies—evaluates independently decidable conditions and records missing or invalid material. An explicit scope exclusion or demonstrably false fully resolved antecedent yields `not_applicable`; an unknown scope declaration, missing required input, and invalid evaluation specification yield distinct stable diagnostics. Status and completeness are separate: a sufficient known counterexample yields `fail` even when another conjunct is incomplete, while `unassessable` means no sufficient pass or failure conclusion is available. Helper outcomes such as `GateSafe` and `ReviewEffective` store status separately from any boolean value and are bound as conjunctive, alternative, or contextual components. Unknown item statuses, missing applicable items, undeclared component relations, or incorrect aggregation produce a blocking invalid-completeness diagnostic.

### Formal result agenda

1. **Fidelity result:** point imputation from aggregate evidence violates F0 when unsupported distinctions are presented downstream as observations or lose inspectable provenance and assumptions.
2. **Robust-permission result:** F1 fails when a coarse evidence state permits automatic progression that the independent support rule excludes under at least one certified admissible refinement.
3. **Safe-fallback result:** additional constraint or information actions can be permitted under declining information when frozen execute-versus-hold system traces aligned by branch-independent causal cuts show they cannot causally release progression for the focal or spillover cases outside the envelope recomputed at the later pre-state.
4. **Structural-gate result:** an enforced fail-closed pre-action gate preserves `GateSafe`, independent of later reviewer judgment, but does not guarantee effective review or timely decision service.
5. **Nominal-review result:** notification, recipient response opportunity, nonblocking review, stale, action-mismatched, execution-state-ineligible, or execution-state-unsupported authorization, post-action reassessment, or a fail-open timeout does not establish F3.
6. **Queue-instability result:** when review-bound arrival rate persistently exceeds effective service capacity, review delay and deadline failure cannot remain bounded without admission control, prioritization, additional capacity, information acquisition, or policy change.
7. **Restoration result:** correcting the decision state does not establish complete restoration when recovery exposure or another modeled consequence remains after the frozen restoration horizon; an unresolved pre-horizon state is not prematurely failed.
8. **Erosion result:** a case can violate F4 even when action-set counts remain unchanged.

Each result must include explicit assumptions, a proof or bounded proof sketch, a satisfying case, a boundary or counterexample, and an executable check where applicable.

The representation-preservation fixture is reported before the formal results. Keep `P0-Precursor` out of reader-facing prose, and do not count its authored permissive route as a substantive discovery.

### Practical application levels and claim limits

The practitioner method uses the least demanding level capable of supporting the intended conclusion:

1. **Level A — document audit:** maps evidence, representation, declared permission, configured gates, roles, deadlines, and formal correction paths. It can support structural findings and explicit missing-documentation findings, but not realized effectiveness, capacity boundaries, spillovers, or prevalence.
2. **Level B — bounded deterministic trace:** adds versioned cases, ordered events through a declared boundary, complete pre/post states for recorded events, exact actions, available review decisions, and completed or explicitly incomplete horizons. It can support trace-specific property findings within that boundary, but not population frequencies, claims beyond the trace horizon, or shared-resource effects. A case-local F2 claim additionally requires a valid noninterference certificate and remains within-case only.
3. **Level C — dynamic system simulation:** adds complete system state, cohorts, shared queues and resources, keyed exogenous draws, event execution rules, and paired interventions. It can estimate capacity boundaries and system effects within the designed parameter space, but not historical prevalence, legality, or unmodeled real-world causation.

The frozen protocol in `docs/PROCESS_RED_TEAM_PROTOCOL.md` owns the intake fields, escalation rules, and practitioner report. Its output is a vector of property and helper assessments, interventions, owners, and tradeoffs—not a composite compliance score or weighted policy ranking. A property that is in or potentially in scope but lacks required inputs is `unassessable`. A conclusion deliberately outside the selected level is recorded separately as `evaluation_state = omitted_by_claim_limit`, receives no formal status, and names the required escalation; lower-level evidence may not be silently promoted.

## Dynamic Organizational Process-Red-Team Model

### Process entities

The discrete-event model contains:

- initiated income-discrepancy cases;
- latent case states used only to score simulated outcomes;
- annual aggregate and fortnight-specific evidence states;
- latent notice-delivery, digital-access, comprehension, record-access, vulnerability, and engagement characteristics;
- representation policies;
- downstream routing and permission rules;
- recipient notice and response processes;
- recipient- and agency-led evidence acquisition;
- data-matching, staff-assistance, pre-debt review, recovery, and reassessment resources;
- documented 21-day early-OCI and 28-day enhanced-OCI response rules, including extensions where the source profile supports them;
- authority gates and timeout behavior;
- debt calculation, debt raising, recovery, constraint, information, and restoration actions; and
- terminal and intermediate outcomes.

Latent states and error rates are synthetic unless a documented source supports a parameter. They exist to compare policies under declared conditions, not to estimate deployed-system performance.

### Robodebt scenario construction and oracle

Within the Robodebt application, each simulated case begins with a latent fortnight-level income trajectory, benefit-entitlement history, and administrative-access profile stored as semantically identified generic case attributes. The application scenario generator derives the annual employer-income aggregate and broad employment-period evidence from that same trajectory, masks or exposes period-specific records according to the scenario, and supplies an identical initial evidence bundle and latent-access profile to every paired policy. The kernel does not require income, benefit, recipient, or debt fields.

The full-information numerical oracle recomputes an oracle-positive or oracle-negative outcome and amount from the latent fortnight-level trajectory under the declared stylized benefit rule. It is used only for simulation scoring. Policies never observe latent values unless a modeled evidence event reveals them.

This construction makes three quantities auditable:

- whether the declared stylized rule is oracle-positive or oracle-negative;
- how much a calculation based on imputed values differs from the oracle amount; and
- whether later evidence or reassessment can correct the difference.

Numerical oracle correctness, evidentiary sufficiency, and legal validity are separate fields. The benefit rule is a transparent stylized function unless Slice 0 identifies an authoritative, feasible specification. The simulator must not imply that its monetary outputs reproduce historical Robodebt calculations or determine whether a historical debt was lawful.

### Endogenous engagement model

Recipient engagement is an outcome of case characteristics and process design, not a policy-invariant Bernoulli draw. Each case receives shared latent uniforms and characteristics for notice delivery, digital access, comprehension, record availability, response effort, and extension need. Each policy maps those same exogenous draws through its communication, assistance, deadline, and evidence-burden rules to produce policy-specific events.

This design permits paired comparison without assuming that assistance, notice quality, or burden cannot affect response. The model reports engagement failure by reason rather than using nonresponse as a single undifferentiated state.

### Event types

The closed kernel event families are:

- `CASE_ARRIVAL`
- `SOURCE_EVIDENCE_INGESTED`
- `NOTICE_SENT`
- `NOTICE_DELIVERED`
- `NOTICE_FAILED`
- `ACCESS_ATTEMPTED`
- `SUBJECT_RESPONDED`
- `SUBJECT_NONRESPONSE`
- `EXTENSION_REQUESTED`
- `EXTENSION_GRANTED`
- `REPRESENTATION_APPLIED`
- `EVIDENCE_REQUESTED`
- `EVIDENCE_SUBMITTED`
- `EVIDENCE_ACCEPTED`
- `EVIDENCE_REJECTED`
- `EXTERNAL_EVIDENCE_RETURNED`
- `REVIEW_QUEUED`
- `REVIEW_STARTED`
- `REVIEW_COMPLETED`
- `DEADLINE_REACHED`
- `ACTION_COMPUTED`
- `PROGRESSION_EXECUTED`
- `EXTERNAL_CONSEQUENCE_STARTED`
- `EXTERNAL_CONSEQUENCE_UPDATED`
- `CORRECTION_REQUESTED`
- `RESTORATION_EXECUTED`
- `CASE_CLOSED`

Debt calculation, debt assertion, recovery, payment, reassessment, reduction, and zeroing are application-specific action types carried by these generic event families; they are not closed kernel event IDs. Each event preserves a typed event ID, case ID where applicable, event time, event priority and registry, unique branch-independent causal-event key, root exogenous-event or intervention ID, descendant path, microstep and transition ranks, prior state, new state, actor, action IDs, role-bound transformation/decision/transition rule executions, evidence IDs, policy ID, intervention pair and arm, and random-stream provenance. Causal keys are derived from stable causes rather than queue position or branch label so divergent F2 traces remain alignable. Every scenario freezes finite horizon, same-time microstep, causal-depth, and event-count bounds. Duplicate causal keys, zero-time cycles, or bound breaches invalidate the run rather than becoming ordinary censoring.

### Queue and timing model

The primary implementation is a transparent discrete-event simulator using a deterministic event queue and seeded random streams. Avoid a large simulation framework unless the pilot demonstrates a concrete need.

The primary study uses finite cohorts, not a steady-state warm-up design. The model must support:

- configurable cohort size, initiation window, and batch structure;
- policy-dependent recipient engagement hazards derived from shared latent traits and uniforms;
- multiple service resources for assistance, review, recovery, and reassessment;
- queue discipline, capacity, and priority at each staffed stage;
- third-party evidence-retrieval latency and success;
- documented profile-specific response deadlines and extension rules;
- recovery and correction windows; and
- hold-without-debt or impute-and-raise behavior at deadline expiry.

After the initiation window closes, the simulation drains events to a frozen administrative cutoff. Open cases are right-censored with reason codes; they are not silently classified as resolved. The primary load factor scales a declared stage-capacity vector. Stage-specific bottlenecks are sensitivity analyses.

Random draws are keyed by stable case ID, event family, and draw index rather than consumed from queue-order-dependent streams. A policy may change whether an event occurs without shifting unrelated draws for that case or another case.

Validate simple limiting cases against analytical queueing results or hand-computable event traces before running the factorial experiment.

### Historical process profiles

Historical profiles are source-validation fixtures, not policy candidates and not estimates of unreported historical outcomes.

#### R-OCI-Early: July 2016 to January 2017 reference

- 21-day initial response rule measured from the letter date;
- online confirmation or correction of ATO employment information;
- averaging across the employer-reported period after no or incomplete response;
- automatic debt notice and commencement of normal recovery where a debt is calculated;
- documented initial communication, access, and manual-intervention rules; and
- period-specific recovery-fee behavior only where the source manifest supports it.

#### R-OCI-Enhanced: documented early-2017 repair profile

- 28 days from receipt, clearer extensions and assistance;
- strengthened delivery and contact measures;
- clearer communication about averaging and possible debt;
- expanded manual-intervention triggers for disputed or complex cases; and
- updated recovery-fee and review practices as documented.

Slice 0 freezes exact start and end dates, source anchors, and unresolved ambiguities for both profiles. EIC, CUPI, PAYG Manual, and later remediation processes are not blended into either profile; they are separate documented variants if used.

### Counterfactual policy profiles

#### U0: Claimant-led evidence and hold

- treat an unresolved aggregate mismatch as insufficient evidence for debt action;
- preserve observed, missing, disputed, and imputed status;
- permit recipient-submitted evidence, extensions, and review but do not proactively retrieve third-party records; and
- hold without debt or recovery when period-specific support remains insufficient.

#### U1: Impute and progress failure benchmark

- average aggregate income across assumed fortnights;
- permit the imputed values to satisfy the calculation rule;
- raise the calculated debt after the response deadline; and
- omit an effective pre-debt staff-review dependency.

U1 is a diagnostic failure benchmark, not a normatively admissible policy alternative for the historical Robodebt setting.

#### U2C: Impute, review, and fail closed

- retain the imputation flag, assumptions, compatible-state set, and source provenance;
- require staff review with stopping authority before debt raising or recovery;
- authorize debt action only when period-specific evidence satisfies the declared evidence rule;
- request information or hold when the evidence rule is not satisfied; and
- remain closed when review is incomplete at the deadline.

#### U2O: Impute, review, and fail open

- use the same review rule, evidence access, and staffing as U2C;
- allow imputed debt action when the configured review has not completed by timeout; and
- retain a traceable reason code identifying queue delay, missing evidence, or another failed prerequisite.

U2O is a core stress-test comparator, not a recommended policy.

#### U3: Agency-assisted information first

- preserve insufficient-evidence status;
- use confirmed notice delivery, accessible assistance, and extensions when the modeled recipient cannot complete the evidence process within the default window;
- proactively obtain employer, bank, or other period-specific records using modeled agency powers and assistance resources;
- triage unresolved cases to staff review under the same evidence rule as U2C; and
- prohibit debt raising or recovery until period-specific evidence supports the calculation.

The five U-policy profiles are counterfactual designs. The R profiles own historical-process claims. Reviewer error, rubber-stamping, and departures from the declared evidence rule are sensitivity mutations, not silently assumed behavior.

## Document-Grounded Process Application: Robodebt

### Selected case and scope

The selected primary application is Australia's Robodebt program. The primary historical reference is the early OCI process from July 2016 through January 2017; the documented enhanced OCI process in early 2017 is an as-documented repair bundle with mixed activation precision, not a claim that every change began simultaneously. This pairing is suitable because the public record documents evidentiary transformation, notice and access, response timing, automation and staff roles, debt action, recovery, manual intervention, and later reassessment.

The study models the following documented mechanism at process level:

```text
annual employer-income match
    -> request for period-specific information
    -> notice, access, evidence, and response process
    -> missing or inadequate period-specific information by deadline
    -> annual income averaged across assumed fortnights
    -> apparent fortnightly discrepancy and debt calculation
    -> debt raising and possible recovery
    -> later reassessment, reduction, or zeroing when better evidence arrives
```

The historical case is a rule-based automated administrative decision system, not a modern generative-AI deployment. Its value is as a documented instance of evidentiary transformation, scaled automation, administrative burden shifting, and contestability failure. The formal invariant and red-team perturbations are intended for contemporary AI-enabled workflows; transfer remains a bounded analytical claim, not field equivalence.

### Three-axis validity rule

Never use one label to collapse:

1. **Evidentiary support:** whether the declared period-specific evidence rule is satisfied at the moment of action;
2. **Numerical correctness:** whether the simulated amount agrees with the stylized full-information oracle; and
3. **Legal validity:** what authoritative sources establish about the historical process and applicable law.

A simulated amount can equal the oracle while remaining evidentially unsupported. Conversely, numerical disagreement with the stylized oracle is not a legal conclusion. Historical legal findings are quoted or paraphrased from the Royal Commission, Ombudsman, or other authoritative source and never generated by the simulator.

### Formal crosswalk

| Model construct | Robodebt instantiation |
| --- | --- |
| `e_less` | annual employer-income total and broad employment-period information |
| `e_more` | fortnight-specific income and working dates supported by payslips, bank records, employer records, or equivalent evidence |
| `rho(e_less)` | evenly apportioned or otherwise assumed fortnightly income values derived from aggregate data |
| formal authority `L(q)` | source-attributed legal authority or constraint; never inferred from simulation output |
| functional permission `P_auto` | workflow permits debt raising, recovery, or another external action automatically |
| operational action `X` | debt notice, recovery action, payment, hold, review, or correction appearing in the event trace |
| information action | request or agency-assisted retrieval of period-specific records |
| constraint action | hold without debt or pause recovery while evidence or review is pending |
| effective review | authorized staff review of provenance, uncertainty, and relevant records before debt or recovery |
| restoration | reassessment that reduces or zeros a debt, plus separately measured repair of recovery and other modeled consequences |

### Documented process stages to encode

1. data matching and discrepancy initiation;
2. recipient notification, delivery, access, and the profile-specific 21- or 28-day response rule;
3. recipient or agency acquisition of period-specific evidence;
4. income representation and debt calculation;
5. staff assistance or review where routed;
6. debt raising and recovery action; and
7. reassessment, review, reduction, or zeroing.

Slice 0 must distinguish what changed across program periods rather than collapse all historical implementations into one workflow. R-OCI-Early and R-OCI-Enhanced are distinct source fixtures. Any EIC, CUPI, PAYG Manual, remediation, or later review process requires its own profile ID and dated source crosswalk.

### Authoritative source packet

The minimum fixed source packet is:

- Royal Commission into the Robodebt Scheme, [Report](https://robodebt.royalcommission.gov.au/publications/report);
- Royal Commission into the Robodebt Scheme, [Deloitte Robodebt Process Maps](https://robodebt.royalcommission.gov.au/publications/deloitte-robodebt-process-maps), including separate population, identity, income-matching, and debt-calculation maps for OCI and later variants;
- Commonwealth Ombudsman, [Centrelink's Automated Debt Raising and Recovery System, April 2017](https://www.ombudsman.gov.au/__data/assets/pdf_file/0022/43528/Report-Centrelinks-automated-debt-raising-and-recovery-system-April-2017.pdf);
- Commonwealth Ombudsman, [Centrelink's Automated Debt Raising and Recovery System: Implementation Report](https://www.ombudsman.gov.au/__data/assets/pdf_file/0027/286551/Centrelinks-Automated-Debt-Raising-and-Recovery-System.pdf);
- Commonwealth Ombudsman, [Income Apportionment: Lawfulness of Income Apportionment Decisions](https://www.ombudsman.gov.au/__data/assets/pdf_file/0040/299947/Income-Apportionment-Lawfulness.pdf);
- Services Australia, [Information about Robodebt](https://www.servicesaustralia.gov.au/information-about-robodebt?context=60271); and
- Services Australia, [Automation and AI Strategy 2025–27](https://www.servicesaustralia.gov.au/sites/default/files/2025-05/automation-and-ai-strategy-2025-27.pdf), used only for current governance context.

Slice 0 creates a page-, paragraph-, or process-map-node-level source manifest. The Royal Commission and Ombudsman reports own historical and legal claims; the study does not independently re-adjudicate lawfulness.

### Source-sufficiency gate

Before process-code implementation, the Robodebt application must have:

- separate source-anchored diagrams for R-OCI-Early and R-OCI-Enhanced with dates stated;
- explicit role, transition, evidence, deadline, review, debt, recovery, and reassessment anchors;
- a clear mapping to the formal variables;
- a provenance level for every parameter and transition;
- a three-axis classification for each historical or simulated outcome claim; and
- a limitations table identifying every inferred, stylized, or unsupported element.

If the authoritative record cannot support coherent, distinct early and enhanced OCI profiles by the end of Slice 0, stop and narrow the profiles rather than silently blending periods or substituting another case.

### Calibration rule

Documented sources determine process structure wherever possible. Numerical parameters use this hierarchy:

1. directly documented value;
2. documented plausible range;
3. clearly labeled stylized range; or
4. sensitivity parameter with no empirical interpretation.

Never present stylized queue, error, or deadline values as measurements of the documented organization.

## Experimental Design

### Core process-red-team perturbations

The red team does not invent prose findings. It applies deterministic, parameterized mutations to a valid base process and checks which invariant, role, queue, or outcome changes. Every mutation has a stable ID, target stage, expected detectable property, and matched unmutated control.

Required perturbation families are:

1. **Precursor representation-only bridge:** hold the underlying case, uncertain output or evidence bundle, downstream rule, and process state fixed while switching between an uncertainty-preserving representation and a broad fallback representation.
2. **Evidence degradation:** remove period-specific records while preserving the annual aggregate.
3. **Provenance laundering:** retain the same numeric imputation but strip or mistype its inferential status.
4. **Administrative-access failure:** alter notice delivery, digital access, evidence availability, comprehension, or extension need.
5. **Load stress:** increase cohort volume or reduce one declared stage capacity.
6. **Gate mutation:** switch fail-closed to fail-open, remove stopping authority, or move review after action.
7. **Restoration mutation:** delay reassessment, begin recovery earlier, or leave residual consequences after debt correction.

For each family, report whether ordinary component-local checks could still pass—for example, the annual total matches, the calculation follows its programmed rule, or a review field is configured—while F0-F5 or an operational outcome fails. This contrast is the core evidence that process-level red teaming adds value beyond component verification.

### Scenario family

A scenario family fixes the organizational environment and generates the same cases, latent income and access characteristics, potential evidence, service requirements, and keyed random draws for every policy. Realized response, evidence, queue, and action events may differ because policy changes the process. Policies are paired using common random numbers without requiring identical endogenous event streams.

Primary environmental factors:

| Factor | Core levels |
| --- | --- |
| Case-initiation load relative to the declared stage-capacity vector | low `0.6`; near-capacity `0.95`; overloaded `1.2` |
| Cases lacking fortnight-specific evidence at initiation | low `0.10`; medium `0.30`; high `0.50` |
| Prevalence of administrative-access barriers | low `0.10`; medium `0.30`; high `0.50` |
| Third-party period-specific evidence retrievability | low; high |
| Staff access to evidence and provenance | partial; complete |

The nominal core contains `3 x 3 x 3 x 2 x 2 = 108` environmental scenario families. Each valid family runs all five U policies, for up to 540 paired policy conditions. R-OCI-Early and R-OCI-Enhanced run as source-validation profiles on a smaller frozen fixture set and do not inflate the confirmatory counterfactual count.

The core U-policy comparison uses the early-OCI 21-day response clock as its documented reference environment. The enhanced 28-day timing and associated repair mechanisms are evaluated first as the R-OCI-Enhanced fixture and then, if the source crosswalk is complete, as a prespecified documented-variant analysis. Deadline changes are never interpreted independently of the other process changes that accompanied them.

These core factor levels are preregistered stylized conditions unless the Slice 0 source manifest upgrades a value's provenance. The early-OCI 21-day and enhanced-OCI 28-day rules are profile-specific documented structures, not a claim that all Robodebt processes used one deadline. Factor percentages are not estimates of historical Robodebt frequencies or capacities.

The scenario generator must apply semantic validity constraints. The final valid count is frozen after the pilot; a target cardinality is not itself a scientific acceptance criterion.

### Negative controls

Add matched controls in which:

- the aggregate match agrees with full-information fortnightly income;
- an imputed case is independently verified before debt action;
- the case is oracle-negative under both evidence states;
- only information or containment actions change;
- review is not required because no progression threshold is crossed; or
- representation changes but routing and permission do not.

Controls are reported separately and do not inflate the primary scenario count.

### Simulation horizon and replications

Each replicate contains:

- a finite case-initiation window or frozen cohort;
- a frozen administrative follow-up cutoff;
- a rule for draining events after initiation stops; and
- explicit right-censoring for open evidence, review, recovery, or reassessment states.

Begin with 30 seeded replications per scenario family, using common random numbers across policies. Before freeze, set:

- cohort size and initiation window;
- administrative cutoff and event-drain rule;
- right-censoring treatment;
- minimum replications;
- maximum replications, no greater than 100 per family;
- Monte Carlo standard-error targets for primary rates; and
- the rule for extending all paired policies when a family has insufficient precision.

No scenario receives additional replications because its result is surprising or favorable.

### Primary outcomes

#### Evidentiary and functional permission

- robust-permission violations per 1,000 cases;
- actions based on untyped or provenance-suppressed imputation;
- debts raised without the declared period-specific evidentiary support per 1,000 initiated cases;
- configured-gate, `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective` rates;
- pre-debt review-bypass rate;
- provenance- or uncertainty-surfacing loss rate;
- recovery begun before effective review or reassessment; and
- source-attributed legal-status category reported separately from simulated metrics.

#### Numerical decision outcome

- oracle-positive and oracle-negative disposition rates;
- signed and absolute amount error relative to the stylized full-information oracle;
- false action and missed action relative to that oracle;
- late but otherwise oracle-consistent disposition; and
- result stratification by evidentiary-support status.

#### Organizational process

- queue length and waiting-time distribution;
- staff-assistance, pre-debt review, and reassessment utilization;
- deadline-expiry rate;
- throughput;
- cases held without debt pending evidence or review;
- information-acquisition demand and latency;
- cases remaining unresolved;
- notice-delivery and digital-access failures;
- recipient contacts, evidence requests, estimated evidence-production effort, and extensions; and
- time from initiation or debt raising to correction.

#### Recovery exposure and restoration

- days under asserted debt before correction;
- amount recovered before correction;
- recovery fee, collection, or payment exposure when modeled;
- reassessment opportunity, debt reduction, and debt zeroing;
- partial versus complete restoration; and
- unresolved external consequences at the administrative cutoff.

No single weighted utility or scalar policy-regret measure is primary. Report evidentiary support, numerical error, timeliness, agency workload, recipient burden, recovery exposure, and restoration as a vector. Any scalar loss function or Pareto ranking is a sensitivity analysis with explicit normative assumptions. U1 and U2O remain failure comparators even if a stylized throughput metric favors them.

### Primary estimands

1. Capacity boundary at which U2C preserves `GateSafe` but loses effective review or timely decision service.
2. U2O versus U2C difference in robust-permission violations and recovery exposure as the same queues approach overload.
3. U3 versus U0 difference in recipient burden, agency workload, evidentiary support, time to supported disposition, and numerical error.
4. Interaction between policy and administrative-access barriers.
5. Interaction between policy and third-party evidence retrievability.
6. Difference among configured review, `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective`.
7. Difference between early and enhanced OCI fixture traces on documented repair mechanisms, without treating the fixtures as population estimates.

### Hypotheses

- **H1:** As review-bound load rises, U2C retains gate safety but exhibits a capacity boundary beyond which effective review and timely decision service decline sharply while unresolved holds grow.
- **H2:** Under identical cases and service requirements, U2O converts a larger share of queue delay into robust-permission violations and recovery exposure than U2C.
- **H3:** U3 reduces recipient evidence-production burden and action without period-specific support relative to U0 when agency retrieval succeeds within the service window, but increases agency workload and can delay disposition when retrieval is slow or unsuccessful.
- **H4:** Administrative-access barriers reduce engagement under every policy, but clear notice, extensions, and agency assistance reduce the disparity relative to otherwise matched cases.
- **H5:** Complete staff access to provenance and evidence improves effective-review opportunity relative to partial access even when the configured gate and staffing are unchanged.
- **V1:** U1 produces more action through imputation than U0 under enabling-rule fixtures; this is an implementation validation check, not a substantive discovery.
- **V2:** Verified-match and no-action controls do not exhibit robust-permission violations.

H1-H3 are primary. H4-H5 are secondary. V1-V2 are validation expectations.

### Sensitivity analyses

Only after the core design freezes:

- information-acquisition latency and success;
- number and heterogeneity of assistance, review, and reassessment staff;
- priority queue versus first-in-first-out at each staffed stage;
- bursty rather than stationary arrivals;
- documented 21-day versus 28-day profile rules, followed by counterfactual 14- or 56-day deadlines only if useful;
- alternate recovery and correction windows;
- reviewer decision accuracy as a stylized range;
- reviewer rubber-stamping or evidence-rule departure as explicit adversarial mutations;
- alternate latent-state prevalence;
- alternate income-apportionment or default-assumption transformations;
- heterogeneity within administrative-access and vulnerability strata beyond the core prevalence factor; and
- documented process-period variants when source support is sufficient.

Sensitivity analyses must not be blended into the confirmatory core.

## Optional Audit-Checklist Ablation

Run only if the primary evidence packet is complete by the start of Week 6.

### Design

Select 36 episodes from frozen simulation traces:

- 12 functional-permission, fidelity, or surfacing failures;
- 12 matched repaired episodes; and
- 12 benign or overload-only controls.

Compare two prompts:

- `A0`: generic system-safety audit; and
- `A1`: the identical audit plus the formal F0-F5 checklist.

Keep evidence, prompt structure, output schema, model, budget, parser, and task order identical. The only intended treatment is the added checklist.

Maximum primary calls: `36 x 2 = 72`.

### Outcomes

- joint detection and correct causal localization;
- false positives on repaired and benign episodes;
- mitigation replay success; and
- invalid or abstaining output.

Double-code at least half of the optional outputs if this analysis is reported. Results are evaluator-specific and secondary. If the ablation is not completed, remove it cleanly rather than leaving a partial subsystem.

## Statistical Analysis

### Monte Carlo analysis

- Pair policies within scenario family and random seed.
- Report rates, paired differences, uncertainty intervals, and Monte Carlo standard errors.
- Use scenario family as the generalization unit for cross-scenario summaries.
- Separate stochastic uncertainty within a scenario from variation across scenario assumptions.
- Report boundary surfaces and interaction plots, not only grand averages.
- Show the region where review is structurally configured but operationally ineffective.
- Report U2C and U2O separately; never pool fail-closed safety with fail-open timeout behavior.
- Keep negative controls separate from enabling-rule scenarios.
- Report right-censoring and unresolved states by reason and policy.

### Model validation

Required validation includes:

- exact hand traces for small deterministic cases;
- limiting cases with zero initiations, infinite staff capacity, zero service time, complete evidence, universal response, and no deadlines;
- comparison with an analytical M/M/1 or equivalent queue case where assumptions align;
- conservation checks for cases and events;
- repeated-seed reproducibility;
- common-random-number pairing checks; and
- keyed-draw invariance when policy changes the number or order of endogenous events;
- implementation comparison against a slower reference simulator for a small fixture set.

### Interpretation rule

Simulation estimates apply to the declared model and parameter ranges. Document grounding supports structural relevance, not numeric field prediction, unless a parameter is directly sourced. Evidentiary-support and numerical-oracle metrics are simulation outputs; historical legal conclusions remain source-attributed facts.

## Schemas And Fact Ownership

### Required contracts

- `(schema_id = formal_model, schema_version = 1)`: shared `RecordRef`, `RecordMeta`, `StoredRecord`, typed field/representation, compatible-state, role-bound executable-rule, scope-declaration, truth/completeness assessment, diagnostic, false-antecedent, action, total-disposition, gate state, review state and decision, and F0–F5 result payloads.
- `(schema_id = process_model, schema_version = 1)`: dated profile ID, roles, stages, queues, resources, deadlines, extensions, gates, and documented provenance.
- `(schema_id = scenario, schema_version = 1)`: environmental parameters, policy set, horizon, seeds, and validity status.
- `(schema_id = case, schema_version = 1)`: case kind, typed generic latent-state and administrative-access attribute references, evidence state, potential-record references, deadline, and keyed-draw references. Income, debt, recovery, and recipient labels belong to application mappings or typed actions, not the kernel case schema.
- `(schema_id = event, schema_version = 1)`: timestamped transition with closed type, frozen priority registry, unique branch-independent causal-event key, root and descendant path, microstep and transition ranks, actor, actions, role-bound rule executions, evidence, policy, intervention arm, keyed draws, and provenance.
- `(schema_id = simulation.system_state, schema_version = 1)` and `(schema_id = simulation.system_trace, schema_version = 1)`: complete cohort, queue, resource, clock, policy, rule, event, and termination state for shared-capacity interventions.
- `(schema_id = run, schema_version = 1)`: scenario, policy, seed, status, counters, and artifact paths.
- `(schema_id = metric, schema_version = 1)`: named numerator, denominator, unit, scope, and estimate.
- `(schema_id = audit_task, schema_version = 1)` and `(schema_id = audit_finding, schema_version = 1)`: optional audit artifacts only.

Schema family IDs are stable and version-free; a schema version appears only in `schema_version`. All persisted records use `(canonicalization_id = UPS-CANONICAL-JSON, canonicalization_version = 1)`. `RecordRef` always means `(object_id, object_version)`. Domain payloads do not duplicate envelope ownership, provenance, source basis, or source references.

### Schema manifest and closed implementation signatures

Before `schemas.py` is accepted, `data/model/schema_manifest_v1.yaml` must enumerate every persisted payload kind with:

- schema family ID and positive integer version;
- payload discriminator and domain-ID field that must equal `meta.object_id`;
- root versus derived source-basis rules;
- all required and nullable fields, typed `RecordRef` relationships, and discriminated unions;
- every array path marked ordered or `set_semantics`;
- the owner responsible for the fact represented;
- permitted closed `implementation_id` values, immutable code-artifact hashes, role/cardinality/schema input signatures, output schemas, and typed parameter signatures for executable rules; and
- the focused validation test and stable diagnostic for each invariant.

The manifest is a study-specific implementation inventory, not a dynamic registry. `schemas.py` is the executable owner of these contracts and must be generated from or checked bidirectionally against the manifest. A schema class, manifest entry, or stored fixture that exists without its counterpart fails `SCHEMA_MANIFEST_DRIFT`.

The minimum Slice 1 inventory is: `RecordRef`; `SchemaRef`; `RecordMeta`; `StoredRecord`; `Claim`; `UntypedField`; `Representation`; `EvidenceState`; `CompatibleState`; `CompatibleStateSet`; `ProjectionFactSet`; `ExecutableRule`; `RuleInputSpec`; `EvaluationInputBinding`; `AssessmentComponentBinding`; `ScopeDeclaration`; `ApplicabilitySpecification`; `FalseAntecedent`; `AssessmentValue` variants; `Assessment`; `Diagnostic`; `Action`; `Disposition`; `RoleAuthority`; `ProcessStage`; `QueueConfig`; `QueueState`; `ResourceState`; `DeadlineConfig`; `GateConfig`; `GateState`; `ReviewState`; `TemporalScope`; `ProcessProfile`; `PolicyProfile`; `SourceApplicationFixture`; `ApplicationBinding`; `ApplicationMapping`; `ScenarioParameter`; `ScenarioOverlay`; `ParameterBindingReceipt`; `CompiledConfiguration`; `CaseAttribute`; `KeyedDraw`; `TraceSpecification`; `Trace`; `PreState`; `PostState`; `SystemState`; `SystemTrace`; `EventPriorityRegistry`; `Event`; `ReviewDecision`; `InterventionPair`; `InterventionPairResult`; `NoninterferenceCertificate`; `ExpectedResult`; `Scenario`; `SimulationCase`; `Run`; and `Metric`. Fixture-specific schema families may specialize these payloads but may not weaken their invariants.

### Fact ownership

- Formal specification owns definitions, record and assessment envelopes, orders, property contracts, and assumptions.
- Schema manifest owns the complete persisted-model inventory, reference graph, set-versus-sequence declarations, and closed executable-rule signatures; `schemas.py` owns enforcement and may not add undeclared defaults.
- Executable-rule records own frozen parameter values; the named study-specific implementation owns deterministic behavior. Narrative prose owns neither.
- The Robodebt source packet owns claims about the documented historical workflow.
- Process map owns actual roles, stages, authority possession, event timing, and transition provenance; `sigma` may specify the capability and deadline required for a property but may not invent that the process supplies them.
- Historical application adapters own R-OCI-Early and R-OCI-Enhanced source bindings and documented behavior; counterfactual policies and stylized scenario overlays may not overwrite those facts or masquerade as historical values.
- Source fixtures remain immutable artifacts. Application mappings compile their source elements into separate process capabilities and historical policy bindings; raw descriptions and guard strings never execute directly.
- Process profiles own available topology and capabilities. Policy profiles own active transformation, routing, permission, gate, timeout, correction, and restoration behavior.
- Scenario overlays fill declared unbound slots only. Compiled configurations and parameter-binding receipts own the exact runtime composition and reject duplicate owners or unresolved values.
- Legal-status fields consume source-manifest labels and may not be inferred from oracle error.
- Scenario generator owns valid parameter combinations and stable IDs.
- Simulation engine owns event ordering, the priority registry, well-founded termination, branch-independent causal-event keys, complete system-state capture, causal-cut alignment, and state transitions.
- Policy module owns routing and permission behavior.
- Random-stream manager owns seeds and case/event-keyed paired exogenous draws.
- Metrics code owns counters and derived run-level metrics.
- Analysis code owns aggregates, intervals, boundary maps, and tradeoff figures.
- Reports render stored artifacts and may not reconstruct results from prose.

## Repository Architecture

### Planned modules

- `src/uncertainty_permission_simulation/schemas.py`: versioned contracts.
- `src/uncertainty_permission_simulation/rules.py`: static callable registry for manifest-declared executable rules and code-artifact hashing.
- `src/uncertainty_permission_simulation/formal_model.py`: compatible-state and permission orders, evidentiary fidelity, authority distinctions, review semantics, and F0-F5.
- `src/uncertainty_permission_simulation/process_model.py`: stages, resources, queues, deadlines, and process transitions.
- `src/uncertainty_permission_simulation/events.py`: event types, branch-independent causal-event keys, deterministic ordering, and causal-cut construction.
- `src/uncertainty_permission_simulation/profiles.py`: closed, versioned case-neutral process and policy profile loading and validation.
- `src/uncertainty_permission_simulation/configuration.py`: deterministic application mapping, overlay resolution, compiled-configuration construction, and binding receipts.
- `src/uncertainty_permission_simulation/applications/robodebt.py`: thin source-profile adapter for R-OCI-Early and R-OCI-Enhanced; no event-loop or policy logic.
- `src/uncertainty_permission_simulation/policies.py`: U0, U1, U2C, U2O, and U3 behavior.
- `src/uncertainty_permission_simulation/simulator.py`: discrete-event engine.
- `src/uncertainty_permission_simulation/random_streams.py`: reproducible paired streams.
- `src/uncertainty_permission_simulation/scenarios.py`: constrained scenario generation.
- `src/uncertainty_permission_simulation/metrics.py`: run counters and outcomes.
- `src/uncertainty_permission_simulation/analysis.py`: estimates, diagnostics, boundaries, and figures.
- `src/uncertainty_permission_simulation/audit.py`: optional A0/A1 ablation only.
- `src/uncertainty_permission_simulation/cli.py`: validate, trace, pilot, run, resume, reconcile, analyze, evidence-packet, verify-freeze, and audit.

### Planned artifacts

- `data/model/schema_manifest_v1.yaml`: complete study-specific schema inventory and closed implementation signatures.
- `data/model/`: remaining formal and process specifications.
- `data/sources/robodebt/`: source manifest, citation-level notes, and permitted local source extracts or metadata.
- `data/scenarios/`: pilot and frozen core scenarios.
- `data/golden_traces/`: hand-inspected event traces.
- `experiments/configs/`: smoke, pilot, confirmatory, sensitivity, and optional audit configs.
- `docs/FORMAL_MODEL.md`: notation, definitions, results, and assumptions.
- `docs/CONFIGURATION_COMPILATION.md`: deterministic ownership, compilation, overlay, temporal-scope, and generalizability contract.
- `docs/PROCESS_RED_TEAM_PROTOCOL.md`: application levels, intake worksheet, five-step method, report template, and classification rules.
- `docs/P0_PROCEDURE_REVIEW_PACKET.md`: input-only representation-preservation review packet.
- `docs/P0_USABILITY_WALKTHROUGH.md`: P0 reference profile and post-assessment walkthrough.
- `docs/TRANSFER_CANARY.md`: synthetic contemporary-AI transfer review input.
- `docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md`: post-Slice-5 project-lead review and semantic-change control.
- `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`: transfer-canary reference profile.
- `docs/ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md`: staged input rendered from the prespecified executable trace.
- `docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md`: executable-trace reference profile.
- `docs/ROBODEBT_CASE_STUDY.md`: sourced period-specific process map, formal crosswalk, and limitations table.
- `docs/LITERATURE_AND_ORIGINALITY_MAP.md`: structured adjacent-literature and contribution boundary.
- `docs/CONTINUITY_AND_CLAIM_BOUNDARY.md`: internal lineage, standalone, and attackability control.
- `docs/WORKED_TRACE_SELECTION.md`: prespecified Robodebt trace rule.
- `docs/PREREGISTRATION.md`: frozen simulation design and analysis.
- `docs/EXECUTION_LEDGER.md`: slice receipts.
- `docs/DEFERRED.md`: explicit incomplete work.
- `docs/FREEZE_MANIFEST.json`: input, code, environment, source, and analysis hashes.
- `docs/EVIDENCE_PACKET.md`: claim-to-artifact map.

### Explicitly avoid

- a general-purpose simulation framework or plugin architecture beyond the study's closed profile contracts;
- case names, historical citations, or Robodebt-specific branches inside the event engine, formal evaluators, random streams, or metrics;
- silent historical defaults for parameters marked `unsupported`;
- plugin or task registries;
- a database or web application;
- detailed perception-model benchmarking;
- unsupported reconstruction of a deployed system;
- multiple audit backends before the primary study completes; and
- compatibility layers for sibling repositories.

### Dependency order

Two workstreams proceed independently and converge before pilot freeze:

1. **Kernel path:** formal specification -> schema manifest -> schemas and machine-readable P0 records -> canonical synthetic process and policy profiles -> configuration compiler -> process model -> event engine -> random streams -> scenario generator -> metrics -> analysis.
2. **Application path:** source audit -> dated Robodebt source fixtures -> application mapping -> separate process capability and historical policy profiles -> profile and provenance validation -> stylized overlay -> compiled configuration -> worked-trace rendering.

The kernel path may begin once the Slice 0 automated specification gate passes. It does not wait for exact historical calibration. The application path may evolve before freeze, but it must load through public profile contracts and may not add branches to core execution code. Both paths, the executable Robodebt trace, the application-sufficiency review, and all automated pre-freeze checks must pass before Slice 4 confirmatory freeze. Procedure comprehensibility is reviewed by the project lead after Slice 5 analysis and before Slice 6 completion.

The simulator must not depend on reporting, optional audit, or article-writing code.

## Execution Protocol

Only one dependent slice may be active. Every completed slice records:

- files changed;
- files intentionally deferred;
- source additions and provenance;
- commands and results;
- golden traces or comparisons;
- residual risks;
- gates promoted from report-only to blocking; and
- commit SHA.

Record receipts in `docs/EXECUTION_LEDGER.md`.

If a subsystem cannot be completed, finish it, remove it, or record it in `docs/DEFERRED.md` with owner, reason, missing work, risk, and next action. Vague TODOs are not completion evidence.

The plan is complete when its contracts, ownership, gates, commands, decision rules, and external dependencies are explicit and `python3 scripts/validate_plan.py` passes. That does **not** mean the study is complete. Study completion requires Slices 1–6, the evidence packet, and all 39 answers in the Final Completion Audit to be supported by stored evidence.

Every slice receipt uses one diagnostic envelope for failed or waived work: `diagnostic_id`, `slice_id`, `command_or_gate`, `status`, `artifact_refs`, `owner`, `blocking`, `next_action`, and `timestamp`. A blocking failure stops the dependent path. A nonblocking failure must map to a registered deferred item or an explicitly optional subsystem; prose-only waivers are invalid. Stable diagnostic prefixes identify the owner: `PLAN_`, `SOURCE_`, `SCHEMA_`, `CONFIG_`, `FORMAL_`, `SIM_`, `PILOT_`, `FREEZE_`, `RUN_`, `ANALYSIS_`, `REPORT_`, and `QA_`.

### Slice file and mutation contract

The `Owns` list in each slice defines its substantive outputs. This table fixes the default file boundary and the receipt that proves completion; a slice may update `README.md`, `AGENTS.md`, `docs/EXECUTION_LEDGER.md`, and `docs/DEFERRED.md` only to synchronize status or constraints. Any other cross-slice edit requires a ledger entry naming the affected contract and rerunning its earlier blocking gates.

| Slice | Default write boundary | Forbidden mutation | Required receipt |
| --- | --- | --- | --- |
| 0 | current source fixtures, specifications, controls, and validation scripts | simulator implementation or generated empirical results | Slice 0 source/specification validation receipt |
| 1 | `src/.../{schemas,formal_model,configuration,profiles,process_model,events,metrics,cli}.py`, matching unit tests, smoke config, and golden traces | stochastic calibration, confirmatory configs, or application-specific kernel branches | deterministic vertical-slice receipt |
| 2 | `src/.../{simulator,random_streams,policies}.py`, application adapter, validation tests, and telemetry | scenario selection from substantive results or changes to frozen formal meaning | stochastic validation receipt |
| 3 | scenario generator, pilot config/output, dummy analysis, figure prototypes, and executable-trace review input/reference profile | confirmatory-result inspection or post hoc primary estimands | pilot and freeze-candidate decision receipt |
| 4 | preregistration `1.0`, confirmatory/sensitivity configs, dependency lock, and freeze manifest | any confirmatory execution | immutable freeze receipt with commit and artifact hashes |
| 5 | append-only run outputs, reconciliation, analysis, figures, and claim-boundary memo | mutation of frozen inputs or replacement of completed runs | run-completeness and analysis receipt |
| 6 | evidence packet, project-lead comprehensibility review, and manuscript artifacts | new unpreregistered primary analysis or unversioned semantic protocol changes | release, review, and manuscript receipt |
| 7 | isolated optional audit module, config, outputs, and appendix result | changes to core simulation, primary analysis, or main acceptance criteria | optional audit receipt or explicit omission |

### Runtime and escalation budget

Runtime is measured on a named reference environment recorded in the ledger. Plan and source validators target 10 seconds each; focused test groups target 30 seconds; the default deterministic suite targets 3 minutes; Slice 2 validation targets 20 minutes; and the development pilot is capped at 2 wall-clock hours. Slice 3 must freeze a predicted confirmatory ceiling from measured throughput, no greater than 24 wall-clock hours for the core run on the declared reference environment. A preregistered family-wide precision extension may use one additional 24-hour window. Release verification excluding deliberate confirmatory reruns targets 30 minutes.

If a target is missed, first profile and remove implementation waste. If the pilot still predicts a ceiling breach, reduce optional sensitivities, then development-only scenario families, then cohort size or maximum replications under the preregistered precision rule. Never selectively drop a policy, primary contrast, adverse result, or scenario because of its observed direction. If the primary precision target cannot fit after those reductions, stop at Slice 3 and revise the design before freeze.

### Environment and baseline entry gate

Before Slice 1 changes begin, close `D-009` by creating or approving a baseline commit containing the validated Slice 0 plan artifacts. Then create the local environment from the declared project metadata:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
./.venv/bin/python scripts/validate_plan.py
./.venv/bin/python scripts/validate_slice0.py
```

Record the baseline commit, Python version, platform, dependency versions, and validator outputs in the ledger. Development may use any supported Python `>=3.11`; Slice 4 freezes the exact interpreter and dependency lock used for confirmatory execution. UTC owns persisted simulation timestamps, canonical serialization owns ordering, and host locale or hash iteration order may not affect artifact identity.

## Work Slices

### Slice 0: Source, construct, and claim contract

**Purpose:** Establish venue fit, noncircular constructs, a closed kernel/profile boundary, and a defensible application contract before code.

**Owns:**

- structured literature and originality map spanning information order and robust decisions, selective classification and abstention, human-review queueing, administrative burden, automated administrative decision-making, process safety, and red teaming;
- Robodebt authoritative-source packet and citation-level manifest;
- separate source-anchored R-OCI-Early and R-OCI-Enhanced process diagrams;
- machine-readable `R-OCI-Early@1` and `R-OCI-Enhanced@1` source profiles with explicit temporal precision and unsupported parameters;
- `docs/FORMAL_MODEL.md` draft;
- `docs/ROBODEBT_CASE_STUDY.md` draft;
- `docs/PRECURSOR_FIDELITY_FIXTURE.md`, fixing `P0-Preserve`, `P0-Fallback`, the held uncertain output, invariant process inputs, expected comparisons, and no-change falsifier;
- `data/model/schema_manifest_v1.yaml`, enumerating every Slice 1 persisted payload, reference edge, set/sequence path, source-basis rule, and closed executable-rule signature;
- `docs/CONFIGURATION_COMPILATION.md`, fixing source-fixture immutability, process-versus-policy ownership, overlay precedence, parameter-binding receipts, temporal scopes, generic kernel boundaries, and compilation diagnostics;
- `docs/PROCESS_RED_TEAM_PROTOCOL.md` version `0.2`, fixing the five steps, application levels, ordered status procedure, assessment-versus-claim-limit distinction, required inputs, `pass`/`fail`/`unassessable`/`not_applicable` outputs, compact diagnostic lookup, ownership fields, and report rows before confirmatory results;
- `docs/P0_PROCEDURE_REVIEW_PACKET.md`, containing only the representation-preservation inputs for a staged first-pass application;
- `docs/P0_USABILITY_WALKTHROUGH.md`, containing the P0 reference profile, post-assessment explanation, non-composite profile, interventions, tradeoffs, and escalation boundaries;
- `docs/TRANSFER_CANARY.md`, defining one synthetic contemporary-AI workflow review input that uses different domain vocabulary and does not affect the Robodebt simulation;
- `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`, containing the transfer-canary reference profile;
- `docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md`, fixing the post-Slice-5 project-lead review fields, issue log, and editorial-versus-semantic change rule;
- a deterministic worked-trace selection rule fixed before confirmatory execution;
- the internal continuity and claim-boundary control;
- `docs/PREREGISTRATION.md` skeleton;
- `docs/EXECUTION_LEDGER.md`;
- `docs/DEFERRED.md`; and
- synchronized `README.md` and `AGENTS.md` boundaries.

**Must resolve:** compatible-state ordering and concrete denotations, evidentiary fidelity, formal-versus-functional authority, effective review, gate safety, decision service, the record/reference boundary, canonicalization and schema identity, executable-rule bindings, replay-complete assessment and diagnostic references, source-fixture/application-mapping/process-profile/policy-profile/overlay/compiled-configuration ownership, generic event and case records, parameter precedence and conflict rejection, mixed-precision temporal scope, the base-vulnerability-versus-attackability boundary, exact `P0-Precursor` held variables and falsifier, bounded historical profile dates and unresolved fields, three-axis validity language, U0/U1/U2C/U2O/U3 semantics, primary outcomes, three headline article propositions, protocol classification rules, worked-trace selection, and emerging-technology contribution.

**Forbidden:** simulator behavior, pilot tuning, invented historical values, confirmatory outputs, and protocol `1.0`.

**Verification:**

```bash
python3 scripts/validate_slice0.py
python3 scripts/validate_plan.py
python3 -m py_compile scripts/validate_slice0.py scripts/validate_plan.py
```

**Stop if:**

- information or authority order depends on the desired result;
- precautionary actions cannot be distinguished from progression;
- no defensible application can support the evidence transformation, action path, organizational roles, and claim limits needed for the institutional demonstration;
- legal, evidentiary, and numerical claims cannot be kept separate;
- the article cannot explain its emerging-technology contribution without asserting field equivalence; or
- the formal contribution cannot be distinguished from existing value-of-information, queueing, monotonicity, or human-in-the-loop governance work.

**Implementation gate:** the source/profile consistency, complete configuration-contract inventory, generic event/case boundary, compilation ownership, overlay precedence, temporal-scope support, provenance, P0/Robodebt boundary, staged-review-input answer leakage, YAML uniqueness, required-file, and Markdown checks pass structurally; the minimum defensible case threshold is documented; and Slice 1 can be implemented without a historical default, raw narrative execution, case-specific engine branch, or unresolved runtime slot.

**Post-simulation review contract:** after Slice 5 analysis, the project lead applies the procedure in sequence to the P0 input, executable Robodebt worked trace, and transfer canary, records ambiguities, and checks whether the complete method can be understood without hidden author knowledge. This is not independent validation and is not a pre-freeze gate. Editorial corrections may be made in Slice 6; semantic corrections require a new freeze and rerun of affected confirmatory artifacts.

P0 must not be mislabeled as a Robodebt trace. The executable prespecified Robodebt trace does not exist until later slices and receives a separate review input and reference profile during Slice 3.

**Done when:** both automated validators pass, every Slice 0 artifact has a named owner and closed claim boundary, the compiler can be implemented without inventing a runtime value or case-specific branch, all incomplete execution work is registered in `docs/DEFERRED.md`, and the ledger records the post-simulation project-lead review separately from the implementation and freeze gates.

**Commit required:** yes.

### Slice 1: Case-neutral dynamic vertical slice

**Purpose:** Produce inspectable case-neutral traces from arrival through evidence, routing, review or information acquisition, deadline, action, and closure, then prove that a thin Robodebt adapter can use the same engine without modifying it.

**Owns:**

- core schemas;
- event queue;
- notice delivery, endogenous engagement, and one pre-debt review resource;
- deterministic timing mode;
- deterministic configuration compiler and parameter-binding receipts;
- one canonical synthetic process profile plus U1, U2C, and U2O policy profiles;
- one isomorphic vocabulary canary and one non-isomorphic synthetic topology canary;
- a validated R-OCI-Early adapter smoke profile loaded only after the canonical traces pass;
- executable `P0-Preserve`, `P0-Fallback`, and no-change-control fixtures;
- F0-F5 checks;
- metrics skeleton;
- seven golden event traces;
- smoke CLI; and
- a rendered practitioner report for the executable P0 pair that matches `docs/P0_USABILITY_WALKTHROUGH.md` and links every report row to stored trace, assessment, and diagnostic artifacts.

**Golden traces:** precursor held-output representation change, precursor no-change falsifier, case-neutral imputation after nonresponse, U2C gate-safe hold under queue delay, U2O timeout action under the same delay, progression after action-specific evidence, and post-action correction that remains only partially restorative after external exposure. A separate R-OCI-Early adapter trace must bind documented labels and transitions to one of these same semantic paths without changing engine or policy code.

**Forbidden:** full scenario grid, stochastic calibration, optional audit, general frameworks, and UI.

**Verification:**

```bash
PYTHONPATH=src pytest -q tests/unit/test_formal_model.py tests/unit/test_events.py tests/unit/test_process_model.py
```

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml
```

**Stage gate:** the schema manifest, Pydantic models, and stored fixture kinds match bidirectionally; every record validates its schema-family/version pair, source-basis rule, versioned references, declared set/sequence paths, metadata, and canonical hash; every executable rule has closed role/cardinality/schema bindings and an immutable code hash; every routing branch emits a total disposition; every property result validates replay-complete role-bound inputs, declared component relations, truth status, completeness, diagnostics, scope, applicability, and property-specific antecedent/condition contracts. The configuration compiler accepts only exact stored references, splits source-grounded topology from active policy behavior, rejects documented-value overrides and unsupported historical defaults, emits exactly one binding receipt per runtime slot, and produces configurations with zero unresolved slots. Every golden trace conserves the case, preserves evidence types and provenance, orders simultaneous events deterministically, rejects causal-key collisions and nonterminating same-time chains, derives stable causal-event keys, captures complete system state for F2, validates intervention scope, aligns divergent paired system traces by causal cut, and produces the expected formal-authority, functional-permission, gate, review, deadline, exposure, and restoration metrics. Renaming domain labels and loading an isomorphic process profile must preserve projected semantic outcomes and event order while full artifact hashes remain identity-sensitive; a non-isomorphic synthetic topology must execute without a kernel change. The R-OCI-Early adapter must run without importing Robodebt identifiers into the kernel or supplying a default for any `unsupported` historical parameter. `P0-Preserve` and `P0-Fallback` must have identical hashes for the held case, model output, downstream rule, and process state; only the declared interface representation and its downstream consequences may differ. The no-change control must preserve safeguards and permission across both representations. P0's explicit F1/F2 scope exclusions, trace-specific F3 results, required-meaning-based F4 results, and unknown-scope F5 result must match the fixture exactly. The smoke CLI must also render the non-composite P0 practitioner profile, declare Level B and its claim limits, use only closed diagnostic and execution-status values, link each row to its stored artifacts, and reproduce the expected walkthrough without consulting prose.

**Stop if:** a schema cannot be represented without weakening the manifest, a canonical synthetic trace requires an institutional adapter, a non-isomorphic topology requires an engine branch, compilation leaves an unresolved or multiply owned slot, or P0 cannot preserve its held-variable hashes.

**Done when:** both verification commands pass, all seven golden traces and both generalizability canaries have stored expected-versus-actual receipts, the adapter smoke test changes no kernel file, and the ledger records runtime, hashes, diagnostics, residual risks, and the commit SHA.

**Commit required:** yes.

### Slice 2: Stochastic engine and validation

**Purpose:** Establish that the simulator is correct before asking substantive questions.

**Owns:**

- strict process-profile, policy-profile, application-adapter, and stylized-overlay validation;
- keyed initiation, administrative-access, engagement, service, evidence-retrieval, and deadline draws;
- R-OCI-Early and R-OCI-Enhanced application adapters and source-validation fixtures;
- U0, U1, U2C, U2O, and U3 policies;
- assistance, pre-debt review, and reassessment queue disciplines;
- evidence acquisition;
- debt, recovery, and correction windows;
- limiting-case tests;
- analytical queue comparison;
- reference-simulator differential tests; and
- run-level telemetry.

**Forbidden:** pilot scenario selection, confirmatory configs or results, changes to formal semantics merely to satisfy a trace, historical calibration from undocumented quantities, and application-name branches in kernel code.

**Verification:**

```bash
PYTHONPATH=src pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py
```

```bash
PYTHONPATH=src pytest -q tests/integration/test_queue_validation.py tests/integration/test_reference_simulator.py
```

**Stop if:** the reference simulator and production simulator disagree outside a diagnosed tolerance, keyed draws cannot remain stable across divergent event counts, queue benchmarks fail, a source profile requires a silent numeric default, or validation exceeds the runtime budget without a documented reduction that preserves all blocking checks.

**Done when:** hand traces match exactly, analytical queue cases agree within frozen tolerances, paired policies share cases and keyed exogenous draws, policy-dependent event-count changes do not shift unrelated draws, repeated seeds reproduce identical event and metric hashes, semantically equivalent synthetic and application profiles agree on kernel behavior, and every executable non-documented value is supplied by a separately versioned stylized overlay rather than a historical profile.

**Commit required:** yes.

### Slice 3: Experiment pilot and design freeze candidate

**Purpose:** Calibrate runtime, precision, validity constraints, and interpretability without inspecting confirmatory results.

**Owns:**

- constrained scenario generator;
- 12-18 development-only scenario families;
- case-application sufficiency review confirming that each manuscript claim has a source anchor or explicit `inferred`, `stylized`, or `unsupported` boundary;
- adapter-swap rehearsal showing that a second synthetic vocabulary/profile can run without engine changes;
- pilot config;
- finite-cohort, drain-window, administrative-cutoff, and censoring diagnostics;
- Monte Carlo error analysis;
- dummy-data analysis pipeline;
- boundary and tradeoff figure prototypes;
- pilot audit;
- procedure-review materials containing one prespecified Robodebt golden trace and the synthetic contemporary-AI canary, each separated into a first-pass input and reference profile;
- protocol revision log, limited to changes made before confirmatory freeze.

**Pilot questions:** runtime, stage bottlenecks, rare-event frequency, MCSE, cutoff and censoring bias, common-random-number benefit, keyed-draw stability, invalid scenarios, metric redundancy, figure interpretability, and whether core hypotheses are estimable.

**Forbidden:** inspection of confirmatory outputs, result-directed seed or factor selection, deletion of adverse policies, protocol coaching presented as blind QA, and promotion of a stylized value to documented status.

**Verification:**

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli validate experiments/configs/pilot_v1.yaml
```

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli pilot experiments/configs/pilot_v1.yaml
```

```bash
PYTHONPATH=src pytest -q
```

**Stop if:** the dynamic results simply restate policy definitions, the main conclusions depend on scalar utility weights, outcome differences cannot be separated from implementation bugs, queue or access dynamics never affect review and outcomes, or runtime prevents the planned precision target.

**Protocol artifact QA:** before confirmatory freeze, executable P0, Robodebt, and transfer-canary outputs must agree with their versioned reference profiles; closed vocabularies, scope rules, claim limits, reference closure, and review-input/reference separation must pass automatically. These checks establish internal consistency, not usability. After Slice 5 analysis, the project lead performs the staged comprehensibility review and records application level, `evaluation_state`, property status and completeness where assessed, located transition, evidence, diagnostic, missing information or claim limit, diagnostic owner, intervention owner, tradeoff, and ambiguity. Any post-result semantic defect triggers a new freeze and rerun; it may not be repaired through reinterpretation.

**Done when:** valid scenario count, cohort and cutoff rules, keyed seeds, replications, MCSE rules, censoring treatment, exclusions, metrics, plots, and runtime ceiling are ready to freeze; the application adapter meets the minimum defensible case threshold; no historical profile supplies unsupported numeric defaults; the adapter-swap rehearsal passes; the staged review inputs and reference profiles are complete and internally consistent; and every protocol or application-mapping change is logged.

**Commit required:** yes.

### Slice 4: Confirmatory freeze

**Purpose:** Create an immutable boundary before primary results are inspected.

**Owns:**

- finalized formal and process specifications;
- frozen `P0-Precursor` fixture and base-vulnerability-versus-attackability claim boundary;
- selected application identity, Robodebt source manifest, period-specific process map, formal crosswalk, adapter version, parameter-provenance table, and stylized overlays;
- frozen valid scenario families;
- policies and simulator;
- seeds, horizons, replication and extension rule;
- analysis code tested on synthetic dummy results;
- `docs/PROCESS_RED_TEAM_PROTOCOL.md` version `1.0`, including the canary, classification rules, and worked-trace selection rule;
- confirmatory and sensitivity configs; and
- `docs/FREEZE_MANIFEST.json`.

**Freeze manifest hashes:** selected application, sources, formal definitions, `P0-Precursor` fixture, attackability claim boundary, process map, application adapter, parameter-provenance table, stylized overlays, protocol semantics, canary, worked-trace selection rule, parameters, validity rules, policies, code, seeds, random-stream allocation, metrics, exclusions, analysis, environment, dependency lock, and configs.

**Forbidden:** confirmatory execution, unresolved automated pre-freeze gates, unhashed executable inputs, mutable remote-source identity without an explicit rule, and changes to primary analysis after viewing non-dummy results.

**Verification:**

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli validate experiments/configs/confirmatory_v1.yaml
```

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli verify-freeze docs/FREEZE_MANIFEST.json
```

```bash
./.venv/bin/python scripts/verify_repo.py
```

**Done when:** every scenario is valid or diagnostically excluded, predicted runtime fits the ceiling, dummy analysis produces every planned table and figure, all automated artifact and reference-profile checks pass, every source and stylized parameter has a frozen provenance owner, the application can be removed without breaking kernel tests, and no confirmatory output has been inspected.

**Commit required:** yes; record the freeze commit SHA.

### Slice 5: Confirmatory execution and analysis

**Purpose:** Run the frozen dynamic experiment and produce the primary evidence.

**Owns:** append-only run artifacts, reconciliation report, convergence diagnostics, paired estimates, boundary maps, tradeoff figures, the prespecified worked trace and any selection-rule outputs, and claim-boundary memo. Do not select a visually persuasive trace after inspecting results.

**Forbidden:** mutation of frozen inputs, replacement of completed attempts, selective precision extension, suppression of null or adverse results, and unregistered exploratory results presented as confirmatory.

**Verification and execution:**

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli run experiments/configs/confirmatory_v1.yaml
```

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli analyze experiments/configs/confirmatory_v1.yaml
```

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli reconcile experiments/configs/confirmatory_v1.yaml
./.venv/bin/python scripts/verify_repo.py --through-slice 5
```

Use resume only for missing or operationally failed runs. Never replace completed results or change frozen semantic inputs.

**Done when:** every planned run is present or documented as unresolvable; MCSE rules are satisfied or transparently missed; primary and control results are complete; and null, adverse, or counterintuitive results remain visible.

**Commit required:** yes.

### Slice 6: Evidence packet and 10,000-word article

**Purpose:** Integrate formal, computational, and institutional evidence into a complete 10,000-word extended research paper that reports the conducted study and remains traceably continuous with the completed 1,500-word essay.

**Owns:** the release evidence packet, final claim-to-artifact map, reproducibility instructions, completed project-lead comprehensibility review, completed article, and submission-readiness receipt.

**Required packet:**

- formal definitions and assumption table;
- literature and originality map;
- sourced process diagram and model crosswalk;
- simulator validation receipts;
- scenario, seed, run, and exclusion inventory;
- primary paired estimates and MCSE;
- queue and effective-review boundary maps;
- evidentiary-support, numerical-error, timeliness, agency-workload, recipient-burden, recovery-exposure, and restoration results;
- negative-control results;
- the prespecified worked trace and any reproducible selection-rule outputs;
- sensitivity results completed before the deadline;
- exact reproduction commands;
- limitations and claim-boundary memo;
- claim-to-proposition, source, table, figure, trace, or limitation map;
- precursor-to-extension continuity table showing what is retained, refined, tested, supported, bounded, or rejected;
- completed `docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md`, including every material ambiguity and its disposition;
- a self-contained, preregistered five-step process-red-team protocol with `pass`/`fail`/`unassessable`/`not_applicable` outputs, diagnostic/intervention table, fixed Robodebt trace, and compact held-out AI canary in the main manuscript, with extended worksheets and schemas in the repository; and
- complete manuscript draft following the working word budget, with findings in the abstract, introduction, results, and conclusion kept mutually consistent.

**Forbidden:** changing frozen protocol semantics, adding an unregistered primary estimand, presenting Robodebt as a numeric reconstruction or attack, reporting the AI canary as prevalence evidence, and using manuscript prose as the owner of a computational fact.

**Verification:**

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli evidence-packet experiments/configs/confirmatory_v1.yaml
./.venv/bin/python scripts/verify_repo.py --release
```

The release verifier must also enforce the verified venue word-count rule, claim-to-artifact coverage, consistent headline findings, exact reproduction commands, and answers with artifact references for all 39 Final Completion Audit questions.

**Done when:** the evidence packet is sufficient without rerunning the study; the project lead can follow and explain the procedure using the completed simulation and worked examples; every material comprehensibility issue is resolved; any semantic issue has triggered a new freeze and rerun; a complete manuscript remains at or below 10,000 words and reports methods and results rather than future-work promises; every claim has a named evidence owner; every departure from the precursor essay is explicit; and post-result editorial edits have not changed the frozen protocol semantics.

**Commit required:** yes.

### Optional Slice 7: Audit-checklist ablation

**Purpose:** Test whether the fixed checklist improves evaluator-specific artifact detection after the core study and manuscript are already complete.

**Entry condition:** Slice 6 is complete by the start of Week 6 and the article has space for the result.

**Owns:** frozen episode set, A0/A1 prompts, local evaluator config, append-only outputs, blinded scoring packet, and appendix-ready result.

**Forbidden:** any dependency from the core simulator or primary claims on the ablation, prompt rescue after output inspection, more than one evaluator backend, and displacement of a required Slice 6 artifact.

**Verification:**

```bash
PYTHONPATH=src python -m uncertainty_permission_simulation.cli audit experiments/configs/audit_v1.yaml
PYTHONPATH=src pytest -q tests/audit
```

**Stop if:** the comparison requires three personas, multiple evaluators, prompt rescue, or changes to the primary simulation.

**Done when:** the 72-call ceiling is respected, at least half the outputs are double-coded, false positives are reported, and the article labels the result evaluator-specific and secondary.

**Commit required:** yes if executed; otherwise omit the subsystem.

## QA And Failure Ownership

### Golden cases

- valid and invalid versioned record envelopes, including stale source versions and canonical-hash mismatches;
- separately stored claim/field records referenced by a representation, plus rejected partial embedded envelopes and duplicated payload provenance;
- canonical hashes invariant to object-key and declared-set order but sensitive to declared sequence order, schema/canonicalization versions, and normalized decimal/timestamp values;
- schema-manifest/model/fixture inventory agreement and a deliberate one-sided drift failure;
- closed executable-rule bindings with valid parameters, unknown-parameter rejection, and no narrative-text evaluation;
- source fixture plus application mapping compiled into separate process and historical policy profiles with a complete binding receipt;
- documented parameter preserved against an attempted stylized override, unsupported source parameter rejected without an overlay, and one valid stylized fill;
- mixed-precision as-documented temporal bundle that does not acquire a fictitious simultaneous activation date;
- replay-complete assessment and diagnostic graphs with a rejected unversioned or missing input/component reference;
- complete typed claims, intentionally untyped candidate fields, and total versus partial disposition records;
- `P0-Precursor` with identical uncertain model output and a representation-only change that alters surfacing, scrutiny, or permission;
- `P0-Precursor` no-change falsifier where routing and permission remain invariant to the representation;
- more-to-less information coarsening with no permission change;
- aggregate income transformed into unsupported fortnightly precision;
- oracle-correct amount that remains evidentially unsupported;
- numerically erroneous amount with complete provenance;
- no debt raised when period-specific evidence is absent;
- case-neutral progression withheld when action-specific evidence is absent;
- early-OCI 21-day profile and enhanced-OCI 28-day repair profile;
- notice not delivered, digital access unavailable, and evidence unobtainable as distinct traces;
- effective pre-debt review;
- nominal notice without effective review;
- U2C gate-safe hold under overload;
- U2O fail-open action under the same overload;
- F2 execute-versus-hold system traces with divergent endogenous event counts but identical cohort membership, causal-cut alignment, and keyed exogenous draws;
- a shared-capacity fallback that changes another case's timeout path, plus a case-local pair accepted only with a valid noninterference certificate;
- duplicate causal-key, zero-time-cycle, and event-bound fixtures that invalidate the run with stable diagnostics;
- reviewed action that loses current post-review eligibility before execution;
- exact-ID and validated-mapping F4 correspondence, plus a broad-label non-correspondence case;
- P0 required-meaning correspondence with explicit F1/F2 scope exclusions, trace-specific F3 applicability, semantic-null F4 non-applicability, and unknown F5 applicability;
- forward symbolic F4 entailment, reverse-only implication, and mapping-without-rationale cases;
- missing or ambiguous scope declaration, missing required input, invalid specification, and invalid status-aggregation cases with distinct diagnostics;
- assistance, review, or reassessment queue overload;
- third-party evidence resolving the discrepancy;
- period-specific evidence returning after debt or recovery;
- suppressed imputation flag or source provenance;
- debt zeroing with complete restoration;
- debt zeroing after irreversible modeled exposure; and
- successful and expired correction windows.

### Metamorphic checks

- reorder hypotheses and labels while preserving IDs;
- rename domain vocabulary and application labels without changing semantic traces or metrics;
- replace the Robodebt adapter with an isomorphic synthetic adapter without changing kernel behavior;
- execute a non-isomorphic synthetic topology with a different stage order, optional review path, and queue layout without changing kernel code;
- vary a stylized overlay without mutating the source-anchored application record;
- reorder simultaneous input records without changing event priority;
- split one arrival batch into equivalent timestamped arrivals;
- add irrelevant metadata;
- scale all time units consistently;
- replay paired policies with identical exogenous streams;
- add a policy-only event without shifting later keyed draws;
- add a causally inert branch-specific event without changing the F2 result;
- add a causally inert cohort case without changing existing system-level F2 results;
- replace an exact-ID surfaced item with a frozen semantically equivalent mapping without changing F4;
- replace a symbolic correspondence rule with a logically equivalent forward entailment and proof witness without changing F4;
- increase review capacity without increasing queue delay under otherwise identical draws.

### Adversarial mutations

- embed a bare claim, diagnostic, or component assessment inside a parent payload instead of storing and referencing it;
- duplicate `source_refs` or ownership in a payload and make it disagree with `RecordMeta`;
- add a schema class or fixture kind without a manifest entry, or change a declared set path into an ordered path on only one side;
- alter narrative rule text while keeping the typed implementation binding fixed, then make behavior incorrectly follow the prose;
- omit an evaluated input or replace a versioned assessment/diagnostic reference with a raw ID;
- corrupt the information coarsening map;
- relabel imputed fortnightly income as observed;
- infer legal validity from numerical oracle agreement;
- classify a containment action as progression;
- remove reviewer authority while retaining the review label;
- suppress uncertainty from the reviewer;
- align divergent paired traces by event index rather than branch-independent causal cuts;
- replace the F2 hold intervention with a favorable active policy;
- claim a cohort-level F2 pass from a case-local pair without a valid noninterference certificate;
- change cohort membership, shared queue state, or keyed draws between F2 arms;
- treat an event-order collision, same-time livelock, or event-bound breach as successful censoring;
- make recipient response policy-invariant;
- consume random draws in queue order so one extra event changes unrelated cases;
- swap hold-without-debt and impute-and-raise behavior;
- raise a debt or begin recovery before its gate completes;
- execute a reviewed action after it leaves the current post-review set;
- infer F4 correspondence from display text or the workflow's materiality map;
- accept reverse implication, satisfiable overlap, or a mapping without preservation rationale as F4 correspondence;
- classify a missing or ambiguous scope declaration as `not_applicable`, collapse missing inputs and invalid specifications into one reason, or let `unassessable` erase a sufficient known `fail` in an aggregate;
- duplicate or drop a case event;
- reuse a random stream across unrelated variables;
- change a frozen seed or parameter;
- detach a result from source or scenario provenance;
- report stylized parameters as documented values;
- insert a Robodebt-specific condition into the event engine or policy implementation instead of the application adapter;
- supply an executable historical default for a field marked `unsupported`;
- mutate a source-anchored application profile when only a stylized scenario overlay should change;
- execute a raw source description or free-form guard without a closed application binding;
- let a policy create a stage, gate location, resource, or action capability absent from its selected process profile;
- compare complete artifact hashes across renamed adapters instead of the frozen semantic projection; and
- assign a simultaneous activation date to a mixed-precision source bundle without evidence.

### Bug-class table

| Bug class | Owner | Blocking check |
| --- | --- | --- |
| Stored object lacks identity, version, owner, provenance, source version, or canonical hash | schemas/artifact layer | versioned-record envelope regression |
| Nested claim, field, diagnostic, or assessment component bypasses its `StoredRecord` boundary | schemas/artifact layer | reference-only nesting regression |
| Payload duplicates envelope ownership, provenance, source basis, or source references | schemas/artifact layer | envelope-authority regression |
| Schema manifest, Pydantic model, or persisted fixture kind drifts from either counterpart | schemas/artifact layer | `SCHEMA_MANIFEST_DRIFT` bidirectional inventory gate |
| Hash changes under key reordering or remains stable when a declared ordered field changes | schemas/artifact layer | canonicalization and set/sequence-path regression |
| Executable behavior depends on narrative text or an undeclared implementation parameter | schemas/formal model | closed-rule-signature regression |
| Assessment uses unversioned evaluation, component, diagnostic, scope, or input identities | formal model/evaluator | replay-reference closure regression |
| Helper boolean, truth status, completeness, and diagnostic reason collapse into one untyped field | formal model/evaluator | typed assessment-envelope regression |
| Property applicability or required inputs are inferred ad hoc rather than from the frozen F0–F5 contract | formal model/evaluator | property-contract matrix regression |
| Decision rule omits an enabled, post-review, selected, constraint, information, restoration, or gate-requirement field | policy module | total-disposition regression |
| Information ordering encodes the desired permission result | formal model | independent coarsening validation |
| Imputed detail is mislabeled as observed evidence | formal model/representation | evidentiary-fidelity golden test |
| Legal validity inferred from oracle error | source/metrics boundary | three-axis claim-type gate |
| Precautionary action scored as functional-permission expansion | action taxonomy | direction-class golden tests |
| Configured gate mistaken for gate safety, effective review, or decision service | process model | four-way review-state regression |
| Divergent F2 traces aligned by event index, scoped to one case despite shared resources, or using an outcome-selected hold policy | formal model/simulator | intervention-unit, noninterference, explicit-hold, and causal-cut regression |
| Duplicate causal key or zero-time cycle is silently accepted or censored | event engine | total-order and well-founded-termination regression |
| Reviewed action executes after current post-review eligibility lapses | formal model/policy | execution-state `P_post` membership regression |
| F4 correspondence inferred from display text or workflow self-classification | formal model/representation | independent semantic-correspondence regression |
| F4 symbolic entailment is reversed or mapping lacks preservation rationale | formal model/evaluation specification | forward-entailment and mapping-justification regression |
| Truth status, completeness, component relation, or sufficient-witness aggregation is incorrect | formal model/evaluator | applicability/input/specification/component/aggregation diagnostic regression |
| Event time or priority is nondeterministic | event engine | event-hash replay |
| Case is duplicated, lost, or closed twice | simulator | conservation invariant |
| Paired policies receive different exogenous cases or order-dependent draws | random streams | keyed-draw and paired-case hash checks |
| Queue metrics disagree with analytical benchmark | simulator/metrics | queue-validation gate |
| Debt action executes before deadline or review completion | policy module | deadline-and-gate ordering regression |
| Historical profiles silently blend different periods | process application/profiles | dated-transition provenance gate |
| Kernel behavior branches on a case name, historical citation, or application-specific label | simulator/profile boundary | adapter-swap and domain-renaming regressions |
| Unsupported historical field receives a silent executable default | process application/scenario overlay | unsupported-parameter rejection and provenance-overlay gate |
| Raw source prose or guard string executes without a closed mapping | configuration compiler | application-binding closure regression |
| Process capability and active policy behavior have duplicate or ambiguous owners | configuration compiler | process-policy ownership regression |
| Documented value is overwritten or a runtime slot has zero or multiple owners | configuration compiler | parameter-binding receipt and conflict regression |
| Mixed-date repair bundle receives a fictitious simultaneous activation time | process application | temporal-scope precision regression |
| Zeroing is mislabeled complete restoration after residual exposure | metrics | restoration-completeness regression |
| Invalid scenario enters confirmatory run | scenario generator | validity gate |
| MCSE extension favors a result | experiment runner | family-wide extension rule |
| Stylized value appears as sourced | process application | provenance-level audit |
| Frozen input changes | freeze gate | hash-integrity regression |
| Report re-derives results from prose | reporting | artifact-source audit |

Broad gates begin report-only during pilot and become blocking only after diagnostics are calibrated.

## Generalizability And Validity Guardrails

- Information ordering must be defined independently of policy outcome.
- Observed, imputed, missing, and disputed income values must remain distinct in schemas, events, metrics, and displays.
- Formal authority, functional permission, and operational action must remain distinct.
- Evidentiary support, numerical correctness, and historical legal validity must never be collapsed.
- Functional-permission expansion must be distinguished from precautionary constraint.
- Structural code must not depend on domain labels.
- Core event, policy, random-stream, formal-evaluation, and metric behavior must be testable without loading the Robodebt adapter.
- A source-grounded adapter may bind labels and documented transitions but may not own engine semantics.
- The Robodebt application establishes structural relevance and process grounding, not numeric reconstruction of the historical program.
- Stylized parameters remain labeled as stylized in tables and figures.
- Common random numbers pair policies but do not create independent observations; keyed draws must remain stable when endogenous event paths diverge.
- Scenario percentages describe the designed parameter space, not real-world frequencies.
- Queue stability and deadline effects must be reported rather than hidden by averages.
- U2C and U2O must never be pooled.
- No single utility weighting may conceal safety-throughput tradeoffs.
- Behavioral compression and reviewer psychology remain outside the model.
- Legal conclusions are attributed to the Royal Commission or Ombudsman rather than inferred from simulation output.
- Transfer to current AI or national-security systems is limited to the formal invariant, process-red-team method, and explicitly stated institutional similarities.
- The base vulnerability, process-red-team method, structural susceptibility, and adversarial exploitability remain separate claim types. Robodebt does not establish inducibility, observability, repeatability, benefit, or historical attack.
- `P0-Precursor` must hold the uncertain model output and declared process inputs fixed; otherwise it is not a direct extension test.
- Optional audit results do not establish human red-team performance or universal protocol superiority.

## Verification Tiers

### Focused

Formal property, event ordering, policy, queue, random-stream, and metric tests; target under 30 seconds per focused group on the recorded reference environment.

### Default

Full unit suite plus deterministic smoke trace; target under 3 minutes.

### Simulation validation

Golden traces, limiting cases, analytical queue comparison, reference-simulator differential test, conservation, and repeatability; target under 20 minutes.

### Pilot

Development-only scenario subset with runtime, MCSE, finite-cohort cutoff, censoring, validity, and figure diagnostics; hard ceiling 2 wall-clock hours.

### Confirmatory

Frozen core scenario families, paired policies, initial replications, and rule-based family-wide extensions; Slice 4 freezes a measured core ceiling no greater than 24 hours and permits at most one additional 24-hour family-wide extension window.

### Release

Full tests, source-provenance audit, formal consistency, simulator validation, freeze integrity, run completeness, MCSE receipt, negative controls, evidence-packet audit, and exact reproduction command; target under 30 minutes when existing confirmatory artifacts are verified rather than regenerated.

## Stop Conditions

Stop the active slice when:

- information ordering or authority classification remains circular;
- the workflow policy supplies its own evaluation support or materiality without an independently owned, source-labeled `sigma`;
- refinement coverage cannot be certified or fully bounded for a claimed universal F1 result;
- a sampled or witness-search refinement set is used to claim universal F1 pass;
- material action parameters cannot be represented as unambiguous action instances;
- material state transitions cannot be reconstructed with complete pre- and post-event versions;
- an F2 intervention unit, complete initial system state, valid hold intervention, branch-independent causal-event key, or deterministic paired-state alignment rule cannot be specified;
- F4 material items cannot be linked to surfaced items through an independently frozen semantic-correspondence rule;
- the evaluator cannot distinguish unknown scope, missing required input, invalid specification, and invalid aggregation with stable diagnostics;
- the selected application cannot meet the minimum defensible case threshold; pause the application path and narrow or version the Robodebt mapping; replacing the primary application requires a new plan and preregistration version;
- evidentiary, numerical, and legal claim types cannot be kept distinct;
- the emerging-technology contribution depends on asserting that Robodebt was modern AI or that a current system repeats it;
- the article equates process red-teaming or Robodebt's institutional failure with adversarial exploitation;
- `P0-Precursor` cannot reproduce the short paper's held-output comparison and no-change falsifier without changing a declared held variable;
- the formal contribution cannot be distinguished from existing literature;
- a golden trace fails;
- the simulator violates conservation or event-order determinism;
- analytical and simulated queue behavior disagree outside frozen tolerance;
- common-random-number pairing or keyed-draw stability fails;
- an application swap, domain-label rename, or unsupported-parameter rejection test fails;
- the pilot shows recipient response, evidence retrieval, or staffed queues never affect effective review or outcomes;
- the experiment only restates policy definitions;
- rare events cannot be estimated within the runtime ceiling;
- a stylized parameter loses its provenance label;
- the protocol, canary, classification rules, or worked-trace selection rule changes after confirmatory output inspection;
- the project lead cannot follow or explain the procedure after Slice 5 and the ambiguity is neither resolved nor classified as an explicit limitation;
- a post-result wording correction changes frozen semantics without a new freeze and rerun of affected artifacts;
- a realized contestability or restoration result is classified before its frozen evaluation horizon;
- confirmatory code, sources, seeds, or parameters change after freeze;
- the deadline cannot support the primary evidence packet; or
- partial work lacks an explicit deferred-work record.

## Acceptance Criteria

The core study is complete only when:

- The deliverable is a complete 10,000-word extended research paper, not a revised 1,500-word essay, research proposal, or design-only manuscript.
- The paper preserves a visible claim lineage from the completed precursor and labels every substantive refinement, narrowing, or rejection.
- The submitted article stands alone: it states the full hypothesis, definitions, fixture logic, case rationale, and limitations without requiring the short essay; explicit lineage comparison remains an internal audit rather than a reader-facing section.
- Reader-facing prose defines the “representation-preservation fixture” entirely from first principles; `P0-Precursor` remains an internal or supplementary artifact ID, and “precursor” is not used as an unexplained analytical concept.
- The main text distinguishes the base vulnerability from adversarial exploitability and states that Robodebt establishes neither a strategic actor nor the four attackability conditions.
- `P0-Precursor` directly reproduces the essay's held-output comparison, keeps every declared control variable identical, and includes the no-change falsifier.
- The formal model defines compatible-state ordering with conclusion-valid constructive refinement certificates, evidentiary fidelity, independently supported robust functional permission, formal-versus-functional authority, finite or symbolic fully instantiated action sets, trace-state lifting, and an authority-direction action taxonomy.
- Every stored formal, process, fixture, event, and result object validates the shared identity/version/ownership/provenance/hash envelope, and every decision branch emits the complete disposition schema.
- Operational policy and the independent evaluation specification remain distinct; the latter owns source-labeled support, materiality, required meaning and semantic correspondence, F2 intervention/alignment, baseline, action-comparison, feasibility, and restoration-obligation rules.
- A uniformly permissive workflow cannot pass F1 by using its own permission sets as the support oracle.
- Post-review progression binds the exact current action instance and versions to a recorded, unexpired authorization, remains in the current execution-state post-review set, and rechecks independent support at execution.
- F2 tests every added fallback with an explicit frozen hold intervention over a complete intervention unit, aligns divergent system traces by branch-independent causal cuts under identical cohort membership and keyed exogenous inputs, and recomputes robust support at the do-branch pre-state of any newly enabled focal or spillover progression; case-local evidence cannot support a system-level claim without a valid noninterference certificate.
- F4 uses exact semantic identity, an independently justified versioned mapping, or forward symbolic entailment from surfaced semantics to required action-relevant meaning rather than reverse implication, semantic overlap, display-text similarity, or workflow self-classification.
- Formal diagnostics distinguish unknown scope, missing required input, invalid specification, and invalid aggregation while reporting truth status separately from completeness; sufficient known failures dominate unknown conjuncts, and contextual helpers remain non-aggregating.
- F0–F5 use the frozen property-contract matrix; reported helpers and properties separate assessment status, optional value, diagnostic codes, and component results.
- F5 separates structural, prospective, realized-opportunity, uptake, and restoration outcomes and applies frozen reliability thresholds and horizons.
- F0-F5 have explicit scope, assumptions, boundary cases, and executable checks.
- The simulator has a closed case-neutral kernel/profile interface; canonical synthetic profiles exercise every core path before any application adapter is loaded.
- Every executable scenario references a compiled configuration that fixes its process, active policy, independent evaluation specification, application mapping where applicable, overlay, compiler identity, and complete parameter-binding receipts.
- Raw source artifacts remain immutable and non-executable; application bindings, not prose or guard strings, connect them to generic semantic targets.
- Process profiles own capabilities while policy profiles own active behavior; a counterfactual policy cannot create undeclared topology.
- Documented values cannot be overwritten, unsupported values cannot masquerade as history, and every runtime slot has exactly one visible owner.
- Removing the Robodebt adapter leaves all kernel, formal-property, queue, random-stream, and generic policy tests passing.
- The Robodebt adapter introduces no engine or policy branch and supplies no executable default for an `unsupported` historical parameter.
- R-OCI-Early and R-OCI-Enhanced each pass the source gate and have separate dated, source-anchored process maps.
- Every model-to-workflow mapping distinguishes documented structure, attributed statements, inference, stylized assumptions, and unsupported fields; executable stylized values live in separate versioned overlays.
- Every outcome and article claim distinguishes evidentiary support, numerical correctness, and legal status.
- The discrete-event engine produces deterministic hashes for identical seeds and configs.
- Golden traces, conservation checks, limiting cases, and analytical queue validation pass.
- U0, U1, U2C, U2O, and U3 are paired on identical cases and stable keyed exogenous draws within each scenario family.
- Validity constraints determine the final scenario count; invalid configurations fail diagnostically.
- Confirmatory sources, model, policies, parameters, seeds, metrics, exclusions, and analysis freeze before output inspection.
- Primary outcomes report evidentiary support, numerical error, gate safety, effective review, decision service, timeliness, agency workload, recipient burden, recovery exposure, and restoration separately.
- Results include paired estimates, Monte Carlo uncertainty, queue boundaries, and negative controls.
- Configured review, gate safety, effective review, and decision-service effectiveness are reported separately with failure reasons.
- Fail-closed and fail-open review outcomes remain separate.
- Null, adverse, and tradeoff results remain visible.
- The manuscript reports executed confirmatory results and does not use planned analyses as substitutes for findings.
- The main argument uses three headline propositions and H1-H3; the remaining formal results, H4-H5, and full diagnostics support rather than compete with that narrative.
- A practitioner can apply the five-step diagnostic from the main text without first reading the code or appendices; repository materials extend rather than substitute for that explanation.
- The protocol defines Level A document audit, Level B bounded deterministic trace, and Level C dynamic system simulation with minimum inputs, supported conclusions, prohibited conclusions, and mandatory escalation rules.
- Practitioner reports distinguish assessed properties from `omitted_by_claim_limit` receipts; the latter receive no formal status and cannot be counted as `not_applicable` or `unassessable`.
- Every practitioner output is a non-composite diagnostic profile that preserves property/helper statuses, completeness, diagnostics, interventions, owners, tradeoffs, and claim limits; no overall workflow pass or weighted policy score is inferred.
- The P0 usability walkthrough is reproduced by the Slice 1 smoke CLI from versioned stored records, with every report row linked to trace, assessment, and diagnostic artifacts.
- The protocol produces `pass`, `fail`, `unassessable`, or `not_applicable`, treats missing process documentation as an explicit limitation rather than `not_applicable`, and was frozen before confirmatory results.
- After Slice 5 analysis, the project lead completes the staged comprehensibility review on P0, the fixed Robodebt trace, and the synthetic AI canary; ambiguities and dispositions are retained without claiming independence or human-performance evidence, and semantic corrections trigger a new freeze and rerun.
- The worked trace follows a prespecified deterministic rule and is not selected after results for rhetorical force.
- The drafting target is 9,400 words, the 600-word contingency is tracked explicitly, and the submitted manuscript does not exceed the verified venue ceiling.
- Every article claim maps to a formal result, source, run artifact, table, figure, trace, or limitation.
- Exact reproduction commands and environment identifiers appear in the evidence packet.

The optional audit ablation is not part of core acceptance.

## Seven-Week Schedule

- **Week 1:** Slice 0; literature map, source packet, process diagram, formal constructs, precursor-to-extension continuity table, protocol candidate, held-out AI canary, fixed trace-selection rule, and contingency-aware article outline.
- **Week 2:** Slice 1; case-neutral dynamic vertical slice, golden traces, adapter smoke test, and formal-model draft.
- **Week 3:** Slice 2; stochastic kernel, profile and overlay validation, policy implementations, queue validation, and methods draft.
- **Week 4:** Slice 3 and Slice 4; pilot, application-sufficiency and adapter-swap review, executable fixture/reference checks, pre-result protocol revision, precision and runtime decisions, application/protocol/scenario freeze, and dummy analysis rehearsal.
- **Week 5:** Slice 5; confirmatory execution, convergence checks, primary analysis, and results draft.
- **Week 6:** Slice 6; project-lead procedure comprehensibility review, evidence packet, and complete 10,000-word article draft with executed results. Enter optional Slice 7 only if Slice 6 finishes early.
- **Week 7:** Cross-persona claim red team, venue-fit review, limitations, revision, formatting, and submission preparation.

If the schedule slips, cut the optional audit, nonessential sensitivity analyses, later EIC/CUPI/PAYG variants, and presentation artifacts first. Do not cut the minimum defensible application mapping, formal constructs, simulator validation, primary dynamic experiment, negative controls, freeze integrity, provenance separation, or claim-boundary memo.

## Execution Ledger

The canonical status and per-slice receipts are now maintained in `docs/EXECUTION_LEDGER.md`. Do not recreate a second status table here.

## Final Completion Audit

Before declaring the study complete, answer with stored evidence:

1. Is information ordering independent of the downstream permission result?
2. Are observed values, imputed values, missing evidence, and disputed values distinguishable end to end?
3. Are evidentiary support, numerical correctness, and historical legal validity reported as separate claim types?
4. Does the action taxonomy distinguish formal authority, functional permission, operational action, and precautionary constraint?
5. What is formally established, and under which assumptions and refinement set?
6. Are R-OCI-Early and R-OCI-Enhanced separately dated and sourced without later variants leaking into either profile?
7. Does the dynamic simulation add findings not already true by policy definition?
8. When do gate safety, effective review, and decision service diverge, and why?
9. Are notice delivery, administrative access, evidence retrieval, queue overload, deadline expiry, debt action, recovery exposure, and correction visible in the results?
10. Do paired policies share identical cases and stable case/event-keyed exogenous draws even when their event paths diverge?
11. Are evidentiary support, numerical error, delay, agency workload, recipient burden, recovery exposure, and restoration reported without a hidden utility weighting?
12. Did any confirmatory source, parameter, seed, metric, or analysis change after freeze?
13. Does every historical, legal, and organizational claim have a source anchor?
14. Does every quantitative claim have a run artifact and uncertainty statement?
15. Is the emerging-technology transfer limited to the formal invariant, red-team method, and supported institutional connections?
16. Are incomplete or optional subsystems removed or explicitly deferred?
17. Can a repository user reproduce the primary traces, simulation, and analysis from the recorded commands alone?
18. Does the manuscript clearly extend rather than replace the completed 1,500-word essay?
19. Does the 10,000-word paper report conducted analysis and results rather than stop at a formal model and research design?
20. Does the precursor-to-extension continuity table identify every retained, refined, tested, bounded, or rejected claim?
21. Were the protocol semantics, canary, output classifications, and worked-trace rule frozen before confirmatory results?
22. Can the protocol explicitly return `unassessable` when evidence lineage, authority, timing, or process documentation is missing?
23. Did the project lead complete the post-simulation comprehensibility review, record every material ambiguity, and avoid presenting it as independent validation?
24. Does the held-out AI canary demonstrate vocabulary-independent use without being presented as a second empirical case?
25. Did the manuscript stay within the verified ceiling while preserving the 9,400-word core and documenting any use of the 600-word contingency?
26. Does `P0-Precursor` hold the uncertain model output, downstream rule, and process state fixed while varying only the interface representation?
27. Does the paper distinguish base vulnerability, structural susceptibility, process red-teaming, and adversarial exploitability without attributing attackability to Robodebt?
28. Does the main-text AI canary explicitly develop the precursor's LLM-summary example rather than introduce an unrelated emerging-technology vignette?
29. Can a reader understand the hypothesis, representation-preservation fixture, formal claims, Robodebt rationale, simulation, and limitations without opening the short essay?
30. Are lineage comparisons confined to internal drafting controls, acknowledgments, or a concise origin statement rather than organizing the published article as a sequel?
31. Does every protocol application declare Level A, B, or C and remain within that level's claim limits or explicitly escalate?
32. Does the practitioner report preserve the complete assessment profile without an overall compliance score or hidden weighted ranking?
33. Can the project lead move from the intake worksheet through the P0 walkthrough to the executable report and trace every row to stored evidence?
34. Were all post-simulation corrections classified as editorial or semantic, with every semantic correction receiving a new freeze and rerun of affected confirmatory artifacts?
35. Does every unassessed higher-level claim use an `omitted_by_claim_limit` receipt rather than a fabricated fifth status or misleading `not_applicable` result?
36. Can every kernel test run without importing or loading the Robodebt adapter?
37. Does an isomorphic adapter with different domain vocabulary preserve semantic traces, formal assessments, and metrics?
38. Does every executable value absent from the historical record come from a separate, visibly stylized overlay rather than a source profile?
39. Was the selected application, adapter, source packet, parameter-provenance table, and worked-trace rule frozen before confirmatory output inspection?

If any answer is unsupported, the corresponding claim or subsystem remains incomplete.
