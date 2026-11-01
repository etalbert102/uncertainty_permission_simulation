# Robodebt Application Sufficiency Review

Status: Slice 3 pre-freeze candidate

The application meets the minimum defensible threshold for structural grounding. It does not calibrate historical rates, reconstruct amounts, decide legal validity, or establish attackability. Executable numerical assumptions remain in separately versioned stylized overlays.

| Manuscript claim class | Source anchor or boundary owner | Status | Permitted claim |
| --- | --- | --- | --- |
| Early OCI notice, 21-day clock, reminder, nonresponse averaging, debt notice, recovery, reassessment, and review path | `OMB-OCI-2017`, `OMB17-1.17-1.29` | documented | Describe the dated process structure with the source's own period limits. |
| Aggregate-to-fortnight averaging and the risk for intermittent income | `OMB-OCI-2017`, `OMB17-APP-B`; `OMB-IMPLEMENTATION-2019`, `OMB19-P15-16` | documented | Identify the representation transition and its possible mismatch with period-specific income. |
| Baseline routing, calculation, officer handling, automatic debt raising, and advice | `RRC-MAP-4B-2023`, `MAP-4B-1-5`, `MAP-4B-19-28`, `MAP-4B-29-36` | documented process-map structure | Use as a dated process skeleton, not an independent legal finding. |
| Enhanced delivery, access, response-time, extension, manual-intervention, and evidence changes | `OMB-OCI-2017`, `OMB17-1.30-1.46` | documented | Treat as a separate repair profile, not proof that every defect was cured. |
| Clear review paths, inspectable automated rules, proportionate recovery, and access-aware service design | `RRC-REPORT-2023`, `RRC-17-1`, `RRC-17-2`, `RRC-18-1`, `RRC-10-1` | source-attributed recommendation | Attribute the recommendation; do not present it as a simulator finding. |
| Functional permission expands after imputation in the modeled U1 comparator | Formal model, compiled U1 policy, and `RB-WORKED-TRACE-001` | inferred/model-defined | Claim structural susceptibility under declared rules only. |
| Queue capacity, service times, engagement probabilities, retrieval success, correction uptake, and restoration delays | `SLICE3-BASE-STYLIZED-OVERLAY@1` | stylized | Report as study-owned scenario values, never historical estimates. |
| Historical legality of a particular debt | Royal Commission/Ombudsman attribution only | unsupported as an independent study conclusion | The simulation reports no legal verdict. |
| Historical strategic exploitation, observability, repeatability, inducibility, or benefit | none | unsupported | Make no attackability claim about Robodebt. |
| Transfer to contemporary AI systems | Formal invariant plus explicitly supported institutional similarities | bounded inference | Transfer the diagnostic method, not prevalence or outcome rates. |

## Sufficiency decision

- The early and enhanced profiles are dated and remain separate.
- Every executable historical-profile slot is documented or explicitly `unsupported`; no historical default is supplied.
- The source record supports the process skeleton needed to apply the formal invariant.
- The fixed source record does not support population calibration; the paper must preserve that limitation.
- Later EIC, CUPI, PAYG Manual, and remediation variants remain outside the primary application.

Decision: **sufficient for a formal counterfactual simulation grounded in a documented case, subject to the automated pre-freeze artifact gates and frozen remote-source identity rule. Procedure comprehensibility is reviewed by the project lead after Slice 5 and is not evidence of case validity.**
