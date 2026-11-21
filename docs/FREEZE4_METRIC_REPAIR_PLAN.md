# Freeze 4 Metric Repair and Rerun Plan

Status: recorded plan; not yet operative

Current scientific state: Freeze 3 remains active until Slice 4 of this plan is completed

## 1. Objective

Create a post-audit Freeze 4 that repairs measurement and reporting without changing the stochastic process. The completed article will center on the robust-permission rule, its action-specific Robodebt application, the five-step process-red-team protocol, and a bounded dynamic simulation showing timeout activation, queue performance, and the location of unresolved cases.

Freeze 4 is change control after inspection of Freeze 3 results. It is not a preregistration or an untouched confirmatory study. All Freeze 4 outputs must remain available even if the simulation is later demoted in the article.

## 2. Current Gap

The current article and analysis have five linked defects:

1. The fail-open-minus-fail-closed rows for unsupported progression, gate safety, unresolved holding, and modeled downstream exposure repeat the same timeout count with different signs or labels.
2. U3 conditional review and gate metrics encode zero-request replications as `0.0`, which confounds non-applicability with failure.
3. The action-stage hold measure omits evidence requests and cases still open before action, so it does not measure unresolved non-progression.
4. The aggregate recovery-exposure measure does not distinguish supported from unsupported entry.
5. `DecisionServiceEffective` lacks a valid supported-disposition numerator because the modeled state space does not contain a complete supported no-action outcome.

The active freeze and release machinery is also version-specific. Freeze creation, output discovery, parent-config validation, release verification, and tests currently assume Freeze 3, the V2 configuration identities, and the V2 output roots. Freeze 4 therefore requires a controlled infrastructure migration before any scientific rerun.

## 3. Scientific Invariants

Freeze 4 must preserve:

- policies U0 through U3;
- every queue discipline and transition rule;
- all capacities, deadlines, service times, and probabilities;
- the 108-family designed grid;
- cohort size and case membership;
- seed derivation and common random numbers;
- action-support rules and refinement certificates;
- the Robodebt application mapping;
- correction and restoration behavior; and
- the historical Freeze 3 manifest, compact outputs, and attestation chain.

No parameter, sensitivity, interaction, outcome, or policy branch may be introduced after result inspection to make the simulation more interesting.

## 4. Non-Goals

This plan will not:

- calibrate the simulation to historical Robodebt;
- estimate legal validity, monetary error, recipient harm, welfare, or overall policy value;
- locate an analytic queue-stability or capacity threshold;
- add abandonment, strategic behavior, adaptive staffing, priority optimization, or organizational learning;
- invent terminal resolution for conservative holds or open recovery paths;
- replace the current case-study source manifest with a general literature inventory;
- overwrite or delete Freeze 3 artifacts; or
- make the repository public without separate project-lead authorization.

## 5. Design Principles

1. **Change measurement, not behavior.** Metric and analysis code may change; event-generating policy and simulator behavior may not.
2. **One empirical quantity per accounting identity.** Complementary or sign-reversed consequences may be decomposed but not presented as independent findings.
3. **Non-applicability is not zero.** Conditional measures store their raw numerator and denominator and return `null` when the denominator is zero.
4. **Preserve weak results.** Core and sensitivity results remain in the evidence packet regardless of manuscript prominence.
5. **Separate decision, process, and consequence states.** Supported progression, unresolved non-progression, review performance, and recovery-path entry remain distinct.
6. **Fail visibly.** An unexpected event difference, incomplete state partition, or unverifiable historical freeze blocks continuation.

## 6. Fact Ownership and Dependency Map

| Fact or artifact | Owner | Downstream rule |
| --- | --- | --- |
| Policy behavior and action decisions | `policies.py` and frozen policy profiles | Metric and reporting code may inspect but not reinterpret or mutate behavior. |
| Event order, queue visits, and cutoff state | `simulator.py` | Freeze 4 expects exact semantic continuity with Freeze 3. |
| Raw metric numerators and state partitions | metric extraction layer | Analysis consumes stored counts; prose may not rederive them from displayed rates. |
| Conditional estimands and MCSE | confirmatory analysis layer | Figures and tables consume analysis receipts rather than recomputing statistics. |
| Freeze identity and frozen inventory | freeze machinery | Run, reconcile, analyze, and release gates consume the active manifest. |
| Historical case claims | Robodebt source manifest and application records | General literature additions do not enter this manifest unless they support a new historical claim. |
| Article wording and exhibit selection | manuscript and reporting layer | Editorial prominence cannot delete or mutate stored results. |

Dependency order:

`repair contract -> freeze-version infrastructure -> metric semantics -> pilot/report rehearsal -> Freeze 4 -> core and sensitivity runs -> differential audit -> scientific-value gate -> manuscript -> release packet`

## 7. Freeze 4 Metric Contract

### 7.1 Primary timeout result

The primary timeout quantity is:

`timeout_activation_rate = required reviews not completed by their action deadline / initiated cases`.

Fail-open progression, fail-closed holding, gate failure, and downstream entry are declared consequences of this activation. They may appear in an accounting decomposition, but they do not receive separate empirical-precision claims.

### 7.2 Decision-state partition

At cutoff, every initiated case belongs to exactly one state:

1. `supported_progression`;
2. `unsupported_progression`;
3. `evidence_requested`;
4. `held`; or
5. `pre_action_open`.

The five counts must sum exactly to the initiated cohort. Missing or multiple classification is fatal.

### 7.3 Primary U3 comparison

The sole aggregate U3-minus-U0 decision contrast is:

`unresolved_nonprogression = evidence_requested + held + pre_action_open`.

When unsupported progression is zero, supported progression is the complement of this quantity and does not receive a second inferential row.

### 7.4 Recovery-path entry

The analysis stores:

- `supported_recovery_entry`;
- `unsupported_recovery_entry`; and
- `no_recovery_entry_by_cutoff`.

These fields describe flow location. They are not independent confirmation of the decision-state contrast and do not imply harm, recovery completion, or restoration.

### 7.5 Conditional review and gate estimands

For each family-policy cell:

`conditional_timely_review = sum(timely_review_count across replications) / sum(review_request_count across replications)`.

The analysis stores total timely completions, total review requests, the number of zero-request replications, the conditional rate, and a delete-one-replication cluster-jackknife MCSE. This is a request-weighted estimand. If total requests equal zero, the rate and MCSE are `null`.

Conditional gate safety uses the same ratio-of-sums and cluster-jackknife rule with safe and applicable gate counts.

### 7.6 Retired primary constructs

`DecisionServiceEffective` is removed from Freeze 4 primary metrics and article claims. The present model cannot identify a complete supported no-action disposition, so substituting another numerator would not repair the construct. The formal concept remains available for future models and is explicitly marked unestimated here.

The aggregate legacy censoring rate is removed from primary reporting. Stage-aware open-path reasons remain in the supplement.

### 7.7 Prespecified designed-grid summaries

The grid is exactly balanced for the following unweighted summaries:

- U2C timeout activation by load: 36 families per level;
- U3 unresolved non-progression by access barrier: 36 families per level;
- U3 unresolved non-progression by retrievability: 54 families per level; and
- U3 unresolved non-progression by staff access: 54 families per level.

These are descriptions of the designed grid, not population effects or historical estimates. No additional interaction is promoted after the rerun.

## 8. Execution Protocol

Only one slice may be in progress. Every completed slice records changed files, intentionally untouched files, commands run, results, residual risk, and commit SHA in the canonical ledger in Section 9.

### Slice 0 — Record and validate the repair contract

**Scope:** establish this plan as the controlling implementation document.

**Owned files:** this plan and its ledger entry.

**Forbidden files:** all active freeze, configuration, runtime, analysis, output, and manuscript files.

**Expected changes:** validate exact estimands, factor aggregation, full-disclosure rule, stop conditions, and deferred-work policy.

**Verification:** Markdown structure inspection; repository diff check; comparison against current Freeze 3 status.

**Done when:** every new metric has a numerator, denominator, applicability rule, aggregation rule, precision rule, and claim boundary, and Freeze 3 remains active and untouched.

**Commit:** required.

### Slice 1 — Implement version-aware Freeze 4 infrastructure

**Scope:** migrate freeze and release machinery without changing scientific behavior.

**Owned files:** freeze machinery, configuration validation, release verification, stable configuration entrypoints, freeze tests, manifest attestation records, and execution ledger.

**Forbidden files:** policy decisions, event scheduling, random streams, evaluation specification, source fixtures, and result outputs.

**Expected changes:**

- preserve the active manifest exactly as `docs/FREEZE_MANIFEST_V3.json`;
- add Freeze 3 to the historical attestation ledger;
- advance the active identity to `UPS-CONFIRMATORY-FREEZE@4`;
- retain stable config filenames while advancing their internal core and sensitivity IDs;
- assign `outputs/confirmatory_v3` and `outputs/sensitivity_information_latency_v3`;
- update output-existence checks, parent-config validation, run/reconcile/analyze bindings, release verification, and tests; and
- leave V2 output roots untouched.

**Verification:** historical Freeze 3 manifest and commit binding; Freeze 4 candidate creation against empty V3 roots; negative tests for bad freeze ID, parent ID, output root, manifest hash, and attestation.

**Done when:** Freeze 3 verifies independently, the Freeze 4 candidate infrastructure recognizes only V3 roots as pre-run blockers, and all focused tests pass.

**Commit:** required.

### Slice 2 — Implement metrics and semantic QA

**Scope:** implement the metric contract without changing generated behavior.

**Owned files:** metric extraction, confirmatory aggregation, analysis schemas, and focused tests.

**Forbidden files:** policy behavior, event generation, queue scheduling, stochastic draws, action-support rules, and Robodebt-specific branches in generic code.

**Expected changes:** raw counts, five-state partition, recovery-entry partition, nullable conditional ratios, cluster jackknife, retired-primary-metric handling, and stable diagnostics.

**Golden cases:** zero review requests; one timely and one late review; completed unresolved review; supported versus unsupported recovery entry; pre-action open case; exact five-state conservation; complementary-result detection.

**Metamorphic checks:** case reordering; semantic policy-label substitution; duplicated cohort; irrelevant-event insertion.

**Adversarial checks:** missing or double classification; numerator above denominator; orphaned recovery entry; malformed null; zero applicable clusters.

**Done when:** focused and full tests pass, the partitions conserve every case, and no zero denominator becomes a substantive zero.

**Commit:** required.

### Slice 3 — Run a development pilot and reporting rehearsal

**Scope:** test the full analysis path before Freeze 4 issuance.

**Owned files:** development pilot configuration and receipts, analysis rehearsal, reporting builders, focused tests, and ledger.

**Forbidden files:** confirmatory or sensitivity output roots and article numerical claims.

**Expected changes:** validate ratio-of-sums, jackknife MCSE, factor margins, null propagation, accounting-identity detection, and draft exhibit schemas.

**Exhibit contract:**

- Figure 3A: timely review and timeout activation by load;
- Figure 3B: U0 and U3 decision-state decomposition;
- Figure 3C: U3 unresolved non-progression across the three declared organizational factors;
- Table 3: one timeout estimate, one U3 unresolved contrast, conditional review diagnostics, interaction-event counts, and workload-event counts; and
- recovery-entry flow, U1 validation, and latency detail in the supplement.

**Done when:** the pilot produces internally coherent output, no main-table row duplicates another algebraically, and the reporting builders consume analysis artifacts rather than prose constants.

**Commit:** required.

### Slice 4 — Issue Freeze 4

**Scope:** create the active immutable scientific manifest.

**Owned files:** active manifest, historical attestation ledger, freeze receipt, and execution ledger.

**Forbidden files:** any scientific input after the executable checkpoint commit.

**Procedure:** run all gates; commit reviewed executable inputs; confirm a clean tree; create Freeze 4; verify Freeze 3 and Freeze 4 independently; record identities and hashes.

**Stop conditions:** unverifiable Freeze 3; nonempty V3 roots; policy or transition drift; metric-contract mismatch; unexplained environment drift.

**Done when:** Freeze 4 verifies from a clean committed input state and the historical chain remains valid.

**Commit:** required.

### Slice 5 — Rerun core and latency sensitivity

**Scope:** execute both declared suites under Freeze 4.

**Expected volume:** 16,200 core attempts and 16,200 sensitivity attempts at 30 replications; 2,592,000 case-policy trajectories total. Expected initial runtime is approximately 22 minutes. Apply the frozen 30-to-60 replication rule if required.

**Procedure for each suite:** run; resume/replay; reconcile; analyze; verify append-only behavior and hashes.

**Done when:** both suites reconcile with no missing or unexpected attempt IDs, their analyses self-verify, and compact receipts bind them to Freeze 4.

**Commit:** compact results and receipts required. Large attempts follow the established artifact policy.

### Slice 6 — Perform the Freeze 3/4 differential audit

**Scope:** prove behavioral continuity and classify every permitted result difference.

**Expected exact matches:** cohort hashes, event hashes, action-support outcomes, unchanged valid metrics, and common-random-number identities.

**Expected differences:** new counts and partitions, denominator-corrected conditional measures, retired invalid metrics, and changed schema or artifact identities.

**Mismatch procedure:** classify identity-only serialization, event-detail, event-order, timestamp, action, queue, and outcome differences separately. Event-order, timestamp, action, queue, or substantive transition differences block release.

**Done when:** machine-readable and human-readable differential receipts account for every difference.

**Commit:** required.

### Slice 7 — Apply the scientific-value gate

**Scope:** decide article prominence without suppressing results.

The simulation retains a full results section only if:

- U3 unresolved non-progression varies by at least 0.05 across at least one prespecified organizational factor;
- the difference exceeds twice the relevant simulation-error scale; and
- the conditional-review denominator is large enough to interpret and is reported.

If the gate fails, demote the simulation to a short implementation illustration, state that the repaired analysis did not yield a sufficiently informative non-identity U3 result, preserve all results in the supplement, and remove dynamic simulation from the headline contribution or title.

No new parameter, sensitivity, interaction, or outcome may be introduced after this decision.

**Done when:** the decision, evidence, and manuscript consequence are recorded before prose revision.

**Commit:** required.

### Slice 8 — Reconstruct the manuscript

**Scope:** align the article with the repaired scientific product.

**Required changes:**

- present robust permission as a definition and operational test;
- replace formal characterizations with implications;
- state that aggregate-only debt calculation and the resulting debt notice fail F1 under the enhanced Robodebt profile, while the receipt-and-ignoring guard may constrain later collector referral without repairing upstream permission;
- explain that completed unresolved U3 review requests evidence;
- distinguish the paper from Lin et al., Wang and Rachev, Green, Rinta-Kahila et al., Carney, and Lykouris and Weng;
- remove the invalid service measure from the abstract and result claims;
- update research questions and the formal-to-simulation map to mark timely supported service unestimated;
- remove internal field names;
- retain the executable military fixture in the supplement while removing the armed-targeting narrative from the main article;
- report one timeout result and one U3 aggregate contrast;
- describe recovery-path entry directionally; and
- retain latency-sensitivity results in the supplement even if uninformative.

**Word target:** 9,500 to 9,750 words before references.

**Done when:** Markdown, exhibits, supplement, and APA Word export agree; the word ceiling holds; and rendered pages pass visual inspection.

**Commit:** required.

### Slice 9 — Complete the release audit

**Scope:** assemble the final evidence packet and submission-ready artifacts.

**Required packet:** this plan and completed ledger; archived Freeze 3 manifest; active Freeze 4 manifest; both reconciled Freeze 4 suites; differential receipts; semantic metric audit; scientific-value decision; full results; revised manuscript, figures, tables, supplement, and APA Word export; source and citation audit; manuscript-audit output; word count; test results; and release-gate output.

**Done when:** every reported number traces to Freeze 4, all limitations and deferred items are explicit, and the only remaining external action is any separately authorized repository-publicity step.

**Commit:** required.

## 9. Canonical Execution Ledger

This table is the sole status ledger for this plan. Do not create a second status table.

| Slice | Status | Entry condition | Completion evidence | Commit |
| --- | --- | --- | --- | --- |
| 0. Repair contract | pending | Plan recorded | Contract review and clean diff | — |
| 1. Freeze 4 infrastructure | pending | Slice 0 committed | Historical and candidate freeze tests | — |
| 2. Metric implementation | pending | Slice 1 committed | Golden, metamorphic, adversarial, and full tests | — |
| 3. Pilot and reporting rehearsal | pending | Slice 2 committed | Pilot receipt and exhibit-contract audit | — |
| 4. Freeze 4 issuance | pending | Slices 0–3 committed and clean | Active manifest and historical verification | — |
| 5. Core and sensitivity rerun | pending | Freeze 4 verifies | Run indexes, reconciliations, and analyses | — |
| 6. Differential audit | pending | Both suites complete | Machine and human differential receipts | — |
| 7. Scientific-value gate | pending | Differential audit passes | Recorded retain/demote decision | — |
| 8. Manuscript reconstruction | pending | Value decision recorded | Integrated Markdown, DOCX, exhibits, and QA | — |
| 9. Release audit | pending | Manuscript package complete | Final evidence packet and release verification | — |

Allowed statuses are `pending`, `in_progress`, `complete`, and `blocked`. Only one slice may be `in_progress`.

Each completion entry must record:

- files changed;
- files intentionally left unchanged;
- commands and gates run;
- result of each command;
- fixtures or comparisons used;
- residual risk;
- deferred items; and
- commit SHA.

## 10. Verification Tiers

| Tier | Purpose | Typical checks | Runtime target |
| --- | --- | --- | --- |
| Focused | Current bug class | metric, freeze, or analysis unit tests | under 10 seconds |
| Fast/default | Repository regression | `PYTHONPATH=src .venv/bin/python -m pytest -q` | under 2 minutes |
| Candidate | Pre-freeze integrity | plan, Slice 0, Slice 3, config, freeze, and release-candidate gates | under 10 minutes |
| Deep | Scientific execution | core or sensitivity run, replay, reconcile, analyze | approximately 11 minutes per 30-replication suite |
| Artifact | Reader-facing output | exhibit rebuild, Word export, render, visual inspection | under 20 minutes excluding manual inspection |
| Release | Complete package | `python3 scripts/verify_repo.py --release` plus manuscript audit | under 30 minutes excluding reruns |

## 11. Diagnostic Standard

New blocking diagnostics must include a stable code, owner module, family or artifact identity where applicable, concise reason, fatal or warning severity, artifact path, and next action. At minimum, the repair must distinguish:

- zero denominator from zero performance;
- missing classification from double classification;
- identity drift from behavioral event drift;
- historical output presence from active pre-run output contamination;
- algebraic complement from independent simulation result; and
- unresolved process location from terminal resolution.

## 12. Stop Conditions

Stop the current slice rather than continuing when:

- a targeted or full test fails;
- Freeze 3 cannot be verified;
- a V3 output exists before Freeze 4 issuance;
- policy, transition, queue, parameter, seed, or source behavior changes;
- the ledger is not updated;
- a metric lacks an explicit denominator or applicability rule;
- the state partition does not conserve the cohort;
- an event-hash mismatch remains unexplained;
- a result is added after the scientific-value gate; or
- a partial subsystem lacks a deferred-work entry.

## 13. Anti-Half-Done and Deferred-Work Policy

If a slice cannot complete a subsystem, choose exactly one:

1. finish it in the same slice;
2. remove the partial implementation; or
3. add a deferred-work record below with owner, reason, missing work, risk, and next action.

Vague TODO comments are not completion evidence.

### Deferred-work register

| ID | Owner | Reason | Missing work | Risk | Next action | Status |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | No deferred work recorded at plan creation | — | — | — | closed |

## 14. Red-Team and Generalizability Checks

- Confirm generic metric code contains no Robodebt identifiers.
- Confirm a semantically equivalent renamed policy fixture yields the same state partition.
- Confirm factor summaries use balanced designed cells rather than observed case frequency as population weights.
- Confirm complementary outcomes cannot both appear as independent primary findings.
- Confirm weak or null sensitivity results remain in the evidence packet.
- Confirm the value gate can demote the simulation without deleting its outputs.
- Confirm Freeze 3 can be reconstructed without the active Freeze 4 manifest.
- Confirm the paper remains intelligible if the supplement is unavailable.

## 15. Final Acceptance Criteria

The plan is complete only when:

- Freeze 3 and Freeze 4 verify independently;
- generated stochastic behavior is unchanged;
- zero denominators never become substantive zeros;
- every case belongs to exactly one decision state;
- core and latency sensitivity are both retained;
- Table 3 contains no algebraically duplicated findings;
- service effectiveness is no longer claimed as simulated;
- the enhanced Robodebt F1 result is explicit;
- weak or negative repaired findings remain disclosed;
- the simulation passes the value gate or is visibly demoted;
- the article remains below 10,000 words; and
- every reported number traces to a Freeze 4 artifact.

Repository activation remains a separate project-lead decision.
