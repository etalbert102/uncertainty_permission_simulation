# Uncertainty-to-Permission Simulation

This repository develops an invariant-based process-red-team method and a case-neutral finite-cohort dynamic simulation kernel for evidentiary transformation, review capacity, and functional permission. The Australian Robodebt program is its primary source-grounded application, not an engine dependency or a numerical calibration target.

Its deliverable is a 10,000-word extended research paper building on the completed 1,500-word essay *When Uncertainty Expands Authority: How AI Workflows Can Reduce Scrutiny*. The essay is an upstream claim contract; this repository owns the formalization, documented case application, conducted simulation, results, and extended manuscript.

The focal mechanism is:

> incomplete or aggregate evidence -> unsupported apparent precision -> permission change -> burden and review-capacity interaction -> debt and correction outcomes

The study asks when aggregate annual income data can become apparently precise fortnightly values, how that representation changes automatic functional permission, and when notice, administrative access, staff review, evidence acquisition, or reassessment provides effective control under realistic workload and timing constraints.

## Status

The research and implementation plan is execution-ready; this does not mean the study is complete. Slice 0 automated source-and-specification implementation gate passes, while independent reader QA remains required before protocol `1.0` and confirmatory freeze. No simulator or confirmatory results exist. No pilot, evidence packet, or completed manuscript exists either.

The canonical execution plan is [docs/STUDY_PLAN.md](docs/STUDY_PLAN.md).

The claim-driven drafting blueprint is [docs/ARTICLE_OUTLINE.md](docs/ARTICLE_OUTLINE.md).

The draft fixed-output compatibility specification is [docs/PRECURSOR_FIDELITY_FIXTURE.md](docs/PRECURSOR_FIDELITY_FIXTURE.md). It defines the representation-preservation comparison and its no-change falsifier; it is not yet implemented or frozen.

The draft formal specification is [docs/FORMAL_MODEL.md](docs/FORMAL_MODEL.md). It defines constructive refinement modes, an independently owned evaluation specification, evidentiary fidelity, finite and symbolic action sets, event-state support reevaluation, separate truth/completeness diagnostics, operational review, horizon-aware F0–F5, and the three headline propositions; it is not yet implemented or frozen.

The draft practitioner method is [docs/PROCESS_RED_TEAM_PROTOCOL.md](docs/PROCESS_RED_TEAM_PROTOCOL.md). It defines document-audit, bounded-trace, and dynamic-simulation application levels; a five-step intake and diagnostic workflow; mandatory escalation; and a non-composite report profile. Blinded QA uses packet-only copies of [docs/P0_COLD_READER_PACKET.md](docs/P0_COLD_READER_PACKET.md) and [docs/TRANSFER_CANARY.md](docs/TRANSFER_CANARY.md), controlled through [docs/COLD_READER_QA_RECEIPT.md](docs/COLD_READER_QA_RECEIPT.md). [docs/P0_USABILITY_WALKTHROUGH.md](docs/P0_USABILITY_WALKTHROUGH.md) and [docs/TRANSFER_CANARY_EXPECTED_PROFILE.md](docs/TRANSFER_CANARY_EXPECTED_PROFILE.md) are withheld oracles and must be opened only after a reader locks their assessment. Their results remain expected projections until Slice 1 emits executable records.

The draft machine-readable schema inventory is [data/model/schema_manifest_v1.yaml](data/model/schema_manifest_v1.yaml). It fixes acyclic record/reference boundaries, canonicalization, role-bound closed rule signatures, truth/completeness assessments, complete system-intervention traces, well-founded event execution, payload ownership, and set-versus-sequence paths for the first implementation slice; executable models have not yet been created.

The [configuration compilation contract](docs/CONFIGURATION_COMPILATION.md) fixes the case-neutral boundary: immutable source fixture, application mapping, process capability profile, active policy profile, independent evaluation specification, stylized overlay, and complete parameter-binding receipts compile into the only configuration the simulator may execute.

The Robodebt source packet is indexed in [data/sources/robodebt/source_manifest.yaml](data/sources/robodebt/source_manifest.yaml), with separate [early](data/sources/robodebt/r_oci_early.yaml) and [enhanced](data/sources/robodebt/r_oci_enhanced.yaml) application profiles. [docs/ROBODEBT_CASE_STUDY.md](docs/ROBODEBT_CASE_STUDY.md) renders the dated process maps, formal crosswalk, three-axis claim rule, parameter provenance, and limitations. These artifacts ground structure; they do not reconstruct historical rates, supply silent defaults for unsupported quantities, decide legality, or define kernel behavior.

Slice 0 control artifacts include the [literature and originality map](docs/LITERATURE_AND_ORIGINALITY_MAP.md), [continuity and claim-boundary control](docs/CONTINUITY_AND_CLAIM_BOUNDARY.md), [preregistration skeleton](docs/PREREGISTRATION.md), and [prespecified worked-trace rule](docs/WORKED_TRACE_SELECTION.md). The [plan completion receipt](docs/PLAN_COMPLETION_RECEIPT.md) records why the design is ready to execute without implying that the research has been conducted. The execution and external-dependency status is recorded in [docs/EXECUTION_LEDGER.md](docs/EXECUTION_LEDGER.md) and [docs/DEFERRED.md](docs/DEFERRED.md).

## Intended Contribution

The repository will support:

- a compatible-state information order with conclusion-valid constructive refinement coverage, evidentiary-fidelity condition, and independently supported robust-permission invariant;
- explicit separation of formal authority, functional permission, and operational action;
- explicit separation of observed, imputed, missing, and disputed evidence;
- a direct precursor-fidelity fixture that holds the uncertain model output and process inputs fixed while varying only whether the interface preserves alternatives or emits the broad fallback;
- explicit separation of the base vulnerability, process-red-team susceptibility, and adversarial exploitability conditions;
- a finite-cohort discrete-event model of notice, endogenous engagement, evidence retrieval, staff review, debt action, recovery, and reassessment;
- a closed case-neutral configuration boundary separating kernel behavior, formal evaluation, process profiles, policy profiles, source-grounded application adapters, and stylized scenario overlays;
- deterministic configuration compilation that rejects raw narrative execution, documented-value overwrite, unsupported historical defaults, duplicate parameter owners, and unresolved runtime slots;
- early and enhanced OCI historical validation profiles;
- five paired counterfactual profiles, including fail-closed and fail-open review;
- explicit separation of evidentiary support, simulated numerical error, and source-attributed legal validity;
- authoritative Robodebt process grounding with dated, documented-versus-stylized provenance;
- negative controls, confirmatory freezing, and reproducible Monte Carlo analysis;
- a pre-result-frozen five-step protocol with `pass`, `fail`, `unassessable`, and `not_applicable` outputs, tested through cold-reader artifact QA on a fixed Robodebt trace and held-out AI canary; and
- an evidence packet and complete 10,000-word research article reporting executed results.

The simulation evaluates declared counterfactual systems. Canonical synthetic profiles establish the mechanism; Robodebt establishes structural relevance through a thin source-grounded adapter. The study does not numerically reconstruct Robodebt, estimate unreported historical quantities, independently determine legality, or establish equivalence to current AI systems. Its emerging-technology contribution is the transferable formal invariant and process-red-team method.

## Repository Boundary

This is intentionally separate from `decision_space_harness`. It does not share that repository's task registries, protocols, or historical outputs.

Canonical terminology and motivating research remain in the sibling `decision_space_writing` repository. Historical and process claims are owned by the authoritative source manifest in `data/sources/robodebt/`.

The completed precursor essay remains in `../in_progress/uncertainty_expands_authority/when-uncertainty-expands-authority-final-revision.md` and is not edited from this repository.

## Planned Layout

```text
data/
  model/             Formal and process specifications
  sources/robodebt/  Source manifest and citation-level notes
  scenarios/         Pilot and frozen scenario families
  golden_traces/     Hand-inspected event traces
docs/                Plan, case study, preregistration, ledger, and evidence packet
experiments/configs/ Smoke, pilot, confirmatory, and sensitivity configs
outputs/             Generated run artifacts; ignored except for the placeholder
scripts/             Repository and freeze verification
src/uncertainty_permission_simulation/
tests/
```

## Next Step

The validated Slice 0 baseline and environment receipt required by `D-009` are committed. Begin Slice 1 by implementing the closed schemas and deterministic configuration compiler, followed by the case-neutral vertical trace, isomorphic vocabulary canary, non-isomorphic topology canary, and R-OCI-Early adapter smoke test in that order. In parallel, complete the independent readability gate by distributing the existing oracle-free bundles, obtaining locked packet-only returns from at least two eligible readers, comparing them with the withheld profiles, and logging any revisions. Reader QA must pass before protocol `1.0` and confirmatory freeze, but exact historical calibration is not required to implement the kernel.
