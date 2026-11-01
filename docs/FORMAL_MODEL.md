# Formal Model of Uncertainty, Functional Permission, and Operational Review

Status: draft Slice 0 specification; not frozen and not yet implemented

Formal-model version: `draft-0.10`

## Purpose

This document defines the formal objects, properties, and executable diagnostics used by the uncertainty-to-permission study. Its central question is:

> When evidence becomes less decision-relevant, what may the workflow now do automatically, which safeguards remain operational, and which consequences can still be restored?

The model separates evidence, representation, policy, routing, permission, execution, review, and restoration. It is deliberately process-level: a component can be accurate or calibrated while the complete workflow violates a permission or review property.

The formal model supports three headline propositions:

1. **Robust permission:** weaker evidence must not introduce an automatic progression action that the independent support rule excludes under some certified admissible refinement.
2. **Operational review:** a configured gate can remain safe while review or timely decision service fails; timeout semantics determine whether overload becomes unresolved delay or unsupported progression.
3. **Contestability and restoration:** nominal correction does not establish meaningful contestability or complete restoration when intervention is unreachable, late, or leaves residual consequences.

These are conditional claims about declared models and traces. They do not independently determine legality, empirical prevalence, historical causation, or adversarial exploitation.

## Non-Goals

The model does not:

- infer lawfulness from simulation output;
- assign one universal utility ordering across safety, timeliness, burden, workload, and restoration;
- model reviewer psychology, deference, or behavioral compression;
- treat every external effect as progression;
- infer an information order from confidence scores alone;
- convert the representation-preservation fixture into empirical evidence;
- estimate historical Robodebt frequencies or harms; or
- establish adversarial exploitability without separate evidence of inducibility, observability, repeatability, and benefit.

## Core Domains

| Symbol | Domain | Meaning |
| --- | --- | --- |
| `C` | cases | Units moving through the workflow |
| `Theta` | latent states | Complete case states used for compatibility or oracle scoring |
| `E` | evidence states | Information legitimately available at a declared process point |
| `R` | representations | Typed claims exposed to downstream components or roles |
| `Q` | process states | Workflow state, configured rules, gates, roles, and deadlines |
| `T` | time | Ordered event time or simulation clock |
| `U` | roles | Organizational actors with declared visibility and authority |
| `A` | actions | Typed workflow operations or dispositions |
| `K` | consequence dimensions | Modeled decision, monetary, recovery, burden, or other effects |
| `Pi` | policy maps | Materiality, safeguard, and authorization rules implemented by the workflow under test |
| `Sigma` | evaluation specifications | Independently owned support, materiality, refinement-coverage, and baseline rules used to evaluate the workflow |
| `Tau` | traces | Ordered events for one case under one policy configuration |

All identities are stable IDs. Display labels are not formal identities.

### Stored-record, reference, and schema-identity contract

Every stored evidence, candidate field, claim, transformation, policy, evaluation, required-meaning, rule, action, state, event, review, applicability, diagnostic, and result record is carried in one versioned envelope. Nested domain objects that need independent identity, provenance, evaluation, or reuse are stored separately and referenced; they are never embedded as partial envelopes.

```text
RecordRef = (
    object_id: string,
    object_version: positive_integer
)

RecordMeta = (
    object_id: string,
    object_version: positive_integer,
    schema_id: string,
    schema_version: positive_integer,
    canonicalization_id: string,
    canonicalization_version: positive_integer,
    owner_id: string,
    provenance_status,
    source_basis,
    source_refs: list[RecordRef]
)

StoredRecord[T] = (
    meta: RecordMeta,
    payload: T,
    content_hash: sha256_hex
)
```

`schema_id` is a stable schema-family identifier and never contains its version; `schema_version` is the positive integer version of that family. Thus `(schema_id = P0-SCHEMA-CASE, schema_version = 1)` is valid, while treating `P0-SCHEMA-CASE-1` and `schema_version = 1` as two version authorities is prohibited. `object_id` is always a canonical string, never a tuple or display label. A deterministic compound identity must be serialized by its declared ID constructor before it enters a record.

`provenance_status` is one of `documented`, `hypothetical`, `simulated`, or `derived`. `source_basis` is exactly one of `versioned_sources` or `synthetic_no_external_source`. `versioned_sources` requires a nonempty `source_refs` list. `synthetic_no_external_source` requires an empty list and is permitted only for a hypothetical or simulated root record. Derived and documented records always use `versioned_sources`. A `RecordRef` resolves to exactly one stored object/version pair; reusing that pair with a different hash is a blocking integrity failure.

The envelope owns record provenance. A payload must not repeat `owner_id`, `provenance_status`, `source_basis`, or `source_refs`. Domain-specific IDs below, such as `claim_id` or `action_instance_id`, must equal `meta.object_id`. Any material payload change requires a new `object_version`; a schema-shape change requires a new `schema_version`. A schema-version change that alters a material payload representation also increments the affected object version. Missing identity, ownership, version, provenance, source-basis, or reproducible hash fields are invalid rather than defaulted.

Representations contain `RecordRef` values to separately stored `Claim` or `UntypedField` records. Assessments similarly reference separately stored components and diagnostics. Implementations may dereference these records into an in-memory object graph, but persisted JSON or YAML must preserve the envelope boundary.

The persisted reference graph must be constructible without unresolved-reference or hash cycles. A parent aggregate owns references to its separately stored children; a child may carry the parent's predeclared stable ID and specification reference but does not point back to the versioned parent when the parent already references that child. Thus a `Trace` references its events while each event carries `trace_id`, not `trace_ref`. An `InterventionPair` owns the frozen intervention inputs, each generated `SystemTrace` references the pair, and a later `InterventionPairResult` joins the two completed trace references. Any proposed bidirectional `RecordRef` edge that prevents topological validation is a blocking `SCHEMA_REFERENCE_CYCLE` failure.

Every reference-bearing payload field is covered by the manifest's `reference_target_roles` matrix or by a narrower payload-local override. A declaration contains a nonempty set of permitted payload kinds or the literal `any` for an intentionally polymorphic relationship. Omission is `SCHEMA_MANIFEST_DRIFT`; resolving a typed relationship to a different payload kind is `SCHEMA_REFERENCE_TARGET_INVALID`. `any` relaxes only the target-kind restriction: identity/version resolution and cycle checks remain mandatory. The stored bundle records how many typed and explicitly polymorphic references were exercised.

### Configuration and application boundary

Formal evaluation is applied only to a validated `CompiledConfiguration`. That record binds exactly one process capability profile, one active policy profile, one independent evaluation specification, an application mapping where applicable, and one scenario overlay, together with the deterministic compiler identity and a complete parameter-binding receipt. The detailed precedence and compilation rules are fixed in `docs/CONFIGURATION_COMPILATION.md`.

The process profile supplies possible roles, stages, resources, queues, gate locations, transitions, and action types. The policy profile supplies active transformation, routing, permission, gate, timeout, correction, and restoration behavior. This separation prevents an application process diagram from silently enabling an action and prevents a counterfactual policy from inventing topology absent from its selected process profile.

Source application artifacts and their narrative descriptions are not executable rules. An application binding must map each used source element to a generic semantic target and, where behavior is claimed, to a closed `ExecutableRule`. A source parameter marked `unsupported` contributes no runtime value. A scenario overlay may fill only a declared unbound parameter slot; it cannot overwrite a documented value. Every runtime slot has exactly one visible owner, and any conflict or unresolved slot invalidates compilation before a trace can exist.

Kernel event families and simulated cases are application-neutral. Application-specific operations such as debt assertion or recovery are typed action instances, not core event IDs, and income values are semantically identified case attributes rather than required case fields. Consequently, the same formal definitions operate over a differently labeled or differently shaped evidence-to-action workflow without changing the kernel.

### Canonical serialization and hashing

All persisted records use `(canonicalization_id = UPS-CANONICAL-JSON, canonicalization_version = 1)`. Version 1 has the following complete contract:

1. validate the payload against its declared schema before hashing;
2. encode UTF-8 JSON with Unicode strings normalized to NFC, object keys sorted lexically, and no insignificant whitespace;
3. preserve array order unless the schema marks that exact field path `set_semantics`; for such fields, reject duplicates and sort elements by their canonical JSON bytes;
4. encode identifiers, enums, decimal quantities, and simulation times as schema-validated strings; decimal strings use plain notation with no leading plus, no redundant leading or trailing zeroes, and zero encoded as `"0"`;
5. encode integral counters as JSON integers and booleans and null as JSON literals; binary floating-point values, `NaN`, infinities, and negative zero are forbidden in persisted records;
6. encode civil timestamps as UTC RFC 3339 strings ending in `Z`, with seconds required and fractional seconds omitted when zero;
7. hash the canonical object `{ "meta": ..., "payload": ... }` with SHA-256 and lowercase hexadecimal output; `content_hash` is excluded from its own input; and
8. reject unknown fields, duplicate JSON keys, unresolved references, schema-family/version mismatches, and any object/version pair previously observed with another hash.

Every schema declares which arrays have `set_semantics`; no code may infer set behavior from a field name or current value. Ordered event, lineage, causal-path, and diagnostic arrays preserve order. Stable-ID collections such as action sets, alternative sets, visibility-role sets, and source-reference sets use `set_semantics` unless their schema explicitly defines an order.

Whenever a domain field permits more than one value shape, it uses this closed discriminated union rather than arbitrary JSON:

```text
TypedValue =
    NullValue(kind = null)
  | BooleanValue(kind = boolean, value: boolean)
  | IntegerValue(kind = integer, value: integer)
  | DecimalValue(kind = decimal, value: normalized_decimal_string, unit_id: string | null)
  | StringValue(kind = string, value: string)
  | IDValue(kind = id, value: string)
  | RecordRefValue(kind = record_ref, value: RecordRef)
  | ListValue(kind = list, semantics: ordered | set, values: list[TypedValue])
  | MappingValue(kind = mapping, entries: map[string, TypedValue])
```

`ListValue(semantics = set)` rejects duplicate canonical values and sorts them under the canonicalization contract; `ordered` preserves order. `MappingValue` keys use the ordinary lexical object-key rule. Unknown kinds and untagged scalars are invalid. More specific schemas, such as `AssessmentValue`, may admit only a strict subset of these variants.

## Information States and Compatible Refinements

### Compatibility set

For evidence state `e in E`, define:

```text
Gamma(e) = {theta in Theta : theta is compatible with e
            under the declared source, measurement, and admissibility rules}
```

`Gamma(e)` is owned by the evidence model, not the downstream permission rule.

### Information preorder

Write:

```text
e_more >=_E e_less
```

when all of the following hold:

1. `Gamma(e_more) subset_of Gamma(e_less)`;
2. the relationship follows from a declared coarsening, garbling, or source-addition rule fixed before permission outcomes are inspected; and
3. the two states are comparable under the same source and measurement assumptions.

`e_more >=_E e_less` means that `e_more` is at least as informative as `e_less`. Equality of compatibility sets permits informational equivalence. Strict refinement additionally requires a proper subset or another declared strictness criterion.

Define the admissible refinement set:

```text
Ref(e_less) = {e_more in E : e_more >=_E e_less
               and e_more satisfies the frozen admissibility rules}
```

Incomparable evidence states are excluded from monotonicity comparisons. Refinements may not be added or removed after their action consequences are observed.

Freezing is necessary but not sufficient. For every `e_less` evaluated under F1, the evidence model must also provide a **refinement-coverage certificate** owned by the evaluation specification. The certificate records:

- the refinement generator or complete finite enumeration;
- the source and measurement assumptions that bound admissibility;
- excluded refinement classes and reasons for exclusion;
- a coverage argument showing that no state compatible with those assumptions is silently omitted; and
- a version and hash fixed before workflow permission outcomes are inspected.

If coverage cannot be established, F1 is `unassessable`; a frozen convenience sample of refinements is not a valid universal set.

The certificate declares exactly one constructive coverage mode:

1. `finite_exact`: complete explicit enumeration;
2. `symbolic_exact`: a constraint system plus a reproducible proof or solver certificate that denotes exactly the admissible refinements;
3. `conservative_outer`: a proved superset of all admissible refinements; a universal F1 pass is valid, but a failure requires an independently validated admissible witness; or
4. `witness_search`: sampling, optimization, or adaptive search over candidate refinements; a validated admissible counterexample can prove F1 failure, but absence of a counterexample cannot produce `pass`.

Every certificate records its mode, denotation, generator or constraint version, solver and tolerance settings where applicable, proof or validation artifact, and whether the requested conclusion is sound under that mode. A sampled or merely convenient set never supports a universal pass.

`Ref(e_less)` remains the semantic target set of genuinely admissible refinements. Let `Ref_cert(e_less)` be the denotation actually represented by the certificate. Under `finite_exact` and `symbolic_exact`, `Ref_cert = Ref`; under `conservative_outer`, `Ref subset_of Ref_cert`; under `witness_search`, no coverage equality is claimed and every failure witness must be validated as a member of `Ref`. The implementation never relabels outer or sampled candidates as genuinely admissible merely because they were generated.

### Coarsening map

A deterministic coarsening is a declared many-to-one map:

```text
g: E_more -> E_less
g(e_more) = e_less
```

For finite models, partitions or hypothesis sets are sufficient. If a probabilistic relation is used, the specification must state whether it is support refinement, calibrated distributional coarsening, or Blackwell-style garbling. A scalar confidence difference alone does not define `>=_E`.

### Running administrative example

For the Robodebt application:

- `e_less` contains an annual employer-income total and a broad employment period;
- admissible `e_more` states contain fortnight-specific income and working dates consistent with that aggregate; and
- averaging the annual total across fortnights is a representation rule, not a refinement that reveals the actual fortnightly state.

## Claims, Representations, Policy Maps, and Evaluation Specifications

### Claim record

A representation is a finite set of `RecordRef` values resolving to candidate-field records. A conforming field resolves to a typed `Claim`; an `UntypedField` remains representable only so F0 can diagnose a malformed or uncertainty-laundering representation rather than failing artifact parsing before evaluation.

Each typed claim has:

```text
Claim = (
    field_kind = claim,
    claim_id,
    field_name,
    value,
    evidence_type,
    transformation_ref,
    assumption_refs,
    compatible_state_ref,
    visibility,
    semantic_id,
    semantic_type,
    semantic_scope_ref,
    polarity,
    uncertainty_status
)
```

The claim record's `meta.source_refs`, plus `transformation_ref`, `assumption_refs`, `compatible_state_ref`, and nonnull `semantic_scope_ref`, are `RecordRef` values. `meta.source_refs` is the sole source-lineage authority; the payload does not duplicate it. `assumption_refs = []` is a valid explicit declaration of no additional assumptions and denotes the universal assumption state; a missing assumption field is invalid. Semantic fields may be null when no semantic-correspondence check applies, but every field used in `exact_id` F4 correspondence must supply them. Semantic scope is versioned so a claim about an earlier object version cannot correspond to a revised object merely because its stable ID is unchanged.

```text
UntypedField = (
    field_kind = untyped,
    field_id,
    field_name,
    value,
    visibility
)
```

An `UntypedField` is still a valid `StoredRecord` with envelope provenance, but its payload deliberately has no claim evidence type, transformation, assumptions, compatible-state semantics, or semantic-correspondence fields. It therefore cannot satisfy F0. Downstream rules may still consume its value when the fixture is deliberately testing that failure mode; envelope provenance must never be promoted into missing claim-level support.

```text
Representation = (
    representation_id,
    field_refs: list[RecordRef],
    provenance_visible
)
```

`field_refs` has `set_semantics` unless a representation schema explicitly assigns semantic order. Every referenced field must resolve, its domain ID must equal its envelope object ID, and its source and transformation references must resolve before the representation is evaluable.

`evidence_type` is exactly one of:

- `observed`: directly supplied by a declared source;
- `derived`: entailed by sources under a recorded deterministic transformation;
- `imputed`: filled under an assumption and not asserted as observed;
- `disputed`: at least two live values or source claims conflict; or
- `missing`: the required value is unavailable.

For a claim `z`, let `Den(z) subset_of Theta` be the latent states in which its asserted value is true under its recorded assumptions.

### Executable rule and compatible-state records

Behavioral records may contain explanatory display text, but no evaluator, transformation, routing rule, or hash may interpret that text. Every executable choice is a closed, typed binding:

```text
ParameterBinding = (
    parameter_id,
    value_kind: literal | record_ref | record_ref_set | input_field,
    value
)

InputFieldBinding = (
    input_role_id: string,
    field_path: json_pointer
)

RuleInputSpec = (
    role_id: string,
    accepted_schema_refs: list[SchemaRef],
    cardinality: one | optional | many
)

ExecutableRule = (
    rule_id,
    rule_kind: transformation | routing | applicability | materiality |
               correspondence | deadline | support | intervention | aggregation,
    implementation_id,
    implementation_version,
    parameters: list[ParameterBinding],
    input_role_specs: list[RuleInputSpec],
    output_schema_ref: SchemaRef
)

SchemaRef = (
    schema_id,
    schema_version
)
```

`implementation_id` is selected from the study-specific closed enum in `schemas.py`; it is not a plugin name or dynamically imported function. `implementation_version` changes whenever behavior changes. Parameter names, kinds, required fields, input roles, accepted schemas, cardinalities, and output schema are validated against that implementation's declared signature. An `input_field` parameter always contains an `InputFieldBinding`; a bare JSON pointer is invalid because it cannot distinguish two inputs with the same schema. Runtime executions and assessments bind concrete records to these role IDs. A prose expression such as “current output contains X” is not executable data and cannot satisfy this contract. The immutable code-artifact hash, closed implementation signature, and rule-record hashes are all included in the freeze manifest.

Property scope is stored separately from its predicate:

```text
ScopeDeclaration = (
    scope_declaration_id,
    property_id,
    evaluation_unit_kind,
    mode: included | included_conditional | excluded | undetermined,
    applicability_rule_ref: RecordRef | null,
    exclusion_reason_code: string | null,
    undetermined_field_ids: list[string]
)
```

`included` uses a constant-true applicability rule. `included_conditional` requires an applicability rule. `excluded` requires a frozen exclusion reason and has no predicate. `undetermined` identifies the exact missing scope fields and yields `unassessable`; it is not an exclusion. Deadline semantics use typed boundary-event IDs, comparison operators, and clock/instant references. Intervention requirements use enumerated capabilities (`stop`, `delay`, `modify`) and versioned action references. Semantic correspondence uses a declared mode and enumerated compared fields; narrative rationales may accompany a mapping but never replace its typed mapping or proof artifact.

Finite source semantics use explicit records:

```text
CompatibleStateSet = (
    compatible_state_set_id,
    evidence_ref: RecordRef,
    denotation_mode: finite_exact | symbolic_exact,
    state_refs: list[RecordRef],
    projection_fact_set_ref: RecordRef,
    taxonomy_ref: RecordRef | null
)

ProjectionFactSet = (
    projection_fact_set_id,
    evidence_ref: RecordRef,
    facts: list[ProjectionFact]
)

ProjectionFact = (
    source_field_path,
    relation: equals | contains | contains_all | subset_of,
    typed_value,
    true_in_state_refs: list[RecordRef]
)
```

`finite_exact` requires a nonempty, duplicate-free `state_refs` set. Every direct derived projection must cite a transformation rule and a projection fact that establishes its source-field semantics across every compatible state. A statement that states are merely “consistent with the output” is insufficient. `symbolic_exact` instead requires the constraint and proof artifacts already required by the refinement-certificate contract.

### Representation transformation

A versioned transformation policy `kappa` maps evidence to a representation:

```text
rho_kappa: E -> R
r = rho_kappa(e)
```

The transformation cannot inspect the desired routing or permission result. Different `kappa` values may preserve, aggregate, impute, suppress, or type information differently, but every output claim remains traceable to its sources and transformation record when F0 is satisfied.

### Policy map

An operational policy map `pi in Pi` is separate from evidence and model output. It records what the workflow under test actually implements, including:

- which distinctions or uncertainty states are material;
- which actions require which evidence;
- which safeguards a material distinction triggers;
- which roles may stop, delay, modify, or authorize an action; and
- which deadlines or emergency conditions apply.

Policy relevance may not be inserted into a model-output record. The operational workflow can inspect only fields visible in `r` and `pi`.

### Independent evaluation specification

An evaluation specification `sigma in Sigma` is owned independently of the workflow transformation and decision rule. It is fixed before simulation outcomes are inspected and records:

- source-grounded or explicitly hypothetical action-support rules;
- evaluation materiality, required-meaning records, semantic-correspondence mode and artifacts, and the evidence for including or excluding each material item;
- refinement admissibility and coverage obligations;
- F2 intervention-unit rule, complete-system-state boundary, execute/hold interventions, case-local noninterference certificate when applicable, causal-key construction, paired-cohort and exogenous-input, boundary, and alignment rules;
- baseline selection criteria and permitted alternatives;
- action-comparison fields and authorization conditions;
- contestability-feasibility rules, reliability thresholds, and interval decisions;
- restoration-obligation triggers, evaluation modes, and horizons.

Historical claims in `sigma` require source references. Normative or hypothetical choices must be labeled as such and receive sensitivity analysis where a reasonable alternative could change a result. Neither `pi`, `rho_kappa`, nor `D` may define or revise `sigma` from the desired permission outcome.

Define:

```text
ActionSupported_sigma(a, e, q, t)
```

as true only when the fully instantiated action `a` satisfies the evidence, authorization, target, parameter, and timing conditions in the independent evaluation rule. This is an evaluative support judgment, not a legal conclusion and not a statement that the workflow selects the action.

For each property `Fj`, define:

```text
SpecificationValid_Fj(sigma, x)
```

as true only when the parts of `sigma` required by property `Fj` at evaluation input `x` are present, internally consistent, source-labeled, and frozen independently of workflow outcomes. F1 requires support rules, refinement coverage, baseline selection, and action comparison; F2 additionally requires intervention-unit validity, complete initial system state, the execute/hold intervention, branch-independent causal-key, boundary, paired-cohort and exogenous-input rules, and a noninterference certificate for local scope; F3 requires action-identity, required authorization capability, and execution-state support rules, while current `P_post` membership and actual reviewer authority are separate workflow inputs; F4 requires evaluation materiality, required meaning, semantic correspondence, required intervention-capability type, and surfacing-deadline semantics, while actual role identity, authority possession, and event timing are process inputs; F5 requires the applicable feasibility, reliability, obligation, horizon, consequence, and baseline rules. An unrelated missing specification component does not make a property unassessable. A property that depends on an invalid or missing required component is `unassessable` unless a separately valid failure witness is sufficient under the frozen property logic; it can never pass.

### Materiality

Define:

```text
Material_pi(e, q)
```

is the set of cases, distinctions, uncertainty states, and stopping options treated as material by the operational workflow. Separately:

```text
Material_sigma(e, q)
```

is the independently evaluated material set. F4 uses `Material_sigma`; comparing it with `Material_pi` reveals operational omissions. An item cannot be excluded from `Material_sigma` merely because surfacing it produces an inconvenient action. When materiality is genuinely contested, the competing sourced specifications are evaluated as sensitivity variants rather than collapsed into one hidden choice.

### Surfacing

For role `u in U`:

```text
Surfaced(r, q, u)
```

is the set of case IDs, typed claims, material distinctions, warnings, options, and stopping operations visible to `u` in process state `q`.

For a surfaced item `v`, independently material item `m`, and affected action `a`, let:

```text
RequiredMeaning_sigma(m, a, e, q)
```

be the frozen action-relevant proposition that must reach an authorized role, including the required type, scope, polarity, uncertainty status, and stopping or modification relevance. Each required-meaning record has a stable ID, joins the material item to the affected action and evidence/process scope, and records its source or hypothetical status, version, and owner. Define:

```text
Corresponds_sigma(v, m, a, e, q)
```

as true only when the frozen evaluation specification establishes that `v` preserves `RequiredMeaning_sigma(m, a, e, q)`. `sigma` declares one of three correspondence modes:

- `exact_id`: `v` and `m` share the stable semantic ID and the required type, scope, polarity, and uncertainty fields agree;
- `versioned_mapping`: a frozen, hashed mapping records source and target IDs, source or hypothetical status, preservation rationale, version, and owner; or
- `symbolic_entailment`: under recorded assumptions, the surfaced semantics directionally entail the required meaning:

```text
Semantics_sigma(v) entails RequiredMeaning_sigma(m, a, e, q)
```

Symbolic entailment records the rule, assumptions, solver or proof method, and reproducible witness. The reverse implication alone, satisfiable overlap, shared vocabulary, display-text similarity, a shared broad label, or the workflow's own materiality map cannot establish correspondence. A versioned mapping without an independently reviewable preservation rationale is also invalid. A missing, ambiguous, reverse-only, or circular correspondence rule makes the affected F4 item `unassessable` with `FM_SEMANTIC_CORRESPONDENCE_INVALID`.

Define semantic surfacing as:

```text
SemanticallySurfaced_sigma(m, a, e, r, q, u) iff
    exists v in Surfaced(r, q, u):
        Corresponds_sigma(v, m, a, e, q)
```

Visibility alone does not imply that `u` has authority or time to intervene.

## Decision and Routing Rule

A versioned decision rule maps the visible representation, fixed policy map, process state, and time to a total disposition:

```text
D(r, pi, q, t) = (
    route,
    routing_reasons,
    automatic_actions,
    post_review_actions,
    selected_actions,
    constraints,
    information_actions,
    restoration_actions,
    gate_requirements
)
```

Every branch must be total. Malformed or unknown inputs produce an explicit `unassessable` disposition with no automatic progression. Missing fields may not silently become zero, false, or evidence of absence unless the frozen rule explicitly and validly defines that semantics.

Representation and routing are causally distinct. A coarse representation is not intrinsically permissive; permission depends on how `D` and `pi` treat it.

`automatic_actions` and `post_review_actions` are complete sets of fully instantiated action instances that the workflow enables, not merely recommendations, selected actions, or actions observed in the trace. `selected_actions` records the subset chosen for scheduling or execution. Absence from an enabled set means unavailable under that rule version; absence only from `selected_actions` does not mean prohibited.

## Action and Authority Model

### Action record

Each `a in A` is a fully instantiated action instance:

```text
Action = (
    action_instance_id,
    action_type_id,
    actor_role_id,
    target_id,
    parameter_vector,
    resource_commitment,
    operational_or_external_consequence,
    reversibility_window,
    authorization_requirement,
    source_rule_refs,
    authority_direction
)
```

`source_rule_refs` are versioned `RecordRef` values. `action_instance_id` changes whenever a field designated behaviorally material by `sigma` changes, including target, amount, scope, timing class, authority condition, consequence, or source-rule version. `action_type_id` groups instances for reporting but is never sufficient for F1 membership. Two actions are equal in a permission set only when their canonical comparison fields match under the frozen action-comparison schema. Ambiguous or incomplete action identity makes the affected comparison `unassessable`.

An action set uses one declared representation mode:

1. `finite_explicit`: a complete finite list of action instances;
2. `symbolic_constraint`: a reproducible predicate over the action parameter vector; or
3. `ordered_family`: a symbolic predicate plus a frozen partial order `<=_A` and an explicit closure rule, such as support for every amount no greater than a declared bound.

The denotation of each mode is a set of fully instantiated actions. F1 membership can therefore be evaluated by querying `ActionSupported_sigma(a, e, q, t)` for each coarse enabled action without enumerating the entire action universe. No downward closure, substitutability, or severity ordering is inferred unless `sigma` declares and validates it. Solver-backed membership records the constraint, solver version, tolerances, and witness or proof artifact.

`authority_direction` is exactly one of:

1. `progression`: advances operational execution, commits resources or a case to a further state, imposes an external effect, or forecloses a required safeguard relative to a declared baseline;
2. `constraint`: pauses, blocks, contains, quarantines, or safely shuts down progression;
3. `information`: obtains additional evidence without independently creating an unsupported progression outcome; or
4. `restoration`: reverses or repairs a prior process or consequence state when still feasible.

The action taxonomy is relative to an evaluation baseline `b_sigma(q)` selected under the criteria in `sigma`. It is not inferred from whether an action sounds severe. The baseline record must state its source or hypothetical status, why it is the relevant comparator, and which reasonable alternatives receive sensitivity analysis. An unsupported baseline selection makes direction-dependent properties `unassessable`.

### Routine disposition

A routine or non-escalation disposition qualifies as `progression` only when all of the following are explicit:

1. it advances the workflow to a further or terminal operational state;
2. it commits the organization to no additional safeguard before a declared window closes;
3. the declared baseline would preserve that safeguard under the relevant material condition; and
4. the lost opportunity cannot be recovered automatically without a new action.

Under `P0-BASE1`, the case-bound `P0-A-ROUTINE-C1` and `P0-A-ROUTINE-C2` instances satisfy these conditions because each finalizes its exact target case and can foreclose added observation and prior review. This is organizational workflow progression, not authority over a physical object.

### Formal authority

```text
L(q) subset_of A
```

is the set of actions formally authorized in process state `q`. Historical `L(q)` values require authoritative sources. A hypothetical model may declare `L(q)` explicitly but must label it hypothetical.

### Functional permission

```text
P_auto(e, q, t) subset_of A
```

contains actions that the workflow can execute from `e` in state `q` at time `t` without a new effective prior review or external authorization event.

`P_auto` is the complete enabled set, not the selected or executed set. A workflow adapter must enumerate every automatically enabled action instance even when the simulator later selects only one.

For fixed transformation, policy, and decision-rule versions, this is derived as:

```text
P_auto(e, q, t)
    = automatic_actions(D(rho_kappa(e), pi, q, t))
```

```text
P_post(e, q, t) subset_of A
```

contains actions unavailable through the automatic path but executable through a declared review or authorization path once its prerequisites are satisfied. Review completion does not reclassify the action into `P_auto`; the exact action remains in `P_post` only while its current process-state, timing, policy, and other eligibility conditions hold.

```text
P_post(e, q, t)
    = post_review_actions(D(rho_kappa(e), pi, q, t))
```

Define:

```text
P_auto_progress(e, q, t)
    = {a in P_auto(e, q, t) : direction(a) = progression}
```

Define the independently supported progression set:

```text
J_progress_sigma(e, q, t)
    = {a in A : direction(a) = progression
                and ActionSupported_sigma(a, e, q, t)}
```

`J_progress_sigma` is owned by `sigma`, not derived from `D`, `P_auto`, selected actions, or executed traces. A workflow can therefore be internally consistent and still enable an unsupported action.

Formal authority and functional permission are independent analytical fields. The model does not assume `P_auto subset_of L`. When both are assessable:

```text
AuthorityGap(e, q, t) = P_auto(e, q, t) minus L(q)
```

is a diagnostic, not an independent legal conclusion.

### Operational action

```text
X(c, t) subset_of A
```

records actions actually executed for case `c` by time `t`. Permission does not imply execution, and execution does not establish formal authority.

## Process Traces, Gates, and Review

### Trace

A case trace `tau in Tau` is a totally ordered event sequence for one case. A system trace `tau_sys in Tau_system` contains the same event records for a frozen cohort and shared queue/resource state. Every event records a typed event kind; case; evidence; representation; process; action; transformation, decision, and transition rules; policy; actor; time; event priority; branch-independent causal-event key; root cause; descendant path; intervention pair and arm; and keyed exogenous draws as applicable. Each executed rule is paired with its execution role, exact rule reference, and role-bound runtime inputs; a generic rule reference plus an unordered input set is not replayable.

For event index `i`, define the complete pre-event state:

```text
s_i = PreState(tau, i) = (
    case_id,
    evidence_state,
    representation,
    process_state,
    time,
    policy_version,
    transformation_version,
    decision_rule_version,
    evaluation_spec_version,
    enabled_action_instances,
    selected_action_instances
)
```

For shared-capacity interventions, define:

```text
SystemState = (
    system_state_id,
    case_state_refs: list[RecordRef],
    queue_state_refs: list[RecordRef],
    resource_state_refs: list[RecordRef],
    clock_ref: RecordRef,
    scenario_ref: RecordRef,
    policy_ref: RecordRef,
    transformation_ref: RecordRef,
    decision_rule_ref: RecordRef,
    evaluation_spec_ref: RecordRef
)
```

The case, queue, and resource collections are complete for the declared intervention unit. A case-local intervention is encoded as a degenerate system state containing exactly one case and no shared resource that can affect another case. If the focal action consumes or changes a shared queue, resource, deadline service, or timeout state, a case-local declaration is invalid.

`PostState(tau, i)` is the state after applying event `i`. Every event that changes evidence, process state, time-dependent eligibility, policy, transformation, decision rule, evaluation specification, or a material action parameter creates a new state. Support and permission may not be carried across that boundary without reevaluation.

Event execution is well founded. Every event has the total order key:

```text
EventOrderKey(event) = (
    timestamp,
    priority,
    causal_event_key
)
```

`causal_event_key` is unique within a trace, so two events cannot share the same total key. Its declared constructor includes the stable root-event key and a nonempty descendant path for endogenous descendants. An event may schedule another event at the same timestamp only with a strictly increasing `microstep_rank` and a strictly decreasing frozen transition-rank measure. Each scenario declares a finite maximum microstep rank, causal-path depth, event count, and terminal horizon. Exceeding one of those bounds yields an invalid run with `SIM_EVENT_LIVELOCK` or `SIM_EVENT_BOUND_EXCEEDED`; it is never treated as ordinary censoring or a successful absence of violations. Simultaneous progression, review, authorization, evidence, and expiry events are resolved solely by the frozen priority registry.

For shorthand:

```text
P_robust_sigma(s_i)
    = intersection(
        J_progress_sigma(e_more, q_i, t_i)
        for e_more in Ref(e_i)
    )
```

using the versions recorded in `s_i`. Define trace-level support safety:

```text
TraceSupportSafe(tau) passes iff, at every event i:
    each automatically enabled progression action a
        is in P_robust_sigma(s_i)
    and each executed post-review progression action a
        is in P_post(e_i, q_i, t_i)
        and satisfies ActionSupported_sigma(a, e_i, q_i, t_i)
        and is authorized by a review valid in s_i
```

This trace property lifts the snapshot definitions without comparing unlike snapshots. A policy, process, evidence, deadline, or version change starts a new local evaluation; it is not silently folded into the earlier F1 comparison.

Each local robust-support check remains subject to its refinement-certificate mode. If the mode cannot support universal pass, `TraceSupportSafe` cannot pass merely because no violation was found; it is `unassessable` unless a validated witness establishes failure.

### Gate requirement and configuration

For action `a`:

- `GateRequired(c, a, t)` means the frozen policy requires prerequisites before `a`;
- `GateConfigured(c, a, t)` means the workflow has an explicit dependency; and
- `PrereqSatisfied(c, a, t)` means all declared evidence, authority, and review prerequisites are satisfied.

An absent gate is `not_applicable` for `GateSafe`; it is separately diagnosed as a missing required gate when `GateRequired` is true.

### Gate safety

For a configured gate:

```text
GateSafe(c, a, t) = true
```

only when the workflow makes `a` unavailable and prevents its execution at every event before `PrereqSatisfied` becomes true. A fail-open timeout is not gate-safe once it releases `a` with unmet prerequisites.

### Effective review

`ReviewEffective(c, a, t)` is true only when all conditions hold:

1. the case is surfaced before automatic progression;
2. evidence, provenance, and material uncertainty required by the review rule are visible;
3. an identified reviewer has stopping, delaying, or modifying authority;
4. the workflow enforces the dependency;
5. review begins and completes before progression or deadline expiry forecloses intervention; and
6. the decision, evidence used, and any override are recorded.

If a necessary condition is observably false, the semantic predicate is `ReviewEffective = false` and its reported assessment has `status = fail, value = false`. When required information is unavailable and no prerequisite is known to fail, the reported assessment has `status = unassessable` and no boolean value; the semantic predicate is not evaluated.

### Decision service

Let `H(c)` be the declared service deadline. A disposition is `DispositionSupported_sigma` when it satisfies the frozen independent evidence and authorization rule; this is not a legal determination.

```text
DecisionServiceEffective(c) = true
```

only when the process reaches a supported disposition by `H(c)`.

A fail-closed gate can be safe while decision service fails. A fail-open gate can convert the same delay into unsupported action.

## Property Status Values

Every reported property or helper assessment uses one envelope rather than mixing booleans, strings, and status values. All dependencies are versioned references; an unversioned component or evaluation-unit ID is invalid.

```text
Assessment = (
    assessment_id,
    property_or_helper_id,
    evaluation_unit_ref: RecordRef,
    status,
    completeness: complete | incomplete | invalid,
    value: AssessmentValue | null,
    scope_declaration_ref: RecordRef | null,
    applicability_rule_ref: RecordRef | null,
    diagnostic_refs: list[RecordRef],
    component_bindings: list[AssessmentComponentBinding],
    aggregation_rule_ref: RecordRef | null,
    false_antecedent_ref: RecordRef | null,
    missing_or_invalid_fields,
    evaluation_input_bindings: list[EvaluationInputBinding]
)

AssessmentComponentBinding = (
    role_id: string,
    relation: conjunctive_required | alternative_sufficient | contextual,
    assessment_ref: RecordRef
)

EvaluationInputBinding = (
    role_id: string,
    record_ref: RecordRef
)

AssessmentValue =
    BooleanValue(value: boolean)
  | DecimalValue(value: normalized_decimal_string, unit_id)
  | IDSetValue(values: list[string])
  | IntervalValue(lower, upper, unit_id, boundary_mode)

TypedDiagnosticValue =
    NullValue()
  | BooleanValue(value: boolean)
  | IntegerValue(value: integer)
  | DecimalValue(value: normalized_decimal_string, unit_id | null)
  | StringValue(value: string)
  | IDValue(value: string)
  | RecordRefValue(value: RecordRef)
  | IDSetValue(values: list[string])
  | IntervalValue(lower, upper, unit_id, boundary_mode)

Diagnostic = (
    diagnostic_id,
    code,
    category,
    owning_layer,
    severity: warning | blocking,
    property_or_helper_id,
    message_template_id,
    case_ref: RecordRef | null,
    trace_ref: RecordRef | null,
    action_refs: list[RecordRef],
    context_refs: list[RecordRef],
    expected_value: TypedDiagnosticValue | null,
    observed_value: TypedDiagnosticValue | null,
    artifact_path,
    suggested_next_action
)
```

`property_or_helper_id`, diagnostic `code`, diagnostic `category`, and diagnostic `owning_layer` are selected from the closed versioned registries in `data/model/schema_manifest_v1.yaml`; they are not arbitrary strings. Run status and scenario-validity status use closed registries for the same reason. Adding or renaming one of these values is a schema and protocol change, not a display-text edit.

`AssessmentValue` and `TypedDiagnosticValue` are discriminated unions, never arbitrary JSON. Semantic predicates in the definitions below remain boolean after their applicable evaluation gates pass; their reported forms, including `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective`, use `Assessment`. A report may therefore contain `status = fail` with `BooleanValue(false)`, but never place `false`, `unassessable`, and `not_applicable` in one untyped field.

`evaluation_input_bindings` is the complete, duplicate-free, role-bound set of records whose values or versions affected the assessment. A role may occur more than once only when its declared cardinality is `many`. Reports must replay from these bindings without consulting prose or guessing a record's role from its schema family. `component_bindings` distinguishes logically aggregated components from contextual helpers. A `contextual` helper can explain an incomplete assessment but cannot determine its aggregate status. This permits, for example, a currently ineffective review helper to accompany an F3 assessment whose execution horizon has not yet occurred without treating the helper as a completed F3 item. `aggregation_rule_ref = null` is permitted only for the standard conjunctive rule or an assessment with no aggregating components; any alternative, threshold, or mixed relation requires a closed executable aggregation rule.

`pass` requires `completeness = complete`, empty `diagnostic_refs`, `false_antecedent_ref = null`, and empty `missing_or_invalid_fields`. `fail` and `unassessable` require at least one diagnostic record. `not_applicable` requires `completeness = complete` and either a versioned excluded `scope_declaration_ref` or a separately stored structured false-antecedent record; it cannot be justified by a free-text sentence. Component assessments and diagnostics are separately stored `StoredRecord` objects and their references must resolve before aggregate validation.

`completeness = complete` means every input required to evaluate the reported scope and condition was available and valid. `incomplete` means a required input, horizon, or precision target remains unavailable, but the available inputs are not structurally invalid. `invalid` means a required schema, specification, reference, rule binding, or aggregation contract is invalid. A definitive counterexample can produce `status = fail` with `completeness = incomplete` when the missing material cannot reverse that counterexample. Invalid material produces `unassessable` unless a separately valid counterexample is sufficient under the property's frozen logic.

Every formal assessment returns exactly one aggregate status:

- `pass`: the property is in scope, every required condition was evaluated, and every condition holds;
- `fail`: the property is in scope and at least one sufficient, independently valid failure witness establishes that a required condition is violated;
- `unassessable`: applicability cannot be established, or the property is in scope but no sufficient failure witness exists and required evidence, input, precision, horizon, or specification is unavailable or invalid; or
- `not_applicable`: the property's antecedent is false or the property is outside the fixture's declared scope.

### Property-scoped evaluation contracts

The following contracts are frozen with `sigma` and the applicable fixture or process profile. Scope declaration and substantive antecedent resolution are separate: a missing or ambiguous scope declaration uses `FM_APPLICABILITY_UNDETERMINED`, while a declared conditional scope with missing resolution input or specification uses the input or specification diagnostic.

| Property | Included scope and demonstrably false antecedent | Inputs/specification needed to resolve the antecedent | Additional requirements when applicable |
| --- | --- | --- | --- |
| F0 | included when representation fidelity is declared for the unit; false only through an explicit fixture/profile scope exclusion | declared representation and consumer/role scope | source records and versions; candidate representation fields; transformation; lineage, compatible-state, and visibility records; operational-policy fields; claim-support semantics; applicable inspectability/materiality rules |
| F1 | included when an evidence-refinement comparison for automatic progression is declared; false through an explicit scope exclusion, not merely because the automatic progression set is empty | comparison ID, `e_less`, process/time scope, and frozen refinement relation | transformation, policy, and decision-rule versions; complete automatic progression set; action identities; refinement certificate/denotation; support rule; admissibility/coverage; baseline; action-comparison schema |
| F2 | included when fallback evaluation over a declared refinement comparison is in scope; false when a valid comparison establishes no `FallbackAdded` action or the fixture explicitly excludes the comparison | compared evidence states and complete action sets; action directions and identities; refinement relation and coverage | complete initial system state and intervention unit; transition model; execute/hold system traces and interventions; noninterference certificate for local scope; causal keys; paired cohort and exogenous inputs; boundary, alignment, reversibility, and independent-authorization rules |
| F3 | included when post-review progression evaluation is in scope; false when valid current action sets contain no in-scope progression action in `P_post` | current `P_post`; action directions and identities; action-comparison schema | execution-state `P_post`; gate state; review record; actual reviewer role/authority; evidence/process states; event timing and versions; required authorization capability; execution-state support and override rules |
| F4 | included when surfacing preservation is declared for the action scope; false when a valid evaluation-materiality rule yields no material item affecting an in-scope action | in-scope action records; evaluation materiality and action scope | representation and surfaced items; required-meaning/correspondence artifacts; required intervention-capability and deadline semantics; actual role assignment/authority; process state; progression, expiry, and surfacing times |
| F5 | included when contestability/restoration evaluation is declared for the action scope; false when valid action and obligation-scope rules establish that no in-scope action carries either obligation | in-scope consequential actions; obligation-scope, evaluation-mode, and consequence-scope rules | action/post-state; process graph; actual standing, evidence access, capacity, timing and trace; feasibility rules; thresholds and interval rule; consequence values; baseline-selection rule and values; horizons |

A fixture-level scope exclusion is a versioned `ScopeDeclaration` with `mode = excluded`, and the assessment references it through `scope_declaration_ref`. An included-but-conditional property cannot become `not_applicable` until all antecedent-resolution inputs and specification components validate. Once the antecedent is true, a missing additional input is `FM_REQUIRED_INPUT_MISSING` and a missing or invalid additional `sigma` component is `FM_EVALUATION_SPEC_INVALID`; neither may be reclassified as a false antecedent.

For property `Fj` at input `x`, the evaluator uses this ordered procedure:

```text
Evaluate(Fj, x):
    1. read the frozen ScopeDeclaration_Fj(x)
    2. if the scope declaration is missing or invalid:
           return unassessable with completeness = invalid
               and FM_APPLICABILITY_UNDETERMINED
    3. if mode = undetermined:
           return unassessable with completeness = incomplete
               and FM_APPLICABILITY_UNDETERMINED
    4. if mode = excluded:
           return not_applicable
    5. validate AntecedentInputs_Fj(x)
    6. if an antecedent-resolution input is missing:
           return unassessable with completeness = incomplete
               and FM_REQUIRED_INPUT_MISSING
    7. if an antecedent-resolution input is invalid:
           return unassessable with completeness = invalid
               and FM_REQUIRED_INPUT_MISSING
    8. validate AntecedentSpecification_Fj(sigma, x)
    9. if an antecedent-resolution specification component is missing or invalid:
           return unassessable with completeness = invalid
               and FM_EVALUATION_SPEC_INVALID
   10. evaluate Applicable_Fj(x)
   11. if Applicable_Fj(x) is false:
           return not_applicable
   12. validate and evaluate each independently decidable condition or item
   13. retain every sufficient, independently valid failure witness
   14. record missing condition inputs as incomplete and invalid condition
       specifications or bindings as invalid
   15. if any retained witness is sufficient under the frozen property logic:
           return fail with completeness = complete, incomplete, or invalid
           as established by the remaining required material
   16. if no sufficient failure witness exists and required material is missing:
           return unassessable with completeness = incomplete
   17. if no sufficient failure witness exists and required material is invalid:
           return unassessable with completeness = invalid
   18. return pass with completeness = complete
```

Applicability rules and scope exclusions are frozen before outcomes are inspected. Missing evidence cannot be converted into `not_applicable` by declaring a case out of scope after the fact.

For a conjunctive aggregate, any `fail` item makes the aggregate `fail`; otherwise any `unassessable` item makes the aggregate `unassessable`; otherwise at least one `pass` makes it `pass`; otherwise all items are `not_applicable` and the aggregate is `not_applicable`. The aggregate completeness is the worst applicable component completeness under `invalid > incomplete > complete`. Contextual bindings never enter this truth aggregation. Disjunctive or threshold aggregates must declare their own frozen truth table and sufficient-witness rule rather than reuse the conjunctive rule. An absent or unknown item status, a missing applicable item, an undeclared component relation, or an aggregate output that violates its declared rule returns `unassessable` with `completeness = invalid` and `FM_STATUS_AGGREGATION_INVALID`; it blocks freeze or execution until corrected.

## F0: Evidentiary Fidelity

F0 has four separately reported dimensions.

### F0.1 Claim support

- An `observed` claim must be supplied by its declared source.
- A `derived` claim must be entailed by its source claims under its recorded transformation and assumptions:

```text
Gamma(e) is not empty
and AssumptionStates(z) is not empty
and Gamma(e) intersect AssumptionStates(z) is not empty
and Gamma(e) intersect AssumptionStates(z) subset_of Den(z)
```

The nonempty conditions prevent contradictory evidence or assumptions from satisfying entailment vacuously. If consistency cannot be assessed, claim support is `unassessable`.

- An `imputed` claim need not be entailed, but it must remain typed `imputed`, retain its assumption and compatible-state set, and never masquerade as observed.
- `missing` and `disputed` claims cannot silently become observed values.
- A material `UntypedField` fails F0.1 with `FM_EVIDENCE_TYPE_COLLAPSED`; it cannot borrow a claim type or lineage from transformation code that downstream consumers cannot inspect.

### F0.2 Lineage completeness

Every material candidate field is a typed `Claim`, and every material claim retains source, transformation, assumption, and version IDs sufficient for deterministic replay. A material `UntypedField` fails this dimension.

### F0.3 State distinction

Observed, derived, imputed, disputed, and missing states remain distinguishable to every downstream rule that uses the field.

### F0.4 Inspectability

Downstream rules and authorized reviewers can inspect the type and provenance needed by the operational policy and applicable evaluation specification.

Define:

```text
F0(e, r, pi, sigma) =
    ClaimSupport(e, r)
    and LineageComplete(r)
    and StateDistinction(r)
    and Inspectable(r, pi, sigma)
```

A truthful broad label can pass claim support but fail F0 because its lineage, assumptions, alternatives, or uncertainty are unavailable. F0 failure therefore does not imply literal falsehood.

## F1: Robust Automatic-Permission Monotonicity

For fixed process state, time, evaluation specification, baseline, operational policy map, representation rule, decision rule, and action taxonomy, define the robust support envelope:

```text
P_robust_sigma(e_less, q, t)
    = intersection(
        J_progress_sigma(e_more, q, t)
        for e_more in Ref(e_less)
    )
```

`P_robust_sigma` is the largest set of progression action instances independently supported across every admissible refinement. It is not derived from what the workflow happens to enable under those refinements.

```text
F1(e_less, q, t, sigma) passes iff
    SpecificationValid_F1(sigma, (e_less, q, t))
    and refinement coverage mode supports a universal pass
    and every compared action instance has unambiguous identity
    and P_auto_progress(e_less, q, t) subset_of P_robust_sigma(e_less, q, t)
```

Equivalently, F1 fails when there exist `a` and `e_more in Ref(e_less)` such that:

```text
a in P_auto_progress(e_less, q, t)
and a not_in J_progress_sigma(e_more, q, t)
```

The failure witness must report why `ActionSupported_sigma(a, e_more, q, t)` is false and validate that `e_more` is genuinely admissible. Missing support rules, an unsound certificate for the requested conclusion, or ambiguous action identity produce `unassessable`, not `pass`. `witness_search` can establish failure from a validated counterexample but never pass from failure to find one. A `conservative_outer` pass is sound, while a failure is conclusive only when its witness is independently validated as admissible. Only enabled automatic progression actions are tested. Selected actions, incomparable states, changed deadlines, different policies, changed process states, and post-review actions do not belong in one F1 comparison.

A workflow that automatically enables the same action under every evidence state does not thereby pass: it fails whenever the independent support rule excludes that action under any admissible refinement.

## F2: Safe Fallback Allowance

F2 is an allowance, not an obligation. Define a fallback added under weaker evidence:

```text
FallbackAdded(a, e_less, q, t) iff
    a in P_auto(e_less, q, t)
    and direction(a) in {constraint, information}
    and exists e_more in Ref(e_less): a not_in P_auto(e_more, q, t)
```

For every `FallbackAdded` action `a`, whether or not the observed policy selected it, construct an interventional pair from initial system state `S_0` under identical frozen cohort membership and exogenous inputs:

```text
tau_do_sys   = system trace under Execute(a, S_0)
tau_hold_sys = system trace under Hold_a(S_0)
```

`Hold_a` is an explicit baseline intervention frozen with the transition model and evaluation specification before outcomes are inspected. The execute and hold arms share one intervention-pair ID, which is excluded from branch labeling and supplies their common intervention root key. `Hold_a` records that `a` was withheld, applies none of `a`'s direct state changes, and schedules no event whose causal root is that withheld action; events of the same type caused by another root remain eligible. Every other initial state component, cohort member, policy, resource, and exogenous input remains identical. `Hold_a` may not be replaced after the fact by another active policy. If no substantively valid hold intervention can be declared, F2 is `unassessable`.

The `InterventionPair` record is frozen before either arm executes and therefore contains no outcome-trace references. Each completed `SystemTrace` references that pair. After both traces validate independently, an `InterventionPairResult` references the pair and both traces and becomes the F2 assessment unit. This direction of ownership prevents an intervention/trace hash cycle and prevents observed outcomes from entering the intervention specification.

The intervention pair declares `intervention_unit = case_local | cohort_system`. `case_local` is valid only when a frozen noninterference certificate establishes that executing `a` cannot change a shared queue, resource, service deadline, timeout transition, or another case's state before the comparison boundary. Otherwise `cohort_system` is required. A local pass supports only the within-case statement `F2_local`; it cannot establish system-level safe fallback. The paper's shared-capacity policies use `cohort_system` and report both focal-case and spillover results.

Paired states are aligned by causal cuts, never by event index. Every event has a branch-independent key:

```text
CausalCut(event) = (
    time_since_S_0,
    event_priority,
    causal_event_key
)
```

where `causal_event_key` is derived from the stable case ID, root exogenous-event or intervention ID, and descendant path rather than queue position or branch label. Let `K` be the sorted union of causal cuts appearing in either system trace plus the declared horizon cut. `CutState(tau_sys, k)` is the complete system state after all events with keys less than `k` and before any event at `k`; when a keyed event is absent from one branch, that branch simply carries its prior state to the next cut. Shared exogenous events use the same `(case_id, event_family, draw_index)`, value, and cut in both traces. Endogenous descendants may occur in only one branch without shifting later exogenous draws or state correspondence.

The comparison stops for each affected case immediately before that case's earliest cut in either trace containing a new-evidence event, effective review, external authorization, separately declared intervention, or the causal horizon. Define `UnsupportedRelease_sigma(a, S_0)` as true when, for the focal case or any case in the declared intervention unit, some aligned cut `k` before that case's boundary automatically enables a progression action `p` in `CutState(tau_do_sys, k)`, does not enable it in `CutState(tau_hold_sys, k)`, and places it outside `P_robust_sigma` at the do-branch case pre-state. Support is therefore recomputed where `p` is enabled rather than inherited from `S_0`. This captures queue and timeout spillovers: an information or review action for one case is unsafe under `F2_system` if its resource effect releases unsupported progression for another case. Reachability is evaluated on the frozen transition model; labels such as “information” do not determine the result.

For each added fallback action:

```text
F2Item(a, S_0, sigma) passes iff
    FallbackAdded(a, e_less(S_0), q(S_0), t(S_0))
    and the declared intervention unit is valid
    and not UnsupportedRelease_sigma(a, S_0)
    and a satisfies its declared reversibility conditions
    and a satisfies its independent authorization conditions
```

`F2(S_0, sigma)` is `pass` only when every added fallback item passes at its declared intervention scope, `fail` when any item has a sufficient failure witness, `not_applicable` when a valid comparison establishes that no fallback is added, and `unassessable` when refinement coverage, the hold intervention, intervention-unit validity, causal-cut keys, paired causal semantics, transition model, support rule, action identity, or another required condition is unavailable. F2 does not excuse a progression action merely because it is described as precautionary.

## F3: Review-Preserved Progression

F3 applies only to progression actions withheld from `P_auto` and placed in `P_post`. Each review decision records:

```text
ReviewDecision = (
    review_id,
    case_ref: RecordRef,
    reviewer_role_id,
    authority_ref: RecordRef,
    evidence_refs: list[RecordRef],
    representation_ref: RecordRef,
    policy_ref: RecordRef,
    rule_ref: RecordRef,
    authorized_action_refs: list[RecordRef],
    authorization_conditions,
    decision_time,
    expiry_time,
    decision,
    reason_refs: list[RecordRef],
    revalidation_refs: list[RecordRef]
)
```

Every reference resolves to its exact object version and canonical content hash. `ReviewAuthorizes(review_id, a, t_exec)` is true only when the exact fully instantiated action reference appears in the authorized set, all recorded conditions still hold, the case, representation, evidence, policy, and rule versions remain valid or receive a recorded revalidation, and execution follows `decision_time` and precedes expiry. A changed amount, target, consequence, material evidence state, representation, policy, or rule requires revalidation or a new review.

For action `a`, trace `tau`, review state `s_review`, and execution pre-state `s_exec`, F3 passes only when:

```text
a in P_post(e(s_review), q(s_review), t(s_review))
and a not_in P_auto(e(s_review), q(s_review), t(s_review))
and GateRequired(c, a, t(s_review))
and GateConfigured(c, a, t(s_review))
and GateSafe(c, a, t_exec)
and ReviewEffective(c, a, t_review)
and ReviewAuthorizes(review_id, a, t_exec)
and a in P_post(e(s_exec), q(s_exec), t(s_exec))
and ActionSupported_sigma(a, e(s_exec), q(s_exec), t(s_exec))
and execution(a) occurs only after that recorded review decision
```

Current `P_post` membership is checked independently of recorded authorization. A process-state, timing, eligibility, or policy change can remove the action from the current post-review set even when the earlier review remains authentic; such an action must not execute without a new valid route and, where required, revalidation. The independent support rule may recognize a documented discretionary override, but its evidence, authority, reasons, and scope must be encoded in `sigma` and satisfied at `s_exec`. A notification, response opportunity, reviewer label, nonblocking review, fail-open timeout, post-action reassessment, stale review, unsupported reviewer decision, review of a different action instance, or authorization for an action no longer in the current post-review set does not satisfy F3.

F3 is not a substitute for F1: a progression action protected by valid review is outside the automatic set tested by F1.

## F4: Surfacing Preservation

Let `u` range over roles authorized to stop, delay, or modify action `a`. Define:

```text
F4Item(m, a, e, r, q, t, sigma) passes iff
    m in Material_sigma(e, q)
    and exists u such that
        SemanticallySurfaced_sigma(m, a, e, r, q, u)
        and u has relevant intervention authority over a
        and surfacing occurs before the earliest progression or expiry event
```

`F4(c, e, r, q, t, sigma)` evaluates every applicable `(m, a)` pair. It is `pass` only when every item passes, `fail` when at least one item fails, `not_applicable` when the valid evaluation specification contains no material item affecting an in-scope action, and `unassessable` when evaluation materiality, semantic correspondence, role authority, action identity, or event timing is unavailable. A mismatch in which `m in Material_sigma` but `m not_in Material_pi` is reported explicitly as an operational-materiality omission.

F4 fails when abstraction or operational policy removes a material case, distinction, uncertainty state, warning, or stopping option from every authorized role before intervention becomes impossible.

Action-set counts are not sufficient. Replacing one stopping option with one progression option can preserve the count while violating F4.

## F5: Contestability and Restoration

### Contestability

Represent the process as a directed state-transition graph `G = (Q, transitions)`. Define `StructurallyFeasibleCorrectionPath(c, a, s_post)` as a path from the post-action state that can halt or modify `a` within its contestability window and whose transitions have a legally or hypothetically authorized actor, attainable required evidence, available procedural standing, and satisfiable ordering conditions.

```text
StructurallyContestable(c, a, s_post) = true iff
    at least one StructurallyFeasibleCorrectionPath(c, a, s_post) exists
```

Graph-theoretic reachability alone is insufficient. Structural contestability still does not claim that a case can operationally use the path under realized access, burden, workload, or timing.

For stochastic or capacity-constrained processes, define prospective operational contestability:

```text
p_contest(c, a, s_post)
    = Pr_sigma(
        a correction path can be initiated and completed by H_contest(c, a)
        | s_post, frozen policy and exogenous model
      )

ContestabilityProspective(c, a, s_post) passes iff
    StructurallyContestable(c, a, s_post)
    and p_contest(c, a, s_post) >= alpha_contest_sigma(c, a)
```

For an exact calculation, compare `p_contest` directly with the frozen reliability threshold. For Monte Carlo estimation, `pass` requires the prespecified interval lower bound to meet the threshold, `fail` requires its upper bound to fall below the threshold, and an interval crossing the threshold is `unassessable` pending additional precision. The interval rule, confidence level, and replication extension rule are frozen before results.

For a completed trace, define realized operational contestability:

```text
ContestabilityRealized(c, a, tau) passes iff
    before H_contest(c, a), at least one declared correction path
    was actually available with its required notice, evidence access,
    standing, authority, service capacity, and timing conditions
```

The realized opportunity is reported separately from whether the affected person invoked it and whether a correction ultimately completed.

### Restoration

For modeled consequence dimensions `k in K`, let `z_k(c, t)` be the case consequence and `z_k^base(c)` its baseline value.

```text
RestorationComplete(c, t) = true iff
    for every modeled k in K:
        z_k(c, t) = z_k^base(c)
    and no declared irreversible residual remains
```

If the decision state is corrected but any modeled monetary, recovery, burden, timing, or external consequence remains, restoration is partial.

Let `ContestabilityDue_sigma(c, a, t)` mean that the independent evaluation specification requires a live correction path, let `RestorationDue_sigma(c, a, t)` mean that it has triggered a correction or restoration obligation, and let `H_restore(c, a)` be its deadline. Then:

```text
F5Prospective(c, a, s_post, sigma) passes iff
    a is an in-scope consequential action
    and, when contestability is due,
        ContestabilityProspective(c, a, s_post) passes
    and, when prospective restoration is evaluated,
        Pr_sigma(RestorationComplete by H_restore | restoration due, s_post)
            >= alpha_restore_sigma(c, a)

F5Realized(c, a, tau, t_eval, sigma) passes iff
    a is an in-scope executed consequential action
    and, for every applicable component,
        its evaluation horizon has been reached
        or that component completed early
    and, when contestability is due,
        ContestabilityRealized(c, a, tau) passes
    and, when restoration is due,
        exists t_restore <= H_restore(c, a):
            RestorationComplete(c, t_restore)
```

`sigma` declares whether a reported aggregate is prospective or realized; the paper reports structural, prospective, and realized components separately wherever each is available. A realized component that is incomplete before its deadline returns `status = unassessable` with `FM_EVALUATION_HORIZON_PENDING`, not `fail`. After the horizon, F5 is `fail` when a required operational contest path was unavailable or a triggered restoration obligation remained incomplete. It is `unassessable` when an applicable graph, reliability threshold, probability or interval rule, access or capacity input, consequence dimension, baseline, obligation, or horizon is missing. It is `not_applicable` only when valid action and obligation-scope records establish that no in-scope action carries a contestability or restoration obligation.

When prospective restoration is estimated rather than calculated exactly, the same frozen lower-bound/pass, upper-bound/fail, and threshold-crossing/unassessable interval rule used for prospective contestability applies to `alpha_restore_sigma`.

## Headline Proposition 1: Robust Permission

### Assumptions

- `Ref(e_less)` has a frozen constructive certificate whose coverage mode is sound for the claimed pass or failure.
- Process state, time, policy, representation rule, decision rule, baseline, and action taxonomy are held fixed.
- `sigma` is valid and independent of the workflow under evaluation.
- Progression action identity, independent support, and automatic permission are total and inspectable through finite or reproducible symbolic membership queries.

### Statement

`P_robust_sigma(e_less, q, t)` is the unique maximal progression-action set, ordered by set inclusion, independently supported under every admissible refinement. F1 holds if and only if:

```text
P_auto_progress(e_less, q, t)
    subset_of P_robust_sigma(e_less, q, t)
```

### Proof sketch

Every member of the intersection is independently supported by each admissible refinement, so the intersection itself is refinement-robust. Any strict superset contains at least one action outside the intersection; by definition, at least one refinement does not support that action, so the superset is not robust. The F1 equivalence follows immediately. A single unsupported membership provides a finite counterexample and proves failure. Because support comes from `sigma` rather than `D`, universal workflow permissiveness cannot satisfy the proposition by construction.

### Satisfying case

Under aggregate evidence, the workflow may hold the case and request records. Those are constraint and information actions. No automatic progression action is added, so F1 is preserved and F2 may apply.

### Minimal counterexample

A coarse annual total automatically permits a fully instantiated consequential imputed disposition. Under one admissible fortnight-specific refinement, the independent support rule excludes that same action instance. The action belongs to the coarse automatic progression set but not to the robust support envelope, so F1 fails.

### Executable diagnostic

For each coarse state and action, emit the refinement record or symbolic witness under which independent support fails. A violation report must include the coarsening-map ID, coverage mode, certificate and denotation hashes, action instance and type IDs, material parameter vector, coarse permission reason, evaluation-rule ID, failed support condition, and validated counterexample refinement.

## Headline Proposition 2: Operational Review

### Assumptions

- Event ordering is deterministic.
- A fail-closed gate cannot be bypassed while prerequisites are unmet.
- Review work has declared service demands and finite capacity.
- Deadline and timeout semantics are explicit.

### Statement

1. A correctly enforced fail-closed gate preserves `GateSafe` regardless of queue delay, but does not by itself establish `ReviewEffective` or `DecisionServiceEffective`.
2. For a finite service window of length `H`, reviewer capacity `c`, initial unfinished workload `B0`, and required review work `W`, if:

```text
W + B0 > c * H
```

then not every required review can complete within the window under any work-conserving schedule.
3. When prerequisites remain unmet at timeout, fail-closed semantics convert the capacity shortfall into unresolved or delayed cases; fail-open semantics can convert it into unsupported automatic progression.

### Proof sketch

Part 1 follows from the structural dependency: no event can enable or execute the guarded action before prerequisites. Review may nevertheless lack evidence, authority, service, or time. Part 2 is a capacity bound: required work exceeds the maximum service deliverable within the window. Part 3 follows by applying the declared timeout transition to cases whose prerequisites remain unmet.

### Boundary case

When `W + B0 = c * H`, completion is possible only if service is perfectly available and no setup, priority, evidence, or synchronization loss exists. The simulation must not label equality as a robust operating margin.

### Counterexample to nominal review

A workflow displays a review field but permits action at timeout without a completed review. The gate is fail open, `ReviewEffective` is false, and the reviewer label does not satisfy F3.

### Queueing corollary

For a stationary work-conserving review queue under standard regularity assumptions, offered load at or above service capacity cannot sustain a stable bounded backlog. The simulation uses the finite-window capacity bound as the primary interpretation and treats asymptotic queueing results as validation support.

## Headline Proposition 3: Contestability and Restoration

### Assumptions

- The process graph, authorized correction transitions, deadlines, evaluation mode, and consequence dimensions are declared before evaluation.
- Evidence access, procedural standing, service capacity, timing feasibility, reliability thresholds, interval rules, and restoration-obligation rules are declared before evaluation.
- Baseline values exist for every modeled restoration dimension.

### Statement

Nominal notice or correction of one decision coordinate does not establish F5. Structural path existence, prospective operational reliability, realized opportunity, correction uptake, and restoration are distinct. A prospective pass requires the frozen reliability threshold; a realized pass requires an actually available path by the contestability horizon and, whenever restoration is due, return of every modeled consequence dimension to baseline by the restoration horizon with no declared irreversible residual.

### Proof sketch

If no structurally feasible correction path exists, neither prospective nor realized operational contestability can pass. If the estimated operational probability lies below the frozen threshold, the prospective condition fails; if no path was actually available by the horizon, the realized condition fails. If a transition corrects the decision coordinate but some `z_k` differs from baseline, the universal condition for `RestorationComplete` is false. Before an unresolved horizon, the realized component is `unassessable`, not prematurely failed.

### Satisfying case

A timely reassessment halts recovery, corrects the decision, returns all modeled funds, clears recovery status, and leaves no residual modeled exposure.

### Minimal counterexample

A reassessment zeros the decision balance after recovery activity has already produced a modeled residual consequence. The decision coordinate is corrected, but restoration remains partial.

## Supporting Formal Results

| ID | Result | Assumptions | Primary property | Executable witness |
| --- | --- | --- | --- | --- |
| `FR0` | Unsupported point detail presented as observed, or stripped of required provenance and assumptions, fails evidentiary fidelity. | Claim semantics and policy-required lineage declared | F0 | offending claim and missing lineage fields |
| `FR1` | One admissible refinement under which an independently evaluated support rule excludes a coarse-state automatic progression action is sufficient to fail robust permission. | Valid `sigma`, certified refinement coverage, and unambiguous action identity | F1 | action/refinement/support-rule triple |
| `FR2` | New constraint or information actions under weaker evidence can be allowed without violating F1 when an explicit execute-versus-hold pair aligned by causal cuts shows they cannot release progression outside the envelope at the resulting pre-state. | Frozen hold intervention, causal keys, paired semantics, and safe-fallback conditions hold | F2 | aligned trace pair and causal non-release proof |
| `FR3` | A fail-closed gate can remain safe even when review or decision service fails. | Enforced dependency and deterministic ordering | Gate safety | held action plus failed review reason |
| `FR4` | Notification, nonblocking review, fail-open timeout, stale review, unsupported reviewer decision, review of a different action instance, loss of current post-review eligibility, or post-action correction does not establish review-preserved progression. | Review prerequisites, execution-state eligibility and support, and exact action identity declared | F3 | first failed prerequisite, eligibility/support failure, or authorization mismatch |
| `FR5` | Required review work beyond finite-window capacity prevents universal timely completion. | Work and capacity measurable | Operational review | `W + B0 - cH` shortfall |
| `FR6` | Decision correction does not establish complete restoration when any modeled residual remains after the restoration horizon. | Consequence vector and evaluation horizon declared | F5 | non-restored dimension |
| `FR7` | Surfacing can fail even when action-set counts are unchanged, display text resembles the material item, or the operational policy omits the item from its own materiality map. | Valid independent materiality, semantic correspondence, and stable action identity | F4 | removed or non-corresponding material item, policy omission, or stopping option |

These eight results support the three headline propositions; they are not eight competing article claims.

## Executable Diagnostic Contract

### Required inputs

- valid `RecordMeta` envelopes and canonical content hashes for every stored object used by the evaluation;
- stable evidence-state IDs and `Gamma` or equivalent finite compatibility records;
- coarsening-map, admissible-refinement-set, constructive coverage mode, and refinement-certificate IDs;
- typed representation claims with lineage;
- frozen operational policy map and independently owned evaluation specification;
- total decision rule;
- fully instantiated action records, action-set representation and membership-query artifacts, canonical comparison schema, and sourced baseline-selection record;
- F2 execute and hold interventions, declared intervention unit, complete initial system state, case-local noninterference certificate where applicable, branch-independent causal-event keys, event priorities, boundary rules, and keyed exogenous-input records;
- F4 required-meaning records and correspondence mode plus exact-ID records, versioned mappings, or symbolic-entailment artifacts as applicable;
- process, role, authority, gate, deadline, and service records;
- review decisions binding exact action instances, evidence, rule versions, conditions, and expiry;
- frozen causal transition graph for safe-fallback and contestability checks;
- ordered event and system traces with complete pre- and post-event state/version records, total event keys, termination bounds, and explicit invalid-run diagnostics;
- frozen scope-declaration and executable-applicability-rule records, property-scoped antecedent/condition input and specification schemas, stable status-reason diagnostic records, and status-aggregation rules;
- F5 evaluation mode, reliability thresholds, interval decision rules, and contestability/restoration horizons; and
- consequence vector and restoration baseline where F5 is evaluated.

### F0 check

```text
for each material candidate field z in representation:
    fail explicitly if z is an UntypedField
    validate evidence type
    validate support rule for that type
    reject empty or inconsistent evidence/assumption intersections
    validate source, transformation, assumption, and version lineage
    validate observed/derived/imputed/disputed/missing distinction
    validate policy-required downstream inspectability
return pass only if every dimension passes
```

### F1 check

```text
for each e_less:
    validate SpecificationValid_F1(sigma, (e_less, q, t))
    validate that the constructive coverage mode supports the requested conclusion
    freeze and hash the refinement certificate, denotation, and generator or constraints
    validate canonical identity and action-set membership semantics
    coarse = P_auto_progress(e_less, q, t)
    for each a in coarse:
        query ActionSupported_sigma(a, e_more, q, t)
            universally over the certified refinement denotation
    for each violation emit a counterexample refinement
        and the failed independent support condition;
        validate witness admissibility
```

Empty or missing refinement sets, a coverage mode unsound for the requested conclusion, missing independent support, ambiguous action identity, or an unresolved symbolic query are `unassessable`, not automatic passes. `witness_search` can prove failure from a validated witness but never universal pass.

### F2 check

```text
evaluate frozen applicability and property-scoped inputs
identify every FallbackAdded action from the focal case in initial system state S_0
if a valid comparison finds none: return not_applicable
for each fallback:
    construct the complete initial system state S_0
    validate cohort membership and shared queue/resource closure
    require a noninterference certificate for case_local scope;
        otherwise require cohort_system scope
    apply the frozen Execute and Hold_a interventions
    generate tau_do_sys and tau_hold_sys under identical cohort membership
        and keyed exogenous inputs
    build the sorted union of branch-independent causal cuts
    validate shared exogenous event keys, values, and cuts
    compare complete system CutState values until each affected case's
        earliest causal boundary
    at every cut where progression is newly enabled only in tau_do_sys
        for any case in scope:
        recompute P_robust_sigma at that case's do-branch pre-state
        fail if the action is outside that current envelope
    validate reversibility and independent authorization conditions
return pass only if every fallback passes
```

### F3 and review check

```text
if action is not post-review progression:
    return not_applicable
check gate required, configured, and safe
check evidence and uncertainty visibility
check reviewer identity and stopping authority
check enforced dependency
check completion before action and deadline
check exact action instance is in the recorded authorization
check target, parameters, evidence, policy, and rule versions
check authorization conditions and expiry at execution
recompute P_post at the execution pre-state
fail if the exact action is no longer in the current post-review set
recompute ActionSupported_sigma at the execution pre-state
check recorded decision, revalidation, and override
```

### F4 check

```text
validate independent evaluation materiality
validate required-meaning records, required intervention capability,
    and surfacing-deadline semantics
validate the independent semantic-correspondence mode and artifacts
compare Material_sigma with Material_pi and report omissions
for each evaluation-material item and affected action:
    read actual role assignments and intervention authority
        from the process inputs
    find the first surfaced item satisfying Corresponds_sigma
    find earliest progression or expiry event
    fail if no authorized role receives a semantically corresponding item in time
```

### F5 check

```text
check structural path feasibility
if prospective mode:
    estimate or calculate p_contest and any restoration probability
    apply frozen thresholds and interval decision rules
if realized mode:
    if an unresolved deadline has not been reached:
        return status = unassessable
            with FM_EVALUATION_HORIZON_PENDING
    check actual path availability by H_contest
    if restoration is due, compare every modeled consequence dimension
        with its baseline by H_restore
report structural, prospective, realized-opportunity,
    correction-uptake, restoration, and aggregate statuses separately
```

## Diagnostic Codes

Minimum blocking diagnostics are:

- `SCHEMA_MANIFEST_DRIFT`;
- `SCHEMA_PARTIAL_EMBEDDED_RECORD`;
- `SCHEMA_ENVELOPE_AUTHORITY_DUPLICATED`;
- `SCHEMA_EXECUTABLE_RULE_INVALID`;
- `SCHEMA_DIAGNOSTIC_INCOMPLETE`;
- `SCHEMA_REFERENCE_UNRESOLVED`;
- `SCHEMA_REFERENCE_TARGET_INVALID`;
- `SCHEMA_REFERENCE_CYCLE`;
- `SCHEMA_CANONICALIZATION_INVALID`;
- `FM_EVIDENCE_ORDER_CIRCULAR`;
- `FM_REFINEMENT_SET_MISSING`;
- `FM_REFINEMENT_COVERAGE_UNPROVEN`;
- `FM_REFINEMENT_MODE_UNSOUND_FOR_CONCLUSION`;
- `FM_REFINEMENT_WITNESS_INVALID`;
- `FM_REFINEMENT_INCOMPARABLE`;
- `FM_APPLICABILITY_UNDETERMINED`;
- `FM_REQUIRED_INPUT_MISSING`;
- `FM_EVALUATION_SPEC_INVALID`;
- `FM_STATUS_AGGREGATION_INVALID`;
- `FM_ACTION_SUPPORT_MISSING`;
- `FM_CLAIM_UNSUPPORTED`;
- `FM_CLAIM_SUPPORT_VACUOUS`;
- `FM_LINEAGE_INCOMPLETE`;
- `FM_EVIDENCE_TYPE_COLLAPSED`;
- `FM_POLICY_NOT_INSPECTABLE`;
- `FM_ACTION_UNTYPED`;
- `FM_ACTION_IDENTITY_AMBIGUOUS`;
- `FM_ACTION_SET_QUERY_UNRESOLVED`;
- `FM_BASELINE_MISSING`;
- `FM_BASELINE_SELECTION_UNSUPPORTED`;
- `FM_RULE_NOT_TOTAL`;
- `FM_ROBUST_PERMISSION_VIOLATION`;
- `FM_TRACE_SUPPORT_STALE`;
- `FM_UNSAFE_FALLBACK_ACTION`;
- `FM_CAUSAL_HOLD_INVALID`;
- `FM_CAUSAL_TRACE_MISALIGNED`;
- `FM_INTERVENTION_UNIT_INVALID`;
- `SIM_SYSTEM_STATE_INCOMPLETE`;
- `SIM_EVENT_ORDER_INVALID`;
- `SIM_EVENT_LIVELOCK`;
- `SIM_EVENT_BOUND_EXCEEDED`;
- `FM_REQUIRED_GATE_MISSING`;
- `FM_GATE_FAIL_OPEN`;
- `FM_REVIEW_EVIDENCE_MISSING`;
- `FM_REVIEW_AUTHORITY_MISSING`;
- `FM_REVIEW_LATE`;
- `FM_REVIEW_UNRECORDED`;
- `FM_REVIEW_ACTION_MISMATCH`;
- `FM_REVIEW_VERSION_STALE`;
- `FM_REVIEW_ACTION_NOT_POST_AT_EXECUTION`;
- `FM_REVIEW_ACTION_UNSUPPORTED_AT_EXECUTION`;
- `FM_MATERIALITY_SOURCE_MISSING`;
- `FM_SEMANTIC_CORRESPONDENCE_INVALID`;
- `FM_OPERATIONAL_MATERIALITY_OMISSION`;
- `FM_MATERIAL_ITEM_UNSURFACED`;
- `FM_CONTEST_PATH_UNREACHABLE`;
- `FM_CONTEST_PATH_INFEASIBLE`;
- `FM_CONTEST_RELIABILITY_BELOW_THRESHOLD`;
- `FM_CONTEST_INTERVAL_INCONCLUSIVE`;
- `FM_EVALUATION_HORIZON_PENDING`;
- `FM_RESTORATION_PARTIAL`; and
- `FM_AUTHORITY_STATUS_UNASSESSABLE`.

Every `fail` or `unassessable` assessment references a stored diagnostic containing the property ID, stable code, case and trace references, evidence and process references, action references where applicable, material parameters, expected and observed typed values, owning layer, artifact path, suggested next action, and severity. Every `not_applicable` result references the executable applicability rule plus either a structured false-antecedent record or the frozen excluded scope declaration.

## Observable Trace Mapping

| Property | Passing signal | Failure signal | Primary metric |
| --- | --- | --- | --- |
| F0 | typed claims with complete replayable lineage | unsupported, untyped, relabeled, or noninspectable claim | fidelity failures by reason |
| F1 | every coarse automatic progression instance is independently supported under the certified refinement denotation | validated action/refinement/support-rule witness violates subset | robust-permission violation rate by coverage mode |
| F2 | explicit execute-versus-hold system pair over a valid intervention unit does not newly enable focal or spillover progression outside the envelope at its current pre-state | invalid scope/hold/alignment or paired system traces show newly released unsupported progression | unsafe fallback count by focal/spillover scope |
| F3 | exact action instance is withheld until effective, current authorization, remains in the execution-state post-review set, and remains independently supported | missing/unsafe gate, ineffective review, stale version, action mismatch, lost post-review eligibility, or unsupported execution state | unsupported post-review progression rate |
| F4 | every independently material item has a valid semantic correspondent that reaches an authorized role before progression/expiry | invalid correspondence, operational omission, or no timely semantically corresponding surfacing | unsurfaced-material rate |
| F5 | structural path plus prospective reliability or realized opportunity, and complete restoration when due | below-threshold/inconclusive reliability, unavailable realized path, or residual consequence after horizon | structural, prospective, realized, and restoration rates |
| Gate safety | configured gate blocks until prerequisites | guarded action enabled or executed early | gate-safety failure rate |
| Decision service | supported disposition by service deadline | unresolved, unsupported, or late disposition | timely supported-disposition rate |

## Practical Application Boundary

The formal model supports three application levels defined operationally in `docs/PROCESS_RED_TEAM_PROTOCOL.md`: a Level A document audit, a Level B bounded deterministic trace, and a Level C dynamic system simulation. The selected level limits the conclusions that an assessment may support. In particular, a document audit cannot establish realized review effectiveness or capacity boundaries; a bounded case trace cannot establish outcomes beyond its declared horizon, shared-resource noninterference, or cohort effects without the required system comparison; and simulation results apply only to the declared model and parameter space.

The practitioner output is a profile of property and helper assessments, not a composite compliance score. F0–F5, `GateSafe`, `ReviewEffective`, `DecisionServiceEffective`, and any supporting components retain their own statuses, completeness, diagnostics, inputs, and claim boundaries. No weighted average, traffic-light rollup, or overall workflow pass is part of this formal model. A project that needs such a decision rule must specify, source, freeze, and validate it separately rather than infer it from assessment order or display formatting.

When a property is in or potentially in scope but the selected application level lacks an input required to evaluate it, the evaluator returns `unassessable` with the missing input and required escalation. When the protocol deliberately omits a claim that the selected level cannot support, the practitioner report records `evaluation_state = omitted_by_claim_limit` outside the assessment envelope and creates no property status. It may not approximate a higher-level result from lower-level evidence or convert omission into `not_applicable`.

## Representation-Preservation Fixture Reconciliation

The fixture in `docs/PRECURSOR_FIDELITY_FIXTURE.md` holds the evidence and model output fixed while varying the representation transformation. It therefore tests representation-induced routing and permission, not F1 evidence monotonicity.

Formal classifications are:

- `P0-Preserve` passes F0 when all typed fields retain their declared lineage and remain inspectable.
- `P0-Fallback` can report the defensible raw value `vehicle`, but the fixture deliberately represents it as an `UntypedField`. It therefore cannot pass the typed F0.1 claim-support check and also fails the applicable lineage, state-distinction, and inspectability checks. Those failures do not imply that the raw label is literally false.
- The enabling fallback fails F4 because independently frozen `P0-SIGMA-1` designates the hidden armed-vehicle alternative as material and no authorized role receives it before routine disposition.
- The same-rule semantic null is `not_applicable` for F4 because the valid evaluation materiality record contains no material item affecting its in-scope action; it does not pass vacuously.
- F1 and F2 are `not_applicable` under explicit fixture-level scope exclusions. F3 is `unassessable` where an enhanced disposition exposes a post-review progression path without a completed review or execution, and `not_applicable` where no post-review progression action exists.
- the case-bound P0 routine-action instances qualify as progression relative to `P0-BASE1`: each advances its exact target case to terminal routine disposition and can foreclose the required scrutiny window.
- A safe gate with incomplete reviewer evidence can return `GateSafe(status = pass, value = true)` while `ReviewEffective(status = fail, value = false)`.

The fixture's enabling result is an authored compatibility witness, not a formal theorem, empirical estimate, or prevalence claim.

## Robodebt Instantiation Contract

The document-grounded application may instantiate the formal model as follows:

| Formal object | Robodebt application |
| --- | --- |
| `e_less` | annual employer-income aggregate and broad employment period |
| `e_more` | fortnight-specific income and working-date records |
| `rho(e_less)` | fortnightly values imputed by averaging aggregate income |
| progression actions | debt finalization, recovery initiation, or another source-anchored consequential transition |
| constraint actions | hold, recovery pause, or block pending evidence/review |
| information actions | recipient- or agency-led acquisition of period-specific records |
| restoration actions | reassessment, debt correction, repayment, recovery reversal, or other modeled repair |
| operational materiality map | materiality implemented by the reconstructed workflow policy |
| evaluation specification | independently source-anchored evidentiary distinctions, action-support rules, refinement coverage, and baseline criteria |

This mapping does not itself establish historical legality, monetary correctness, actual service capacity, actual error rates, or complete restoration. Those claim types remain outside scope, separately sourced, or simulated as explicitly declared.

## Base Vulnerability and Adversarial Exploitability

A **base uncertainty-to-permission vulnerability** exists in the declared model when representation or routing causes weaker or less decision-relevant information to remove a safeguard or expand unsupported automatic progression.

**Structural susceptibility** means a prespecified process mutation can reproduce that vulnerability under declared conditions.

**Adversarial exploitability** requires separate evidence of all four:

1. inducibility;
2. observability;
3. repeatability; and
4. benefit.

Neither a failed property check nor successful red-team mutation establishes those four conditions. The Robodebt application does not attribute a strategic actor or historical attack.

## Assumptions and Boundary Conditions

- Evidence comparability is local to declared source and measurement assumptions.
- The refinement set is frozen before action outcomes are inspected; its constructive coverage mode determines which pass or failure conclusions are sound.
- Operational materiality is distinct from independently evaluated materiality.
- Evaluation support, materiality, action comparison, and baseline selection are owned by `sigma`, source-labeled, and independent of preferred workflow results.
- Process state, time, baseline, rule, and policy remain fixed within a formal comparison unless the proposition explicitly varies them.
- Trace-level properties reevaluate support at every material state or version boundary.
- F2 intervention unit, complete initial system state, cohort membership, interventions, causal-event keys, event priorities, and boundary rules are frozen before paired outcomes are inspected; paired system traces align by causal cut rather than event index.
- Event execution has a unique total key and finite horizon, microstep, causal-depth, and event-count bounds; bound failures invalidate a run rather than become favorable censoring.
- Historical formal authority can be `unassessable`; simulation code cannot fill a source gap.
- Safe constraint and information actions remain distinct from progression.
- Review opportunity, gate safety, effective review, and decision service remain distinct.
- F4 semantic correspondence is independently specified and cannot be inferred from display-text similarity or the workflow's own materiality map.
- Finite-window capacity results do not estimate historical capacity.
- Consequence dimensions define the scope of restoration; unmodeled harms cannot be declared restored.
- Prospective, realized-opportunity, correction-uptake, and restoration results remain distinct, and unresolved horizons do not become premature failures.
- Null, adverse, and counterintuitive results remain valid outputs.

## QA Strategy

### Golden cases

- valid and invalid `RecordMeta` envelopes, including stale source versions and a content-hash mismatch;
- complete typed claim versus intentionally representable `UntypedField` consumed by a downstream rule;
- truthful broad label with complete lineage;
- truthful broad label with missing provenance and material alternatives;
- imputed point value correctly typed and inspectable;
- imputed point value relabeled as observed;
- derived claim with contradictory assumptions that would otherwise pass vacuously;
- missing or ambiguous scope declaration returning `unassessable` with `FM_APPLICABILITY_UNDETERMINED` rather than `not_applicable`;
- missing property input returning `unassessable` with `FM_REQUIRED_INPUT_MISSING` while an invalid specification uses `FM_EVALUATION_SPEC_INVALID`;
- conjunctive aggregate containing both `unassessable` and `fail` items returning `fail` with `completeness = incomplete` while retaining both component results;
- contextual failed helper accompanying an incomplete property without entering that property's truth aggregation;
- explicit fixture-level scope exclusion returning `not_applicable` with predicate and fixture-version evidence;
- coarse state with no automatic progression;
- universally permissive workflow with one refinement under which independent support excludes its automatic progression action;
- exact finite and symbolic-exact refinement certificates producing the same F1 result;
- witness-search counterexample that proves failure but cannot prove pass;
- conservative-outer pass and a spurious outer-set failure rejected for lack of an admissible witness;
- action type held constant while a material amount or target changes;
- symbolic action family with a declared downward-closure rule and the same family without that rule;
- safe information-seeking fallback;
- information-labeled fallback that causally releases unsupported progression;
- fallback whose delayed progression is supported initially but unsupported at its later execution state;
- paired F2 system traces with different endogenous event counts that retain identical causal-cut alignment, cohort membership, and keyed exogenous draws;
- focal-case fallback that consumes shared review capacity and releases unsupported timeout progression for another case;
- valid case-local F2 pair with a frozen noninterference certificate and an otherwise identical pair rejected for lacking that certificate;
- same-time event chain that terminates under the transition-rank rule and a zero-time cycle rejected with `SIM_EVENT_LIVELOCK`;
- invalid F2 hold intervention that substitutes another active policy rather than withholding the tested action;
- containment mislabeled as progression and progression mislabeled as containment;
- configured fail-closed gate with late review;
- fail-open timeout with unmet prerequisites;
- safe gate with incomplete reviewer evidence;
- timely complete review;
- valid review followed by execution of a different amount, target, or stale rule version;
- exact reviewed action that becomes independently unsupported before execution;
- exact reviewed action removed from the current `P_post` set before execution;
- operational policy omits an independently material distinction;
- exact-ID and validated-mapping semantic correspondents producing the same F4 result;
- symbolic F4 correspondence whose surfaced semantics directionally entail the required action-relevant meaning;
- reverse-only symbolic implication rejected as an invalid F4 specification;
- broad surfaced text that resembles a material item but lacks valid semantic correspondence;
- exact-ID F4 item with a missing required-meaning record returning `unassessable` rather than pass or fail;
- material warning removed while action-set count stays constant;
- reachable complete restoration;
- structurally contestable case below the prospective reliability threshold;
- realized F5 evaluation before its horizon returning `status = unassessable` with `FM_EVALUATION_HORIZON_PENDING`;
- realized path available but not invoked, reported separately from correction uptake;
- decision correction with residual consequence; and
- representation-preservation fixture enabling, semantic-null, and routing-control pairs.

### Metamorphic checks

- reorder hypotheses, claims, actions, or source records while preserving IDs;
- rename domain display labels;
- replace equivalent time units consistently;
- split or combine equivalent evidence records without changing `Gamma`;
- change selected actions without changing the complete enabled-action set;
- replace an action display label while preserving its canonical comparison fields;
- add irrelevant metadata;
- reorder simultaneous input records under fixed event priority;
- change oracle-only truth without changing pre-oracle behavior;
- replay equivalent finite refinements in a different enumeration order;
- replace exact finite refinements with a provably equivalent symbolic constraint;
- add a causally inert branch-specific event without changing F2 causal-cut results;
- add a causally inert case to a cohort without changing system-level F2 results for existing cases;
- replace an exact-ID F4 correspondent with a validated semantically equivalent mapped item;
- replace a symbolic F4 rule with a logically equivalent forward entailment and proof witness;
- split one trace interval into state-preserving clock events without changing trace-level support; and
- express an equivalent action-support region through reordered symbolic constraints.

### Adversarial mutations

- delete an object or schema version, owner, provenance status, source version, or canonical hash and allow a consumer to default it;
- omit a required claim field while retaining a plausible rendered value;
- define refinement after observing the desired action;
- delete a refinement that supplies a counterexample;
- freeze an incomplete convenience sample while claiming universal refinement coverage;
- claim universal pass from `witness_search` after finding no counterexample;
- treat an inadmissible conservative-outer witness as a conclusive failure;
- derive evaluation support or materiality from the workflow decision rule;
- convert a missing or ambiguous scope declaration into `not_applicable`;
- omit a required input while returning `pass` or `fail`;
- allow `unassessable` to erase a sufficient known failure, treat a contextual helper as a conjunctive condition, discard subordinate results, or accept an unknown item status;
- align divergent F2 traces by event index or queue position;
- claim a system-level F2 pass from a case-local pair without a valid noninterference certificate;
- alter cohort membership, shared queue state, or keyed exogenous draws between intervention arms;
- allow duplicate causal-event keys, an unbounded same-time cycle, or an event-bound breach to appear as ordinary censoring;
- replace `Hold_a` with an outcome-selected active policy;
- retain an action type ID while changing a material parameter under the same instance ID;
- relabel imputed evidence as observed;
- make assumptions contradictory so derived-claim entailment passes vacuously;
- remove lineage while retaining a plausible value;
- infer policy materiality from model output;
- classify a progression action as information-seeking;
- remove reviewer authority while retaining a review label;
- hide evidence from a configured reviewer;
- execute an action instance not authorized by the review or after its evidence/rule version becomes stale;
- carry forward support across a material state boundary without reevaluation;
- authorize the exact action instance but execute it after independent support disappears;
- execute an authorized action after it leaves the current `P_post` set;
- infer F4 correspondence from display-text similarity or the operational materiality map;
- accept reverse implication, satisfiable overlap, or an unexplained ID mapping as F4 semantic correspondence;
- permit timeout progression through a nominally fail-closed gate;
- mark an absent gate as safe;
- infer legal authority from functional permission;
- declare complete restoration from decision correction alone;
- declare a graph-reachable but operationally infeasible correction path contestable;
- fail a realized contestability or restoration component before its frozen horizon;
- change a reliability threshold or interval decision rule after inspecting estimates; and
- allow oracle or expected-result fields to influence routing.

## Fact Ownership

- This document owns the final draft definitions of the versioned stored-record and typed assessment envelopes, truth/completeness semantics and role-bound component aggregation, `>=_E`, constructive refinement modes, `sigma`, the property-scoped scope/antecedent/condition matrix, F0–F5, status diagnostics, action-set denotations, case/system trace-state lifting, total and well-founded event execution, F2 intervention scope and causal-cut alignment, action identity and directions, permission and support sets, gate safety, effective review, review authorization, required meaning and directional semantic correspondence, decision service, contestability modes, and restoration.
- `docs/PRECURSOR_FIDELITY_FIXTURE.md` owns P0 values, transformations, controls, and expected traces, subject to these definitions.
- The future source manifest owns historical and legal facts.
- The future Robodebt case-study document owns the source-anchored formal crosswalk.
- Machine-readable schemas own runtime values after freeze.
- Analysis code owns quantitative estimates and uncertainty intervals.
- Reports render stored artifacts and do not infer formal results from prose.

## Freeze and Change Control

Before this model is frozen:

1. validate the schema manifest and its bidirectional agreement with executable models and stored fixture kinds;
2. implement stored-record metadata, reference closure, source-basis, set/sequence, canonicalization, version, and hash validation;
3. encode finite examples for F0–F5;
4. implement satisfying and failing golden traces;
5. reconcile every P0 classification against this document;
6. complete the action taxonomy, total-disposition schema, action-set representation, membership-query contract, and canonical comparison schema for all modeled policies;
7. source and freeze the evaluation specifications independently of workflow outcomes;
8. freeze admissible refinement generators or symbolic constraints and validate that each coverage mode supports its claimed conclusions;
9. implement property-scoped scope-declaration, antecedent/condition input, replay-complete typed-assessment, truth/completeness, component-relation, and diagnostic-record tests, including stable diagnostics for unknown scope, missing inputs, invalid specifications, sufficient failures, and invalid aggregation;
10. implement event-state capture, total event ordering, well-founded termination bounds, trace-level support reevaluation, complete-system F2 execute/hold interventions, intervention-scope validation, branch-independent causal-cut alignment, and keyed-exogenous invariance tests;
11. implement exact review-to-action binding, execution-state `P_post` membership, execution-state support, and stale-version tests;
12. freeze F5 modes, thresholds, interval rules, and horizons;
13. implement F4 correspondence modes and exact-ID, justified-mapping, forward-entailment, reverse-only, invalid, and ambiguous correspondence tests;
14. cold-read the notation and diagnostics with two readers;
15. record formal-definition and fixture hashes in the freeze manifest; and
16. log every semantic revision and its reason.

After freeze, a change to an evidence order, action classification, materiality rule, property definition, diagnostic status, or proposition assumption is a formal protocol change rather than prose editing.

## Acceptance Criteria

This draft is ready for implementation only when:

- every stored-record schema requires the stable identity/version/ownership/provenance envelope and canonical hash, and every result schema requires the typed assessment envelope;
- every independently identified claim, candidate field, diagnostic, assessment component, rule, and result is a separate `StoredRecord` reached through a versioned `RecordRef`; no partial embedded envelope is accepted;
- schema-family identity is version-free, canonicalization version is explicit, every collection path declares set or sequence semantics, and normalized decimal/time encodings are fixed before hashes are persisted;
- payloads cannot duplicate envelope ownership, provenance, source basis, or source references;
- every executable transformation, routing, applicability, materiality, correspondence, deadline, support, intervention, and nonstandard aggregation record uses a closed implementation ID, version, typed signature, and parameters rather than narrative interpretation;
- every assessment contains replay-complete role-bound input and component bindings, completeness, scope, applicability, false-antecedent, and diagnostic references as its status requires;
- every symbol and comparison has one declared owner;
- information order is independent of downstream permission;
- incomparable states cannot enter F1 checks, refinement coverage is constructive, and each conclusion is permitted by its coverage mode;
- every action instance has canonical material parameters and a baseline-relative authority direction;
- finite and symbolic action sets have equivalent denotational membership semantics, with no inferred closure rule;
- the decision-rule schema and every fixture branch require the complete disposition tuple;
- workflow permission, independent action support, and action selection remain distinct;
- evaluation materiality, required meaning, semantic correspondence, support, baseline selection, and refinement coverage are independently owned and source-labeled;
- formal authority, automatic permission, post-review permission, and execution remain distinct;
- F0 reports its four dimensions before its aggregate status;
- F0 cannot pass derived-claim support through an empty or contradictory assumption intersection;
- F1 emits a validated admissible action/refinement/support-rule witness for every failure, cannot claim universal pass from witness search, and a universally permissive workflow cannot self-certify;
- F2 tests every added fallback using a frozen explicit hold intervention, a complete declared intervention unit, branch-independent causal-cut alignment, identical cohort membership and keyed exogenous inputs, and support reevaluated for every newly enabled action at its do-branch pre-state; a case-local pass cannot support a system-level claim without a frozen noninterference certificate;
- F3 requires effective prior review authorizing the exact current action instance, current execution-state `P_post` membership, and independent support at execution rather than a configured label;
- absent gates, unsafe gates, ineffective review, and failed service remain distinct;
- F4 uses independently evaluated materiality and semantic correspondence, requires forward entailment or a justified mapping, rejects display-text or workflow self-certification, reports operational-policy omissions, and has an aggregate status rule;
- F5 reports structural, prospective, realized-opportunity, uptake, and restoration results separately; applies frozen thresholds and horizons; rejects infeasible correction paths; and cannot report complete restoration with a residual modeled consequence;
- P0 reconciles without turning its fixed-output comparison into F1 evidence;
- Robodebt mappings remain structural rather than numerical or legal inference;
- every property uses a frozen scope-declaration record, phased antecedent/condition contracts, a frozen executable applicability-rule record, stored diagnostic records, declared component relations, and a truth/completeness aggregation rule that never lets an unknown component erase a sufficient known failure; and
- practitioner reports preserve a non-composite assessment profile, declare the application level and claim limits, and escalate rather than manufacture conclusions that require unavailable trace or system inputs; and
- the document can be implemented without consulting the precursor essay or chat history.

Meeting these criteria completes the formal-model specification only. It does not freeze the model, complete Slice 0, execute the simulation, or establish a research result.
