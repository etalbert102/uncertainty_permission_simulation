# Evidence Packet

Status: Freeze 4 local release package complete; public activation deferred

Updated: 2026-11-21

Study: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

## 1. Claim boundary

This is a formal counterfactual simulation over a designed parameter grid, grounded by a documented Robodebt application. It is not a numerical reconstruction of Robodebt. The study does not estimate historical prevalence, monetary correctness, legal validity, population effects, subjective burden, field efficacy, practitioner usability, or overall policy value.

Evidence is interpreted in this order:

1. the active freeze identifies the prespecified scientific inputs and executable environment;
2. validation and differential receipts establish implementation behavior within their declared limits;
3. reconciliations establish run completeness;
4. analysis receipts establish designed-grid estimates and finite-run Monte Carlo precision; and
5. article prose may narrow but may not enlarge those claims.

An internal self-hash identifies canonical JSON content after excluding its own hash field. A file SHA-256 identifies stored bytes. They are not interchangeable.

## 2. Packet inventory

| Required component | Primary artifact | Status |
| --- | --- | --- |
| Repair contract and completed ledger | [Freeze 4 plan](FREEZE4_METRIC_REPAIR_PLAN.md) | all nine implementation slices complete; closeout recorded |
| Archived prior freeze | [Freeze 3 manifest](FREEZE_MANIFEST_V3.json) and [attestations](FREEZE_COMMIT_ATTESTATIONS.json) | preserved and verified |
| Active design freeze | [Freeze 4 manifest](FREEZE_MANIFEST.json) | verified |
| Core and sensitivity suites | `outputs/confirmatory_v3/`; `outputs/sensitivity_information_latency_v3/` | complete and reconciled |
| Behavioral continuity | [differential audit](FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.md) | pass |
| Semantic metric audit | Freeze 4 plan, Slices 0–3; tests | complete |
| Scientific-value decision | [decision receipt](FREEZE4_SCIENTIFIC_VALUE_DECISION.md) | retain full simulation section |
| Full results | analysis JSON, [Figure 3](figures/figure3_simulation_results.svg), [Table 3 data](tables/table3_simulation_results.json) | synchronized |
| Manuscript package | [article](ARTICLE_MANUSCRIPT.md), [supplement](ARTICLE_SUPPLEMENTARY_MATERIAL.md), [APA Word copy](ARTICLE_MANUSCRIPT_APA.docx) | Slice 8 committed and visually inspected |
| Source and citation audit | [literature audit](LITERATURE_SEARCH_AUDIT.md), source manifest, case-study crosswalk | updated for named comparisons |
| Manuscript audit | [Freeze 4 audit receipt](FREEZE4_MANUSCRIPT_AUDIT_RECEIPT.md) | 24 stages complete; bounded repair applied; two manual dispositions resolved |
| Word count and artifact QA | [submission receipt](SUBMISSION_READINESS_RECEIPT.md) | 7,144 call-counted source words; 39-page Word copy inspected |
| Repository tests and release gate | test suite; `scripts/verify_repo.py` | 209 tests pass; final release gate returns `release: true` |

## 3. Freeze identities

### Active Freeze 4

| Item | Value |
| --- | --- |
| Freeze ID | `UPS-CONFIRMATORY-FREEZE@4` |
| Manifest self-hash | `bd330d56273ae7a85aed872b5e1442400b02b1f6b822c1fa6154ae2de5d62c63` |
| Frozen inventory | 84 files |
| Executable checkpoint | `d7e8494` |
| Core config hash | `9c323731dacf5fae84b89f938e7cdd6bf698f9763cb0a1c2b3a3d9a62c8e8a00` |
| Sensitivity config hash | `04a5b801a8ee3da2cab7874f7e748f8c98e1de21cc30339513c5a606108c0b47` |
| Negative-control receipt hash | `a90f810032f3b0af9acde802401fd07294ceb42d69575df32226f35a9014b45b` |

The active manifest verifies the formal model, source fixtures, experiment configurations, simulation and analysis code, evaluation specification, and scientific tests. Manuscript and reporting artifacts remain outside the immutable inventory so that results can be reported without silently changing scientific inputs.

### Historical continuity

Freeze 2 and Freeze 3 remain preserved and commit-attested. Freeze 3 is archived as `FREEZE_MANIFEST_V3.json`; the earlier pre-bridge manifests and evaluation-specification correction remain available. Active Freeze 4 does not overwrite those records.

## 4. Execution and result chain

| Suite | Attempts | Trajectories | Run-index self-hash | Reconciliation self-hash | Analysis self-hash |
| --- | ---: | ---: | --- | --- | --- |
| Core | 16,200 | 1,296,000 | `ee02db83b3c1fdd5820b0c9df6bc1a5873021cccc8bb0e7056e59a2144a43dd5` | `9eec52257c6c089b39737cca1656d02b9be2ade6cad0a310d24cebf4737b88c7` | `5ac3d5c5a5d04cea7241e76ec5f390f9f266cfbd60cafd2339507dd44e360588` |
| Retrieval-latency sensitivity | 16,200 | 1,296,000 | `35c4330db4cfffcd49117214993c4674cf2ccf5824ac081514ea8036cf6c35f4` | `a3267a7c9e736381d209b651e51531ceb17ab478f01f69153b78f9f5e91707b8` | `d5762c5194d62e5c3dd6082bd72bb0c2856765c2326087e8988882ecded93570` |

Each reconciliation observed exactly the expected 16,200 attempt IDs with no missing or unexpected IDs. Resume/replay created zero additional attempts. Reconciliation and analysis reruns reproduced their hashes. Both suites satisfied the frozen precision rule at 30 replications, so no extension to 60 was authorized.

The stored compact indexes, reconciliations, analyses, and analysis SVGs are committed. The 32,400 append-only per-attempt files remain local ignored intermediates; exact regeneration from frozen inputs is the public reproducibility route.

## 5. Freeze 3/4 differential audit

The [machine receipt](FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json) has audit hash `916c1c203be866725b3d64c537e41187b604ac635d49cca20a98995aaccf4778`.

Across all 32,400 paired attempts:

- cohort, event, and action-support receipts matched;
- event detail, order, timestamps, actions, queues, and outcomes had zero blocking mismatches;
- shared valid metrics and common-random-number identities matched; and
- compiled configuration and attempt identities changed as expected because the manifest, config, schema, and stored row fields changed.

Freeze 4 therefore changes measurement and reporting, not generated behavior. It removes the invalid service measure from primary reporting, makes conditional review metrics denominator-aware, conserves every initiated case across five decision states, and separates three recovery-entry states from terminal resolution.

## 6. Scientific-value gate

The [value decision](FREEZE4_SCIENTIFIC_VALUE_DECISION.json) has decision hash `b418d8660a6139eff94687a598b551b3f003ca0ae9c00d45e2b2def75b74af06` and retains the full simulation section.

| U3 factor | Unresolved non-progression range | Largest level MCSE | Range/MCSE | Gate |
| --- | ---: | ---: | ---: | --- |
| Access barrier | 0.025775 | 0.001238 | 20.8 | fail: below 0.05 |
| Retrievability | 0.214823 | 0.001206 | 178.1 | pass |
| Staff access | 0.000764 | 0.000988 | 0.8 | fail |

The U3 review diagnostic contains 44,381 requests and 42,098 timely completions. Twenty of 3,240 family-replications had no review request and were treated as not applicable; all 108 families had a positive aggregate request denominator. The latency sensitivity retained a 0.214591 retrievability range. This gate controls article prominence only and does not validate the model against historical Robodebt.

## 7. Nonredundant simulation results

The machine-readable Table 3 has self-hash `efbb334a25e4647cc665c462b1c0a3ff56d96de3f7c6b4903df12d6475067959`. The main article reports one quantity per decision-state accounting identity.

| Quantity | Estimate | Family range | Simulation MCSE | Interpretation boundary |
| --- | ---: | ---: | ---: | --- |
| Fail-closed timeout activation per initiated case | 0.476 | 0.042–0.881 | 0.0024 | queue deadline misses; fail-open progression and fail-closed holding are authored consequences |
| U3 minus U0 unresolved non-progression | −0.594 | −0.815 to −0.369 | 0.0009 | sole aggregate U3/U0 decision-state contrast |
| U2C timely review conditional on request | 0.524 | — | — | 135,766/259,200 requests; not timely supported service |
| Additional U3 interaction events per case | 1.096 | 0.860–1.312 | 0.0018 | event count, not effort, burden, welfare, or cost |
| Additional U3 agency-work events per case | 1.209 | 0.749–1.728 | 0.0017 | event count, not staffing cost, efficiency, or policy value |

Under U3, timely review of incomplete evidence requests more evidence; it does not authorize progression. Recovery-path entry is reported directionally because it may follow supported or unsupported progression and is not itself error, harm, success, resolution, or restoration.

## 8. Formal and documented application

| Evidence layer | Artifact | Supported use | Excluded inference |
| --- | --- | --- | --- |
| Formal model | [FORMAL_MODEL.md](FORMAL_MODEL.md) | definition and operational test for robust permission; review and restoration conditions | prevalence or universal legal rule |
| Representation fixture | main article plus supplement executable fixture | isolates representation suppression while evidence and downstream rule remain fixed | empirical interface effect or attackability |
| Robodebt application | [ROBODEBT_CASE_STUDY.md](ROBODEBT_CASE_STUDY.md) and fixed source profiles | maps documented evidence transformation, notice, review, referral, and reassessment to the formal diagnostics | numerical calibration, independent causation, or legal judgment |
| Dynamic simulation | frozen V3 analyses | estimates queue and decision-state quantities in a designed grid | historical Robodebt rates or population effects |
| Five-step protocol | [PROCESS_RED_TEAM_PROTOCOL.md](PROCESS_RED_TEAM_PROTOCOL.md) | prospective inspectable workflow test | validated usability or reproducible practitioner performance |

The enhanced OCI profile is structurally compatible with the proposed mechanism, but its action-specific historical F1 verdict is `unassessable` without an exact action instance, independent support prerequisite, and defeating admissible same-total refinement. A later receipt-and-ignoring guard cannot supply missing period evidence upstream. The case illustrates rather than validates the rule.

## 9. Source and citation audit

The source manifest retains official locators and use boundaries for the fixed Robodebt packet. The [literature audit](LITERATURE_SEARCH_AUDIT.md) is a structured search and citation-chaining record, not a systematic-review claim.

The final comparison pass explicitly distinguishes this article from:

- Lin et al. on observable evidence-to-action chains for tool-using agents;
- Wang and Rachev on analytic capacity regimes;
- Green on the limits of human-oversight mandates;
- Rinta-Kahila et al. on Robodebt system destructiveness;
- Carney on Robodebt legality and rule-of-law safeguards; and
- Lykouris and Weng on learned deferral and scheduling under congestion.

The contribution is the joint operationalization: a refinement-based action-set test, source-bounded administrative application, fixed-rule capacity/timeout simulation, and prospective process protocol. No priority claim is made for uncertainty-to-action auditing, human oversight, queueing, contestability, administrative burden, or Robodebt scholarship separately.

## 10. Manuscript and artifact QA

The Slice 8 package commit is `b1d6f57`; its ledger closeout is `b6b5153`. The final bounded endpoint repair and audited package are committed at `d7e193f`.

- conservative Markdown count before `References`: 7,144 words;
- APA Word export: 39 pages, three tables, three figures, three sections;
- full-resolution visual inspection: all pages pass;
- ZIP integrity: pass;
- accessibility: zero high-, medium-, or low-severity findings;
- images: three inline images with expected dimensions;
- section audit: portrait, landscape Table 3, portrait restoration; and
- repository regression: 209 tests pass.

The adjacent manuscript-audit pipeline received an immutable manuscript copy and bounded Freeze 4 packet. It completed 24 stages and one repair round. The [audit receipt](FREEZE4_MANUSCRIPT_AUDIT_RECEIPT.md) records the accepted edits, the project-lead disposition of both manual flags, and hashes for the external release reports.

## 11. Reproduction and verification

From the repository root with the recorded environment installed:

```bash
PYTHONPATH=src .venv/bin/python -m uncertainty_permission_simulation.cli verify-freeze docs/FREEZE_MANIFEST.json
.venv/bin/python scripts/verify_repo.py --through-slice 5
PYTHONPATH=src .venv/bin/python -m pytest -q
```

The canonical run, resume, reconcile, and analyze commands are stored in the Freeze 4 plan and experiment configuration help. The compact result chain is sufficient to inspect reported results; regenerating ignored attempt files is required for complete attempt-level replay in a fresh public checkout.

## 12. Remaining external action

The local release audit is complete: the bounded manuscript corrections and manual dispositions are recorded, the APA copy was regenerated and inspected, the artifact identities are synchronized, all 209 tests pass, and `scripts/verify_repo.py --release` returns `release: true`.

The only external action left is repository activation and a logged-out URL check. No external-reader return, formal comprehensibility review, usability study, or supplement-eligibility assumption is a release blocker.
