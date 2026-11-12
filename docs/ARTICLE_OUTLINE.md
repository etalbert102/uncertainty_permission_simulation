# Article Outline: From Incomplete Evidence to Automated Action

Status: results-informed drafting outline; design-frozen simulation and candidate evidence packet complete; manuscript-audit candidate selectively merged at 8,958 call-counted main-text words excluding bibliography; detailed protocol machinery and worked-trace receipts moved to a publication-facing supplement while the five substantive steps remain in the article; citation and source-description defects corrected; final publisher-style formatting, independent source-anchor verification, publisher-rendered count, and submission-readiness receipt pending; one prespecified service metric excluded after semantic audit; no formal comprehensibility review required

Working title: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

Target: a standalone article of no more than 10,000 words for the Stanford CISAC/GTG volume *Emerging Technologies and the Future of Decision-Making*

## Paper Promise

The paper explains and demonstrates a process-level failure mode: weaker or coarsened evidence can expand what an organization is functionally permitted to do when representation, routing, review, or timeout rules relax safeguards. It contributes:

1. a formal model separating evidence, representation, formal authority, functional permission, action, review, contestability, and restoration;
2. a deterministic controlled pair showing how representation alone can change routing and automatic permission;
3. a documented Robodebt process application that establishes institutional relevance without pretending to numerically reconstruct historical Robodebt;
4. a frozen finite-cohort dynamic simulation showing how review capacity and timeout semantics change organizational outcomes; and
5. a five-step process-red-team protocol designed for practical application.

The article stands alone. The 1,500-word precursor essay is lineage evidence, not required reading, and its title or argument must not be used as an unexplained premise.

## Results-Led Thesis

Uncertainty does not expand authority by itself. Authority expands when a workflow turns incomplete evidence into a representation, route, or timeout rule that permits progression without the safeguards the evidence state requires. In the design-frozen simulation, fail-closed review remained gate-safe as load rose but accumulated unresolved holds, while the matched fail-open design converted the same review shortfall into unsupported progression and recovery exposure. The information-first policy avoided unsupported progression, but its prespecified interaction-event proxy moved opposite the expected burden direction and agency-workload events increased; because that proxy does not measure effort or welfare, the substantive evidence-production-burden question remains unresolved. Effective governance therefore requires explicit choices among safety, timeliness, burden, workload, exposure, and restoration rather than a nominal reviewer or a single “best policy.”

## Claim Hierarchy

- **Historical claims:** source-attributed facts about early and enhanced Online Compliance Intervention processes.
- **Formal claims:** propositions that follow from the declared definitions, assumptions, and counterexamples.
- **Simulation claims:** estimates within the frozen 108-family stylized parameter space.
- **Application-oriented contribution:** a complete five-step protocol, worked example, and worksheets intended to make the method easier to apply. The paper does not claim validated usability, practitioner performance, or reproducible classifications by new users.

Never convert a simulation estimate into historical Robodebt prevalence, capacity, monetary error, legality, or causation. Never treat process red-teaming as evidence of historical strategic attack.

### Design-freeze interpretation and measurement-audit decision

The repository artifact named `PREREGISTRATION.md` is an internal prospective design-freeze record, not a claim that this computational demonstration was externally preregistered or that it tests population-level empirical hypotheses. It documents that scenarios, policies, seeds, metrics, stopping rules, and planned contrasts were fixed before core-output inspection. The reader-facing article should call this a **prespecified simulation protocol**, **prospective analysis plan**, or **design freeze**.

The prespecified `DecisionServiceEffective` concept remains part of the formal and practical framework, but its core simulation output is excluded from substantive interpretation. The implementation counted every case without a review request as successful service rather than verifying a supported disposition by the service deadline. This makes cross-policy values—especially U3−U0—semantically invalid and makes the label unsafe even where a policy-specific value happens to track effective review.

The article must report this exclusion as a post-run construct-validation finding, omit the numerical service estimates from substantive tables and figures, and avoid substituting another outcome after results were seen. This is a limitation of the computational demonstration, not evidence about an empirical population. Repairing the metric would require a new version, freeze, and affected rerun; this outline does not retrofit the frozen study.

## Word Budget

| Section | Words | Required job |
| --- | ---: | --- |
| 1. Introduction | 700 | State the problem, completed design, findings, contribution, and boundaries. |
| 2. Mechanism, literature, and research questions | 800 | Establish the mechanism from first principles and locate the contribution. |
| 3. Formal model | 1,150 | Present only the constructs and propositions needed to understand and use the method. |
| 4. Robodebt process application | 1,100 | Establish the documented case mapping and its inference limits. |
| 5. Dynamic simulation methods | 1,200 | Make the executed design, estimands, validation, and claim boundary reproducible. |
| 6. Results | 1,800 | Report the three prespecified expectations, measurement exclusion, controls, sensitivity, censoring, uncertainty, and tradeoffs. |
| 7. Process-red-team protocol and governance implications | 1,600 | Deliver the five-step method, fixed worked example, interventions, and bounded transfer. |
| 8. Limitations and conclusion | 750 | Bound interpretation and state the transferable result. |
| **Named-section subtotal** | **9,100** |  |
| **Reserve** | **900** | Abstract, captions, transitions, endnotes, and necessary qualifications. |
| **Maximum** | **10,000** | Bibliography excluded under the verified call. |

Draft a 200–250-word abstract from the reserve after the main text is stable.

This results-informed 9,100-word core and 900-word reserve supersede the pre-results 9,400-word core and 600-word reserve in `docs/STUDY_PLAN.md`; they do not alter the 10,000-word submission ceiling or any simulation contract.

## Abstract — Draft Last

Use six moves:

1. Problem: automated workflows can convert incomplete evidence into consequential action even when each component follows its local rule.
2. Gap: component accuracy, transparency, and nominal human review do not show that uncertainty remains operationally constraining.
3. Method: formal model, deterministic representation pair, documented Robodebt mapping, and prospectively design-frozen dynamic simulation.
4. Findings: fail-closed safety/backlog tradeoff; fail-open conversion of delay into unsupported progression; adverse prespecified interaction-event result with substantive burden unresolved.
5. Boundary: stylized designed-parameter-space findings, extensive terminal censoring, and exclusion of the semantically invalid service metric—not a numerical reconstruction or legal judgment about Robodebt.
6. Contribution: an application-oriented process-red-team protocol for tracing evidence into functional permission.

Do not open with Robodebt, use policy IDs, or claim a universally preferred policy.

## 1. Introduction — 700 Words

### 1.1 The organizational failure mode — 180 words

- Open with the standalone puzzle: a defensible abstraction can remove the distinction that would trigger caution.
- Follow the full chain: evidence → representation → routing → review → action → correction/restoration.
- Define functional permission in plain language: what the operating workflow allows to proceed, whether or not formal authority changed.
- State the paper's central question: when evidence becomes less decision-relevant, what may the workflow now do automatically?

### 1.2 Why nominal review is insufficient — 130 words

- Distinguish a configured gate, a gate that remains fail-closed, effective review, and timely supported decision service.
- Explain why a review field, notice, or appeal right can coexist with ineffective intervention.
- Introduce capacity and timeout semantics as organizational design choices, not implementation details.
- Preserve timely supported service as a concept while flagging that the core simulation did not validly operationalize it.

### 1.3 Completed research design — 170 words

- Name the four evidence layers: deterministic representation pair, formal model, documented Robodebt process mapping, and dynamic simulation.
- Explain why Robodebt is analytically useful while stating that it was not a modern generative-AI system.
- State that the simulation uses source-anchored process structure plus visibly stylized parameters and counterfactual policies.

### 1.4 Findings and contributions — 220 words

- Preview expectation 1: fail-closed review preserved gate safety at every tested load while effective review fell and unresolved holds rose; describe this as a capacity response across three prespecified loads, not an estimated threshold.
- Preview expectation 2: fail-open timeouts converted the same capacity shortfall into unsupported progression and recovery exposure.
- Preview expectation 3 honestly: the conditional evidence-production-burden expectation was not answerable as framed. In the prespecified unconditional U3−U0 contrast, the interaction-event proxy increased along with agency workload; substantive recipient burden remains unresolved.
- State that the invalid `DecisionServiceEffective` simulation output is excluded and that extensive terminal censoring prevents complete-restoration claims.
- State the formal, computational, institutional, and practical contributions.
- End with the roadmap and the historical/formal/simulation claim boundary.

Core exhibit: **Figure 1, evidence-to-action chain with the five protocol steps.**

## 2. Mechanism, Literature, and Research Questions — 800 Words

### 2.1 Representation-preservation controlled pair — 210 words

- Define “controlled pair” explicitly: two deterministic traces of the same synthetic case and model output, with the policy, downstream rule, reviewer resource, clock, and zero random draws held fixed.
- Preserve arm: typed alternatives, confidence, uncertainty, and provenance remain visible.
- Fallback arm: the same output becomes the broad untyped label `vehicle`.
- Explain how this sole representation change alters routing, scrutiny, gate configuration, and automatic permission.
- State what the pair does not test: model accuracy, latent truth, frequency, queues, or historical behavior.

This plain-language definition resolves an author-noted ambiguity and must appear before any formal notation.

### 2.2 Mechanism and bounded expectation — 170 words

- State the three conditions: a defensible representation, a hidden policy-relevant distinction, and downstream relaxation of a safeguard.
- Separate progression actions from constraints, information acquisition, and restoration.
- Separate base vulnerability from attackability; attackability additionally requires inducibility, observability, repeatability, and benefit.

### 2.3 Literature and originality — 270 words

Organize prior work into three functional clusters:

- uncertainty, calibration, abstention, and uncertainty communication;
- human oversight, contestability, administrative burden, and algorithmic administration; and
- sociotechnical assurance, process safety, and red teaming.

Treat uncertainty-to-action binding as prior work. Locate the paper's narrower contribution in its information-refinement invariant, independently supported automatic progression, finite-capacity review, restoration semantics, executable controls, and documented process application. Avoid exhaustive-absence or “first paper” claims.

### 2.4 Three research questions and falsifiability — 150 words

1. When may weaker evidence safely support automatic progression?
2. When does a configured safeguard remain safe, effective, and timely under access and capacity constraints?
3. Which interventions avoid unsupported progression without hiding delay, burden, workload, exposure, or unresolved cases?

Name the falsifiers: no representation-to-permission change in an enabling controlled pair; no capacity/timeout effect across the frozen range; or no diagnostic value beyond component-local checks.

## 3. Formal Model — 1,150 Words

### 3.1 Evidence, compatible states, and refinement — 200 words

- Define evidence state, compatible-state set, and independently specified refinement/coarsening.
- Explain why confidence alone is not an information order.
- Distinguish exact finite, symbolic exact, conservative outer, and witness-search certificates; search cannot establish universal pass.

### 3.2 Representation and evidentiary fidelity — 160 words

- Define the representation map and typed evidence states: observed, derived, imputed, disputed, and missing.
- Present F0 evidentiary fidelity and F4 material surfacing.
- Explain uncertainty laundering: an aggregate can remain numerically consistent while losing the distinctions needed for policy or review.

### 3.3 Authority, permission, and action — 170 words

- Separate formal authority, automatic functional permission, and executed action.
- Define fully instantiated actions and the progression/constraint/information/restoration taxonomy.
- Separate operational policy from the independently owned evaluation specification.
- Require support to be reevaluated after material changes in evidence, representation, time, policy, or rule version.

### 3.4 Robust permission and safe fallbacks — 210 words

- State F1: a progression action automatically permitted under weaker evidence must be independently supported under every certified admissible refinement.
- State F2: a new constraint or information fallback is safe only under a valid execute-versus-hold intervention over the complete unit, including spillovers when resources are shared.
- Give one minimal satisfying example and one counterexample.
- Make clear that uncertainty may safely expand information-seeking or reversible constraint without expanding progression authority.

### 3.5 Review, service, contestability, and restoration — 210 words

- State F3 review-preserved progression and distinguish `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective`.
- Require review authorization to bind the exact action, evidence and rule versions, conditions, and expiry.
- State F5 and distinguish structural correction, prospective reliability, realized correction, and complete restoration.
- Explain that correction of a decision coordinate does not prove restoration of every consequence.

### 3.6 Two formal propositions and one simulation implication — 200 words

- Proposition 1: weaker evidence cannot justify new automatic progression outside the independent support envelope.
- Proposition 2: fail-closed and fail-open review may have identical review completion but opposite permission consequences under overload.
- Give a compact proof sketch or constructive argument for each proposition in the main article, including its load-bearing assumptions. Full notation and proofs remain in the repository supplement.
- Simulation implication, not a formal proposition: under the frozen U3 implementation and parameter space, information acquisition exchanged unresolved holds for more interaction events, agency workload, and downstream exposure; this is contingent on the modeled process and cannot be proved from the formal definitions alone.
- Move full notation, proofs, subordinate lemmas, and exhaustive counterexamples to repository supplement Module A.

## 4. Robodebt as a Documented Process Application — 1,100 Words

### 4.1 Why this case — 140 words

- Explain the analytical fit: aggregate evidence, evidentiary transformation, notice and access, deadlines, automation, review, recovery, correction, and restoration.
- Explain why the case is useful for process analysis without presenting it as contemporary AI equivalence.

### 4.2 Sources and application validity — 180 words

- Identify the Royal Commission and other authoritative process sources and the source cutoff.
- Separate documentary validity, structural mapping validity, and numerical calibration validity.
- State that the first two are supported within the mapped scope; the third is deliberately not claimed.

### 4.3 Early OCI process profile — 300 words

- Trace annual income matching, transformation into fortnightly values, notice, recipient evidence burden, deadlines, automated debt progression, review opportunity, and recovery.
- Mark which facts are documented and which executable quantities remain unsupported historically.
- Locate the representation-to-permission transition without inferring strategic exploitation.

### 4.4 Enhanced OCI and repair mechanisms — 180 words

- Describe documented changes in evidentiary handling, review, and correction while keeping dates and process variants separate.
- Treat enhanced OCI as a bounded repair profile, not proof that every failure was eliminated.

### 4.5 Formal crosswalk and inference limits — 200 words

- Map source records to evidence states, transformations, actions, gates, review, contestability, and restoration.
- Explain why unsupported historical parameters cannot become executable defaults.
- State the legal, monetary, prevalence, causation, and behavioral non-claims.

### 4.6 Transition to simulation — 100 words

- Explain that Robodebt establishes structural relevance; the simulation tests counterfactual governance mechanisms over a stylized parameter space.
- Introduce the policies as study-owned interventions, not descriptions of historical alternatives.

Core exhibit: **Figure 2, early and enhanced OCI process maps with source/stylized boundaries.**

## 5. Dynamic Simulation Methods — 1,200 Words

### 5.1 Kernel and unit of analysis — 170 words

- Describe the case-neutral discrete-event kernel, finite cohorts, queues, deadlines, keyed exogenous draws, complete state snapshots, and administrative cutoff.
- Explain common-random-number pairing and branch-independent causal keys.
- State that Robodebt identifiers do not enter generic kernel logic.

### 5.2 Five policy designs — 250 words

| Policy | Operational role | Central tradeoff |
| --- | --- | --- |
| U0 | Claimant-led evidence and hold | avoids unsupported progression but can retain unresolved cases and recipient effort |
| U1 | Impute and progress | failure benchmark, not a recommendation |
| U2C | Impute, review, fail closed | preserves gate safety but can accumulate unresolved holds |
| U2O | Impute, review, fail open | resolves timeouts through progression at the risk of unsupported action |
| U3 | Agency-assisted information first | seeks support but consumes agency resources and may add interactions or exposure |

Define these as counterfactual study policies. Do not label any as historical Robodebt policy.

### 5.3 Design-frozen scenario and execution — 260 words

- Report five factors: load, missing evidence, administrative-access barrier, evidence retrievability, and staff access.
- Report 108 valid families, 80 cases per family-replication, five paired policies, and 30 replications.
- Core: 16,200 family-policy-replication runs, representing 1,296,000 simulated case-policy trajectories. Sensitivity: the same number of runs and trajectories in a separate suite with evidence-retrieval latency doubled from 10 to 20.
- Report the frozen seed inventories, day-650 cutoff, no precision extension, manifest identity, and complete reconciliation.
- Explain the role of the design freeze in one concise methods paragraph: protection against result-driven tuning and support for exact reproduction, not conversion of a constructed simulation into population-level empirical inference.
- Map reader-facing expectations 1–3 to internal freeze labels H1–H3 once in Table 1 or a methods note; do not repeat the internal labels in headings.

### 5.4 Outcomes and estimands — 260 words

- Interpretable primary safety/process rates: unsupported progression, gate safety, effective review, unresolved hold, external/recovery-process exposure, and right-censoring.
- The prespecified recipient interaction-event rate equals responses plus assistance requests per initiated case. Preserve its frozen field name, `recipient_burden_rate`, in reproducibility materials, but do not call it a direct measure of evidence-production burden, subjective burden, effort, welfare, or monetary cost.
- Agency-workload event rate equals completed assistance, retrieval, review, and reassessment events per case.
- Prespecified substantive contrasts: U2O−U2C and U3−U0. Report U1−U0 separately as an implementation-validation contrast, not a substantive result.
- Report family-specific paired estimates, 95% MCSE intervals, cross-family variation, and load-stratified descriptive summaries. Explain that MCSE intervals quantify finite-run simulation noise, not population sampling uncertainty, historical uncertainty, or model uncertainty.
- Label cross-family and load-stratified means as unweighted summaries over the deliberately designed scenario families. Do not present them as estimates for a real-world scenario distribution.
- Exclude numerical `DecisionServiceEffective` simulation results: the implemented numerator treated every no-review case as successful service instead of checking for a supported disposition by the deadline.

### 5.5 Validation, controls, and claim boundary — 260 words

- Summarize hand traces, queue checks, deterministic replay, configuration closure, adapter swap, negative controls, and append-only receipts.
- Report 32,400 reconciled family-policy-replication runs across both suites, representing 2,592,000 simulated case-policy trajectories. Describe the 178 tests as automated validation checks, then report maximum core MCSE `0.04332` and maximum sensitivity MCSE `0.04051`.
- Distinguish execution integrity from measurement validity: all runs reconciled and passed their design-frozen checks, but the post-run semantic audit invalidated the service interpretation.
- State that the simulation estimates only the declared model and parameter space; do not use successful execution to rehabilitate an invalid construct.
- Explain stage-specific censoring and why an open path at day 650 cannot be treated as completed restoration or failure.

Core exhibit: **Table 1, policy definitions, frozen contrasts, and claim limits.**

## 6. Results — 1,800 Words

### 6.1 Integrity, measurement audit, and precision — 220 words

- Report complete reconciliation: 16,200 core and 16,200 sensitivity family-policy-replication runs, zero missing or unexpected IDs.
- Report MCSE compliance, negative controls, deterministic replay, and the absence of execution changes after the design freeze.
- Report the `DecisionServiceEffective` semantic mismatch as a post-run construct-validation failure, not an execution failure or an empirical-population finding. Show the intended definition, implemented numerator, reason for exclusion, and rerun requirement for any future repair.
- State the unit of every number before interpretation.
- State at the outset that U0, U2C, and U3 are terminally right-censored in every family-level cell, so the study cannot estimate their complete-restoration rates.

### 6.2 Prespecified expectation 1: fail-closed safety across tested load regimes — 320 words

- Report that U2C gate safety remained `1.000` at low, middle, and high load in the descriptive load summaries.
- Report that mean effective review across the other factors fell from `0.857` to `0.502` to `0.212` as load rose from `0.6` to `0.95` to `1.2`.
- Report that unresolved holds rose from `0.143` to `0.498` to `0.788` over the same load levels.
- State that the gate-safety, effective-review, and unresolved-hold pattern matches the prespecified expectation within the designed parameter space; its service component was not evaluable because that measure failed semantic audit. Three prespecified load levels show a capacity response but do not locate a threshold or estimate a continuous boundary.
- Do not describe unresolved holds as harmless or historical frequencies.

### 6.3 Prespecified expectation 2: fail-open timeouts convert delay into progression — 330 words

- Compare U2O with U2C on paired families.
- Report the family-level U2O−U2C unsupported-progression differences: cross-family descriptive mean `+0.476`, range `+0.042` to `+0.881`; every family-specific 95% MCSE interval excludes zero.
- External/recovery-process-exposure differences match that direction and magnitude; unresolved holds and gate safety move in the opposite direction.
- Report that effective-review rates are identical between U2O and U2C within each matched family: timeout semantics change what happens after review failure, not whether review completed.
- State that the direction of the fail-open/fail-closed contrast follows from the declared policy semantics. The simulation contribution is its magnitude, family variation, and queue-dependent tradeoff—not the discovery that fail-open permits progression.
- Explain that exposure is structurally downstream of progression in this kernel and therefore is not an independent replication of the unsupported-progression result.
- State that the paired estimates exhibit the prespecified modeled pattern and quantify its operating consequences without presenting fail closed as costless or treating the result as evidence about a real-world population.

### 6.4 Prespecified expectation 3: information-first tradeoff — 390 words

- Lead with the disposition: the conditional evidence-production-burden expectation was not answerable as framed. The executed contrast is unconditional across designed families, the interaction-count proxy does not measure evidence-production effort or welfare, and the service measure failed semantic audit.
- U3 and U0 both produced zero unsupported progression, so U3 could not improve that safety outcome relative to an already conservative hold policy.
- In the separately prespecified unconditional comparison across families, U3−U0 increased the recipient interaction-event proxy per case by a descriptive mean of `1.096` (range `0.860` to `1.312`) and agency-workload events by `1.209` (range `0.749` to `1.728`); all family-specific MCSE intervals exclude zero.
- U3 sharply reduced unresolved holds but increased external/recovery-process exposure. Explain that exposure can follow supported progression and is not itself proof of unsupported action or harm. Do not report the invalid decision-service contrast.
- Interpret the finding as a tradeoff: information acquisition can resolve cases, but this implementation adds interactions and organizational work rather than simply transferring effort away from recipients.
- State the construct-validity result precisely: the prespecified proxy moved opposite the expected direction, but it cannot establish whether U3 increased or reduced evidence-production effort, subjective burden, or welfare. The conditional substantive-burden expectation remains unresolved rather than rejected.

### 6.5 Censoring, controls, and sensitivity — 300 words

- Lead with policy-specific right-censoring. U0, U2C, and U3 remained open at the declared terminal horizon in every family-level cell, while U1 and U2O had lower but material censoring.
- Break censoring out by reason in repository supplement Module D and prohibit claims of complete restoration from open paths.
- Explain that administrative observation closure is not case resolution and that stage-level event findings remain interpretable only within their declared horizons.
- Report the U1 failure-benchmark contrast and the five negative controls without treating implementation validation as a substantive discovery.
- Report that doubling evidence-retrieval latency left the principal qualitative patterns intact; keep sensitivity estimates separate from the core.

### 6.6 Synthesis — 240 words

Answer the three questions directly:

1. weaker evidence may not automatically expand progression beyond independently supported actions;
2. fail-closed review can preserve gate safety while effective review deteriorates, whereas fail-open timeouts convert the same review shortfall into permission and exposure; and
3. information acquisition must be evaluated on interaction events, workload, timing, exposure, and restoration rather than assumed to dominate conservative holding; its effect on substantive recipient burden remains unmeasured here.

Separate formal, simulated, and historical evidence in a compact matrix. State the strongest finding, most important tradeoff, and largest unresolved uncertainty. Repeat that the service metric is excluded and that terminal censoring prevents complete-restoration comparisons.

Core exhibits:

- **Figure 3, multi-panel capacity, timeout, and information-first tradeoffs.**
- **Table 2, prespecified paired estimates, MCSE, scenario range, and claim boundary.**

## 7. Process-Red-Team Protocol and Governance Implications — 1,600 Words

### 7.1 What the protocol produces — 200 words

- State the boundary first: usability is a design objective, not an evaluated outcome of this study.
- Define the unit: one evidence-to-action path through representation, routing, review, action, and restoration.
- Present Levels A, B, and C with their minimum inputs, claim limits, and escalation rules.
- Explain `assessed` versus `omitted_by_claim_limit`.
- Define `pass`, `fail`, `unassessable`, and `not_applicable`, with completeness reported separately.
- Prohibit an aggregate compliance score or weighted policy ranking.

### 7.2 Step 1: map transformations and ownership — 160 words

- Inventory evidence types, transformations, assumptions, visibility, provenance, and ownership.
- Locate the first transition where a policy-relevant distinction disappears.
- Apply F0 and F4.

### 7.3 Step 2: test what weaker evidence permits — 160 words

- Inventory exact progression, constraint, information, and restoration actions.
- Test automatic progression against an independent support rule and valid refinement certificate.
- Treat defaults and fail-open timeouts as permission rules.

### 7.4 Step 3: test operational review — 160 words

- Separate gate configuration, gate safety, effective review, and timely supported service conceptually; do not use the excluded simulation output as an example of valid service measurement.
- Check evidence visibility, stopping authority, dependency, timing, exact authorization, and execution-state support.

### 7.5 Step 4: stress access, workload, and deadlines — 160 words

- Select the simplest adequate level: document audit, bounded trace, or system simulation.
- Report safety, delay, recipient burden, agency workload, exposure, and unresolved cases separately.

### 7.6 Step 5: test contestability and restoration — 160 words

- Separate structural correction, prospective reliability, realized opportunity, uptake, correction, and restoration.
- Require a consequence vector and baseline before claiming complete restoration.

### 7.7 Fixed Robodebt worked example — 300 words

- Apply all five steps to the prespecified deterministic early-OCI-style trace and its repair arm.
- Show what component-local checks see, then locate the process-level transition and operational consequence.
- Record status, completeness, diagnostic, owner, intervention, tradeoff, and claim limit for each row.
- Do not call the trace representative or statistically typical.

### 7.8 Governance interventions and bounded transfer — 300 words

- Connect each failure mechanism to a specific intervention and empowered owner.
- Report the tradeoff for provenance preservation, evidence acquisition, fail-closed review, capacity reservation, deadline change, recovery pause, and restoration.
- Apply the protocol briefly to the held-out LLM-summary canary as a transfer check, not a second empirical case.
- Use ordinary author editorial QA: define “controlled pair” in plain language, resolve material clarity issues, and state residual limitations without creating a formal comprehensibility or usability claim.

Supplementary exhibits: **Tables S1–S2, assessment profile and ownership/intervention receipt for the fixed Robodebt trace.**

Section 7 makes no formal usability claim. The stored P0, Robodebt, and canary examples plus the evidence-packet traceability check may inform ordinary author editing; they are not a required evaluation.

## 8. Limitations and Conclusion — 750 Words

### 8.1 Limitations — 450 words

Address each limit and say whether it narrows interpretation or requires new evidence:

- formal dependence on the declared refinement set, action order, and support rule;
- documentary boundaries around early and enhanced OCI profiles;
- stylized parameters and lack of historical numerical calibration;
- exclusion of the semantically invalid core `DecisionServiceEffective` output and the absence of a valid simulated timely-supported-disposition comparison;
- an interaction-event proxy that cannot establish evidence-production effort, subjective burden, or welfare;
- extensive policy-specific terminal censoring;
- no modeled reviewer psychology, discretion, deference, or strategic behavior;
- no legal adjudication or monetary-entitlement oracle;
- no scalar normative ranking across safety, service, burden, workload, exposure, and restoration;
- no practitioner study, usability validation, or evidence that new users will reproduce the protocol's classifications;
- bounded transfer to contemporary AI workflows; and
- no evidence of historical adversarial exploitation.

### 8.2 Conclusion — 300 words

- Return to the opening question about what weaker evidence newly permits.
- State the formal answer under the declared assumptions.
- State the simulation answer: timeout semantics determine whether review shortfall becomes unresolved holding or unsupported progression; the modeled information-first policy created additional interaction and workload events, while its effect on substantive recipient burden remains unresolved.
- State that the study does not estimate a capacity threshold, complete restoration for heavily censored policies, or timely supported service across policies.
- Reaffirm that meaningful control is a property of the full evidence-to-action process under load.
- Close with the transferable diagnostic: what may the system now do, who can still stop it, and can they do so before the consequence becomes difficult to restore?

## Core Exhibit Plan

| ID | Exhibit | Section | Evidence owner |
| --- | --- | --- | --- |
| Figure 1 | Evidence-to-action chain and five protocol steps | 1, 7 | formal model and protocol 1.0 |
| Figure 2 | Early and enhanced OCI process maps | 4 | source manifest and process profiles |
| Table 1 | Policies, contrasts, metrics, and claim limits | 5 | frozen configs and prospective design-freeze record |
| Figure 3 | Multi-panel capacity, timeout, and information-first tradeoffs | 6 | core and sensitivity analysis receipts |
| Table 2 | Prespecified paired estimates and computational precision | 6 | analysis receipts |
| Tables S1–S2 | Assessment profile and ownership/intervention receipt for the fixed trace | supplement | frozen protocol and worked-trace receipt |

Five main-text exhibits are the current ceiling. The publication-facing supplement carries Tables S1–S2 and the detailed protocol machinery; exhaustive formal results, full scenario tables, censoring reasons, controls, sensitivity details, and source crosswalks remain in repository supplement modules.

## Repository Supplement Modules

- **Module A:** notation, propositions, proof sketches, and counterexamples.
- **Module B:** source manifest, dated Robodebt profiles, crosswalk, and inference limits.
- **Module C:** simulation schemas, parameters, validation, design-freeze record, and reproducibility receipts.
- **Module D:** full family-level results, controls, censoring reasons, sensitivity, and trace-selection receipt.
- **Repository supplement:** protocol worksheets, example inputs/reference profiles, executable traces, evidence packet, and commands. Optional author editorial notes are not a study result.

These modules are repository supplements, not submitted appendices. The publication-facing protocol supplement is a separate candidate artifact; whether it may accompany submission outside the 10,000-word ceiling must be confirmed against the publisher's instructions. If it counts toward that ceiling, it must be shortened or withheld rather than silently added to the article. The main article must remain understandable without the repository or supplement.

## Drafting Order

1. Build Table 2 and Figure 3 directly from the stored analysis receipts; exclude the invalid service metric and lock the result language and units.
2. Draft Sections 5 and 6 from the frozen configs, manifest, reconciliation, and analysis artifacts.
3. Draft Sections 3 and 4 from the formal model and source packet, retaining only notation used later.
4. Run an ordinary author editorial pass over the protocol presentation; no formal review return is required, and any semantic defect still triggers a new freeze and affected rerun.
5. Draft Section 7 from the frozen protocol, fixed Robodebt trace, canary, and completed review; render the full trace as Tables S1–S2 in the publication-facing supplement.
6. Draft Section 2 so the mechanism and literature lead naturally into the formal and simulation contributions.
7. Draft Section 1, Section 8, and the abstract last from the locked claim/evidence matrix.
8. Run the word-count, claim-to-evidence, standalone-reader, source, and reproduction audits before prose polish.

## Completion Gates

- Total counted words do not exceed 10,000; the 900-word reserve and 9,100-word named-section target are tracked rather than silently consumed.
- Every quantitative statement names its unit and points to a stored analysis artifact.
- The reader-facing paper describes the prospective analysis record as a simulation design freeze, not an empirical preregistration; internal H1–H3 labels are mapped once to prespecified expectations and omitted from section headings.
- The invalid `DecisionServiceEffective` simulation output is omitted from substantive tables, figures, and conclusions; the construct-validation exclusion is disclosed in methods and results. Any repair requires a new version, freeze, and affected rerun.
- Expectation 1 is described as a capacity response across three tested loads, not a located threshold or continuous boundary.
- Expectation 2 distinguishes policy-semantic direction from simulated magnitude and scenario variation; exposure is not presented as independent confirmation of progression.
- Expectation 3 is classified as not answerable as framed; the unconditional adverse proxy result and unresolved conditional substantive-burden claim are visible in the abstract, introduction, results, and conclusion rather than buried.
- MCSE intervals are identified as computational-precision intervals, and unweighted scenario-family summaries are not presented as population estimates.
- Every historical or legal statement has a source-manifest anchor.
- Every formal proposition states its assumptions and receives a compact proof sketch or constructive argument in the main article, with full proofs or executable checks in the repository; contingent simulation implications are not labeled formal propositions.
- Core and sensitivity results remain separate.
- Censoring and unresolved cases are reported by policy and reason; extensive terminal censoring appears in the abstract boundary and results synthesis.
- Robodebt remains structural grounding, not numerical calibration or contemporary-AI equivalence.
- The controlled pair is defined without repository jargon or reliance on the precursor essay.
- The main text contains all five substantive protocol steps, the controlled-pair rule, compact escalation logic, and claim limits; the publication-facing supplement contains detailed inputs, output fields, status/completeness rules, receipt fields, and the worked trace. This completeness is not presented as evidence of usability.
- No project-lead or external-reader return is required; internal examples and author editing are not presented as independent validation, a practitioner study, or evidence of human performance.
- No formal usability, adoption, efficiency, inter-rater reliability, or reproducible-classification claim appears.
- Any semantic post-result change receives a new freeze and affected rerun.
- The final literature-update search recorded in `docs/DEFERRED.md` is completed before submission.
- No overall workflow score, weighted policy winner, historical prevalence estimate, legality inference, or attackability claim appears.

Internal continuity and claim-lineage controls remain in `docs/CONTINUITY_AND_CLAIM_BOUNDARY.md`; they are not reader-facing exhibits.
