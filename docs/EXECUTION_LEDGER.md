# Execution Ledger

This ledger is the canonical slice-status record. Update it at the end of every slice and whenever a stop condition changes status.

## Slice Status

| Slice | Status | Commit | Verification | Residual risk |
| --- | --- | --- | --- | --- |
| 0. Source, construct, and claim contract | implementation, plan, and baseline gates passed — pre-freeze reader QA pending | `9cf836c` | automated Slice 0 and plan gates pass from declared environment | two eligible locked reader returns are not yet available; this blocks Slice 4, not Slice 1 engineering |
| 1. Case-neutral dynamic vertical slice | complete | `93e2da6` | 27 tests; 726-record closed bundle; three stored validation receipts match; both artifact hashes repeat | stochastic execution and empirical validation remain Slice 2 work |
| 2. Stochastic engine and validation | in progress — consequence-vector restoration passes | `75a88ea` checkpoint | 131 tests; repeatable five-policy restoration/censoring smoke artifact; all prior gates pass | no monetary consequence coordinate, earlier-stage censoring, full analytical benchmark, or reference-simulator comparison yet |
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

## Slice 2 Timeout Action Checkpoint

Status: policy-owned pre-exposure dispositions and fail-open/fail-closed timeout actions implemented; Slice 2 not complete

Checkpoint commit: `ade893aa7f95f7affc26a8200a0d6d1fb4fcd7c1` (`Apply policy timeout actions`)

### Scope and fact ownership

- Policy behavior owns the action selected after routing or review timeout. The simulator owns when the decision occurs and emits the resulting authorization, computation, and progression events.
- Evidentiary sufficiency and timely review authorization remain separate facts. Overall progression support requires both when review is mandatory, but the artifact also reports each axis independently.
- Gate safety applies only to cases with a configured review dependency. A no-review policy is not counted as gate-safe merely because its action happened to be supported.
- This checkpoint ends at executed progression. It does not equate functional permission, action computation, or progression with external exposure, recovery, debt, legality, or historical outcome.

### Implemented

- Added a closed final-disposition contract for `progress`, `hold`, and `request_evidence`, with evidence status, review requirement, timely completion, recorded authorization, timeout status, gate state, functional permission, and stable reason codes.
- Corrected the prior generic decision seam so visible uncertainty cannot accidentally suppress U2O's declared fail-open timeout; the deterministic Slice 1 fixture continues through a compatibility wrapper and retains its stored outputs.
- U0 progresses only with sufficient evidence and otherwise holds; U1 progresses through either sufficient evidence or declared imputation; U2C holds on review timeout; U2O progresses on the same timeout; U3 progresses with acquired evidence and otherwise requests evidence or holds.
- Added `EXTERNAL_AUTHORIZATION_RECORDED` only for timely, evidence-sufficient reviewed progression, followed by `ACTION_COMPUTED` and, when selected, `PROGRESSION_EXECUTED` in the frozen event order.
- Preserved branch-independent action causal keys across U2C/U2O while allowing only U2O's late cases to add progression descendants.
- Added separate counts and rates for holds, information requests, progression, full support, evidentiary support, evidentiary failure, missing authorization, gate safety, fail-open progression, and fail-closed holds.
- Added blocking run-integrity checks proving that dispositions partition cases, support classifications independently partition progression, and gate-safe/unsafe classifications partition only gate-applicable cases.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 53 focused policy, action, pairing, replay, support, configuration, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 8 queue/action integration tests, including matched U2 timeout divergence and evidence-versus-authorization separation |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 89 tests in 0.34 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: repeated artifact SHA-256 `7765db0d62b09df357fdcb409de2a5790971f51495eff4d7fe20c5044d1596ae` |
| smoke action inspection | U2C: 4 timeout holds and 1 request-evidence action; U2O: the same schedule yields 4 fail-open progressions and 1 request-evidence action; U1: 1 fully supported and 4 evidentially unsupported progressions |
| support-axis inspection | U2O's 4 late progressions all lack timely authorization; 1 has sufficient evidence and 3 also lack sufficient evidence |
| gate inspection | U2C: 5/5 applicable cases gate-safe; U2O: 1/5 gate-safe and 4/5 gate-unsafe; U3: 2/2 applicable cases gate-safe |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Extend only executed progression into external consequence and recovery states; preserve the distinction among permission, computation, execution, and exposure.
- Add correction requests, reassessment capacity, administrative cutoff/censoring, and dimension-specific restoration.
- Wire assistance capacity only through a declared process stage and preserve its engagement effect separately from review capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this pre-exposure action artifact as a substantive simulation result.

## Slice 2 Exposure and Recovery-Initiation Checkpoint

Status: executed progression extends through typed external exposure and recovery initiation; Slice 2 not complete

Checkpoint commit: `cc773a4f2b7c60f17c9cc4a9123a5fe7dbe8e023` (`Add recovery exposure progression`)

### Scope and fact ownership

- Only `PROGRESSION_EXECUTED` may create `EXTERNAL_CONSEQUENCE_STARTED`; functional permission and `ACTION_COMPUTED` remain non-exposure states.
- The upstream action decision owns evidentiary sufficiency, timely authorization, support, and reason codes. Consequence events carry those values and their source causal keys without re-deriving them.
- The typed `recover` action means operational recovery or collection initiation. It is distinct from corrective reassessment and `RESTORATION_EXECUTED`.
- `external_consequence_delay` and `recovery_start_delay` are stylized or sensitivity inputs bound through the compiled overlay. They are not historical estimates, and this checkpoint models neither recovery service competition nor exposure amount.

### Implemented

- Added typed stochastic-process recovery capability and action references plus nonnegative external-consequence and recovery-start timing slots.
- Added one external-consequence start and one recovery-active update for each and only each executed progression, with stable progression-to-consequence-to-recovery causal references.
- Preserved the frozen same-time order `ACTION_COMPUTED` -> `PROGRESSION_EXECUTED` -> `EXTERNAL_CONSEQUENCE_STARTED` -> `EXTERNAL_CONSEQUENCE_UPDATED`, including zero-delay boundary tests.
- Added separate counts and rates for external exposure, recovery initiation, supported and unsupported exposure, evidentially unsupported exposure, and unauthorized exposure.
- Added blocking invariants requiring progression and exposure counts to match, exposure and recovery-start counts to match, support to partition exposure, and evidentiary and authorization classifications to remain unchanged across the boundary.
- Added a matched overload test showing that the same late-review schedule creates no exposure under U2C but creates unauthorized exposure and recovery initiation under U2O.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 59 focused replay, typed-process, causal-reference, timing, support, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 9 queue/action/exposure integration tests, including matched fail-open/fail-closed recovery exposure |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 96 tests in 0.36 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: repeated artifact SHA-256 `66ccb35fce638ab0cf79e90f0fd5a29d61a00413a13d6c44bf42a4a506b8ff54` |
| smoke exposure inspection | U0: 1 supported exposure; U1: 5 exposures, 4 evidentially unsupported; U2C: 0 exposures; U2O: 4 unauthorized exposures, 3 also evidentially unsupported; U3: 3 supported exposures; every exposure has one recovery-start update |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Add correction requests, reassessment capacity, recovery-service and correction windows, administrative cutoff/censoring, and dimension-specific restoration.
- Wire assistance capacity only through a declared process stage and preserve its engagement effect separately from review and reassessment capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this stylized exposure/recovery smoke artifact as a substantive, empirical, legal, or historical result.

## Slice 2 Correction Request and Reassessment-Service Checkpoint

Status: unsupported exposure can enter a typed, capacity-constrained reassessment queue; Slice 2 not complete

Checkpoint commit: `c307c7f17a5544c136b401b67a8f4d22d85492cc` (`Add correction reassessment queue`)

### Scope and fact ownership

- The upstream action decision owns progression support. Unsupported exposure is correction-eligible; the correction stage consumes that classification without re-deriving it.
- Correction uptake is separate from eligibility. This stylized checkpoint compares the shared `administrative_access` draw with a compiled `correction_uptake_probability`, making the induced cross-stage correlation explicit rather than adding an unregistered random family.
- `CORRECTION_REQUESTED` records uptake and queue entry. A reassessment queue visit records service start, and `REVIEW_COMPLETED` with `review_kind = reassessment` records completion. Reassessment completion explicitly records `correction_executed = false` and `restoration_executed = false`.
- The queue visit, rather than a same-time `REVIEW_STARTED` event, owns reassessment start because the frozen event-priority registry would otherwise place an immediate post-action review start before its `CORRECTION_REQUESTED` cause.
- The queue drains without an administrative cutoff in this checkpoint. Late reassessment is measured, but no open case is yet right-censored.

### Implemented

- Added declared recovery, correction, and reassessment process stages; typed reassessment capability and action; and compiled correction-request delay, uptake, reassessment capacity/service, and correction-window slots.
- Added correction requests only for unsupported exposure with a successful uptake draw. Supported exposure never enters the correction queue.
- Added a separate work-conserving FIFO reassessment resource using the existing keyed `reassessment_service` draw, stable request/server identities, correction deadlines, and causal links from recovery through request to service completion.
- Added separate counts, rates, wait-time metrics, schedule hash, and blocking partitions for correction eligibility, requested versus unrequested correction, reassessment starts/completions, and timely versus late completion.
- Fixed the generic service scheduler to perform time arithmetic and totals at 50-digit Decimal precision. The exact-boundary regression proves reassessment completion at its correction deadline is timely and precedes the deadline event.
- Added capacity monotonicity, zero/one uptake, supported-exposure exclusion, typed-profile closure, replay, causal-reference, and no-premature-restoration tests.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 72 focused replay, correction-uptake, queue, exact-boundary, typed-profile, causal-reference, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 11 queue/action/exposure/reassessment integration tests, including capacity monotonicity and supported-exposure exclusion |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 111 tests in 0.42 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: repeated artifact SHA-256 `ba834ea7e98d8d207a6c1acdcf2be5da72b1974d536a19ced7391c3b31d9f586` |
| smoke correction inspection | U1: 4 eligible exposures, 3 requests, 1 unrequested, all 3 reassessments late; U2O: 4 eligible, 3 requests, 1 unrequested, 2 timely and 1 late; U0, U2C, and U3 have no unsupported exposure or correction request |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Add typed correction outcomes without equating decision correction with complete restoration.
- Add recovery-service dynamics, administrative cutoff/right-censoring, and dimension-specific restoration over decision, recovery, and other modeled consequence coordinates.
- Wire assistance capacity only through its declared stage and preserve its engagement effect separately from review and reassessment capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this stylized correction/reassessment smoke artifact as a substantive, empirical, legal, or historical result.

## Slice 2 Decision-Correction Outcome Checkpoint

Status: completed reassessment corrects the decision coordinate while recovery remains active; Slice 2 not complete

Checkpoint commit: `0513a872182c143e9369b7e11ceab99ab8c02ee7` (`Add typed correction outcomes`)

### Scope and fact ownership

- The upstream action decision continues to own progression support and its reason codes. The correction outcome consumes that exact basis and records `unsupported_progression_confirmed`; it does not manufacture a new support judgment.
- Within this stylized seam, every drained reassessment of a correction-eligible unsupported exposure corrects the decision coordinate. No separate historical correction-accuracy claim or unregistered random draw is introduced.
- Correction timeliness is inherited from reassessment completion against the compiled correction window. Late reassessment may still correct the decision after that window; timeliness and correction execution are reported separately.
- The correction event sets `decision_state = corrected_to_baseline` while keeping exposure and recovery active and `restoration_complete = false`. It is not a `RESTORATION_EXECUTED` event and cannot satisfy complete restoration.
- At the exact deadline, reassessment completion is timely. Under the frozen priority registry, the deadline marker sorts between reassessment completion and its same-timestamp consequence update; the causal references and explicit timely flag preserve the transition semantics.
- Because the queue still drains without an administrative cutoff, every accepted correction request eventually completes and corrects. Unresolved correction currently means eligible exposure without uptake; censoring will later add requested-but-open cases.

### Implemented

- Added a typed `correct` consequence update causally linked to the original exposure, correction request, and reassessment completion.
- Carried the original unsupported-reason codes into the correction outcome and added blocking validation that only unsupported executed progression may receive this outcome.
- Added separate counts and rates for executed, timely, late, and unresolved correction; recovery still active after correction; and mean/maximum exposure time to decision correction.
- Corrected recovery-start telemetry to count only the typed `recover` consequence update now that multiple external-consequence updates can occur in one trace.
- Added invariants requiring reassessment completion and correction execution to match in the drained checkpoint, correction timing to match reassessment timing, corrected plus unresolved cases to partition eligible exposure, and every decision correction to leave recovery/restoration state unchanged.
- Extended exact-boundary, zero-uptake, capacity, metric, causal-lineage, replay, and no-premature-restoration tests.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 72 focused replay, correction-outcome, queue, exact-boundary, causal-reference, and metric tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 11 queue/action/exposure/reassessment/correction integration tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 111 tests in 0.42 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass: repeated artifact SHA-256 `f2b59fa7b9f7bcf635777b5aac633d24ec03f604198ecf562b82c8483721b486` |
| smoke correction inspection | U1: 4 eligible, 3 corrected late, 1 unresolved; U2O: 4 eligible, 2 corrected timely, 1 corrected late, 1 unresolved; recovery remains active after all 6 corrections; U0, U2C, and U3 require no correction |
| exposure-duration inspection | corrected U1 cases average `28.9434778347` time units to correction; corrected U2O cases average `21.9412930461`; these are stylized smoke diagnostics, not substantive estimates |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Add recovery-service dynamics, administrative cutoff/right-censoring, and dimension-specific restoration over decision, recovery, and other modeled consequence coordinates.
- Preserve requested-but-open correction separately from no uptake and from completed-but-late correction once censoring exists.
- Wire assistance capacity only through its declared stage and preserve its engagement effect separately from review and reassessment capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this stylized decision-correction smoke artifact as a substantive, empirical, legal, or historical result.

## Slice 2 Recovery-Service and Late-Stage Censoring Checkpoint

Status: recovery is capacity-constrained and unfinished recovery/correction work is right-censored at a declared observation boundary; Slice 2 not complete

Checkpoint commit: `392278e` (`Add recovery queue and right censoring`)

### Scope and fact ownership

- Recovery is now a distinct FIFO service resource. Queue entry occurs after the compiled recovery-start delay; the current fixed service requirement is owned by the stylized overlay and intentionally adds no exogenous draw family after Slice 1 draw closure.
- The queue preserves planned start and completion times while separately recording whether each visit started or completed by the administrative cutoff. Planned post-cutoff work is auditable but is not emitted or counted as an observed completion.
- This is explicitly a late-stage censoring checkpoint. The cutoff must follow every action and external-consequence start. A configuration that would censor engagement, review, action, or exposure formation is rejected rather than simulated with unsupported semantics.
- `CASE_CLOSED` records administrative observation closure, `right_censored = true`, and an open-state reason. It does not assert case resolution or complete restoration.
- Recovery completion, decision correction, and complete restoration remain different coordinates. A corrected decision continues to record active recovery exposure and incomplete restoration.

### Implemented

- Added compiled recovery capacity, fixed service demand, recovery window, and administrative-cutoff slots with typed validation and overlay receipts.
- Extended the generic service scheduler with exact-boundary cutoff status, `service_in_progress_at_cutoff` versus `service_not_started_by_cutoff` reasons, observed wait/service totals, and completion/censoring partitions included in the schedule hash.
- Replaced immediate recovery activation with a capacity-constrained recovery queue. Only service completed by the cutoff emits the typed recovery update; every exposure is partitioned into completed recovery, right-censored service, or queue entry unavailable by the cutoff.
- Prevented post-cutoff correction requests, reassessment completions, deadlines, and correction outcomes from entering observed traces. Requested-but-open reassessment is separate from failed uptake and from correction not yet available.
- Added one administrative closure event per case, explicit closure reasons, no-post-cutoff-event invariants, and separate recovery, reassessment, correction-availability, and case-censoring metrics.
- Updated the CLI artifact with all three queue schedules and cutoff statuses. The claim limit now identifies a stylized recovery-resource and late-stage right-censoring smoke artifact.
- Added invalid-cutoff, exact-boundary, recovery-capacity monotonicity, recovery/reassessment censoring, replay, metric, and earlier-stage rejection tests.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 80 focused replay, cutoff, recovery, correction, queue, metric, and exact-boundary tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 13 queue/action/recovery/reassessment integration tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 121 tests in 0.45 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass twice with identical artifact SHA-256 `4fe6674e2fd3c8b648c7a121a1dde55bd21e0bd754db1f76e4fd86318aa62f7e` |
| smoke cutoff inspection | U1: 5 exposures, 3 recovery completions, 2 censored recovery visits, and 2 observed corrections; U2O: 4 exposures, 2 recovery completions, 2 censored recovery visits, and 1 requested reassessment censored in service with no correction outcome |
| observation-boundary inspection | all 25 policy-case traces close at time 70; no emitted event occurs after the cutoff; every planned queue visit retains explicit cutoff status and censoring reason |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Add dimension-specific restoration over decision, recovery, monetary, and other modeled consequence coordinates; do not treat recovery-service completion or decision correction as complete repair.
- Extend the observation boundary to engagement/review/action stages with explicit state semantics before permitting an earlier cutoff.
- Wire assistance capacity only through its declared stage and preserve its engagement effect separately from review, recovery, and reassessment capacity.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this stylized recovery/censoring artifact as a substantive, empirical, legal, or historical result.

## Slice 2 Consequence-Vector Restoration Checkpoint

Status: correction and restoration are separate typed transitions, and restoration completeness is evaluated over a declared consequence vector; Slice 2 not complete

Checkpoint commit: `75a88ea` (`Add consequence-vector restoration outcomes`)

### Scope and fact ownership

- Every unsupported external exposure creates a restoration obligation. This obligation is independent of whether correction is requested or completed.
- Reassessment completion owns decision correction only. Its consequence update retains active recovery exposure and explicitly records incomplete restoration.
- The policy profile owns whether a post-correction restoration transition is active. The generic kernel owns deterministic execution and consequence-vector evaluation.
- The current modeled restoration dimensions are exactly `decision_state`, `recovery_state`, and `residual_external_consequence`, each with an explicit baseline. Monetary amounts, payments, fees, burden, and unmodeled harms are outside this checkpoint and cannot be declared restored.
- The restoration horizon begins at external-consequence start. The stylized overlay owns its duration and the post-correction restoration delay. Repair at the horizon is timely; repair after it clears the decision and recovery dimensions but leaves a declared irreversible external residual.

### Implemented

- Added compiled restoration-delay and restoration-window slots plus an explicit restoration stage and policy-owned `restore` action requirement for U1 and U2O, the policies with reachable unsupported-progression correction paths.
- Added `RESTORATION_EXECUTED` only after typed decision correction and only when the policy activates restoration. The event carries source references, declared dimensions, baseline states, realized states, restored and unrestored dimension IDs, horizon timing, and complete-versus-partial status.
- Added a blocking vector invariant that recomputes completeness from every modeled state against its declared baseline. The event's `restoration_complete` flag cannot independently assert success.
- Classified exact-horizon restoration as timely and complete. A late action is observed partial restoration with an irreversible residual, not complete restoration and not right-censoring.
- Distinguished pre-horizon pending obligations from expired obligations. Pending work is right-censored; expiration without completion is an observed failed outcome and closes without a censoring label.
- Revised case closure so resolved complete/partial/expired outcomes and right-censored open outcomes partition the cohort instead of forcing every administrative closure into censoring.
- Added separate due, executed, timely, late, complete, partial, pending, expired, unresolved-consequence, restoration-time, resolved-case, and censored-case metrics and CLI fields.
- Added exact-horizon, zero-delay ordering, late-partial, expired-unexecuted, policy-ownership, typed-profile closure, vector-baseline, metric, and censoring regressions.

### Verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/unit/test_simulator.py tests/unit/test_random_streams.py tests/unit/test_policies.py tests/unit/test_metrics.py` | pass: 90 focused restoration, replay, queue, cutoff, policy, metric, and exact-boundary tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q tests/integration/test_queue_validation.py` | pass: 13 queue/action/recovery/reassessment/restoration integration tests |
| `PYTHONPATH=src ./.venv/bin/python -m pytest -q` | pass: 131 tests in 0.47 seconds; all earlier regressions retained |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli cohort experiments/configs/stochastic_smoke_v1.yaml` | pass twice with identical artifact SHA-256 `9e230c4266390554f2d95fb7c27a786b068ceead0f4c5487cd6847c1062d7cdd` |
| smoke restoration inspection | U1: 4 obligations, 1 complete restoration, and 3 pending horizons; U2O: 4 obligations and 4 pending horizons; no smoke case is mislabeled partial or expired merely because the cutoff arrives first |
| closure inspection | the one completely restored U1 case closes as resolved; the other 24 policy-case traces remain right-censored; focused fixtures separately prove partial and expired outcomes close as observed failures |
| `PYTHONPATH=src ./.venv/bin/python -m uncertainty_permission_simulation.cli trace experiments/configs/smoke_v1.yaml` | pass: 9 Slice 1 traces; summary hash `b49ea5936727d23c3871a91555ba68d56d30f8f8c95a02e8c68ca9ae5210f739` and record hash `29ec5616135d9e94a6d8e84dbdff3879fcc63dfbacadaa4e640258dab2912db8` unchanged |
| `./.venv/bin/python scripts/validate_plan.py` and `./.venv/bin/python scripts/validate_slice0.py` | pass |
| runtime-module compilation and generic-kernel case-name scan | pass |

### Remaining before Slice 2 closeout

- Wire assistance capacity only through its declared stage and preserve its engagement effect separately from review, recovery, and reassessment capacity.
- Extend the observation boundary to engagement/review/action stages with explicit state semantics before permitting an earlier cutoff.
- Add monetary, payment, fee, or burden consequence dimensions only through a typed extension with explicit baseline and restoration rules; the current three-coordinate result must not be silently promoted.
- Execute both R-OCI adapters only through compiled profiles and stylized overlays; add semantically equivalent synthetic/application comparisons.
- Expand analytical queue checks, add a slower reference simulator, exact stochastic golden traces, and stored stochastic validation receipts.
- Do not enter pilot scenario selection or treat this stylized restoration artifact as a substantive, empirical, legal, or historical result.
