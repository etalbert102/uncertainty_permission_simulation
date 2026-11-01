# Article Outline: When Uncertainty Expands Authority

Status: drafting blueprint; result statements remain placeholders until confirmatory analysis is complete

Working title: *When Uncertainty Expands Authority: Formalizing and Stress-Testing Automated Decision Workflows Through Robodebt*

Target: 10,000-word extended research paper for the Stanford CISAC/GTG volume *Emerging Technologies and the Future of Decision-Making*

Internal lineage source, not required reading: *When Uncertainty Expands Authority: How AI Workflows Can Reduce Scrutiny*

Drafting control: allocate 9,400 words to named sections and hold 600 words unassigned for counted abstract text, captions, transitions, qualifications, and reviewer-required clarification. The reserve is not an additional section and should not be spent merely to reach 10,000 words.

## Paper-Level Argument

### Central thesis

Uncertainty does not itself expand authority. Authority expands when a workflow converts weaker evidence into a representation, route, or timeout rule that permits consequential action with fewer effective safeguards. Preventing that failure requires more than accurate components or a nominal human-review step: the whole evidence-to-action process must preserve provenance, restrict automatic progression to actions robust across compatible refinements, surface material uncertainty to an authorized reviewer, and remain effective under realistic workload and timing constraints.

### Empirical-demonstration claim

Robodebt supplies a documented institutional process in which aggregate evidence, evidentiary transformation, notice and access, deadlines, automation, review, recovery, and later correction can be mapped onto the formal model. The simulation does not numerically reconstruct Robodebt. It uses source-anchored early and enhanced OCI process structures to test declared counterfactual governance designs across stylized conditions.

The Robodebt application provides a documented setting in which to examine the base uncertainty-to-permission mechanism and its organizational consequences. It does not establish that a strategic actor induced or exploited that mechanism, and the paper must not use process red-teaming as evidence of a historical adversarial attack.

### Expected contribution

The paper makes four contributions:

1. It replaces an intuitive “weaker evidence should not expand authority” rule with an explicit information order, action taxonomy, and robust-permission condition.
2. It uses a representation-preservation fixture to isolate how interface abstraction changes routing and permission while the underlying uncertain output remains fixed.
3. It distinguishes a configured review gate from gate safety, effective review, and timely decision service.
4. It combines counterfactual tracing with a validated finite-cohort discrete-event simulation of workload, access, evidence retrieval, timeout semantics, and restoration.

### Main-text argument contract

The article has three headline questions and three corresponding propositions. Full RQ1–RQ6 and F0–F5 mappings remain in the evidence packet, but they do not become separate competing narratives in the manuscript.

1. **Robust permission:** What may weaker evidence newly permit? Evidentiary fidelity, robust automatic-permission monotonicity, and safe fallbacks form one headline proposition.
2. **Operational review:** When does configured review remain gate-safe, effective, and timely under access and capacity constraints? Review, surfacing, and queue behavior form the second proposition.
3. **Contestability and restoration:** Which safeguards prevent or repair unsupported action without hiding delay, burden, exposure, or unresolved cases? Contestability and restoration form the third proposition.

H1–H3 provide the main quantitative narrative. H4–H5 and the remaining formal results are secondary evidence and move to the appendix unless one changes a headline conclusion.

### Protocol integrity contract

- Freeze the five steps, required inputs, `pass`/`fail`/`unassessable`/`not_applicable` outputs, diagnostic fields, held-out AI canary, and worked-trace selection rule before confirmatory results.
- Permit semantic revisions only before confirmatory freeze; record every change and reason. After results, allow editorial clarifications only unless a new freeze and rerun is performed.
- After freeze, quantitative results and examples may populate the protocol, but its semantic tests cannot change in response to favorable or inconvenient findings.
- Use a deterministic golden Robodebt trace selected before confirmatory execution. Do not claim it is statistically representative.

### Claim discipline

Until confirmatory results are frozen, use “the study tests,” “the model predicts,” or “the analysis will estimate,” never “the study shows.” Replace result placeholders only from stored analysis artifacts. Keep three claim types separate throughout:

- historical and legal claims come from authoritative sources;
- formal claims follow from declared definitions and assumptions; and
- quantitative claims come from the simulation and apply only to its declared parameter space.

## Abstract — 200–250 Words

Draft the abstract against the 600-word reserve until the venue confirms whether it counts toward the ceiling.

Draft last. Use six moves:

1. **Problem:** automated workflows can turn incomplete evidence into consequential action even when each component follows its local rule.
2. **Gap:** accuracy, calibration, transparency, and nominal human review do not establish that uncertainty remains operationally constraining.
3. **Method:** introduce the formal invariant, map it to early and enhanced Online Compliance Intervention (OCI) process profiles, and run a paired finite-cohort discrete-event simulation across evidence, access, workload, provenance, and review conditions.
4. **Primary findings:** insert one sentence each for the capacity boundary, fail-open/fail-closed contrast, and information-acquisition tradeoff after analysis.
5. **Interpretation:** state what the results establish for the declared model and what they do not establish about historical Robodebt outcomes.
6. **Contribution:** process red-teaming evaluates how evidence quality changes functional permission across an organization, not only how a component predicts.

Do not open the abstract with Robodebt, call the simulation empirical measurement of Robodebt, or report a weighted “best policy.”

## 1. Introduction: From Uncertainty to Functional Permission — 700 Words

### 1.1 The organizational failure mode — 170 words

- Open with the complete puzzle in standalone form: a defensible abstraction can remove the very distinction that would trigger caution.
- Move immediately from model output to the complete chain: evidence → representation → routing → review → action → restoration.
- State that local correctness can coexist with an unsafe process-level authority shift.
- Define “functional permission” in plain language before introducing notation later.

### 1.2 Why nominal safeguards are insufficient — 130 words

- Explain that provenance visibility, a review field, or a formal right to contest does not guarantee timely intervention.
- Introduce the key operational distinction: a gate may be configured, remain fail-closed, receive effective review, and deliver a timely supported decision—or fail at any one of those levels.

### 1.3 Research strategy and case selection — 160 words

- Describe the three connected layers: formal model, document-grounded Robodebt application, and dynamic simulation.
- Justify Robodebt as a documented rule-based administrative workflow with scaled evidence transformation, burden shifting, automation, review, and correction.
- State explicitly that Robodebt was not a modern generative-AI system and that the simulation is not a numerical reconstruction.
- Explain the contemporary emerging-technology connection in one sentence: AI-generated summaries, confidence abstractions, and cross-system routing can similarly determine whether material uncertainty reaches an authorized reviewer.

### 1.4 Contributions, questions, and results preview — 240 words

- State the theoretical, computational, and institutional contributions in one sentence each.
- Compress RQ1–RQ6 into three reader-facing questions:
  1. When may weaker evidence safely support automatic progression?
  2. When does a formal safeguard remain effective under access and capacity constraints?
  3. What governance interventions prevent unsupported action without hiding burden, delay, or unresolved cases?
- Insert a three-sentence findings preview after confirmatory analysis using plain language: the review-capacity boundary; fail-closed versus fail-open timeout behavior; and agency-assisted versus claimant-led evidence acquisition. Introduce policy IDs only in Section 5.
- End with the article roadmap.

Primary exhibit: **Figure 1, “The evidence-to-action chain and five-step process-red-team protocol.”** Show evidence, representation, routing, review, action, and restoration, with the five practitioner steps and plain-language diagnostic questions mapped to the relevant transitions. Define F0–F5 in Section 3 rather than requiring readers to decode formal IDs in the introduction.

## 2. From Workflow Uncertainty to a Testable Research Program — 800 Words

### 2.1 The mechanism and bounded hypothesis — 200 words

- State the full bounded hypothesis directly: holding underlying evidence or model output fixed, suppressing a policy-relevant alternative can reduce scrutiny and expand de facto permission.
- Preserve the three necessary conditions: defensible representation, hidden policy-relevant distinction, and downstream relaxation of a safeguard.
- Clarify that uncertainty may instead justify constraint, containment, or information-seeking action.
- Separate the base vulnerability from attackability: a strategic attack additionally requires inducibility, observability, repeatability, and benefit.
- State that Robodebt grounds the base vulnerability, not historical strategic exploitation.

### 2.2 Where existing assurance stops — 220 words

Organize the literature into three functional clusters rather than six cursory mini-reviews:

- prediction uncertainty, calibration, abstention, and uncertainty communication;
- human oversight, contestability, algorithmic administration, and administrative burden; and
- sociotechnical assurance, process safety, and adversarial red teaming.

Treat Anyabolu, Dubey, and Hattab's 2026 uncertainty-to-action binding framework as the closest neighboring formulation. Do not claim that this article originates binding uncertainty to oversight responses. Distinguish the present contribution through evidence refinement, independently supported automatic progression, finite-capacity operational review, restoration semantics, and the documented application.

The gap is not that these traditions ignore context or action composition. It is that the evidence-to-functional-permission mapping is rarely represented as this specific testable invariant whose operational review conditions can be stressed under load.

### 2.3 From hypothesis to full study — 250 words

- Identify what the bounded hypothesis alone cannot establish: a formal information relation, typed action model, operational review criteria, institutional application, and dynamic evidence under load.
- Devote 100–120 words to a self-contained hypothetical operations-center vignette: the same uncertain pickup-versus-armed-vehicle estimate is sent through either an uncertainty-preserving interface or a broad `vehicle` fallback while the underlying case, output, downstream rule, and process state remain fixed. Compare routing, scrutiny, review, and automatic permission, and include a no-change negative-control rule. Call this the **representation-preservation fixture**; keep repository ID `P0-Precursor` in internal artifacts and the supplement, not the manuscript.
- Explain the move from this fully stated defense vignette to a public-administration case without claiming domain equivalence.
- State the three-layer research logic explicitly: the fixture isolates the representation-induced causal mechanism; the formal invariant generalizes it to evidence refinement and automatic permission; and the dynamic simulation tests its operational consequences when evidence, access, workload, gates, and restoration vary.
- Define the general class: workflows in which incomplete or coarsened evidence can alter consequential permission.

### 2.4 Research questions and falsifiability — 130 words

- State only the three headline questions in the main text; map RQ1–RQ6 to them in the appendix or evidence packet.
- Separate three kinds of disconfirmation:
  - **mechanism:** representation or coarsening produces no permission or scrutiny change in an enabling case, or weaker evidence reliably increases safeguards;
  - **operational:** no review-capacity or timeout effect appears over a prespecified range demonstrably spanning the relevant service boundary; a null over an inadequate range is inconclusive rather than falsifying; and
  - **practical value:** the protocol detects or localizes no failure beyond component-local checks on prespecified positive and negative controls.

Internal drafting control: maintain the **lineage continuity matrix** at the end of this outline. It supports the claim audit and must not appear as a published exhibit or become required reading.

## 3. Formalizing Uncertainty, Authority, and Review — 1,250 Words

### 3.1 Evidence states and compatible refinements — 220 words

- Define latent state space `Theta`, evidence states `E`, compatible-state set `Gamma(e)`, and refinement relation.
- Require coarsening to be specified independently of the downstream permission result.
- Require a constructive refinement-coverage certificate and distinguish exact finite, symbolic exact, conservative-outer, and witness-search conclusions; witness search cannot establish universal pass.
- Use the annual-total versus fortnight-specific-income example as the running illustration.
- Explain why confidence scores alone do not define the information order.

### 3.2 Representation and evidentiary fidelity — 180 words

- Define `rho(e)` and the required types: observed, derived, imputed, disputed, and missing.
- State that `observed` means supplied by an identified source record, while entailment under assumptions is the test for a `derived` claim.
- State F0 and explain uncertainty laundering: unsupported detail may look precise even when its numeric aggregate remains consistent.
- Separate transformation fidelity from the downstream action it enables.

### 3.3 Formal authority, functional permission, and action — 180 words

- Distinguish formal authority `L(q)`, automatic functional permission `P_auto(e,q)`, and executed action `X(case,t)`.
- Distinguish the workflow's operational policy from the independently owned evaluation specification `sigma`, including its action-support, materiality, required-meaning and directional-correspondence, required intervention capability, F2 intervention/alignment, baseline, refinement-coverage, and action-comparison rules. Actual roles, authority possession, and event timing remain process facts.
- Introduce progression, constraint, information, and restoration actions.
- Define permission over fully instantiated action instances so changes in amount, target, scope, or timing cannot hide behind one action-type ID.
- Allow finite-explicit, symbolic-constraint, and ordered-family action sets, with no inferred closure rule.
- Define complete pre-event state and explain that support is reevaluated after every material evidence, process, time, policy, rule, or version change.
- Explain why consequential containment is not automatically an expansion of progression authority.

### 3.4 Robust permission and safe fallbacks — 220 words

- State F1: an automatic progression action allowed under weaker evidence must be independently supported under every certified admissible refinement; universal workflow permissiveness cannot self-certify.
- State F2: weaker evidence may introduce safe constraint or information-seeking actions only when a frozen execute-versus-explicit-hold pair over the complete intervention unit, aligned by branch-independent causal cuts under identical cohort membership and keyed exogenous inputs, shows it cannot release focal or spillover progression outside the envelope recomputed at the later action's pre-state. A case-local pair supports only a local claim unless a frozen noninterference certificate excludes shared-resource effects.
- Provide one satisfying example and one minimal counterexample.
- Make clear that the rule concerns automatic progression, not every action with an external effect.

### 3.5 Effective review, surfacing, and restoration — 220 words

- State F3–F5.
- Define configured gate, `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective` separately.
- Explain why notification, nonblocking review, fail-open timeout, or post-action correction does not establish effective prior review.
- Require review authorization to bind the exact action instance, evidence and rule versions, conditions, and expiry.
- Require the action to remain in the current post-review set and retain independent support at the execution pre-state, including any explicitly modeled discretionary override.
- Define F4 from independently evaluated materiality and require exact semantic identity, an independently justified versioned mapping, or forward entailment from surfaced semantics to required action-relevant meaning; reverse implication, overlap, workflow materiality, and display-text similarity are insufficient. Separate the capability and deadline required by `sigma` from the process evidence that an actual role possesses that capability in time.
- Separate structural path existence, prospective reliability, realized path availability, correction uptake, and restoration; apply frozen thresholds and horizons and do not fail unresolved pre-horizon cases.
- Define complete versus partial restoration.

### 3.6 Three headline propositions and simulation implications — 230 words

- Report the representation-preservation fixture first in plain language, without its internal repository ID and without treating its authored permissive route as an empirical discovery.
- Group the eight formal-result targets under three headline propositions: robust permission, operational review, and contestability/restoration.
- In the main text, state each proposition, its governing assumptions, its intuition, and one diagnostic example or counterexample. Give a proof sketch only where it is necessary to understand the result.
- Move complete proof sketches, additional satisfying cases and counterexamples, subordinate lemmas, and exhaustive boundary cases to Appendix A.
- End with observable implications: which event-trace patterns constitute F0–F5 failures.

Appendix table: **Table A1, “Formal properties and observable diagnostics.”** Columns: property, formal requirement, passing trace, failure trace, and primary metric. Summarize the usable diagnostic in Section 7 rather than repeating the full table in the main text.

Appendix candidates: complete notation table, full proof sketches, exhaustive finite counterexamples, and executable formal fixtures.

## 4. Robodebt as a Documented Process Application — 1,100 Words

### 4.1 Why this case is analytically useful — 120 words

- Define Online Compliance Intervention (OCI) on first use before using the acronym for the early and enhanced profiles.
- Justify selection by mechanism visibility, not notoriety alone.
- Name the documented links: aggregate income matching, request for period-specific evidence, response deadline, averaging, debt action, recovery, and later reassessment.

### 4.2 Scope, sources, and three-axis validity — 200 words

- Fix the early OCI period and the enhanced OCI repair profile using source-manifest dates.
- Identify the Royal Commission and Ombudsman as owners of historical and legal claims.
- State the distinction among evidentiary support, simulated operational outcomes, and source-attributed legal validity; note that monetary correctness is outside the model.
- Explain the provenance hierarchy: documented value, documented range, stylized range, sensitivity parameter.

### 4.3 Early OCI process profile — 280 words

- Trace roles, evidence, transitions, 21-day response rule, nonresponse path, income averaging, automatic debt action, recovery, and possible later correction.
- Identify exactly where aggregate evidence becomes apparent fortnightly precision.
- Map functional permission separately from source-attributed formal authority.
- Label every unresolved ambiguity instead of filling it with simulation assumptions.

### 4.4 Enhanced OCI repair profile — 180 words

- Describe the documented 28-day-from-receipt rule, strengthened delivery and contact, clearer averaging notice, assistance, and manual-intervention changes.
- Treat this as a distinct dated profile, not as proof that all defects were cured.
- Identify which F0–F5 conditions each repair plausibly addresses and which remain dependent on implementation or workload.

### 4.5 Formal crosswalk and inference limits — 220 words

- Map annual aggregate to `e_less`, period-specific records to `e_more`, income averaging to `rho(e_less)`, and debt/recovery to progression actions.
- Map hold, record acquisition, review, and reassessment to constraint, information, post-review, and restoration actions.
- Separate documented workflow structure from stylized service times, prevalence, and behavioral parameters.
- State why the case supports structural relevance but not simulation calibration to historical outcome rates.

### 4.6 Transition to experiment — 100 words

- Explain that the source record supplies the process skeleton; the simulation asks how alternative safeguards behave across declared conditions that the historical record does not numerically estimate.

Primary exhibit:

- **Figure 2, “Early and enhanced OCI evidence-to-action process maps.”** Use aligned lanes so repairs and unchanged transitions are visible.
- **Appendix Table B1, “Formal-model-to-Robodebt crosswalk and provenance.”** Include construct, process instantiation, source anchor, and documented/stylized status. Keep only the essential mappings in the main-text process map.

## 5. Dynamic Process-Red-Team Simulation — 1,200 Words

### 5.1 Design overview — 120 words

- Describe a paired, finite-cohort discrete-event simulation with a frozen initiation window and administrative cutoff.
- State that process mutations, not prose judgments, implement the red team.
- Begin with the representation-preservation fixture, then name the six dynamic perturbation families: evidence degradation, provenance laundering, administrative-access failure, load stress, gate mutation, and restoration mutation.
- Reiterate the inferential sequence: the fixed-output fixture identifies the representation mechanism, while the dynamic perturbations estimate how the generalized invariant behaves under organizational conditions; do not present every perturbation as another direct test of the fixed-output hypothesis.
- Clarify that red-team mutations establish structural susceptibility under declared conditions, not an actor's historical inducement, observation, repetition, or benefit.

### 5.2 Synthetic cases and endogenous engagement — 160 words

- Generate typed aggregate-only, period-specific, verified, missing, and disputed evidence states, and reveal support-changing records only through modeled evidence events.
- Explain that the independent evaluation specification scores action-specific support without a latent debt-amount oracle.
- Model delivery, access, comprehension, records, response effort, and extensions using shared latent traits and policy-specific mappings.

### 5.3 Historical fixtures and counterfactual policies — 260 words

- Identify R-OCI-Early and R-OCI-Enhanced as source-validation fixtures, not population estimators.
- Define U0, U1, U2C, U2O, and U3 in one compact paragraph or table.
- Emphasize the paired contrasts:
  - U2C versus U2O isolates timeout semantics under the same review system.
  - U3 versus U0 isolates agency-assisted evidence acquisition.
  - U1 is a failure benchmark, not a recommended policy.

### 5.4 Scenario design and estimands — 250 words

- Describe the five core factors and the nominal 108 validatable scenario families.
- State the common-random-number and keyed-draw design, including complete initial system-state capture, fixed cohort membership, branch-independent causal-event keys used to align divergent F2 traces without event-index matching, and finite event/microstep/depth bounds that turn livelock into an invalid run rather than favorable censoring.
- Identify H1–H3 as the complete main-text quantitative narrative, H4–H5 as secondary appendix results, and V1–V2 as validation expectations.
- Define primary estimands as paired policy differences and capacity-boundary surfaces, not global policy rankings.

### 5.5 Outcomes and analysis — 210 words

- Group outcomes into evidentiary/permission, organizational, and recovery/restoration families, with correction and censoring reported explicitly.
- Report configured review, gate safety, effective review, and decision service separately.
- Describe paired estimates, uncertainty intervals, Monte Carlo standard errors, interaction plots, and right-censoring reports.
- Reject a single weighted utility as primary; retain the safety-throughput-burden vector.

### 5.6 Validation, freezing, and interpretation — 200 words

- Summarize golden traces, limiting cases, analytical queue comparison, reference-simulator differential tests, conservation, deterministic replay, and keyed-draw invariance.
- State the pilot/freeze/confirmatory sequence and family-wide replication-extension rule.
- Reiterate that estimates apply to the declared model and ranges.

Primary table: **Table 1, “Policies, process mutations, and primary contrasts.”**

Appendix candidates: event schema, scenario-validity rules, full factor grid, parameter provenance, preregistration, seed manifest, validation receipts, and sensitivity specifications.

## 6. Results: Where Safeguards Hold and Fail — 1,850 Words

Do not draft quantitative conclusions until the confirmatory evidence packet is complete. Preserve null, adverse, and counterintuitive results.

### 6.1 Validation and run integrity — 150 words

- Report scenario/run completeness, excluded invalid configurations, replication counts, MCSE compliance, censoring, and all validation gates.
- State any deviations from the freeze before substantive results.

### 6.2 The review-capacity boundary — 400 words

- Answer H1 and RQ2.
- Show where U2C remains `GateSafe` while `ReviewEffective` or `DecisionServiceEffective` declines.
- Report unresolved holds, queue delay, and deadline expiry alongside unsupported-action rates.
- Interpret a null threshold or gradual boundary honestly if no sharp transition appears.

Primary exhibit: **Figure 3, “Capacity and timeout semantics.”** Use aligned panels: Panel A shows gate safety, effective review, and decision service across load; Panel B shows how the same queue pressure becomes holds under U2C and unsupported action under U2O.

### 6.3 Fail closed versus fail open — 350 words

- Answer H2.
- Compare U2C and U2O on identical cases, service requirements, evidence access, and staffing.
- Report robust-permission violations, action without period-specific support, and recovery exposure together with throughput and delay.
- Do not pool the policies or describe fail-closed delay as harmless.

Use Figure 3 Panel B rather than a separate exhibit.

### 6.4 Information acquisition and burden transfer — 350 words

- Answer H3.
- Compare U3 and U0 on recipient evidence effort, agency workload, supported disposition, delay, correction opportunity, and unresolved cases.
- Stratify by third-party retrievability and administrative-access barriers.
- Identify the conditions under which agency assistance improves support and the conditions under which it merely relocates the bottleneck.

Primary exhibit: **Figure 4, “U3–U0 tradeoffs across evidence retrievability and access barriers.”**

### 6.5 Secondary access and provenance results — 200 words

- Summarize only whether H4–H5 qualify a headline conclusion; move their full estimates and plots to the appendix.
- Distinguish nonresponse causes rather than treating all nonresponse as equivalent.
- Show whether complete provenance access changes reviewer opportunity even when formal gate and staffing are fixed.

### 6.6 Negative controls and sensitivity — 200 words

- Report V1–V2, matched negative controls, and only prespecified sensitivities.
- State whether representation changes without permission changes correctly avoid F1 violations.
- Identify which conclusions survive alternative queue disciplines, timing, retrieval, or reviewer assumptions.

### 6.7 Results synthesis — 200 words

- Answer the three headline questions in a compact claim/evidence matrix; retain the RQ1–RQ6 mapping in the evidence packet.
- Separate formal findings, simulated findings, and historical observations.
- State the strongest supported conclusion, the most important tradeoff, and the largest unresolved uncertainty.

Primary table: **Table 2, “Primary paired estimates, uncertainty, and claim boundaries.”** Each row must include estimand, contrast, estimate, interval, MCSE, scenario scope, and interpretation limit.

Appendix candidates: full scenario-family results, secondary outcomes, detailed censoring, all sensitivity plots, prespecified or reproducibly selected traces, and negative-control tables.

## 7. A Practical Process-Red-Team Protocol — 1,750 Words

This section is the paper's practical deliverable. It must be usable without the appendices or code while remaining traceable to the formal model and simulation results. Present the protocol as a repeatable diagnostic, not a universal compliance standard or a promise that every organization can run the full simulation. Its semantic steps and output classes are frozen before confirmatory results; result-dependent prose may illustrate but not redefine them.

### 7.1 What the protocol diagnoses — 220 words

- Define the target class: workflows that transform incomplete, uncertain, disputed, or aggregated evidence before permitting consequential action.
- Explain why a correct component output, compliant calculation, visible provenance field, or configured reviewer may still coexist with a process failure.
- State the protocol's unit of analysis: one evidence-to-action path, including representation, routing, review, action, and restoration.
- Introduce the three application levels: document audit for structural claims, bounded deterministic trace for case-specific temporal claims through a declared horizon, and dynamic system simulation for shared-resource, feedback, and capacity claims. State each level's minimum inputs, claim limits, and escalation trigger.
- Specify the common minimum inputs: process map, evidence types, permission rules, review dependencies, deadlines, roles, timeout behavior, and correction path.
- Require one typed assessment envelope at every step, with exactly one status—`pass`, `fail`, `unassessable`, or `not_applicable`—and separate `complete`, `incomplete`, or `invalid` completeness, plus any optional value, stable diagnostics, role-bound component results, and role-bound evaluated inputs. Apply the frozen scope declaration, validate what is needed to resolve a conditional antecedent, and then evaluate independently decidable conditions. Distinguish unknown scope, missing required input, invalid evaluation specification, and invalid aggregation. `not_applicable` requires an explicit scope exclusion or demonstrably false fully resolved antecedent; a sufficient known failure takes conjunctive truth precedence over an unknown component, while completeness preserves the unresolved material.
- Distinguish a formal assessment from `evaluation_state = omitted_by_claim_limit`: the latter records that the selected level cannot support an unattempted conclusion, receives no status, and names the required escalation.
- State the complete output: a non-composite profile of property/helper classifications, located transitions, evidence used, observable traces, stress tests, interventions, owners, tradeoffs, unresolved information, application level, and claim limits. Prohibit an overall workflow pass, compliance score, or weighted policy ranking.

Figure 1 overlays the five protocol steps on the evidence-to-action chain; do not add a separate protocol box.

### 7.2 Step 1: Map evidence transformations and ownership — 190 words

- Inventory what is observed, derived, imputed, disputed, or missing at every handoff; verify that observed claims are supplied by identified source records rather than merely inferable from other claims.
- Record which source, assumption, team, interface, and rule owns each transformation.
- Identify policy-relevant alternatives or missing distinctions that can disappear before routing.
- Test F0 and F4 using one ordinary case, one degraded-evidence case, and one provenance-suppressed case.
- Output: an evidence lineage and the first transition at which relevant uncertainty becomes unavailable.

### 7.3 Step 2: Test what weaker evidence newly permits — 190 words

- List automatic progression, constraint, information, and restoration actions separately.
- For every fully instantiated progression action permitted under a coarse state, ask whether the independent support rule permits it under every refinement denoted by a conclusion-valid certificate.
- Give the operational version in plain language: specify the support rule and exact, symbolic, conservative, or witness-search method before examining the workflow outcome; a validated counterexample can establish failure, but failure to find one through search cannot establish pass.
- Treat a fail-open timeout, default value, or missing-as-zero rule as an authority rule rather than a neutral implementation detail.
- Test F1 with a paired evidence counterfactual and F2 with fallback-versus-explicit-hold system traces under identical cohort membership and keyed exogenous inputs, aligned by branch-independent causal cuts rather than event index and recomputing support for focal and spillover cases at each material state.
- Output: the exact evidence-to-permission edge that is safe, unsupported, or unresolved.

### 7.4 Step 3: Verify that review is operationally effective — 240 words

- Identify who sees the case, what evidence and uncertainty they receive, what authority they hold, and whether the workflow actually waits for them.
- Measure configured review, gate safety, effective review, and timely decision service separately.
- Test missing evidence, missing authority, process suppression, deadline expiry, and fail-open timeout as distinct failure reasons.
- Require recorded decisions and overrides that bind the exact action instance, evidence and rule versions, conditions, and expiry; immediately before execution, verify both current post-review eligibility and independent support.
- Output: whether review prevents unsupported progression, merely labels it, or preserves safety while leaving cases unresolved.

### 7.5 Step 4: Stress access, workload, and deadlines — 240 words

- Vary evidence availability, notice delivery, administrative access, comprehension, initiation load, service capacity, and deadline rules.
- Use the simplest adequate method: hand traces for deterministic failures, queue calculations for simple capacity questions, and simulation when feedback, multiple queues, or endogenous response make static analysis insufficient.
- Require escalation from document audit to bounded deterministic trace when event order or realized completion matters, and from bounded trace to system simulation when shared queues, capacity, timeouts, or spillovers can change another case.
- Identify the boundary at which the declared control loses effective review or decision service.
- Report safety, delay, recipient burden, agency workload, and unresolved cases separately.
- Output: the operating region in which the safeguard remains effective and the overload behavior outside it.

### 7.6 Step 5: Test contestability and restoration — 190 words

- Follow the trace beyond the initial action through notice, appeal, reassessment, recovery, repayment, and correction where applicable.
- Ask separately whether a structural correction path exists, whether its prospective operational probability meets the frozen reliability threshold, whether it was available in the realized trace, whether it was invoked, and whether correction completed.
- Distinguish corrected decision state from complete restoration of monetary and other modeled consequences.
- Test delayed evidence, expired correction windows, reliability intervals that straddle the threshold, pre-horizon unresolved cases, and residual exposure after reversal.
- Output: whether the process is meaningfully contestable and what harm remains after correction.

### 7.7 Worked application: one fixed Robodebt trace — 240 words

- Walk one early-OCI-style case from annual income match through missing period-specific evidence, averaging, deadline, debt action, recovery exposure, and later reassessment.
- First show what component-local checks observe: aggregate consistency, execution of the programmed calculation, and presence of a notice or review field.
- Then apply the five steps to locate evidentiary laundering, permission expansion, ineffective review, deadline/load exposure, and incomplete restoration.
- Use the deterministic golden trace and paired repair path selected in Slice 0, before confirmatory output inspection. Do not substitute a more visually persuasive trace later.
- Do not call the example representative, present it as a typical historical case, or use invented historical frequencies.

Integrate the trace into Table 3 rather than creating a separate box.

### 7.8 From diagnosis to intervention and bounded transfer — 240 words

- Connect each failure to a mechanism-specific intervention: preserve provenance, restrict automatic progression, acquire evidence, enforce fail-closed dependency, add capacity or admission control, change deadlines, pause recovery, or strengthen restoration.
- Show the associated tradeoff rather than presenting interventions as costless.
- Assign an owner able to change representation, routing, gates, and timeout behavior together.
- Apply the frozen protocol in 100–150 main-text words to one held-out contemporary-AI canary: an LLM case summary that suppresses a conflicting record and changes routing. Introduce the case and its causal relevance from first principles. In the internal lineage audit, map it to the source essay's LLM-summary example; do not require the reader to consult that essay. The canary uses different vocabulary and is not used to tune the formal model or simulation.
- Treat the canary as a generalizability check, not a second empirical case or evidence of prevalence.
- Transfer the protocol only when consequential action, evidence transformation, cross-team routing, review dependency, and restoration have close analogues; do not imply current Services Australia systems reproduce Robodebt.

Primary table: **Table 3, “Five-step diagnostic applied to one fixed trace.”** Columns: step, property/helper, required input, `pass`/`fail`/`unassessable`/`not_applicable` rule, completeness, observable signal, fixed Robodebt-trace finding, intervention, owner, tradeoff, and claim limit. Add rows rather than combining incompatible statuses. This single display supplies the reusable diagnostic and worked example without creating an overall score.

Repository supplement: provide the compact F0–F5 glossary and ordered decision procedure, three-level intake and escalation worksheet, evidence-lineage worksheet, trace schema, stress-test template, staged P0, Robodebt, and AI-canary review inputs, reference profiles, the completed project-lead comprehensibility review, executable worked trace, and reproduction commands outside the article. The main text must still explain the complete five-step method.

## 8. Limitations and Conclusion — 750 Words

### 8.1 Limitations — 450 words

Address each boundary directly:

- **Formal scope:** results depend on the declared refinement set, action order, and review definition.
- **Case scope:** early and enhanced OCI profiles are bounded by source coverage and must not be blended with later variants.
- **Simulation scope:** synthetic cases and stylized parameters do not estimate historical frequencies, capacity, errors, debts, or harms.
- **Behavioral scope:** the model represents structural opportunity and endogenous engagement, not reviewer psychology, deference, or behavioral compression.
- **Legal scope:** the simulator does not determine lawfulness; legal conclusions remain source-attributed.
- **Normative scope:** separate outcome vectors expose but do not resolve value choices among safety, timeliness, burden, workload, and restoration.
- **External validity:** transfer to AI-enabled or national-security workflows requires evidence of the same institutional mechanism.
- **Adversarial scope:** the study tests a base vulnerability and structural susceptibility; it does not establish inducibility, observability, repeatability, benefit, or historical exploitation in Robodebt.
- **Research-design scope:** state any unresolved model sensitivity, censoring, source ambiguity, or precision failure.

For each limitation, say whether it narrows interpretation, motivates a sensitivity analysis, or requires future empirical work.

### 8.2 Conclusion — 300 words

- Return to the article's opening question: can weaker evidence relax safeguards before an authorized person can act?
- State the formal answer under the declared assumptions.
- State the simulation answer using only supported results and tradeoffs.
- Reaffirm that the study establishes a bounded vulnerability test while leaving actor-specific attackability as a separate evidentiary claim.
- Reiterate the institutional lesson: meaningful control is a property of the evidence-to-action process under load, not the presence of a model explanation or reviewer label.
- Close with the transferable test: when evidence becomes less decision-relevant, what may the system now do, who can still stop it, and can they do so before the consequence becomes difficult to restore?

## Exhibit Plan

| ID | Exhibit | Section | Evidence owner | Core or appendix |
| --- | --- | --- | --- | --- |
| Figure 1 | Evidence-to-action chain with plain-language diagnostics and five-step protocol overlay | 1 and 7 | formal specification and frozen protocol | core |
| Figure 2 | Early and enhanced OCI process maps | 4 | source manifest and process profiles | core |
| Table 1 | Policies, mutations, and primary contrasts | 5 | frozen policy and scenario specs | core |
| Figure 3 | Multipanel review-capacity boundary and fail-closed/fail-open contrast | 6 | confirmatory analysis artifacts | core |
| Figure 4 | Information-acquisition tradeoffs | 6 | confirmatory analysis artifacts | core |
| Table 2 | Primary paired estimates and boundaries | 6 | confirmatory analysis artifacts | core |
| Table 3 | Five-step diagnostic, fixed trace, intervention, and tradeoff | 7 | frozen protocol and prespecified golden trace | core |
| Drafting matrix | Lineage continuity audit | drafting audit | claim-boundary memo | repository only |
| Appendix Table A1 | Formal properties and observable diagnostics | appendix | formal specification and executable checks | appendix |
| Appendix Table B1 | Formal-to-Robodebt crosswalk and provenance | appendix | case-study crosswalk | appendix |
| Appendix A | Notation, propositions, proof sketches, and counterexamples | appendix | formal evidence packet | appendix |
| Appendix B | Source manifest, dated profiles, and inference limits | appendix | Robodebt source packet | appendix |
| Appendix C | Simulation schemas, parameters, validation, and freeze receipts | appendix | simulation evidence packet | appendix |
| Appendix D | Full results, controls, sensitivities, and prespecified or reproducibly selected traces | appendix | analysis evidence packet | appendix |
| Repository protocol | Worksheets, trace schema, checklist, and stress-test template | supplement | evidence packet | repository |
| Transfer canary | Held-out contemporary-AI workflow application | supplement | frozen protocol QA packet | repository |

The seven core exhibits are the ceiling, not a target to exceed. If the venue counts substantial table text against the word limit, move Table 1 to the appendix and retain its policy definitions in concise prose. Do not cut the process map, primary estimates, capacity/timeout visualization, protocol overlay, or fixed worked trace.

## Internal Lineage Continuity Matrix

| Source-essay element | Treatment in standalone paper | New test or evidence | Failure condition |
| --- | --- | --- | --- |
| Hold the uncertain model output fixed and vary only the interface representation | Preserve exactly in `P0-Precursor` before the Robodebt generalization | Paired uncertainty-preserving and broad-fallback traces plus no-change control | Fixture changes the underlying output, rule, or process state, or cannot represent the falsifier |
| Uncertainty can expand de facto authority through representation and routing | Retain but narrow to declared evidence orders and automatic progression | F0–F2, policy traces, permission metrics | Coarsening never changes permission in enabling cases |
| Workflow, not model output alone, allocates authority | Formalize across representation, routing, review, action, and restoration | F0–F5 diagnostics and perturbation families | Component checks detect every induced process failure |
| Broad fallback can remove a safeguard | Generalize to uncertainty-laundering representations | Evidentiary-fidelity fixtures and provenance mutations | Typed and untyped representations behave identically where routing can inspect type |
| Weaker evidence should not reduce scrutiny or expand consequential action | Refine into robust automatic-permission monotonicity plus safe-fallback allowance | Propositions, counterexamples, U-policy comparisons | Rule cannot distinguish progression from safe constraint/information action |
| Human review matters only when uncertainty is visible and intervention is possible | Extend with timing, authority, evidence, dependency, and recording requirements | U2C/U2O comparison and review-state metrics | Configured review remains effective across all tested overload and access conditions |
| The vulnerability becomes adversarial when an actor can induce, observe, repeat, and benefit | Preserve as a separate attackability layer, not an assumed property of Robodebt | Four claim-boundary fields and explicit non-claim | Paper equates red-team mutation or institutional failure with historical adversarial exploitation |
| Stress review under load | Execute as the primary dynamic simulation | H1–H2 and queue-boundary analysis | Load adds no insight beyond static policy semantics |
| Prefer information-seeking and reversible intervention | Test rather than assume | U3/U0 comparison and restoration metrics | Information acquisition only transfers burden or creates worse unresolved delay |
| Decision records should join representation, rules, interventions, and overrides | Convert to trace and provenance requirements | Event schema, replay, and artifact-source audit | Trace cannot identify the rule or evidence responsible for an action |
| LLM summaries can suppress conflicts without becoming literally false | Develop as the held-out contemporary-AI canary | Frozen protocol application in the main text and post-simulation project-lead review | Canary is omitted, tuned to the protocol, or presented as a second empirical case |

This matrix is a drafting control, not a results table. Update its status only from formal checks, source artifacts, or frozen simulation results.

## Drafting Sequence

1. Draft and version the five-step protocol, classification rules, AI canary, and deterministic trace-selection rule during Slice 0.
2. Draft Sections 2–4 from the internal lineage source, formal specification, and source packet, then remove any reader-facing dependence on the lineage source, internal artifact IDs, or unexplained defense context.
3. Validate executable fixture/reference agreement and review-input/reference separation before confirmatory freeze; freeze protocol version `1.0` with the scenario and analysis specifications.
4. Draft Section 5 only after the scenario and analysis specifications freeze.
5. Build the seven core exhibit shells with stable IDs before confirmatory execution.
6. Draft Section 6 directly from the evidence packet after run reconciliation and MCSE checks.
7. After Slice 5 analysis, have the project lead apply the frozen procedure to the staged P0, Robodebt, and AI-canary inputs; resolve editorial ambiguities, and require a new freeze and rerun for any semantic correction before drafting Section 7.
8. Draft Section 1, the abstract, and Section 8 last so every summary statement matches the actual findings.
9. Run the claim-to-evidence audit, lineage continuity audit, and standalone-reader audit before prose polish.

## Completion Check

The outline has been successfully converted into an article only when:

- the named sections remain near the 9,400-word drafting target, use of the 600-word contingency is recorded, and the complete manuscript remains below the verified venue ceiling without deleting formal assumptions, case boundaries, methods, primary results, or limitations;
- every historical and legal statement has a source-manifest anchor;
- every formal claim has assumptions and a proof, counterexample, or executable check;
- every quantitative claim points to a frozen run artifact and uncertainty statement;
- the results section reports nulls, tradeoffs, censoring, and negative controls;
- the introduction, abstract, results, and conclusion state the same findings at the same level of confidence;
- Robodebt is described as structural grounding rather than numeric reconstruction or modern-AI equivalence;
- the internal lineage audit records which source-essay claims are retained, refined, bounded, or rejected without appearing as reader-facing scaffolding;
- every section defines its problem, construct, fixture, and evidentiary boundary without requiring access to the short essay;
- the manuscript defines the representation-preservation fixture entirely in plain language; `P0-Precursor` remains an internal or supplementary artifact ID and does not appear in reader-facing prose;
- the article explicitly distinguishes the fixed-output representation test, the generalized formal invariant, and the dynamic organizational stress test without presenting them as interchangeable evidence;
- every acronym, formal-property label, hypothesis ID, and policy ID is defined before reader-facing use, and the abstract and introduction prefer plain-language contrasts;
- the protocol was frozen before confirmatory results, every pre-freeze revision is logged, and no result-dependent semantic change is hidden as prose editing;
- the project lead has completed the post-simulation comprehensibility review on the staged P0, fixed Robodebt trace, and synthetic AI canary inputs; every material ambiguity has a disposition, the review is not presented as independent validation, and every semantic correction received a new freeze and rerun;
- every protocol step yields `pass`, `fail`, `unassessable`, or `not_applicable`, and missing documentation never defaults to a pass or `not_applicable`;
- the worked trace follows the prespecified deterministic rule and is not described as representative;
- the main text contains no more than seven core exhibits;
- a reader can apply the five-step protocol and diagnostic table without opening the repository, while repository artifacts support deeper implementation; and
- no proposed analysis is written as a completed finding.
