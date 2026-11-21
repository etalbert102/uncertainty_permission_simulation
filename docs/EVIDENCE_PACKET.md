# Evidence Packet

Status: Slice 6 local submission candidate, updated 2026-11-21 after bounded audit repair

Study: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

This packet indexes the formal model, source-grounded application, executable validation, design freeze, corrected confirmatory runs, quantitative results, and integrated article. The first Goldfish review exposed a runtime gap between the declared evaluation specification and its implementation. The second exposed incomplete certificate-coverage metadata, action identity that was too coarse, ephemeral bridge receipts, and a freeze whose file contents needed explicit commit attestation. The repair uses an external content-addressed specification, coverage argument, exact case-specific action comparison, stored per-attempt receipts, and release verification of every result link. Freeze 3 and both complete 16,200-attempt suites were executed from clean committed inputs. Across the two suites, 2,592,000 routing receipts matched 2,592,000 action receipts with zero identity or result mismatches. Every cell summary, paired estimate, precision result, and common-random-number diagnostic exactly matches the preceding corrected run. A conservative whitespace-delimited source count places the revised article at 9,997 words before the bibliography after the bounded audit repair. The regenerated APA copy has 51 pages, all visually inspected. Public repository activation remains the only external release step. No reader study, usability claim, inter-rater claim, or practitioner-performance claim is supplied.

## 1. Scope and evidence rule

The study is a formal counterfactual simulation over a designed parameter space. Robodebt establishes structural relevance and supplies a documented application; it is not numerically reconstructed. The simulation does not estimate historical prevalence, monetary correctness, legal validity, population effects, unmodeled field causation, or attackability.

Evidence is interpreted in this order:

1. The freeze manifest identifies the prespecified source, design, executable, and environment artifacts.
2. Stored validation receipts establish implementation properties within their declared claim limits.
3. Reconciliation receipts establish run completeness.
4. Analysis receipts establish estimates and finite-run Monte Carlo precision.
5. Article prose may narrow those claims but may not enlarge them.

An internal self-hash is the canonical identity stored inside a JSON receipt after excluding its own hash field. A byte hash is the SHA-256 of the file as stored. They answer different questions and are labeled below.

### Slice 6 packet-coverage crosswalk

| Required component | Packet location and owner | Status |
| --- | --- | --- |
| Formal definitions and assumptions | Section 3; `FORMAL_MODEL.md` | present |
| Literature and originality | Section 3; `LITERATURE_AND_ORIGINALITY_MAP.md` | present; final update and comparison-language audit complete |
| Sourced process diagrams and model crosswalk | Section 3; `ROBODEBT_CASE_STUDY.md` | present |
| Simulator validation | Section 4; Slice 1/2, pilot, control, and worked-trace receipts | present |
| Scenario, seed, run, and exclusion inventory | Section 5 | present |
| Paired estimates and MCSE | Section 6; core and sensitivity analyses | present |
| Queue/effective-review boundary map | Section 6; stored capacity figure and three tested load points | present within tested points; no continuous threshold claim |
| Support, timeliness, workload, burden, exposure, correction, restoration | Sections 6-7 | present where valid; service excluded and terminal correction/restoration comparisons bounded by frozen output and censoring |
| Negative controls | Section 4 | present; 5/5 pass |
| Prespecified worked trace and selection rule | Sections 4 and 8 | present |
| Prespecified sensitivity | Sections 5-6 | present |
| Exact inspection and reproduction commands | Section 10 | present; planned packet CLI absent and disclosed |
| Limitations and claim boundary | Sections 1, 7-8, and 12 | present |
| Claim-to-proposition/source/exhibit/trace/limitation map | Section 6 | present |
| Precursor continuity | Section 9; `CONTINUITY_AND_CLAIM_BOUNDARY.md` | present |
| Author editorial pass | Sections 8-9; protocol/governance draft | present as ordinary editing, not formal review evidence |
| Self-contained five-step protocol, Robodebt trace, and AI canary | Section 8; protocol/governance draft and stored fixtures | present in drafted Section 7 |
| Complete integrated manuscript and consistent headline findings | Section 9 | present; source, integration, and APA-format review complete |
| Goldfish review resolution | Sections 1-12; `GOLDFISH_RESOLUTION.md` | all scientific and presentation findings resolved; public activation remains project-lead controlled |
| Evaluation-specification correction and exact-rerun comparison | Section 2; `EVALUATION_SPECIFICATION_CORRECTION.md` | present; executable bridge closed and all reported estimates unchanged |

## 2. Freeze and repository identity

| Item | Stored identity or value | Evidence |
| --- | --- | --- |
| Freeze ID | `UPS-CONFIRMATORY-FREEZE@3` | `FREEZE_MANIFEST.json` |
| Freeze manifest self-hash | `47170f8cb450709b19f0bf47b48b887208ee75cde07dbf1ee34169891f6b9c6b` | [Freeze manifest](FREEZE_MANIFEST.json) |
| Frozen repository head | `dc96716c0865517ab0f61700fb0a06ca39d0042a` | clean committed inputs bound by `repository_head_at_creation` |
| Freeze time | `2026-11-20T16:04:30.207544+00:00` | manifest |
| Frozen file inventory | 79 files; inventory-path hash `296d603f57879919ccb8aa4a3b6065052a8465733049f20eb9aa7cb1e5719aa4` | manifest |
| Source inventory | 10 selected sources, retrieved through 2026-10-31; source-manifest hash `fff48f4a818f29cd7ea5e7168c877c6697cd287a0714c2147b436814c2d87500` | manifest and [source manifest](../data/sources/robodebt/source_manifest.yaml) |
| Frozen runtime | CPython 3.14.4, macOS 26.5.2 arm64 | manifest |
| Packet assembly head | `fc2c6966a9fcf5b9ed9740e3c5067426dc51e8f1` | `git rev-parse HEAD` before this packet was added |

The source manifest records official URLs, publication metadata, local record hashes, and citation locators. Remote source bytes were not archived or byte-hashed at freeze; the manifest records `remote_byte_hash: null` and `http_outcome_at_freeze: not_rechecked`. Historical claims must therefore be checked against the cited official locator, not treated as vendored-source reproduction.

The original manifest and the second bridge manifest are preserved as `FREEZE_MANIFEST_PRE_EVALUATION_BRIDGE.json` and `FREEZE_MANIFEST_EVALUATION_BRIDGE_V2.json`. The original attempts are retained locally under `outputs/archive_pre_evaluation_bridge/`. The second manifest's creation-head field recorded a dirty-worktree HEAD rather than the commit containing its exact frozen bytes; `FREEZE_COMMIT_ATTESTATIONS.json` relabels that field and machine-checkably binds all 77 blobs to commit `74d657e42a60c28f7ab2675d8934cd11b2afd1e9`. Freeze 3 refuses dirty creation and verifies every manifest blob against its recorded commit.

The auditable defect, repair, rerun identities, and field-by-field equality result are summarized in [Evaluation-Specification Correction Receipt](EVALUATION_SPECIFICATION_CORRECTION.md).

### Release evidence packaging

The release candidate includes the two compact run indexes, reconciliations, analysis receipts, and four analysis SVGs under `outputs/`. Together they are approximately 7.6 MB and make the run inventory, estimates, precision, and derived plots inspectable without rerunning 32,400 attempts. The 32,400 per-attempt JSON files remain ignored (approximately 134 MB locally). Each run-index entry retains the attempt ID and hash; full attempt-level replay requires either the separately retained local/archive set or regeneration from the frozen runner. This boundary keeps the repository evidence-bearing without misrepresenting a summary receipt as raw data.

| Packaged artifact | File SHA-256 |
| --- | --- |
| Core run index | `edaec2fb9397e3edb36f19085487a67372382e0b8659b3fa6442f1ac4277f9c7` |
| Core reconciliation | `fac09612d80d9d62b32826daa1ae8c82b8ebbd369e24fd82ca106f77dbbc4af3` |
| Core analysis | `343784fad87713de810e84c8b7fa66449d3d5f54a659ebd5fd2114a16d4a9dab` |
| Core capacity/timeout SVG | `d4ecc9c52ad16b758498c3e718f700a5cb225fde58dfcb05d38468aa2de018f9` |
| Core information-tradeoff SVG | `fd8b122c9ca5932217e424575ac1faf0ca26b6cc503a1b81a810bd42214fbc83` |
| Sensitivity run index | `02ff9c984fece6f62dee059a9a76f7b81ce54335127e86b9a8a4505087c35dea` |
| Sensitivity reconciliation | `cd27f3b67a885e3908352c17a9da68d9ec5adce3b0304be1dbb57562e7323810` |
| Sensitivity analysis | `49685548ed78016aa2d26699fca6d03895dae03556509f7a9a34da4daa64a99b` |
| Sensitivity capacity/timeout SVG | `22f52e37eec54f33fa56e791ea0ed85f47a2afdc14370a77dd220b6e059d6a5c` |
| Sensitivity information-tradeoff SVG | `76f25bfd8f4ac4f104ae61951c01cdbf4a8ff57405f3c633c8f11dcc67429062` |

## 3. Formal, historical, and continuity record

| Function | Primary artifact | Frozen byte hash or current byte hash | Claim limit |
| --- | --- | --- | --- |
| Formal definitions, assumptions, F0-F5, and propositions | [Formal model](FORMAL_MODEL.md) | `27c93a090b6811def20c6618f719d255b60970aaf73b26ff6c1bf3cba996a7e3` | Formal results hold only under stated definitions, assumptions, and refinement set. |
| P0 representation-preservation comparison | [Precursor fidelity fixture](PRECURSOR_FIDELITY_FIXTURE.md) | `0b30ded91efd84e36d4e8da08fbe1c45bde4b03bcdf32a4cd362e83c58ac7d04` | Controlled formal/trace fixture, not an empirical interface study. |
| Five-step process-red-team method | [Protocol](PROCESS_RED_TEAM_PROTOCOL.md) | `ba2f845e2025545dadbe4f6d48db1c5c9313cd1b78c78118419d4dd85e64f4a3` | Inspectable method, not validated usability or practitioner performance. |
| Robodebt process history and formal crosswalk | [Case study](ROBODEBT_CASE_STUDY.md) | `d451a24a795849fcb3f13fcc522288cbced5957a30a4d427edc91f449302fc9d` | Source-grounded structural application, not numerical reconstruction or independent legal conclusion. |
| Early and enhanced profiles | [Early profile](../data/sources/robodebt/r_oci_early.yaml); [enhanced profile](../data/sources/robodebt/r_oci_enhanced.yaml) | `248211b2...e720a`; `c9e2df36...14e1` | Separately dated profiles; mixed-precision chronology remains explicit. |
| Literature/originality map | [Literature map](LITERATURE_AND_ORIGINALITY_MAP.md) | current byte hash `667ff0490c8c97ddf28d02cd5c93c814bddea8dd5f0f90bc6f312fac0e06a291` | Structured scoping map, not a systematic review; final update complete. |
| Precursor continuity and standalone boundary | [Continuity control](CONTINUITY_AND_CLAIM_BOUNDARY.md) | `448dbd056c00de911108d284d40018dd774bf4ac430e8ac1e632a7e914b1e608` | Internal drafting control; published article must stand alone. |
| Worked-trace selection | [Selection rule](WORKED_TRACE_SELECTION.md) | `5b4640979dfbbd2b7f29b63116bc4fdc157c8978b7a606e4d092484cce3885d2` | Explanatory fixed trace, not representative sampling. |

The paper separates three claim classes: formal consequences of declared definitions; simulated operational outcomes in the designed parameter space; and source-attributed historical or legal statements. Monetary correctness is outside all three.

Source-metadata correction note: the frozen `OMB-APPORTIONMENT-2023` manifest entry uses “Income Apportionment—Lawfulness of Income Apportionment Decisions” as a shorthand title. The issuing document's displayed title is *Lessons in Lawfulness: Own Motion Investigation into Services Australia’s and the Department of Social Services’ Response to the Question of the Lawfulness of Income Apportionment before 7 December 2020*, which the article now uses. The source identity, issuing body, date, URL, locator, permitted use, and terminology-boundary claim are unchanged. Because `source_manifest.yaml` belongs to the immutable 77-file scientific inventory, this post-freeze bibliographic correction is carried in the current evidence packet rather than silently rewriting the frozen input.

### Formal assumption summary

| Formal result or construct | Load-bearing assumptions | Evidence owner |
| --- | --- | --- |
| Information ordering and refinement | The compatible-refinement relation has a sound frozen coverage certificate and is defined independently of the downstream permission result. | `FORMAL_MODEL.md`, Information States and Compatible Refinements |
| Proposition 1: robust permission | Process state, time, policy, representation and decision rules, baseline, and action taxonomy are held fixed; the evaluation specification is valid and independent; action identity, support, and permission are total and inspectable. | `FORMAL_MODEL.md`, Headline Proposition 1 |
| Proposition 2: operational review | Event ordering is deterministic; fail-closed gates cannot be bypassed; review demand and finite capacity are declared; deadlines and timeout semantics are explicit. | `FORMAL_MODEL.md`, Headline Proposition 2 |
| Proposition 3: contestability/restoration | Process graph, correction transitions, deadlines, reliability and interval rules, consequence dimensions, obligations, and baseline values are declared before evaluation. | `FORMAL_MODEL.md`, Headline Proposition 3 |
| Executable F0-F5 assessment | Applicability, required inputs, evaluation rules, evidence references, completeness, and diagnostic aggregation follow the frozen property contracts. | `FORMAL_MODEL.md`, Executable Diagnostic Contract; `PROCESS_RED_TEAM_PROTOCOL.md` |
| Dynamic estimates | Cases and exogenous draws are paired within family/replication; queue and timeout rules are those frozen in the configs; scenario factors are stylized; the day-650 cutoff and right-censoring rules apply. | experiment configs, freeze manifest, and analysis receipts |
| Cross-family summaries | Families receive equal weight because no real-world scenario distribution is claimed. | methods/results draft and analysis receipts |

### Sourced process-map and model-crosswalk ownership

The [Robodebt case study](ROBODEBT_CASE_STUDY.md#source-anchored-process-maps) contains separate Mermaid process diagrams for Early OCI and the early-2017 repair bundle. Each node carries a Royal Commission process-map or Commonwealth Ombudsman locator. Its [early-to-enhanced change crosswalk](ROBODEBT_CASE_STUDY.md#early-to-enhanced-change-crosswalk) maps access, notice, deadlines, manual routing, evidence acquisition, provisional results, and collection referral to sources and formal relevance. Its [formal-model crosswalk](ROBODEBT_CASE_STUDY.md#formal-model-crosswalk) maps the documented application to `e_less`, `e_more`, transformation, authority, functional permission, gates, review, contestability, and restoration.

These diagrams own topology and documented transition meaning only. They do not own probabilities, queue disciplines, capacity, effect sizes, or formal conclusions. The scenario overlay and generic kernel own those separate facts.

## 4. Validation and executable receipts

| Receipt | Stored evidence | Result | Claim limit |
| --- | --- | --- | --- |
| Deterministic vertical slice | [Slice 1 records](../data/golden_traces/slice1_records_v1.json), byte hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` | 726 records; closure valid; 9 expected/observed comparisons; 4,240 typed and 51 explicit polymorphic references resolved; three architecture/application receipts match | Deterministic implementation validation only. |
| Stochastic engine | [Slice 2 receipt](../data/golden_traces/slice2_stochastic_validation_v1.json), byte hash `96293c252f484dfa6be20c346671df8f20f935413bdc7ea5ad4d9f49c9e06a77` | 5 exact golden traces and replays; 3 queue receipts; 2 application-equivalence receipts; keyed paired-draw canary matches | Implementation validation, not a pilot or substantive result. |
| Development pilot | [Pilot receipt](../data/pilot/pilot_v1_receipt.json), self-hash `e1f53d50d30aa71d5ebc33bc276e892e0452730d2e1dd1a445f881d188299b31` | 15 families, 5 policies, 6 replications; runtime and precision design rehearsed | Development diagnostics only; excluded from confirmatory claims. |
| Negative controls | [Control receipt](../data/golden_traces/slice4_negative_control_receipt_v2.json), self-hash `ff0be43e83326f5de2e3fe103ae9dbc40c392ddd5f27c619efc7d4754eb7d2a0` | 5/5 pass | Matched control behavior only. |
| Fixed Robodebt trace | [Worked trace](../data/golden_traces/robodebt_worked_trace_v1.json), internal artifact hash `5057bf6a0836a97c849bf5a22f37c2bf79abe63b6a2040d9ad4f063537a0755d`, byte hash `eaa28ab1cb90828383aca462726ae79e8ba0de324f0b771c538a4acaac5f6baa` | Baseline/repair controlled pair compiled under specification hash `279d3888856f434a12a6be950cbff7b19d5745054aa5a3ead2bb59a5a2fd05a2` | Explanatory Level B trace; no representativeness, legality, monetary, or attackability inference. |
| Executable evaluation bridge | separately stored specification, exact action instances, and retained receipts | Finite exact certificates record generator/version/hash, assumptions, exclusions, coverage argument, proof identity, and conclusion mode; routing and execution receipts bind the exact case-specific action and support result | Binary period-evidence specification only; not a universal domain specification. |
| Automated repository checks | test suite | 182 tests passed before Freeze 3 execution | Test coverage is implementation evidence, not substantive validity. |

The kernel is case-neutral. The stored isomorphic-vocabulary receipt checks semantic preservation under renamed vocabulary; the non-isomorphic-topology receipt checks that a changed topology is not falsely treated as isomorphic; and the application-adapter receipt checks that Robodebt-specific material remains outside the kernel.

The five matched controls are individually visible rather than collapsed into the 5/5 count:

| Control | Required behavior | Result |
| --- | --- | --- |
| `P0-SAME-RULE-SEMANTIC-NULL` | A representation-only semantic null must not manufacture a permission difference. | pass |
| `P0-ROUTING-INVARIANCE` | Preserved semantic projection under the fixed rule must preserve routing/action behavior. | pass |
| `VERIFIED-MATCH-PROGRESSION` | Action-specific evidence plus timely required review may progress without a robust-permission violation. | pass |
| `NO-SUPPORT-NO-PROGRESSION` | Unsupported evidence states must remain held. | pass |
| `NO-THRESHOLD-NO-PROGRESSION` | A pending case must not progress before the declared threshold/deadline. | pass |

## 5. Confirmatory execution inventory

| Suite | Families x policies x replications | Runs; trajectories | Run-index self-hash | Reconciliation self-hash | Analysis self-hash | Precision decision |
| --- | ---: | ---: | --- | --- | --- | --- |
| Core `CONFIRMATORY-V2` | 108 x 5 x 30 | 16,200; 1,296,000 | `5ff83bdd32a9231d6e5333a3ce30365f54da47256a52a2a78727caa06387e676` | `58f27a685d1b7b5891765ec4f1b0faab34bc2077f98a5aa8edc6ce87e7e58e64` | `b3c2fde249fe38bc6778edac77cfd929144ddc48a8c41a150a97518636752112` | Maximum paired/rate MCSE 0.04332; targets 0.06/0.05 met; no extension. |
| Retrieval-latency sensitivity `SENSITIVITY-INFORMATION-LATENCY-V2` | 108 x 5 x 30 | 16,200; 1,296,000 | `68b06d4b670bc2b8be33bde1f495e5fea9e4a1766c946be78230399a120f3d2f` | `35861361f474c8a08ceddc9682e91bd778de669b7a6819a166ab66112b1a5c4a` | `210b211cc4893411813e4c747f8491f83121515d0ccf868e7be36ce5e91095f4` | Maximum paired/rate MCSE 0.04051; targets met; no extension. |

Both corrected reconciliations report 16,200 expected and observed attempts, zero missing IDs, and zero unexpected IDs. The suites total 32,400 runs and 2,592,000 case-policy trajectories. Their stored evaluation-bridge summaries are `da3388f3e2d7e45a668849a96d76b12ccd7a9777eaee2cb9ebe9751c29ae31dd` (core) and `9c48733e8ea16e25af96b552d4b6a1eb3ebbfac344ada9cb18c88c9b22216c71` (sensitivity); each reports 1,296,000 routing/action comparisons and zero mismatches. The sensitivity doubles retrieval-latency scale from 10 to 20 days and remains separate from the core. It tests delayed routing and queue phasing, not acquisition failure, abandonment, or deadline expiry.

| Frozen design identity | Core | Sensitivity |
| --- | --- | --- |
| Config hash | `4501a127e5c91f90eb368d2290c0ede63bf600894f9322e8760c14031869af77` | `09f7c2656b25cf76cbeb2ce0e215d765559f9400e6dc998642036fbfe6058431` |
| Scenario hash | `16bdb11bdf3dba909f4f71feaf25acefebd72d1ca21e61efe2c38265f2607506` | `9181f8192d5cfccca0a3e9d3d0850bd03e9b009ab3a5d358ee86ff599559da38` |
| Seed inventory | 3,240 seeds; `f4967748d83393b82a5f3c05442438798e9343fa708aeb0483ddc46ece62bfcb` | 3,240 seeds; `d424167cf637a756914b600e2963ba9d21c54c5fc27f22726bac6a8f320af139` |
| Primary contrasts | U2O-U2C, U3-U0, U1-U0 | U3-U0 |

The frozen metric inventory was unsupported progression, gate safety, review completion, decision service, unresolved holding, the field named `recovery_exposure_rate`, recipient burden, agency workload, and right-censoring. Reporting calls the field modeled downstream exposure, renames review completion and the interaction proxy for construct accuracy, and excludes the invalid decision-service field, as detailed in section 7. The complete constrained grids had no run-level exclusions: every expected attempt is present. Invalid or inapplicable measures are omitted at interpretation, not by deleting runs or cases.

The core factor grid crosses nominal initiation load (0.60, 0.95, 1.20), missing evidence (0.10, 0.30, 0.50), access barrier (0.10, 0.30, 0.50), retrievability (low/high), and staff access (partial/complete). Load is a designed input, not observed utilization or a historically estimated threshold. Policies are paired within family and replication through case/event-keyed common random numbers.

## 6. Quantitative claim-to-artifact map

All means and ranges below are unweighted summaries across 108 deliberately designed families. Each family estimate uses 30 paired replications. Normal intervals are estimate +/- 1.96 x MCSE and describe finite-run precision only, not population, historical, parameter, or model uncertainty.

| Claim | Result | Direct evidence | Boundary |
| --- | --- | --- | --- |
| Fail-closed safety under tested loads | U2C mean gate safety was 1.000 at loads 0.60, 0.95, and 1.20. Timely review completion fell 0.857 -> 0.502 -> 0.212 while unresolved holding rose 0.143 -> 0.498 -> 0.788. | Core analysis `cell_summaries`; [Methods/results draft](ARTICLE_METHODS_RESULTS_DRAFT.md), sec. 6.2 | Three tested loads do not locate a continuous threshold. Safety is not service or resolution. |
| Timeout consequence | U2O-U2C unsupported progression +0.476 (family range +0.042 to +0.881; all 108 intervals above zero). Gate safety and unresolved holding changed by -0.476; modeled downstream exposure changed by +0.476. | Core analysis `paired_estimates`; manuscript Table 3 | Direction follows declared timeout semantics; simulation contributes magnitude and scenario variation. |
| Review-completion equivalence | U2O-U2C timely-review-completion difference was 0.000 in all 108 families. | Core analysis `paired_estimates`; manuscript Table 3 | Measures timely pre-action completion, not the full formal `ReviewEffective` construct. |
| Information-first comparison | U3-U0 unsupported progression 0.000; interaction events +1.096 (+0.860 to +1.312); workload events +1.209 (+0.749 to +1.728); modeled downstream exposure +0.594 (+0.369 to +0.815); all nonzero-family intervals above zero. | Core analysis `paired_estimates`; manuscript Table 3 | Interaction events are not effort, subjective burden, welfare, or cost. U3 review metrics are excluded because zero-request replications lack a denominator-aware value. |
| Descriptive unresolved holding | Designed-family mean unresolved holds: U3 0.009, U0 0.766. | Core analysis `cell_summaries`; sec. 6.4 | Descriptive, not a generated paired estimand; fewer action-stage holds do not prove terminal resolution. |
| Validation contrast | U1-U0 unsupported progression +0.781 (+0.578 to +0.914); all 108 intervals above zero. | Core analysis `paired_estimates`; manuscript Table 3 | Benchmark activation only, not a policy recommendation or independent discovery. |
| Retrieval-latency sensitivity | U3-U0: interactions +1.098 (+0.855 to +1.325), workload +1.209 (+0.748 to +1.724), modeled downstream exposure +0.595 (+0.370 to +0.824); both policies again had zero unsupported progression. | Sensitivity analysis `paired_estimates`; sec. 6.5 | Stability to one prespecified perturbation, not general robustness. |

The deterministic publication exhibit is [Figure 3](figures/figure3_simulation_results.svg), byte hash `47254796358999b72660ef93be7e673fe9e422619aa672e53b17ef784c150d06`. Table 3 appears in the [integrated manuscript](ARTICLE_MANUSCRIPT.md). The analysis JSON, not the rendered exhibit, remains the quantitative source of record. The execution ledger retains earlier renderer hashes as historical receipts rather than the current exhibit identity.

### Queue and effective-review boundary map

The stored core capacity and information-tradeoff artifacts are under `outputs/confirmatory_v2/analysis/`; the corresponding sensitivity artifacts are under `outputs/sensitivity_information_latency_v2/analysis/`. Their byte hashes are recorded in the active analysis receipts. Figure 3 is the publication-facing deterministic rendering.

| U2C nominal load | Gate safety | Timely review completion | Unresolved holding | Interpretation |
| ---: | ---: | ---: | ---: | --- |
| 0.60 | 1.000 | 0.857 | 0.143 | Most queued reviews complete in time, while the fail-closed boundary remains intact. |
| 0.95 | 1.000 | 0.502 | 0.498 | Roughly half of initiated cases remain held rather than released through incomplete review. |
| 1.20 | 1.000 | 0.212 | 0.788 | Review completion is low, but overload still does not bypass the gate. |

This is a three-point capacity response, not a located continuous boundary. A configured gate, gate safety, timely review completion, full `ReviewEffective`, and valid decision service are distinct. The simulation directly estimates the first three only to the extent stated: it fixes the non-timing review conditions by policy rather than varying them, so the numerical rate is labeled timely review completion; the decision-service output failed semantic audit.

### Outcome-interpretability matrix

| Outcome family | Valid evidence | What can be said | What cannot be said |
| --- | --- | --- | --- |
| Evidentiary support | Unsupported-progression estimates and worked trace | Compare support-dependent progression under the frozen evaluation rule. | Monetary correctness, legal validity, or historical error prevalence. |
| Timeliness | Timely review completion, holds, deadlines, and censoring | Compare completion and unresolved holding within frozen windows. | Timely supported decision service; its frozen numerator is invalid. |
| Agency workload | Completed modeled assistance, retrieval, review, and reassessment events | Compare event counts per initiated case. | Cost, staffing need, cognitive effort, or historical workload. |
| Recipient burden | Response plus assistance-request interaction events | Compare modeled interaction counts only. | Learning, compliance, psychological burden, welfare, or subjective effort. |
| Modeled downstream exposure | Entry into the simulated external/recovery path | Compare exposure rates and paired policy differences. | Error, harm, amount recovered, or independent confirmation of unsupported action. |
| Correction | Worked-trace reassessment/correction events; stage-aware attempt telemetry | Show that correction is distinct from prior exposure and restoration. | A preregistered paired correction-rate result: the frozen analysis receipt did not emit one. |
| Restoration | Worked-trace residual consequence and stage-aware closure coding | Show trace-specific partial restoration and identify open terminal paths. | Complete-restoration policy comparisons: U0, U2C, and U3 lack modeled terminal-resolution events, and no registered paired restoration estimand exists. |

### Master claim-owner map

| Claim family | Formal proposition or construct | Source/run owner | Article exhibit or trace | Required limitation |
| --- | --- | --- | --- | --- |
| Representation can change permission while held facts remain fixed | F0, F4, P0 fixture | Slice 1 record bundle and P0 receipt | representation-preservation fixture; [Figure 1](figures/figure1_evidence_to_action_protocol.svg) | Controlled fixture, not interface-effect prevalence or usability evidence. |
| Weaker evidence must not add unsupported automatic progression | Characterization 1; F1; FR1 | formal model, worked trace, core paired estimates | Table 3; U2O-U2C and U1-U0; Robodebt trace | Direction is partly rule-defined; simulation contributes magnitude and variation. |
| Fail-closed safety can coexist with review/service failure | Characterization 2; FR3, FR5 | core analysis and queue validation | Figure 3 panels A-B; Table 3 | Three load points do not estimate a universal or continuous threshold. |
| Fail-open timeout converts review shortfall into progression | Characterization 2, part 3 | U2O-U2C paired estimates | Figure 3B; Table 3 | Applies to declared policies and parameter space, not all institutions. |
| Information-first changes a vector of outcomes | action taxonomy; F1/F2 boundary | U3-U0 core and sensitivity receipts | Figure 3C; Table 3 | No scalar welfare ranking; interaction proxy is not substantive burden. |
| Correction is not complete restoration | Proposition 3; F5; FR6 | fixed worked trace and censoring receipts | Supplementary Tables S1–S2, baseline B-08 to B-10 | Trace-specific; terminal comparative restoration remains unidentified. |
| Robodebt is a structurally suitable application | application contract | source manifest, dated profiles, process maps/crosswalk | [Figure 2](figures/figure2_robodebt_process_profiles.svg) and fixed trace | No numerical reconstruction, independent legality finding, or attackability claim. |
| Method transfers across vocabulary | F0-F5 protocol and isomorphic-adapter contract | transfer canary and Slice 1 receipt | compact LLM-summary canary | Representability only; no validated transfer or practitioner-performance claim. |
| Contribution is a bounded synthesis | formal characterizations plus dynamic demonstration | literature/originality map and conducted analyses | integrated introduction and conclusion | No claim to invent information ordering, queues, burden, oversight, or red teaming generally. |

## 7. Measurement audit and censoring

The frozen output includes a `decision_service_effective_rate`, but its numerator counted every no-review case without checking for a supported disposition. That construct is invalid. It is excluded from numerical results, figures, and conclusions, and no post hoc substitute is introduced. Repair would require a new version, freeze, and affected rerun.

The stored `review_effective_rate` measures timely pre-action review completion among queued requests. The article calls it **timely review completion** because it does not vary or score all visibility, authority, dependency, binding, and recording conditions in the formal `ReviewEffective` construct.

The stored `recipient_burden_rate` counts interaction events. The article calls it **recipient interaction events per case** because it does not measure effort, subjective burden, welfare, or cost.

U3 review metrics are excluded from confirmatory interpretation because zero-request replications were encoded as `0.0` rather than not applicable; averaging them would understate conditional performance. No denominator-aware replacement is introduced post hoc.

Administrative closure does not manufacture resolution. Every U0, U2C, and U3 family cell had an open-or-administratively-censored terminal-path rate of 1.000 because those policies lacked modeled terminal-resolution events. Designed-family means were 0.219 for U1 and 0.524 for U2O. Terminal resolution and complete restoration therefore cannot be compared across all five policies, although earlier stage outcomes remain interpretable.

## 8. Robodebt application and transfer boundary

The source packet contains separately dated R-OCI-Early and R-OCI-Enhanced profiles, a process diagram/crosswalk, parameter-provenance table, and explicit documented-versus-stylized mappings. Every executable quantity absent from the historical source record must come from a visibly synthetic scenario overlay. The case-sufficiency assessment is in [CASE_APPLICATION_SUFFICIENCY.md](CASE_APPLICATION_SUFFICIENCY.md).

The fixed Robodebt example is Level B. It holds case, evidence, access, later evidence, process, clocks, evaluation rules, resources, and draws fixed while varying the policy. It illustrates how failed access, imputation, deadline expiry, and permission rules can combine; it is not representative evidence about historical frequency or outcomes.

The LLM-summary transfer canary is an author-constructed cross-vocabulary illustration. It does not validate transfer, current-system prevalence, legality, strategic exploitation, adoption, efficiency, or practitioner performance. The paper may claim that the same formal vocabulary can represent the example, not that unfamiliar users can apply the protocol reliably.

### Article-and-optional-appendix protocol completeness

| Required element | Drafted location | Evidence status |
| --- | --- | --- |
| Level A/B/C choice and escalation | Article Section 7.1 and protocol 1.0 | present |
| Step 1: evidence transformation and surfacing | Article Section 7.2 | present |
| Step 2: permission and fallback | Article Section 7.3 | present |
| Step 3: operational review | Article Section 7.4 | present |
| Step 4: access, workload, deadlines, and queues | Article Section 7.5 | present |
| Step 5: contestability and restoration | Article Section 7.6 | present |
| `pass`/`fail`/`unassessable`/`not_applicable` and `omitted_by_claim_limit` | protocol 1.0 and optional technical appendix | present; omitted claims receive no fabricated assessment status |
| Diagnostic owner, intervention owner, tradeoff | Supplementary Table S2 and protocol report contract | present |
| Fixed Level B Robodebt pair | Article Section 7.7; artifact hash `5057bf6a...755d` | present; prespecified rather than selected from results |
| Compact held-out AI canary | Article Section 7.8 | present as bounded illustration |
| Optional implementation worksheet and worked-trace receipts | [Online technical appendix](ARTICLE_SUPPLEMENTARY_MATERIAL.md) | present as Tables S1–S2 and reference worksheet; not required for article interpretation |
| Extended worksheets/schemas | repository protocol packets and schema manifest | present |
| Author editorial pass | critically revised Section 7 and traceability notes | present; ordinary editing only, with no formal return or usability inference |

## 9. Article and continuity inventory

| Article component | Status | Artifact |
| --- | --- | --- |
| Claim-driven architecture and word budget | drafted and reviewed | [Article outline](ARTICLE_OUTLINE.md) |
| Dynamic methods, results, Figure 3, Table 3 | integrated and critically revised | [Integrated manuscript](ARTICLE_MANUSCRIPT.md) |
| Five-step protocol, worked example, governance interventions | drafted and critically revised | [Protocol/governance draft](ARTICLE_PROTOCOL_GOVERNANCE_DRAFT.md) |
| Limitations and conclusion | integrated and reviewed | [Integrated manuscript](ARTICLE_MANUSCRIPT.md) |
| Introduction, mechanism/literature, formal-model exposition, and case application | integrated and reviewed; Figures 1–2 built | [Integrated manuscript](ARTICLE_MANUSCRIPT.md) |
| Integrated manuscript and word count | conservative whitespace-delimited source count 9,997 words before the bibliography after the bounded audit repair; final APA Word copy has 51 visually inspected pages, three tables, three figures, and three correctly oriented sections | [Integrated manuscript](ARTICLE_MANUSCRIPT.md) and [APA Word manuscript](ARTICLE_MANUSCRIPT_APA.docx) |
| Optional online technical appendix | detailed levels, statuses, completeness rules, receipt fields, reference worksheet, and fixed Robodebt worked trace assembled without a usability claim; may be withheld without impairing the article | [Online technical appendix](ARTICLE_SUPPLEMENTARY_MATERIAL.md) |

The paper is a natural extension of *When Uncertainty Expands Authority* because it formalizes and tests the precursor mechanism. It remains standalone by defining its own concepts, motivating the case, presenting conducted analysis, and restricting lineage material to internal controls, acknowledgments, or a concise origin statement. The continuity table in `CONTINUITY_AND_CLAIM_BOUNDARY.md` classifies precursor claims as retained, refined, tested, bounded, or rejected.

The current departure log records the core uncertainty-to-permission rule as retained and narrowed; nominal “human review” as extended into gate safety, effective review, and service; the two-phase counterfactual as extended into a dynamic process study; the motivating vignette as extended through the Robodebt application; and adversarial language as narrowed into separate vulnerability, susceptibility, and attackability layers. None of these lineage labels is itself reader-facing evidence.

## 10. Reproduction and inspection commands

Run from the repository root in the declared environment. The first group inspects existing receipts without rerunning the simulation:

```bash
jq '{status,target_replications,expected_attempt_count,observed_attempt_count,missing:(.missing_attempt_ids|length),unexpected:(.unexpected_attempt_ids|length),manifest_hash,run_index_hash,reconciliation_hash}' outputs/confirmatory_v2/reconciliation.json
jq '{analysis_hash,family_count,attempt_count,replications,extension_required,precision,evaluation_bridge_summary,claim_limit}' outputs/confirmatory_v2/analysis/analysis_r030.json
jq '{status,target_replications,expected_attempt_count,observed_attempt_count,missing:(.missing_attempt_ids|length),unexpected:(.unexpected_attempt_ids|length),manifest_hash,run_index_hash,reconciliation_hash}' outputs/sensitivity_information_latency_v2/reconciliation.json
jq '{analysis_hash,family_count,attempt_count,replications,extension_required,precision,evaluation_bridge_summary,claim_limit}' outputs/sensitivity_information_latency_v2/analysis/analysis_r030.json
```

The established validation commands are:

```bash
./.venv/bin/python scripts/validate_plan.py
./.venv/bin/python scripts/validate_slice0.py
./.venv/bin/python scripts/validate_slice3.py --allow-confirmatory-output
PYTHONPATH=src ./.venv/bin/python -m pytest -q
```

When per-attempt artifacts are present—either locally retained, restored from an archive, or regenerated—the following commands regenerate the derived reconciliation and analysis receipts:

```bash
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli reconcile experiments/configs/confirmatory_v1.yaml
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli analyze experiments/configs/confirmatory_v1.yaml
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli reconcile experiments/configs/sensitivity_information_latency_v1.yaml
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli analyze experiments/configs/sensitivity_information_latency_v1.yaml
```

In a clean checkout of frozen input commit `dc96716c0865517ab0f61700fb0a06ca39d0042a`, with `docs/FREEZE_MANIFEST.json` from the release package, the recorded environment installed, and the version-2 output directories absent, the complete suites are generated before reconciliation and analysis with:

```bash
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli run experiments/configs/confirmatory_v1.yaml
PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli run experiments/configs/sensitivity_information_latency_v1.yaml
```

These full-run commands are reproduction instructions, not commands to run inside the current result-bearing working tree. A reproducer must compare the resulting run-index, reconciliation, and analysis self-hashes with section 5.

`scripts/verify_repo.py --release` verifies the frozen inventory, stored analyses, negative controls, repository validators, tests, and presence of this packet. Passing it is a technical repository gate, not a submission-readiness certificate: it does not enforce final manuscript completeness, word count, claim coverage, or the 39-question audit. Those remain explicit human/editorial release conditions.

The plan named an `evidence-packet` CLI command, but it was not implemented before the confirmatory freeze. Adding it now would alter the frozen executable inventory after results. This packet is therefore assembled as a non-frozen documentation artifact from stored self-hashes and receipts. The discrepancy is recorded rather than repaired post hoc.

## 11. Final completion audit

Status key: **supported** means stored evidence answers the question within the declared claim limit; **bounded** means only the narrower answer stated here is supported; **pending** means the study cannot yet be declared complete. Under the study plan, any bounded or pending answer keeps the corresponding broader claim incomplete.

| # | Status | Answer and evidence |
| ---: | --- | --- |
| 1 | supported | Yes. Information ordering and permission evaluation have separate owners in the formal model and compiled configuration. |
| 2 | supported | Yes. Observed, imputed, missing, and disputed states are typed through the schema, fixture, traces, and reports. |
| 3 | supported | Yes. Formal support, simulated outcomes, and sourced legal/historical statements are separated; monetary correctness is expressly outside scope. |
| 4 | supported | Yes. The formal model and article distinguish formal authority, functional permission, operational action, and precautionary constraint. |
| 5 | supported | The propositions are formal consequences only under the definitions, assumptions, evaluation specification, and declared refinement set in `FORMAL_MODEL.md`. |
| 6 | supported | Yes. R-OCI-Early and R-OCI-Enhanced are separately dated, sourced, and protected by mixed-precision temporal validation. |
| 7 | supported | Yes, narrowly. Rule directions are partly definitional, while magnitudes, family variation, queue consequences, censoring, and sensitivity are simulation outputs. |
| 8 | supported | Gate safety remains 1.000 under U2C while timely review completion falls and holds rise; U2O and U2C share completion rates but produce opposite permission consequences. Invalid decision-service values are excluded. |
| 9 | bounded | The model and traces expose all named mechanisms, and results report their principal aggregate consequences. Not every mechanism has an independently valid headline estimand; service and substantive burden remain unmeasured. |
| 10 | supported | Yes. Case/event-keyed draws, paired membership, and common-random-number diagnostics are stored. |
| 11 | supported | Yes. Support, delay, workload, interactions, exposure, correction, and restoration/censoring are separate; there is no utility weighting. |
| 12 | supported | No declared confirmatory source, parameter, seed, metric, or analysis identity changed. Direct hashes match and the immutable 77-file scientific inventory verifies after the article-only renderer was relocated outside the frozen trees. |
| 13 | supported | The integrated manuscript includes a repository-grounded reference list. Publication records were checked, identified metadata defects were corrected, and the final 2026-11-11 literature update integrated the closest new comparisons. An APA Word review copy is complete; any later publisher-specific house style remains an external production step, not a source-support gap. |
| 14 | supported | The final source audit recomputed headline quantitative claims from stored core and sensitivity artifacts and checked historical and literature claims against the source packet and publication records. No substantive contradiction was found. |
| 15 | supported | Yes. Transfer is limited to the formal invariant, method, and bounded institutional connections; the canary carries explicit nonclaims. |
| 16 | supported | Yes. Optional or incomplete subsystems are removed, excluded, or recorded in `DEFERRED.md`; the invalid service construct is explicitly excluded. |
| 17 | bounded | Existing commands reproduce traces and derived simulation analysis from stored inputs/attempts, and the technical release verifier passes. The planned packet CLI remains absent and is deliberately not added post-freeze. |
| 18 | supported | The integrated article defines the mechanism, formal model, case application, simulation, and protocol without requiring the precursor; standalone integration and cold-read review are complete. |
| 19 | supported | Yes. Confirmatory and sensitivity analyses were conducted; the methods/results draft reports stored results rather than only a design. |
| 20 | supported | Yes. The continuity table classifies precursor claims as retained, refined, tested, bounded, or rejected. |
| 21 | supported | Yes. Protocol semantics, canary, classifications, and worked-trace selection/specification appear in the pre-output freeze. |
| 22 | supported | Yes. `unassessable` is a first-class status for missing lineage, authority, timing, or process evidence. |
| 23 | supported | Yes. Drafts explicitly reject usability, inter-rater, practitioner-performance, and formal comprehensibility claims. |
| 24 | bounded | The canary demonstrates representability across a different vocabulary, not validated use by independent practitioners or a second empirical case. |
| 25 | supported | A conservative source count places the integrated article at 9,997 whitespace-delimited words before the bibliography, leaving 3 words under the verified ceiling. The separately tracked online technical appendix is optional, is not needed to interpret the article, and will be withheld unless the venue permits supplementary material. |
| 26 | supported | Yes. P0 holds the uncertain output, downstream rule, and process state fixed while changing only interface representation. |
| 27 | supported | Yes. The formal model and case boundary distinguish base vulnerability, structural susceptibility, process red-teaming, and adversarial exploitability; Robodebt is not labeled attackable. |
| 28 | supported | Yes. The main-text canary develops the precursor's LLM-summary example rather than introducing an unrelated vignette. |
| 29 | bounded | The integrated article is written to stand alone and does not rely on the precursor as an unexplained premise. No formal reader study or comprehensibility claim is required. |
| 30 | supported | Yes. Lineage is confined to internal controls and a prospective concise origin statement, not the article's organizing structure. |
| 31 | supported | Yes. The protocol requires Level A/B/C declaration, claim-limit compliance, and escalation. |
| 32 | supported | Yes. The report preserves the complete profile and prohibits an overall score or hidden weighted ranking. |
| 33 | supported | The intake-to-walkthrough-to-executable chain is mechanically traceable to stored evidence. This is inspectability, not a claim that an unfamiliar project lead can use it successfully. |
| 34 | supported | Post-simulation changes recorded to date are editorial or execution-control changes. The invalid service measure was excluded, not semantically repaired; no semantic correction has been made without a new freeze/rerun. |
| 35 | supported | Yes. Higher-level claims outside the selected level use `omitted_by_claim_limit`, not a fabricated fifth assessment status. |
| 36 | supported | Yes. Kernel validation is case-neutral and does not require loading the Robodebt adapter. |
| 37 | supported | Yes. The stored isomorphic-vocabulary receipt preserves semantic projections, event order, metrics, and artifact identity. |
| 38 | supported | Yes. Unsupported historical values cannot execute; stylized overlays have separate ownership and parameter-binding receipts. |
| 39 | supported | Yes. The application, adapter, source packet, provenance table, and worked-trace rule/specification are included in the pre-output freeze. |

## 12. Release activation and next action

The cited-source audit, literature update, APA review-copy formatting, rendered word-count check, optional-appendix fallback, non-destructive validators, stored-artifact checks, and local submission-readiness receipt are complete. The article can be submitted without the optional appendix and remains below the verified ceiling.

One intentionally deferred external activation remains: make the repository publicly accessible before submission, as the data-and-code statement promises. At activation, confirm that the public evidence packet is reachable and state that exact regeneration from the frozen runner is the supported route for ignored per-attempt files retained outside Git.

The selected release receipts and figures must be committed with this packet. Per-attempt files may remain outside Git because exact regeneration from the frozen runner is the supported public route; any separate archive location may be added later without enlarging the paper's claims.

No external reader return or formal comprehensibility review is a release blocker.
