# Configuration Compilation Contract

Status: preimplementation architecture contract; no executable compiler or simulation results

## Purpose

The simulator executes only a validated `CompiledConfiguration`. It never executes a Robodebt source YAML file, narrative transition description, free-form guard, application label, or unbound scenario parameter directly.

The compiler is deterministic and study-specific. It combines closed records without providing a plugin or dynamic registry mechanism.

## Input Ownership

| Input | Owns | Must not own |
| --- | --- | --- |
| `SourceApplicationFixture` | Immutable path and hash of a source-grounded application artifact, dated scope, claim IDs, unsupported slots | Executable defaults or counterfactual behavior |
| `ApplicationMapping` and `ApplicationBinding` | Mapping from source elements to generic roles, stages, transitions, actions, rules, and parameter slots | Event-loop logic or unsupported historical quantities |
| `ProcessProfile` | Capability graph: roles, stages, resources, queues, deadlines, gate locations, transition topology, action types, parameter slots | Active transformation, routing, permission, timeout, correction, or restoration policy |
| `PolicyProfile` | Active transformation, routing, permission, gate, timeout, evidence-acquisition, correction, and restoration rules | Historical claims not supplied by a source fixture or process capabilities not declared by the process profile |
| `EvaluationSpecification` | Independent support, materiality, correspondence, review, intervention, and restoration tests | Operational policy behavior |
| `ScenarioOverlay` | Executable values for declared unbound slots, with stylized or sensitivity ownership | Mutation of a documented value or creation of a new undeclared slot |
| `CompiledConfiguration` | Exact executable input bundle and binding receipts | New facts, inferred defaults, or narrative interpretation |

## Compilation Sequence

1. Validate every stored envelope, schema version, canonical hash, source reference, and reference target.
2. Validate each source fixture's artifact hash and `TemporalScope`. Raw source artifacts remain immutable inputs.
3. Resolve every `ApplicationBinding` from a source element ID to a declared generic semantic target. Descriptions and guard strings cannot execute.
4. Compile the application mapping into a source-grounded process capability graph and, where supported, a distinct historical policy profile. One source transition may supply evidence for both outputs, but each compiled behavior has one owner.
5. Select exactly one process profile, one active policy profile, and one independent evaluation specification for each compiled configuration.
6. Check that every policy rule uses a capability, action type, gate location, or parameter slot declared by the selected process profile. Policy rules cannot add undeclared topology at runtime.
7. Apply the scenario overlay only to declared unbound parameter slots.
8. Emit one `ParameterBindingReceipt` for every runtime slot. Reject duplicate owners, conflicts, undocumented overrides, and unresolved slots.
9. Emit a `CompiledConfiguration` containing exact references, compiler version and code hash, binding receipts, and zero unresolved parameter slots.
10. Validate the scenario and run against compiled-configuration references. Neither may select a process or policy through free text.

## Parameter Resolution

For each declared parameter slot:

- A documented source value is authoritative and cannot be overwritten by an overlay.
- A source field marked `unsupported` supplies no executable value.
- A stylized overlay may fill an unsupported or otherwise explicitly unbound slot.
- A sensitivity overlay may fill an explicitly unbound slot only in a declared sensitivity configuration.
- Two candidate executable values for the same slot produce `PROFILE_PARAMETER_CONFLICT`.
- A value targeting an undeclared slot produces `SCENARIO_PARAMETER_INVALID`.
- An unsupported source field used without an overlay owner produces `PROFILE_UNSUPPORTED_PARAMETER`.
- Any unresolved runtime slot produces `SCENARIO_CONFIGURATION_INCOMPLETE`.

The receipt records the target slot, target owner, resolved parameter record, and whether the value came from a documented source, stylized overlay, or sensitivity overlay.

## Process And Policy Separation

Application source material may describe topology and behavior together. The compiler must separate them:

- The process profile records that a notice, response path, review resource, calculation stage, progression action, correction path, or restoration capability exists.
- The historical policy profile records when evidence is transformed, how cases route, which actions become automatic, which gate semantics apply, what occurs at timeout, and how correction or restoration proceeds.
- Counterfactual U policies replace the active policy profile while using only capabilities declared by the selected process profile.
- If a counterfactual needs a capability absent from the historical process, it must select a separately versioned counterfactual process profile. A policy may not silently create the capability.

For Robodebt, `EARLY-T06-NONRESPONSE-AVERAGING` and automatic debt progression are source evidence for historical policy bindings, while their stages, actors, and possible actions belong to the capability graph. U1 may reproduce those policy semantics as a declared benchmark; it does not inherit them implicitly from the process profile.

## Temporal Semantics

`TemporalScope` supports:

- `simulation_only` for synthetic profiles;
- `dated_interval` with explicit endpoint precision; and
- `as_documented_bundle` for a source-grounded collection of changes not asserted to activate simultaneously.

The enhanced OCI fixture uses `as_documented_bundle`, records its reference date and mixed change-window precision, and sets `simultaneous_activation_claimed = false`. The compiler may use that bundle for structural comparison but may not invent a single historical activation timestamp.

## Generic Kernel Boundary

Core events describe process semantics such as evidence ingestion, subject response, review, progression, external consequence, correction, and restoration. Application-specific outcomes such as debt assertion, recovery payment, or debt zeroing are `Action.action_type_id` values supplied by the application profile.

`SimulationCase` stores generic, semantically identified `CaseAttribute` references. Income trajectories, benefit histories, and administrative-access features are Robodebt scenario attributes, not required kernel fields.

No core module may branch on an application ID, source citation, display label, or action-type name. Reports may render application labels from stored mappings.

## Generalizability Checks

Two different checks are required:

1. **Isomorphic vocabulary canary:** rename roles, stages, application labels, and action labels while retaining semantic bindings. Projected semantic events, assessments, and metrics must match; complete artifact hashes must differ because identity and provenance differ.
2. **Non-isomorphic topology canary:** use a synthetic process with a different number or order of stages, an optional review path, and a different queue layout. It must execute without kernel changes and must produce behavior appropriate to its own topology.

Semantic comparisons use a frozen projection rule over event families, authority-direction actions, formal assessments, and metric definitions. They never compare display text or require full artifact-hash identity.

## Blocking Diagnostics

- `PROFILE_APPLICATION_MAPPING_INVALID`: a source element, claim, artifact hash, or semantic target is missing or inconsistent.
- `PROFILE_POLICY_PROCESS_OVERLAP`: active behavior is owned by both the process and policy profile, or a policy creates undeclared topology.
- `PROFILE_TEMPORAL_SCOPE_INVALID`: temporal precision or bundle semantics are fabricated or inconsistent.
- `PROFILE_PARAMETER_CONFLICT`: more than one executable owner supplies a slot or an overlay attempts to overwrite a documented value.
- `PROFILE_UNSUPPORTED_PARAMETER`: an unsupported source field is treated as executable history.
- `PROFILE_CASE_LEAKAGE`: core schema or behavior depends on an application-specific name or field.
- `SCENARIO_CONFIGURATION_INCOMPLETE`: compilation leaves an unresolved slot or required input reference.

Any of these diagnostics invalidates the configuration before trace execution.

## Slice 1 Entry Receipt

Slice 1 may begin only when:

- the schema manifest declares every record in this contract;
- the Slice 0 validator checks the required fields and generic-kernel exclusions structurally rather than by prose alone;
- the plan, preregistration, source application, and ledger use the same composition semantics; and
- the repository records that the architecture amendment passed validation.
