# Goldfish Annotated Review Report

**Status:** Round 1 complete; no manuscript edits applied
**Review date:** 2026-11-19
**Target:** `docs/ARTICLE_MANUSCRIPT.md` (`full file`, lines 1–496; SHA-256 `73258d939ce24e7e60737cd0f2fd501dd1b46882c9e978c7ebb1bcd5f0265bfd`)
**Repository state reviewed:** commit `dd6df521c212f45978417f2e43c9f2003bed9271`
**Standard:** verified venue contract plus the call-grounded manuscript standard used for this review

## Reviewer Status

| Reviewer | Status | Primary lens |
| --- | --- | --- |
| Design critic | completed | formal-model, simulation, implementation, and source validity |
| Comprehension reviewer | completed | interdisciplinary clarity and self-containment |
| Structural reviewer | completed | architecture, hierarchy, exhibits, links, and package structure |
| Zoom-out reviewer | completed | contribution payoff, simplicity, novelty, and venue fit |
| Style reviewer | completed | claim calibration, prose, citations, and submission presentation |

All five reviewers operated in fresh contexts without the parent conversation, read their complete persona, the complete manuscript, the complete review standard, and the venue contract, and made no edits. The Elephant resolver rechecked the principal code, artifact, word-count, and repository-access findings before adjudication.

## Executive Verdict

**Disposition: major revision before submission, with two release blockers.**

The manuscript has a strong acceptance case: it is a substantially developed, venue-aligned article with a coherent formal rule, source-disciplined institutional application, executed simulation, transparent measurement exclusions, and a useful five-step governance protocol. The numerical claims sampled by the reviewers match the stored analyses, and no material Robodebt source contradiction was found.

The strongest rejection case is narrower and technical. The manuscript presents the simulation as using an independently owned, frozen, action-specific evaluation rule and at points interprets results through the formal robust-permission set. The confirmatory executable path stores only the opaque identifier `CONFIRMATORY-EVALUATION@1`; it does not bind or invoke the repository's general evaluation-specification and action-support machinery. Support is instead computed by the binary condition `adequate_response_evidence or retrieved_evidence`, plus timely review authorization where required. The resulting numbers are valid for that authored binary model, but the executable evidence does not support the stronger formal-to-simulation bridge currently described. The paper must either bind the specification and rerun or materially narrow that bridge.

The second blocker is operational rather than scientific: the repository remains private, and both URLs promised in the data-and-code statement return 404 publicly.

## Prioritized Findings & AI Suggestions

### G-01 — Executable evaluation specification does not support the claimed formal-to-simulation bridge

**Reviewer lenses:** Design critic; comprehension reviewer
**Severity:** Blocker
**Affected scope:** [Sections 3.3–3.6, 4.5, 5.1, 5.4, 6.2–6.3, and 8.2](docs/ARTICLE_MANUSCRIPT.md#L101)

**Discrepancy description.** The article says an independently owned evaluation specification supplies action-support rules, that policies and evaluation rules retain separate frozen owners, and that simulated unsupported progression is evaluated under the frozen rule. It then says fail-closed behavior kept automatic progression within the robust-permission set. In the confirmatory path, however, [`confirmatory.py`](src/uncertainty_permission_simulation/confirmatory.py#L190) passes only the string `CONFIRMATORY-EVALUATION@1`; [`configuration.py`](src/uncertainty_permission_simulation/configuration.py#L58) stores that ID but binds no specification object, support conditions, or refinement certificate. The general `action_support_membership` rule exists in [`rules.py`](src/uncertainty_permission_simulation/rules.py#L135) but is not called by the simulator. Instead, [`simulator.py`](src/uncertainty_permission_simulation/simulator.py#L798) sets evidence sufficiency to `adequate_response_evidence or retrieved_evidence`, and [`policies.py`](src/uncertainty_permission_simulation/policies.py#L177) combines that Boolean with review authorization.

The main text also never states this actual binary support criterion. A reader therefore cannot reconstruct the headline outcome from the article, while the executable record does not establish the stronger independent-specification claim.

**Rationale.** This is not a numerical error. It is an evidence-to-claim mismatch at the article's signature integration point. The frozen simulation supports conclusions about progression with or without its binary period-evidence prerequisite and review authorization. It does not demonstrate runtime evaluation against the general formal specification or certified robust-permission envelope.

***AI suggestion: PROPOSE FIX.***

**Proposed repair.** Choose one of two paths:

1. Preserve the strong integration claim by binding an immutable, content-addressed evaluation specification into compilation, invoking its action-support rule at action time, freezing the revised design, and rerunning affected artifacts; or
2. Preserve the existing run by stating the binary period-evidence and review-authorization rule explicitly, removing claims that the confirmatory simulation executes the general independent specification or directly establishes `P_robust` membership, and presenting the formal model and simulation as related but more weakly connected layers.

The second path is the bounded editorial route; the first is the stronger scientific route.

### G-02 — Public data-and-code links are not active

**Reviewer lenses:** Structural reviewer; style reviewer
**Severity:** Blocker
**Affected scope:** [Data and Code Availability](docs/ARTICLE_MANUSCRIPT.md#L428)

**Discrepancy description.** The GitHub repository is currently private. The repository URL and evidence-packet URL both return public 404 responses, while the manuscript promises public access before submission.

**Rationale.** This does not affect the study's scientific validity, but submission in the current state would contain dead links and fail the manuscript's own availability commitment.

***AI suggestion: PROPOSE FIX.***

**Proposed repair.** Before submission, make the intended repository public, test both exact URLs from a logged-out session, and change the statement from future to present tense. If public release will not occur, remove the dead links and state a truthful access procedure.

### G-03 — Research Question 2 overstates what was evaluated about review

**Reviewer lens:** Design critic
**Severity:** Major
**Affected scope:** [Research questions](docs/ARTICLE_MANUSCRIPT.md#L77), [outcomes](docs/ARTICLE_MANUSCRIPT.md#L229), [results](docs/ARTICLE_MANUSCRIPT.md#L259), and [protocol Step 3](docs/ARTICLE_MANUSCRIPT.md#L358)

**Discrepancy description.** Research Question 2 asks when a safeguard remains “gate-safe, effective, and timely under access and capacity constraints.” The simulation estimates configured gate safety and timely review completion. The other `ReviewEffective` conjuncts—surfacing, relevant evidence, reviewer authority, action binding, enforced dependency, and recording—are fixed assumptions or structural conditions, not varied or scored. “Partial staff access” lengthens service time rather than testing those access conditions. Timely supported service was invalidly measured and excluded.

**Rationale.** The manuscript acknowledges most of this in Methods, but the research question still implies a broader evaluation than the results provide.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Rewrite RQ2 around configured gate safety and timely review completion under the tested access/capacity conditions. State that the remaining effective-review conjuncts are held invariant and demonstrated only structurally or in deterministic fixtures.

### G-04 — U3's configured review path is excluded without explaining applicability and zero denominators

**Reviewer lens:** Design critic
**Severity:** Major
**Affected scope:** [Policy table](docs/ARTICLE_MANUSCRIPT.md#L197), [outcomes](docs/ARTICLE_MANUSCRIPT.md#L229), and [information-first results](docs/ARTICLE_MANUSCRIPT.md#L275)

**Discrepancy description.** U3 routes unresolved cases to fail-closed review, yet U3 gate-safety and review-completion outcomes are outside the frozen applicable set. The run artifacts contain those values, but the metric code maps zero denominators to `0.0`; averaging replications with no unresolved cases would understate conditional performance. Exclusion avoids reporting that biased summary but leaves U3's review mechanism unevaluated.

**Rationale.** Readers need to know why a configured gate is declared non-applicable and why “U3 avoided unsupported progression” does not imply demonstrated U3 gate or review performance.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Explain the prespecified applicability decision and zero-denominator issue in Section 5.4 or 6.4. Do not add a post hoc confirmatory estimate. Any new N/A-aware estimand would require a revised freeze and affected rerun.

### G-05 — “Right-censoring” obscures structural non-absorption

**Reviewer lens:** Design critic
**Severity:** Major
**Affected scope:** [Methods](docs/ARTICLE_MANUSCRIPT.md#L229), [measurement audit](docs/ARTICLE_MANUSCRIPT.md#L251), [censoring results](docs/ARTICLE_MANUSCRIPT.md#L285), and [limitations](docs/ARTICLE_MANUSCRIPT.md#L404)

**Discrepancy description.** Every U0, U2C, and U3 family cell has a rate of 1.000 because the kernel lacks terminal-resolution events for conservative holds and supported exposure paths; correction and restoration are modeled only after unsupported progression. The manuscript accurately says these rates include structurally open or unmodeled paths, but repeatedly naming the aggregate “right-censoring” can sound like an observation-window limitation rather than omitted absorbing-state semantics.

**Rationale.** Cross-policy terminal comparison is impossible by construction, and lower values under policies that generate unsupported action partly reflect the existence of remediation paths available only after that action. The dynamic restoration contribution is therefore narrower than the formal restoration semantics.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Use “structurally open or unmodeled terminal path” for the aggregate outcome and reserve “administrative right-censoring” for cases actually cut off at day 650. State directly that the dynamic design cannot compare terminal resolution across all five policies and models restoration only for selected unsupported-progression paths.

### G-06 — The surviving simulation payoff is narrower than the surrounding architecture

**Reviewer lenses:** Zoom-out reviewer; design critic; style reviewer
**Severity:** Major
**Affected scope:** [Contribution statement](docs/ARTICLE_MANUSCRIPT.md#L31), [simulation purpose](docs/ARTICLE_MANUSCRIPT.md#L189), [Results](docs/ARTICLE_MANUSCRIPT.md#L249), and [Conclusion](docs/ARTICLE_MANUSCRIPT.md#L416)

**Discrepancy description.** The most defensible dynamic contribution is valuable but compact: finite capacity determines how often non-completion activates a timeout rule, and the timeout rule determines whether that activation becomes holding or progression. Several other directions follow definitions; the supported-service measure failed; terminal resolution/restoration is unavailable for principal policies; U3 burden is unresolved; and three load points do not identify a threshold.

**Rationale.** The current manuscript is candid about each limit, but the combined architecture can still imply a broader completed dynamic contribution than survived measurement audit. The original plan's capacity-boundary ambition is not achieved.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Recenter the simulation contribution around timeout-activation frequency, load-dependent timely completion, designed-family variation, and the matched finding that identical completion can produce opposite permission consequences. Treat U3 as secondary and explicitly partial. Remove any remaining implication that the study located a threshold or completed a general service, correction, or restoration comparison.

### G-07 — Formal novelty and literature-wide separation are overstated

**Reviewer lenses:** Zoom-out reviewer; style reviewer; design critic
**Severity:** Major
**Affected scope:** [Literature and proposed integration](docs/ARTICLE_MANUSCRIPT.md#L67), [formal propositions](docs/ARTICLE_MANUSCRIPT.md#L123), and [Conclusion](docs/ARTICLE_MANUSCRIPT.md#L416)

**Discrepancy description.** Proposition 1 follows directly from defining robust permission as an intersection; Proposition 2 combines a non-bypassable gate, a simple capacity inequality, and authored timeout semantics. These are useful characterizations, but not deep standalone theorems. Separately, “adjacent work generally treats [the four elements] separately” is a literature-wide tendency claim that the non-systematic originality map cannot establish.

**Rationale.** The original contribution is the operational coupling of evidence refinement, independent support, action identity, automatic permission, timeout behavior, and restoration—not the mathematical depth of the component results or an absence claim about an entire literature.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Call the propositions formal characterizations or diagnostic results, remove the field-general premise, and state affirmatively: “This article couples four elements….” If comparison language remains, name the closest cited approaches and the exact element each does not address.

### G-08 — Emerging-technology fit is defensible but exposed to desk rejection

**Reviewer lens:** Zoom-out reviewer
**Severity:** Major
**Affected scope:** [Title and abstract](docs/ARTICLE_MANUSCRIPT.md#L1), [Introduction](docs/ARTICLE_MANUSCRIPT.md#L13), [Robodebt rationale](docs/ARTICLE_MANUSCRIPT.md#L131), [bounded transfer](docs/ARTICLE_MANUSCRIPT.md#L386), and [Conclusion](docs/ARTICLE_MANUSCRIPT.md#L416)

**Discrepancy description.** The only documented institutional application is a historical administrative process that is explicitly not contemporary AI. The direct AI example is author-constructed and unvalidated. This is honest and consistent with the formal transfer claim, but an editor could still read the article as a Robodebt governance paper with a hypothetical AI analogy. The title foregrounds review capacity, timeout rules, and Robodebt rather than robust permission and process red teaming; it can also suggest a historically calibrated Robodebt simulation.

**Rationale.** The paper satisfies the verified call methodologically, but its future-facing use is less evidentially developed than its historical testbed.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Make ex ante use in AI-enabled workflows the organizing frame before the case; say explicitly what Robodebt uniquely contributes that the formal model and synthetic run cannot; bring the LLM-summary counterpoint earlier; and consider a title led by robust permission/process red teaming rather than the case. Do not imply contemporary-AI field validation.

### G-09 — Readers need one map connecting the evidence layers and F0–F5

**Reviewer lenses:** Comprehension reviewer; zoom-out reviewer; structural reviewer
**Severity:** Major
**Affected scope:** [Completed research design](docs/ARTICLE_MANUSCRIPT.md#L27), [Formal Model](docs/ARTICLE_MANUSCRIPT.md#L83), [Protocol](docs/ARTICLE_MANUSCRIPT.md#L336), and [Conclusion](docs/ARTICLE_MANUSCRIPT.md#L416)

**Discrepancy description.** Readers must retain a road-object pair, two Robodebt profiles, a generic five-policy simulation, a Robodebt worked trace, and an LLM canary. The diagnostics appear as F0/F4, F1/F2, F3/F5, interleaved with named review/service constructs. No compact main-text map states what each evidence layer answers, what F0–F5 test, or what each cannot establish. The deterministic pair also disappears from the final conclusion.

**Rationale.** The parts are individually explained, but the article-level architecture is cognitively expensive and the conclusion does not fully close the four-layer design announced in the introduction.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Add a compact evidence-architecture/diagnostic table, adapted from the supplementary worksheet, with `Layer or diagnostic`, `Question`, `Evidence required`, and `Cannot establish`. Compress or relocate road-object details rather than adding net words. Restore one bounded sentence about the deterministic pair in the conclusion.

### G-10 — Repository vocabulary and policy naming impede a fresh reader

**Reviewer lenses:** Comprehension reviewer; style reviewer
**Severity:** Nit
**Affected scope:** [Sections 3.6, 4.5, 5–7](docs/ARTICLE_MANUSCRIPT.md#L123)

**Discrepancy description.** “Frozen receipt,” “separate frozen owners,” “append-only receipts,” and “transfer canary” are repository lifecycle terms rather than ordinary policy language. U3 shifts among “agency-assisted information first,” “information first,” and “information-first.” The first use can be read as a sentence fragment without “policy.”

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Prefer “prespecified analysis output,” “separately controlled inputs,” “immutable audit record,” and “author-constructed LLM-summary example.” Define **agency-assisted information-first policy (U3)** once and use “information-first policy” thereafter.

### G-11 — The evidence packet records a stale Figure 3 byte hash

**Reviewer lens:** Comprehension reviewer
**Severity:** Nit
**Affected scope:** [`EVIDENCE_PACKET.md` Figure 3 receipt](docs/EVIDENCE_PACKET.md#L174)

**Discrepancy description.** The packet records `16d4f7d5…ece1`; the committed `docs/figures/figure3_simulation_results.svg` hashes to `6b94f3de…492d`. The old value corresponds to an earlier rendering. The analysis JSON remains the numerical source of record, and no numerical discrepancy was found.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Update the packet to the current byte hash and distinguish the historical pre-APA renderer receipt in the execution ledger from the current publication exhibit.

### G-12 — The retrieval-latency sensitivity tests queue phasing, not acquisition failure

**Reviewer lens:** Design critic
**Severity:** Nit
**Affected scope:** [Sensitivity methods and results](docs/ARTICLE_MANUSCRIPT.md#L227)

**Discrepancy description.** Doubling retrieval latency does not add an acquisition deadline, abandonment condition, or service-window failure; routing waits for return subject to the distant administrative cutoff. Near-identical results therefore establish stability to delayed routing and queue phasing only.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Add one sentence stating exactly that scope and excluding evidence-acquisition failure, abandonment, and deadline-expiry robustness.

### G-13 — Two local presentation defects should be repaired

**Reviewer lenses:** Style reviewer; comprehension reviewer
**Severity:** Nit
**Affected scope:** [Conclusion](docs/ARTICLE_MANUSCRIPT.md#L420) and [Figure 2](docs/figures/figure2_robodebt_process_profiles.svg)

**Discrepancy description.** In the conclusion, “The information-first policy likewise prevented unsupported progression” follows a sentence about fail-open review, momentarily reversing the intended comparison. Figure 2 uses `EIC` and `CUPI` without expansion.

***AI suggestion: PROPOSE FIX.***

**Proposed edit.** Replace the conclusion clause with “Like fail-closed review, the information-first policy prevented unsupported progression….” Replace the unexplained figure acronyms with “later program variants” or expand them.

### G-14 — Broad caveat removal is not supported by the full review

**Reviewer lenses:** Structural reviewer; zoom-out reviewer; style reviewer
**Severity:** Nit
**Affected scope:** Abstract, methods, results, table notes, limitations, and conclusion

**Discrepancy description.** Two reviewers found the repeated exclusions defensive and costly under the 191-word margin. The style reviewer independently found that most repetitions protect a live inference at the point where readers could overgeneralize.

***AI suggestion: CONTEST.***

**Justification.** A broad deletion pass would weaken claim discipline. Selective compression is justified only where the same qualification appears twice at one inferential level or where a new architecture table can carry it without loss. Preserve the abstract, methods definition, primary results synthesis, table-specific notes, limitations, and conclusion boundaries.

### G-15 — Missing affiliation is not a verified call-compliance defect

**Reviewer lens:** Style reviewer
**Severity:** Nit
**Affected scope:** [Author block](docs/ARTICLE_MANUSCRIPT.md#L3)

**Discrepancy description.** The manuscript gives an author name and correspondence email but no affiliation or independent-researcher designation.

***AI suggestion: DECLINE.***

**Justification.** The verified venue contract contains no author-block or affiliation rule, and an employer affiliation cannot be inferred safely. Confirm the eventual submission form's anonymity and affiliation fields; add “Independent researcher” only if accurate and desired.

## Checks That Passed

- The conservative source count is 9,809 words before the bibliography, 191 below the verified ceiling.
- The reported run counts, family counts, paired-replication count, load-response values, principal contrasts, ranges, maximum MCSE values, sensitivity values, and censoring rates match the stored analyses sampled by reviewers.
- No substantive Robodebt source contradiction was found. The early/enhanced periods, notice clocks, averaging transition, repair bundle, evidence-access limits, and attributed collector-referral condition are bounded and source-supported.
- The article consistently rejects historical numerical calibration, independent legal judgment, monetary-error estimation, causal attribution to the proposed mechanism, field-transfer claims, and validated usability.
- Heading hierarchy, Markdown structure, two tables, three figures, callouts, local image links, reference order, and in-text/reference matching passed review.
- The visible author identity and correspondence email are present. The venue contract does not require an affiliation.
- The title, abstract, introduction, results, governance section, and conclusion generally describe the same bounded contribution.
- The article fits the call's permitted formal, simulation, case, institutional, and policy methods. Its venue risk is contribution payoff and contemporary-AI framing, not categorical ineligibility.

## Strongest Acceptance Case

The paper identifies a memorable workflow failure that model-centric evaluation misses: losing decision-relevant information can expand what a system automatically permits. It separates authority, support, permission, execution, review, service, correction, and restoration; grounds those distinctions in a documented institutional process; and uses a matched dynamic model to show that identical review completion can coexist with opposite permission consequences. The source and measurement discipline is unusually candid, and the five-step protocol gives organizations a concrete way to inspect AI-enabled workflows before rollout.

## Strongest Rejection Case

The paper's strongest integration claim outruns its executable implementation: the confirmatory model does not bind the independent evaluation specification described by the formal framework. Beyond that disconnect, several simulation directions are authored into policy semantics, the supported-service metric failed, principal policies lack terminal absorption, substantive burden and complete restoration remain unresolved, and the contemporary-AI case is only hypothetical. A skeptical editor could therefore see an elaborate formal and computational architecture producing a narrower stylized result than the title and near-10,000-word presentation imply.

## Recommended Resolution Order

1. Decide whether to rerun with a bound evaluation specification or narrow the formal-to-simulation claim to the existing binary evidence model.
2. Reframe RQ2, U3 applicability, structural non-absorption, and the simulation contribution around what the frozen execution actually supports.
3. Tighten formal novelty and literature-positioning claims.
4. Improve the evidence-layer/F0–F5 map and emerging-technology framing within the existing word budget.
5. Apply the local terminology, Figure 3 hash, sensitivity-scope, conclusion, and figure-acronym fixes.
6. Activate and verify the public repository immediately before submission.

No manuscript change should be applied until the project lead chooses the G-01 resolution path.
