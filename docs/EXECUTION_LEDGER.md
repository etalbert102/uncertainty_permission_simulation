# Execution Ledger

This ledger is the canonical slice-status record. Update it at the end of every slice and whenever a stop condition changes status.

## Slice Status

| Slice | Status | Commit | Verification | Residual risk |
| --- | --- | --- | --- | --- |
| 0. Source, construct, and claim contract | implementation, plan, and baseline gates passed — pre-freeze reader QA pending | `9cf836c` | automated Slice 0 and plan gates pass from declared environment | two eligible locked reader returns are not yet available; this blocks Slice 4, not Slice 1 engineering |
| 1. Case-neutral dynamic vertical slice | complete | `93e2da6` | 27 tests; 726-record closed bundle; three stored validation receipts match; both artifact hashes repeat | stochastic execution and empirical validation remain Slice 2 work |
| 2. Stochastic engine and validation | in progress — shared review queue and deadline races pass | `dc4fec0` checkpoint | 82 tests; repeatable five-policy, globally ordered review-queue smoke artifact; all prior gates pass | no final-action timeout dynamics, later-stage queues, full analytical benchmark, or reference-simulator comparison yet |
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
- formal model: `4326b4e97046a71a7605442bfcaa5b2f662c5aa4f1f4242a6dd4259d0da0d0e5`
- P0 fixture: `ef9d0b8c6593e35e68b0089538bcc5503e107a005c02087c6977dedbb2938992`
- protocol: `73fa13ad87fc98eba57fbdd34be7831bea62faa38e96fe26450a7d754e621274`
- schema manifest: `e5de5c8ac638dc99adbecaa287affadf367ae24211452c4db093c9ef003b493e`
- worked-trace specification: `279d3888856f434a12a6be950cbff7b19d5745054aa5a3ead2bb59a5a2fd05a2`
- worked-trace selection rule: `4122731dbea9b3d64ba448445f43dee7e6af4c82c839f144db6f08a0eb304c92`
- study plan: `076c1092741c3da82025167a431f847187cde39cb6ab12751d7052f77626467d`
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

## Slice 1 Closeout Receipt

Status: complete

Checkpoint commit: `33aaa0916578a8a5ce692993025a26e36e9296ec` (`Begin Slice 1 deterministic vertical slice`)

Stored-record checkpoint commit: `f27921764526dd13612fd34e11610cf4434a6ed8` (`Materialize Slice 1 stored record bundle`)

Executable-rule checkpoint commit: `0bb87c2b9431512e1df43d2508825e1ad7912b9e` (`Close executable rule registry`)

Typed-reference checkpoint commit: `b880f45cb031e41f5f39490febf37e95ad1c8c60` (`Enforce typed reference targets`)

Complete reference-closure commit: `c016e516479d60d757e74196c0efe281962a7e50` (`Complete typed reference closure`)

Stored-validation-receipt completion commit: `93e2da62f5d4f4a003846c152fa4dd7811d7b38d` (`Close Slice 1 with stored validation receipts`)

### Implemented

- Manifest-driven Pydantic inventory for all declared payload kinds, strict record metadata/envelopes, schema identity, source-basis and provenance checks, canonical hashing, set-order normalization, and binary-float rejection.
- Deterministic configuration compilation with process/policy capability separation, documented-value protection, unsupported-slot handling, one receipt per runtime slot, and zero-unresolved-slot enforcement.
- Case-neutral event queue, stable priority ordering, causal-key collision rejection, microstep bound, U1/U2C/U2O deterministic behavior, trace-derived metrics, and P0 F0–F5/helper report rendering.
- Nine trace arms covering the seven required golden behaviors, the isomorphic vocabulary canary, non-isomorphic topology canary, and thin R-OCI-Early adapter smoke compilation.
- A canonical 726-record bundle containing compiled-configuration inputs, parameter receipts, trace specifications, nonempty typed representations, compatible-state support, per-event pre/post process states, events, total dispositions, traces, prespecified expected results, metrics, P0 assessments, diagnostics, the R-OCI-Early source fixture, and three validation receipts.
- Recursive reference resolution and cycle rejection, nine independent expected-versus-actual trace comparisons, and 18 P0 report-row links to stored assessments and diagnostics.
- A static 16-callable implementation registry with exact manifest inventory matching and per-implementation hashes bound to the complete code artifact; dynamic imports and narrative evaluation are absent.
- Exact rule validation for implementation kind/version, required and unknown parameters, parameter kinds and closed values, input roles/cardinalities/schema sets, and output schema. Nested set-semantics paths now canonicalize before rule-record hashing.
- A stored routing-rule signature with four typed parameters, four declared input roles, a matching output schema, and a top-level receipt linking its code-artifact and rule-record hashes.
- A complete manifest role matrix covers 254 reference-bearing payload fields through 178 shared roles or payload-local overrides. Twenty-four intentionally polymorphic roles are marked `any`; omission, stale roles, nested pseudo-paths, duplicate targets, and unknown target kinds fail manifest validation.
- The golden bundle exercises nine nonempty representation-to-field edges spanning both `Claim` and `UntypedField`, uses separate preserve/fallback transformation rules, stores three matching rule receipts, and records a reference-target receipt covering 4,240 typed and 51 polymorphic references.
- The isomorphic-vocabulary receipt stores expected and observed semantic projection, event order, metrics, and artifact-identity checks. The non-isomorphic-topology receipt stores the expected and observed stage order, event order, compiler identity, topology difference, and unresolved-slot result. The R-OCI-Early adapter receipt stores configuration and mapping identities, compiler identity, kernel case-identifier absence, exact binding slots and provenance, unresolved slots, and unsupported-default use.
- Receipt envelopes recompute exact deep equality from the stored expected and observed values; a producer cannot label a mismatch as a match. A mutation test changes one observed canary field and verifies that the stored receipt becomes `mismatch`.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 27 tests, including missing role, malformed nested path, wrong local and global target kinds, nonempty union targets, rule mutations, receipt mutation, and cycle rejection |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 trace arms |
| repeated smoke run | pass in 0.24 seconds; summary SHA-256 `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739`; record bundle SHA-256 `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8`; both identical across reruns |
| rule-registry hash closure | pass: 16 manifest declarations equal 16 static callables and every declared SHA-256 reproduces; registry artifact SHA-256 `2ca97cbecfcf511dd502da2e85ec0cd7b06fa83b43ad0423cd1fce1d2a5a9556` |
| `./.venv/bin/python scripts/validate_plan.py` | pass |
| `./.venv/bin/python scripts/validate_slice0.py` | pass: 10 sources, 10 claims, 2 profiles, 6 YAML files, 95 closed diagnostics |

### Closeout assessment

- The Slice 1 done condition is satisfied: all core expected results and all three architecture/application checks are stored, reference closed, deterministic, and gate checked.
- Slice 2 owns the stochastic engine, distributional validation, telemetry, and stochastic validation receipts. No stochastic or empirical result is claimed by this closeout.
- Independent cold-reader QA remains an external pre-freeze requirement and does not become satisfied through simulator self-tests.

## Slice 2 In-Progress Checkpoint

Status: keyed-random finite-cohort substrate implemented; Slice 2 not complete

Checkpoint commit: `3e43494903409af0793ba953f8dfe321f9b4dad4` (`Begin Slice 2 keyed stochastic substrate`)

### Scope and fact ownership

- This increment owns only shared exogenous stochastic facts: closed draw-family IDs, stable `(seed_id, case_id, event_family_id, draw_index)` identities, latent unit-interval values, finite-cohort construction, and replay telemetry.
- Policy-specific engagement mappings, event paths, queue behavior, evidence acquisition, deadlines, actions, and outcomes remain downstream consumers. This checkpoint does not encode those semantics early.
- Every executable value in the smoke run is synthetic or identified by the separately versioned stylized overlay ID. No historical parameter is inferred or calibrated.

### Implemented

- Added 13 closed draw families covering initiation, administrative access, notice and engagement traits, assistance/review/reassessment service, evidence retrieval, and deadline extension.
- Added SHA-256 keyed uniform draws derived directly from the seed and stable draw key. Draw request order, unrelated branch draws, and case input order cannot advance or shift another draw.
- Added strict key validation, open-interval decimal values, stable draw IDs and content hashes, draw caching/deduplication, and manifest-level rejection of duplicate draw-family IDs.
- Added a policy-neutral finite-cohort generator with deterministic case ordering, arrival times inside the declared initiation window, per-case draw hashes, family counters, duplicate-key telemetry, and a cohort artifact hash.
- Added `cohort` CLI execution and `experiments/configs/stochastic_smoke_v1.yaml`. Its generated artifact is explicitly labeled as a stochastic-substrate smoke output with no policy, queue, empirical, or historical outcome claim.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_random_streams.py tests/unit/test_simulator.py` | pass: 24 focused replay, key-validation, manifest, divergent-branch, case-order, seed, overlay-provenance, cohort, and telemetry tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 51 tests in 0.29 seconds; all Slice 1 regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: 5 cases, 65 unique keyed draws, zero duplicate keys; repeated artifact SHA-256 `f9f7b0faea380798d43a71c33e1450583f3818ffaf0913e738691987b0a026c4` |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: Slice 1 deterministic artifact unchanged |
| `./.venv/bin/python scripts/validate_plan.py` | pass |
| `./.venv/bin/python scripts/validate_slice0.py` | pass: 10 sources, 10 claims, 2 profiles, 7 YAML files, 95 closed diagnostics |

### Remaining after the keyed-random substrate checkpoint

- Implement U0, U1, U2C, U2O, and U3 mappings from shared exogenous traits to policy-specific engagement and events.
- Implement assistance, review, and reassessment resources and queue disciplines, then evidence, deadline, action, correction, censoring, and restoration behavior.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Add exact hand traces, limiting cases, analytical queue tolerances, a slower reference simulator, stored stochastic receipts, and run-level artifacts.
- Do not enter pilot scenario selection or treat this smoke artifact as a substantive simulation result.

## Slice 2 Policy and Engagement Checkpoint

Status: all five engagement-stage mappings implemented through compiled configurations; Slice 2 not complete

Checkpoint commit: `67880070bea0e346cdd20890415738e3ab476665` (`Add compiled policy engagement traces`)

### Scope and fact ownership

- The shared cohort continues to own exogenous case facts. Each policy consumes the same stable keyed draws and may diverge only through declared policy behavior and overlay-owned parameters.
- The compiler remains the execution boundary. Engagement execution rejects an uncompiled configuration, unresolved parameter slots, an overlay identity mismatch, receipt-value drift, or provenance drift.
- This checkpoint ends at review routing. It does not simulate queue service, review completion, final action, correction, restoration, or a historical outcome.

### Implemented

- Closed U0, U1, U2C, U2O, and U3 behavior ownership for imputation, evidence-status preservation, review scope, fail-open semantics, assistance, extensions, and proactive evidence retrieval.
- Added a stochastic process profile and stylized overlay bindings for notice and engagement probabilities, effort thresholds and bonuses, extension timing, evidence retrieval, and the already declared review inputs.
- Mapped each shared case into deterministic, case-neutral engagement traces with stable causal keys for notice, access, response, evidence, representation, retrieval, and review-routing events.
- Preserved adequate evidence as period-specific evidence; restricted imputation labels to imputed representations; routed U2C and U2O through review for every progressing case and U3 through review only while unresolved.
- Added separate, non-composite counts and rates for notice failure, response, adequate response evidence, assistance, extension, retrieval, and review routing.
- Expanded the smoke CLI to compile and execute each policy, emit configuration identities and per-policy telemetry, and state the artifact's engagement-only claim limit.
- Updated the README results-boundary gate to recognize the implemented engineering simulator while still requiring explicit no-pilot, no-confirmatory-result, and non-empirical claim limits.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 42 focused policy, pairing, replay, causal-key, configuration-boundary, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 69 tests in 0.31 seconds; all Slice 1 regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: 5 cases, 5 compiled policy runs, 65 unique keyed draws, zero duplicate keys; repeated artifact SHA-256 `ae0ae23a6aac154e65cfaf37154f140ec45bbb35efd149e0ce051b4738145c57` |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 deterministic traces |
| `./.venv/bin/python scripts/validate_plan.py` | pass: 8 slices, 3 primary hypotheses, 5 policies, 39 audit questions, 9 deferred items, 10,000-word ceiling |
| `./.venv/bin/python scripts/validate_slice0.py` | pass: 10 sources, 10 claims, 2 profiles, 7 YAML files, 95 closed diagnostics |
| `python -m py_compile` over the five modified runtime modules | pass |
| `./.venv/bin/python -m py_compile scripts/validate_slice0.py` | pass |
| Case-name scan over generic policy, simulator, and metric modules | pass: no Robodebt or R-OCI identifiers |

### Remaining before Slice 2 closeout

- Implement assistance, review, and reassessment service resources with explicit capacity and queue disciplines; make completion compete with deadlines.
- Extend routed traces through final action, recovery, correction, censoring, and restoration while preserving shared exogenous draw identity across divergent paths.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Add exact stochastic hand traces, limiting cases, analytical queue tolerances, a slower reference simulator, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this engagement smoke artifact as a substantive simulation result.

## Slice 2 Shared Review Queue Checkpoint

Status: deterministic shared review scheduling and service-deadline competition implemented; Slice 2 not complete

Checkpoint commit: `dc4fec05889778a0cd4f61779de0c8df0a10c7d0` (`Add shared review queue scheduling`)

### Scope and fact ownership

- The simulator owns scheduling, stable server assignment, global event order, and queue telemetry. Policy profiles continue to own whether a case enters review and what a later timeout will do.
- The shared `review_service` keyed draw owns each case's latent service requirement. The current stylized mapping is explicit: service demand equals that shared unit-interval draw multiplied by the overlay's `review_service_time` value.
- The separately compiled `review_service_window` begins at queue entry and supplies this checkpoint's review-service deadline. It is not a historical parameter or a complete action/correction horizon.
- This checkpoint records whether review completed by its service deadline but deliberately stops before applying fail-closed holds, fail-open progression, or another final action.

### Implemented

- Added typed, immutable queue configuration, request, visit, run, and telemetry contracts with blocking diagnostics for malformed configurations, requests, duplicate identities, and unsupported disciplines.
- Added finite-cohort, work-conserving FIFO scheduling with explicit positive integer capacity, deterministic case/request ties, stable server IDs, input-order invariance, and a canonical schedule hash.
- Added the compiled `review_service_window` overlay slot and generated `REVIEW_STARTED`, `REVIEW_COMPLETED`, and review-specific `DEADLINE_REACHED` events from shared review draws.
- Added one globally ordered cohort event stream per policy; each stored case trace is tested as the exact projection of that system trace.
- Preserved identical U2C/U2O requests and schedule hashes before timeout semantics diverge. Capacity changes alter service timing without altering case draw hashes.
- Froze exact-boundary behavior: a review completing at its deadline is timely, and `REVIEW_COMPLETED` precedes `DEADLINE_REACHED` under the closed priority registry.
- Added separate queue counts, conditional start/completion/timeliness rates, wait-time metrics, queue visits, system events, and the review-queue-only claim boundary to the smoke artifact.
- Added a hand-computable finite-window capacity case: four two-unit jobs exactly fill two servers over a four-unit window, while a fifth job exceeds the `W > cH` bound and finishes late.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 49 focused queue, pairing, replay, configuration, policy, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 5 capacity, deadline, system-trace, policy-pairing, and hand-calculation tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_events.py` | pass: 4 event-order and causal-key tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 82 tests in 0.33 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: 5 cases, 5 compiled policy runs, 65 unique keyed draws, zero duplicate keys; repeated artifact SHA-256 `ad407e556aaabb972de89378b7aa4c52d060eb800809814c1c014ac603f15414` |
| smoke queue inspection | U2C/U2O schedule hashes identical; 5 queued, 1 timely, 4 late under the declared stylized overlay; U3 queues 2, with 1 timely and 1 late |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 deterministic traces |
| `./.venv/bin/python scripts/validate_plan.py` | pass: 8 slices, 3 primary hypotheses, 5 policies, 39 audit questions, 9 deferred items, 10,000-word ceiling |
| `./.venv/bin/python scripts/validate_slice0.py` | pass: 10 sources, 10 claims, 2 profiles, 7 YAML files, 95 closed diagnostics |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Apply policy-owned timeout semantics and evidence support to produce final hold, progress, or request-evidence decisions without conflating review completion with valid authorization.
- Extend the globally ordered trace through action execution, external exposure, correction, censoring, and restoration.
- Wire assistance and reassessment resources only when their owning process stages exist; do not infer staffed historical capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand the analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this review-queue smoke artifact as a substantive simulation result.
