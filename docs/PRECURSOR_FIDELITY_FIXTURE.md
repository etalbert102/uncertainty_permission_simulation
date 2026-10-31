# Representation-Preservation Fixture

Repository ID: `P0-Precursor`

Status: draft Slice 0 specification; not frozen and not yet implemented

Fixture specification version: `draft-0.10`

Reader-facing name: **representation-preservation fixture**

## Purpose

This fixture converts the paper's motivating fixed-output comparison into a deterministic, executable research object. It tests whether changing only the interface-transformation policy applied to one uncertain model output changes routing, scrutiny, review opportunity, or automatic functional permission under a fixed policy map and downstream rule.

The fixture includes three paired comparisons:

1. an **enabling pair**, in which suppressing a policy-relevant alternative changes the workflow outcome;
2. a **same-rule semantic null**, in which neither representation contains a policy-relevant alternative and the enabling rule produces no permission difference; and
3. a **routing-invariance control**, in which a representation-independent safeguard produces the same outcome despite the representation change.

The enabling pair is a compatibility and regression test for the bounded uncertainty-to-permission mechanism. It is not an empirical result. The same-rule null checks the mechanism's necessary policy-relevance condition. The routing-invariance control checks the execution harness. Together, they prevent a successful run from amounting only to an authored permissive route.

## Place in the Research Design

The fixture isolates a narrow causal contrast within the declared hypothetical workflow:

> fixed case, model output, policy map, routing rule, process state, resources, and time -> different interface transformation -> different representation -> routing and permission comparison

The formal model then generalizes this logic to declared evidence refinements and robust automatic permission. The dynamic simulation separately examines how the generalized invariant behaves when evidence availability, administrative access, workload, gates, deadlines, and restoration vary. Those later perturbations must not be described as additional fixed-output tests.

`docs/P0_COLD_READER_PACKET.md` renders only the inputs needed for blinded protocol QA. `docs/P0_USABILITY_WALKTHROUGH.md` contains the withheld expected profile and must not be distributed until a reader locks their report. The walkthrough remains an oracle projection until Slice 1 emits the same non-composite assessment profile from executable stored records; neither artifact adds or changes fixture semantics.

## Layer and Access Contract

The fixture keeps six layers separate:

1. **Model output:** uncertain estimates and alternatives only.
2. **Representation transformation:** selects and types fields exposed downstream.
3. **Policy map:** identifies which visible alternatives trigger which safeguards.
4. **Routing rule:** combines the representation, policy map, and process state.
5. **Action and gate semantics:** determine what may proceed automatically and what must wait.
6. **Oracle validation:** scores latent truth after routing and cannot influence workflow behavior.

Runtime access is allowlisted:

| Stage | May read | Must not read |
| --- | --- | --- |
| Representation transformation | selected model-output record and its own transformation configuration | latent case state, routing outcome, expected trace |
| Policy evaluation | visible representation and fixed policy map | hidden model-output fields, latent case state, expected trace |
| Routing | policy-evaluation output, visible representation, non-oracle case metadata, process state, resources, and clock | latent case state, expected trace |
| Oracle validation | completed trace, latent case state, and expected-output specification | nothing that can alter the completed trace |

Any behavioral access to an oracle-only or expected-result field is a blocking failure.

## Stable Identities

| ID | Object | Role |
| --- | --- | --- |
| `P0-C1` | Core hypothetical tracked-object case | Fixed case for enabling and routing-invariance pairs |
| `P0-C2` | Semantic-null tracked-object case | Fixed case for same-rule null pair |
| `P0-M1` | Core uncertain model output | Contains a policy-relevant alternative but no policy judgment |
| `P0-M2` | Semantic-null model output | Contains no policy-relevant alternative |
| `P0-COMPAT-M1` | Core output compatible-state record | Owns source semantics used by derived-claim checks |
| `P0-COMPAT-M2` | Semantic-null output compatible-state record | Owns source semantics used by derived-claim checks |
| `P0-PROJECTION-M1` | Core output projection-fact set | Establishes direct derivations from `P0-M1` across its compatible states |
| `P0-PROJECTION-M2` | Semantic-null projection-fact set | Establishes direct derivations from `P0-M2` across its compatible states |
| `P0-THETA-M1-ARMED` | Core compatible state | Latent armed-technical state with the exact `P0-M1` source snapshot |
| `P0-THETA-M1-CIVILIAN` | Core compatible state | Latent civilian-pickup state with the exact `P0-M1` source snapshot |
| `P0-THETA-M1-MODIFIED` | Core compatible state | Latent modified-truck state with the exact `P0-M1` source snapshot |
| `P0-THETA-M2-CIVILIAN` | Semantic-null compatible state | Latent civilian-pickup state with the exact `P0-M2` source snapshot |
| `P0-THETA-M2-VAN` | Semantic-null compatible state | Latent delivery-van state with the exact `P0-M2` source snapshot |
| `P0-THETA-M2-MODIFIED` | Semantic-null compatible state | Latent modified-truck state with the exact `P0-M2` source snapshot |
| `P0-Q1-C1` | Pre-routing process state for `P0-C1` | Fixed case-bound process state |
| `P0-Q1-C2` | Pre-routing process state for `P0-C2` | Fixed case-bound process state |
| `P0-RES1` | Resource configuration | Fixed available reviewer and sensor resources |
| `P0-T1` | Clock configuration | Fixed open observation and decision window |
| `P0-BASE1` | Declared hypothetical policy baseline | Requires scrutiny before routine disposition when a material alternative is visible |
| `P0-Preserve` | Uncertainty-preserving representation transformation | Experimental transformation |
| `P0-Fallback` | Broad fallback representation transformation | Experimental transformation |
| `P0-R-M1-PRESERVE` | Stored `P0-M1` preserving representation | Generated representation record |
| `P0-R-M1-FALLBACK` | Stored `P0-M1` fallback representation | Generated representation record |
| `P0-R-M2-PRESERVE` | Stored `P0-M2` preserving representation | Generated representation record |
| `P0-R-M2-FALLBACK` | Stored `P0-M2` fallback representation | Generated representation record |
| `P0-TAXONOMY-1` | Fixed object-class taxonomy | Owns the defensibility relation between alternatives and `vehicle` |
| `P0-POLICY-1` | Materiality and safeguard policy map | Fixed organizational policy judgment |
| `P0-SIGMA-1` | Independent evaluation specification | Owns fixture evaluation rules and property scope |
| `P0-APPLICABILITY-1` | Property scope and applicability specification | Owns P0 F0–F5 and helper scope declarations and predicates |
| `P0-SCOPE-F0` | F0 scope declaration | Includes rendered representations |
| `P0-SCOPE-F1` | F1 scope declaration | Excludes evidence-refinement comparison from P0 |
| `P0-SCOPE-F2` | F2 scope declaration | Excludes evidence-refinement fallback comparison from P0 |
| `P0-SCOPE-F3` | F3 scope declaration | Conditions evaluation on a post-review progression action |
| `P0-SCOPE-F4` | F4 scope declaration | Conditions evaluation on an applicable material item and action |
| `P0-SCOPE-F5` | F5 scope declaration | Records undetermined obligation scope |
| `P0-SCOPE-GATE-SAFE` | GateSafe helper scope declaration | Conditions evaluation on a configured gate |
| `P0-SCOPE-REVIEW-EFFECTIVE` | ReviewEffective helper scope declaration | Conditions evaluation on a required or configured prior-review path |
| `P0-SCOPE-DECISION-SERVICE` | DecisionServiceEffective helper scope declaration | Includes bounded traces but requires a service horizon and supported disposition |
| `P0-APP-F0` | F0 applicability rule | Constant true for a rendered P0 representation |
| `P0-APP-F3` | F3 applicability rule | Tests the post-review action set |
| `P0-APP-F4` | F4 applicability rule | Tests material-item applicability to the output/action pair |
| `P0-APP-GATE-SAFE` | GateSafe applicability rule | Tests whether a gate is configured |
| `P0-APP-REVIEW-EFFECTIVE` | ReviewEffective applicability rule | Tests whether prior review is required or configured |
| `P0-APP-DECISION-SERVICE` | DecisionServiceEffective applicability rule | Constant true for a rendered P0 bounded trace |
| `P0-CORRESPOND-F4` | F4 correspondence rule | Applies exact semantic-ID and field correspondence |
| `P0-DEADLINE-F4` | F4 surfacing-deadline rule | Requires surfacing before routing completes at `T0` |
| `P0-ACTION-COMPARE-1` | Action-comparison schema | Owns behaviorally material action fields |
| `P0-MATERIAL-ARMED-TECHNICAL-1` | Evaluation-material item | Identifies the live armed-technical alternative when present |
| `P0-RM-ARMED-TECHNICAL-ROUTINE-1` | Required-meaning record | Defines what must be surfaced before routine disposition |
| `P0-D-ENABLE` | Representation-sensitive routing rule | Produces the hypothesized contrast when all necessary conditions hold |
| `P0-D-CONTROL` | Representation-independent safeguard rule | Produces the routing-invariance control |
| `P0-A-INFO-C1` | Retask sensor or obtain additional observation for `P0-C1` | Information action |
| `P0-A-REVIEW-C1` | Conduct authorized review for `P0-C1` before routine disposition | Review action and dependency |
| `P0-A-ROUTINE-C1` | Finalize `P0-C1` without enhanced scrutiny | Progression action relative to `P0-BASE1` |
| `P0-A-ROUTINE-C2` | Finalize `P0-C2` without enhanced scrutiny | Progression action relative to `P0-BASE1` |

Implementations must use these IDs rather than matching display text such as “technical,” “vehicle,” or “routine.”

### Stored-record metadata

Every fixed object, transformation, generated representation, rule, and expected-result record uses the `RecordMeta` and `StoredRecord` contract in `docs/FORMAL_MODEL.md`. In this draft:

- each object in the stable-identity table has `object_version = 1` unless a table explicitly overrides it;
- every schema used by the fixture has `schema_version = 1`;
- every record uses `(canonicalization_id = UPS-CANONICAL-JSON, canonicalization_version = 1)`;
- `stable_representation_id` maps `(P0-M1, P0-Preserve)`, `(P0-M1, P0-Fallback)`, `(P0-M2, P0-Preserve)`, and `(P0-M2, P0-Fallback)` to the canonical string IDs `P0-R-M1-PRESERVE`, `P0-R-M1-FALLBACK`, `P0-R-M2-PRESERVE`, and `P0-R-M2-FALLBACK`; each has `object_version = 1`;
- fixture-authored records have `provenance_status = hypothetical`, transformed claims and representations have `provenance_status = derived`, and expected results have `provenance_status = hypothetical`;
- case and model-output records are owned by `P0-FIXTURE-OWNER-1`; compatible-state, state, and projection-fact records by `P0-EVIDENCE-OWNER-1`; transformations and generated field/representation records by `P0-TRANSFORM-OWNER-1`; taxonomy and action records by `P0-SEMANTICS-OWNER-1`; process/resource/clock records by `P0-PROCESS-OWNER-1`; the operational policy by `P0-POLICY-OWNER-1`; routing rules by `P0-ROUTING-OWNER-1`; evaluation, applicability, materiality, required-meaning, and scope records by `P0-EVAL-OWNER-1`; executed traces, events, and state snapshots by `P0-SIMULATOR-OWNER-1`; actual assessments and diagnostics by `P0-EVALUATOR-OWNER-1`; and trace specifications and expected results by `P0-QA-OWNER-1`; and
- every source reference contains the referenced object's ID and version.

Schema identity is fixed by object kind:

| Object kind | Schema ID |
| --- | --- |
| case and model output | `P0-SCHEMA-CASE`; `P0-SCHEMA-MODEL-OUTPUT` |
| compatible state, state, and projection facts | `P0-SCHEMA-COMPATIBLE-STATE`; `P0-SCHEMA-STATE`; `P0-SCHEMA-PROJECTION-FACT-SET` |
| process, resource, clock, and baseline | `P0-SCHEMA-PROCESS`; `P0-SCHEMA-RESOURCE`; `P0-SCHEMA-CLOCK`; `P0-SCHEMA-BASELINE` |
| executable transformation, routing, and applicability rules | `P0-SCHEMA-EXECUTABLE-RULE` |
| taxonomy | `P0-SCHEMA-TAXONOMY` |
| policy and evaluation specification | `P0-SCHEMA-POLICY`; `P0-SCHEMA-EVALUATION` |
| applicability specification, scope declaration, and action comparison | `P0-SCHEMA-APPLICABILITY`; `P0-SCHEMA-SCOPE-DECLARATION`; `P0-SCHEMA-ACTION-COMPARISON` |
| material item and required meaning | `P0-SCHEMA-MATERIAL-ITEM`; `P0-SCHEMA-REQUIRED-MEANING` |
| action | `P0-SCHEMA-ACTION` |
| disposition, state snapshot, event, and review decision | `formal_model.disposition`; `formal_model.pre_state`; `formal_model.post_state`; `event`; `formal_model.review_decision` |
| non-record rule result | `formal_model.boolean_predicate` |
| preserved and fallback representation | `P0-SCHEMA-PRESERVE`; `P0-SCHEMA-FALLBACK` |
| typed claim and untyped field | `P0-SCHEMA-CLAIM`; `P0-SCHEMA-UNTYPED-FIELD` |
| trace specification and executed trace | `P0-SCHEMA-TRACE-SPEC`; `P0-SCHEMA-TRACE` |
| expected result, assessment, diagnostic, and false antecedent | `P0-SCHEMA-EXPECTED-RESULT`; `P0-SCHEMA-ASSESSMENT`; `P0-SCHEMA-DIAGNOSTIC`; `P0-SCHEMA-FALSE-ANTECEDENT` |

Synthetic root records use `source_basis = synthetic_no_external_source`, the explicit empty list `source_refs = []`, and `provenance_status = hypothetical`. Derived records use `source_basis = versioned_sources` and reference their exact versioned fixture inputs. The machine-readable fixture materializes every metadata field; none is a runtime default. Payloads do not repeat envelope owner, provenance, or source fields. A changed payload increments that object's version, while a changed field shape increments its schema version and, when it changes the stored payload, the object version. The stored `content_hash` follows the global canonicalization contract and is not included in its own hash input.

## Fixed Cases

Both cases are synthetic and hypothetical. They do not require images. If placeholder payloads are implemented, they must be structured synthetic records rather than purported operational artifacts.

### Core case: `P0-C1`

A low-resolution sensor observes a pale object moving on a road under atmospheric distortion. The latent case state is an armed technical. That state is oracle-only and is not available to transformations, policy evaluation, or routing.

### Semantic-null case: `P0-C2`

The non-oracle case metadata is identical to `P0-C1`. The latent case state is a civilian pickup and remains oracle-only. Its paired model output contains no alternative designated material by `P0-POLICY-1`.

### Case fields

| Field | `P0-C1` | `P0-C2` | Visibility |
| --- | --- | --- | --- |
| `case_id` | `P0-C1` | `P0-C2` | All fixture stages |
| `case_kind` | `synthetic_hypothetical_track` | `synthetic_hypothetical_track` | All fixture stages |
| `latent_object_type` | `armed_technical` | `civilian_pickup` | Oracle validation only |
| `sensor_resolution_px` | `[12, 18]` | `[12, 18]` | Non-oracle case metadata |
| `atmospheric_distortion` | `true` | `true` | Non-oracle case metadata |
| `road_track` | `true` | `true` | Non-oracle case metadata |
| `low_resolution_track` | `true` | `true` | Non-oracle case metadata |
| `historical_or_operational_source` | `none` | `none` | Validation metadata |

Changing a latent state within a primary pair is prohibited. A separate oracle-leak probe changes only the oracle field across a cloned case and must leave transformation, policy evaluation, routing, and permission outputs unchanged.

## Fixed Model Outputs

Model-output records contain no policy-relevance field or safeguard instruction.

### Core output: `P0-M1`

| Field | Fixed value |
| --- | --- |
| `model_output_id` | `P0-M1` |
| `primary_estimate_id` | `pickup_like_silhouette` |
| `primary_confidence_decimal` | `"0.42"` |
| `broad_class_id` | `vehicle` |
| `fallback_threshold_decimal` | `"0.6"` |
| `alternative_ids` | `armed_technical`, `civilian_pickup`, `modified_truck` |
| `alternative_probabilities` | `not_provided` |
| `source_type` | `synthetic_model_output` |

### Semantic-null output: `P0-M2`

`P0-M2` is identical in structure and numeric values to `P0-M1`, but its alternatives are `civilian_pickup`, `delivery_van`, and `modified_truck`. None is designated material by `P0-POLICY-1`.

The fixture must not invent probabilities for alternatives. The `0.42` value attaches only to the pickup-like primary estimate. Both representations in a pair derive from one stored output; neither branch may call a model, modify the output, or recompute the estimate.

`P0-COMPAT-M1` and `P0-COMPAT-M2` use `denotation_mode = finite_exact`. Their payloads are fully fixed:

| Compatible-state set | `evidence_ref` | `state_refs` | `projection_fact_set_ref` | `taxonomy_ref` |
| --- | --- | --- | --- | --- |
| `P0-COMPAT-M1` | `(P0-M1, 1)` | `(P0-THETA-M1-ARMED, 1)`, `(P0-THETA-M1-CIVILIAN, 1)`, `(P0-THETA-M1-MODIFIED, 1)` | `(P0-PROJECTION-M1, 1)` | `(P0-TAXONOMY-1, 1)` |
| `P0-COMPAT-M2` | `(P0-M2, 1)` | `(P0-THETA-M2-CIVILIAN, 1)`, `(P0-THETA-M2-VAN, 1)`, `(P0-THETA-M2-MODIFIED, 1)` | `(P0-PROJECTION-M2, 1)` | `(P0-TAXONOMY-1, 1)` |

Each state record has payload `(state_id, evidence_ref, latent_object_type_id)`. The `P0-M1` state payloads use `armed_technical`, `civilian_pickup`, and `modified_truck`; the `P0-M2` state payloads use `civilian_pickup`, `delivery_van`, and `modified_truck`, in the same order as the IDs above. State records use `meta.source_refs = [evidence_ref, (P0-TAXONOMY-1, 1)]` and `provenance_status = hypothetical`; the compatible-state and projection records use those state and evidence records as their versioned sources.

The projection-fact sets contain these typed facts; `true_in_state_refs` is the complete `state_refs` set for that row's output:

| Fact-set ID | Source field path | Relation | Typed value |
| --- | --- | --- | --- |
| `P0-PROJECTION-M1` | `/broad_class_id` | `equals` | ID `vehicle` |
| `P0-PROJECTION-M1` | `/primary_estimate_id` | `equals` | ID `pickup_like_silhouette` |
| `P0-PROJECTION-M1` | `/primary_confidence_decimal` | `equals` | decimal string `"0.42"` |
| `P0-PROJECTION-M1` | `/fallback_threshold_decimal` | `equals` | decimal string `"0.6"` |
| `P0-PROJECTION-M1` | `/alternative_ids` | `contains_all` | ID set `armed_technical`, `civilian_pickup`, `modified_truck` |
| `P0-PROJECTION-M2` | `/broad_class_id` | `equals` | ID `vehicle` |
| `P0-PROJECTION-M2` | `/primary_estimate_id` | `equals` | ID `pickup_like_silhouette` |
| `P0-PROJECTION-M2` | `/primary_confidence_decimal` | `equals` | decimal string `"0.42"` |
| `P0-PROJECTION-M2` | `/fallback_threshold_decimal` | `equals` | decimal string `"0.6"` |
| `P0-PROJECTION-M2` | `/alternative_ids` | `contains_all` | ID set `civilian_pickup`, `delivery_van`, `modified_truck` |

The transformation rule defines an `alternative_ids` member as a live unresolved classification alternative; that rule, rather than latent truth, supports the alternative claims and `alternatives_status = unresolved`. A direct projection uses `assumption_refs = []`, explicitly denoting no additional assumptions and the universal assumption state. These exact records allow F0 to test derived-claim entailment rather than accepting a prose assertion that compatible states exist.

### Taxonomy: `P0-TAXONOMY-1`

The fixed taxonomy maps `armed_technical`, `civilian_pickup`, `delivery_van`, `modified_truck`, and `pickup_like_silhouette` to the broad class `vehicle`. Fixture validation uses this record to establish that the fallback label is compatible with every listed alternative. The taxonomy is not a policy-materiality map and cannot trigger routing.

## Fixed Process, Resource, Clock, and Baseline Records

### Process states: `P0-Q1-C1` and `P0-Q1-C2`

| Field | `P0-Q1-C1` | `P0-Q1-C2` |
| --- | --- | --- |
| `process_state_id` | `P0-Q1-C1` | `P0-Q1-C2` |
| `case_ref` | `(P0-C1, 1)` | `(P0-C2, 1)` |
| `stage` | `pre_routing` | `pre_routing` |
| `current_route` | `unassigned` | `unassigned` |
| `prior_escalation` | `false` | `false` |
| `active_review_gate` | `false` | `false` |
| `emergency_authorization` | `false` | `false` |

### Resources: `P0-RES1`

| Field | Fixed value |
| --- | --- |
| `resource_config_id` | `P0-RES1` |
| `reviewer_role_id` | `P0-ROLE-REVIEWER` |
| `reviewer_available` | `true` |
| `reviewer_stopping_authority` | `true` |
| `additional_sensor_available` | `true` |
| `queue_state` | `nominal` |

### Clock: `P0-T1`

| Field | Fixed value |
| --- | --- |
| `clock_config_id` | `P0-T1` |
| `decision_time` | `T0` |
| `observation_window` | `open` |
| `review_deadline` | `open` |

No stochastic draws are permitted in `P0`; `random_draw_count` must equal zero. Queue load, service time, deadline pressure, actor behavior, and emergency rules do not vary. They belong to the dynamic simulation.

### Declared baseline: `P0-BASE1`

`P0-BASE1` is a hypothetical evaluation baseline, not a claim about an actual operation. `P0-SIGMA-1` selects it independently for formal classification.

| Field | Fixed value |
| --- | --- |
| `baseline_id` | `P0-BASE1` |
| `trigger_rule_ref` | `(P0-APP-F4, 1)` |
| `required_action_refs_when_triggered` | `(P0-A-INFO-C1, 1)`, `(P0-A-REVIEW-C1, 1)` |
| `blocked_action_refs_until_review` | `(P0-A-ROUTINE-C1, 1)` |
| `final_action_refs` | `(P0-A-ROUTINE-C1, 1)`, `(P0-A-ROUTINE-C2, 1)` |

Thus, when the stored model output contains an alternative designated material by the evaluation specification, the baseline preserves the alternative for downstream inspection, obtains additional information, and completes authorized review before finalizing routine disposition.

## Action and Gate Semantics

| Instance ID | Type ID | Actor-role ID | Target ID | Resource/commitment ID | Consequence ID | Reversibility ID | Authorization requirement / source-rule ref | Authority-direction class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `P0-A-INFO-C1` | `P0-A-TYPE-INFO` | `P0-ROLE-WORKFLOW` | `P0-C1` | `P0-COMMIT-ADDITIONAL-SENSOR` | `P0-CONSEQUENCE-ADDITIONAL-EVIDENCE` | `P0-REV-CANCEL-BEFORE-EXECUTION` | `P0-AUTH-POLICY`; `(P0-POLICY-1, 1)` | `information` |
| `P0-A-REVIEW-C1` | `P0-A-TYPE-REVIEW` | `P0-ROLE-REVIEWER` | `P0-C1` | `P0-COMMIT-REVIEWER-TIME-STOPPING` | `P0-CONSEQUENCE-CONSTRAIN-ROUTINE` | `P0-REV-WHILE-OBSERVATION-OPEN` | `P0-AUTH-POLICY`; `(P0-POLICY-1, 1)` | `constraint` |
| `P0-A-ROUTINE-C1` | `P0-A-TYPE-ROUTINE` | `P0-ROLE-WORKFLOW` | `P0-C1` | `P0-COMMIT-CLOSE-SCRUTINY-WINDOW` | `P0-CONSEQUENCE-TERMINAL-ROUTINE` | `P0-REV-WHILE-OBSERVATION-OPEN` | `P0-AUTH-POLICY`; `(P0-POLICY-1, 1)` | `progression` relative to `(P0-BASE1, 1)` |
| `P0-A-ROUTINE-C2` | `P0-A-TYPE-ROUTINE` | `P0-ROLE-WORKFLOW` | `P0-C2` | `P0-COMMIT-CLOSE-SCRUTINY-WINDOW` | `P0-CONSEQUENCE-TERMINAL-ROUTINE` | `P0-REV-WHILE-OBSERVATION-OPEN` | `P0-AUTH-POLICY`; `(P0-POLICY-1, 1)` | `progression` relative to `(P0-BASE1, 1)` |

Each row is a fully instantiated action instance. Its omitted `parameter_vector` is `MappingValue(kind = mapping, entries = {})`; each semantic token in the material columns is an `IDValue`; and its `source_rule_refs` contains the versioned ref in the Authorization column. The stable resource/commitment, consequence, reversibility, and authorization tokens—not the following explanatory labels—enter action identity and hashes. `P0-COMMIT-ADDITIONAL-SENSOR` means one additional sensor task; `P0-CONSEQUENCE-ADDITIONAL-EVIDENCE` means evidence acquisition without final disposition; `P0-COMMIT-REVIEWER-TIME-STOPPING` means reviewer time with stopping authority; `P0-CONSEQUENCE-CONSTRAIN-ROUTINE` means routine progression is constrained pending a recorded decision; `P0-COMMIT-CLOSE-SCRUTINY-WINDOW` and `P0-CONSEQUENCE-TERMINAL-ROUTINE` mean the enhanced-scrutiny opportunity closes as the case advances to terminal routine disposition; and the two reversibility tokens have their literal timing meanings.

`P0-ACTION-COMPARE-1` has `material_field_names = [actor_role_id, target_id, parameter_vector, resource_commitment, operational_or_external_consequence, reversibility_window, authorization_requirement, source_rule_refs, authority_direction]` with `set_semantics` on the field-name list and on each action's `source_rule_refs`. Any change to one of those fields requires a new instance ID even if the type ID is unchanged.

`P0-A-ROUTINE-C1` and `P0-A-ROUTINE-C2` do not claim authority over a physical object. They are case-specific workflow dispositions that advance the organization's case and can foreclose the opportunity for enhanced scrutiny. Under the criteria in `docs/FORMAL_MODEL.md`, each qualifies as progression relative to `P0-BASE1` because it advances its exact target case to terminal routine disposition, commits the workflow to no additional safeguard before the observation window can close, and requires a new action to recover the lost scrutiny opportunity.

A fail-closed review gate blocks `P0-A-ROUTINE-C1` until `P0-A-REVIEW-C1` completes. Gate configuration, gate safety, evidence completeness, stopping authority, enforced dependency, review completion, and effective review are recorded separately. P0 does not configure a review path for `P0-C2`.

## Closed Executable-Rule Bindings

P0 uses the `ExecutableRule` contract in `docs/FORMAL_MODEL.md`. The following implementation IDs form a closed Slice 1 enum; they are study-specific functions, not dynamic plugins. Every parameter is a typed literal or `RecordRef`, and each implementation rejects unknown parameters.

| Rule ID | Kind | Implementation ID/version | Typed parameters | Output schema |
| --- | --- | --- | --- | --- |
| `P0-Preserve` | `transformation` | `p0_preserve_projection` / `1` | source bindings `model_output:/broad_class_id`, `model_output:/primary_estimate_id`, `model_output:/primary_confidence_decimal`, `model_output:/fallback_threshold_decimal`, `model_output:/alternative_ids`; projection map `P0-M1 -> (P0-PROJECTION-M1, 1)`, `P0-M2 -> (P0-PROJECTION-M2, 1)`; alternative semantic type `classification_alternative`; polarity `live`; uncertainty status `unresolved` | `P0-SCHEMA-PRESERVE`, version 1 |
| `P0-Fallback` | `transformation` | `p0_threshold_broad_fallback` / `1` | confidence binding `model_output:/primary_confidence_decimal`; threshold binding `model_output:/fallback_threshold_decimal`; comparator `less_than`; output path `/broad_class_id` | `P0-SCHEMA-FALLBACK`, version 1 |
| `P0-D-ENABLE` | `routing` | `p0_visible_material_route` / `1` | policy ref `(P0-POLICY-1, 1)`; broad-class ID `vehicle`; action map `P0-C1 -> [(P0-A-INFO-C1, 1), (P0-A-REVIEW-C1, 1), (P0-A-ROUTINE-C1, 1)]`, `P0-C2 -> [(P0-A-ROUTINE-C2, 1)]`; constructor enum values `enhanced`, `routine`, `unassessable` | `formal_model.disposition`, version 1 |
| `P0-D-CONTROL` | `routing` | `p0_low_resolution_control_route` / `1` | case-field binding `case:/low_resolution_track`; action map `P0-C1 -> [(P0-A-INFO-C1, 1), (P0-A-REVIEW-C1, 1), (P0-A-ROUTINE-C1, 1)]`; constructor enum values `enhanced`, `routine`, `unassessable` | `formal_model.disposition`, version 1 |
| `P0-APP-F0` | `applicability` | `constant_true` / `1` | none | `formal_model.boolean_predicate`, version 1 |
| `P0-APP-F3` | `applicability` | `any_action_direction_in_disposition_set` / `1` | set binding `disposition:/post_review_action_refs`; required direction `progression` | `formal_model.boolean_predicate`, version 1 |
| `P0-APP-F4` | `applicability` | `material_item_applies_to_output_action` / `1` | material-item ref `(P0-MATERIAL-ARMED-TECHNICAL-1, 1)`; output binding `model_output:/alternative_ids`; required ID `armed_technical`; affected action ref `(P0-A-ROUTINE-C1, 1)` | `formal_model.boolean_predicate`, version 1 |
| `P0-APP-GATE-SAFE` | `applicability` | `boolean_input_is_true` / `1` | input field binding `state:/gate_configured` | `formal_model.boolean_predicate`, version 1 |
| `P0-APP-REVIEW-EFFECTIVE` | `applicability` | `any_boolean_input_is_true` / `1` | input field bindings `state:/gate_required`, `state:/gate_configured` | `formal_model.boolean_predicate`, version 1 |
| `P0-APP-DECISION-SERVICE` | `applicability` | `constant_true` / `1` | none | `formal_model.boolean_predicate`, version 1 |
| `P0-CORRESPOND-F4` | `correspondence` | `exact_semantic_fields` / `1` | compared fields `semantic_id`, `semantic_type`, `semantic_scope_ref`, `polarity`, `uncertainty_status`; required-meaning ref `(P0-RM-ARMED-TECHNICAL-ROUTINE-1, 1)` | `formal_model.boolean_predicate`, version 1 |
| `P0-DEADLINE-F4` | `deadline` | `event_strictly_before_boundary` / `1` | surfaced-event type `REPRESENTATION_SURFACED`; boundary-event type `ROUTING_COMPLETED`; clock ref `(P0-T1, 1)`; boundary instant ID `T0` | `formal_model.boolean_predicate`, version 1 |

The machine-readable records contain the table's tokens and references, not its explanatory prose. The implementation signature table in `schemas.py` owns allowed parameter names and kinds; the rule records own their fixed values. Changing an implementation's behavior increments its implementation version and the enclosing rule object version.

The rules' `input_role_specs` are also fixed. Both transformations bind `model_output`; `P0-D-ENABLE` binds `representation`, `policy`, `process_state`, and `clock`; `P0-D-CONTROL` binds `representation`, `case`, `process_state`, and `clock`; `P0-APP-F0` and `P0-APP-DECISION-SERVICE` bind `representation`; `P0-APP-F3` binds `disposition` and cardinality-many `actions`; `P0-APP-F4` binds `model_output`, `material_item`, and `affected_action`; the gate and review helper-applicability rules bind `state` to the applicable `GateState`, while the helper conditions separately bind `ReviewState` where required; `P0-CORRESPOND-F4` binds `surfaced_claim`, `material_item`, and `required_meaning`; and `P0-DEADLINE-F4` binds cardinality-many `events` and one `clock`. Each role declares its accepted schema references and cardinality, and each output schema must match the closed implementation signature. No implicit input role or schema is permitted.

## Representation Transformations

Both transformations are deterministic functions of a stored model-output record. They cannot read the case, latent truth, policy map, routing rule, process state, resources, clock, or expected result.

### `P0-Preserve`

```text
rho_preserve(model_output_record):
    model_ref = ref(model_output_record)
    transform_ref = (P0-Preserve, 1)
    compatible_ref = compatible_ref(model_ref)
    projection_ref = projection_ref(model_ref)

    derived(field_name, value, semantic = null):
        claim_id = stable_claim_id(
            model_ref.object_id, P0-Preserve, field_name, value
        )
        claim_payload = {
            field_kind: claim,
            claim_id: claim_id,
            field_name: field_name,
            value: value,
            evidence_type: derived,
            transformation_ref: transform_ref,
            assumption_refs: [],
            compatible_state_ref: compatible_ref,
            visibility: [policy_evaluator, router, reviewer],
            semantic_id: semantic.id if semantic else null,
            semantic_type: semantic.type if semantic else null,
            semantic_scope_ref: semantic.scope_ref if semantic else null,
            polarity: semantic.polarity if semantic else null,
            uncertainty_status: semantic.uncertainty_status if semantic else null
        }
        claim_meta = derived_meta(
            object_id = claim_id,
            schema_id = P0-SCHEMA-CLAIM,
            owner_id = P0-TRANSFORM-OWNER-1,
            source_refs = [
                model_ref, transform_ref, compatible_ref, projection_ref
            ]
        )
        return ref(Store(claim_meta, claim_payload))

    field_refs = [
        derived("broad_class", model_output_record.payload.broad_class_id),
        derived("primary_estimate", model_output_record.payload.primary_estimate_id),
        derived("primary_confidence_decimal", model_output_record.payload.primary_confidence_decimal),
        derived("fallback_threshold_decimal", model_output_record.payload.fallback_threshold_decimal),
        derived("alternatives_status", unresolved)
    ]
    field_refs += [
        derived(
            "alternative",
            alternative_id,
            semantic = {
                id: alternative_id,
                type: classification_alternative,
                scope_ref: model_ref,
                polarity: live,
                uncertainty_status: unresolved
            }
        ) for alternative_id in sorted(model_output_record.payload.alternative_ids)
    ]

    representation_id = stable_representation_id(
        model_ref.object_id, P0-Preserve
    )
    representation_payload = {
        representation_id: representation_id,
        field_refs: field_refs,
        provenance_visible: true
    }
    representation_meta = derived_meta(
        object_id = representation_id,
        schema_id = P0-SCHEMA-PRESERVE,
        owner_id = P0-TRANSFORM-OWNER-1,
        source_refs = [model_ref, transform_ref] + field_refs
    )
    return Store(representation_meta, representation_payload)
```

### `P0-Fallback`

```text
rho_fallback(model_output_record):
    model_ref = ref(model_output_record)
    transform_ref = (P0-Fallback, 1)
    require decimal(model_output_record.payload.primary_confidence_decimal)
            < decimal(model_output_record.payload.fallback_threshold_decimal)

    field_id = stable_field_id(
        model_ref.object_id, P0-Fallback, "object_class"
    )
    field_payload = {
        field_kind: untyped,
        field_id: field_id,
        field_name: object_class,
        value: model_output_record.payload.broad_class_id,
        visibility: [policy_evaluator, router, reviewer]
    }
    field_meta = derived_meta(
        object_id = field_id,
        schema_id = P0-SCHEMA-UNTYPED-FIELD,
        owner_id = P0-TRANSFORM-OWNER-1,
        source_refs = [model_ref, transform_ref]
    )
    field_ref = ref(Store(field_meta, field_payload))

    representation_id = stable_representation_id(
        model_ref.object_id, P0-Fallback
    )
    representation_payload = {
        representation_id: representation_id,
        field_refs: [field_ref],
        provenance_visible: false
    }
    representation_meta = derived_meta(
        object_id = representation_id,
        schema_id = P0-SCHEMA-FALLBACK,
        owner_id = P0-TRANSFORM-OWNER-1,
        source_refs = [model_ref, transform_ref, field_ref]
    )
    return Store(representation_meta, representation_payload)
```

`Store` requires complete `RecordMeta`, validates the payload, applies the global canonicalization profile, computes `content_hash`, persists the record, and returns it. `derived_meta` supplies `object_version = 1`, `schema_version = 1`, `canonicalization_id = UPS-CANONICAL-JSON`, `canonicalization_version = 1`, `provenance_status = derived`, and `source_basis = versioned_sources`; it has no defaults outside this fixture constructor. `ref` returns only `(object_id, object_version)`.

The fallback `object_class` is deliberately an `UntypedField`, not a malformed stored artifact. This permits routing to consume its value while F0 diagnoses the missing evidence type and lineage. The fallback label remains defensible: `P0-TAXONOMY-1` places every alternative in both model outputs under the declared broad class `vehicle`. The failure is not literal falsity or targeted misclassification. The transformation removes confidence, alternatives, typing, and downstream-inspectable provenance.

### Treatment contract

Within each pair, only the transformation ID, transformation configuration, and representation mechanically produced by that transformation may differ. The case, model output, taxonomy, operational policy map, independent evaluation specification, routing rule, process state, resources, clock, baseline, and absence of random draws must match.

## Fixed Policy Map

`P0-POLICY-1` is an organizational policy record, not part of either model output.

| Field | Fixed value |
| --- | --- |
| `policy_map_id` | `P0-POLICY-1` |
| `material_alternative_ids` | `armed_technical` |
| `materiality_reason_id` | `armed_vehicle_requires_added_scrutiny` |
| `required_information_action_refs` | `(P0-A-INFO-C1, 1)` |
| `required_review_action_refs` | `(P0-A-REVIEW-C1, 1)` |
| `blocked_until_review_action_refs` | `(P0-A-ROUTINE-C1, 1)` |
| `authorized_action_refs` | `(P0-A-INFO-C1, 1)`, `(P0-A-REVIEW-C1, 1)`, `(P0-A-ROUTINE-C1, 1)`, `(P0-A-ROUTINE-C2, 1)` |
| `confidence_alone_is_material` | `false` |

Policy evaluation resolves every `field_ref`, selects records whose payload has `field_kind = claim`, `field_name = alternative`, and policy-evaluator visibility, extracts their typed `value`, or returns an empty set when none exist, and intersects those IDs with `material_alternative_ids`. The broad-class branch resolves the unique visible field whose `field_name` is `broad_class` or `object_class` and may consume either a `Claim` or the deliberately valid `UntypedField`. Policy evaluation emits `visible_material_alternative_ids` and a routing reason; it does not alter the representation, borrow envelope provenance as claim support, or infer that hidden alternatives are absent.

## Fixed Independent Evaluation Specification

`P0-SIGMA-1` is a hypothetical fixture evaluation record, separate from `P0-POLICY-1` and never consumed by `P0-D-ENABLE` or `P0-D-CONTROL`. It is frozen before paired routing outcomes are evaluated.

| Field | Fixed value |
| --- | --- |
| `evaluation_spec_id` | `P0-SIGMA-1` |
| `evaluation_basis` | `hypothetical_fixture`, not historical or legal |
| `material_alternative_ids` | `armed_technical` |
| `materiality_reason_id` | `armed_vehicle_requires_added_scrutiny` |
| `baseline_selection_ref` | `(P0-BASE1, 1)` |
| `action_comparison_schema_ref` | `(P0-ACTION-COMPARE-1, 1)` |
| `action_set_representation_mode` | `finite_explicit` |
| `applicability_spec_ref` | `(P0-APPLICABILITY-1, 1)` |
| `scope_declaration_refs` | `(P0-SCOPE-F0, 1)`, `(P0-SCOPE-F1, 1)`, `(P0-SCOPE-F2, 1)`, `(P0-SCOPE-F3, 1)`, `(P0-SCOPE-F4, 1)`, `(P0-SCOPE-F5, 1)`, `(P0-SCOPE-GATE-SAFE, 1)`, `(P0-SCOPE-REVIEW-EFFECTIVE, 1)`, `(P0-SCOPE-DECISION-SERVICE, 1)` |
| `semantic_correspondence_mode` | `exact_id` |
| `required_meaning_refs` | `(P0-RM-ARMED-TECHNICAL-ROUTINE-1, 1)` |
| `semantic_correspondence_rule_ref` | `(P0-CORRESPOND-F4, 1)` |
| `required_intervention_capabilities` | enum set `stop`, `delay`, `modify` |
| `required_intervention_action_ref` | `(P0-A-ROUTINE-C1, 1)` |
| `surfacing_deadline_rule_ref` | `(P0-DEADLINE-F4, 1)` |
| `f5_undetermined_field_ids` | `contestability_obligation_scope`, `restoration_obligation_scope`, `applicable_action_scope`, `path_refs`, `horizon_refs`, `consequence_dimension_refs`, `baseline_refs` |

The evaluation-material record is:

| Field | Fixed value |
| --- | --- |
| `material_item_id` | `P0-MATERIAL-ARMED-TECHNICAL-1` |
| `semantic_id` | `armed_technical` |
| `semantic_type` | `classification_alternative` |
| `semantic_scope_binding` | enum `input_model_output_ref` |
| `polarity` | `live` |
| `uncertainty_status` | `unresolved` |
| `applicability_rule_ref` | `(P0-APP-F4, 1)` |
| `affected_action_refs` | `(P0-A-ROUTINE-C1, 1)` |
| `evaluation_basis` | `hypothetical_fixture` |

The required-meaning record is:

| Field | Fixed value |
| --- | --- |
| `required_meaning_id` | `P0-RM-ARMED-TECHNICAL-ROUTINE-1` |
| `material_item_ref` | `(P0-MATERIAL-ARMED-TECHNICAL-1, 1)` |
| `material_semantic_id` | `armed_technical` |
| `affected_action_ref` | `(P0-A-ROUTINE-C1, 1)` |
| `evidence_scope_rule_ref` | `(P0-APP-F4, 1)` |
| `process_state_ref` | `(P0-Q1-C1, 1)` |
| `clock_ref` | `(P0-T1, 1)` |
| `required_semantic_type` | `classification_alternative` |
| `required_semantic_scope_binding` | enum `input_model_output_ref` |
| `required_polarity` | `live` |
| `required_uncertainty_status` | `unresolved` |
| `relevance_action_refs` | `(P0-A-INFO-C1, 1)`, `(P0-A-REVIEW-C1, 1)`, `(P0-A-ROUTINE-C1, 1)` |
| `required_intervention_capabilities` | enum set `stop`, `delay`, `modify` |
| `surfacing_deadline_rule_ref` | `(P0-DEADLINE-F4, 1)` |
| `evaluation_basis` | `hypothetical_fixture` |

`P0-MATERIAL-ARMED-TECHNICAL-1` is applicable only when the current stored model output contains `armed_technical` as a live alternative. It therefore applies to `P0-M1` and not `P0-M2`. Actual reviewer assignment, stopping authority, availability, and event timing come from `P0-RES1`, the case-bound `P0-Q1-C1` or `P0-Q1-C2` process state, and `P0-T1`; `P0-SIGMA-1` specifies the required capability and deadline but does not invent that operational fact.

The evaluation specification independently establishes the fixture's F4 materiality, exact-ID semantic correspondence, and baseline-relative action classification. Its agreement with the operational policy's materiality list is an authored control, not self-certification: routing reads only `P0-POLICY-1`, while formal evaluation reads `P0-SIGMA-1`. Display-text similarity does not satisfy correspondence. P0 deliberately does not declare whether an in-scope action carries an F5 obligation; missing scope facts therefore make F5 `unassessable` with `FM_APPLICABILITY_UNDETERMINED`. The fixture does not assert the false antecedent needed for `not_applicable`, and absence of a modeled path is not treated as an assessable F5 failure. Changing either object requires its own version and hash.

### Property applicability for P0

`P0-APPLICABILITY-1` contains the ordered set of the following versioned scope-declaration references. Each referenced payload is fixed before any trace result is inspected:

| Scope ID | Property | Evaluation-unit kind | Mode | Applicability-rule ref | Exclusion reason or undetermined fields |
| --- | --- | --- | --- | --- | --- |
| `P0-SCOPE-F0` | F0 | rendered representation | `included` | `(P0-APP-F0, 1)` | none |
| `P0-SCOPE-F1` | F1 | evidence-refinement comparison | `excluded` | null | `P0_NO_EVIDENCE_REFINEMENT_COMPARISON` |
| `P0-SCOPE-F2` | F2 | evidence-refinement fallback comparison | `excluded` | null | `P0_NO_EVIDENCE_REFINEMENT_FALLBACK_COMPARISON` |
| `P0-SCOPE-F3` | F3 | disposition trace | `included_conditional` | `(P0-APP-F3, 1)` | none |
| `P0-SCOPE-F4` | F4 | output/action pair | `included_conditional` | `(P0-APP-F4, 1)` | none |
| `P0-SCOPE-F5` | F5 | consequential action obligation | `undetermined` | null | `contestability_obligation_scope`, `restoration_obligation_scope`, `applicable_action_scope` |

When `P0-APP-F3` or `P0-APP-F4` evaluates false, the evaluator stores a `FalseAntecedent` record with deterministic ID `P0-FA-{trace_id}-{property_id}`, the rule ref, role-bound evaluation inputs, and typed observed value. The resulting `not_applicable` assessment references that record. F1 and F2 instead reference their excluded scope declarations; F5 references `P0-SCOPE-F5` and the diagnostic for its named undetermined fields.

Helper assessments use the same mechanism:

| Scope ID | Helper | Evaluation-unit kind | Mode | Applicability-rule ref |
| --- | --- | --- | --- | --- |
| `P0-SCOPE-GATE-SAFE` | `GateSafe` | trace gate state | `included_conditional` | `(P0-APP-GATE-SAFE, 1)` |
| `P0-SCOPE-REVIEW-EFFECTIVE` | `ReviewEffective` | trace review state | `included_conditional` | `(P0-APP-REVIEW-EFFECTIVE, 1)` |
| `P0-SCOPE-DECISION-SERVICE` | `DecisionServiceEffective` | bounded trace | `included` | `(P0-APP-DECISION-SERVICE, 1)` |

False helper antecedents use the same deterministic `FalseAntecedent` constructor with the helper ID in place of the property ID.

## Total Downstream Rules

Every rule branch emits the complete disposition required by `D(r, pi, q, t)`. The fixture uses three total constructors:

```text
EnhancedDisposition(case_id, declared_reason, review_evidence_complete):
    require case_id == P0-C1
    route = enhanced_scrutiny
    routing_reasons = [declared_reason]
    automatic_action_refs = [(P0-A-INFO-C1, 1), (P0-A-REVIEW-C1, 1)]
    post_review_action_refs = [(P0-A-ROUTINE-C1, 1)]
    selected_action_refs = [(P0-A-INFO-C1, 1), (P0-A-REVIEW-C1, 1)]
    constraint_action_refs = [(P0-A-REVIEW-C1, 1)]
    information_action_refs = [(P0-A-INFO-C1, 1)]
    restoration_action_refs = []
    gate_requirements = [{
        guarded_action_ref: (P0-A-ROUTINE-C1, 1),
        prerequisite_action_ref: (P0-A-REVIEW-C1, 1),
        semantics: fail_closed
    }]
    review_evidence_complete = supplied argument

RoutineDisposition(case_id, declared_reason):
    route = routine
    routing_reasons = [declared_reason]
    automatic_action_refs = [routine_action_ref(case_id)]
    post_review_action_refs = []
    selected_action_refs = [routine_action_ref(case_id)]
    constraint_action_refs = []
    information_action_refs = []
    restoration_action_refs = []
    gate_requirements = []
    review_evidence_complete = false

UnassessableDisposition(case_id, declared_reason):
    route = unassessable
    routing_reasons = [declared_reason]
    automatic_action_refs = []
    post_review_action_refs = []
    selected_action_refs = []
    constraint_action_refs = []
    information_action_refs = []
    restoration_action_refs = []
    gate_requirements = []
    review_evidence_complete = false
```

`routine_action_ref(P0-C1) = (P0-A-ROUTINE-C1, 1)` and `routine_action_ref(P0-C2) = (P0-A-ROUTINE-C2, 1)`; every other input is invalid. The constructors return complete disposition payloads. The routing wrapper assigns deterministic ID `P0-DISPOSITION-{trace_specification_id}`, stores the payload under `(schema_id = formal_model.disposition, schema_version = 1)`, and sets envelope source refs to the trace specification, representation, policy, routing rule, process, clock, and every referenced action. `P0-A-REVIEW-C1` appearing in `automatic_action_refs` means that the workflow can automatically enable and queue the review operation; it does not mean the human review completes automatically. `P0-A-ROUTINE-C1` appears in `post_review_action_refs` only while the fail-closed review path is configured. An unknown or malformed input returns `UnassessableDisposition` with no enabled or selected action.

### Enabling rule: `P0-D-ENABLE`

Apply exactly the same rule to `P0-Preserve` and `P0-Fallback`:

```text
visible_material_ids = intersect(
    visible_claim_values(representation.field_refs, "alternative"),
    P0-POLICY-1.material_alternative_ids
)

if visible_material_ids is not empty:
    return EnhancedDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = visible_material_alternative,
        review_evidence_complete = true
    )
else if visible_field_value(
    representation.field_refs, ["broad_class", "object_class"]
) == vehicle:
    return RoutineDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = no_visible_material_alternative
    )
else:
    return UnassessableDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = malformed_or_unknown_representation
    )
```

The rule intentionally treats “no visible material alternative” as sufficient for routine disposition. It must not record or imply that no material alternative exists in the hidden model output. That authored interface-routing coupling is the vulnerability being represented, not evidence of its prevalence.

### Routing-invariance rule: `P0-D-CONTROL`

Apply exactly the same rule to `P0-Preserve` and `P0-Fallback`:

```text
if non_oracle_case.low_resolution_track == true:
    return EnhancedDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = low_resolution_track,
        review_evidence_complete =
            visible_claim_values(
                representation.field_refs, "alternative"
            ) is not empty
            and representation.provenance_visible == true
    )
else if non_oracle_case.low_resolution_track == false:
    return RoutineDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = adequate_resolution_track
    )
else:
    return UnassessableDisposition(
        case_id = process_state.case_ref.object_id,
        declared_reason = missing_resolution_status
    )
```

This rule checks that the harness can preserve safeguards and permissions across representation changes. Because fallback review lacks the hidden alternatives and provenance, it does not establish effective review even though the gate remains safe.

## Required Traces

| Trace-specification ID | Case/output | Transformation | Rule | Expected route | Information action | Gate | `P_auto_progress` contains its case-bound routine action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P0-E-PRESERVE` | `P0-C1` / `P0-M1` | `P0-Preserve` | `P0-D-ENABLE` | `enhanced_scrutiny` | yes | fail closed | no |
| `P0-E-FALLBACK` | `P0-C1` / `P0-M1` | `P0-Fallback` | `P0-D-ENABLE` | `routine` | no | absent | yes |
| `P0-S-PRESERVE` | `P0-C2` / `P0-M2` | `P0-Preserve` | `P0-D-ENABLE` | `routine` | no | absent | yes |
| `P0-S-FALLBACK` | `P0-C2` / `P0-M2` | `P0-Fallback` | `P0-D-ENABLE` | `routine` | no | absent | yes |
| `P0-N-PRESERVE` | `P0-C1` / `P0-M1` | `P0-Preserve` | `P0-D-CONTROL` | `enhanced_scrutiny` | yes | fail closed | no |
| `P0-N-FALLBACK` | `P0-C1` / `P0-M1` | `P0-Fallback` | `P0-D-CONTROL` | `enhanced_scrutiny` | yes | fail closed | no |

The enabling comparison is `P0-E-PRESERVE` versus `P0-E-FALLBACK`. The same-rule semantic null is `P0-S-PRESERVE` versus `P0-S-FALLBACK`. The routing-invariance control is `P0-N-PRESERVE` versus `P0-N-FALLBACK`.

Each trace-specification record has `object_version = 1`, `schema_id = P0-SCHEMA-TRACE-SPEC`, `schema_version = 1`, owner `P0-QA-OWNER-1`, and versioned source refs to every case/output/transformation/rule and held input named by its row.

## Observable Outputs and Review Classification

Every trace must emit:

- trace, pair, case, output, transformation, policy-map, evaluation-specification, rule, process, resource, clock, and baseline IDs;
- complete `PreState` and `PostState` records and hashes for every event;
- component hashes and the paired `held_bundle_hash`;
- `random_draw_count`;
- visible alternatives, confidence, typing, and provenance fields;
- `visible_material_alternative_ids`;
- route and routing reason;
- complete automatic, post-review, selected, constraint, information, and restoration action-instance sets;
- referenced `GateState` records owning gate requirement, configuration, semantics, and prerequisite facts;
- referenced `ReviewState` records owning reviewer availability, authority, evidence completeness, dependency, and completion facts;
- `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective` assessment envelopes, including status, optional boolean value, and diagnostic reasons;
- automatic progression action-instance IDs;
- formal-property classifications and diagnostic reasons; and
- applicability, role-bound inputs, component relation, truth status, completeness, and aggregate records; and
- fixture-specification and implementation versions.

Expected review classifications are:

| Trace | Gate required | Gate configured | `GateSafe` status/value | Evidence complete | Completion modeled | `ReviewEffective` status/value | `DecisionServiceEffective` status/value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P0-E-PRESERVE` | `true` | `true` | `pass` / `true` | `true` | no | `unassessable` / none | `unassessable` / none |
| `P0-E-FALLBACK` | `true` | `false` | `not_applicable` / none | `false` | no gate | `fail` / `false` | `unassessable` / none |
| `P0-S-PRESERVE` | `false` | `false` | `not_applicable` / none | not routed to review | no gate | `not_applicable` / none | `unassessable` / none |
| `P0-S-FALLBACK` | `false` | `false` | `not_applicable` / none | not routed to review | no gate | `not_applicable` / none | `unassessable` / none |
| `P0-N-PRESERVE` | `true` | `true` | `pass` / `true` | `true` | no | `unassessable` / none | `unassessable` / none |
| `P0-N-FALLBACK` | `true` | `true` | `pass` / `true` | `false` | no | `fail` / `false` | `unassessable` / none |

`GateSafe` is `not_applicable` when no gate is configured. The enabling fallback's `gate_required = true` and `gate_configured = false` record the missing safeguard without pretending that a configured gate failed. A `ReviewEffective` assessment with `status = fail, value = false` is appropriate when a necessary condition is definitively absent. `status = unassessable` with no boolean value is reserved for a potentially valid review path whose completion is not modeled. `DecisionServiceEffective` is `unassessable/incomplete` on all six bounded traces with `FM_REQUIRED_INPUT_MISSING` because P0 declares the helper in scope but supplies neither a service deadline nor a supported final disposition by that deadline.

### Expected-result and actual-assessment records

Each ID in the Required Traces table is a stored `TraceSpecification` record, not the executed trace artifact. An expected-result record has deterministic ID `P0-EXPECTED-{trace_spec_id}`, references the trace specification and all frozen fixture inputs, and contains expected disposition fields plus `ExpectedAssessmentSpec` entries:

```text
ExpectedDispositionSpec = (
    route,
    routing_reasons,
    automatic_action_refs,
    post_review_action_refs,
    selected_action_refs,
    constraint_action_refs,
    information_action_refs,
    restoration_action_refs,
    gate_requirements,
    review_evidence_complete
)

ExpectedAssessmentSpec = (
    property_or_helper_id,
    expected_status,
    expected_completeness,
    expected_value: AssessmentValue | null,
    required_diagnostic_codes,
    scope_declaration_ref,
    applicability_rule_ref,
    false_antecedent_required
)
```

These are closed expected-value schemas, not arbitrary JSON. The expected result is an oracle-only comparison record, not an `Assessment` and not a behavioral input. The executed trace receives deterministic ID `P0-TRACE-{trace_spec_id}` and `object_version = 1`. Actual assessments use ID `P0-ASSESS-{executed_trace_id}-{property_or_helper_id}`, reference the executed trace as `evaluation_unit_ref`, and materialize the complete `Assessment` contract from `docs/FORMAL_MODEL.md`. Diagnostics use ID `P0-DIAG-{assessment_id}-{diagnostic_code}`. Expected records may be frozen before execution because they reference trace specifications, not future outputs.

The expected formal-property entries are therefore fully determined per trace. Every `pass`, `fail`, and `not_applicable` entry below has `completeness = complete`. F3 entries shown as `unassessable` have `completeness = incomplete` because execution and completed review are not modeled; F5 entries also have `completeness = incomplete` because a valid `undetermined` scope declaration names the still-missing obligation-scope fields.

| Trace specification | F0 | F1 | F2 | F3 | F4 | F5 |
| --- | --- | --- | --- | --- | --- | --- |
| `P0-E-PRESERVE` | `pass` | `not_applicable` | `not_applicable` | `unassessable` | `pass` | `unassessable` |
| `P0-E-FALLBACK` | `fail` | `not_applicable` | `not_applicable` | `not_applicable` | `fail` | `unassessable` |
| `P0-S-PRESERVE` | `pass` | `not_applicable` | `not_applicable` | `not_applicable` | `not_applicable` | `unassessable` |
| `P0-S-FALLBACK` | `fail` | `not_applicable` | `not_applicable` | `not_applicable` | `not_applicable` | `unassessable` |
| `P0-N-PRESERVE` | `pass` | `not_applicable` | `not_applicable` | `unassessable` | `pass` | `unassessable` |
| `P0-N-FALLBACK` | `fail` | `not_applicable` | `not_applicable` | `unassessable` | `fail` | `unassessable` |

Required diagnostic-code sets are exact: fallback F0 failures require `FM_EVIDENCE_TYPE_COLLAPSED`, `FM_LINEAGE_INCOMPLETE`, and `FM_POLICY_NOT_INSPECTABLE`; applicable F3 paths without a completed review require `FM_REVIEW_UNRECORDED`, with `P0-N-FALLBACK` also retaining contextual `FM_REVIEW_EVIDENCE_MISSING`; failing F4 entries require `FM_MATERIAL_ITEM_UNSURFACED`; every F5 entry requires `FM_APPLICABILITY_UNDETERMINED`; and every `DecisionServiceEffective` entry requires `FM_REQUIRED_INPUT_MISSING`. F1/F2 exclusions and false F3/F4 antecedents use no failure diagnostic: they reference the excluded scope declaration or generated false-antecedent record. Passing assessments have no diagnostics. The failed `ReviewEffective` helper for `P0-N-FALLBACK` is a `contextual` component of the incomplete F3 assessment, not a completed F3 item and therefore not a conjunctive failure witness.

For helper results, `GateSafe` passes have no diagnostics; its `not_applicable` entries require a false-antecedent record from `P0-APP-GATE-SAFE`. `ReviewEffective` unassessable entries require `FM_REVIEW_UNRECORDED`; the enabling fallback requires `FM_REQUIRED_GATE_MISSING` and `FM_REVIEW_EVIDENCE_MISSING`; the routing-control fallback requires `FM_REVIEW_EVIDENCE_MISSING`; and semantic-null `not_applicable` entries require a false-antecedent record from `P0-APP-REVIEW-EFFECTIVE`.

Every actual assessment's `evaluation_input_bindings` binds named roles to the executed trace, trace specification, case, model output, transformation, representation, policy, routing rule, process, resource, clock, baseline, evaluation specification, applicability specification, scope declaration, and applicability rule when present. F0 additionally binds every field, compatible-state, projection-fact, and taxonomy ref; F3 binds disposition, gate state, review state or decision, and actions; F4 binds material item, required meaning, correspondence rule, deadline rule, role, and action; F5 binds the scope declaration and available actions even though its obligation scope is undetermined. Gate and review helper assessments bind the disposition plus their gate or review-state records; decision-service assessments bind the disposition, clock, and missing service-deadline role. Role cardinality is validated before hashing, so these bindings form a replay contract rather than an unordered version map.

## Expected Comparisons

### Enabling pair

The pair passes only when all held hashes match, transformation and representation hashes differ, the preserved representation exposes the material alternative, and the fallback does not. The route must change from enhanced scrutiny to routine disposition; the information action and prior-review dependency must disappear; and `P0-A-ROUTINE-C1` must become automatically permitted only in the fallback branch.

### Same-rule semantic null

The pair passes only when all held hashes match, transformation and representation hashes differ, neither representation exposes an alternative designated material by `P0-POLICY-1`, and both branches retain identical routine routing and permission under `P0-D-ENABLE`.

### Routing-invariance control

The pair passes only when all held hashes match, transformation and representation hashes differ, and both branches retain enhanced scrutiny, the information action, the fail-closed gate, and exclusion of `P0-A-ROUTINE-C1` from automatic progression. The fallback branch must still record incomplete review evidence and ineffective review.

## Formal-Property Mapping

| Property | Enabling pair | Semantic null | Routing-invariance control | Interpretation |
| --- | --- | --- | --- | --- |
| F0 evidentiary fidelity | preserve `pass`; fallback `fail` | preserve `pass`; fallback `fail` | preserve `pass`; fallback `fail` | Fallback labels remain defensible but omit downstream-inspectable typing, transformation, assumptions, and provenance. |
| F1 robust automatic permission | `not_applicable` | `not_applicable` | `not_applicable` | `P0-APPLICABILITY-1` explicitly excludes evidence-refinement comparison; every pair holds its evidence and model output fixed. |
| F2 safe fallback allowance | `not_applicable` | `not_applicable` | `not_applicable` | The fixture identifies `P0-A-INFO-C1` as an information action but does not vary evidence states. |
| F3 review-preserved progression | preserve `unassessable`; fallback `not_applicable` | both `not_applicable` | preserve and fallback `unassessable` | Enhanced dispositions place the case-bound routine action in `post_review_action_refs`, but no completed review or execution is modeled. The control fallback retains its known review-evidence failure beneath the `unassessable` aggregate. Routine dispositions contain no post-review progression action. |
| F4 surfacing preservation | preserve `pass`; fallback `fail` | both `not_applicable` | preserve `pass`; fallback `fail` | The required meaning is present and timely only in the preserved `P0-M1` representation. `P0-M2` contains no applicable evaluation-material item. |
| F5 contestability and restoration | `unassessable` | `unassessable` | `unassessable` | `P0-SIGMA-1` does not declare F5 obligation scope or required path, horizon, consequence, and baseline inputs; applicability is therefore undetermined with `FM_APPLICABILITY_UNDETERMINED`, not false or failed. |

No F1–F3 pass or failure may be claimed from `P0`. F1 and F2 are explicitly outside fixture scope. F3 is `unassessable` where a post-review progression path exists but review completion and execution are absent, and `not_applicable` otherwise. The fixture checks compatibility with the later formal generalization rather than supplying substantive F1–F3 evidence.

Under `docs/FORMAL_MODEL.md`, the fallback's defensible broad value is an `UntypedField`, so it cannot pass typed claim support and also fails the applicable lineage, state-distinction, and inspectability checks. The aggregate F0 failure must retain those dimension-level reasons and must not describe the raw label as literally false.

## Deterministic Hash Contract

Use `(canonicalization_id = UPS-CANONICAL-JSON, canonicalization_version = 1)` exactly as defined in `docs/FORMAL_MODEL.md`. P0 schemas mark only these paths with `set_semantics`: every `meta.source_refs`; model-output `alternative_ids`; taxonomy member sets; visibility-role sets; representation `field_refs`; policy material, information, review, blocked-action, and authorized-action refs; compatible-state `state_refs`; projection-fact `true_in_state_refs`; evaluation-specification reference sets and capability sets; disposition automatic, post-review, selected, constraint, information, and restoration action refs; assessment component bindings, diagnostic refs, and evaluation-input bindings; and expected required-diagnostic-code sets. Event sequences, causal paths, routing-reason precedence, and ordered diagnostic presentation preserve array order. No serializer may guess set behavior from an `_ids` or `_refs` suffix.

Each component hash covers its complete metadata and payload, committing object/schema/canonicalization versions, owner, provenance status, source basis, and versioned source references. The stored `content_hash` field is excluded from its own hash input. Display labels never enter behavioral hashes.

For each pair, record:

```text
non_oracle_case_hash = H(non-oracle case fields)
oracle_hash           = H(oracle-only case fields)
model_output_hash     = H(model-output record)
process_state_hash    = H(case-bound process-state record)
resource_config_hash  = H(P0-RES1)
clock_config_hash     = H(P0-T1)
baseline_hash         = H(P0-BASE1)
taxonomy_hash         = H(P0-TAXONOMY-1)
policy_map_hash       = H(P0-POLICY-1)
evaluation_spec_hash  = H(P0-SIGMA-1)
routing_rule_hash     = H(rule ID, version, and total structured rule)
transform_hash        = H(transformation ID, version, and total structured transformation)
representation_hash   = H(rendered structured representation)

held_bundle_hash = H(
    non_oracle_case_hash,
    oracle_hash,
    model_output_hash,
    process_state_hash,
    resource_config_hash,
    clock_config_hash,
    baseline_hash,
    taxonomy_hash,
    policy_map_hash,
    evaluation_spec_hash,
    routing_rule_hash,
    fixture_spec_version,
    random_draw_count
)
```

Within a pair, all components of `held_bundle_hash` must match. Only `transform_hash` and `representation_hash` may differ before policy evaluation and routing. Enabling and routing-control rule hashes must differ. The semantic-null pair must share the enabling-rule hash. `random_draw_count` must equal zero in every trace. Deterministic replay must reproduce every hash and observable output.

The oracle-leak probe changes `oracle_hash` in a cloned case while holding the non-oracle input projection fixed. It is evaluated as a metamorphic comparison, not as a primary pair with equal held hashes.

## QA and Mutation Checks

### Golden assertions

1. All six traces match the required trace table exactly.
2. The enabling pair changes routing and permission while every held hash matches.
3. The semantic null produces no routing or permission change under the enabling rule.
4. The routing-invariance control preserves safeguards and permission across transformations while correctly detecting incomplete fallback review evidence.
5. Neither fallback is classified as a false prediction merely because it reports `vehicle`.
6. No trace reports historical, legal, operational, prevalence, or attackability claims.
7. Every F5 output is `unassessable` with `FM_APPLICABILITY_UNDETERMINED`; none is inferred as `not_applicable` or `fail` from the missing correction model.
8. Every stored fixture object validates its ID, object version, schema ID/version, owner, provenance status, source references, and canonical content hash.
9. Every `P0-Preserve` field required by F0 is a complete typed claim; every `P0-Fallback` broad label remains explicitly represented as an `UntypedField`.
10. Every routing branch emits a complete formal disposition, including all enabled, post-review, selected, constraint, information, restoration, and gate-requirement sets.
11. F4 exact-ID cases use `P0-RM-ARMED-TECHNICAL-ROUTINE-1`; a missing surfaced correspondent fails with `FM_MATERIAL_ITEM_UNSURFACED`, while the semantic-null traces are `not_applicable` rather than passing vacuously.
12. All six `DecisionServiceEffective` assessments are `unassessable/incomplete` with `FM_REQUIRED_INPUT_MISSING`; no trace silently converts the missing service deadline into a claim-limit omission, pass, failure, or non-applicability result.

### Metamorphic checks

- Reorder unranked alternative IDs while preserving IDs; outputs must remain unchanged.
- Change display labels while preserving IDs; outputs must remain unchanged.
- Reorder serialized fields; canonical hashes and outputs must remain unchanged.
- Add irrelevant display metadata; routing and permission must remain unchanged.
- Replay traces in a different execution order; per-trace outputs must remain unchanged.
- Change only an oracle-only latent state in the oracle-leak probe; every pre-validation output must remain unchanged.
- Replace the display phrase for routine disposition while retaining the case-bound routine-action IDs; action classification must remain unchanged.
- Replace display text for `armed_technical` while retaining its stable ID; F4 correspondence must remain unchanged.

### Adversarial implementation mutations

- Add a policy-relevance field to a model output; schema validation must fail.
- Delete or silently default an object ID, object/schema version, owner, provenance status, source version, or content hash; stored-record validation must fail.
- Remove a required claim field from `P0-Preserve` or relabel the fallback `UntypedField` as a conforming typed claim; the F0 regression must fail.
- Let a transformation read the policy map, routing outcome, latent state, or expected trace; the access-contract gate must fail.
- Let routing read hidden model-output fields or latent truth; the access-contract or oracle-leak gate must fail.
- Change confidence, alternatives, process state, resources, clock, baseline, taxonomy, policy map, or rule in only one paired branch; validation must fail with the mismatched component ID.
- Allow display-text matching to control routing; the label-renaming metamorphic test must fail.
- Allow display-text similarity or `P0-POLICY-1` to establish F4 semantic correspondence; the independent-correspondence gate must fail.
- Remove the required-meaning record, change the semantic scope, or substitute `value` equality for stable semantic identity; F4 must become `unassessable` with `FM_SEMANTIC_CORRESPONDENCE_INVALID` rather than retain the expected pass/fail.
- Treat a missing visible warning or alternative as evidence that no hidden material alternative exists; diagnostics must identify the unsupported inference.
- Report a configured gate as effective review without complete evidence and a completed authorized review event; the review-classification gate must fail.
- Make either null/control result differ across transformations; the corresponding null gate must fail.
- Consume a random draw; deterministic-fixture validation must fail.
- Emit a partial decision-rule disposition; totality validation must fail.

### Diagnostic standard

Every failure reports a stable code, pair and trace IDs, owning layer, mismatched component or failed property, expected and observed values, artifact path, suggested next action, and blocking severity.

Minimum diagnostic codes are:

- `P0_LAYER_ACCESS_VIOLATION`;
- `P0_MODEL_POLICY_CONTAMINATION`;
- `P0_HELD_INPUT_MISMATCH`;
- `P0_TRANSFORM_DERIVATION_FAILURE`;
- `P0_RULE_MISMATCH`;
- `P0_RULE_NOT_TOTAL`;
- `P0_EXPECTED_CONTRAST_MISSING`;
- `P0_SEMANTIC_NULL_CHANGED`;
- `P0_ROUTING_CONTROL_CHANGED`;
- `P0_ORACLE_LEAK`;
- `P0_TEXT_IDENTITY_LEAK`;
- `P0_SEMANTIC_CORRESPONDENCE_INVALID`;
- `P0_REVIEW_OVERCLAIM`;
- `P0_RANDOMNESS_USED`; and
- `P0_NONDETERMINISTIC_REPLAY`.

## Manuscript Rendering

The manuscript should describe the fixture from first principles and omit `P0-Precursor`:

> Consider a hypothetical operations center receiving the same uncertain estimate through two interfaces: a pickup-like silhouette at 42 percent confidence with an armed-vehicle alternative, or only the defensible fallback label “vehicle.” A fixed policy map requires added observation and review when that alternative is visible. Holding the case, output, policy, rule, and process state constant, the preserving interface triggers those safeguards while the fallback permits routine disposition. In a same-rule null case with no policy-relevant alternative, both interfaces permit the same disposition; a separate harness control routes every low-resolution track to review. The comparison therefore isolates a representation effect under declared rules without treating the authored result as empirical prevalence.

This paragraph is an explanatory rendering, not a report of empirical findings. Numerical or implementation results may replace it only after the executable fixture passes and the claim language remains bounded.

## Attackability and Claim Boundaries

The fixture may support only the following claim:

> Within the declared hypothetical workflow, suppressing a policy-relevant alternative while holding the case, model output, taxonomy, policy map, process state, resources, time, and routing rule fixed changes scrutiny and automatic functional permission under the enabling rule.

It does not establish:

- that a deployed system uses this rule;
- the prevalence, frequency, probability, or magnitude of the vulnerability;
- that the hypothetical object, sensor, model, interface, or workflow represents an actual operation;
- that the route is lawful, unlawful, safe, unsafe, correct, or incorrect in a real setting;
- **Inducibility:** that a strategic actor can induce the ambiguity;
- **Observability:** that an actor can observe the routing response;
- **Repeatability:** that the condition is repeatable in practice;
- **Benefit:** that exploitation would benefit an actor;
- that historical adversarial exploitation occurred;
- that Robodebt is equivalent to the defense vignette; or
- that the dynamic simulation numerically estimates this vignette.

Inducibility, observability, repeatability, and benefit remain separate claim-boundary fields. They are not parameters or expected outputs of `P0`.

## Fact Ownership

- This document owns fixture IDs, fixed values, access rules, transformation semantics, the taxonomy, operational policy map, independent evaluation specification, routing semantics, expected traces, and acceptance conditions until frozen machine-readable specifications supersede it.
- The precursor essay owns the motivating conceptual comparison but is not an executable source of runtime values.
- `docs/FORMAL_MODEL.md` owns the draft F0–F5 definitions, authority classes, and the criteria under which routine disposition qualifies as progression.
- Machine-readable fixture records will own runtime values after freeze; code must consume those records rather than re-derive facts from prose.
- Simulation code consumes stable IDs and structured fields; it must not infer behavior from display labels.
- Generated reports render stored trace artifacts and may not re-derive expected results from narrative text.

Any conflict between this draft and the later formal specification must be resolved explicitly in the claim-boundary memo before implementation is accepted.

## Freeze and Change Control

Before the fixture is frozen:

1. reconcile action classification and F0–F5 mappings with `docs/FORMAL_MODEL.md`;
2. validate `data/model/schema_manifest_v1.yaml` and its bidirectional agreement with schema models and P0 fixture kinds;
3. have two cold readers identify every held, varied, oracle-only, and prohibited field using packet-only copies of `docs/P0_COLD_READER_PACKET.md`, without consulting the precursor essay, this formal fixture, the usability walkthrough, or expected outputs;
4. confirm that readers can distinguish the same-rule semantic null from the routing-invariance control;
5. convert fixed records, transformations, the taxonomy, operational policy map, independent evaluation specification, total rules, and expected outputs to machine-readable fixtures;
6. run the reference-closure, canonicalization, oracle-leak, label-renaming, semantic-correspondence, rule-totality, and no-randomness gates;
7. record canonical hashes and fixture version in the freeze manifest; and
8. log every semantic revision and its reason.

After freeze, display wording may be clarified, but no held field, transformation, policy map, rule, expected comparison, property classification, or acceptance condition may change in response to simulation results without a declared protocol deviation.

## Acceptance Criteria

This draft is ready for implementation only when:

- `data/model/schema_manifest_v1.yaml` contains every P0 payload kind, reference edge, closed rule signature, and set/sequence declaration used here, and validates as YAML;
- every P0 fixed value, compatible-state denotation, rule parameter, scope declaration, expected assessment, and diagnostic expectation can be transcribed without interpreting narrative prose;
- model output, transformation, taxonomy, operational policy, evaluation specification, routing, action, review, and oracle layers have separate owners and schemas;
- every fixed and varied object has a stable ID and version;
- claims, untyped fields, diagnostics, and assessment components are stored separately and reached only through versioned references; partial embedded envelopes and duplicated payload provenance are rejected;
- every stored object validates the shared metadata envelope and canonical content hash;
- all branches within each pair share every held-bundle component;
- only transformation and representation hashes differ before routing;
- the enabling pair produces the prespecified routing and permission difference;
- the same-rule semantic null and routing-invariance control preserve their specified safeguards and permissions;
- routine disposition continues to satisfy the formal progression-action contract and is removed from `P_auto_progress` claims if a later frozen definition changes that classification;
- F4 correspondence is determined only by `P0-SIGMA-1`'s required-meaning record and exact stable semantic-ID rule and is invariant to display wording;
- F5 remains `unassessable` with `FM_APPLICABILITY_UNDETERMINED` unless a later version explicitly declares obligation scope and all required inputs;
- F1 and F2 remain outside fixture scope; F3 produces only the prespecified `unassessable` or `not_applicable` results; completed effective review, contestability, restoration, attackability, prevalence, and historical claims remain outside the fixture's conclusions;
- oracle-only fields, expected results, display text, ordering, irrelevant metadata, and execution order cannot control behavior;
- invalid paired inputs, partial rules, and random draws fail visibly before outcome comparison;
- deterministic replay reproduces hashes and outputs; and
- a standalone reader can understand the case, causal contrast, two controls, and non-claims without the short essay.

Meeting these criteria completes the fixture specification only. It does not complete Slice 0, implement the fixture, freeze the protocol, or produce a research result.
