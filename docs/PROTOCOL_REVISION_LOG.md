# Protocol and Application Revision Log

This is the pre-freeze semantic change log required by the preregistration. Entries are append-only. A row marked `yes` in the rerun column invalidates prior blind QA for freeze purposes and requires new eligible readers.

| Date | Version/artifact | Owner | Change | Reason | Affected property, hypothesis, or artifact | Semantic? | Cold-reader rerun? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-31 | Protocol `0.2` candidate | study design | Established three application levels, non-composite F0–F5 reporting, and closed status vocabulary. | Slice 0 construct closure. | F0–F5; P0 and transfer packets | yes | yes, initial QA required |
| 2026-11-01 | Slice 3 worked-trace packet `1.0-candidate` | implementation | Added the executable prespecified Robodebt trace packet, withheld expected profile, trace-specific receipt, and oracle-free builder. | The pre-freeze QA target must be the Robodebt trace rather than P0. | `RB-WORKED-TRACE-001`; protocol operational usability | no protocol-semantic change; new application artifact | yes, initial Slice 3 QA required |
| 2026-11-01 | Counterfactual process extension `1` | study design | Declared assistance, extension, and agency evidence acquisition as study-owned counterfactual capabilities in the U3 worked-trace arm. | U3 cannot masquerade as a historical early-OCI capability. | Worked trace; H3; historical claim boundary | yes for trace mapping, not protocol meaning | yes |

No confirmatory result had been generated or inspected when these entries were made.
