# Execution Ledger

This ledger is the canonical slice-status record. Update it at the end of every slice and whenever a stop condition changes status.

## Slice Status

| Slice | Status | Commit | Verification | Residual risk |
| --- | --- | --- | --- | --- |
| 0. Source, construct, and claim contract | implementation, plan, and baseline gates passed — pre-freeze reader QA pending | `9cf836c` | automated Slice 0 and plan gates pass from declared environment | two eligible locked reader returns are not yet available; this blocks Slice 4, not Slice 1 engineering |
| 1. Case-neutral dynamic vertical slice | in progress — stored-record checkpoint passes | `33aaa09` initial checkpoint | 15 tests; 707-record closed bundle; both artifact hashes repeat | executable-rule signature/hash closure and stored canary/adapter receipts remain incomplete |
| 2. Stochastic engine and validation | pending | — | — | — |
| 3. Experiment pilot and freeze candidate | pending | — | — | — |
| 4. Confirmatory freeze | pending | — | — | — |
| 5. Confirmatory execution and analysis | pending | — | — | — |
| 6. Evidence packet and 10,000-word article | pending | — | — | — |

## Slice 0 Closeout Receipt

Status: automated implementation closeout complete; independent-reader acceptance remains an external pre-freeze gate

### Files changed or added

- Source grounding: `data/sources/robodebt/source_manifest.yaml`, `r_oci_early.yaml`, `r_oci_enhanced.yaml`, and `docs/ROBODEBT_CASE_STUDY.md`.
- Research controls: `docs/LITERATURE_AND_ORIGINALITY_MAP.md`, `docs/CONTINUITY_AND_CLAIM_BOUNDARY.md`, `docs/PREREGISTRATION.md`, `docs/WORKED_TRACE_SELECTION.md`, and `data/scenarios/worked_trace_spec_v1.yaml`.
- Execution controls: `docs/EXECUTION_LEDGER.md`, `docs/DEFERRED.md`, `scripts/validate_slice0.py`, `scripts/build_cold_reader_bundle.py`, and `docs/COLD_READER_DISTRIBUTION.md`.
- Reconciled boundaries: `README.md`, `AGENTS.md`, `docs/STUDY_PLAN.md`, `docs/CONFIGURATION_COMPILATION.md`, and `docs/PROCESS_RED_TEAM_PROTOCOL.md`.
- Previously completed Slice 0 specifications retained: formal model, P0 fixture, schema manifest, article outline, blinded packets, withheld profiles, and QA receipt.

### Source additions and provenance

- Royal Commission report/recommendation anchors.
- Royal Commission Deloitte OCI process-map nodes.
- Commonwealth Ombudsman 2017 and 2019 report anchors.
- Commonwealth Ombudsman 2023 income-apportionment terminology boundary.
- Services Australia Robodebt and 2025–27 automation/AI context.

The repository records authoritative URLs and citation-level locators but does not vendor remote PDF bytes. `content_hash: null` is explicit in the source manifest; the later freeze manifest must either record retrieved bytes or document why authoritative remote identifiers remain the source identity.

### Commands and results

| Command | Result |
| --- | --- |
| `python3 scripts/validate_plan.py` | pass: 8 slices, 3 primary hypotheses, 5 policies, 39 completion questions, 9 deferred items, 10,000-word ceiling |
| `python3 scripts/validate_slice0.py` | pass: 10 sources, 10 claims, 2 profiles, 5 YAML files, 93 closed diagnostics; configuration inventory, generic kernel boundary, compilation ownership, overlay binding, and temporal-bundle checks blocking |
| `python3 -m py_compile scripts/validate_slice0.py scripts/build_cold_reader_bundle.py` | pass |
| In-memory configuration-gate mutation audit | pass: rejected case-specific `DEBT_RAISED`, missing `CompiledConfiguration`, loose `Scenario.policy_refs`, and `SimulationCase.latent_income` |
| `python3 scripts/build_cold_reader_bundle.py --reader-id CR-001 --output outputs/cold_reader/CR-001.zip` | pass; archive SHA-256 `52981e5faa95ec62b137f8720c73a56b22eec350ae2cacb7d7c9d248d4762fae` |
| `python3 scripts/build_cold_reader_bundle.py --reader-id CR-002 --output outputs/cold_reader/CR-002.zip` | pass; archive SHA-256 `3b60fff959084f812b929aee914a3b0f44313e2d123993a793d60b05375764d3` |
| Zip allowlist and manifest inspection | pass: only protocol, P0 packet, transfer packet, blank receipt, instructions, and hash manifest |
| Markdown fence, trailing-whitespace, and local-link checks | pass |

Current candidate hashes after the flexible-kernel plan revision:

- source manifest: `fff48f4a818f29cd7ea5e7168c877c6697cd287a0714c2147b436814c2d87500`
- early profile: `248211b2b87c4372fc1eda307c4e6a81d9deb29b5b3d40e143490a24e17e720a`
- enhanced profile: `c9e2df36c3b37e134f6a98889b28cf15abc291253a0b0ee525519230e7fd14e1`
- case-study rendering: `72f91b2c13a012bfdc433c4dca6b2cdd9cf1ea99200850f53cad71e30f465b08`
- formal model: `da06b6c9896a961fcecbb87d0428d1cb7fa3703362a4c911f7a3434e8544389f`
- P0 fixture: `ef9d0b8c6593e35e68b0089538bcc5503e107a005c02087c6977dedbb2938992`
- protocol: `73fa13ad87fc98eba57fbdd34be7831bea62faa38e96fe26450a7d754e621274`
- schema manifest: `fef9e760bc7eabcaffb05b4774dd7a9a55e2059a1dca6e0bd41bac966db78359`
- worked-trace specification: `279d3888856f434a12a6be950cbff7b19d5745054aa5a3ead2bb59a5a2fd05a2`
- worked-trace selection rule: `4122731dbea9b3d64ba448445f43dee7e6af4c82c839f144db6f08a0eb304c92`
- study plan: `91ca2216a40beb61c9d960310b0c4357866f0a553ac21a08a8ada1d003d4ac48`
- preregistration skeleton: `d9c88cc777966e5b8d8cc8615cfe4bcf19d41d88d3a488550276cff0f8994510`
- configuration compilation contract: `208c5e0dbb66e8f70dc300c7cc373a7206e5863928eb56c07f3f3b93ada30b6d`
- Slice 0 validator: `12f656690bab510bfb03f63e7028aee224b2483794f288a530ed960da3c7d6e3`
- plan validator: `66a345f418d9d2229885dfd91fac99847f05fbb68b6e573ea98ca45f56acdd95`
- plan completion receipt: `e1423b9e979c8a151c2d27048d58801c8e34a05d4898ef8e0f560516ff234379`

### Golden traces or comparisons

- P0 expected profile exists but remains an oracle projection until Slice 1.
- Transfer-canary expected profile exists but remains a withheld oracle.
- Robodebt worked trace is prespecified as `RB-WORKED-TRACE-001`; executable output does not yet exist.

### Residual risks

- Independent cold-reader artifact QA cannot be self-certified by the drafting agent.
- The closed kernel/profile/adapter/overlay compilation boundary is now structurally specified and blocking in Slice 0, but it is not executable until Slice 1 creates the models and compiler.
- Source-profile implementation may expose schema gaps in Slice 1/2.
- Literature map is a structured scoping review, not a systematic review.
- Remote authoritative PDFs are referenced by official URL and locator but are not vendored or byte-hashed; the confirmatory freeze must either archive retrieved bytes or record a deliberate remote-identity rule.

### Gates promoted

The source/profile consistency, configuration-contract inventory, generic event/case boundary, compilation ownership, overlay-slot binding, mixed-precision temporal scope, blinded-packet leakage, YAML uniqueness, required-file, Markdown, and P0/Robodebt-boundary checks are blocking in `scripts/validate_slice0.py`. They are sufficient to enter Slice 1. Independent reader QA remains blocking for protocol `1.0` and Slice 4 confirmatory freeze. Protocol classification semantics remain pre-freeze candidate version `0.2`.

### Pre-Slice-1 architecture amendment — 2026-10-31

- Added closed records for temporal scopes, policy profiles, immutable source fixtures, application bindings and mappings, scenario overlays, parameter-binding receipts, compiled configurations, and generic case attributes.
- Replaced debt-, recovery-, customer-, and income-specific core event or case fields with generic event families and semantic case attributes; application-specific outcomes remain typed actions.
- Made scenarios and runs consume compiled configurations rather than loose policy references.
- Separated process capability ownership from active policy behavior and prohibited policies from creating undeclared topology.
- Defined deterministic precedence: documented values cannot be overwritten, unsupported source values are non-executable, overlays fill declared unbound slots only, and every runtime slot has exactly one owner.
- Added mixed-precision temporal-bundle support so the enhanced profile does not acquire a fictitious common activation date.
- Added isomorphic-vocabulary and non-isomorphic-topology canaries to the Slice 1 gate.
- Promoted these requirements from prose checks to structural validation. No simulation, pilot, or confirmatory result was inspected.

### Flexible-kernel plan revision — 2026-10-31

- Reclassified Robodebt as a thin source-grounded application adapter rather than an engine dependency.
- Required canonical synthetic profiles before institutional adapters.
- Separated unsupported historical fields from executable stylized scenario overlays.
- Added domain-renaming, adapter-swap, case-removal, and unsupported-default rejection gates.
- Moved independent reader QA from the Slice 1 entry path to the pre-freeze path; its evidentiary requirement is unchanged.
- No case, simulation, pilot, or confirmatory result was inspected in making this revision.

### Plan-completeness audit — 2026-10-31

- Added a uniform slice file/mutation contract, explicit forbidden work, executable verification commands, done conditions, failure diagnostics, and measured runtime/escalation budgets for Slices 0–7.
- Removed a stale case-specific `latent income` field from the generic kernel case contract and synchronized the CLI surface with planned reconciliation and evidence-packet commands.
- Registered invitation verification and authoritative-source byte identity as owned pre-freeze dependencies rather than leaving them as prose reminders.
- Added `docs/PLAN_COMPLETION_RECEIPT.md` and `scripts/validate_plan.py`. The validator checks eight slice contracts, three primary hypotheses, five policies, 39 completion questions, nine deferred items, and the 10,000-word budget.
- Registered the untracked repository baseline and environment receipt as `D-009`; it blocks Slice 1 mutation but does not make the study plan incomplete.
- Verification command: `python3 scripts/validate_plan.py`.
- Planning is execution-ready only; Slices 1–6 and all empirical outputs remain unexecuted.

### Baseline pre-commit review — 2026-10-31

- Candidate scope: 41 repository-owned files comprising research specifications, source/application fixtures, validators, package metadata, package placeholder, and directory placeholders. Generated cold-reader ZIPs, `.venv`, bytecode, caches, and editable-install metadata remain ignored.
- Safety review: no symlinks, unexpected binary candidates, private-key headers, common access-key/token forms, or credential assignments were found in the candidate set. No user-specific absolute path is stored in a committed artifact.
- Environment: CPython `3.14.4`; `macOS-26.5.2-arm64-arm-64bit-Mach-O`; local editable package `uncertainty-permission-simulation==0.1.0`.
- Installed dependencies: `numpy==2.5.4`, `orjson==3.13.0`, `pydantic==2.14.2`, `pydantic_core==2.50.2`, `PyYAML==6.0.3`, `pytest==9.2.0`, `annotated-types==0.8.0`, `iniconfig==2.3.1`, `packaging==26.3`, `pluggy==1.7.0`, `Pygments==2.21.0`, `typing_extensions==4.16.0`, and `typing-inspection==0.4.4`.
- Fresh-environment regression: `./.venv/bin/python scripts/validate_plan.py`, `./.venv/bin/python scripts/validate_slice0.py`, and Python compilation all pass. The environment rehearsal exposed and fixed an overbroad Markdown scan that had entered `.venv`; repository Markdown validation now excludes `.git`, `.venv`, `build`, and `dist`.
- There are no simulator tests yet because Slice 1 has not begun; this receipt certifies the plan/source baseline only.

### Commit receipt

The reviewed 41-file Slice 0 baseline is commit `9cf836cb15edba29235abc60b4f754d311343fe3` (`Establish simulation study baseline`). The repository-local author name is `Eli`; the pre-existing configured email was retained. This follow-up ledger update closes `D-009` and records the immutable baseline SHA. Independent reader receipts remain a separate mandatory pre-freeze dependency.

## Slice 1 In-Progress Checkpoint

Status: deterministic schema/compiler/process checkpoint implemented; Slice 1 not complete

Checkpoint commit: `33aaa0916578a8a5ce692993025a26e36e9296ec` (`Begin Slice 1 deterministic vertical slice`)

### Implemented

- Manifest-driven Pydantic inventory for all declared payload kinds, strict record metadata/envelopes, schema identity, source-basis and provenance checks, canonical hashing, set-order normalization, and binary-float rejection.
- Deterministic configuration compilation with process/policy capability separation, documented-value protection, unsupported-slot handling, one receipt per runtime slot, and zero-unresolved-slot enforcement.
- Case-neutral event queue, stable priority ordering, causal-key collision rejection, microstep bound, U1/U2C/U2O deterministic behavior, trace-derived metrics, and P0 F0–F5/helper report rendering.
- Nine trace arms covering the seven required golden behaviors, the isomorphic vocabulary canary, non-isomorphic topology canary, and thin R-OCI-Early adapter smoke compilation.
- A canonical 707-record bundle containing compiled-configuration inputs, parameter receipts, trace specifications, per-event pre/post process states, events, total dispositions, traces, prespecified expected results, metrics, P0 assessments, and diagnostics.
- Recursive reference resolution and cycle rejection, nine independent expected-versus-actual trace comparisons, and 18 P0 report-row links to stored assessments and diagnostics.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 15 tests |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 trace arms |
| repeated smoke run | summary SHA-256 `a5a37cc0c70099126e66d4ccf864cc6a119760cd32f74e2ab20d8ad2a9df75b2`; record bundle SHA-256 `5343ac2baa9170737717b285449f1bdb45f95dbd8b23c1da618e9717ffc09842`; both identical across reruns |
| `./.venv/bin/python scripts/validate_plan.py` | pass |
| `./.venv/bin/python scripts/validate_slice0.py` | pass after status synchronization |

### Remaining before Slice 1 closeout

- Enforce every `ExecutableRule` against its manifest-declared implementation kind, version, required parameters, role/cardinality/schema bindings, output schema, and actual immutable code-artifact hash.
- Validate typed reference-target schemas where the manifest declares them, rather than only identity/version existence and graph acyclicity.
- Materialize stored expected-versus-actual receipts for the isomorphic vocabulary canary, non-isomorphic topology canary, and R-OCI-Early adapter compilation; the current core golden traces already have stored expected results.
- Rerun all gates, record runtime and artifact hashes, update this ledger, and create the required Slice 1 completion commit.
