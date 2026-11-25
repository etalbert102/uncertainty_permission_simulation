# Evidence Packet

Status: Freeze 5 local reporting-repair package complete; public activation deferred

Updated: 2026-11-24

Study: *From Incomplete Evidence to Automated Action: A Formal Model and Dynamic Simulation of Review Capacity and Timeout Rules, with a Robodebt Application*

## 1. Claim boundary

This is a formal counterfactual simulation over a designed parameter grid, grounded by a documented Robodebt application. It is not a numerical reconstruction of Robodebt. The study does not estimate historical prevalence, monetary correctness, legal validity, population effects, subjective burden, field efficacy, practitioner usability, component-causal effects within the information-first bundle, or overall policy value.

Evidence is interpreted in this order:

1. the active freeze identifies the fixed scientific inputs and executable environment;
2. validation and differential receipts establish implementation behavior within their declared limits;
3. reconciliations establish run completeness;
4. stored analysis receipts establish designed-grid estimates and finite-run Monte Carlo precision; and
5. article prose may narrow but may not enlarge those claims.

## 2. Packet inventory

| Required component | Primary artifact | Status |
| --- | --- | --- |
| Reporting-repair contract | [Freeze 5 plan](FREEZE5_REPORTING_REPAIR_PLAN.md) and [execution ledger](EXECUTION_LEDGER.md) | complete |
| Archived prior freeze | [Freeze 4 manifest](FREEZE_MANIFEST_V4.json) and [attestations](FREEZE_COMMIT_ATTESTATIONS.json) | preserved and verified |
| Active design freeze | [Freeze 5 manifest](FREEZE_MANIFEST.json) | verified |
| Core and sensitivity suites | `outputs/confirmatory_v4/`; `outputs/sensitivity_information_latency_v4/` | complete and reconciled |
| Behavioral continuity | [Freeze 4/5 differential audit](FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.md) | all 32,400 pairs pass |
| Full results | analysis JSON, [Figure 3](figures/figure3_simulation_results.svg), [Table 3 data](tables/table3_simulation_results.json) | synchronized |
| Manuscript package | [article](ARTICLE_MANUSCRIPT.md), [supplement](ARTICLE_SUPPLEMENTARY_MATERIAL.md), [APA Word copy](ARTICLE_MANUSCRIPT_APA.docx) | regenerated and inspected |
| Reporting-repair audit | [Freeze 5 receipt](FREEZE5_MANUSCRIPT_REPAIR_RECEIPT.md) | pass |
| Repository checks | tests; `scripts/verify_repo.py` | 218 tests and release gate pass |

## 3. Freeze identity and execution

| Item | Value |
| --- | --- |
| Freeze ID | `UPS-CONFIRMATORY-FREEZE@5` |
| Manifest self-hash | `d18c7377c6b84d6ac4748ab6be9ab512c2d76cc958b2273bd2a78737957fd4ea` |
| Frozen inventory | 85 files |
| Executable checkpoint | `05f4638` |
| Historical-attestation hash | `807dc8bc879cb4b50de309b5c439d92356fdc6f58dddbecfdebcfcdbc7a8ec68` |
| Negative-control receipt hash | `25a2a4107258f7ef43ab912b4f11894d74d76df222da2b747653cb997db09a81` |

The active manifest covers the formal model, source fixtures, experiment configurations, simulation and analysis code, evaluation specification, and scientific tests. Reporting artifacts remain outside the immutable scientific inventory so that results can be rendered without silently changing executable inputs.

| Suite | Attempts | Trajectories | Run-index hash | Reconciliation hash | Analysis hash |
| --- | ---: | ---: | --- | --- | --- |
| Core | 16,200 | 1,296,000 | `4d761fb22c36f3261f8c38266ecab9be8d99258f79a7ddca3399bc86c504e30e` | `b1f854c17ce8c8a423b183e2d9ca9219d7c08473fc4ebd073a8d0b32c3596500` | `7bf7ee0a3ef39b355bcb9f7ddcf9320787b954e6ebbf9f83faa1e62210b98ba0` |
| Retrieval-latency sensitivity | 16,200 | 1,296,000 | `7f03f0f410543d6688bfa7ce7b5f090ef4a806ab46566405fdd42fefa5b335ba` | `c6c8cc5aed45b415070f86e8fdfc4a0782d3027efd327e811e0fa54aaadd2173` | `3a67f1c898a90296ebde3c0d29bee843edfef840c7f1cd2e0ecd2c0b9fab62a7` |

Each reconciliation observed exactly the expected 16,200 attempt IDs. Replay created zero new attempts and retained all existing attempts. Repeated analyses reproduced byte-identical hashes. Both suites stopped at the frozen 30 paired replications because every precision target passed.

## 4. Freeze 4/5 behavioral identity

The [machine-readable audit](FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json) passes at audit hash `edab65cb1e809a5af30f5e855e2aaa402831a00230b8291b5f991c4e8843bce8`.

Across all 32,400 paired attempts, Freeze 4 and Freeze 5 have identical cohort hashes, complete event hashes, event counts, evaluation-bridge receipts, event details, order, timestamps, actions, queues, every shared stored-row field, and every pre-existing analysis field. Config and schema identities changed as expected. Freeze 5 therefore adds observability and reporting fields; it does not change generated behavior.

This identity proof does not remove outcome-selection risk. Freeze 4 followed inspection of Freeze 3, and Freeze 5 followed informal pre-submission feedback. The manuscript discloses both changes and states that the Freeze 4 unresolved-non-progression contrast is the sign-reversed value of the earlier exposure contrast under a corrected label.

## 5. Nonredundant simulation results

Table 3 has internal self-hash `6ff5645b9f894bc6a107c890c50e61ee28b41835c9aecbf532566adc9edb26bd` and draws directly from the Freeze 5 core analysis.

| Quantity | Estimate | Family range | Simulation MCSE | Interpretation boundary |
| --- | ---: | ---: | ---: | --- |
| Fail-closed timeout activation per initiated case | 0.476 | 0.042–0.881 | 0.0024 | queue deadline misses; timeout consequences are rule-defined |
| U2O evidence-only failure | 0.000 | 0.000–0.000 | — | rule-implied zero: completed review cannot authorize unsupported progression |
| U2O authorization-only failure | 0.105 | 0.004–0.368 | 0.0008 | evidence sufficient; timely authorization missing |
| U2O joint evidence-and-authorization failure | 0.372 | 0.025–0.759 | 0.0020 | both prerequisites missing |
| U3 minus U0 unresolved non-progression | −0.594 | −0.815 to −0.369 | 0.0009 | sole aggregate U3/U0 decision-state contrast |
| U2C timely review conditional on request | 135,766/259,200 = 0.524 | — | — | request-weighted queue diagnostic |
| Additional U3 interaction events per case | +1.096 | 0.860–1.312 | 0.0018 | event count, not effort, burden, welfare, or cost |
| Additional U3 agency-work events per case | +1.209 | 0.749–1.728 | 0.0017 | event count, not staffing cost or policy value |

The fail-open union is exactly partitioned by its three exclusive components. All fail-open progression lacks timely authorization, while 0.372 is also evidentially unsupported. The 0.476 is one timeout-activation result, not several independent effects.

U3 sequential stage rates are 0.573 adequate response evidence, 0.427 retrieval requests, 0.256 retrieved evidence, 0.171 unresolved after acquisition and entering review, 0.162 evidence requested after timely review, and 0.009 held after timeout. These values locate cases in the declared sequence. They do not identify independent assistance, retrieval, or review effects. Because the model has no post-request response cycle, completed review changes the unresolved-state label rather than evidentiary resolution.

## 6. Formal and documented application

| Evidence layer | Supported use | Excluded inference |
| --- | --- | --- |
| Formal model | definition and operational test for robust permission; review and restoration conditions | prevalence or universal legal rule |
| Representation fixture | isolates representation suppression while case, evidence, and downstream rule remain fixed | empirical interface effect or exploitability |
| Robodebt application | maps documented evidence transformation, notice, action, recovery, and reassessment to the diagnostics | numerical calibration, independent causation, actual-case debt, or legal judgment |
| Dynamic simulation | estimates queue activation, failure composition, and unresolved-case location in a designed grid | historical Robodebt rates or overall policy ranking |
| Five-step protocol | prospective inspectable workflow test | validated usability or practitioner performance |

Under the study-authored period-evidence specification, the documented averaging rule fails F1 at the rule level when the employment interval includes non-benefit fortnights: an admissible same-total refinement can place all earnings there, where no debt is supported, while averaging can assign income to benefit fortnights and permit progression. Other interval structures require separate action-specific analysis. A verdict for an actual historical case remains `unassessable` without its exact action, income timing, benefit record, and applicable support rule. The application illustrates the test; it does not independently validate it.

## 7. Manuscript and artifact QA

- Markdown count before `References`: 7,661 whitespace-delimited words, leaving 2,339 below the 10,000-word ceiling.
- APA Word export: 41 rendered pages, three tables, three figures, and three correctly oriented sections.
- Full-resolution visual inspection: all 41 pages pass; exhibits are legible and unclipped.
- ZIP integrity: pass.
- Accessibility: zero high-, medium-, or low-severity findings.
- Images: three inline images with expected dimensions.
- Section audit: portrait, landscape Table 3, then portrait restoration.
- Heading audit: 11 Heading 1 and 37 Heading 2 paragraphs; exhibit labels use their dedicated style.
- Repository regression: 218 tests pass.

## 8. Reproduction and remaining external action

From the repository root with the recorded environment installed:

```bash
PYTHONPATH=src .venv/bin/python -m uncertainty_permission_simulation.cli verify-freeze docs/FREEZE_MANIFEST.json
.venv/bin/python scripts/verify_repo.py --through-slice 5
PYTHONPATH=src .venv/bin/python -m pytest -q
```

The canonical run, reconcile, and analyze commands and their outputs are recorded in the Freeze 5 plan and execution ledger. The compact result chain is committed; ignored append-only attempt files are deterministically regenerable from frozen inputs.

The bounded reporting repair is locally complete. The remaining external action is repository activation and a logged-out URL check. Publicity remains under project-lead control and is not inferred from this repair.
