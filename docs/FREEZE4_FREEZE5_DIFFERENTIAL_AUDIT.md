# Freeze 4/Freeze 5 Differential Audit

Status: **pass**

Every Freeze 4 attempt was paired with its Freeze 5 counterpart (32,400 attempts). Cohort hashes, complete system-event hashes, event counts, evaluation-bridge receipts, top-level study identities, every pre-existing row field, and every pre-existing analysis field are exact. There are no missing or unexpected attempt identifiers and no blocking mismatch.

The event hash is a digest of the ordered system stream, including each case identifier, causal key, event type, timestamp, and event details. Exact event hashes therefore establish that Freeze 5 changed reporting rather than cases, event order, timing, actions, queues, or modeled outcomes.

The compiled-configuration hash changes in every pair because the compiled receipt binds executable identity; this is an expected identity change after the frozen reporting code advanced. The evaluation specification and its routing/action comparison receipt remain byte-identical. Attempt hashes and schema versions change because Freeze 5 adds 19 stored row fields and advances the attempt schema.

## New reporting only

For fail-open review, Freeze 5 stores evidence-only, authorization-only, and joint failures plus the two overlapping unions. For information first, it stores adequate response evidence, retrieval attempts and successes, unresolved evidence after acquisition, and review-request incidence. All old cell estimates, paired contrasts, precision decisions, process contrasts, random-number diagnostics, and evaluation summaries are unchanged.

Machine receipt: `docs/FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json`
