# Slice 3 Development Pilot Audit

Status: engineering and design-freeze candidate; independent cold-reader QA pending

The pilot used 15 outcome-independent, pairwise-coverage scenario families, six replications, 48 cases per replicate, and all five policies. It executed 21,600 case-policy runs. The detailed development rows remain ignored; the tracked receipt contains aggregate diagnostics and explicit development-only claim limits.

## Design decisions

| Item | Freeze candidate |
| --- | --- |
| Core environmental families | all 108 semantically valid Cartesian families |
| Cohort | 80 cases per family-replication |
| Initiation | finite window derived from cohort size, review service scale, review capacity, and declared load factor |
| Administrative cutoff | day 650; events beyond the cutoff are not executed and open paths are right-censored by reason |
| Minimum replications | 30 paired replications per family |
| Maximum replications | 60 paired replications per family |
| Rate MCSE target | 0.05 |
| Paired-difference MCSE target | 0.06 |
| Extension | if any primary metric misses its target at 30, extend every policy in every valid family to 60 using the next frozen seeds |
| Confirmatory runtime ceiling | 24 hours for the core run; one separate 24-hour family-wide precision extension window |
| Outputs | append-only aggregate run rows, reconciliation, paired estimates, intervals, MCSE, censoring, boundary/tradeoff figures, and claim-boundary memo |

The measured pilot throughput predicts roughly 8.4 minutes for the 108-family, 30-replication, 80-case core on the recorded development environment, well below the 24-hour ceiling. Runtime is a planning estimate, not a performance guarantee.

## Precision decision

The largest applicable six-replication cell and paired MCSE was approximately 0.110. Applying the prespecified square-root replication projection gives approximately 0.049 at 30 replications, meeting the candidate 0.05 rate and 0.06 paired targets. The pilot itself was intentionally too small to satisfy those final targets. Precision is reassessed across every valid family after the 30-replication core; extension is family-wide and direction-blind.

## Dynamic and censoring diagnostics

The queue is behaviorally active rather than a restatement of policy definitions. Across the development subset, mean U2C timely-review effectiveness changed from approximately 0.922 at load 0.6 to 0.601 at load 0.95 and 0.324 at load 1.2. Fail-open timeout semantics changed progression outcomes relative to the same fail-closed queue. All policies retained identical cohort hashes within each family-seed pair.

The pilot initially made a tempting but incorrect inference from the case-level right-censoring rate: ongoing recovery exposure and safe unresolved holds are deliberately open at the administrative cutoff, even when a timely decision was delivered. The analysis now scores timely decision service separately from terminal case restoration and retains stage-specific censoring reasons. It does not relabel an open consequence as resolved merely to improve completion rates.

Common random numbers help some estimands and not others; the observed paired-to-unpaired variance ratio spans both sides of one. Pairing is retained because it preserves case-level comparability, but no blanket variance-reduction claim is made.

## Artifact and generalizability checks

- A second synthetic profile identity ran through the unchanged engine with identical cohort, event, and telemetry results while keeping configuration identity distinct.
- The dummy-data pipeline emitted every cell and paired-estimate contract without reading pilot or confirmatory output.
- Capacity/timeout and information-workload figure prototypes render from stored aggregates and are visibly marked provisional.
- The fixed `RB-WORKED-TRACE-001` pair compiles with complete parameter receipts and renders a separate blinded packet and withheld expected profile.
- The Robodebt sufficiency review keeps documented, inferred, stylized, and unsupported claims separate.

## Stop-condition decision

No Slice 3 engineering stop condition fired: queue and access dynamics affect review and outcomes; the primary conclusions do not require scalar utility weights; paired outcome differences are distinguishable from replay/adapter failures; and projected runtime fits the precision rule. The design is an engineering freeze candidate, not an authorized confirmatory freeze. Independent packet-only returns from at least two eligible readers, invitation verification, literature/citation review, and the source-identity decision remain pre-freeze gates.
