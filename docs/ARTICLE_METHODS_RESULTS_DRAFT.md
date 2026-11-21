# Article Draft: Dynamic Simulation Methods and Results

Status: synchronized publication-facing extract from Freeze 4. The canonical prose is Sections 5–6 of [ARTICLE_MANUSCRIPT.md](ARTICLE_MANUSCRIPT.md); this file preserves a compact review copy and traceability map.

## Methods summary

The study used a finite-cohort discrete-event simulation to measure how often limited review capacity activated declared timeout rules and where cases accumulated. Each run followed 80 cases under one scenario family, policy, and replication. The 108-family core crossed nominal load (0.60, 0.95, 1.20), missing-evidence probability (0.10, 0.30, 0.50), access-barrier probability (0.10, 0.30, 0.50), retrieval success (0.35, 0.85), and staff access (partial, complete). Five policies and 30 paired replications produced 16,200 core runs and 1,296,000 case-policy trajectories. A separate 16,200-run sensitivity doubled retrieval latency.

The policies were conservative holding (U0), impute and progress (U1), review with a fail-closed timeout (U2C), review with a fail-open timeout (U2O), and agency-assisted information first (U3). U2O−U2C isolated the consequence of review non-completion under shared review machinery. U3−U0 compared assisted evidence acquisition with conservative holding. U1−U0 remained an implementation-validation contrast.

Every initiated case entered exactly one decision state: supported progression, unsupported progression, evidence requested after completed review, unresolved hold, or still open before action. Unresolved non-progression combined the final three states. A separate partition recorded recovery-path entry after supported progression, entry after unsupported progression, or no entry. Timely review used review requests as its denominator and was null when no request existed. Timely supported service was not estimated.

Freeze 4 repaired metric semantics without changing policies, cases, random streams, queues, or events. A differential audit paired all 32,400 Freeze 3 and Freeze 4 attempts and found identical cohorts, events, ordering, timestamps, actions, queues, and shared outcomes. Both Freeze 4 suites reconciled and reproduced deterministically at 30 replications; 209 automated checks passed at freeze issuance.

## Results summary

Under fail-closed review, timeout activation rose from 0.143 to 0.498 to 0.788 across the three nominal loads, while timely completion conditional on a review request fell from 0.857 to 0.502 to 0.212. Across the full grid, 135,766 of 259,200 U2C review requests completed on time. Mean timeout activation was 0.476 of initiated cases (family range 0.042–0.881). Because fail open changed only the consequence of non-completion, the same quantity is the mean increase in unsupported progression under U2O relative to U2C; it is one result, not several independent contrasts.

U3 and U0 both produced zero unsupported progression. U3 reduced unresolved non-progression by 0.594 relative to U0 (family range 0.369–0.815). U3 produced 44,381 review requests, 42,098 of which completed on time; 20 of 3,240 family-replications had no request, and every family had a positive aggregate denominator. A completed review of still-incomplete evidence requested evidence and left the case unresolved rather than authorizing progression.

Within U3, unresolved non-progression was 0.064 under high retrievability and 0.279 under low retrievability, a range of 0.215. Access-barrier levels spanned 0.026 and staff-access levels spanned 0.001. Relative to U0, U3 added 1.096 modeled interaction events and 1.209 agency-work events per initiated case. These counts do not measure effort, subjective burden, welfare, staffing cost, or overall policy value. Recovery-path entry shifted directionally toward entry after supported progression.

Doubling retrieval latency left the retrievability range at 0.215 and did not change the zero-unsupported-progression result for U0 and U3. The sensitivity tests routing and queue phasing only.

## Traceability

| Artifact | Freeze 4 source |
| --- | --- |
| Active design freeze | `docs/FREEZE_MANIFEST.json`, self-hash `bd330d56273ae7a85aed872b5e1442400b02b1f6b822c1fa6154ae2de5d62c63` |
| Core reconciliation | `outputs/confirmatory_v3/reconciliation.json`, hash `9eec52257c6c089b39737cca1656d02b9be2ade6cad0a310d24cebf4737b88c7` |
| Core analysis | `outputs/confirmatory_v3/analysis/analysis_r030.json`, hash `5ac3d5c5a5d04cea7241e76ec5f390f9f266cfbd60cafd2339507dd44e360588` |
| Sensitivity reconciliation | `outputs/sensitivity_information_latency_v3/reconciliation.json`, hash `a3267a7c9e736381d209b651e51531ceb17ab478f01f69153b78f9f5e91707b8` |
| Sensitivity analysis | `outputs/sensitivity_information_latency_v3/analysis/analysis_r030.json`, hash `d5762c5194d62e5c3dd6082bd72bb0c2856765c2326087e8988882ecded93570` |
| Differential audit | `docs/FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json`, hash `916c1c203be866725b3d64c537e41187b604ac635d49cca20a98995aaccf4778` |
| Scientific-value decision | `docs/FREEZE4_SCIENTIFIC_VALUE_DECISION.json`, hash `b418d8660a6139eff94687a598b551b3f003ca0ae9c00d45e2b2def75b74af06` |
| Figure 3 | `docs/figures/figure3_simulation_results.svg` |
| Table 3 data | `docs/tables/table3_simulation_results.json`, hash `efbb334a25e4647cc665c462b1c0a3ff56d96de3f7c6b4903df12d6475067959` |
