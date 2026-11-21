# From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application

**Eli Talbert**

Independent researcher

Correspondence: etalbert102@gmail.com

## Abstract

AI-generated classifications, summaries, and recommendations can enter workflows that route cases, assign review, trigger deadlines, and permit action. The central question is: when evidence becomes less decision-relevant, what may an automated workflow now do? This article proposes robust permission: weaker evidence should not newly enable an exact action—such as debt calculation, recovery, or account provisioning—unless that action remains independently supported across every admissible refinement. Reviewed progression must remain outside the automatic set, bind the exact action, and revalidate support at execution. The study states these rules formally, demonstrates them with a deterministic pair, applies them to the documented Robodebt process, and uses a design-frozen finite-cohort simulation to estimate how often limited capacity activates declared timeout consequences. Across three loads, fail-closed review remained gate-safe while timely completion declined and holding increased. A matched fail-open policy converted the same review shortfall into unsupported progression and modeled downstream exposure. An information-first policy avoided unsupported progression but increased interaction and workload events; substantive burden remains unresolved. Semantic audit excluded an invalid service measure. The study neither reconstructs historical Robodebt nor supports a continuous capacity threshold or cross-policy restoration comparison. Its five-step protocol keeps safety, delay, workload, modeled downstream exposure, and unresolved cases separate.

*Keywords:* automated decision-making, human oversight, uncertainty, discrete-event simulation, Robodebt

## 1. Introduction

### 1.1 The organizational failure mode

A defensible abstraction can still remove the distinction that would have triggered caution. A classifier may truthfully report a broad category; an agency may consistently transform an annual total into period values; a large language model summary may accurately compress its source. Yet once that representation enters an operating workflow, it can change routing, review, deadlines, and action. Emerging technologies motivate the inquiry because their outputs may move across systems and trigger downstream rules quickly; this paper does not establish adoption, prevalence, or comparative importance. The relevant unit of governance is therefore not the model output alone, but the full chain from evidence and representation through routing, review, action, correction, and restoration.

The emerging-technology connection is functional rather than historical. Before deploying an AI-enabled workflow, an organization can vary the representation of the same output and stress the downstream gate under expected and adverse load. Robodebt contributes something the synthetic examples cannot: a documented, consequential institutional sequence from evidence transformation through automated action, recovery, and reassessment. It is a testbed for that governance architecture, not evidence about current AI prevalence or performance.

This paper calls what the operating workflow allows to proceed *functional permission*. Functional permission is distinct from formal authority, legal validity, and action actually taken. It includes every action the workflow makes automatically available in the current state, whether or not an operator selects it and whether or not formal authority has changed. The central question is: when evidence becomes less decision-relevant, what may the workflow now do automatically? The failure occurs when lost information removes a safeguard or enables progression the remaining evidence cannot independently support. In the Robodebt application, that would mean using imputed fortnightly values after nonresponse to enable debt calculation, debt notice, or recovery.

### 1.2 Why nominal review is insufficient

The presence of a review field does not answer that question. A gate may be missing, fail open, or control the wrong action. Review is effective only if the case is surfaced before automatic progression, evidence bearing on the exact action is visible, an authorized reviewer can stop or modify that action, the workflow enforces that dependency, and the decision is completed and recorded before intervention is foreclosed. The formal model calls this `ReviewEffective`. `DecisionServiceEffective` separately asks whether the process reaches a supported disposition by a declared deadline. Neither construct is offered as a universal empirical requirement. Capacity and timeout rules are governance choices because they determine what happens when review does not finish. In the simulation, the reported review measure captures only timely completion; the service result is excluded because its numerator did not verify supported dispositions by the deadline.

### 1.3 Completed research design

The study combines five evidence layers: a formal model, a controlled representation pair, a documented Robodebt application, a dynamic simulation, and a prospective protocol. Within that architecture, F0 tests evidentiary fidelity, F1 robust permission, F2 fallback consequences, F3 operational review, F4 material surfacing, and F5 correction and restoration. Table 1 maps each layer to those diagnostics. None substitutes for another.

**Table 1**

*Evidence Architecture and Diagnostic Scope*

| Layer | Question and principal diagnostics | Evidence used | Cannot establish |
| --- | --- | --- | --- |
| Formal model | What may weaker evidence permit, and what must review or restoration satisfy? F1–F5 | Declared refinement, support, action, gate, and consequence rules | Frequency, historical causation, or welfare |
| Controlled representation pair | Can representation alone change routing and automatic permission? F0 and F4; F1 is unassessable because evidence is fixed | Same synthetic case and output; only representation changes | Prevalence, queues, or review effectiveness |
| Robodebt application | Does a documented process contain the relevant evidence-to-action structure? F0, F4, and structural F3/F5 | Fixed source packet and dated OCI profiles | Independent causation or numerical calibration |
| Dynamic simulation | How often do capacity and timeout rules activate, and with what modeled process outcomes? Paired outcomes relevant to F2, the timing component of F3, and selected F5 paths; no formal F2 assessment | Designed families, paired policies, and finite queues | Historical rates, complete welfare, or full terminal comparison |
| Five-step protocol | Can the same questions be posed prospectively in another inspectable workflow? All diagnostics as applicable | Article procedure | Usability, field transfer, or prevalence |

### 1.4 Findings and contributions

The results separate rule-implied directions from dynamic quantities. Fail-closed gate safety and fail-open release follow the policy definitions; the simulation estimates how often finite capacity activates those consequences. Across three prespecified loads, timely review completion fell and unresolved holding rose under fail-closed review. These load points show a response to load; they do not estimate a historical or continuous threshold. Holding review machinery and paired cases fixed, fail-open timeouts redirected the same non-completion into unsupported progression and modeled downstream exposure. An agency-assisted information-first policy also produced zero unsupported progression, but added interaction and agency-workload events and increased modeled downstream exposure relative to conservative holding. Because the interaction measure counts events rather than evidence-production effort, psychological cost, or welfare, the substantive recipient-burden question remains unresolved.

Two measurement limits qualify those results: the invalid decision-service output is omitted, and open terminal paths prevent complete-resolution and complete-restoration comparisons. The unresolved issue is therefore whether any tested intervention avoids unsupported progression without hiding delay, burden, workload, modeled downstream exposure, or unresolved cases.

This paper’s claimed contribution is the joint specification and demonstration of a workflow-level permission rule: loss of decision-relevant information cannot by itself expand automatic progression unless the action remains independently supported, while capacity and timeout rules determine whether unresolved review produces holding or action. The article connects that rule to a representation pair with negative controls, a documented institutional application, explicit restoration semantics, a finite-capacity simulation, and a five-step protocol.

Figure 1 previews the evidence-to-action chain that serves as the unit of analysis and the five diagnostic steps developed in Section 7.

**Figure 1**

*Evidence-to-Action Chain and Five Process-Red-Team Steps*

![Figure 1. Evidence-to-action chain and five process-red-team steps.](figures/figure1_evidence_to_action_protocol.svg)

*Note.* The protocol follows one action through representation, permission, review, execution, and restoration while keeping formal authority, independent support, automatic permission, and executed action distinct.

## 2. Mechanism, Literature, and Research Questions

### 2.1 Representation-preservation controlled pair

A controlled pair is two deterministic traces of the same synthetic case and the same stored model output. The operational policy, routing rule, process state, reviewer resource, clock, and absence of random draws are held fixed. Only the representation transformation and the representation it mechanically emits differ. This domain-neutral mechanism test isolates representation suppression: the evidence is fixed while only its downstream representation changes. The Robodebt application instead concerns aggregate evidence transformed into imputed period values, and the simulation includes unresolved or missing period evidence. Their shared conclusion is limited to the downstream permission structure: a policy-material distinction is lost or unresolved, and a downstream rule changes permission.

The output describes a low-resolution road object as a pickup-like silhouette with confidence 0.42 and lists live alternatives that include an armed technical. In the preservation arm, typed alternatives, confidence, unresolved status, and provenance remain visible. The material alternative triggers an information action, enhanced scrutiny, and a fail-closed review dependency; routine disposition is unavailable automatically. In the fallback arm, the identical output becomes the broad untyped label `vehicle`. That label is compatible with every listed alternative and is not literally false, but it suppresses the distinction used by the fixed policy. The same downstream rule now routes the case routinely, removes the information and review steps, and automatically permits routine disposition. Here, routine disposition means finalizing the synthetic organizational case without enhanced scrutiny; it does not authorize action against the physical object.

Two controls bound the interpretation. When the output contains no policy-material alternative, changing representation leaves routing unchanged. When the safeguard is representation-independent, both representations retain scrutiny. The pair therefore demonstrates the mechanics of representation suppression changing permission; it does not show that the evidence itself became weaker, and F1 is unassessable because the evidence is fixed. It does not test model accuracy, latent truth, frequency, queues, historical conduct, or whether completed review would be effective.

### 2.2 Mechanism and scope

The shared permission structure requires three conditions: a representation that is defensible at some level of abstraction, or an unresolved evidence state; a distinction that matters to an independently specified policy or support rule; and a downstream rule that relaxes a safeguard when that distinction disappears. None is sufficient alone. Coarsening can be harmless when the lost distinction is immaterial, and weaker evidence can properly trigger a hold or a request for more information.

The action direction matters. *Progression* advances or commits the process, imposes an external consequence, or forecloses a required safeguard. *Constraint* pauses or contains progression; *information* obtains evidence without independently releasing unsupported progression; and *restoration* repairs a prior process or consequence. The claim is that information loss should not add unsupported automatic progression, although it may justify separately evaluated constraints or information seeking. The rule preserves permission rather than guaranteeing complete safety: delay, deprivation, abandonment, queue displacement, and spillovers are not measured here as terminal consequences.

This is a base workflow vulnerability, not necessarily an attack. Structural susceptibility means a declared mutation can reproduce it. Adversarial exploitability requires separate evidence that the mechanism is inducible, observable, repeatable, and beneficial to an actor. Neither the controlled pair nor the Robodebt application supplies those four findings.

### 2.3 Literature and proposed integration

Three research traditions frame the unresolved workflow question. Work on information structures, robust choice, selective classification, abstention, and uncertainty communication establishes that evidence can be ordered, ambiguity can matter to choice, and uncertain outputs can be withheld or communicated (Blackwell, 1953; El-Yaniv & Wiener, 2010; Franc & Průša, 2019; Gilboa & Schmeidler, 1989; Prabhudesai et al., 2023). Uncertainty-to-action binding already makes oversight responses to uncertainty explicit (Anyabolu et al., 2026). Recent agent and fraud-operation preprints further distinguish correct endpoints from actions supported by established, authorized, or sufficiently fresh evidence (Deng, 2026; Liao et al., 2026; Lin et al., 2026). The unresolved question here is whether the surrounding workflow expands automatic progression when decision-relevant information is lost.

Research on effective human oversight, automation bias, administrative burden, automated administration, and contestability shows why nominal human presence may be insufficient. It also treats burden, discretion, and challenge mechanisms as institutional rather than interface-level problems (Alon-Barkat & Busuioc, 2023; Bennett et al., 2026; Landau et al., 2024; Moynihan et al., 2015; Roehl, 2023; Roehl & Hansen, 2024; Sterz et al., 2024; Sztandar-Sztanderska, 2026). Hardy’s (2026) Oversight-to-Control framework is a particularly close institutional comparison because it separates observation, interpretation, challenge, intervention, and recovery. The present integration adds the robust-permission rule and an executed dynamic counterfactual while leaving reviewer psychology outside its numerical claims.

Finally, queueing, system safety, AI risk governance, and algorithmic impact assessment treat performance as a property of service capacity, control structures, context, ownership, and feedback rather than a component in isolation (Leveson, 2012; Little, 1961; National Institute of Standards and Technology, 2023; Reisman et al., 2018). Recent queue-control preprints explicitly coordinate automation or escalation with limited human review and service capacity (Montanari et al., 2026; Wang & Rachev, 2026). The present study does not propose an optimal controller; it stress-tests fixed safeguard and timeout rules across declared capacity conditions. Here, *process red teaming* means stress-testing how evidence, rules, capacity, deadlines, and defaults interact across a workflow; it does not imply an adversarial attack.

The paper brings these literatures together around one organizational sequence. Information ordering and robust choice supply the refinement and support structure. Selective classification and uncertainty-to-action work inform rules for withholding action or seeking evidence. Oversight, queue control, and contestability add finite capacity, action-binding review, correction, and restoration. The controlled pair, dynamic simulation, and documented application then show how these elements interact in one process. The claimed contribution lies in that integration and demonstration, not in field-wide priority or any single component.

### 2.4 Research questions and falsifiability

The study asks: (1) when may weaker evidence support automatic progression under the proposed robust-permission rule; (2) under the tested access and capacity conditions, does a configured gate block progression with unmet prerequisites, and how does timely review completion vary; and (3) which interventions avoid unsupported progression without hiding delay, burden, workload, modeled downstream exposure, or unresolved cases? The remaining `ReviewEffective` conditions are held invariant or demonstrated structurally, not estimated.

The design can fail its intended contribution. The representation account would lose diagnostic value if a valid enabling pair showed no representation-to-permission change, or if ordinary component-local checks located every induced failure. The dynamic account would narrow to authored semantics if access, capacity, and deadlines produced no consequential variation across the frozen range. The practical account would fail if it could not locate a transition, responsible owner, intervention, tradeoff, and replayable repair beyond what a local accuracy or calculation check already provides. These are contribution-level falsifiers, not population hypotheses.

## 3. Formal Model

In plain language, the model asks three questions. What possibilities remain compatible with the evidence? Which exact actions does the workflow make automatically available? Would each progression action still be supported if the missing detail were resolved in any admissible way? In the Robodebt mapping, the annual employer total is aggregate evidence, supported fortnight-specific income records define finer evidence states, and imputed fortnightly values are not treated as observed period evidence; debt calculation, debt notice, and recovery are the actions under inspection. If support for an action fails under any admissible refinement, the workflow must seek evidence, pause the case, or require effective review; a reviewed action must be supported again before execution. The notation below keeps formal authority, operational permission, and executed action distinct.

### 3.1 Evidence, compatible states, and refinement

An evidence state `e` denotes a set of states compatible with what is known. Evidence `e_more` refines `e_less` when its compatible set is a nonempty subset of the coarser set under independently declared source and measurement assumptions. Refinement is therefore about excluded possibilities, not confidence alone: two estimates with different confidence scores need not be comparable, and a more confident transformation can still discard a policy-relevant distinction.

The admissible refinements of `e_less`, written `Ref(e_less)`, must be specified independently of the action the workflow prefers. A pass must cover every admissible refinement. Coverage can be established by enumerating the full set, defining it symbolically, or testing a sound conservative superset. A validated counterexample can prove failure, but an unsuccessful search cannot prove a pass. If the support rule, refinement coverage, or action identity is missing, the result is `unassessable`, not a pass inferred from missing evidence.

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

F3 governs progression withheld from the automatic set pending review. `GateSafe` asks whether a configured dependency prevents action while prerequisites remain unmet. In this study’s evaluative definition, `ReviewEffective` additionally requires timely surfacing, access to evidence bearing on the exact action, an authorized reviewer with stopping power, enforced dependency, completion before foreclosure, and a recorded decision. `DecisionServiceEffective` asks whether a supported disposition is reached by a declared deadline. A gate can be gate-safe while the latter two fail.

Review authorization binds the exact action, case, evidence and rule versions, conditions, and expiry. Notice, a reviewer label, a stale decision, post-action reassessment, or authorization of a different action instance does not satisfy F3.

Because pre-action review does not establish post-action repair, F5 separates six questions often collapsed into “appeal available”: Does a feasible correction path exist? Is it prospectively reliable under access, capacity, and timing? Was an opportunity available? Was it used? Did correction finish? Did every modeled consequence return to baseline? Correcting the recorded decision does not prove restoration of recovery status, money, access, time, or another consequence. Pending horizons are `unassessable`; after the horizon, any required residual prevents complete restoration.

### 3.6 Formal propositions and simulation implication

**Formal characterization 1—robust permission.** `P_robust` is the unique maximal progression-action set supported under every admissible refinement, and F1 holds if and only if automatic progression under the coarser evidence is its subset. Each member of the intersection is supported everywhere. Any strict superset contains an action excluded by at least one refinement, which supplies a counterexample. The result is conditional on a sound declared refinement certificate, fixed comparison state and rules, unambiguous action identity, and an independently specified support rule.

**Formal characterization 2—operational review.** A correctly enforced fail-closed gate remains gate-safe regardless of delay, but need not yield effective review or timely supported service. Over a service window `H`, an aggregate reviewer service rate `μ` cannot complete required work `W` plus initial backlog `B0` when `W + B0 > μH`. If prerequisites remain unmet at timeout, fail-closed semantics retain unresolved cases; fail-open semantics can release unsupported progression. The two designs may therefore have identical review completion yet opposite permission consequences. This diagnostic characterization requires deterministic ordering, a non-bypassable fail-closed gate, declared finite capacity, and explicit deadlines and timeout rules.

These characterizations do not determine whether information acquisition improves operational outcomes. An information-first policy may preserve permission while changing interactions, workload, modeled downstream exposure, and unresolved holding; those quantities depend on the declared process and parameters and must be estimated rather than derived. The simulation therefore treats information first as an empirical policy comparison, not a third theorem. Full notation, proofs, subordinate properties, and counterexamples remain in the repository specification.

## 4. Robodebt as a Documented Process Application

### 4.1 Why this case

The record documents an OCI evidence-to-action process. Aggregate income was matched, transformed into period values, and presented through notices and online access. Deadlines and responses shaped routing into automated calculation and debt action, followed by recovery, reassessment, and review. That observable sequence makes Robodebt structurally compatible with the proposed mechanism. The analytical mapping is the study’s: the documents do not establish that representation loss independently caused the outcome, and policy intent, legal interpretation, incentives, and evidentiary risk remain alternative explanations. Robodebt is a documented institutional testbed, not contemporary machine learning or generative AI.

### 4.2 Sources and application validity

The fixed packet contains ten sources retrieved through 31 October 2026. Ombudsman reports provide the principal process record (Commonwealth Ombudsman, 2017, 2019), Deloitte maps provide node-level structure (Deloitte for the Royal Commission into the Robodebt Scheme, 2023a, 2023b, 2023c), and the Royal Commission supplies attributed historical findings and recommendations (Royal Commission into the Robodebt Scheme, 2023). Services Australia (2025) supplies limited current context. The Ombudsman’s income-apportionment report is used only to distinguish that practice from Robodebt income averaging (Commonwealth Ombudsman, 2023).

The analysis distinguishes three validity questions. First, are attributed facts anchored to the proper source and period? Second, does the study reasonably map those facts onto evidence, transformation, routing, action, review, and correction constructs? The dated early and enhanced OCI profiles support both judgments, but neither establishes that the proposed mechanism independently caused the program’s outcomes. Third, numerical calibration would require historical distributions for arrivals, capacity, service, engagement, retrieval, correction, and restoration. The packet does not supply them, so the paper makes no calibration claim.

### 4.3 Early OCI process profile

The early profile covers the July 2016 OCI launch through 19 January 2017, ending before the first specifically dated letter change. Under the documented OCI design, matched Australian Taxation Office (ATO) pay-as-you-go income and Centrelink information passed through refresh, inclusion, discrepancy, and risk rules before a notice was sent through the selected digital channel or last-known address. The initial letter allowed 21 days from its date to respond, with a reminder after 14 days (Commonwealth Ombudsman, 2017, paras. 1.17–1.29; Deloitte for the Royal Commission into the Robodebt Scheme, 2023a, 2023b, 2023c).

A responding recipient could confirm or correct employer, amount, and pay-period information and supply evidence; specified errors or unresolved inputs could receive compliance-officer handling. The documented process placed responsibility on recipients to reconstruct and enter historical income information. The Ombudsman noted that decision accuracy depended on their ability to obtain those records despite weaker information-gathering powers and possible bank-statement costs (Commonwealth Ombudsman, 2017, paras. 3.26–3.28). If the recipient did not respond by the due date, the documented OCI design evenly apportioned ATO earnings information over the employer-reported employment period, calculated entitlement and any debt, issued a debt notice when the calculation produced one, and commenced normal recovery. Later information could trigger reassessment, and internal review remained available (Commonwealth Ombudsman, 2017, paras. 1.17–1.29, Appendix B).

The critical analytical transition is not aggregation alone. An annual employer total is evidence about total income, but even apportionment creates fortnightly values through a transformation rather than revealing actual fortnightly income. In the documented OCI pathway, nonresponse allowed those values to feed automatic calculation, debt notice, and recovery; the study maps that sequence as a coupling of representation, deadline, and permission. This establishes compatibility with the proposed mechanism, not causation, frequency, or the legal or monetary validity of any particular debt.

The documentary record fixes the 21-day clock, 14-day reminder, averaging transition, debt-notice path, recovery, and reassessment opportunity. It does not yield model-ready queue capacity, service-time, notice-engagement, evidence-retrieval, correction-uptake, or restoration-delay distributions. Those quantities remain visibly stylized in the simulation.

### 4.4 Enhanced OCI and repair mechanisms

The enhanced profile is an as-documented early-2017 repair bundle, not a single policy activated on one invented date. The Commonwealth Ombudsman’s (2017) April report identified changes beginning with the first letter revision on 20 January and further changes during February. The bundle added direct access using a confirmation code and customer reference number, clearer contact information, registered-mail and telephone follow-up, more recent address information where authorized, and 28 days from receipt with a signposted extension route.

The documented OCI design also expanded manual intervention for disputed inputs, complex circumstances, selected other-income answers, and difficulty accessing records. It added online bank-statement entry with net-to-gross calculation, clearer handling when payslips were unavailable, a visible estimated gross amount, and more opportunity to revise inputs before accepting a provisional result. The Ombudsman reported that bank statements had already been accepted as reasonable historical-income evidence when other evidence was unavailable. The attributed agency statement supplies the evidence; the documented requirement that a notice be received and ignored supplies the operational guard against debt-collector referral after nonresponse (Commonwealth Ombudsman, 2017, paras. 1.30–1.46).

These changes target access, surfacing, evidence acquisition, routing, and recovery gating. Together they define the repair profile examined here. They do not show that every failure disappeared or that configured manual intervention was adequately staffed, timely, or effective. Later program variants and remediation processes are outside this profile.

Figure 2 contrasts the documented early OCI pathway with the enhanced repair bundle and identifies the separate simulation layer.

**Figure 2**

*Early and Enhanced OCI Process Profiles*

![Figure 2. Early and enhanced OCI process profiles.](figures/figure2_robodebt_process_profiles.svg)

*Note.* Source-grounded process structure establishes analytical relevance; the simulation layer remains explicitly stylized rather than a numerical reconstruction of Robodebt. The historical process structure is synthesized from Commonwealth Ombudsman (2017, paras. 1.17–1.46, Appendix B) and Deloitte for the Royal Commission into the Robodebt Scheme (2023a, 2023b, 2023c).

### 4.5 Formal crosswalk and inference limits

The documents support the process facts; the crosswalk is the study’s analytical mapping. An annual employer-income total and broad employment period are treated as coarser evidence. Supported fortnight-specific income and working dates are treated as admissible finer states. Evenly apportioning the total is treated as a representation rule because it creates period values from aggregate evidence.

The documented profile identifies debt calculation, notice, recovery, hold, and evidence-request actions. Executable simulation instances become fully specified only after valid source bindings and separate parameter overlays are compiled. The response deadline and nonresponse branch map to timeout semantics. The enhanced receipt-and-ignoring condition maps to a gate on collector referral, but configuration alone does not establish gate safety.

Notice and interface records bear on whether material information reaches a responsible officer or reviewer, but the record does not identify that actor at every transition. An officer route is a possible review path, not proof of effective review. Reassessment is a correction path. Complete restoration would additionally require every modeled consequence—including recovery status and residual downstream exposure—to return to baseline.

The historical process profile supplies no action-support criterion. The study independently specifies period-specific support, materiality, action identity, review conditions, and restoration obligations; none can be attributed to the historical program. Historical formal authority remains source-attributed and may be unassessable, and simulation code cannot fill the legal or documentary gap. When the record does not identify a particular official, agency unit, software component, or gate owner, the article attributes only the recorded state change to the OCI design and leaves the actor unassessable.

Unsupported historical parameters cannot become defaults; executable values come from versioned simulation overlays. Royal Commission and Ombudsman findings remain attributed rather than becoming simulation outputs.

### 4.6 Transition to simulation

Because the required historical numerical distributions are unavailable, the simulation asks a counterfactual governance question over a declared parameter space. Five counterfactual policies compare conservative holding, automatic progression, fail-closed and fail-open review, and agency-assisted information acquisition; none is a label for a historical Robodebt policy. The dated application profiles own the documented structure, while versioned overlays own every unsupported executable parameter.

## 5. Dynamic Simulation Methods

### 5.1 Purpose, kernel, and unit of analysis

The simulation has a limited purpose: to measure how often finite capacity activates declared timeout consequences and to trace coupled process outcomes within the simulated system. It does not discover the logical direction of the gates. We implemented a finite-cohort discrete-event simulation of an administrative evidence-to-action process. Each run followed 80 cases under one scenario family, policy, and replication. Policies were paired within each family and replication, and the scenario family was the summary unit across designed conditions. Cases moved through engagement, evidence representation, routing, possible review, action, modeled downstream exposure, correction, and restoration. Staffed stages used finite-capacity, work-conserving FIFO queues with deterministic tie-breaking. At day 650, the system recorded both administratively censored work and paths lacking a modeled terminal-resolution event; neither was treated as resolved.

The kernel was case-neutral: no Robodebt identifier or case-specific rule entered its event logic. Robodebt established structural relevance; unmeasured quantities remained simulation inputs, not historical calibration. Policies, evaluation specifications, execution settings, and scenario mappings were separately controlled inputs.

Cases first entered with fixed membership, latent attributes, potential evidence, and access attributes. The model retained the documented 21-day response deadline; all queue capacity, service, engagement, retrieval, correction, restoration, and cutoff values were declared stylized assumptions rather than historical defaults. The support decision was then governed by a stored evaluation specification: progression required period-specific evidence from a response or proactive retrieval. The specification declared the binary evidence universe, assumptions, exclusions, complete-enumeration argument, generator and proof identities, conclusion-validity mode, and material action-comparison fields. The supported state had one supporting refinement; the unresolved state had supporting and non-supporting refinements, placing progression outside `P_robust`. A validated symbolic family instantiated the exact case-specific progression action. At routing and execution, the kernel evaluated that action across every certified refinement and retained compact receipts binding the specification, implementation, certificate, evidence state, action identity, and result.

Matched policies shared those case inputs and exogenous draws. Draws were keyed by case, event family, and index, so policy-induced events could not shift unrelated draws. This common-random-number design reduced computational noise without suppressing policy-induced path differences.

### 5.2 Policy designs

Table 2 compares five specified counterfactual interventions, not labels for historical Robodebt policies.

**Table 2**

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

Before inspecting core results, we froze policies, scenarios, seeds, outcomes, contrasts, and precision and analysis rules. This internal design freeze constrained result-driven tuning and supports reproduction; it was neither an external preregistration nor a basis for population inference. Implementation corrections and reruns are reported with validation in Section 5.5 and the evidence packet.

The core crossed five designed relationships, none a historical Robodebt estimate. Nominal initiation load `L` was 0.60, 0.95, or 1.20; with 80 cases, two reviewers, and mean service demand `s/2`, the initiation window was `Ns/(2kL)`. Realized review demand still depended on routing. Missing-evidence and access-barrier probabilities were each 0.10, 0.30, or 0.50. Retrieval success was 0.35 or 0.85. Partial staff access increased the uniform review-service scale from 10 to 15 days; complete access retained 10 days.

Keyed `U[0,1)` draws generated binary events and stochastic timings. The model retained the documented 21-day response deadline and used a 14-day review window. Prespecified simulation settings governed notice, assistance, extensions, retrieval, recovery, correction, reassessment, restoration, and the day-650 cutoff. Recovery and reassessment used fixed service demands; review and other stochastic timings used keyed variates. Complete values and binding receipts are in the frozen configuration and evidence packet.

The 108-family design used five policies and 30 paired replications: 16,200 core runs and 1,296,000 case-policy trajectories. Load was a designed input, not measured utilization or an estimated threshold. The frozen manifest fixed 3,240 family-replication seeds per suite.

Monte Carlo standard error (MCSE) targets were 0.05 for rates and 0.06 for paired differences. A miss after 30 replications would have extended every core cell to 60; none did. A separate 16,200-run sensitivity doubled retrieval-latency scale from 10 to 20 days without pooling with the core. Because retrieval still awaited return subject only to the distant administrative cutoff, this tests delayed routing and queue phasing—not acquisition failure, abandonment, or deadline expiry.

### 5.4 Outcomes and comparisons

Unsupported progression was executed progression outside the robust-permission set defined by the binary period-evidence specification or lacking required timely review authorization. Its rate, unresolved holding, modeled downstream exposure, and open-or-censored terminal-path rate used initiated cases as denominator. Gate safety used applicable configured gates and tested whether they blocked progression while prerequisites remained unmet. These definitions govern findings only inside the modeled workflow.

Administrative closure did not manufacture a terminal disposition. Conservative holds and supported downstream-exposure paths had no modeled terminal-resolution event, so they remained structurally open even when no queue extended to day 650. Complete restoration was observed or ruled out only on modeled correction-and-restoration paths following unsupported progression. The immutable field `right_censored_rate` therefore aggregates structural non-absorption with administrative censoring. Cross-policy terminal resolution is not comparable by construction.

The prespecified `review_effective_rate` divided timely pre-action completions by queued requests. Policies supplied surfacing, stopping authority, gate dependency, action binding, and recording; the rate did not vary or score those conditions. Partial staff access lengthened service rather than creating a separate visibility failure. We therefore call it **timely review completion**: the timing component, not validation of the full formal `ReviewEffective` construct. These operational measures are not legal judgments.

U3 queued review only for cases still unresolved after assistance and retrieval. Some replications therefore had no applicable review request, and the legacy metric encoded a zero denominator as `0.0`. Averaging those structural zeros would understate conditional performance. The prespecified applicable-metric set consequently excluded U3 gate safety and timely review completion. This avoids a biased confirmatory summary but leaves U3’s configured review path unevaluated; adding a denominator-aware estimand would require a new design freeze.

The interaction-event rate counted responses plus assistance requests per case. Its immutable legacy field name, `recipient_burden_rate`, does not measure effort, subjective burden, welfare, or cost. Agency workload counted completed assistance, retrieval requests, completed reviews, and completed reassessments per case. **Modeled downstream exposure** marked entry into the simulated external/recovery path. It could follow supported or unsupported progression and was not itself error or harm.

We report family-specific paired differences, 95% normal MCSE intervals, family ranges, and unweighted designed-family means. MCSE measures finite-run precision, not population, historical, or model uncertainty; cross-family means assume no real-world scenario distribution.

The service construct required a supported disposition by deadline, but its numerator counted every no-review case without checking disposition. We excluded all numerical service results and chose no substitute; repair requires a new version, freeze, and affected rerun.

### 5.5 Validation, controls, and claim boundary

Validation found one material defect: earlier certificates omitted coverage and action-identity fields required by the formal model. Freeze 3 added those fields and exact case-specific actions, retained the prior append-only attempts, and reran both suites. Hand traces, queues and timeouts, replay, configuration closure, adapter substitution, conservation, five negative controls, and routing/execution receipts then passed; all 32,400 attempts reconciled, representing 2,592,000 trajectories, and 182 automated checks passed. Cell summaries, paired estimates, precision results, and common-random-number diagnostics were unchanged; maximum MCSE was 0.04332 core and 0.04051 sensitivity. Detailed receipts, hashes, freeze administration, and execution totals remain in the reproducible package.

## 6. Results

### 6.1 Execution integrity, precision, and measurement audit

All 16,200 core and 16,200 sensitivity runs reconciled with no missing or unexpected identifiers. Three path states govern interpretation: a resolved path contains a modeled terminal-resolution event; structural non-absorption means the model supplies no such event; administrative censoring means observation ends before an available terminal event. The legacy terminal-path field combines the latter two. The measurement audit also excluded the invalid service measure without a post hoc substitute.

### 6.2 Fail-closed gate safety across tested load regimes

Under its configured rule, review with a fail-closed timeout (U2C) retained mean gate safety of 1.000 at nominal loads 0.60, 0.95, and 1.20. Across the other factors, timely review completion fell from 0.857 to 0.502 to 0.212, while unresolved holding rose from 0.143 to 0.498 to 0.788.

Fail-closed review thus kept automatic progression within the robust-permission set defined by the frozen binary period-evidence specification, retaining cases that review did not resolve in time. Gate safety is not timely service, and holding is not harmless: it defers action while leaving recipients and administrators in an open process.

Within the design, this pattern matches the prespecified expectation, but three loads do not locate a continuous threshold.

### 6.3 Fail-open timeouts convert review shortfall into progression

The paired fail-open-minus-fail-closed contrast (U2O−U2C) held cases, draws, and review machinery fixed while changing only the consequence of non-completion. Unsupported progression increased by an unweighted mean +0.476 across families (range +0.042 to +0.881); all 108 family MCSE intervals lay above zero.

Put operationally, unfinished reviews did not disappear. Fail closed left them as unresolved holds; fail open released them into progression after timeout. Timely-review completion was identical, while mean unresolved holding fell by 0.476 and unsupported progression and modeled downstream exposure each rose by 0.476; gate safety fell by the same amount.

The timeout rule, not better review, changed what non-completion did. The direction follows the declared policies; the simulation estimates how often it activated across designed families—0.042 to 0.881 of initiated cases—and traces the queue consequences. Exposure remains a downstream process state, not independent confirmation.

### 6.4 The information-first tradeoff

The planned information-first comparison could not answer the burden question as framed: the interaction proxy counted events rather than effort or welfare.

The valid comparison is narrow: both the information-first policy and conservative holding produced zero unsupported progression in all 108 families, but this does not establish terminal resolution, burden reduction, or overall superiority. The design named unresolved cases, but the prespecified output omitted that paired metric. Descriptively, unweighted designed-family mean unresolved-hold rates were 0.009 under information first and 0.766 under conservative holding: fewer action-stage holds, not a paired estimate or proven terminal resolution. U3 gate safety and timely review completion were excluded because review was conditional and zero-request replications were encoded as zero rather than not applicable. We therefore do not interpret those outputs; zero unsupported progression does not validate U3’s review mechanism.

Information first minus conservative holding increased interaction events by mean +1.096 per case (range +0.860 to +1.312) and workload events by +1.209 (+0.749 to +1.728); every family interval lay above zero. Because conservative holding generates none of the counted workload events, that direction follows from the metric and policy definitions; the simulation supplies magnitude and variation.

The paired modeled-downstream-exposure rate increased by an unweighted family mean +0.594 (range +0.369 to +0.815), with every interval above zero. Because both policies had zero unsupported progression, this reflects downstream movement that can follow supported action. Descriptively, the information-first policy combined fewer action-stage holds with more interactions, work, and downstream exposure while terminal paths remained open. Substantive burden therefore remains unresolved rather than rejected.

### 6.5 Censoring, validation contrast, and sensitivity

Every U0, U2C, and U3 family cell had an open-or-administratively-censored terminal-path rate of 1.000; unweighted designed-family means were 0.219 for U1 and 0.524 for U2O. For U0, U2C, and U3, the value is driven by missing terminal-resolution semantics, not simply observation ending at day 650. The simulation therefore cannot compare terminal disposition or complete restoration across all five policies. Earlier stage-specific outcomes remain interpretable within their horizons.

At the cutoff, unweighted designed-family mean shares of initiated cases remaining before modeled downstream exposure or on an open downstream-exposure path were 76.6% and 23.4% under conservative holding. The corresponding shares were 88.5% and 11.5% under fail-closed review, and 17.1% and 82.9% under the information-first policy. Impute and progress left 21.9% on the latter path. Fail-open review left 52.4% open, split between 40.9% before exposure and 11.5% on the downstream-exposure path. These classifications combine structural non-absorption with administrative censoring and imply neither resolution nor complete restoration; exact codes remain in the analysis artifacts.

Separately, the paired impute-and-progress minus conservative-hold validation contrast increased unsupported progression by mean +0.781 (range +0.578 to +0.914), with every interval above zero. It confirms benchmark activation, not a substantive discovery or recommendation.

Finally, with retrieval latency doubled, the information-first policy and conservative holding again had zero unsupported progression. Their paired unweighted designed-family mean differences were +1.098 interaction events per initiated case (+0.855 to +1.325), +1.209 workload events per initiated case (+0.748 to +1.724), and +0.595 in modeled-downstream-exposure rate (+0.370 to +0.824). Every family interval remained positive. This is stability to delayed routing and queue phasing, not to acquisition failure, abandonment, deadline expiry, or model uncertainty generally.

### 6.6 Synthesis

The simulation’s defensible contribution is activation frequency and designed-scenario variation, not rule direction or a capacity threshold. Its clearest demonstration is that identical timely-review-completion rates can coexist with opposite permission consequences. The third research question is only partly answered: timely supported service was invalidly measured, substantive burden was represented only by an interaction-event proxy, and structural non-absorption blocked terminal-resolution and complete-restoration comparisons.

Figure 3 visualizes the load response and the two principal paired-policy tradeoffs.

**Figure 3**

*Capacity, Timeout, and Information-First Tradeoffs*

![Figure 3. Capacity, timeout, and information-first tradeoffs.](figures/figure3_simulation_results.svg)

*Note.* The figure reports the frozen core simulation of 108 designed families with 30 paired replications per family. Panel A shows the fail-closed load response. Panels B and C show unweighted means and family ranges for the paired policy contrasts. Family ranges describe variation across designed scenarios, not uncertainty; Panel C labels its different outcome units explicitly.

Table 3 reports the prespecified paired estimates, computational-precision summaries, and claim boundaries underlying those contrasts.

**Table 3**

*Prespecified Paired Estimates, Computational Precision, and Claim Boundaries*

| Contrast | Outcome | Mean difference | Family range | MCSE range; intervals excluding zero | Claim note |
| --- | --- | ---: | ---: | ---: | :---: |
| U2O − U2C | Unsupported-progression rate | +0.476 | +0.042 to +0.881 | 0.009–0.043; 108/108 above | <sup>a</sup> |
| U2O − U2C | Gate-safety rate | −0.476 | −0.881 to −0.042 | 0.009–0.043; 108/108 below | <sup>a</sup> |
| U2O − U2C | Timely-review-completion rate | 0.000 | 0.000 to 0.000 | 0.000; 0/108 | <sup>a</sup> |
| U2O − U2C | Unresolved-hold rate | −0.476 | −0.881 to −0.042 | 0.009–0.043; 108/108 below | <sup>a</sup> |
| U2O − U2C | Modeled-downstream-exposure rate | +0.476 | +0.042 to +0.881 | 0.009–0.043; 108/108 above | <sup>b</sup> |
| U3 − U0 | Unsupported-progression rate | 0.000 | 0.000 to 0.000 | 0.000; 0/108 | <sup>c</sup> |
| U3 − U0 | Recipient interaction events per case | +1.096 | +0.860 to +1.312 | 0.012–0.024; 108/108 above | <sup>c</sup> |
| U3 − U0 | Agency-workload events per case | +1.209 | +0.749 to +1.728 | 0.011–0.027; 108/108 above | <sup>c</sup> |
| U3 − U0 | Modeled-downstream-exposure rate | +0.594 | +0.369 to +0.815 | 0.006–0.013; 108/108 above | <sup>b, c</sup> |
| U1 − U0 | Unsupported-progression rate | +0.781 | +0.578 to +0.914 | 0.004–0.011; 108/108 above | <sup>d</sup> |

*Note.* MCSE = Monte Carlo standard error. Differences are left policy minus right policy. Means and ranges are unweighted summaries over 108 deliberately designed scenario families. Each family estimate uses 30 paired replications. A family-specific computational-precision interval is the paired estimate ± 1.96 × MCSE; these intervals do not represent population, historical, or model uncertainty. The semantically invalid timely-supported-decision-service output is excluded. U3−U0 unresolved holding is absent because the prespecified output did not generate that paired estimand; U3 review metrics are excluded because zero-request replications lacked a denominator-aware value.

<sup>a</sup> Timeout directions follow the declared fail-open/fail-closed semantics; the simulation supplies magnitude and family variation. The policies used the same review queue, and fewer holds represent progression rather than established resolution. A fail-open release with unmet prerequisites is not gate-safe.

<sup>b</sup> Exposure is structurally downstream, may follow supported progression, and is neither independent confirmation nor proof of harm.

<sup>c</sup> Both policies prevented unsupported progression; interaction events do not measure effort, subjective burden, welfare, or cost, while the workload direction follows the metric and policy definitions.

<sup>d</sup> U1−U0 is implementation validation, not a substantive discovery or recommendation.

Taken together, the formal rule identifies what must be inspected, the documented application identifies where it appears in an institutional process, and the simulation shows why review must be tested under capacity and timeout conditions. Section 7 converts those lessons into a five-step protocol.

## 7. Process-Red-Team Protocol and Governance Implications

### 7.1 What the protocol produces

Usability is a design objective, not an evaluated result. Begin with one consequential action and trace representation, routing, review, execution, contestability, and restoration. Return separate findings, missing inputs, located transitions, interventions, owners, and tradeoffs—not an overall score. Use documents for structural findings, a deterministic trace for ordered events, and simulation when conclusions depend on timing or shared resources. A controlled pair changes only the named representation, rule, or intervention. If required inputs are unavailable, return `unassessable` and name them. The five steps below are a candidate article-level procedure for inspectable workflows; an optional appendix supplies implementation fields and worksheets.

### 7.2 Step 1: map transformations and ownership

For each handoff, record the source value and type—observed, derived, imputed, disputed, or missing—the transformation, assumptions, representation, provenance, and owner. Locate the first point where a policy-relevant distinction disappears or becomes unavailable to an empowered role. F0 tests evidentiary fidelity; F4 tests material surfacing. A broad label may fail by hiding imputation, conflict, lineage, or action-relevant scope. Repairs retain typed provenance, expose disputes, bind transformations to sources, and name the responsible interface or workflow owner.

### 7.3 Step 2: test what weaker evidence permits

Inventory exact progression, constraint, information, and restoration actions. For each automatic progression, record target, parameters, prerequisites, support, default, and timeout. F1 fails when weaker evidence permits an action excluded under any valid refinement; passage requires a certificate covering the declared set. F2 compares a fallback with holding it over every affected case, queue, resource, and deadline. Shared-resource effects require a system-level comparison. Repairs include narrower permission, evidence acquisition, reversible constraint, effective review, or fail-closed timeout.

### 7.4 Step 3: test whether review is operational

Decompose “human review”: Is a gate configured and blocking? Does an authorized reviewer receive material evidence and control the exact action? Does the workflow wait? Is authorization current at execution? Is a supported disposition reached by the service deadline?

Report `GateSafe`, `ReviewEffective`, F3, and `DecisionServiceEffective` separately. A fail-closed gate may be safe while service fails; completed review may be stale or nonbinding. With no gate, `GateSafe` is not applicable, although a required missing gate remains a failure. Locate defects in visibility, stopping authority, dependency, timing, execution-state revalidation, or capacity—not in the mere presence of a reviewer label.

### 7.5 Step 4: stress access, workload, and deadlines

Use the simplest adequate level: documents for timeout rules, traces for event order, queue calculations for simple capacity questions, and dynamic simulation for shared resources, feedback, or spillovers. If the question concerns a boundary rather than a sampled operating region, state how that boundary was located and with what resolution.

Stress access, evidence, arrivals, service demand, capacity, deadlines, and timeouts. Report gate safety, timely completion, unresolved cases, interaction events, workload, modeled downstream exposure, and restoration separately. Do not equate delay with safety, backlog reduction with resolution, or interaction events with subjective burden. Recommendations must identify improvement, deterioration, and what remains unmeasured.

### 7.6 Step 5: test contestability and restoration

Separate six questions hidden by “appeal available”: Does a structural path exist? Is access reliable? Was an opportunity available? Was it used? Did correction occur? Were all required consequences restored? Documents support structural findings; realized and timely conclusions require a trace or system model with declared horizons.

Declare the consequence vector and baseline before claiming restoration. Correcting a decision does not restore recovery status, time, access, or other consequences. Pending horizons are unassessable, not failed. Repairs may pause recovery, acquire evidence, reserve reassessment capacity, extend windows, and separate correction from restoration ownership. Keep costs and delays visible and name every omitted consequence.

### 7.7 Fixed Robodebt worked example

The worked pair makes the five steps concrete but remains explanatory, not representative. Step 1 locates the annual-total-to-fortnightly-imputation transformation and its ownership question. Step 2 names the actions enabled after nonresponse: debt calculation, debt notice, and recovery. Step 3 asks whether officer handling receives material evidence and binds those exact actions. Step 4 fixes a notice that does not reach the recipient before the 21-day deadline and tests that access event while holding the case, evidence, later evidence, process, clocks, resources, rules, and draws fixed. Step 5 separates reassessment from restoration of downstream exposure. Only the policy changes: impute and progress versus information first.

In the baseline, the fixed notice does not reach the recipient by the 21-day deadline. The deadline expires, and aggregate income becomes an imputed period representation without surfaced uncertainty. Unsupported modeled debt progression and downstream exposure follow; later correction leaves that exposure unrestored at the day-60 restoration check. The repair holds progression, obtains records, records a supported disposition, and avoids modeled downstream exposure. This trace does not establish that information first is costless, generally superior, or historically typical.

That trace matters because a local check might confirm that averaging ran as specified; another might confirm that notice issued. Neither establishes how failed access, imputation, deadline expiry, and the permission rule combine. It demonstrates that combination in this fixed example, but does not show that no other diagnostic could expose it.

An optional online technical appendix provides the detailed assessment profile, ownership and intervention receipt, evidence limits, statuses, and tradeoffs for readers implementing the protocol.

### 7.8 Governance interventions and transfer limits

The worked example also locates four intervention owners, but their controls are not interchangeable and their evidentiary status differs.

**Representation and interface owners:** preserve evidence state, provenance, and material disputes; the tradeoff is additional interface and record complexity.

**Information-service and policy owners:** evidence acquisition combined with holding is model-demonstrated; improved access and deadline extension are separate trace-supported proposals, not tested equivalents. Their tradeoffs are added interactions, workload, and delayed disposition.

**Gate and operational owners:** fail-closed timeout behavior is model-demonstrated. Reserved staff capacity, metered arrivals, and priority scheduling are unvalidated design proposals; their tradeoffs may include resource consumption, queue displacement, and unresolved holding.

**Recovery and restoration owners:** the documented enhanced OCI profile identifies recovery gating. Pausing external action during contest and repairing consequences beyond the decision record remain trace-supported proposals. Correction is not consequence-complete restoration; tradeoffs include deferred collection, prolonged open cases, and remediation outside the decision system.

Applied prospectively, this candidate procedure can examine a current AI deployment before rollout or a material workflow change: run matched representations of the same output—with and without provenance, alternatives, disputes, or temporal detail—through the actual downstream rules, then stress the resulting gate under expected and adverse load. This is an ex ante governance use, not evidence that contemporary deployments reproduce Robodebt.

## 8. Limitations and Conclusion

### 8.1 Limitations

The formal results are conditional. Robust permission depends on the declared set of admissible refinements, independently owned support rule, fully instantiated action identities, and ordering that separates progression from constraint, information acquisition, and restoration. An omitted refinement or misspecified support rule can change an assessment. These dependencies limit the conclusion to systems where those objects can be specified and inspected. Missing evidence or rules should produce `unassessable`, not an inferred pass. New domains require their own evaluation specification and refinement-coverage argument.

Likewise, the Robodebt application establishes documented structural relevance and compatibility with the proposed mechanism, not independent causation or numerical calibration. The selected sources, dates, and recorded precision limit the early and enhanced OCI profiles. Executable queue, engagement, retrieval, service, correction, and restoration values are stylized. Simulation rates therefore do not estimate historical Robodebt prevalence, capacity, delay, debt error, or causal effects. Historical quantification would require a separately sourced dataset, new measurement model, and new design freeze. The study supplies no monetary-entitlement oracle and makes no independent legal judgment.

The simulation adds four measurement limits. First, we excluded the decision-service output. Its numerator did not verify a supported disposition by the deadline, and repair requires a revised metric and affected rerun. Second, interaction events record responses and assistance requests, not evidence-production effort, psychological cost, welfare, or subjective burden. U3’s additional interactions therefore leave substantive burden unresolved. Third, the prespecified analysis emitted no paired correction or restoration estimand. Its legacy censoring field was 1.000 in every U0, U2C, and U3 family cell because those policies lacked modeled terminal-resolution events; it therefore combines structural non-absorption with administrative censoring. Earlier stage outcomes remain interpretable, but terminal resolution and complete restoration are not comparable across all policies. Fourth, MCSE measures finite-run precision only, while unweighted cross-family means imply no real-world scenario distribution.

Beyond measurement, the kernel represents declared rules, finite queues, deadlines, keyed exogenous variation, and modeled correction paths. It does not model reviewer psychology, discretion, deference to automated outputs, strategic adaptation, endogenous demand, adaptive staffing, priority rules, or organizational learning. Nor does it supply a single welfare measure. Gate safety, timeliness, unresolved holding, interaction events, agency workload, modeled downstream exposure, correction, and restoration remain separate outcomes. Because no welfare function combines them, the model cannot rank policies overall. Delay, deprivation, abandonment, queue displacement, and spillovers were not measured as terminal consequences. Consequence-complete comparison requires future evidence, including broader sensitivities or observed institutional traces.

Finally, the study provides a Robodebt worked trace but no practitioner study, usability validation, adoption evidence, or estimate of inter-rater agreement. The prospective AI application is therefore a candidate diagnostic, not evidence of field transfer or prevalence. Process susceptibility also does not prove historical attackability: inducibility, observability, repeatability, and actor benefit were not established.

### 8.2 Conclusion

The central question is what the workflow may newly do when a policy-material distinction is suppressed in representation, replaced by imputation, or left unresolved by missing period evidence. Under the declared refinement and support rules, weaker evidence cannot justify automatic progression unless the action remains independently supported across the admissible refinements. It may permit separately evaluated constraint, information-acquisition, or restoration actions without expanding automatic progression. This identifies functional permission and operational control in the evidence-to-action process; it does not locate legal or formal authority.

The deterministic representation pair first shows that suppressing a distinction in the representation of fixed evidence can change routing and automatic permission; it does not assess evidentiary refinement. The Robodebt application documents a different sequence, from aggregate income to imputed period values and action after nonresponse. The simulation then estimates how often unresolved or missing period evidence activates authored timeout consequences under load. Across three loads, fail-closed review preserved gate safety while timely review completion declined and unresolved holding increased. With review machinery and paired cases fixed, fail-open timeouts redirected non-completion into unsupported progression and modeled downstream exposure. The information-first policy also prevented unsupported progression but added interaction and agency-workload events and increased modeled downstream exposure relative to conservative holding; this exposure is a process state, not established error or harm. Its effect on substantive recipient burden remains unknown. These are designed-parameter-space results, not a historical capacity threshold or Robodebt reconstruction.

The study supports no single policy ranking. As a proposed governance principle, control depends on whether uncertainty remains visible, whether the gate binds the exact action, whether an empowered reviewer can act before timeout, what follows non-completion, and whether correction restores every modeled consequence. The invalid service measure blocks a timely-supported-service comparison, while structural non-absorption blocks cross-policy complete-restoration comparison. Fail-closed and information-first handling are permission-preserving within the demonstrated model, not established generally safer remedies: delay, deprivation, abandonment, queue displacement, spillovers, and consequence-complete welfare were not measured.

For organizations considering AI-generated classifications, recommendations, summaries, or agent actions, the conditional diagnostic implication is: testing model output is not enough. Organizations must also test what downstream systems permit when provenance, alternatives, disputes, or temporal detail disappear, and whether human control remains action-binding under actual workload and deadlines. The Robodebt application supplies a documented automated process in which to observe that structure; the claim of transfer to contemporary AI remains a proposed diagnostic, not field validation.

For process red teaming of inspectable workflows, the candidate diagnostic is compact: when evidence becomes weaker, what may the system now do; who can still stop it; and can they do so before the result becomes difficult to reverse? Answering those questions requires tracing evidence through representation, permission, capacity, action, and restoration. Treating that full chain—not the presence of a reviewer or the local correctness of one component—as the unit of governance is the article’s proposed principle.

## Data and Code Availability

The reproducible package is staged at https://github.com/etalbert102/uncertainty_permission_simulation with code, specifications, source manifest, receipts, analyses, and reproduction commands. On 20 November 2026, the repository was unavailable through logged-out public access. Public activation and a logged-out link check are required before submission; independent regeneration through that route therefore remains pending. The locally verified evidence packet records manifest and analysis hashes, commit-bound provenance, prior freezes, and append-only attempts. Historical documents remain with publishers or issuing institutions and are identified in the source manifest.

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
