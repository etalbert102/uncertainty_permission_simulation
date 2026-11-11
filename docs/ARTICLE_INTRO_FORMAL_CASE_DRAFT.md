# Article Draft: Introduction, Mechanism, Formal Model, and Robodebt Application

Status: first publication-facing draft bounded by the controlled representation fixture, formal specification, fixed Robodebt source packet, frozen simulation receipts, and evidence packet

Working title: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

The section numbers follow `ARTICLE_OUTLINE.md`. Source keys in the traceability notes are drafting controls; final citation form and bibliography remain subject to the manuscript-wide citation audit.

## 1. Introduction

### 1.1 The organizational failure mode

A defensible abstraction can still remove the distinction that would have triggered caution. A classifier may truthfully report a broad category; an agency may consistently transform an annual total into period values; a summary may accurately compress its source. Yet once that representation enters an operating workflow, it can change routing, review, deadlines, and action. The relevant chain is therefore not evidence or model output alone, but evidence, representation, routing, review, action, and eventual correction or restoration.

This paper calls what the operating workflow allows to proceed *functional permission*. Functional permission is distinct from formal authority, legal validity, and action actually taken. It includes every action the workflow makes automatically available in the current state, whether or not an operator selects it and whether or not formal authority has changed. The central question is: when evidence becomes less decision-relevant, what may the workflow now do automatically? The failure of interest occurs when lost information removes a safeguard or adds consequential progression that the remaining evidence cannot independently support.

### 1.2 Why nominal review is insufficient

The presence of a review field does not answer that question. A configured gate may be absent, fail open, or bind the wrong action. A correctly fail-closed gate can preserve safety while cases wait indefinitely. Review is effective only when relevant evidence is visible, an authorized person can stop or modify the exact action, the dependency is enforced, and intervention occurs in time. Timely supported decision service adds a further requirement: a supported disposition must be reached within a declared window. Capacity and timeout rules are thus governance choices, not implementation details. This study retains timely supported service as a formal construct, but excludes its simulation output because the implemented numerator did not verify supported dispositions by the deadline.

### 1.3 Completed research design

The study combines four evidence layers. First, an executable deterministic pair holds a synthetic case, model output, policy, downstream rule, resources, and clock fixed while changing only how uncertainty is represented. Second, a formal model distinguishes evidence refinement, representation, formal authority, automatic permission, review, contestability, and restoration. Third, a fixed source packet maps those constructs onto the early and enhanced Online Compliance Intervention (OCI) processes associated with Australia's Robodebt scheme. Robodebt is analytically useful because aggregate evidence, transformation, notice, access, deadlines, automation, recovery, and reassessment appear in one documented process; it was not a modern generative-AI system. Fourth, a prospectively design-frozen discrete-event simulation combines source-anchored process structure with visibly stylized queue, access, service, correction, and restoration parameters. The simulation tests counterfactual study policies, not historical Robodebt alternatives.

### 1.4 Findings and contributions

The results separate safety from service. Across three prespecified loads, fail-closed review remained gate-safe while timely review completion fell and unresolved holding rose; three points show a capacity response, not a historical or continuous threshold. Holding review machinery and paired cases fixed, fail-open timeouts converted the same non-completion into unsupported progression and recovery exposure. An agency-assisted information-first policy also produced zero unsupported progression, but added interaction and agency-workload events and increased modeled exposure relative to conservative holding. Because the interaction measure counts events rather than evidence-production effort, psychological cost, or welfare, the substantive recipient-burden question remains unresolved.

Two measurement limits narrow those findings. The invalid decision-service output is omitted rather than repaired after inspection. In addition, every conservative-hold, fail-closed-review, and information-first family cell had a terminal right-censoring rate of 1.000, preventing complete-resolution and complete-restoration comparisons for those policies.

The paper contributes a workflow-level permission invariant, an executable representation pair with negative controls, a documented institutional application, a finite-capacity simulation, and a five-step process-red-team protocol. It does not estimate historical Robodebt rates, debts, legality, or causal effects; validate practitioner usability; or establish strategic exploitation. Section 2 isolates the mechanism and locates it in adjacent research. Section 3 states the formal model. Section 4 establishes the case mapping and its limits. Sections 5 and 6 describe the simulation and results, Section 7 turns the analysis into a bounded protocol, and Section 8 states the limitations and transferable conclusion.

## 2. Mechanism, Literature, and Research Questions

### 2.1 Representation-preservation controlled pair

A controlled pair is two deterministic traces of the same synthetic case and the same stored model output. The operational policy, routing rule, process state, reviewer resource, clock, and absence of random draws are held fixed. Only the representation transformation and the representation it mechanically emits differ.

The output describes a low-resolution road object as a pickup-like silhouette with confidence 0.42 and lists live alternatives that include an armed technical. In the preservation arm, typed alternatives, confidence, unresolved status, and provenance remain visible. The material alternative triggers an information action, enhanced scrutiny, and a fail-closed review dependency; routine disposition is unavailable automatically. In the fallback arm, the identical output becomes the broad untyped label `vehicle`. That label is compatible with every listed alternative and is not literally false, but it suppresses the distinction used by the fixed policy. The same downstream rule now routes the case routinely, removes the information and review steps, and automatically permits routine disposition. Here, routine disposition means finalizing the synthetic organizational case without enhanced scrutiny; it does not authorize action against the physical object.

Two controls bound the interpretation. When the output contains no policy-material alternative, changing representation leaves routing unchanged. When the safeguard is representation-independent, both representations retain scrutiny. The pair therefore isolates a representation-to-permission mechanism; it does not test model accuracy, latent truth, frequency, queues, historical conduct, or whether completed review would be effective.

### 2.2 Mechanism and bounded expectation

The mechanism requires three conditions: a representation that is defensible at some level of abstraction; a distinction that matters to an independently specified policy or support rule; and a downstream rule that relaxes a safeguard when that distinction disappears. None is sufficient alone. Coarsening can be harmless when the lost distinction is immaterial, and weaker evidence can properly trigger a hold or a request for more information.

The action direction matters. *Progression* advances or commits the process, imposes an external consequence, or forecloses a required safeguard. *Constraint* pauses or contains progression; *information* obtains evidence without independently releasing unsupported progression; and *restoration* repairs a prior process or consequence. The bounded expectation is that information loss should not add unsupported automatic progression, although it may justify separately evaluated constraints or information seeking.

This is a base workflow vulnerability, not necessarily an attack. Structural susceptibility means a declared mutation can reproduce it. Adversarial exploitability requires separate evidence that the mechanism is inducible, observable, repeatable, and beneficial to an actor. Neither the controlled pair nor the Robodebt application supplies those four findings.

### 2.3 Literature and originality

Three research clusters frame the contribution. Work on information structures, robust choice, calibration, selective classification, abstention, and uncertainty communication establishes that evidence can be ordered, ambiguity can matter to choice, and uncertain outputs can be withheld or communicated (Blackwell 1953; Gilboa and Schmeidler 1989; El-Yaniv and Wiener 2010; Franc and Průša 2019; Prabhudesai et al. 2023). Uncertainty-to-action binding already makes oversight responses to uncertainty explicit (Anyabolu, Dubey, and Hattab 2026). This paper does not claim those ideas as new; it asks whether the surrounding workflow expands automatic progression when decision-relevant information is lost.

Research on effective human oversight, automation bias, administrative burden, automated administration, and contestability shows why nominal human presence is inadequate and why burdens, discretion, and challenge mechanisms must be treated institutionally (Moynihan, Herd, and Harvey 2015; Alon-Barkat and Busuioc 2022; Roehl 2023, 2024; Sterz et al. 2024; Bennett, Currie, and Podoletz 2024; Landau et al. 2024; Vaccaro and Waldo 2024). The present model operationalizes a narrower distinction among gate safety, action-binding review, timely supported service, correction opportunity, and restoration, while leaving reviewer psychology outside its numerical claims.

Finally, queueing, system safety, AI risk governance, and algorithmic impact assessment treat performance as a property of service capacity, control structures, context, ownership, and feedback rather than a component in isolation (Little 1961; Leveson 2011; Reisman et al. 2018; NIST 2023). Here, *process red teaming* means stress-testing how evidence, rules, capacity, deadlines, and defaults interact across a workflow; it does not imply an adversarial attack. We synthesize these established ideas into an information-refinement permission invariant and test its implications in a finite-capacity process. The narrower contribution couples independently supported automatic progression to evidence refinement, adds explicit restoration semantics, and carries the analysis through executable controls and a source-bounded public-administration application. It is a bounded synthesis claim, not an assertion that prior work ignored uncertainty, authority, oversight, or process safety.

### 2.4 Research questions and falsifiability

The study asks: (1) when may weaker evidence safely support automatic progression; (2) when does a configured safeguard remain safe, effective, and timely under access and capacity constraints; and (3) which interventions avoid unsupported progression without hiding delay, burden, workload, exposure, or unresolved cases?

The design can fail its intended contribution. The representation account would lose diagnostic value if a valid enabling pair showed no representation-to-permission change, or if ordinary component-local checks located every induced failure. The dynamic account would narrow to authored semantics if access, capacity, and deadlines produced no consequential variation across the frozen range. The practical account would fail if it could not locate a transition, responsible owner, intervention, tradeoff, and replayable repair beyond what a local accuracy or calculation check already provides. These are contribution-level falsifiers, not population hypotheses.

## 3. Formal Model

### 3.1 Evidence, compatible states, and refinement

An evidence state `e` denotes a set of states compatible with what is known. Evidence `e_more` refines `e_less` when its compatible set is a nonempty subset of the coarser set under independently declared source and measurement assumptions. Refinement is therefore about excluded possibilities, not confidence alone: two estimates with different confidence scores need not be comparable, and a more confident transformation can still discard a policy-relevant distinction.

The admissible refinements of `e_less`, written `Ref(e_less)`, must be specified independently of the action the workflow prefers. A universal pass requires an appropriate certificate. A finite exact certificate enumerates the complete set; a symbolic exact certificate defines it reproducibly; and a conservative outer certificate may prove a pass by testing a sound superset. Witness search can prove failure by finding and validating one admissible counterexample, but failure to find a witness cannot prove universal support. If the support rule, refinement coverage, or action identity is missing, the result is `unassessable`, not a pass inferred from missing evidence.

### 3.2 Representation and evidentiary fidelity

A versioned map transforms evidence into the representation consumed downstream. Claims remain typed as observed, derived, imputed, disputed, or missing and retain their sources, assumptions, transformations, and versions. F0, *evidentiary fidelity*, asks whether claims are supported as typed, lineage is complete, evidence states remain distinguishable, and downstream rules can inspect the required provenance. F4, *material surfacing*, asks whether the meaning of every independently material distinction reaches a role that can intervene before action or expiry.

These tests detect uncertainty laundering without equating abstraction with falsehood. An annual total may be accurate, or the broad label `vehicle` compatible with every live alternative, while the representation loses the type, provenance, dispute, or temporal pattern needed for policy and review. A truthful aggregate can therefore pass a local consistency check yet fail the workflow-level fidelity or surfacing requirement.

### 3.3 Authority, permission, and action

Formal authority `L(q)` is the action set authorized in process state `q`: historical values require an authoritative source, while hypothetical models may declare and label them explicitly. Automatic functional permission `P_auto(e,q,t)` is the complete set that the operating workflow can execute without a new effective review or external authorization. Executed action `X(c,t)` records what actually occurred. The three sets are analytically independent: permission does not imply execution or legality, and consistent implementation does not prove independent evidentiary support.

Actions are fully instantiated by target, parameters, timing, consequence, reversibility, authority condition, and rule version. They are classified relative to a declared baseline as progression, constraint, information, or restoration. An independently owned evaluation specification supplies materiality, admissible refinements, action-support rules, comparison fields, review conditions, contestability thresholds, and restoration obligations. It may not be revised to produce a preferred workflow result. Support and permission are reevaluated after any material change in evidence, representation, time, process state, policy, or rule version.

### 3.4 Robust permission and safe fallbacks

For coarser evidence, define the robust support envelope as the intersection of progression actions independently supported under every admissible refinement:

`P_robust(e_less,q,t) = intersection of J_progress(e_more,q,t) over e_more in Ref(e_less)`.

F1 passes exactly when every automatically permitted progression action under `e_less` belongs to that envelope. A minimal satisfying case holds the case and requests records while automatically permitting no new progression. A minimal failure occurs when an annual total automatically enables a specific imputed disposition, but at least one admissible period-specific refinement fails the independent support rule for that same action. Workflow consistency cannot manufacture support because the evaluation rule is separate from the permission rule.

F2 governs newly added constraint or information actions. A helpful label is insufficient: the action must be compared with an explicit hold from the same initial state, with the same cohort and exogenous inputs. The comparison must include the whole affected unit when an action consumes shared resources or changes another case's queue, deadline, or timeout. The fallback fails if executing it releases unsupported progression for the focal case or a spillover case, or if required authorization or reversibility is absent. Thus uncertainty may expand information seeking or reversible constraint, but only after evaluating what that intervention causes; it cannot be relabeled progression.

### 3.5 Review, service, contestability, and restoration

F3 governs progression withheld from the automatic set pending review. `GateSafe` asks whether a configured dependency prevents action while prerequisites remain unmet. `ReviewEffective` additionally requires timely surfacing, relevant evidence, an authorized reviewer with stopping power, enforced dependency, completion before foreclosure, and a recorded decision. `DecisionServiceEffective` asks whether a supported disposition is reached by a declared deadline. A gate can be safe while the latter two fail.

Review authorization binds the exact action, case, evidence and rule versions, conditions, and expiry. Notice, a reviewer label, a stale decision, post-action reassessment, or authorization of a different action instance does not satisfy F3.

F5 separates six questions often collapsed into “appeal available”: whether a feasible correction path exists; whether it is prospectively reliable under access, capacity, and timing; whether a realized opportunity was available; whether the opportunity was used; whether correction completed; and whether every modeled consequence returned to baseline. Correcting a decision coordinate does not prove restoration of recovery status, money, access, time, or another consequence. Pending horizons are `unassessable`; after the horizon, any required residual prevents complete restoration.

### 3.6 Formal propositions and simulation implication

**Proposition 1—robust permission.** The robust envelope is the unique maximal progression-action set supported under every admissible refinement, and F1 holds if and only if automatic progression under the coarser evidence is its subset. Each member of the intersection is supported everywhere. Any strict superset contains an action excluded by at least one refinement, which supplies a counterexample. The result depends on a sound refinement certificate, fixed comparison state and rules, unambiguous action identity, and an independent support specification.

**Proposition 2—operational review.** A correctly enforced fail-closed gate remains gate-safe regardless of delay, but need not yield effective review or timely supported service. Over a service window `H`, reviewer capacity `c` cannot complete required work `W` plus initial backlog `B0` when `W + B0 > cH`. If prerequisites remain unmet at timeout, fail-closed semantics retain unresolved cases; fail-open semantics can release unsupported progression. The two designs may therefore have identical review completion yet opposite permission consequences. This requires deterministic ordering, a non-bypassable fail-closed gate, declared finite capacity, and explicit deadlines and timeout rules.

The information-first result is not a third theorem. Under the frozen implementation and parameter space, information acquisition exchanged unresolved holding for more interaction events, agency workload, and modeled exposure. That empirical tradeoff depends on the declared process and parameters and cannot be derived from the formal definitions alone. Full notation, proofs, subordinate properties, and counterexamples remain in the repository specification.

## 4. Robodebt as a Documented Process Application

### 4.1 Why this case

Robodebt provides a documented evidence-to-action process in which aggregate income records were matched, transformed into period values, presented through notices and online access, routed by deadlines and response states, used in automated calculation and debt action, and followed by recovery, reassessment, and review. Those features make it useful for examining how representation, access, review, and restoration interact. The application does not equate Robodebt with contemporary machine learning or generative AI. Its analytical role is to establish that the formal objects correspond to consequential institutional transitions in a source-documented administrative workflow.

### 4.2 Sources and application validity

The fixed packet contains ten sources retrieved through 31 October 2026. The principal process source is the Commonwealth Ombudsman's April 2017 report, supplemented by its 2019 implementation report; Deloitte process maps commissioned for the Royal Commission provide node-level routing and calculation structure; and the Royal Commission report owns its historical findings and governance recommendations. Services Australia material supplies only bounded program or current governance context. The 2023 Ombudsman report on income apportionment is used solely to prevent that distinct practice from being conflated with Robodebt income averaging.

Three validity claims remain separate. Documentary validity concerns whether attributed facts are anchored to the proper source and period. Structural mapping validity concerns whether those facts instantiate evidence, transformation, routing, action, review, and correction constructs. Both are supported within the early and enhanced OCI profiles. Numerical calibration validity would require historical distributions for arrivals, capacity, service, engagement, retrieval, correction, and restoration. The packet does not supply them, so the paper deliberately makes no calibration claim.

### 4.3 Early OCI process profile

The early profile covers the July 2016 OCI launch through 19 January 2017, ending before the first specifically dated letter change. Matched Australian Taxation Office pay-as-you-go income and Centrelink information passed through refresh, inclusion, discrepancy, and risk rules before a notice was sent through the selected digital channel or last-known address. The initial letter allowed 21 days from its date to respond, with a reminder after 14 days (Commonwealth Ombudsman 2017, paras. 1.17–1.29; Deloitte maps 2B, 3B, and 4B).

A responding recipient could confirm or correct employer, amount, and pay-period information and supply evidence; specified errors or unresolved inputs could receive compliance-officer handling. The process placed responsibility on recipients to reconstruct and enter historical income information. The Ombudsman noted that decision accuracy depended on their ability to obtain those records despite weaker information-gathering powers and possible bank-statement costs (Commonwealth Ombudsman 2017, paras. 3.26–3.28). If the recipient did not respond by the due date, the documented process evenly apportioned ATO earnings information over the employer-reported employment period, calculated entitlement and any debt, issued a debt notice when the calculation produced one, and commenced normal recovery. Later information could trigger reassessment, and internal review remained available (Commonwealth Ombudsman 2017, paras. 1.17–1.29 and appendix B).

The critical transition is not aggregation alone. An annual employer total is evidence about total income, but even apportionment creates fortnightly values through a transformation rather than revealing actual fortnightly income. When nonresponse allows those values to feed automatic calculation, debt notice, and recovery, representation, deadline, and permission become coupled. This establishes a documented pathway on which the formal diagnostic can operate; it does not independently decide whether a particular debt was legally or monetarily valid, how often the pathway occurred, or why an individual failed to respond.

The documentary record fixes the 21-day clock, 14-day reminder, averaging transition, debt-notice path, recovery, and reassessment opportunity. It does not yield model-ready queue capacity, service-time, notice-engagement, evidence-retrieval, correction-uptake, or restoration-delay distributions. Those quantities remain visibly stylized in the simulation.

### 4.4 Enhanced OCI and repair mechanisms

The enhanced profile is an as-documented early-2017 repair bundle, not a single policy activated on one invented date. The Ombudsman's April report identified changes beginning with the first letter revision on 20 January and further changes during February. The bundle added direct access using a confirmation code and customer reference number, clearer contact information, registered-mail and telephone follow-up, more recent address information where authorized, and 28 days from receipt with a signposted extension route.

It also expanded manual intervention for disputed inputs, complex circumstances, selected other-income answers, and difficulty accessing records; allowed bank statements when payslips were unavailable; made an estimated gross amount visible; and provided more opportunity to revise inputs before accepting a provisional result. An attributed agency statement added a guard against debt-collector referral after nonresponse until the agency was satisfied that the notice had been received and ignored (Commonwealth Ombudsman 2017, paras. 1.30–1.46).

These changes target access, surfacing, evidence acquisition, routing, and recovery gating. They form a bounded repair profile, not proof that every failure disappeared or that configured manual intervention was adequately staffed, timely, or effective. Later EIC, CUPI, PAYG Manual, and remediation processes are outside this profile.

### 4.5 Formal crosswalk and inference limits

In the crosswalk, an annual employer-income total and broad employment period are coarser evidence; supported fortnight-specific income and working dates are admissible finer states. Even apportionment is a representation rule. The documented profile identifies debt-calculation, notice, recovery, hold, and evidence-request action classes and their direction; executable simulation instances become fully specified only after valid source bindings and separately owned stylized overlays are compiled. The response deadline and nonresponse branch map to timeout semantics. The enhanced receipt-and-ignoring condition maps to a gate on collector referral, but its documented configuration does not by itself establish gate safety. Notice and interface records bear on surfacing; an officer route is a possible review path, not proof of effective review. Reassessment is a correction path, while complete restoration would additionally require every modeled consequence—such as recovery status or residual exposure—to return to baseline.

The operational profile never supplies its own support oracle. The study's independent evaluation specification defines period-specific support, materiality, action identity, review conditions, and restoration obligations. Historical formal authority remains source-attributed and may be unassessable; simulation code cannot fill a legal or documentary gap.

Accordingly, the application supports structural relevance, not numerical reconstruction. Unsupported historical parameters cannot become defaults; executable values come from separately versioned stylized overlays. The study makes no independent claim about legality, monetary entitlement or error, historical prevalence, causal effects, recipient behavior, reviewer psychology, or strategic exploitation. It keeps the early and enhanced profiles separate and attributes Royal Commission and Ombudsman findings rather than converting them into simulation outputs.

### 4.6 Transition to simulation

The Robodebt record shows that aggregate evidence, transformation, access, deadlines, automated progression, review paths, recovery, and reassessment can coexist in one consequential workflow. It cannot show how alternative capacity and timeout arrangements would behave across controlled conditions because the needed historical numerical distributions are unavailable. The simulation therefore asks a counterfactual governance question over a declared stylized parameter space. Its five policies are study-owned designs used to compare conservative holding, automatic progression, fail-closed and fail-open review, and agency-assisted information acquisition. They are not labels for historical Robodebt policies.

## Draft Traceability Notes (Not Article Prose)

| Draft component | Evidence owner |
| --- | --- |
| Paper promise, word roles, findings, and claim hierarchy | `docs/ARTICLE_OUTLINE.md`; `docs/EVIDENCE_PACKET.md` |
| Controlled representation pair and controls | `docs/PRECURSOR_FIDELITY_FIXTURE.md`; `docs/P0_USABILITY_WALKTHROUGH.md`; stored P0 records; [Figure 1](figures/figure1_evidence_to_action_protocol.svg) |
| Literature positioning and bounded originality | `docs/LITERATURE_AND_ORIGINALITY_MAP.md`; `docs/LITERATURE_SEARCH_AUDIT.md` |
| Evidence, refinement, representation, actions, F0–F5, and propositions | `docs/FORMAL_MODEL.md`, version `1.0` |
| Early and enhanced OCI profiles | `docs/ROBODEBT_CASE_STUDY.md`; `data/sources/robodebt/r_oci_early.yaml`; `data/sources/robodebt/r_oci_enhanced.yaml`; [Figure 2](figures/figure2_robodebt_process_profiles.svg) |
| Historical source anchors and cutoff | `data/sources/robodebt/source_manifest.yaml`, retrieved through `2026-10-31` |
| Case-application validity and prohibited inferences | `docs/CASE_APPLICATION_SUFFICIENCY.md`; `docs/CONTINUITY_AND_CLAIM_BOUNDARY.md` |
| Simulation previews and measurement exclusions | `docs/ARTICLE_METHODS_RESULTS_DRAFT.md`; core and sensitivity analysis receipts |
