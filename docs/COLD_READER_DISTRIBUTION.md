# Cold-Reader Distribution Procedure

Status: Slice 0 distribution control; no valid reader returns recorded

## Two QA Stages

The repository uses two distinct artifact-QA stages:

1. **Slice 0 construct-readability QA:** eligible readers receive the representation-preservation packet and transfer canary. This checks whether the protocol and construct boundaries can be applied before simulator implementation.
2. **Slice 3 pre-freeze protocol QA:** new eligible readers receive the executable, prespecified Robodebt worked-trace packet and the transfer canary. This checks the Level C/trace-facing protocol before version `1.0` freezes.

The P0 packet is not a Robodebt trace. It tests continuity with the short essay. The future Robodebt packet must be rendered from `RB-WORKED-TRACE-001` after the executable trace exists; it must not be substituted with P0 in a receipt labeled “Robodebt.”

## Eligibility

An eligible reader:

- did not draft the protocol or packets;
- has not seen either withheld oracle, fixture expected-result table, or executable expected output;
- receives an exported packet rather than repository access; and
- can return a locked assessment without coaching.

The oracle custodian may answer logistics questions but not explain classifications, diagnostics, or expected results. Possible or confirmed oracle exposure invalidates the run for blind QA; retain it only as a practice receipt.

## Build a Slice 0 Bundle

```bash
python3 scripts/build_cold_reader_bundle.py \
  --reader-id CR-001 \
  --output outputs/cold_reader/CR-001.zip
```

The builder uses a closed allowlist and packages only:

- the protocol;
- the blinded P0 packet;
- the blinded transfer canary;
- the blank QA receipt;
- distribution instructions; and
- a byte-level hash manifest.

It refuses output outside the repository workspace and never copies the formal fixture or withheld expected profiles. Distribute only the zip file, not a repository link.

## Custodian Procedure

1. Assign a pseudonymous reader ID; record no personal data.
2. Build the archive and retain the printed archive SHA-256.
3. Record the distribution timestamp and secure channel outside the reader artifact.
4. Receive and timestamp the locked return before opening either oracle.
5. Confirm exposure status and blind-run validity.
6. Compare every expected row, including omissions and claim-limit receipts.
7. Record ambiguity and any semantic/display-only revision.
8. If semantics change, increment versions and use new readers for the rerun.

Agreement is not the only outcome. Unsupported certainty, owner conflation, omitted tradeoffs, incorrect `not_applicable`, and prohibited claims are blocking ambiguities even when headline statuses happen to match.

## Current Boundary

No completed receipt is stored as of 2026-10-31. The drafting agent cannot certify independence. Slice 0 may be marked source-and-specification complete only after the project lead decides whether the preliminary independent-reader gate is satisfied; protocol version `1.0` and confirmatory freeze remain blocked until valid pre-freeze QA is complete.
