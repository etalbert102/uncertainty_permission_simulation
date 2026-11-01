"""Build an oracle-free Slice 3 packet for independent artifact QA."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ALLOWLIST = {
    "protocol.md": Path("docs/PROCESS_RED_TEAM_PROTOCOL.md"),
    "robodebt_worked_trace.md": Path("docs/ROBODEBT_WORKED_TRACE_PACKET.md"),
    "transfer_canary.md": Path("docs/TRANSFER_CANARY.md"),
    "qa_receipt.md": Path("docs/SLICE3_COLD_READER_QA_RECEIPT.md"),
}
FORBIDDEN = {
    Path("docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md"),
    Path("docs/TRANSFER_CANARY_EXPECTED_PROFILE.md"),
    Path("data/golden_traces/robodebt_worked_trace_v1.json"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reader-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", args.reader_id):
        raise SystemExit("reader-id must be a 1-64 character study-local token")
    if args.output.suffix.lower() != ".zip":
        raise SystemExit("output must end in .zip")
    root = Path(__file__).resolve().parents[1]
    payloads: dict[str, bytes] = {}
    resolved_allowlist: set[Path] = set()
    for archive_name, relative in ALLOWLIST.items():
        path = (root / relative).resolve(strict=True)
        if root not in path.parents or path.is_symlink():
            raise SystemExit(f"unsafe allowlist path: {relative}")
        resolved_allowlist.add(path)
        payloads[archive_name] = path.read_bytes()
    forbidden = {(root / path).resolve(strict=True) for path in FORBIDDEN}
    if resolved_allowlist & forbidden:
        raise SystemExit("withheld oracle entered distribution allowlist")
    payloads["README.md"] = (
        f"# Slice 3 Cold-Reader Distribution\n\nReader ID: `{args.reader_id}`\n\n"
        "Use only these packet files. Lock and return the completed receipt before any oracle is opened. "
        "This evaluates artifacts, not readers; record no personal data.\n"
    ).encode()
    manifest = {
        "bundle_format": 1,
        "qa_stage": "slice_3_pre_freeze",
        "reader_id": args.reader_id,
        "contains_oracles": False,
        "files": {
            name: {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
            for name, data in sorted(payloads.items())
        },
        "forbidden_pre_return_access": [str(path) for path in sorted(FORBIDDEN)],
    }
    payloads["distribution_manifest.json"] = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode()
    output = args.output.resolve()
    if root not in output.parents:
        raise SystemExit("output must remain inside repository workspace")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(payloads.items()):
            info = ZipInfo(name, date_time=(2026, 11, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    print(json.dumps({"output": str(output), "sha256": sha256(output.read_bytes()).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
