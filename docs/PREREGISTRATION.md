# Preregistration Skeleton

Status: version `1.0` confirmatory contract; development pilot inspected; no confirmatory results generated or inspected

Protocol version: `1.0`

Formal specification: `docs/FORMAL_MODEL.md`, version `1.0`

Candidate source-grounded application profiles: `R-OCI-Early@1` and `R-OCI-Enhanced@1`; neither is an engine dependency or population calibration

## Study Question

Under what combinations of evidentiary incompleteness, representation policy, administrative access, workload, deadlines, review semantics, evidence acquisition, and restoration design does a workflow permit automatic progression without robust support, lose effective review, or convert service failure into external harm?

## Design Classification

This is a formal counterfactual simulation implemented in a case-neutral dynamic kernel and grounded through a documented Robodebt application adapter. Canonical synthetic profiles establish the mechanism and validation behavior; Robodebt establishes structural relevance. The study is not a historical numerical reconstruction, an estimate of current-system prevalence, a legal adjudication, or a test of historical strategic exploitation.

Each executable arm uses a validated compiled configuration containing one process capability profile, one active policy profile, one independent evaluation specification, an application mapping where applicable, a scenario overlay, and a complete parameter-binding receipt. Raw source descriptions and unsupported historical fields are non-executable.

The completed evidence stack will contain:

1. a formal specification and finite structural checks;
2. an executable representation-preservation fixture;
3. dated source-validation adapters for early and enhanced OCI plus a parameter-provenance table separating documented structure from stylized overlays;
4. a finite-cohort discrete-event simulation of declared counterfactual policies; and
5. a frozen five-step process-red-team protocol.

## Primary Hypotheses

- **H1 — fail-closed capacity boundary:** As review-bound load rises, U2C retains `GateSafe` but reaches a boundary beyond which `ReviewEffective` and `DecisionServiceEffective` decline while unresolved holds grow.
- **H2 — timeout semantics:** Under identical cases and exogenous service requirements, U2O converts more queue delay into robust-permission violations and recovery exposure than U2C.
- **H3 — information-first tradeoff:** When agency evidence retrieval succeeds within the service window, U3 reduces recipient evidence-production burden and action without period-specific support relative to U0, but increases agency workload and may delay disposition when retrieval is slow or unsuccessful.

H1–H3 are the only primary substantive hypotheses.

## Secondary Hypotheses and Validation Expectations

- **H4:** Administrative-access barriers reduce engagement under every policy; clearer notice, extensions, and agency assistance reduce but need not eliminate the disparity.
- **H5:** Complete staff access to evidence and provenance improves effective-review opportunity relative to partial access under otherwise identical gate and staffing conditions.
- **V1:** U1 produces more progression through imputation than U0 in the enabling fixture. This validates implementation and is not a substantive discovery.
- **V2:** Verified-match, no-support/no-progression, no-threshold, and routing-invariance controls do not exhibit robust-permission violations.

## Policies

| Policy | Frozen semantic role | Gate semantics | Historical status |
| --- | --- | --- | --- |
| U0 | Claimant-led evidence and hold | no debt progression while required evidence is missing | counterfactual comparator |
| U1 | Impute and progress | automatic progression after declared imputation rule | failure benchmark; not recommended |
| U2C | Impute, review, fail closed | progression remains blocked until valid review completes | counterfactual comparator |
| U2O | Impute, review, fail open | timeout enables progression | stress-test comparator; not recommended |
| U3 | Agency-assisted information first | acquire evidence, hold while unresolved, then review as required | counterfactual comparator |

Historical R-OCI profiles are source-validation application fixtures, not policy arms, population estimators, or owners of kernel semantics. Parameters absent from the source record remain `unsupported` in those fixtures; executable study values must come from separate versioned stylized overlays.

## Unit, Cohort, and Pairing

- Unit of simulation: a case moving through a finite-cohort administrative process.
- Unit of generalization for cross-scenario summaries: scenario family.
- Policy comparison: paired within scenario family and seed.
- Exogenous draws: keyed by case ID, event family, and draw index.
- Endogenous event counts may differ by policy and must not shift unrelated draws.
- All policies within a family receive identical case membership, latent case attributes, potential evidence, access attributes, and keyed exogenous draws.

## Core Scenario Factors

| Factor | Prespecified levels | Provenance |
| --- | --- | --- |
| Initiation load relative to declared capacity vector | `0.6`, `0.95`, `1.2` | stylized |
| Missing fortnight-specific evidence at initiation | `0.10`, `0.30`, `0.50` | stylized |
| Administrative-access barriers | `0.10`, `0.30`, `0.50` | stylized |
| Third-party evidence retrievability | low, high | stylized |
| Staff access to evidence/provenance | partial, complete | stylized |

The nominal Cartesian count is 108 environmental families and up to 540 paired policy conditions. Semantic-validity constraints determine the final count. The final count is frozen after the pilot; target cardinality is not an acceptance criterion.

## Historical Fixture Values

- R-OCI-Early uses the documented 21-day clock measured from the letter date and the separately documented 14-day reminder.
- R-OCI-Enhanced uses the documented 28-day clock measured from receipt and keeps the separately documented 14-day post-provisional warning distinct.
- No queue, service, engagement, retrieval, or error distribution is treated as historically measured by the fixed source packet.
- Deadline contrasts are not interpreted as the effect of time alone when other documented profile changes differ.

The Robodebt mapping may be corrected, narrowed, or versioned before confirmatory freeze if source review or artifact QA shows that it does not meet the minimum defensible case threshold. Any change is logged. Replacing Robodebt as the primary application requires a new plan and preregistration version. The selected application identity, source manifest, adapter version, compiled process and policy profiles, provenance table, stylized overlays, and inference limits are frozen before confirmatory execution.

## Primary Outcomes

No composite workflow score or primary scalar utility is permitted.

### Evidentiary and permission outcomes

- robust-permission violations per 1,000 initiated cases;
- progression based on untyped or provenance-suppressed imputation;
- debt action without declared period-specific support;
- configured-gate, `GateSafe`, `ReviewEffective`, and `DecisionServiceEffective` rates;
- pre-action review bypass;
- surfacing loss; and
- recovery begun before effective review or reassessment.

### Process outcomes

- queue length, waiting time, utilization, expiry, throughput, unresolved holds, information-acquisition demand and latency;
- notice/access failures, contacts, evidence requests, estimated evidence-production effort, and extensions; and
- time to supported disposition or correction.

### Recovery and restoration outcomes

- days under asserted debt before correction;
- modeled recovery or collection exposure;
- reassessment opportunity, reduction, and zeroing; and
- partial versus complete restoration with residual consequences reported separately.

### Deliberate outcome boundary

The study does not model a latent monetary entitlement, a full-information debt-amount oracle, signed or absolute amount error, or amount recovered. It estimates quantitative event rates, timing, workload, burden, exposure, correction, and restoration outcomes under the declared process model. These simulated operational outcomes remain distinct from both evidentiary support and source-attributed legal validity.

## Primary Estimands

1. The load boundary at which U2C preserves gate safety while losing effective review or timely decision service.
2. Paired U2O-minus-U2C differences in robust-permission violations and recovery exposure near that boundary.
3. Paired U3-minus-U0 differences in recipient burden, agency workload, evidentiary support, time to supported disposition, unresolved cases, and correction opportunity.

Secondary estimands cover interactions with access barriers, evidence retrievability, staff provenance access, and the distinction among configured review and the three operational helpers.

## Controls

Required matched controls include:

- complete period-specific evidence supporting progression;
- independent verification before progression;
- cases with no supported progression eligibility under either evidence state;
- changes limited to information or constraint actions;
- no review requirement because no progression threshold is crossed; and
- representation change with invariant routing and permission.

Controls are reported separately and do not inflate the primary scenario count.

## Horizon and Censoring

Each replicate must declare:

- finite case-initiation window or frozen cohort;
- administrative follow-up cutoff;
- event-drain rule after initiation stops;
- right-censoring for open evidence, review, recovery, and reassessment states; and
- evaluation horizons for realized contestability and restoration.

Open cases remain visible by reason and policy. A realized contestability or restoration status cannot be assigned before its frozen horizon.

## Replications and Precision

The Slice 3 freeze candidate uses 80 cases per family-replication. The finite initiation window is derived from cohort size, review-service scale, review capacity, and the declared load factor; the administrative cutoff is day 650. Open evidence, review, recovery, reassessment, or restoration paths remain right-censored by stage-specific reason. A timely decision is scored separately from terminal restoration.

The minimum is 30 paired replications per valid family and the maximum is 60, with the maximum no greater than 100 per family under any candidate revision. The MCSE targets are 0.05 for primary rates and 0.06 for paired policy differences. The family-wide extension rule is: if any applicable primary metric misses its target at 30 replications, every policy in every valid family extends to 60 using the next frozen seeds. The core confirmatory runtime ceiling is 24 wall-clock hours on the frozen environment; the extension has one separate 24-hour ceiling.

No family receives extra replications because a result is surprising, favorable, or publication-worthy.

## Analysis

- Estimate within-family paired policy differences using common random numbers.
- Report rates, paired differences, uncertainty intervals, and Monte Carlo standard errors.
- Separate stochastic uncertainty within families from variation across scenario assumptions.
- Report boundary surfaces and interactions, not only pooled means.
- Keep U2C and U2O separate.
- Report nulls, adverse results, censoring, unresolved states, and tradeoffs.
- Treat any scalar loss or Pareto ranking as a labeled sensitivity analysis with explicit normative weights.

## Validation Before Substantive Interpretation

Required gates:

- seven exact golden traces;
- canonical synthetic traces that do not load an institutional adapter;
- isomorphic adapter/domain-renaming invariance;
- a non-isomorphic synthetic topology with different stage order, optional review, and queue layout;
- compiled-configuration closure with exactly one owner per runtime slot;
- rejection of documented-value overwrite, raw narrative execution, and policy-created undeclared topology;
- rejection of case-specific engine branches and silent defaults for `unsupported` historical parameters;
- conservation of cases and events;
- deterministic simultaneous-event ordering;
- zero-arrival, infinite-capacity, zero-service-time, complete-evidence, universal-response, and no-deadline limits;
- comparison with an analytical queue case where assumptions align;
- repeated-seed hash identity;
- keyed-draw invariance under policy-dependent event-count changes;
- slower reference-simulator differential checks; and
- V1/V2 control expectations.

Substantive estimates remain invalid until all blocking gates pass.

## Worked Trace

The article trace is fixed by `docs/WORKED_TRACE_SELECTION.md` and `data/scenarios/worked_trace_spec_v1.yaml`. It is a prespecified explanatory trace, not statistically representative. Its ID and specification cannot change after confirmatory output inspection.

## Exclusions and Claim Limits

- No numeric reconstruction of Robodebt outcomes.
- No simulator-generated historical legal conclusion.
- No historical attackability claim.
- No inference from the synthetic AI canary to deployment prevalence.
- No pooling of early OCI, enhanced OCI, EIC, CUPI, PAYG Manual, or remediation processes.
- No tuning of factors, exclusions, metrics, seeds, or analysis after confirmatory freeze.

## Change Control

Before freeze, every semantic, application-mapping, compilation-contract, or overlay change records date, owner, reason, and affected hypothesis/property/artifact. After freeze, any change to the selected application, sources, adapter, compiled configuration, stylized overlays, definitions, policies, parameters, seeds, metrics, exclusions, code, or analysis invalidates the affected confirmatory run and requires a new versioned freeze.

The protocol reaches version `1.0` only in Slice 4 after pilot validation, executable fixture/reference agreement, application-sufficiency review, and all automated pre-freeze gates pass. Slice 3 fixes the design-freeze candidate values above but does not freeze confirmatory seeds or authorize confirmatory execution. The project-lead comprehensibility review occurs after Slice 5 analysis; editorial corrections do not alter the freeze, while semantic corrections invalidate affected confirmatory artifacts and require a new versioned freeze and rerun.
