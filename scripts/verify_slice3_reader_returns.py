"""Validate locked external returns and emit a pre-freeze gate receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uncertainty_permission_simulation.qa import QAReturnError, verify_external_qa_gate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("returns", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        values = [json.loads(path.read_text(encoding="utf-8")) for path in args.returns]
        result = verify_external_qa_gate(ROOT, values)
    except (OSError, json.JSONDecodeError, QAReturnError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.output:
        output = args.output.resolve()
        if ROOT not in output.parents:
            raise SystemExit("output must remain inside the repository workspace")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass" if result["external_qa_gate_passed"] else "fail",
        "reader_count": result["reader_count"],
        "gate_receipt_hash": result["gate_receipt_hash"],
    }, sort_keys=True))
    return 0 if result["external_qa_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
