# Freeze 3/Freeze 4 Differential Audit

Status: **pass**

This audit pairs every stored Freeze 3 and Freeze 4 attempt. It tests behavioral continuity separately from the expected metric-schema, configuration, manifest, and attempt-hash changes.

| Suite | Paired attempts | Cohort mismatches | Event mismatches | Support-receipt mismatches | Blocking mismatches |
| --- | ---: | ---: | ---: | ---: | ---: |
| core | 16,200 | 0 | 0 | 0 | 0 |
| information_latency_sensitivity | 16,200 | 0 | 0 | 0 | 0 |

## Interpretation

Exact cohort hashes, event hashes, evaluation-bridge receipts, shared valid metrics, held-state bridges, recovery-entry bridges, and stage-coded censoring bridges establish that Freeze 4 changed measurement and reporting rather than generated behavior. Attempt hashes change because the configuration identity, manifest identity, schema version, and stored row fields changed.

`DecisionServiceEffective` and the aggregate censoring rate were removed from primary reporting. Conditional review and gate measures now store raw counts, use null for non-applicability, and are aggregated by ratio of sums. The five decision states and three recovery-entry states are new measurements of unchanged traces.

Machine receipt: `docs/FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json`
