# Evidence Packet

Status: Slice 6 candidate, assembled 2026-11-11 from stored artifacts

Study: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

This packet is the inspection index for the formal model, source-grounded application, executable validation, frozen design, confirmatory runs, quantitative results, and integrated article. It does not itself certify submission readiness. The technical repository release gate passes, and the manuscript's identified false and incomplete bibliographic attributions have been corrected; final publisher-style formatting, source-anchor polish, publisher-rendered word counting, and the submission-readiness receipt remain pending. No reader study, formal comprehensibility return, usability claim, inter-rater claim, or practitioner-performance claim is required or supplied.

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
| Literature and originality | Section 3; `LITERATURE_AND_ORIGINALITY_MAP.md` | present; final manuscript comparison-language audit pending |
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
| Complete integrated manuscript and consistent headline findings | Section 9 | pending |

## 2. Freeze and repository identity

| Item | Stored identity or value | Evidence |
| --- | --- | --- |
| Freeze ID | `UPS-CONFIRMATORY-FREEZE@1` | `FREEZE_MANIFEST.json` |
| Freeze manifest self-hash | `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c` | [Freeze manifest](FREEZE_MANIFEST.json) |
| Frozen repository head | `0b8e890b0ed7a773cfaf328997a3e865ded3457a` | `repository_head_at_creation` in manifest |
| Freeze time | `2026-11-01T19:35:05.140725+00:00` | manifest |
| Frozen file inventory | 77 files; inventory-path hash `93569b6ad029ae634213e6e02f162f7c28e39567d83889ae414abba6b6190a0c` | manifest |
| Source inventory | 10 selected sources, retrieved through 2026-10-31; source-manifest hash `fff48f4a818f29cd7ea5e7168c877c6697cd287a0714c2147b436814c2d87500` | manifest and [source manifest](../data/sources/robodebt/source_manifest.yaml) |
| Frozen runtime | CPython 3.14.4, macOS 26.5.2 arm64 | manifest |
| Packet assembly head | `fc2c6966a9fcf5b9ed9740e3c5067426dc51e8f1` | `git rev-parse HEAD` before this packet was added |

The source manifest records official URLs, publication metadata, local record hashes, and citation locators. Remote source bytes were not archived or byte-hashed at freeze; the manifest records `remote_byte_hash: null` and `http_outcome_at_freeze: not_rechecked`. Historical claims must therefore be checked against the cited official locator, not treated as vendored-source reproduction.

The declared frozen scientific inputs and stored results retain their recorded hashes. A post-freeze article renderer was initially added beneath the manifest-covered `scripts/*.py` tree, causing inventory drift even though it did not affect the scientific run. It now lives at `reporting/build_article_figure3.py`, outside the frozen executable and verification trees. This restores the original 77-file inventory without rewriting or expanding the immutable manifest. The move changes reporting organization only; the renderer remains bound to the stored core-analysis self-hash.

A later execution-control decision retiring formal comprehensibility review had also edited one frozen reference profile and three frozen validators. Those four files have been restored byte-for-byte to their manifest identities. The retirement remains recorded in non-frozen current-control documents: no completed return, agreement measure, usability claim, or practitioner-performance claim is required. The restored release validator checks only that the retained optional-notes file exists; it does not require completion or treat it as evidence.

### Release evidence packaging

The release candidate includes the two compact run indexes, reconciliations, analysis receipts, and four analysis SVGs under `outputs/`. Together they are approximately 7.6 MB and make the run inventory, estimates, precision, and derived plots inspectable without rerunning 32,400 attempts. The 32,400 per-attempt JSON files remain ignored (approximately 134 MB locally). Each run-index entry retains the attempt ID and hash; full attempt-level replay requires either the separately retained local/archive set or regeneration from the frozen runner. This boundary keeps the repository evidence-bearing without misrepresenting a summary receipt as raw data.

| Packaged artifact | File SHA-256 |
| --- | --- |
| Core run index | `b5adc0ec16ab237fd903a34fcbdc3f134ff9c0f3afe380b0b51f3ca5fa07d207` |
| Core reconciliation | `ab7a90f6fdbe0ec5d14001d544f364e84e43ea4b8ce5ff881c1dcec072c3e4d0` |
| Core analysis | `0b22048528518825343657c0a1e1df95880df99ef7a937ba2dee2cb0a680bf8a` |
| Core capacity/timeout SVG | `d4ecc9c52ad16b758498c3e718f700a5cb225fde58dfcb05d38468aa2de018f9` |
| Core information-tradeoff SVG | `fd8b122c9ca5932217e424575ac1faf0ca26b6cc503a1b81a810bd42214fbc83` |
| Sensitivity run index | `daa0010d57c81762fa0d5dd5c27f8942380e24a8b9a427bea1e2d525459de891` |
| Sensitivity reconciliation | `f0cdbaa2f0e8026a50142b817fdd7bb19e3a6e5b28468ba5e62164d6ca779729` |
| Sensitivity analysis | `509525b249e0a60d1c3fffd223f64230eeb661f8caab0d4b88711b4ec358510c` |
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
| Literature/originality map | [Literature map](LITERATURE_AND_ORIGINALITY_MAP.md) | current byte hash `667ff0490c8c97ddf28d02cd5c93c814bddea8dd5f0f90bc6f312fac0e06a291` | Structured scoping map, not a systematic review; final update pending. |
| Precursor continuity and standalone boundary | [Continuity control](CONTINUITY_AND_CLAIM_BOUNDARY.md) | `448dbd056c00de911108d284d40018dd774bf4ac430e8ac1e632a7e914b1e608` | Internal drafting control; published article must stand alone. |
| Worked-trace selection | [Selection rule](WORKED_TRACE_SELECTION.md) | `5b4640979dfbbd2b7f29b63116bc4fdc157c8978b7a606e4d092484cce3885d2` | Explanatory fixed trace, not representative sampling. |

The paper separates three claim classes: formal consequences of declared definitions; simulated operational outcomes in the designed parameter space; and source-attributed historical or legal statements. Monetary correctness is outside all three.

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
| Stochastic engine | [Slice 2 receipt](../data/golden_traces/slice2_stochastic_validation_v1.json), byte hash `7e30903f264a0c9630ebdd27b5e113cf94ec71b670c79a8105491a35a8273c66` | 5 exact golden traces and replays; 3 queue receipts; 2 application-equivalence receipts; keyed paired-draw canary matches | Implementation validation, not a pilot or substantive result. |
| Development pilot | [Pilot receipt](../data/pilot/pilot_v1_receipt.json), self-hash `e1f53d50d30aa71d5ebc33bc276e892e0452730d2e1dd1a445f881d188299b31` | 15 families, 5 policies, 6 replications; runtime and precision design rehearsed | Development diagnostics only; excluded from confirmatory claims. |
| Negative controls | [Control receipt](../data/golden_traces/slice4_negative_control_receipt_v1.json), self-hash `ed9c0462413d96db8b14ec44c2062fc2433df448ed29f95784560fa239d7a861` | 5/5 pass | Matched control behavior only. |
| Fixed Robodebt trace | [Worked trace](../data/golden_traces/robodebt_worked_trace_v1.json), internal artifact hash `5057bf6a0836a97c849bf5a22f37c2bf79abe63b6a2040d9ad4f063537a0755d`, byte hash `eaa28ab1cb90828383aca462726ae79e8ba0de324f0b771c538a4acaac5f6baa` | Baseline/repair controlled pair compiled under specification hash `279d3888856f434a12a6be950cbff7b19d5745054aa5a3ead2bb59a5a2fd05a2` | Explanatory Level B trace; no representativeness, legality, monetary, or attackability inference. |
| Automated repository checks | test suite | 178 tests passed at Slice 5 closeout | Test coverage is implementation evidence, not substantive validity. |

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
| Core `CONFIRMATORY-V1` | 108 x 5 x 30 | 16,200; 1,296,000 | `5153ce51558ce63db314b89e4cea206c345760d904dc5c54caec219a05d6a8d6` | `89ff2c78d842459fb210dcae112ef0f725447ca8a090db8226e17cbd2b203d48` | `bb486ee634365e53b7de464eb8cae8fc1e9169a29e1b6ad0ed3b496a684341cc` | Maximum paired/rate MCSE 0.04332; targets 0.06/0.05 met; no extension. |
| Retrieval-latency sensitivity | 108 x 5 x 30 | 16,200; 1,296,000 | `b4e2bd26a04b0390a9a206fb983f7e78b869a30e616a72aa36dbbbd656719ce7` | `db8ccf476a4815f276cd5b3dc233d5c9fe37a7de296c687e1e031b0af23c5493` | `0abaab09c09c94eb797d46ade1dbe5d7dd46c1ce85d515ba769ed4d1b5bc82db` | Maximum paired/rate MCSE 0.04051; targets met; no extension. |

Both reconciliations report 16,200 expected and observed attempts, zero missing IDs, and zero unexpected IDs. The suites total 32,400 runs and 2,592,000 case-policy trajectories. The sensitivity doubles retrieval-latency scale from 10 to 20 days and remains separate from the core rather than being pooled.

| Frozen design identity | Core | Sensitivity |
| --- | --- | --- |
| Config hash | `f3e3b06d9ef76aba35e3abad60dbc6595d5a28edb63cb916a8ed52d9ea6e179b` | `9e2aabd38cb2306c443aa113595dfebd4dbcf73bf4ad28f839d55eb378b40ba7` |
| Scenario hash | `16bdb11bdf3dba909f4f71feaf25acefebd72d1ca21e61efe2c38265f2607506` | `9181f8192d5cfccca0a3e9d3d0850bd03e9b009ab3a5d358ee86ff599559da38` |
| Seed inventory | 3,240 seeds; `f4967748d83393b82a5f3c05442438798e9343fa708aeb0483ddc46ece62bfcb` | 3,240 seeds; `d424167cf637a756914b600e2963ba9d21c54c5fc27f22726bac6a8f320af139` |
| Primary contrasts | U2O-U2C, U3-U0, U1-U0 | U3-U0 |

The frozen metric inventory was unsupported progression, gate safety, review completion, decision service, unresolved holding, recovery exposure, recipient burden, agency workload, and right-censoring. Reporting renames review completion and the interaction proxy for construct accuracy and excludes the invalid decision-service field, as detailed in section 7. The complete constrained grids had no run-level exclusions: every expected attempt is present. Invalid or inapplicable measures are omitted at interpretation, not by deleting runs or cases.

The core factor grid crosses nominal initiation load (0.60, 0.95, 1.20), missing evidence (0.10, 0.30, 0.50), access barrier (0.10, 0.30, 0.50), retrievability (low/high), and staff access (partial/complete). Load is a designed input, not observed utilization or a historically estimated threshold. Policies are paired within family and replication through case/event-keyed common random numbers.

## 6. Quantitative claim-to-artifact map

All means and ranges below are unweighted summaries across 108 deliberately designed families. Each family estimate uses 30 paired replications. Normal intervals are estimate +/- 1.96 x MCSE and describe finite-run precision only, not population, historical, parameter, or model uncertainty.

| Claim | Result | Direct evidence | Boundary |
| --- | --- | --- | --- |
| Fail-closed safety under tested loads | U2C mean gate safety was 1.000 at loads 0.60, 0.95, and 1.20. Timely review completion fell 0.857 -> 0.502 -> 0.212 while unresolved holding rose 0.143 -> 0.498 -> 0.788. | Core analysis `cell_summaries`; [Methods/results draft](ARTICLE_METHODS_RESULTS_DRAFT.md), sec. 6.2 | Three tested loads do not locate a continuous threshold. Safety is not service or resolution. |
| Timeout consequence | U2O-U2C unsupported progression +0.476 (family range +0.042 to +0.881; all 108 intervals above zero). Gate safety and unresolved holding changed by -0.476; exposure changed by +0.476. | Core analysis `paired_estimates`; Table 2 in methods/results draft | Direction follows declared timeout semantics; simulation contributes magnitude and scenario variation. |
| Review-completion equivalence | U2O-U2C timely-review-completion difference was 0.000 in all 108 families. | Core analysis `paired_estimates`; Table 2 | Measures timely pre-action completion, not the full formal `ReviewEffective` construct. |
| Information-first comparison | U3-U0 unsupported progression 0.000; interaction events +1.096 (+0.860 to +1.312); workload events +1.209 (+0.749 to +1.728); exposure +0.594 (+0.369 to +0.815); all nonzero-family intervals above zero. | Core analysis `paired_estimates`; Table 2 | Interaction events are not effort, subjective burden, welfare, or cost. Workload direction partly follows metric/policy definitions. Exposure is not error or harm. |
| Descriptive unresolved holding | Designed-family mean unresolved holds: U3 0.009, U0 0.766. | Core analysis `cell_summaries`; sec. 6.4 | Descriptive, not a generated paired estimand; fewer action-stage holds do not prove terminal resolution. |
| Validation contrast | U1-U0 unsupported progression +0.781 (+0.578 to +0.914); all 108 intervals above zero. | Core analysis `paired_estimates`; Table 2 | Benchmark activation only, not a policy recommendation or independent discovery. |
| Retrieval-latency sensitivity | U3-U0: interactions +1.098 (+0.855 to +1.325), workload +1.209 (+0.748 to +1.724), exposure +0.595 (+0.370 to +0.824); both policies again had zero unsupported progression. | Sensitivity analysis `paired_estimates`; sec. 6.5 | Stability to one prespecified perturbation, not general robustness. |

The deterministic publication exhibit is [Figure 3](figures/figure3_simulation_results.svg), byte hash `16d4f7d5fe5c30b7e22e44eedbe5124a963ad93459ef55880f11946b0c12ece1`. Table 2 is embedded in the [methods/results draft](ARTICLE_METHODS_RESULTS_DRAFT.md). The analysis JSON, not the rendered exhibit, remains the quantitative source of record.

### Queue and effective-review boundary map

The stored core capacity artifact is `outputs/confirmatory_v1/analysis/capacity_timeout_r030.svg`, SHA-256 `d4ecc9c52ad16b758498c3e718f700a5cb225fde58dfcb05d38468aa2de018f9`. The stored core information-tradeoff artifact is `outputs/confirmatory_v1/analysis/information_tradeoff_r030.svg`, SHA-256 `fd8b122c9ca5932217e424575ac1faf0ca26b6cc503a1b81a810bd42214fbc83`. The corresponding sensitivity artifact hashes are `22f52e37eec54f33fa56e791ea0ed85f47a2afdc14370a77dd220b6e059d6a5c` and `76f25bfd8f4ac4f104ae61951c01cdbf4a8ff57405f3c633c8f11dcc67429062`. Figure 3 is the publication-facing deterministic rendering.

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
| Recovery exposure | Entry into the modeled external/recovery path | Compare exposure rates and paired policy differences. | Error, harm, amount recovered, or independent confirmation of unsupported action. |
| Correction | Worked-trace reassessment/correction events; stage-aware attempt telemetry | Show that correction is distinct from prior exposure and restoration. | A preregistered paired correction-rate result: the frozen analysis receipt did not emit one. |
| Restoration | Worked-trace residual consequence and stage-aware censoring | Show trace-specific partial restoration and identify open terminal paths. | Complete-restoration policy comparisons: U0, U2C, and U3 are fully terminally censored, and no registered paired restoration estimand exists. |

### Master claim-owner map

| Claim family | Formal proposition or construct | Source/run owner | Article exhibit or trace | Required limitation |
| --- | --- | --- | --- | --- |
| Representation can change permission while held facts remain fixed | F0, F4, P0 fixture | Slice 1 record bundle and P0 receipt | representation-preservation fixture; [Figure 1](figures/figure1_evidence_to_action_protocol.svg) | Controlled fixture, not interface-effect prevalence or usability evidence. |
| Weaker evidence must not add unsupported automatic progression | Proposition 1; F1; FR1 | formal model, worked trace, core paired estimates | Table 2; U2O-U2C and U1-U0; Robodebt trace | Direction is partly rule-defined; simulation contributes magnitude and variation. |
| Fail-closed safety can coexist with review/service failure | Proposition 2; FR3, FR5 | core analysis and queue validation | Figure 3 panels A-B; Table 2 | Three load points do not estimate a universal or continuous threshold. |
| Fail-open timeout converts review shortfall into progression | Proposition 2, part 3 | U2O-U2C paired estimates | Figure 3B; Table 2 | Applies to declared policies and parameter space, not all institutions. |
| Information-first changes a vector of outcomes | action taxonomy; F1/F2 boundary | U3-U0 core and sensitivity receipts | Figure 3C; Table 2 | No scalar welfare ranking; interaction proxy is not substantive burden. |
| Correction is not complete restoration | Proposition 3; F5; FR6 | fixed worked trace and censoring receipts | Supplementary Tables S1–S2, baseline B-08 to B-10 | Trace-specific; terminal comparative restoration remains unidentified. |
| Robodebt is a structurally suitable application | application contract | source manifest, dated profiles, process maps/crosswalk | [Figure 2](figures/figure2_robodebt_process_profiles.svg) and fixed trace | No numerical reconstruction, independent legality finding, or attackability claim. |
| Method transfers across vocabulary | F0-F5 protocol and isomorphic-adapter contract | transfer canary and Slice 1 receipt | compact LLM-summary canary | Representability only; no validated transfer or practitioner-performance claim. |
| Contribution is a bounded synthesis | all three propositions plus dynamic demonstration | literature/originality map and conducted analyses | introduction/discussion pending | No claim to invent information ordering, queues, burden, oversight, or red teaming generally. |

## 7. Measurement audit and censoring

The frozen output includes a `decision_service_effective_rate`, but its numerator counted every no-review case without checking for a supported disposition. That construct is invalid. It is excluded from numerical results, figures, and conclusions, and no post hoc substitute is introduced. Repair would require a new version, freeze, and affected rerun.

The stored `review_effective_rate` measures timely pre-action review completion among queued requests. The article calls it **timely review completion** because it does not vary or score all visibility, authority, dependency, binding, and recording conditions in the formal `ReviewEffective` construct.

The stored `recipient_burden_rate` counts interaction events. The article calls it **recipient interaction events per case** because it does not measure effort, subjective burden, welfare, or cost.

Administrative closure does not manufacture resolution. Every U0, U2C, and U3 family cell was terminally right-censored; designed-family mean censoring was 0.219 for U1 and 0.524 for U2O. These values include structurally open paths. Complete restoration cannot be compared for the fully censored policies, although earlier stage-specific outcomes remain interpretable within their declared horizons.

## 8. Robodebt application and transfer boundary

The source packet contains separately dated R-OCI-Early and R-OCI-Enhanced profiles, a process diagram/crosswalk, parameter-provenance table, and explicit documented-versus-stylized mappings. Every executable quantity absent from the historical source record must come from a visibly synthetic scenario overlay. The case-sufficiency assessment is in [CASE_APPLICATION_SUFFICIENCY.md](CASE_APPLICATION_SUFFICIENCY.md).

The fixed Robodebt example is Level B. It holds case, evidence, access, later evidence, process, clocks, evaluation rules, resources, and draws fixed while varying the policy. It illustrates how failed access, imputation, deadline expiry, and permission rules can combine; it is not representative evidence about historical frequency or outcomes.

The LLM-summary transfer canary is an author-constructed cross-vocabulary illustration. It does not validate transfer, current-system prevalence, legality, strategic exploitation, adoption, efficiency, or practitioner performance. The paper may claim that the same formal vocabulary can represent the example, not that unfamiliar users can apply the protocol reliably.

### Article-and-supplement protocol completeness

| Required element | Drafted location | Evidence status |
| --- | --- | --- |
| Level A/B/C choice and escalation | Article Section 7.1 and protocol 1.0 | present |
| Step 1: evidence transformation and surfacing | Article Section 7.2 | present |
| Step 2: permission and fallback | Article Section 7.3 | present |
| Step 3: operational review | Article Section 7.4 | present |
| Step 4: access, workload, deadlines, and queues | Article Section 7.5 | present |
| Step 5: contestability and restoration | Article Section 7.6 | present |
| `pass`/`fail`/`unassessable`/`not_applicable` and `omitted_by_claim_limit` | protocol 1.0 and supplementary material | present; omitted claims receive no fabricated assessment status |
| Diagnostic owner, intervention owner, tradeoff | Supplementary Table S2 and protocol report contract | present |
| Fixed Level B Robodebt pair | Article Section 7.7; artifact hash `5057bf6a...755d` | present; prespecified rather than selected from results |
| Compact held-out AI canary | Article Section 7.8 | present as bounded illustration |
| Publication-facing detailed worksheet and worked-trace receipts | [Supplementary material](ARTICLE_SUPPLEMENTARY_MATERIAL.md) | present as Tables S1–S2 and reference worksheet |
| Extended worksheets/schemas | repository protocol packets and schema manifest | present |
| Author editorial pass | critically revised Section 7 and traceability notes | present; ordinary editing only, with no formal return or usability inference |

## 9. Article and continuity inventory

| Article component | Status | Artifact |
| --- | --- | --- |
| Claim-driven architecture and word budget | drafted and reviewed | [Article outline](ARTICLE_OUTLINE.md) |
| Dynamic methods, results, Figure 3, Table 2 | drafted and critically revised | [Methods/results draft](ARTICLE_METHODS_RESULTS_DRAFT.md) |
| Five-step protocol, worked example, governance interventions | drafted and critically revised | [Protocol/governance draft](ARTICLE_PROTOCOL_GOVERNANCE_DRAFT.md) |
| Limitations and conclusion | drafted; integration review pending | [Limitations/conclusion draft](ARTICLE_LIMITATIONS_CONCLUSION_DRAFT.md) |
| Introduction, mechanism/literature, formal-model exposition, and case application | drafted and critically revised; Figures 1–2 built; integration review pending | [Sections 1–4 draft](ARTICLE_INTRO_FORMAL_CASE_DRAFT.md) |
| Integrated manuscript and word count | manuscript-audit candidate selectively merged; 8,958 whitespace-delimited main-text words excluding bibliography under the verified call; bibliography and source-description defects corrected; publisher-style formatting, independent source-anchor verification, and rendered count pending | [Integrated manuscript](ARTICLE_MANUSCRIPT.md) |
| Publication-facing protocol supplement | detailed levels, statuses, completeness rules, receipt fields, reference worksheet, and fixed Robodebt worked trace assembled without a usability claim | [Supplementary material](ARTICLE_SUPPLEMENTARY_MATERIAL.md) |

The paper is a natural extension of *When Uncertainty Expands Authority* because it formalizes and tests the precursor mechanism. It remains standalone by defining its own concepts, motivating the case, presenting conducted analysis, and restricting lineage material to internal controls, acknowledgments, or a concise origin statement. The continuity table in `CONTINUITY_AND_CLAIM_BOUNDARY.md` classifies precursor claims as retained, refined, tested, bounded, or rejected.

The current departure log records the core uncertainty-to-permission rule as retained and narrowed; nominal “human review” as extended into gate safety, effective review, and service; the two-phase counterfactual as extended into a dynamic process study; the motivating vignette as extended through the Robodebt application; and adversarial language as narrowed into separate vulnerability, susceptibility, and attackability layers. None of these lineage labels is itself reader-facing evidence.

## 10. Reproduction and inspection commands

Run from the repository root in the declared environment. The first group inspects existing receipts without rerunning the simulation:

```bash
jq '{status,target_replications,expected_attempt_count,observed_attempt_count,missing:(.missing_attempt_ids|length),unexpected:(.unexpected_attempt_ids|length),manifest_hash,run_index_hash,reconciliation_hash}' outputs/confirmatory_v1/reconciliation.json
jq '{analysis_hash,family_count,attempt_count,replications,extension_required,precision,claim_limit}' outputs/confirmatory_v1/analysis/analysis_r030.json
jq '{status,target_replications,expected_attempt_count,observed_attempt_count,missing:(.missing_attempt_ids|length),unexpected:(.unexpected_attempt_ids|length),manifest_hash,run_index_hash,reconciliation_hash}' outputs/sensitivity_information_latency_v1/reconciliation.json
jq '{analysis_hash,family_count,attempt_count,replications,extension_required,precision,claim_limit}' outputs/sensitivity_information_latency_v1/analysis/analysis_r030.json
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

In a clean checkout of frozen head `0b8e890b0ed7a773cfaf328997a3e865ded3457a`, with the recorded environment installed and output directories absent, the complete suites are generated before reconciliation and analysis with:

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
| 13 | bounded | The integrated manuscript includes a repository-grounded reference list, and the false authorship, omitted coauthor, incomplete author-list, and incorrect-title defects found in integration review are corrected. Final publisher-style formatting and source-anchor polish remain open. |
| 14 | pending | Draft quantitative claims map to run artifacts and MCSE statements. Final manuscript-wide coverage remains pending. |
| 15 | supported | Yes. Transfer is limited to the formal invariant, method, and bounded institutional connections; the canary carries explicit nonclaims. |
| 16 | supported | Yes. Optional or incomplete subsystems are removed, excluded, or recorded in `DEFERRED.md`; the invalid service construct is explicitly excluded. |
| 17 | bounded | Existing commands reproduce traces and derived simulation analysis from stored inputs/attempts, and the technical release verifier passes. The planned packet CLI remains absent and is deliberately not added post-freeze. |
| 18 | bounded | The integrated article defines the mechanism, formal model, case application, simulation, and protocol without requiring the precursor; final standalone editorial review remains open. |
| 19 | supported | Yes. Confirmatory and sensitivity analyses were conducted; the methods/results draft reports stored results rather than only a design. |
| 20 | supported | Yes. The continuity table classifies precursor claims as retained, refined, tested, bounded, or rejected. |
| 21 | supported | Yes. Protocol semantics, canary, classifications, and worked-trace selection/specification appear in the pre-output freeze. |
| 22 | supported | Yes. `unassessable` is a first-class status for missing lineage, authority, timing, or process evidence. |
| 23 | supported | Yes. Drafts explicitly reject usability, inter-rater, practitioner-performance, and formal comprehensibility claims. |
| 24 | bounded | The canary demonstrates representability across a different vocabulary, not validated use by independent practitioners or a second empirical case. |
| 25 | bounded | The integrated manuscript has 8,958 whitespace-delimited main-text words excluding bibliography, leaving 1,042 words under the verified call ceiling. The publication-facing supplement is tracked separately, but its eligibility outside that ceiling must be confirmed; a publisher-rendered submission count remains pending. |
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

## 12. Release blockers and next actions

The study is not yet complete. Release requires:

1. Draft and integrate the remaining article sections.
2. Normalize the bibliography and audit every final comparison-to-prior-work, historical, legal, and quantitative claim against the literature map, source packet, or run receipt; update the map only if final drafting introduces a new claim or source.
3. Run the final 10,000-word budget check, including the 9,400-word core and any use of the 600-word contingency.
4. Re-run all non-destructive validators, confirm the exact stored artifact identities above, and issue a submission-readiness receipt only when every pending or bounded completion item has been narrowed or closed.

The selected release receipts and figures must be committed with this packet. Per-attempt files may remain outside Git only if the final release states their archival location or confirms that exact regeneration from the frozen runner is the supported route.

No external reader return or formal comprehensibility review is a release blocker.
