# Literature and Originality Map

Status: Slice 0 structured scoping map; bibliography must be normalized before manuscript submission

## Purpose

This map prevents the paper from claiming novelty for established ideas and identifies the narrower synthesis the study must demonstrate. It is not a systematic review and does not support publication-count or absence-of-literature claims.

## Adjacent Literatures

| Literature | Representative anchor | What it already establishes | What this study may use | What this study must not claim as new |
| --- | --- | --- | --- | --- |
| Comparison of information structures | Blackwell, “Equivalent Comparisons of Experiments,” *Annals of Mathematical Statistics* 24(2), 1953, DOI [10.1214/aoms/1177729032](https://doi.org/10.1214/aoms/1177729032) | Experiments can be ordered by informativeness through decision-theoretic comparisons and garbling relations. | A declared refinement/coarsening relation independent of the downstream permission rule. | The general idea of ordering more- and less-informative evidence. |
| Selective classification and abstention | El-Yaniv & Wiener, “On the Foundations of Noise-free Selective Classification,” *JMLR* 11, 2010, [paper](https://jmlr.org/papers/v11/el-yaniv10a.html); Franc & Průša, “On Discriminative Learning of Prediction Uncertainty,” ICML 2019, [paper](https://proceedings.mlr.press/v97/franc19a.html) | Reject options trade coverage for predictive risk; abstention and uncertainty estimation can improve component decisions. | The distinction between component abstention and what the surrounding workflow permits next. | Abstention, calibration, or risk-coverage tradeoffs themselves. |
| Robust decision making under ambiguity | Gilboa & Schmeidler, “Maxmin Expected Utility with Non-Unique Prior,” *Journal of Mathematical Economics* 18(2), 1989, DOI [10.1016/0304-4068(89)90018-9](https://doi.org/10.1016/0304-4068(89)90018-9) | Decision rules can be evaluated across sets of plausible states or priors. | Requiring automatic progression to be supported across compatible refinements. | Max-min or robust-choice reasoning generally. |
| Queueing and service systems | Little, “A Proof for the Queuing Formula: L = λW,” *Operations Research* 9(3), 1961, DOI [10.1287/opre.9.3.383](https://doi.org/10.1287/opre.9.3.383) | Arrival, capacity, and waiting time are linked; nominal service steps may fail under load. | Modeling review as a finite-capacity service dependency and validating limiting cases analytically. | Queueing theory or capacity boundaries in general. |
| Administrative burden | Moynihan, Herd & Harvey, “Administrative Burden,” *JPART* 25(1), 2015, DOI [10.1093/jopart/muu009](https://doi.org/10.1093/jopart/muu009); Herd & Moynihan, “Administrative Burdens in the Social Safety Net,” *JEP* 39(1), 2025, DOI [10.1257/jep.20231394](https://doi.org/10.1257/jep.20231394) | Citizen-state interaction can impose learning, compliance, and psychological costs, unequally distributed. | Separating recipient evidence-production and access burdens from agency workload. | The concept or taxonomy of administrative burden. |
| Automated administrative decision making | Roehl, “Automated decision-making and good administration,” *Government Information Quarterly* 40(4), 2023, DOI [10.1016/j.giq.2023.101864](https://doi.org/10.1016/j.giq.2023.101864); Roehl, “Automated, administrative decision-making and good governance,” *Public Administration Review*, 2024, DOI [10.1111/puar.13799](https://doi.org/10.1111/puar.13799) | Automation changes discretion, administration, transparency, and governance tradeoffs. | Treating authority allocation and review as organizational properties. | The observation that automation changes public-sector discretion or accountability. |
| Contestability | Landau, Dempsey, Kamar & Bellovin, “Recommendations for Government Development and Use of Advanced Automated Systems,” 2024, [Stanford CISAC](https://cisac.fsi.stanford.edu/publication/recommendations-government-development-and-use-advanced-automated-systems-make) | Effective challenge mechanisms are central to fairness and can reveal systemic error. | Splitting structural availability, realized opportunity, uptake, and restoration. | The normative importance of review or contestability. |
| System safety and control structures | Leveson, *Engineering a Safer World*, MIT Press, 2011; Leveson & Thomas, *STPA Handbook*, [MIT](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf) | Safety is a system/control problem involving constraints, feedback, coordination, and migration under operational conditions. | Evaluating the evidence-to-action workflow rather than component accuracy alone. | System-level safety analysis, control structures, or feedback reasoning. |
| AI risk governance and red teaming | NIST, *AI Risk Management Framework 1.0*, 2023, [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1) | AI risk management requires contextual mapping, measurement, governance, monitoring, and differentiated human roles. | A repeatable process-red-team protocol with explicit ownership and claim limits. | Contextual AI risk management or red teaming generally. |
| Public-sector algorithmic impact assessment | Reisman et al., *Algorithmic Impact Assessments*, AI Now Institute, 2018, [report](https://ainowinstitute.org/publication/algorithmic-impact-assessments-report-2); Royal Commission Recommendation 17.2 | Public agencies need structured assessment, public accountability, and independent scrutiny of automated decisions. | Linking a formal invariant to trace-level diagnostics and interventions. | Impact assessment, transparency, or independent audit as policy proposals. |

## Specific Gap the Paper Tests

The paper does not claim a new theory of information, abstention, queues, burden, administrative law, or system safety. Its proposed contribution is the joint specification and empirical demonstration of a narrower workflow invariant:

> A loss of decision-relevant information must not, by itself, add automatic progression actions unless each added action is independently supported across the admissible refinements or is authorized through an effective, action-binding review; weaker evidence may still add constraint, information-seeking, or restoration actions.

The contribution requires all of the following to be present together:

1. an evidence order independent of the permission rule;
2. explicit separation of formal authority, functional permission, and executed action;
3. an action taxonomy that does not mistake precautionary constraint for authority expansion;
4. independently owned support, materiality, and semantic-correspondence rules;
5. separate tests for gate safety, effective review, timely decision service, contestability, and restoration;
6. a dynamic finite-cohort demonstration showing how load, access, deadlines, and recovery semantics change outcomes; and
7. a document-grounded public-administration application with strict historical and legal claim boundaries.

If the completed study merely shows that an explicitly permissive rule behaves permissively, or that queues grow when load exceeds capacity, it has not demonstrated this contribution.

## Originality Claims and Falsifiers

| Candidate claim | Evidence required | Falsifier or narrowing condition |
| --- | --- | --- |
| The formal invariant locates a workflow failure missed by component-level correctness checks. | At least one controlled representation/provenance or routing mutation where a local accuracy/calculation check passes but F0–F4 localizes the permission failure. | Existing component checks catch every induced failure, or the formal result follows tautologically from the authored policy label. |
| Dynamic process red teaming adds information beyond a static policy table. | Load/access/evidence perturbations change `ReviewEffective`, `DecisionServiceEffective`, exposure, or restoration while the configured rule remains fixed. | Dynamic results merely restate fail-open/fail-closed definitions or never depend on queues, access, or timing. |
| The method produces operational interventions rather than only critique. | Diagnostics identify a transition, diagnostic owner, intervention owner, tradeoff, and replayable repair. | Suggested fixes are generic transparency language or cannot be tied to a trace transition. |
| Robodebt is a valid structural application. | Separate dated profiles, citation-level transition anchors, provenance for every parameter, and explicit unsupported elements. | Profiles blend periods, rely on later variants, or require undocumented historical numbers. |
| The method transfers beyond the case vocabulary. | The blinded contemporary-AI canary yields the same mechanism-level localization without Robodebt terms. | Success depends on debt-specific labels or tuning after viewing the canary oracle. |

## Positioning Language for the Article

Use:

- “We synthesize established ideas into a workflow-level permission invariant and test its operational implications under finite capacity.”
- “The contribution is the coupling of information loss to automatic action, not a new general ordering of information.”
- “The simulation demonstrates behavior within declared process and parameter assumptions; it does not estimate Robodebt's historical rates.”
- “Process red teaming is the evaluation method; it is not evidence of historical strategic attack.”

Avoid:

- “No prior work has considered uncertainty and authority.”
- “Human review solves the problem.”
- “Robodebt proves the same failure exists in modern AI.”
- “The model establishes that a historical debt was unlawful.”
- “The simulation discovers that overload causes delay.”

## Pre-Submission Literature Gate

Before freezing the manuscript:

1. run forward and backward citation review for the core information-order, abstention, human-oversight, public-ADM, burden, contestability, and system-safety anchors;
2. add any work that already formalizes permission monotonicity or uncertainty-conditioned authority;
3. narrow the originality statement if an equivalent invariant is found;
4. distinguish cited theory from sources used only for institutional context; and
5. ensure every “unlike prior work” sentence names a specific comparison rather than an unbounded absence claim.
