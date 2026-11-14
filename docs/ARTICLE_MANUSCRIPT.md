# From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application

## Abstract

Automated decision workflows can convert incomplete evidence into consequential action even when each component follows its local rule. The central question is: when evidence becomes less decision-relevant, what may an automated workflow now do? This article develops a formal model that separates evidence, representation, formal authority, functional permission, execution, review, contestability, and restoration. The formal model supplies a conditional rule for robust permission; a deterministic representation-preservation pair demonstrates its mechanics; a source-bounded application to Australia’s Robodebt program establishes structural compatibility with the proposed mechanism; and a prospectively frozen finite-cohort simulation estimates behavior only inside a stylized system. Across three prespecified loads, fail-closed review remained gate-safe while timely review completion declined and unresolved holding increased. A matched fail-open policy converted the same review shortfall into unsupported progression and recovery-process exposure. An agency-assisted information-first policy also avoided unsupported progression but increased interaction and agency-workload events relative to conservative holding; because the interaction measure does not capture effort or welfare, its effect on substantive recipient burden remains unresolved. The simulation does not reconstruct historical Robodebt, estimate a continuous capacity threshold, or support complete-restoration comparisons for heavily censored policies. A post-run semantic audit also excluded an invalid timely-service measure. The resulting five-step process-red-team protocol is a proposed diagnostic for tracing how evidence transformations, permission rules, operational review, capacity, and restoration interact, while keeping gate safety, delay, burden, workload, exposure, and unresolved cases separate.

*Keywords:* automated decision-making, human oversight, uncertainty, discrete-event simulation, Robodebt

## 1. Introduction

### 1.1 The organizational failure mode

A defensible abstraction can still remove the distinction that would have triggered caution. A classifier may truthfully report a broad category; an agency may consistently transform an annual total into period values; a summary may accurately compress its source. Yet once that representation enters an operating workflow, it can change routing, review, deadlines, and action. The relevant chain is therefore not evidence or model output alone, but evidence, representation, routing, review, action, and eventual correction or restoration.

This paper calls what the operating workflow allows to proceed *functional permission*. Functional permission is distinct from formal authority, legal validity, and action actually taken. It includes every action the workflow makes automatically available in the current state, whether or not an operator selects it and whether or not formal authority has changed. The central question is: when evidence becomes less decision-relevant, what may the workflow now do automatically? The failure of interest occurs when lost information removes a safeguard or adds consequential progression that the remaining evidence cannot independently support.

### 1.2 Why nominal review is insufficient

The presence of a review field does not answer that question. A configured gate may be absent, fail open, or bind the wrong action. A correctly fail-closed gate can remain gate-safe while cases wait indefinitely. In this study, `ReviewEffective` is an evaluative definition: relevant evidence must be visible, an authorized person must be able to stop or modify the exact action, the dependency must be enforced, and intervention must occur in time. It is not offered as an empirically established universal necessity. Timely supported decision service adds a further requirement: a supported disposition must be reached within a declared window. Capacity and timeout rules that determine consequential defaults in the modeled workflow are therefore governance choices, even though such rules may also be implementation details. This study retains timely supported service as a formal construct, but excludes its simulation output because the implemented numerator did not verify supported dispositions by the deadline.

### 1.3 Completed research design

The study combines four evidence layers with distinct inferential roles. The formal model supplies a conditional rule under declared refinement, support, baseline, and action-identity assumptions. An executable deterministic pair holds a synthetic case, model output, policy, downstream rule, resources, and clock fixed while changing only how uncertainty is represented; it demonstrates the rule’s mechanics. A fixed source packet maps the constructs onto the early and enhanced Online Compliance Intervention (OCI) processes associated with Australia’s Robodebt scheme; that application establishes structural compatibility rather than independent causation. A prospectively design-frozen discrete-event simulation combines source-anchored process structure with visibly stylized queue, access, service, correction, and restoration parameters; it estimates behavior only within that frozen system. The simulation tests counterfactual study policies, not historical Robodebt alternatives.

### 1.4 Findings and contributions

The results separate gate safety from service. Across three prespecified loads, fail-closed review remained gate-safe while timely review completion fell and unresolved holding rose; three points show a capacity response, not a historical or continuous threshold. Holding review machinery and paired cases fixed, fail-open timeouts converted the same non-completion into unsupported progression and recovery exposure. An agency-assisted information-first policy also produced zero unsupported progression, but added interaction and agency-workload events and increased modeled exposure relative to conservative holding. Because the interaction measure counts events rather than evidence-production effort, psychological cost, or welfare, the substantive recipient-burden question remains unresolved.

Two measurement limits narrow those findings. The invalid decision-service output is omitted rather than repaired after inspection. In addition, every conservative-hold, fail-closed-review, and information-first family cell had a terminal right-censoring rate of 1.000, preventing complete-resolution and complete-restoration comparisons for those policies.

The paper develops robust permission as a workflow-level rule, an executable representation pair with negative controls, a documented institutional application, a finite-capacity simulation, and a five-step process-red-team protocol. It does not estimate historical Robodebt rates, debts, legality, or causal effects; validate practitioner usability; or establish strategic exploitation. Section 2 isolates the mechanism and locates it in adjacent research. Section 3 states the formal model. Section 4 establishes the case mapping and its limits. Sections 5 and 6 describe the simulation and results, Section 7 turns the analysis into a bounded protocol, and Section 8 states the limitations and candidate diagnostic.

Figure 1 previews the evidence-to-action chain that serves as the unit of analysis and the five diagnostic steps developed in Section 7.

**Figure 1**

*Evidence-to-Action Chain and Five Process-Red-Team Steps*

![Figure 1. Evidence-to-action chain and five process-red-team steps.](figures/figure1_evidence_to_action_protocol.svg)

*Note.* The protocol follows one action through representation, permission, review, execution, and restoration while keeping formal authority, independent support, automatic permission, and executed action distinct.

## 2. Mechanism, Literature, and Research Questions

### 2.1 Representation-preservation controlled pair

A controlled pair is two deterministic traces of the same synthetic case and the same stored model output. The operational policy, routing rule, process state, reviewer resource, clock, and absence of random draws are held fixed. Only the representation transformation and the representation it mechanically emits differ.

The output describes a low-resolution road object as a pickup-like silhouette with confidence 0.42 and lists live alternatives that include an armed technical. In the preservation arm, typed alternatives, confidence, unresolved status, and provenance remain visible. The material alternative triggers an information action, enhanced scrutiny, and a fail-closed review dependency; routine disposition is unavailable automatically. In the fallback arm, the identical output becomes the broad untyped label `vehicle`. That label is compatible with every listed alternative and is not literally false, but it suppresses the distinction used by the fixed policy. The same downstream rule now routes the case routinely, removes the information and review steps, and automatically permits routine disposition. Here, routine disposition means finalizing the synthetic organizational case without enhanced scrutiny; it does not authorize action against the physical object.

Two controls bound the interpretation. When the output contains no policy-material alternative, changing representation leaves routing unchanged. When the safeguard is representation-independent, both representations retain scrutiny. The pair therefore demonstrates the mechanics of a representation-to-permission mechanism; it does not test model accuracy, latent truth, frequency, queues, historical conduct, or whether completed review would be effective.

### 2.2 Mechanism and bounded expectation

The mechanism requires three conditions: a representation that is defensible at some level of abstraction; a distinction that matters to an independently specified policy or support rule; and a downstream rule that relaxes a safeguard when that distinction disappears. None is sufficient alone. Coarsening can be harmless when the lost distinction is immaterial, and weaker evidence can properly trigger a hold or a request for more information.

The action direction matters. *Progression* advances or commits the process, imposes an external consequence, or forecloses a required safeguard. *Constraint* pauses or contains progression; *information* obtains evidence without independently releasing unsupported progression; and *restoration* repairs a prior process or consequence. The bounded expectation is that information loss should not add unsupported automatic progression, although it may justify separately evaluated constraints or information seeking. This is a permission-preserving expectation, not a consequence-complete safety claim: delay, deprivation, abandonment, queue displacement, and spillovers are not measured here as terminal consequences.

This is a base workflow vulnerability, not necessarily an attack. Structural susceptibility means a declared mutation can reproduce it. Adversarial exploitability requires separate evidence that the mechanism is inducible, observable, repeatable, and beneficial to an actor. Neither the controlled pair nor the Robodebt application supplies those four findings.

### 2.3 Literature and proposed integration

Three research traditions frame the unresolved workflow question. Work on information structures, robust choice, selective classification, abstention, and uncertainty communication establishes that evidence can be ordered, ambiguity can matter to choice, and uncertain outputs can be withheld or communicated (Blackwell, 1953; El-Yaniv & Wiener, 2010; Franc & Průša, 2019; Gilboa & Schmeidler, 1989; Prabhudesai et al., 2023). Uncertainty-to-action binding already makes oversight responses to uncertainty explicit (Anyabolu et al., 2026). Recent agent and fraud-operation preprints further distinguish correct endpoints from actions supported by established, authorized, or sufficiently fresh evidence (Deng, 2026; Liao et al., 2026; Lin et al., 2026). The article’s different question is whether the surrounding workflow expands automatic progression when decision-relevant information is lost.

Research on effective human oversight, automation bias, administrative burden, automated administration, and contestability examines the conditions and risks under which nominal human presence may be insufficient and why burdens, discretion, and challenge mechanisms must be treated institutionally (Alon-Barkat & Busuioc, 2023; Bennett et al., 2026; Landau et al., 2024; Moynihan et al., 2015; Roehl, 2023; Roehl & Hansen, 2024; Sterz et al., 2024; Sztandar-Sztanderska, 2026). Hardy’s (2026) Oversight-to-Control framework is a particularly close institutional comparison because it separates observation, interpretation, challenge, intervention, and recovery. This article instead adds an evidence-refinement permission invariant and an executed dynamic counterfactual while leaving reviewer psychology outside its numerical claims.

Finally, queueing, system safety, AI risk governance, and algorithmic impact assessment treat performance as a property of service capacity, control structures, context, ownership, and feedback rather than a component in isolation (Leveson, 2012; Little, 1961; National Institute of Standards and Technology, 2023; Reisman et al., 2018). Recent queue-control preprints explicitly coordinate automation or escalation with congestible human service (Montanari et al., 2026; Wang & Rachev, 2026). This article does not propose an optimal controller; it stress-tests fixed safeguard and timeout rules across declared capacity conditions. Here, *process red teaming* means stress-testing how evidence, rules, capacity, deadlines, and defaults interact across a workflow; it does not imply an adversarial attack. The article synthesizes established ideas into robust permission and tests that construct in a finite-capacity process. Its proposed integration couples evidentiary refinement, independently supported automatic progression, restoration semantics, executable controls, and a source-bounded public-administration application. This is a bounded synthesis claim, not a claim of verified novelty or an assertion that prior frameworks lack those ingredients.

### 2.4 Research questions and falsifiability

The study asks: (1) when may weaker evidence support automatic progression under the proposed robust-permission rule; (2) when does a configured safeguard remain gate-safe, effective, and timely under access and capacity constraints; and (3) which interventions avoid unsupported progression without hiding delay, burden, workload, exposure, or unresolved cases?

The design can fail its intended contribution. The representation account would lose diagnostic value if a valid enabling pair showed no representation-to-permission change, or if ordinary component-local checks located every induced failure. The dynamic account would narrow to authored semantics if access, capacity, and deadlines produced no consequential variation across the frozen range. The practical account would fail if it could not locate a transition, responsible owner, intervention, tradeoff, and replayable repair beyond what a local accuracy or calculation check already provides. These are contribution-level falsifiers, not population hypotheses.

## 3. Formal Model

### 3.1 Evidence, compatible states, and refinement

An evidence state `e` denotes a set of states compatible with what is known. Evidence `e_more` refines `e_less` when its compatible set is a nonempty subset of the coarser set under independently declared source and measurement assumptions. Refinement is therefore about excluded possibilities, not confidence alone: two estimates with different confidence scores need not be comparable, and a more confident transformation can still discard a policy-relevant distinction.

The admissible refinements of `e_less`, written `Ref(e_less)`, must be specified independently of the action the workflow prefers. A universal pass requires an appropriate certificate. A finite exact certificate enumerates the complete set; a symbolic exact certificate defines it reproducibly; and a conservative outer certificate may prove a pass by testing a sound superset. Witness search can prove failure by finding and validating one admissible counterexample, but failure to find a witness cannot prove universal support. If the support rule, refinement coverage, or action identity is missing, the result is `unassessable`, not a pass inferred from missing evidence.

### 3.2 Representation and evidentiary fidelity

A versioned map transforms evidence into the representation consumed downstream. Claims remain typed as observed, derived, imputed, disputed, or missing and retain their sources, assumptions, transformations, and versions. F0, *evidentiary fidelity*, asks whether claims are supported as typed, lineage is complete, evidence states remain distinguishable, and downstream rules can inspect the required provenance. F4, *material surfacing*, asks whether the meaning of every independently material distinction reaches a role that can intervene before action or expiry.

These proposed diagnostics are intended to identify uncertainty laundering without equating abstraction with falsehood. An annual total may be accurate, or the broad label `vehicle` compatible with every live alternative, while the representation loses the type, provenance, dispute, or temporal pattern needed for policy and review. A truthful aggregate can therefore pass a local consistency check yet fail the workflow-level fidelity or surfacing requirement.

### 3.3 Authority, permission, and action

Formal authority `L(q)` is the action set authorized in process state `q`: historical values require an authoritative source, while hypothetical models may declare and label them explicitly. Automatic functional permission `P_auto(e,q,t)` is the complete set that the operating workflow can execute without a new effective review or external authorization. Executed action `X(c,t)` records what actually occurred. The three sets are analytically independent: permission does not imply execution or legality, and consistent implementation does not prove independent evidentiary support.

Actions are fully instantiated by target, parameters, timing, consequence, reversibility, authority condition, and rule version. They are classified relative to a declared baseline as progression, constraint, information, or restoration. An independently owned evaluation specification supplies materiality, admissible refinements, action-support rules, comparison fields, review conditions, contestability thresholds, and restoration obligations. It may not be revised to produce a preferred workflow result. Support and permission are reevaluated after any material change in evidence, representation, time, process state, policy, or rule version. Treating the complete workflow rather than a component as the unit of governance is a proposed principle, not a universal empirical finding.

### 3.4 Robust permission and safe fallbacks

For coarser evidence, define robust permission as the intersection of progression actions independently supported under every admissible refinement:

`P_robust(e_less,q,t) = intersection of J_progress(e_more,q,t) over e_more in Ref(e_less)`.

F1 is the test of this same rule: it passes exactly when every automatically permitted progression action under `e_less` belongs to `P_robust`. A minimal satisfying case holds the case and requests records while automatically permitting no new progression. A minimal failure occurs when an annual total automatically enables a specific imputed disposition, but at least one admissible period-specific refinement fails the independent support rule for that same action. Workflow consistency cannot manufacture support because the evaluation rule is separate from the permission rule.

F2 governs newly added constraint or information actions. A helpful label is insufficient: the action must be compared with an explicit hold from the same initial state, with the same cohort and exogenous inputs. The comparison must include the whole affected unit when an action consumes shared resources or changes another case’s queue, deadline, or timeout. The fallback fails if executing it releases unsupported progression for the focal case or a spillover case, or if required authorization or reversibility is absent. Thus uncertainty may expand information seeking or reversible constraint, but only after evaluating what that intervention causes; it cannot be relabeled progression.

### 3.5 Review, service, contestability, and restoration

F3 governs progression withheld from the automatic set pending review. `GateSafe` asks whether a configured dependency prevents action while prerequisites remain unmet. In this study’s evaluative definition, `ReviewEffective` additionally requires timely surfacing, relevant evidence, an authorized reviewer with stopping power, enforced dependency, completion before foreclosure, and a recorded decision. `DecisionServiceEffective` asks whether a supported disposition is reached by a declared deadline. A gate can be gate-safe while the latter two fail.

Review authorization binds the exact action, case, evidence and rule versions, conditions, and expiry. Notice, a reviewer label, a stale decision, post-action reassessment, or authorization of a different action instance does not satisfy F3.

F5 separates six questions often collapsed into “appeal available”: whether a feasible correction path exists; whether it is prospectively reliable under access, capacity, and timing; whether a realized opportunity was available; whether the opportunity was used; whether correction completed; and whether every modeled consequence returned to baseline. Correcting a decision coordinate does not prove restoration of recovery status, money, access, time, or another consequence. Pending horizons are `unassessable`; after the horizon, any required residual prevents complete restoration.

### 3.6 Formal propositions and simulation implication

**Proposition 1—robust permission.** `P_robust` is the unique maximal progression-action set supported under every admissible refinement, and F1 holds if and only if automatic progression under the coarser evidence is its subset. Each member of the intersection is supported everywhere. Any strict superset contains an action excluded by at least one refinement, which supplies a counterexample. The result depends on a sound refinement certificate, fixed comparison state and rules, unambiguous action identity, and an independent support specification.

**Proposition 2—operational review.** A correctly enforced fail-closed gate remains gate-safe regardless of delay, but need not yield effective review or timely supported service. Over a service window `H`, an aggregate reviewer service rate `μ` cannot complete required work `W` plus initial backlog `B0` when `W + B0 > μH`. If prerequisites remain unmet at timeout, fail-closed semantics retain unresolved cases; fail-open semantics can release unsupported progression. The two designs may therefore have identical review completion yet opposite permission consequences. This requires deterministic ordering, a non-bypassable fail-closed gate, declared finite capacity, and explicit deadlines and timeout rules.

The information-first result is not a third theorem. Under the frozen implementation and parameter space, information acquisition produced more interaction events, agency workload, and modeled exposure; it also coincided descriptively with fewer action-stage holds, but the frozen receipt did not contain a paired unresolved-holding estimand. Those empirical patterns depend on the declared process and parameters and cannot be derived from the formal definitions alone. Full notation, proofs, subordinate properties, and counterexamples remain in the repository specification.

## 4. Robodebt as a Documented Process Application

### 4.1 Why this case

The supplied record documents an OCI evidence-to-action process in which aggregate income records were matched, transformed into period values, presented through notices and online access, routed by deadlines and response states, used in automated calculation and debt action, and followed by recovery, reassessment, and review. Those process facts make the case structurally compatible with the proposed mechanism and useful for examining how representation, access, review, and restoration interact. The analytical mapping is the study’s: the documents do not establish that representation loss independently caused the institutional outcome. Policy intent, legal interpretation, incentives, and the allocation of evidentiary risk remain alternative explanations. The application does not equate Robodebt with contemporary machine learning or generative AI.

### 4.2 Sources and application validity

The fixed packet contains ten sources retrieved through 31 October 2026. The principal process sources are the Commonwealth Ombudsman’s reports (Commonwealth Ombudsman, 2017, 2019); Deloitte’s process maps provide node-level routing and calculation structure (Deloitte for the Royal Commission into the Robodebt Scheme, 2023a, 2023b, 2023c); and the Royal Commission’s report owns its historical findings and governance recommendations (Royal Commission into the Robodebt Scheme, 2023). Services Australia (2025) supplies only bounded program or current governance context. The Commonwealth Ombudsman’s (2023) report on income apportionment is used solely to prevent that distinct practice from being conflated with Robodebt income averaging.

Three validity claims remain separate. Documentary validity concerns whether attributed facts are anchored to the proper source and period. Structural mapping validity concerns the study’s analytical judgment that those facts instantiate evidence, transformation, routing, action, review, and correction constructs. Both are supported within the bounded early and enhanced OCI profiles, but neither establishes that the proposed mechanism independently caused the program’s outcomes. Numerical calibration validity would require historical distributions for arrivals, capacity, service, engagement, retrieval, correction, and restoration. The packet does not supply them, so the paper deliberately makes no calibration claim.

### 4.3 Early OCI process profile

The early profile covers the July 2016 OCI launch through 19 January 2017, ending before the first specifically dated letter change. Under the documented OCI design, matched Australian Taxation Office pay-as-you-go income and Centrelink information passed through refresh, inclusion, discrepancy, and risk rules before a notice was sent through the selected digital channel or last-known address. The initial letter allowed 21 days from its date to respond, with a reminder after 14 days (Commonwealth Ombudsman, 2017, paras. 1.17–1.29; Deloitte for the Royal Commission into the Robodebt Scheme, 2023a, 2023b, 2023c).

A responding recipient could confirm or correct employer, amount, and pay-period information and supply evidence; specified errors or unresolved inputs could receive compliance-officer handling. The documented process placed responsibility on recipients to reconstruct and enter historical income information. The Ombudsman noted that decision accuracy depended on their ability to obtain those records despite weaker information-gathering powers and possible bank-statement costs (Commonwealth Ombudsman, 2017, paras. 3.26–3.28). If the recipient did not respond by the due date, the documented OCI design evenly apportioned ATO earnings information over the employer-reported employment period, calculated entitlement and any debt, issued a debt notice when the calculation produced one, and commenced normal recovery. Later information could trigger reassessment, and internal review remained available (Commonwealth Ombudsman, 2017, paras. 1.17–1.29, Appendix B).

The critical analytical transition is not aggregation alone. An annual employer total is evidence about total income, but even apportionment creates fortnightly values through a transformation rather than revealing actual fortnightly income. In the documented OCI pathway, nonresponse allowed those values to feed automatic calculation, debt notice, and recovery; the study maps that sequence as a coupling of representation, deadline, and permission. This establishes a documented pathway compatible with the proposed mechanism. It does not show that representation loss independently caused the institutional outcome, decide whether a particular debt was legally or monetarily valid, establish how often the pathway occurred, or determine why an individual failed to respond.

The documentary record fixes the 21-day clock, 14-day reminder, averaging transition, debt-notice path, recovery, and reassessment opportunity. It does not yield model-ready queue capacity, service-time, notice-engagement, evidence-retrieval, correction-uptake, or restoration-delay distributions. Those quantities remain visibly stylized in the simulation.

### 4.4 Enhanced OCI and repair mechanisms

The enhanced profile is an as-documented early-2017 repair bundle, not a single policy activated on one invented date. The Commonwealth Ombudsman’s (2017) April report identified changes beginning with the first letter revision on 20 January and further changes during February. The bundle added direct access using a confirmation code and customer reference number, clearer contact information, registered-mail and telephone follow-up, more recent address information where authorized, and 28 days from receipt with a signposted extension route.

The documented OCI design also expanded manual intervention for disputed inputs, complex circumstances, selected other-income answers, and difficulty accessing records; added online bank-statement entry with net-to-gross calculation and clearer handling when payslips were unavailable; made an estimated gross amount visible; and provided more opportunity to revise inputs before accepting a provisional result. The Ombudsman reported that bank statements had already been accepted as reasonable historical-income evidence when other evidence was unavailable. An attributed agency statement added a guard against debt-collector referral after nonresponse until the agency was satisfied that the notice had been received and ignored (Commonwealth Ombudsman, 2017, paras. 1.30–1.46).

These changes target access, surfacing, evidence acquisition, routing, and recovery gating. They form a bounded repair profile, not proof that every failure disappeared or that configured manual intervention was adequately staffed, timely, or effective. Later EIC, CUPI, PAYG Manual, and remediation processes are outside this profile.

Figure 2 contrasts the documented early OCI pathway with the enhanced repair bundle and identifies the separate, study-owned simulation layer.

**Figure 2**

*Early and Enhanced OCI Process Profiles*

![Figure 2. Early and enhanced OCI process profiles.](figures/figure2_robodebt_process_profiles.svg)

*Note.* Source-grounded process structure establishes analytical relevance; the simulation layer remains study-owned and stylized rather than a numerical reconstruction of Robodebt. The historical process structure is synthesized from Commonwealth Ombudsman (2017, paras. 1.17–1.46, Appendix B) and Deloitte for the Royal Commission into the Robodebt Scheme (2023a, 2023b, 2023c).

### 4.5 Formal crosswalk and inference limits

The documents support the process facts; the following crosswalk is the study’s analytical mapping. An annual employer-income total and broad employment period are treated as coarser evidence, while supported fortnight-specific income and working dates are treated as admissible finer states. Even apportionment is mapped as a representation rule. The documented profile identifies debt-calculation, notice, recovery, hold, and evidence-request action classes and their direction; executable simulation instances become fully specified only after valid source bindings and separately owned stylized overlays are compiled. The response deadline and nonresponse branch map to timeout semantics. The enhanced receipt-and-ignoring condition maps to a gate on collector referral, but its documented configuration does not by itself establish gate safety. Notice and interface records bear on surfacing; an officer route is a possible review path, not proof of effective review. Reassessment is a correction path, while complete restoration would additionally require every modeled consequence—such as recovery status or residual exposure—to return to baseline.

The operational profile never supplies its own support oracle. The study’s independent evaluation specification defines period-specific support, materiality, action identity, review conditions, and restoration obligations. Historical formal authority remains source-attributed and may be unassessable; simulation code cannot fill a legal or documentary gap. Where the record does not support attribution to a particular official, agency unit, or software component, the article attributes the transition only to the OCI design or leaves its owner unassessable.

Accordingly, the application supports structural relevance, not numerical reconstruction or an independent causal conclusion. Unsupported historical parameters cannot become defaults; executable values come from separately versioned stylized overlays. The study makes no independent claim about legality, monetary entitlement or error, historical prevalence, causal effects, recipient behavior, reviewer psychology, policy intent, incentives, or strategic exploitation. It keeps the early and enhanced profiles separate and attributes Royal Commission and Ombudsman findings rather than converting them into simulation outputs.

### 4.6 Transition to simulation

Because the required historical numerical distributions are unavailable, the simulation asks a counterfactual governance question over a declared stylized parameter space. Its five policies are study-owned designs used to compare conservative holding, automatic progression, fail-closed and fail-open review, and agency-assisted information acquisition. They are not labels for historical Robodebt policies.

## 5. Dynamic Simulation Methods

### 5.1 Purpose, kernel, and unit of analysis

The simulation has a limited purpose: to test declared gates and timeout defaults under finite capacity within a frozen stylized system. We implemented a finite-cohort discrete-event simulation of an administrative evidence-to-action process. The process unit was a case; one run was an 80-case family-policy-replication cohort; policies were paired within family and replication; and the scenario family was the cross-scenario summary unit. Cases moved through engagement, evidence representation, routing, possible review, action, exposure, correction, and restoration. Shared staffed stages used finite-capacity, work-conserving FIFO queues with deterministic server ties. Open paths at the day-650 cutoff were right-censored by stage rather than classified as resolved.

The kernel was case-neutral: no Robodebt identifier or case-specific rule entered its event logic. Robodebt established structural relevance; unmeasured quantities remained stylized rather than becoming historical calibration. Policies, evaluation rules, execution counts, and scenario mappings retained separate frozen owners.

Matched policies shared case membership, latent attributes, potential evidence, access attributes, and exogenous draws. Draws were keyed by case, event family, and index, so policy-induced events could not shift unrelated draws. This common-random-number design reduced computational noise without suppressing policy-induced path differences.

### 5.2 Policy designs

Table 1 compares five counterfactual policy designs. They are study-owned interventions, not labels for historical Robodebt policies.

**Table 1**

*Counterfactual Study Policies and Principal Modeled Tradeoffs*

| Policy | Operational rule | Principal modeled tradeoff |
| --- | --- | --- |
| Claimant-led evidence and hold (U0) | Hold while required evidence is missing. | Avoids unsupported progression but may retain unresolved cases and interactions. |
| Impute and progress (U1) | Impute and permit automatic progression. | Failure benchmark for progression without action-specific support. |
| Review with fail-closed timeout (U2C) | Impute with evidence status preserved, route all potential progression to review, and hold if review does not complete in time. | Preserves the gate but can accumulate holds. |
| Review with fail-open timeout (U2O) | Impute with evidence status preserved, route all potential progression to review, and permit progression if review times out. | Converts non-completion into potentially unsupported action. |
| Agency-assisted information first (U3) | Assist engagement and retrieve evidence; progress when support is obtained and route unresolved cases to fail-closed review and holding. | Consumes resources and may add interactions, delay, or exposure. |

U2O−U2C isolated the consequence of review non-completion under otherwise shared review machinery. U3−U0 compared assisted evidence acquisition with conservative holding. U1−U0 was an implementation-validation contrast, not a substantive policy comparison.

### 5.3 Frozen scenario design and execution

Before inspecting core results, we froze policies, scenarios, seeds, outcomes, contrasts, and the precision and analysis rules. This prospective record constrained result-driven tuning and supports reproduction; it was not external preregistration or population-level inference.

The core crossed five stylized relationships, none a historical Robodebt estimate. For initiation and review demand, nominal initiation load `L` took values 0.60, 0.95, and 1.20. With `N = 80` cases, `k = 2` review servers, and review-service times `U[0,s)` with mean `s/2`, the initiation window was `Ns/(2kL)`; realized review demand still depended on routing. Missing-evidence probability `m` took values 0.10, 0.30, and 0.50, giving record availability `1 − m`. Access-barrier probability `b` took the same three values, giving access `1 − b`, notice `1 − b/4`, and comprehension `1 − b/2`. Retrieval success was 0.35 in the low condition and 0.85 in the high condition. Partial staff access increased the uniform review-service scale from 10 to 15 days; complete access retained the 10-day scale.

For engagement and assistance, keyed `U[0,1)` variates generated binary events by threshold and stochastic timings by declared scales. The process used a 1-day notice delay, 21-day response deadline, 0.55 response-effort limit, two assistance servers, a 5-day service scale, a 21-day assistance window, 0.25 extension-need probability, and a 7-day extension scale. Retrieval latency was `U[0,10)` days in the core.

For review and downstream handling, review used `k = 2` servers, service time `U[0,s)` with `s = 10` or 15 days by staff access, a 14-day window, and a 1-day exposure delay. Recovery used two servers, a fixed 8-day service demand, and a 20-day window. Correction uptake had probability 0.50 after a 7-day delay; reassessment used two servers, a fixed 10-day service demand, and a 14-day window; restoration used a 5-day delay, a 50-day window, and an administrative cutoff at day 650. Recovery and reassessment therefore used fixed service demands, whereas review and the other declared stochastic timings used keyed variates.

The 108-family design used five policies and 30 paired replications: 16,200 core runs and 1,296,000 case-policy trajectories. Load was a designed input, not measured utilization or an estimated threshold. The frozen manifest fixed 3,240 family-replication seeds per suite under SHA-256 identity `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c`.

MCSE targets were 0.05 for rates and 0.06 for paired differences. A miss after 30 replications would have extended every core cell to 60; none did. A separate 16,200-run sensitivity doubled retrieval-latency scale from 10 to 20 days without pooling with the core.

### 5.4 Outcomes and estimands

Unsupported progression was executed progression lacking action-specific support under the frozen evaluation rule. Its rate, unresolved holding, exposure, and right-censoring used initiated cases as denominator. Gate safety used applicable configured gates and tested whether they blocked progression while prerequisites remained unmet. These definitions govern findings only inside the modeled workflow.

Administrative closure did not manufacture a terminal disposition. Conservative holds and supported downstream-exposure paths had no modeled terminal-resolution event, so they remained right-censored even when no queue extended to day 650. Complete restoration was observed or ruled out only on modeled correction-and-restoration paths following unsupported progression. Censoring therefore identifies an open or unmodeled terminal path, not necessarily excessive elapsed time or evidentiary failure.

The frozen `review_effective_rate` divided timely pre-action completions by queued requests. Policies supplied surfacing, stopping authority, gate dependency, action binding, and recording; the rate did not vary or score those conditions. Partial staff access lengthened service rather than creating a separate visibility failure. We therefore call it **timely review completion**: the timing component, not validation of the full formal `ReviewEffective` construct. These operational measures are not legal judgments.

The interaction-event rate counted responses plus assistance requests per case. Its immutable legacy field name, `recipient_burden_rate`, does not measure effort, subjective burden, welfare, or cost. Agency workload counted completed assistance, retrieval requests, completed reviews, and completed reassessments per case. Exposure marked entry into a downstream consequence path; it could follow supported or unsupported progression and was not itself error or harm.

We report family-specific paired differences, 95% normal MCSE intervals, family ranges, and unweighted designed-family means. MCSE measures finite-run precision, not population, historical, or model uncertainty; cross-family means assume no real-world scenario distribution.

Expectations 1–3 correspond to internal freeze labels H1–H3, not empirical-population hypotheses.

The service construct required a supported disposition by deadline, but its numerator counted every no-review case without checking disposition. We excluded all numerical service results and chose no substitute; repair requires a new version, freeze, and affected rerun.

### 5.5 Validation, controls, and claim boundary

Validation covered hand traces, queues and timeouts, replay, configuration closure, adapter substitution, conservation, five negative controls, and append-only receipts. All 32,400 expected runs reconciled, representing 2,592,000 trajectories; 178 automated checks and all controls passed. Maximum MCSE was 0.04332 core and 0.04051 sensitivity.

Execution integrity does not rehabilitate the invalid service construct. Estimates apply only to the declared model and parameter space, not historical prevalence, legality, monetary error, or omitted mechanisms. Institutional significance would require sensitivity analyses or observed traces addressing adaptive staffing, priority rules, endogenous demand, discretion, learning, and strategic behavior; predictable behavior of this frozen FIFO kernel does not establish that those mechanisms dominate in actual institutions.

## 6. Results

### 6.1 Execution integrity, precision, and measurement audit

All 16,200 core and 16,200 sensitivity runs reconciled with no missing or unexpected identifiers.

We exclude the invalid service measure from results, figures, and conclusions without a post hoc substitute. This is a construct-validity failure in the demonstration, not an execution failure or population finding.

Every U0, U2C, and U3 family cell had terminal right-censoring of 1.000; unweighted designed-family mean censoring rates were 0.219 for U1 and 0.524 for U2O. These values include structurally open terminal paths, not only work that exceeded day 650. The simulation therefore does not identify terminal disposition or permit complete-restoration comparisons for the fully censored policies, although earlier stage-specific outcomes remain interpretable within their horizons.

### 6.2 Expectation 1: fail-closed gate safety across tested load regimes

Definition-driven by the configured fail-closed rule, U2C’s unweighted mean gate safety remained 1.000 at nominal loads 0.60, 0.95, and 1.20. Across the other factors, timely review completion fell from 0.857 to 0.502 to 0.212, while unresolved holding rose from 0.143 to 0.498 to 0.788.

Fail-closed review thus kept automatic progression within the robust-permission set by retaining cases that review did not resolve in time. Gate safety is not timely service, and holding is not harmless: it defers action while leaving recipients and administrators in an open process.

The pattern matches expectation 1 within the design, but three loads do not locate a continuous threshold. The excluded service measure leaves timely-supported service unevaluated, and the simulation does not compare delay, deprivation, abandonment, queue displacement, or spillovers as terminal consequences.

### 6.3 Expectation 2: fail-open timeouts convert review shortfall into progression

The paired U2O−U2C contrast held cases, draws, and review machinery fixed while changing the consequence of non-completion. Unsupported progression increased by an unweighted mean +0.476 across families (range +0.042 to +0.881); all 108 family MCSE intervals lay above zero.

Exposure increased identically; gate safety and unresolved holding moved by the same magnitude in the opposite direction. Timely-review-completion differences were zero in every family. U2C averaged 0.476 unresolved holding and zero unsupported progression; U2O averaged the reverse.

Direction follows the declared timeout rules; the simulation supplies magnitude, scenario variation, and queue consequences. Exposure is downstream of progression, not independent confirmation. Fail closed keeps automatic progression within the robust-permission set but retains cases; fail open replaces those holds with potentially unsupported action and exposure.

### 6.4 Expectation 3: the information-first tradeoff

Expectation 3 was unavailable as framed: U3−U0 was unconditional, the interaction proxy counted events rather than effort or welfare, and service measurement failed audit.

Both policies produced zero unsupported progression in all 108 families. The prospective plan named unresolved cases, but the receipt omitted that paired U3−U0 metric. Descriptively, unweighted designed-family mean unresolved-hold rates were 0.009 under U3 and 0.766 under U0: fewer action-stage holds, not a paired estimate or proven terminal resolution. U3 gate-safety and review values were outside its frozen applicable set and remain uninterpreted.

The paired U3−U0 contrast increased interaction events by mean +1.096 per case (range +0.860 to +1.312) and workload events by +1.209 (+0.749 to +1.728); every family interval lay above zero. The proxy moved opposite the expected direction. Because U0 generates none of the counted workload events, that direction is definition-driven; magnitude and variation are simulated.

The paired exposure rate increased by an unweighted family mean +0.594 (range +0.369 to +0.815), with every interval above zero. Because both policies had zero unsupported progression, this reflects downstream movement that can follow supported action. Descriptively, U3 combined fewer action-stage holds with more interactions, work, and exposure while terminal paths remained open; substantive burden therefore remains unresolved rather than rejected.

### 6.5 Censoring, validation contrast, and sensitivity

Descriptively, unweighted designed-family mean shares of initiated cases remaining before exposure or on an open exposure/recovery path were 76.6%/23.4% under U0, 88.5%/11.5% under U2C, and 17.1%/82.9% under U3. U1 censored 21.9% of initiated cases, all on the latter path; U2O censored 52.4%, split 40.9%/11.5%. These cutoff-stage classifications include structurally open paths and imply neither resolution nor complete restoration; exact codes remain in the repository analysis artifacts.

The paired U1−U0 validation contrast increased unsupported progression by mean +0.781 (range +0.578 to +0.914), with every interval above zero. It confirms benchmark activation, not a substantive discovery or recommendation.

With retrieval latency doubled, U3 and U0 again had zero unsupported progression. Paired unweighted designed-family mean U3−U0 sensitivity differences were +1.098 interaction events per initiated case (+0.855 to +1.325), +1.209 workload events per initiated case (+0.748 to +1.724), and +0.595 in exposure rate (+0.370 to +0.824); every family interval remained positive. This is stability to one perturbation, not general robustness.

### 6.6 Synthesis

The strongest within-model result is that identical timely-review-completion rates can coexist with opposite permission consequences. Timely supported service was invalidly measured, substantive burden received only an interaction-event proxy, and censoring blocked complete-restoration comparisons.

Figure 3 visualizes the load response and the two principal paired-policy tradeoffs.

**Figure 3**

*Capacity, Timeout, and Information-First Tradeoffs*

![Figure 3. Capacity, timeout, and information-first tradeoffs.](figures/figure3_simulation_results.svg)

*Note.* The figure reports the frozen core simulation of 108 designed families with 30 paired replications per family. Panel A shows the fail-closed load response. Panels B and C show unweighted means and family ranges for the paired policy contrasts. Family ranges describe variation across designed scenarios, not uncertainty; Panel C labels its different outcome units explicitly.

Table 2 reports the prespecified paired estimates, computational-precision summaries, and claim boundaries underlying those contrasts.

**Table 2**

*Prespecified Paired Estimates, Computational Precision, and Claim Boundaries*

| Contrast | Outcome | Mean difference | Family range | MCSE range; intervals excluding zero | Claim note |
| --- | --- | ---: | ---: | ---: | :---: |
| U2O − U2C | Unsupported-progression rate | +0.476 | +0.042 to +0.881 | 0.009–0.043; 108/108 above | <sup>a</sup> |
| U2O − U2C | Gate-safety rate | −0.476 | −0.881 to −0.042 | 0.009–0.043; 108/108 below | <sup>a</sup> |
| U2O − U2C | Timely-review-completion rate | 0.000 | 0.000 to 0.000 | 0.000; 0/108 | <sup>a</sup> |
| U2O − U2C | Unresolved-hold rate | −0.476 | −0.881 to −0.042 | 0.009–0.043; 108/108 below | <sup>a</sup> |
| U2O − U2C | External/recovery-process-exposure rate | +0.476 | +0.042 to +0.881 | 0.009–0.043; 108/108 above | <sup>b</sup> |
| U3 − U0 | Unsupported-progression rate | 0.000 | 0.000 to 0.000 | 0.000; 0/108 | <sup>c</sup> |
| U3 − U0 | Recipient interaction events per case | +1.096 | +0.860 to +1.312 | 0.012–0.024; 108/108 above | <sup>c</sup> |
| U3 − U0 | Agency-workload events per case | +1.209 | +0.749 to +1.728 | 0.011–0.027; 108/108 above | <sup>c</sup> |
| U3 − U0 | External/recovery-process-exposure rate | +0.594 | +0.369 to +0.815 | 0.006–0.013; 108/108 above | <sup>b, c</sup> |
| U1 − U0 | Unsupported-progression rate | +0.781 | +0.578 to +0.914 | 0.004–0.011; 108/108 above | <sup>d</sup> |

*Note.* MCSE = Monte Carlo standard error. Differences are left policy minus right policy. Means and ranges are unweighted summaries over 108 deliberately designed scenario families. Each family estimate uses 30 paired replications. A family-specific computational-precision interval is the paired estimate ± 1.96 × MCSE; these intervals do not represent population, historical, or model uncertainty. The semantically invalid timely-supported-decision-service output is excluded. U3−U0 unresolved holding is not included because the frozen receipt did not generate that paired estimand.

<sup>a</sup> Timeout directions follow the declared fail-open/fail-closed semantics; the simulation supplies magnitude and family variation. The policies used the same review queue, and fewer holds represent progression rather than established resolution. A fail-open release with unmet prerequisites is not gate-safe.

<sup>b</sup> Exposure is structurally downstream, may follow supported progression, and is neither independent confirmation nor proof of harm.

<sup>c</sup> Both policies prevented unsupported progression; interaction events do not measure effort, subjective burden, welfare, or cost, while the workload direction follows the metric and policy definitions.

<sup>d</sup> U1−U0 is implementation validation, not a substantive discovery or recommendation.

## 7. Process-Red-Team Protocol and Governance Implications

### 7.1 What the protocol produces

Usability is a design objective, not an evaluated result. The proposed protocol examines an evidence-to-action path through representation, routing, review, action, contestability, and restoration. It returns separate findings, missing information, located transitions, interventions, owners, and tradeoffs—not an overall score.

Use the least demanding adequate level. A document audit supports structural findings; a bounded deterministic trace supports trace-specific conclusions about ordered events; and a dynamic system simulation supports estimates only within its designed parameter space. Escalate when conclusions depend on realized timing, shared resources, spillovers, or endogenous behavior. If the needed inputs are unavailable, return `unassessable` and name them.

A controlled pair compares two arms while holding the declared case or system inputs fixed and changing only the named representation, rule, or intervention. Detailed levels, status codes, completeness rules, receipt fields, and reference worksheets are provided in Sections S1–S4 of the Supplementary Material.

### 7.2 Step 1: map transformations and ownership

For each handoff, record the source value and type—observed, derived, imputed, disputed, or missing—the transformation, assumptions, downstream representation, provenance, and diagnostic owner. Locate the first transition where a policy-relevant distinction disappears or becomes unavailable to an empowered role.

This applies the proposed evidentiary-fidelity (F0) and material-surfacing (F4) diagnostics. A broad label may fail by hiding imputation, conflicting evidence, lineage, or action-relevant scope. Interventions retain typed provenance, expose material disputes, prohibit unsupported relabeling, and bind transformations to sources. Record the intervention owner separately; it may be the interface or workflow owner rather than the evidence producer.

### 7.3 Step 2: test what weaker evidence permits

Inventory exact progression, constraint, information-acquisition, and restoration actions. For each automatic progression, record its target, parameters, prerequisites, support rule, default, and timeout consequence. F1 asks whether weaker evidence permits an action excluded by the support rule under an admissible refinement. One valid counterexample fails F1; passage requires a conclusion-valid certificate covering the frozen refinement set.

F2 compares executing a fallback with holding it over the complete intervention unit: the focal case and every affected queue, resource, deadline, and case. Without noninterference, a case-local trace is insufficient. Defaults and fail-open timeouts are permission rules. Locate failures at the evidence-to-permission edge; responses include narrower functional permission, evidence acquisition, reversible constraint, effective review, or fail-closed timeout.

### 7.4 Step 3: test whether review is operational

Decompose “human review”: Is a gate configured and blocking? Does an authorized reviewer receive material evidence and control the exact action? Does the workflow wait? Is authorization current at execution? Is a supported disposition reached by the service deadline?

Report `GateSafe`, the study-defined `ReviewEffective`, F3, and `DecisionServiceEffective` separately. A fail-closed gate may be gate-safe while service fails; completed review may be stale or nonbinding. With no configured gate, `GateSafe` is not applicable, although a required missing gate is diagnosed under progression or review. The excluded simulation service output is invalid because its numerator failed semantic audit. Target visibility, stopping authority, dependency, timing, execution-state revalidation, or capacity—not a reviewer label.

### 7.5 Step 4: stress access, workload, and deadlines

Use the simplest adequate level: documents for timeout rules, traces for event order, queue calculations for simple capacity questions, and dynamic simulation for shared resources, feedback, or spillovers. If the question concerns a boundary rather than a sampled operating region, state how that boundary was located and with what resolution.

Stress access, evidence, arrivals, service demand, capacity, deadlines, and timeouts. Report gate safety, timely completion, unresolved cases, interaction events, workload, exposure, and restoration separately. Do not equate delay with safety or backlog reduction with resolution. Matched fail-open and fail-closed policies had identical timely-review completion but opposite permission consequences. Interaction events cannot establish subjective burden or welfare. Recommendations must identify improvement, deterioration, and what remains unmeasured.

### 7.6 Step 5: test contestability and restoration

Separate six questions hidden by “appeal available”: does a structural path exist; is access reliable; was an opportunity available and used; did correction occur; were all required consequences restored? Documents support structural findings; realized and timely conclusions require a trace or system model with declared horizons.

Declare the consequence vector and baseline before claiming restoration. Correcting a decision or balance does not restore recovery status, time, access, or other external consequences. Pending horizons are unassessable, not failed. Interventions can pause recovery, enable evidence acquisition, reserve reassessment capacity, extend windows, and separate correction from restoration ownership. Keep their costs and delays visible. Explicitly name every consequence outside the model.

### 7.7 Fixed Robodebt worked example

The fixed bounded controlled pair is explanatory, not representative. It holds the case, evidence, access, later evidence, process, clocks, evaluation rules, resources, and draws fixed. Only policy changes: impute and progress versus agency-assisted information first.

In the baseline, a notice fails, the 21-day deadline expires, and aggregate income becomes an imputed period representation without surfaced uncertainty. Unsupported modeled debt progression and recovery-process exposure follow; later correction leaves that modeled exposure unrestored at the day-60 restoration check. The repair holds progression, obtains records, records a supported disposition, and avoids modeled exposure. This trace does not establish that information first is costless, generally superior, or historically typical.

A component-local check might confirm that averaging ran as specified; another might confirm that notice issued. Neither of those two checks establishes how failed access, imputation, deadline expiry, and the permission rule combine. The process trace demonstrates that combination in this fixed example, but does not show that no other diagnostic could expose it.

The detailed Robodebt assessment profile, ownership and intervention receipt, evidence limits, statuses, and tradeoffs are provided in Section S5 of the Supplementary Material.

### 7.8 Governance interventions and bounded transfer

Transformation and interface owners can preserve evidence state, provenance, and material disputes. Information-service owners can acquire missing evidence, while policy owners can pause or extend deadlines. Gate owners can make review fail closed; operational owners can reserve capacity, meter arrivals, or prioritize material uncertainty. Recovery owners can pause external action during contest, and restoration owners can repair consequences beyond the decision record. These controls are not interchangeable. Provenance increases interface complexity; evidence acquisition adds interactions and workload; fail-closed review accumulates unresolved cases; added capacity consumes resources; longer deadlines delay disposition; recovery pauses defer collection and prolong open cases; and restoration may require remediation outside the decision system.

The frozen transfer canary illustrates the same bounded procedure on a hypothetical LLM-generated vendor-access summary. The source bundle, routing rule, resources, and clock remain fixed while only the summary transformation changes. Its expected profile locates the first material failure where a fluent summary hides a disputed production restriction and contradictory scan, causing the common rule to omit verification and review and permit automatic provisioning. This author-constructed example demonstrates cross-vocabulary representability; it does not validate transfer, deployed-LLM prevalence, legality, strategic exploitation, practitioner reliability, or field efficacy.

## 8. Limitations and Conclusion

### 8.1 Limitations

The formal results are conditional. Robust permission depends on the declared compatible-refinement set, independently owned support rule, fully instantiated action identities, and ordering that separates progression from constraint, information acquisition, and restoration. An omitted refinement or misspecified support rule can change an assessment. These dependencies limit the conclusion to systems where those objects can be specified and inspected. Missing evidence or rules should produce `unassessable`, not an inferred pass. New domains require their own evaluation specification and refinement-coverage argument.

The Robodebt application establishes documented structural relevance and compatibility with the proposed mechanism, not independent causation or numerical calibration. The early and enhanced OCI profiles are bounded by the selected sources, dates, and recorded precision. Executable queue, engagement, retrieval, service, correction, and restoration values are stylized. Simulation rates therefore do not estimate historical Robodebt prevalence, capacity, delay, debt error, or causal effects. Historical quantification would require a separately sourced dataset, new measurement model, and new design freeze. The study supplies no monetary-entitlement oracle and makes no independent legal judgment.

Four measurement limits restrict comparison. First, the decision-service output is excluded because its numerator did not verify a supported disposition by the service deadline; repair requires a revised metric and affected rerun. Second, interaction events record responses and assistance requests, not evidence-production effort, psychological cost, welfare, or subjective burden. U3’s additional interactions therefore leave substantive burden unresolved. Third, the frozen analysis emitted no registered paired correction or restoration estimand. The terminal right-censoring rate was 1.000 in every U0, U2C, and U3 family cell; this includes structurally open or unmodeled terminal paths, not only work continuing to day 650. Earlier stage outcomes remain interpretable, but complete-resolution and complete-restoration comparisons do not. Fourth, MCSE measures finite-run precision only, while unweighted cross-family means imply no real-world scenario distribution.

The kernel represents declared rules, finite queues, deadlines, keyed exogenous variation, and modeled correction paths. It does not model reviewer psychology, discretion, deference to automated outputs, strategic adaptation, endogenous demand, adaptive staffing, priority rules, or organizational learning. Nor does it supply a scalar welfare function. Gate safety, timeliness, unresolved holding, interaction events, agency workload, exposure, correction, and restoration remain separate coordinates, so the results cannot identify a universally optimal or generally safer policy. Delay, deprivation, abandonment, queue displacement, and spillovers were not measured as terminal consequences. Consequence-complete comparison requires future evidence, including broader sensitivities or observed institutional traces.

The study provides executable examples and a cross-vocabulary canary, but no practitioner study, usability validation, adoption evidence, or estimate of inter-rater agreement. The canary supports bounded representability in a contemporary AI-style workflow; it does not establish field transfer or prevalence. Process susceptibility also does not prove historical attackability: inducibility, observability, repeatability, and actor benefit were not established.

### 8.2 Conclusion

The central question is what the workflow may newly do when decision-relevant evidence is lost. Under the declared refinement and support rules, weaker evidence cannot justify automatic progression unless the action remains independently supported across the admissible refinements. It may permit appropriately evaluated constraint, information, or restoration actions without expanding automatic progression. This identifies functional permission and operational control in the evidence-to-action process; it does not locate legal or formal authority.

The simulation shows why that distinction becomes operational under load inside the frozen stylized system. Across three loads, fail-closed review preserved gate safety while timely review completion declined and unresolved holding increased. With review machinery and paired cases fixed, fail-open timeouts converted non-completion into unsupported progression and recovery exposure. The information-first policy likewise prevented unsupported progression but added interaction and agency-workload events and increased modeled exposure relative to conservative holding; exposure is a process state, not established error or harm. Its effect on substantive recipient burden remains unknown. These are designed-parameter-space results, not a historical capacity threshold or Robodebt reconstruction.

The study supports no single policy ranking. Nominal review, notice, or appeal cannot by themselves establish meaningful control. As a proposed governance principle, meaningful control depends on whether uncertainty remains visible, whether the gate binds the exact action, whether an empowered reviewer can act before timeout, what follows non-completion, and whether correction restores every modeled consequence. The invalid service measure blocks a timely-supported-service comparison, while terminal censoring blocks complete-restoration comparisons for the most heavily censored policies. Fail-closed and information-first handling are permission-preserving within the demonstrated model, not established generally safer remedies: delay, deprivation, abandonment, queue displacement, spillovers, and consequence-complete welfare were not measured.

For process red teaming, the candidate diagnostic is compact: when evidence becomes weaker, what may the system now do; who can still stop it; and can they do so before the consequence becomes difficult to restore? Answering those questions requires tracing evidence through representation, permission, capacity, action, and restoration. Treating that full chain—not the presence of a reviewer or the local correctness of one component—as the unit of governance is the article’s proposed principle.

## Data and Code Availability

The code, frozen specifications, source manifest, fixed traces, validation receipts, family-level analysis artifacts, protocol worksheets, and reproduction commands are maintained in the project repository, which is private during manuscript development and will be made publicly accessible before submission. Upon release, the [project repository](https://github.com/etalbert102/uncertainty_permission_simulation) and its [evidence packet](https://github.com/etalbert102/uncertainty_permission_simulation/blob/main/docs/EVIDENCE_PACKET.md) will map the article’s formal, historical, simulation, and worked-example claims to their supporting artifacts. The immutable scientific inventory is identified by SHA-256 `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c`; the release verifier checks that inventory and the stored analyses. Historical source documents remain with their publishers or issuing institutions and are identified by URL and retrieval metadata in the source manifest.

## References

Alon-Barkat, S., & Busuioc, M. (2023). Human–AI interactions in public sector decision making: “Automation bias” and “selective adherence” to algorithmic advice. *Journal of Public Administration Research and Theory, 33*(1), 153–169. https://doi.org/10.1093/jopart/muac007

Anyabolu, C., Dubey, A., & Hattab, G. (2026). Visualizing uncertainty-to-action composition for human oversight. arXiv. https://arxiv.org/abs/2608.16428

Bennett, H., Currie, M., & Podoletz, L. (2026). Universal Credit: Administrative burdens of automated welfare. *Journal of Social Policy, 55*(1), 24–42. https://doi.org/10.1017/S0047279424000175

Blackwell, D. (1953). Equivalent comparisons of experiments. *Annals of Mathematical Statistics, 24*(2), 265–272. https://doi.org/10.1214/aoms/1177729032

Commonwealth Ombudsman. (2017). *Centrelink’s automated debt raising and recovery system*. https://www.ombudsman.gov.au/__data/assets/pdf_file/0022/43528/Report-Centrelinks-automated-debt-raising-and-recovery-system-April-2017.pdf

Commonwealth Ombudsman. (2019). *Centrelink’s automated debt raising and recovery system—Implementation report*. https://www.ombudsman.gov.au/__data/assets/pdf_file/0027/286551/Centrelinks-Automated-Debt-Raising-and-Recovery-System.pdf

Commonwealth Ombudsman. (2023). *Lessons in lawfulness: Own motion investigation into Services Australia’s and the Department of Social Services’ response to the question of the lawfulness of income apportionment before 7 December 2020*. https://www.ombudsman.gov.au/__data/assets/pdf_file/0040/299947/Income-Apportionment-Lawfulness.pdf

Deloitte for the Royal Commission into the Robodebt Scheme. (2023a). *2B. Identity matching—OCI and EIC*. https://robodebt.royalcommission.gov.au/system/files/2023-03/2B-Identity-Matching-Process-Map-OCI-and-EIC.pdf

Deloitte for the Royal Commission into the Robodebt Scheme. (2023b). *3B. Income matching—OCI*. https://robodebt.royalcommission.gov.au/system/files/2023-03/3B-Income-Matching-Process-Map-OCI.pdf

Deloitte for the Royal Commission into the Robodebt Scheme. (2023c). *4B. Debt calculation and notification—OCI baseline*. https://robodebt.royalcommission.gov.au/system/files/2023-03/4B-Debt-Calculation-and-Notification-Process-Map-OCI.pdf

Deng, J. (2026). When can fraud operations authorize automation? A decision-support framework for fresh audit evidence and review workload. arXiv. https://arxiv.org/abs/2608.08577

El-Yaniv, R., & Wiener, Y. (2010). On the foundations of noise-free selective classification. *Journal of Machine Learning Research, 11*, 1605–1641. https://jmlr.org/papers/v11/el-yaniv10a.html

Franc, V., & Průša, D. (2019). On discriminative learning of prediction uncertainty. In K. Chaudhuri & R. Salakhutdinov (Eds.), *Proceedings of the 36th International Conference on Machine Learning* (Vol. 97, pp. 1963–1971). PMLR. https://proceedings.mlr.press/v97/franc19a.html

Gilboa, I., & Schmeidler, D. (1989). Maxmin expected utility with non-unique prior. *Journal of Mathematical Economics, 18*(2), 141–153. https://doi.org/10.1016/0304-4068(89)90018-9

Hardy, K. (2026). From human oversight to effective control: A comparative documentary framework for high-impact AI systems. *Design+*. Advance online publication. https://doi.org/10.36922/DP026290034

Landau, S., Dempsey, J. X., Kamar, E., & Bellovin, S. M. (2024). *Recommendations for government development and use of advanced automated systems to make decisions about individuals*. Stanford Center for International Security and Cooperation. https://cisac.fsi.stanford.edu/publication/recommendations-government-development-and-use-advanced-automated-systems-make

Leveson, N. (2012). *Engineering a safer world: Systems thinking applied to safety*. MIT Press.

Liao, J., Huang, Q., Qian, R., Mao, X., Cheng, J., Cui, K., Li, Y., Sun, J., & Hou, Y. (2026). Auditing provenance sensitivity in LLM agent action selection. arXiv. https://arxiv.org/abs/2607.20827

Lin, H., Cao, S., Luo, Z., Chai, W., Lee, M.-L., & Hsu, W. (2026). From evidence to action: How tool-using agents fail. arXiv. https://arxiv.org/abs/2610.07753

Little, J. D. C. (1961). A proof for the queuing formula: L = λW. *Operations Research, 9*(3), 383–387. https://doi.org/10.1287/opre.9.3.383

Montanari, G., Scarsini, M., & Perchet, V. (2026). Learning when to automate: Queue control in human-AI service systems. arXiv. https://arxiv.org/abs/2607.06017

Moynihan, D. P., Herd, P., & Harvey, H. (2015). Administrative burden: Learning, psychological, and compliance costs in citizen–state interactions. *Journal of Public Administration Research and Theory, 25*(1), 43–69. https://doi.org/10.1093/jopart/muu009

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)*. https://doi.org/10.6028/NIST.AI.100-1

Prabhudesai, S., Yang, L., Asthana, S., Huan, X., Liao, Q. V., & Banovic, N. (2023). Understanding uncertainty: How lay decision-makers perceive and interpret uncertainty in human-AI decision making. In *Proceedings of the 28th International Conference on Intelligent User Interfaces* (pp. 379–396). Association for Computing Machinery. https://doi.org/10.1145/3581641.3584033

Reisman, D., Schultz, J., Crawford, K., & Whittaker, M. (2018). *Algorithmic impact assessments: A practical framework for public agency accountability*. AI Now Institute. https://ainowinstitute.org/publication/algorithmic-impact-assessments-report-2

Roehl, U. B. U. (2023). Automated decision-making and good administration: Views from inside the government machinery. *Government Information Quarterly, 40*(4), Article 101864. https://doi.org/10.1016/j.giq.2023.101864

Roehl, U. B. U., & Hansen, M. B. (2024). Automated, administrative decision-making and good governance: Synergies, trade-offs, and limits. *Public Administration Review, 84*(6), 1184–1199. https://doi.org/10.1111/puar.13799

Royal Commission into the Robodebt Scheme. (2023). *Report of the Royal Commission into the Robodebt Scheme*. https://robodebt.royalcommission.gov.au/publications/report

Services Australia. (2025). *Automation and artificial intelligence strategy 2025–27*. https://www.servicesaustralia.gov.au/sites/default/files/2025-05/automation-and-ai-strategy-2025-27.pdf

Sterz, S., Baum, K., Biewer, S., Hermanns, H., Lauber-Rönsberg, A., Meinel, P., & Langer, M. (2024). On the quest for effectiveness in human oversight: Interdisciplinary perspectives. In *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency* (pp. 2495–2507). Association for Computing Machinery. https://doi.org/10.1145/3630106.3659051

Sztandar-Sztanderska, K. (2026). How context matters: Human oversight of automated decision-making systems in welfare administration. *Journal of European Social Policy, 36*(3), 255–269. https://doi.org/10.1177/09589287251358069

Wang, Z., & Rachev, S. T. (2026). Operating imperfect AI: Reliability drift and human congestion. arXiv. https://arxiv.org/abs/2601.22295
