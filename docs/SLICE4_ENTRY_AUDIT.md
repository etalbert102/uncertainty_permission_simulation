# Slice 4 Entry Audit

Date: 2026-11-01

Status: historical entry audit; all three blockers closed and the Slice 4 freeze was issued on 2026-11-01

## Entry evidence

- Slices 0–3 are committed and their automated gates pass.
- The Slice 3 pilot predicts that the 108-family, 30-replication, 80-case core fits the declared 24-hour runtime ceiling.
- The pilot's direction-blind precision projection supports the frozen candidate of 30 minimum and 60 maximum paired replications.
- Literature, venue, source-identity, application-sufficiency, adapter-swap, and external-dependency decisions are closed.
- No confirmatory output exists or has been inspected.

## Candidate contracts created at entry

`experiments/configs/confirmatory_v1.yaml` carries forward the pilot decisions without inspecting results: all 108 families, all five policies, 80 cases, 30 initial paired replications, a family-wide extension to 60 when any applicable primary metric misses its target, day-650 cutoff, stable seed derivation, separate censoring reasons, and no composite utility.

`experiments/configs/sensitivity_information_latency_v1.yaml` prespecifies one non-core sensitivity in which the evidence-retrieval latency scale doubles from 10 to 20. It remains separate from the core and cannot be pooled into primary estimates.

`requirements-lock.txt` records the exact development environment from which the freeze candidate is being assembled. The final freeze manifest must also record interpreter and platform identity.

## Gaps found before freeze

### S4-B001 — numerical outcome contract

The study plan and preregistration promise disposition and amount error relative to a stylized full-information oracle. The implemented simulator currently records evidentiary support, permission, progression, exposure, correction, restoration, and process metrics, but it does not own a latent numerical amount or a full-information amount oracle. Freezing now would falsely certify a promised outcome that cannot be produced.

Required resolution before protocol `1.0` and the manifest:

- either add a visibly stylized, independently owned numerical-oracle model with keyed latent draws, overlay-owned parameters, policy-blind scoring, tests, and stored dummy-analysis fields; or
- narrow the preregistered numerical claims before freeze and reconcile the plan, outline, metrics, and article contribution accordingly.

**Resolution — 2026-11-01:** closed by deliberate narrowing before freeze. The plan, preregistration, article outline, case-study claim table, repository instructions, candidate configs, tests, and public status now exclude latent monetary entitlement, amount-error, amount-recovered, and historical debt-magnitude claims. The existing process outcomes become the complete confirmatory outcome contract. This is a pre-result scope decision; no confirmatory output existed or was inspected.

### S4-B002 — matched negative-control execution

P0 supplies a semantic null and routing-invariance control, and the simulator has limiting-case tests. The confirmatory pipeline does not yet emit one closed, stored receipt covering the five prespecified negative-control IDs in the candidate config. A test existing somewhere in the suite is not sufficient evidence for the article's negative-control result.

Required resolution: implement deterministic control execution and a stored receipt that keeps controls separate from the 108-family primary count and fails on any unexpected robust-permission violation.

**Resolution — 2026-11-01:** closed by `data/golden_traces/slice4_negative_control_receipt_v1.json`. The deterministic harness executes all five controls in the candidate config, records the applicable pairwise-permission or action-support rule, keeps `primary_family_count` at zero, rejects an unexpected robust-permission violation, and replays byte-equivalently. Both candidate configs verify the stored receipt hash before validating.

### S4-B003 — freeze and run machinery

The repository does not yet implement `verify-freeze`, `scripts/verify_repo.py`, or the append-only confirmatory run/reconcile/analyze path named in the canonical plan. These commands must exist and be mutation-tested before their code is hashed.

**Resolution — 2026-11-01:** closed by the manifest-gated freeze verifier, repository verifier, append-only run/resume path, reconciliation and analysis receipts, deterministic figures, six focused machinery regressions, and the 178-test full suite. The promoted baseline is commit `0b8e890b0ed7a773cfaf328997a3e865ded3457a`; `docs/FREEZE_MANIFEST.json` hashes 77 files and has manifest identity `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c`.

## Entry stop decision

Do not promote the protocol, mark either config ready, create `docs/FREEZE_MANIFEST.json`, or execute a confirmatory case while S4-B003 remains open. Candidate validation and deterministic negative-control replay are permitted because they enumerate or test frozen inputs without executing or inspecting a confirmatory scenario outcome.

This stop condition was satisfied before promotion. Protocol/formal version `1.0`, ready configs, and the immutable manifest were created only after S4-B003 closed. No confirmatory output existed at issuance.
