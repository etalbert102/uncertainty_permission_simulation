# Slice 3 Independent-Reader Handoff

Status: ready for external distribution; no valid returns received

The oracle custodian must send the generated ZIP files, not a repository link. Readers must not receive repository access or either expected profile before their returns are locked.

## Prepared distributions

| Reader ID | Workspace artifact | Archive SHA-256 |
| --- | --- | --- |
| `CR-S3-001` | `outputs/cold_reader/CR-S3-001.zip` | `8f99c5c003cd959f78dee2f464c606a6c334502318a7236288caad7ff6b33af6` |
| `CR-S3-002` | `outputs/cold_reader/CR-S3-002.zip` | `b2649ce1754fb9193c6bd286a4ea372c6e621019c4b2c39231813680c3bb112b` |

Before sending, rebuild each archive with `scripts/build_slice3_reader_bundle.py`, record the printed hash in this table or the custodian's controlled log, and confirm that the manifest says `contains_oracles: false`. Do not open the repository on a reader's device.

## Required return

Each eligible reader returns:

1. the completed `qa_receipt.md`;
2. separate Robodebt baseline and repair F0–F5 rows;
3. all required transfer-canary rows and claim-limit receipts;
4. a conclusion and ambiguity log; and
5. confirmation of no pre-return oracle or repository exposure.

The custodian timestamps and locks each return before opening `docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md` or `docs/TRANSFER_CANARY_EXPECTED_PROFILE.md`. Possible or confirmed exposure invalidates the run for freeze purposes.

## Acceptance and escalation

At least two distinct eligible readers are required. Compare omissions, status, completeness, located transition, diagnostic, missing information/claim limit, diagnostic owner, intervention owner, and tradeoff. Agreement on headline status does not cure unsupported certainty, omitted rows, owner conflation, or prohibited claims. Log every ambiguity in `docs/PROTOCOL_REVISION_LOG.md`; semantic changes require a version increment and new-reader rerun.

No personal data or human-performance claim is authorized.
