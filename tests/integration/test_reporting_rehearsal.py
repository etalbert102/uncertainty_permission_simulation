from copy import deepcopy
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[2]
PILOT_RECEIPT = ROOT / "data/pilot/pilot_v1_receipt.json"
FIGURE = runpy.run_path(str(ROOT / "reporting/build_article_figure3.py"))
TABLE = runpy.run_path(str(ROOT / "reporting/build_article_table3.py"))


def _receipt() -> dict[str, object]:
    return json.loads(PILOT_RECEIPT.read_text(encoding="utf-8"))


def test_figure3_rehearsal_consumes_all_three_repaired_panels() -> None:
    payload = FIGURE["build_payload"](_receipt())
    assert payload["family_count"] == 15
    assert {item["load"] for item in payload["panel_a"]} == {"0.6", "0.95", "1.2"}
    assert {item["policy_id"] for item in payload["panel_b"]} == {"U0", "U3"}
    assert {item["factor"] for item in payload["panel_c"]} == {
        "access_barrier", "retrievability", "staff_access",
    }
    for item in payload["panel_b"]:
        assert abs(sum(item["states"].values()) - 1.0) < 1e-12


def test_figure3_values_come_from_receipt_not_prose_constants() -> None:
    receipt = _receipt()
    baseline = FIGURE["build_payload"](receipt)
    mutated = deepcopy(receipt)
    target = next(
        cell for cell in mutated["cell_summaries"]
        if cell["policy_id"] == "U2C" and cell["factors"]["load"] == "0.6"
    )
    target["timeout_activation_rate"] = float(target["timeout_activation_rate"]) + 0.01
    candidate = dict(mutated)
    candidate.pop("receipt_hash")
    mutated["receipt_hash"] = FIGURE["_canonical_hash"](candidate)
    changed = FIGURE["build_payload"](mutated)
    assert baseline["panel_a"] != changed["panel_a"]


def test_table3_rehearsal_has_one_quantity_per_identity() -> None:
    table = TABLE["build_table"](_receipt(), development=True)
    quantity_ids = [row["quantity_id"] for row in table["rows"]]
    assert table["status"] == "development_only_rehearsal"
    assert len(quantity_ids) == len(set(quantity_ids)) == 5
    assert quantity_ids.count("U3_MINUS_U0_UNRESOLVED_NONPROGRESSION") == 1
    assert all("claim_boundary" in row for row in table["rows"])
