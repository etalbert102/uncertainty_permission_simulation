"""Build an oracle-free cold-reader artifact-QA bundle.

This utility is intentionally independent of the simulation package. It copies only a
closed allowlist of Slice 0 Markdown inputs, records byte hashes, and writes a zip
archive for distribution outside repository access.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZIP_DEFLATED, ZipFile


ALLOWED_FILES = {
    "protocol.md": Path("docs/PROCESS_RED_TEAM_PROTOCOL.md"),
    "p0_packet.md": Path("docs/P0_COLD_READER_PACKET.md"),
    "transfer_canary.md": Path("docs/TRANSFER_CANARY.md"),
    "qa_receipt.md": Path("docs/COLD_READER_QA_RECEIPT.md"),
}

FORBIDDEN_REPOSITORY_FILES = {
    Path("docs/P0_USABILITY_WALKTHROUGH.md"),
    Path("docs/TRANSFER_CANARY_EXPECTED_PROFILE.md"),
    Path("docs/PRECURSOR_FIDELITY_FIXTURE.md"),
    Path("docs/FORMAL_MODEL.md"),
}

VERSION_PATTERNS = {
    "protocol.md": re.compile(r"Status:\s*draft version\s*`([^`]+)`", re.IGNORECASE),
    "p0_packet.md": re.compile(r"packet version\s*`([^`]+)`", re.IGNORECASE),
    "transfer_canary.md": re.compile(r"packet version\s*`([^`]+)`", re.IGNORECASE),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reader-id", required=True, help="Study-local pseudonymous ID")
    parser.add_argument("--output", type=Path, required=True, help="Target .zip path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", args.reader_id):
        raise SystemExit("reader-id must be a 1–64 character study-local token")
    if args.output.suffix.lower() != ".zip":
        raise SystemExit("output must end in .zip")

    repository_root = Path(__file__).resolve().parents[1]
    payloads: dict[str, bytes] = {}
    versions: dict[str, str] = {}

    allowed_resolved = set()
    for archive_name, relative_path in ALLOWED_FILES.items():
        source = (repository_root / relative_path).resolve(strict=True)
        if repository_root not in source.parents or source.is_symlink():
            raise SystemExit(f"unsafe source path: {relative_path}")
        allowed_resolved.add(source)
        data = source.read_bytes()
        payloads[archive_name] = data
        pattern = VERSION_PATTERNS.get(archive_name)
        if pattern:
            match = pattern.search(data.decode("utf-8"))
            if not match:
                raise SystemExit(f"version marker missing from {relative_path}")
            versions[archive_name] = match.group(1)

    forbidden_resolved = {
        (repository_root / path).resolve(strict=True) for path in FORBIDDEN_REPOSITORY_FILES
    }
    if allowed_resolved & forbidden_resolved:
        raise SystemExit("oracle or specification file entered the distribution allowlist")

    instructions = f"""# Cold-Reader Distribution

Reader ID: `{args.reader_id}`

Use only the files in this archive. Do not access the repository, expected profiles,
formal fixture, or executable expected outputs before returning a locked assessment.
Complete both packets using `protocol.md` and record the result in `qa_receipt.md`.
Return the completed receipt and assessment artifacts to the oracle custodian. The
custodian, not the reader, opens withheld profiles after the return is locked.

This exercise evaluates the artifacts, not the reader. Do not add names, contact
details, demographics, or other personal data.
""".encode("utf-8")
    payloads["README.md"] = instructions

    manifest = {
        "bundle_format": 1,
        "reader_id": args.reader_id,
        "purpose": "slice-0 protocol artifact QA",
        "contains_oracles": False,
        "versions": versions,
        "files": {
            name: {"sha256": sha256_bytes(data), "bytes": len(data)}
            for name, data in sorted(payloads.items())
        },
        "forbidden_access_before_locked_return": [
            str(path) for path in sorted(FORBIDDEN_REPOSITORY_FILES)
        ],
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    payloads["distribution_manifest.json"] = manifest_bytes

    output = args.output.resolve()
    if repository_root not in output.parents:
        raise SystemExit("output must remain inside the repository workspace")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(payloads.items()):
            archive.writestr(name, data)

    print(json.dumps({"output": str(output), "sha256": sha256_bytes(output.read_bytes())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
