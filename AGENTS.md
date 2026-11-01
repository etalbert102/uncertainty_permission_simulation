# Repository Instructions

## Canonical Plan

Read `docs/STUDY_PLAN.md` before implementation. Follow its slice order, stop conditions, ledger requirements, and claim boundaries.

## Research Boundaries

- This repository owns the 10,000-word extended research paper; it does not revise or replace the completed 1,500-word precursor essay.
- Treat `../in_progress/uncertainty_expands_authority/when-uncertainty-expands-authority-final-revision.md` as the upstream claim contract. Do not edit it from this repository.
- A formal model and proposed research design are not completion. The paper must report validated, executed simulation results and their limitations.
- Preserve the precursor's exact held-output comparison in `P0-Precursor`: the underlying case, uncertain model output, downstream rule, and process state remain fixed while only the interface representation changes; include the no-change falsifier.
- In manuscript prose, define this from first principles as the “representation-preservation fixture” and keep `P0-Precursor` in internal or supplementary artifacts rather than reader-facing prose. Do not require readers to know the short essay.
- Keep the lineage continuity matrix internal. Reader-facing sections, headings, conclusions, and examples must stand alone rather than present the article as a sequel.
- Keep the base uncertainty-to-permission vulnerability, structural susceptibility, process red-teaming, and adversarial exploitability distinct. Attribute adversarial exploitability only when inducibility, observability, repeatability, and benefit are supported; do not attribute those conditions to Robodebt.
- Freeze the protocol semantics, `pass`/`fail`/`unassessable` classifications, held-out AI canary, and worked-trace selection rule before confirmatory results; post-result prose may not change them.
- After Slice 5 analysis, the project lead reviews whether the complete procedure is understandable using the staged P0, Robodebt, and transfer-canary inputs. Treat this as a comprehensibility review, not independent validation or evidence about human performance.
- Post-simulation editorial clarifications may not alter frozen semantics. Any change to a construct, status rule, required input, application mapping, metric, or supported conclusion requires a new freeze and rerun of affected confirmatory artifacts.
- Draft named article sections to 9,400 words and track the 600-word contingency explicitly; do not spend the reserve merely to reach the 10,000-word ceiling.
- Treat this as a formal counterfactual simulation grounded in Robodebt, not a numeric reconstruction of the historical program or evidence of current-system prevalence.
- Keep observed, imputed, missing, and disputed evidence distinct end to end.
- Keep evidentiary support, simulated numerical correctness, and source-attributed legal validity distinct end to end.
- Keep formal authority, functional permission, and operational action distinct end to end.
- Keep debt action, constraint, staff review, evidence acquisition, recovery, and restoration actions separate.
- Preserve the distinction between decision-space erosion and behavioral compression.
- Attribute historical and legal claims to the Royal Commission, Ombudsman, or another authoritative source at citation level.
- Limit transfer to current AI or national-security systems to the formal invariant, process-red-team method, and explicitly supported institutional similarities.
- Do not tune confirmatory tasks, prompts, metrics, exclusions, or analysis after freeze.
- Negative controls, freeze integrity, source provenance, and the claim-boundary memo are required.

## Architecture

- Implement a case-neutral study kernel behind closed, versioned process-profile, policy-profile, evaluation-specification, application-adapter, and stylized-overlay contracts. Do not turn it into a general-purpose framework, registry, or plugin system.
- Follow `docs/CONFIGURATION_COMPILATION.md`. Execute only validated compiled configurations; raw source YAML, narrative descriptions, and free-form guards are never executable behavior.
- Deterministic code owns evidentiary transformation, policy behavior, permissions, event order, hashes, and replay.
- Process profiles own capabilities and topology. Policy profiles own active transformation, routing, permission, gate, timeout, correction, and restoration behavior. Policies may not create undeclared process capabilities.
- Canonical synthetic profiles must exercise core semantics before any institutional adapter is loaded. Core event, policy, formal-evaluation, random-stream, and metric code may not branch on `Robodebt`, `OCI`, a source citation, or another application label.
- The source manifest and dated R-OCI adapters own Robodebt process and legal claims; simulation code may not invent or blend undocumented history.
- Preserve `data/sources/robodebt/r_oci_early.yaml` and `r_oci_enhanced.yaml` as distinct period fixtures. A parameter marked `unsupported` may not receive a historical default in code.
- Executable study assumptions absent from the historical record belong in a separate versioned stylized scenario overlay. They may not mutate or fill the source-anchored profile.
- Overlays may fill declared unbound slots only. Documented values cannot be overwritten, unsupported source fields provide no executable value, every runtime slot requires exactly one binding receipt, and unresolved or multiply owned slots invalidate compilation.
- Counterfactual policies may not masquerade as historical profiles.
- Random draws must be keyed by stable case, event family, and draw index rather than consumed in queue order.
- Analysis code owns estimates and confidence intervals.
- Reports render stored artifacts; they must not re-derive facts from prose.
- Do not add compatibility dependencies on `decision_space_harness`.

## Execution

- Only one dependent plan slice may be active.
- Before any Slice 1 mutation, close `D-009`: review and commit the validated Slice 0 baseline, create the declared environment, and record both validator outputs and environment versions in the ledger.
- Automated specification, fixture, source, pilot, and freeze gates authorize protocol `1.0` and confirmatory execution. No external-reader return is required.
- The project-lead comprehensibility review occurs only after Slice 5 analysis and blocks Slice 6 completion, not confirmatory freeze or execution.
- Update the execution ledger at the end of every slice.
- Record exact commands, results, residual risk, and commit SHA.
- Finish, remove, or explicitly defer partial subsystems; do not leave unowned TODOs.
- Preserve append-only attempts after model-backed execution begins.
- Run `python3 scripts/validate_plan.py` before entering Slice 1 and after any change to the canonical plan, preregistration, architecture, deferred register, or execution controls.
- Run `python3 scripts/validate_slice0.py` before entering Slice 1 and after any change to source, application profile, protocol, packet, preregistration, or worked-trace artifacts.
- P0 is the synthetic representation-preservation fixture, not a Robodebt trace. Slice 3 generates a separate review input from the executable prespecified Robodebt trace; after Slice 5, the project lead reviews P0, that trace, and the transfer canary in sequence.
