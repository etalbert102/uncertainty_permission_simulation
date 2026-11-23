# Freeze 5 Reporting Decomposition and Replay Plan

Status: bounded repair complete locally; public activation deferred

Date opened: 2026-11-22

## 1. Goal

Create a versioned Freeze 5 reporting layer that separates evidential insufficiency from missing timely review authorization, accounts for the sequential U3 evidence-acquisition stages, and discloses the post-result origin of the repaired outcomes. Replay the unchanged stochastic process, prove event-level identity with Freeze 4, and revise the manuscript only after the new receipts pass.

## 2. Current gap

The Freeze 4 aggregate `unsupported_progression` is the union of two analytically distinct failures: progression without sufficient evidence and progression without required timely authorization. Runtime telemetry owns both facts, but the stored attempt row does not preserve their intersection or exclusive components. The compact output therefore cannot decompose the reported 0.476 without deterministic replay.

U3 also records adequate response evidence, proactive retrieval, retrieved evidence, and post-review evidence requests at runtime, but its stored rows report only the final decision state. This makes stage accounting unavailable and invites causal interpretation of a bundled policy comparison.

## 3. Non-goals

- Do not change a policy, process transition, scenario, parameter, seed, queue, timeout, case, evaluation specification, or random stream.
- Do not add an assistance-only or retrieval-only policy arm.
- Do not estimate independent causal contributions for assistance and retrieval.
- Do not calibrate the model to Robodebt or convert designed-scenario quantities into historical estimates.
- Do not overwrite Freeze 4 attempts, analyses, manifests, or receipts.
- Do not make the repository public without separate project-lead authorization.

## 4. Metric contract

For every progression, store an exclusive four-state partition:

1. evidence sufficient and authorization satisfied;
2. evidence insufficient only;
3. required timely authorization missing only; and
4. both evidence insufficient and required timely authorization missing.

The existing `unsupported_progression` remains the union of states 2–4. The three failure states must sum exactly to it. Evidentially unsupported progression is states 2+4; unauthorized progression is states 3+4. Rates use initiated cases as the denominator.

For every policy, store the sequential evidence-stage counts already owned by runtime telemetry:

- adequate response evidence before proactive retrieval;
- proactive retrieval requests;
- evidence successfully retrieved;
- evidence unresolved after response and retrieval;
- review requests and evidence-request actions.

For U3, adequate response evidence plus retrieved evidence must equal supported progression. Unresolved after acquisition must equal review requests. Timely review may change the recorded decision state to `evidence_requested`; it does not resolve evidence because the model contains no response cycle after that request.

Stage accounting describes the declared sequence. It is not an assistance-versus-retrieval causal decomposition. Any U3–U0 pre-retrieval difference is a paired policy-stage contrast, not a general component effect.

## 5. Deviation disclosure

Freeze 5 is post-result change control, not preregistration. Freeze 4 was itself designed after inspection of Freeze 3 results. The manuscript must state that the Freeze 4 unresolved-non-progression contrast is numerically the sign-reversed Freeze 3 recovery-exposure contrast under a repaired outcome label and that Freeze 5 adds reporting observability after external review. Behavioral identity does not remove outcome-selection risk.

## 6. Slice protocol

### Slice 0 — Contract and baseline

- Record this plan and the opening ledger entry.
- Verify Freeze 4, the release gate, and the 209-test baseline.
- Stop if the baseline is not reproducible.

### Slice 1 — Reporting schema and tests

- Add the exclusive progression partition and evidence-stage counts to stored rows, cell summaries, and analysis receipts.
- Add focused partition, overlap, nullability, row-order, and label-mutation tests.
- Advance config, negative-control, output-root, and active-freeze identities without changing stochastic inputs.
- Archive and attest Freeze 4 before retiring it as active.

### Slice 2 — Freeze and replay

- Commit reviewed executable inputs from a clean tree.
- Issue Freeze 5.
- Run core and sensitivity suites at the frozen 30 replications.
- Reconcile, analyze, replay, and verify append-only behavior.

### Slice 3 — Differential proof and reporting

- Pair every Freeze 4 and Freeze 5 attempt.
- Require exact equality of cohort hashes, event hashes, event order, timestamps, actions, queues, and all unchanged outcomes.
- Permit only schema identities and newly stored reporting fields to differ.
- Produce compact decomposition receipts and update Table 3/Figure 3 data as needed.

### Slice 4 — Manuscript and release package

- Distinguish rule-level Robodebt F1 failure from case-level unassessability.
- Report the fail-open partition without calling authorization-only cases evidentially unsupported.
- Present U3 stage accounting without component-causal percentages.
- Remove the abstract’s selective factor-margin claim, disclose Freeze 3–5 change control, and apply the listed clarity edits.
- Regenerate the APA Word manuscript, inspect every page, update receipts, and run all repository, freeze, release, accessibility, archive, image, and section gates.

## 7. Stop conditions

Stop if any event hash, queue trace, action, timestamp, existing metric, case identity, or random-stream receipt differs between Freeze 4 and Freeze 5; if an exclusive partition fails conservation; if a U3 stage identity fails; if a new result is not traceable to a stored row; or if the manuscript promotes stage accounting to an independent causal effect.

## 8. Completion evidence

Completion requires a verified Freeze 5 manifest; reconciled core and sensitivity analyses; a machine-readable and narrative Freeze 4/5 differential audit; updated Table 3 data and manuscript; a regenerated and fully inspected APA copy; updated evidence, submission, and audit receipts; passing tests; and a release-gate pass. The execution ledger must record commands, results, residual risks, and commit identities for every slice.

## 9. Ledger

| Slice | Status | Evidence |
| --- | --- | --- |
| 0. Contract and baseline | complete | Freeze 4 verified; release gate passed; plan and Slice 0 validators passed; 209 tests passed |
| 1. Reporting schema and tests | complete | exclusive failure and evidence-stage fields implemented; development rehearsal and 218 tests pass; Freeze 4 archived and attested |
| 2. Freeze and replay | complete | both 16,200-attempt suites reconcile at 30 replications; deterministic reruns retained all attempts and reproduced analysis hashes |
| 3. Differential proof and reporting | complete | 32,400-pair behavioral audit passes; Table 3 and Figure 3 regenerated from Freeze 5 analysis |
| 4. Manuscript and release package | complete | manuscript, supplement, APA export, evidence packet, readiness receipt, and repair receipt synchronized; 41 pages inspected; 218 tests and release gate pass |
