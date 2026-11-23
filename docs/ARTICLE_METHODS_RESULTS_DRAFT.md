# Article Draft: Dynamic Simulation Methods and Results

Status: synchronized publication-facing extract from Freeze 5. The canonical prose is Sections 5–6 of [ARTICLE_MANUSCRIPT.md](ARTICLE_MANUSCRIPT.md); this file preserves a compact review copy and traceability map.

## Methods summary

The study used a finite-cohort discrete-event simulation to measure how often limited review capacity activated declared timeout rules and where cases accumulated. Each run followed 80 cases under one scenario family, policy, and replication. The 108-family core crossed nominal load (0.60, 0.95, 1.20), missing-evidence probability (0.10, 0.30, 0.50), access-barrier probability (0.10, 0.30, 0.50), retrieval success (0.35, 0.85), and staff access (partial, complete). Five policies and 30 paired replications produced 16,200 core runs and 1,296,000 case-policy trajectories. A separate 16,200-run sensitivity doubled retrieval latency.

The policies were conservative holding (U0), impute and progress (U1), review with a fail-closed timeout (U2C), review with a fail-open timeout (U2O), and agency-assisted information first (U3). U2O−U2C isolated the consequence of review non-completion under shared review machinery. U3−U0 compared assisted evidence acquisition with conservative holding. U1−U0 remained an implementation-validation contrast.

Every initiated case entered exactly one decision state: supported progression, unsupported progression, evidence requested after completed review, unresolved hold, or still open before action. Unresolved non-progression combined the final three states. Unsupported progression was decomposed into exclusive evidence-only, authorization-only, and joint failures. U3 also stored its sequential evidence and review stages. Timely review used review requests as its denominator and was null when no request existed. Timely supported service was not estimated.

Freeze 5 added reporting observability after external review without changing policies, cases, random streams, queues, or events. A differential audit paired all 32,400 Freeze 4 and Freeze 5 attempts and found identical cohorts, complete event streams, evaluation receipts, and shared outcomes. Both Freeze 5 suites reconciled and reproduced deterministically at 30 replications; 218 automated checks passed.

## Results summary

Under fail-closed review, timeout activation rose from 0.143 to 0.498 to 0.788 across the three nominal loads, while timely completion conditional on a review request fell from 0.857 to 0.502 to 0.212. Across the full grid, 135,766 of 259,200 U2C review requests completed on time. Mean timeout activation was 0.476 of initiated cases (family range 0.042–0.881), and fail open converted each miss into progression. The exclusive partition is 0 evidence-only, 0.105 authorization-only, and 0.372 joint evidence-and-authorization failure. These are components of one result, not separate effects.

U3 and U0 both produced zero unsupported progression. U3 reduced unresolved non-progression by 0.594 relative to U0 (family range 0.369–0.815). Within U3, 0.573 of initiated cases had adequate response evidence, 0.427 entered retrieval, 0.256 obtained evidence, and 0.171 remained unresolved and entered review. Timely review placed 0.162 in an evidence-request state; timeout left 0.009 held. These are sequential stage rates, not independent component effects.

Relative to U0, U3 added 1.096 modeled interaction events and 1.209 agency-work events per initiated case. These counts do not measure effort, subjective burden, welfare, staffing cost, or overall policy value. Recovery-path entry shifted directionally toward entry after supported progression.

Doubling retrieval latency changed every reported U3 stage rate by less than 0.001 and did not change the zero-unsupported-progression result for U0 and U3. The sensitivity tests routing and queue phasing only.

## Traceability

| Artifact | Freeze 5 source |
| --- | --- |
| Active design freeze | `docs/FREEZE_MANIFEST.json`, self-hash `d18c7377c6b84d6ac4748ab6be9ab512c2d76cc958b2273bd2a78737957fd4ea` |
| Core reconciliation | `outputs/confirmatory_v4/reconciliation.json`, hash `b1f854c17ce8c8a423b183e2d9ca9219d7c08473fc4ebd073a8d0b32c3596500` |
| Core analysis | `outputs/confirmatory_v4/analysis/analysis_r030.json`, hash `7bf7ee0a3ef39b355bcb9f7ddcf9320787b954e6ebbf9f83faa1e62210b98ba0` |
| Sensitivity reconciliation | `outputs/sensitivity_information_latency_v4/reconciliation.json`, hash `c6c8cc5aed45b415070f86e8fdfc4a0782d3027efd327e811e0fa54aaadd2173` |
| Sensitivity analysis | `outputs/sensitivity_information_latency_v4/analysis/analysis_r030.json`, hash `3a67f1c898a90296ebde3c0d29bee843edfef840c7f1cd2e0ecd2c0b9fab62a7` |
| Differential audit | `docs/FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json`, hash `edab65cb1e809a5af30f5e855e2aaa402831a00230b8291b5f991c4e8843bce8` |
| Figure 3 | `docs/figures/figure3_simulation_results.svg` |
| Table 3 data | `docs/tables/table3_simulation_results.json`, hash `e5efca36c6245fe137ea98eb2ca5ed977f8657971634dfff14c2367cd957f611` |
