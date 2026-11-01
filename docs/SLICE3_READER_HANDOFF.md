# Slice 3 Independent-Reader Handoff

Status: ready for external distribution; no valid returns received

The oracle custodian must send the generated ZIP files, not a repository link. Readers must not receive repository access or either expected profile before their returns are locked.

## Prepared distributions

| Reader ID | Workspace artifact | Archive SHA-256 |
| --- | --- | --- |
| `CR-S3-001` | `outputs/cold_reader/CR-S3-001.zip` | `2e13a16a1be45c6e8c081721f5c1bd89ac662d248c5d39e57f4210b1fa8aaefb` |
| `CR-S3-002` | `outputs/cold_reader/CR-S3-002.zip` | `98c175ae5a4f4663cb997890d00a58f534b903639d11c183d9aa905815179364` |

Before sending, rebuild each archive with `scripts/build_slice3_reader_bundle.py`, record the printed hash in this table or the custodian's controlled log, and confirm that the manifest says `contains_oracles: false`. Do not open the repository on a reader's device.

## Required return

Each eligible reader returns:

1. the completed `qa_receipt.md` and `assessment_template.json`;
2. separate Robodebt baseline and repair F0–F5 rows;
3. all required transfer-canary rows and claim-limit receipts;
4. a conclusion and ambiguity log; and
5. confirmation of no pre-return oracle or repository exposure.

The custodian timestamps and locks each return before opening `docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md` or `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`. Possible or confirmed exposure invalidates the run for freeze purposes.

## Acceptance and escalation

At least two distinct eligible readers are required. Compare omissions, status, completeness, located transition, diagnostic, missing information/claim limit, diagnostic owner, intervention owner, and tradeoff. Agreement on headline status does not cure unsupported certainty, omitted rows, owner conflation, or prohibited claims. Log every ambiguity in `docs/PROTOCOL_REVISION_LOG.md`; semantic changes require a version increment and new-reader rerun.

No personal data or human-performance claim is authorized.

After both locked JSON returns are received, the custodian runs:

```bash
PYTHONPATH=src python scripts/verify_slice3_reader_returns.py \
  outputs/cold_reader/CR-S3-001-return.json \
  outputs/cold_reader/CR-S3-002-return.json \
  --output outputs/cold_reader/slice3_external_qa_gate_receipt.json
```

The verifier checks packet hashes, archive hashes, eligibility and exposure controls, timestamps, the complete 29-row inventory, closed vocabularies, status/completeness, expected diagnostics, located transitions, distinct readers and runs, and conclusion fields. It authorizes protocol `1.0` promotion only when both locked returns exactly match the withheld profiles. A mismatch remains blocking; do not relabel it an acceptable variant without a separately recorded oracle-custodian adjudication and semantic-change decision.
