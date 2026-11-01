# P0 Procedure-Review Input

Status: draft review-input version `0.1`; contains inputs only

Companion protocol: `docs/PROCESS_RED_TEAM_PROTOCOL.md`, version `0.2`

Reference-profile access: complete the first-pass assessment before consulting it

## Project-Lead Review Instructions

For the first pass, use only this input and the process-red-team protocol. Record where the instructions are unclear before consulting the formal fixture, P0 usability walkthrough, expected-result records, or executable fixture output. Prior familiarity does not invalidate the review, but record it because this is a comprehensibility check rather than an independent or blinded validation exercise.

Complete the protocol intake receipt, choose the application level, classify each requested property/helper or mark it `omitted_by_claim_limit`, identify the first material transition, select diagnostics from the protocol lookup, propose an intervention, distinguish diagnostic and intervention ownership, and state all non-claims. Do not produce an overall score.

## Evaluation Question

Holding the underlying case, uncertain model output, policy, downstream rule, process state, resources, clock, and random draws fixed, does changing only the representation transformation change scrutiny or automatic functional permission? Which formal properties and helpers can be assessed from this bounded trace?

## Fixed Unit and Comparison

| Field | Input |
| --- | --- |
| Evaluation unit | Controlled pair of bounded deterministic trace specifications |
| Core case | `P0-C1`, a synthetic hypothetical low-resolution track |
| Model output | `P0-M1` |
| Arms | `P0-E-PRESERVE` and `P0-E-FALLBACK` |
| Held rule | `P0-D-ENABLE` |
| Held process/resource/clock | `P0-Q1-C1`, `P0-RES1`, `P0-T1` |
| Random draws | None; count is zero in both arms |
| Intended variation | Transformation and the representation it emits |

The case is synthetic. Its latent object type exists only for oracle validation and is unavailable to transformation, policy evaluation, routing, and this protocol application. Do not use latent truth to classify either arm.

## Fixed Model Output

`P0-M1` contains:

| Field | Value |
| --- | --- |
| Primary estimate | `pickup_like_silhouette` |
| Primary confidence | `0.42` |
| Broad class | `vehicle` |
| Fallback threshold | `0.6` |
| Live unresolved alternatives | `armed_technical`, `civilian_pickup`, `modified_truck` |
| Alternative probabilities | Not provided |
| Source | Synthetic model output |

The model output contains no policy-relevance field or safeguard instruction. Every listed alternative is compatible with the broad class `vehicle`. Both arms consume this exact stored output.

## Transformations

### Preserve transformation

`P0-Preserve` emits separately typed derived claims for the broad class, primary estimate, confidence, threshold, unresolved-alternatives status, and each live alternative. Each claim references the fixed model output, transformation, compatible-state set, and projection facts. It declares no additional assumptions. Claim type, transformation, compatible-state meaning, semantic identity, uncertainty status, and provenance are visible to the policy evaluator, router, and reviewer.

### Fallback transformation

Because `0.42 < 0.6`, `P0-Fallback` emits only the broad value `vehicle`. The emitted candidate field is deliberately represented as an `UntypedField`: it has a stored-record envelope and transformation source, but no claim evidence type, claim-level transformation binding, assumption set, compatible-state meaning, semantic identity, uncertainty status, or downstream-visible provenance.

Both transformations are deterministic and cannot access the case, latent truth, policy, routing outcome, process state, resources, clock, or expected results.

## Independent Materiality and Required Meaning

The independently owned evaluation specification declares the unresolved `armed_technical` alternative material to the routine-disposition action. The required meaning is the live unresolved classification alternative `armed_technical`, scoped to `P0-M1`. Exact stable semantic identity establishes correspondence; display-text similarity and the workflow's own materiality rule do not.

For this material item, the declared baseline requires:

- an additional-information action;
- review by a role with stopping authority; and
- a fail-closed dependency preventing routine disposition until review completes.

The independently required surfaced meaning must reach an authorized role before `ROUTING_COMPLETED` at `T0`.

## Held Routing Rule and Actions

`P0-D-ENABLE` applies the following total rule to the visible representation:

1. If a visible live alternative is designated material, route to `enhanced_scrutiny`: enable additional information and review, configure a fail-closed gate, and place the case-bound routine action in the post-review set rather than the automatic progression set.
2. Otherwise, if the broad class is `vehicle`, route to `routine`: place the case-bound routine action in the automatic progression set, with no information action or configured review gate.
3. Otherwise, emit an unassessable disposition with no enabled action.

The exact action instances are:

| Action | Direction | Effect |
| --- | --- | --- |
| `P0-A-INFO-C1` | information | Obtain additional sensor evidence. |
| `P0-A-REVIEW-C1` | constraint | Commit reviewer time with stopping authority and constrain routine disposition pending a recorded decision. |
| `P0-A-ROUTINE-C1` | progression | Advance the case to terminal routine disposition and close the enhanced-scrutiny opportunity. |

## Trace Facts Through the Declared Boundary

Both arms record representation application, representation surfacing, and routing completion at the fixed decision instant. The preserve arm surfaces every typed claim before routing. The fallback arm surfaces its single broad candidate field before routing.

The resource record states that the reviewer is available and has stopping authority. In the preserve arm, the gate is required and configured fail closed, the required review evidence is visible, and the workflow dependency is enforced. Review has not started or completed, no review decision has been recorded, and the routine action has not executed by the trace boundary.

In the fallback arm, the independent baseline still requires a gate and review for the material alternative, but the operational disposition configures no gate, carries no required review evidence, enables no review action, and places the routine action in automatic progression. No action execution, service deadline, contestability path, or restoration horizon is modeled in either arm.

## Frozen Property Scope

| Property/helper | Scope information supplied for review |
| --- | --- |
| F0 | Included for both representations. |
| F1 | Explicitly excluded because evidence and model output do not vary. |
| F2 | Explicitly excluded because there is no execute-versus-hold fallback intervention over a declared intervention unit. |
| F3 | Conditional on an in-scope post-review progression action. |
| F4 | Conditional on an independently material item affecting an in-scope action. |
| F5 | Scope is undetermined because obligation scope, correction path, horizons, consequences, and restoration baseline are absent. |
| GateSafe | Conditional on a configured gate. A separately required missing gate is diagnosed outside this helper. |
| ReviewEffective | Conditional on a required or configured review dependency. |
| DecisionServiceEffective | Included, but no service deadline or supported final disposition is supplied in this packet. |
| Capacity/service boundary | The bounded trace contains no arrival rate, service time, queue discipline, shared capacity, or system intervention. |

## Blank Scope Receipt

- Workflow/profile and version:
- Evaluation unit:
- Application level and rationale:
- Comparison and baseline:
- Claim sought:
- Explicit non-claims:
- Packet version and assessor:

## Blank Assessment Profile

| Step | Property/helper | Evaluation state | Status | Completeness | Located transition | Evidence | Diagnostic or justification | Missing information or claim limit | Intervention | Diagnostic owner | Intervention owner | Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | F0 — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 1 | F0 — fallback |  |  |  |  |  |  |  |  |  |  |  |
| 1 | F4 — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 1 | F4 — fallback |  |  |  |  |  |  |  |  |  |  |  |
| 2 | F1 — preserve/fallback comparison |  |  |  |  |  |  |  |  |  |  |  |
| 2 | F2 — preserve/fallback comparison |  |  |  |  |  |  |  |  |  |  |  |
| 3 | GateSafe — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 3 | GateSafe — fallback |  |  |  |  |  |  |  |  |  |  |  |
| 3 | ReviewEffective — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 3 | ReviewEffective — fallback |  |  |  |  |  |  |  |  |  |  |  |
| 3 | F3 — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 3 | F3 — fallback |  |  |  |  |  |  |  |  |  |  |  |
| 3 | DecisionServiceEffective |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Capacity/service boundary |  |  |  |  |  |  |  |  |  |  |  |
| 5 | F5 — preserve |  |  |  |  |  |  |  |  |  |  |  |
| 5 | F5 — fallback |  |  |  |  |  |  |  |  |  |  |  |

## Conclusion Receipt

State the strongest supported finding, every known failure, every unresolved or omitted conclusion, the first material transition, interventions and tradeoffs, any required escalation, and all prohibited claims. List ambiguities separately. Do not infer historical prevalence, legality, attackability, or an overall workflow score.
