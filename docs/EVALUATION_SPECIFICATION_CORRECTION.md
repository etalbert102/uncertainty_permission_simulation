# Evaluation-Specification Correction Receipt

Date: 2026-11-19

Status: closed by executable repair, second freeze, complete rerun, and exact result comparison

## Finding

The first confirmatory runtime stored the evaluation-specification identifier but derived action support from a case-state shortcut. It therefore did not invoke the declared general action-support rule across an explicit set of admissible refinements. The numerical condition happened to be equivalent for the frozen binary period-evidence design, but provenance alone did not establish that equivalence in execution.

## Repair

The compiled configuration now contains a content-addressed evaluation specification with:

- an independently owned action-support rule;
- explicit supported and unresolved evidence states;
- finite exact refinement certificates;
- an implementation-code hash; and
- a specification content hash.

At routing and action time, the kernel validates those hashes, evaluates the registered support rule over every certified refinement, and stores the evidence-state, specification, implementation, certificate, and robust-support result in the event receipts. Unit tests cover both a singleton supporting certificate and an unresolved certificate containing supporting and non-supporting refinements.

## Second freeze and rerun

The pre-correction compact analyses remain recoverable from repository commit `dd6df521c212f45978417f2e43c9f2003bed9271` and have these self-hashes:

| Pre-correction artifact | Archived identity |
| --- | --- |
| Freeze manifest | `35f360d81e7eebe1effeae813f4144991b0fa043001df6d920d3f8592bfee65c` |
| Core analysis | `bb486ee634365e53b7de464eb8cae8fc1e9169a29e1b6ad0ed3b496a684341cc` |
| Sensitivity analysis | `0abaab09c09c94eb797d46ade1dbe5d7dd46c1ce85d515ba769ed4d1b5bc82db` |

| Item | Corrected identity |
| --- | --- |
| Freeze ID | `UPS-CONFIRMATORY-FREEZE@2` |
| Freeze manifest self-hash | `9d0d2ed34f74608e5aed96b6a28d81ded2d6d15bba552be91706c5ce862b2801` |
| Core run-index self-hash | `3fcb54de9657ae212cee87ddc9c09184798b4948e90b2cd534f8580892c71d99` |
| Core reconciliation self-hash | `4d596c0872aa872214c5815615246a683f5e7be0c6ce8dc38cbae257df23273c` |
| Core analysis self-hash | `4d549f5e1fed84f294052749d9987d807e9fe2199843b44d7eb7aece867b36bd` |
| Sensitivity run-index self-hash | `00851d0dffd7c7b649897d6d78f8d2c90a8f31134f948323b455f8a60823732f` |
| Sensitivity reconciliation self-hash | `08b36d1f16ef1e27435cc1e8a17f929864d0775f20da495f782c6596faf48e9e` |
| Sensitivity analysis self-hash | `f1cbc3437418e803510483a080052444ce75658df42a95fcd5f4f6922f637452` |

Both corrected suites contain 16,200 reconciled attempts and 1,296,000 case-policy trajectories. The pre-correction manifest is preserved as `FREEZE_MANIFEST_PRE_EVALUATION_BRIDGE.json`; the original attempts remain locally archived under `outputs/archive_pre_evaluation_bridge/`. Repository history preserves the compact pre-correction analyses even when the ignored attempt archive is unavailable.

## Exact comparison

The archived and corrected analysis receipts were compared as structured JSON. For both the core and sensitivity suites, all four result-bearing fields were exactly equal:

| Compared field | Core | Sensitivity |
| --- | --- | --- |
| `cell_summaries` | exact match | exact match |
| `paired_estimates` | exact match | exact match |
| `precision` | exact match | exact match |
| `common_random_number_diagnostics` | exact match | exact match |

Configuration, event, manifest, run-index, reconciliation, and analysis identities changed as expected because the executable provenance changed. No scenario, policy, parameter, seed, estimand, exclusion, or claim boundary was changed, and no post hoc result was added.

## Claim limit

This closes the implementation-to-specification bridge for the frozen binary period-evidence demonstration. It does not validate other refinement sets, support rules, historical Robodebt evidence, practitioner usability, or field performance.
