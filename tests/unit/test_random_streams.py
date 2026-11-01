from decimal import Decimal

import pytest
from pydantic import ValidationError

from uncertainty_permission_simulation.random_streams import DRAW_FAMILY_IDS, DrawKey, KeyedRandomStream, normalized_decimal
from uncertainty_permission_simulation.schemas import ContractError, PAYLOAD_MODELS


def test_keyed_draw_replays_exactly() -> None:
    first = KeyedRandomStream("SEED-1").draw("CASE-1", "review_service")
    second = KeyedRandomStream("SEED-1").draw("CASE-1", "review_service")
    assert first == second
    assert Decimal(0) < first.unit_interval_value < Decimal(1)
    assert first.content_hash == second.content_hash


def test_draws_do_not_depend_on_request_order_or_branch_count() -> None:
    baseline = KeyedRandomStream("SEED-1")
    expected = baseline.draw("CASE-1", "evidence_retrieval_success")

    divergent = KeyedRandomStream("SEED-1")
    divergent.draw("CASE-1", "extension_need", 0)
    divergent.draw("CASE-1", "extension_need", 1)
    divergent.draw("CASE-2", "review_service", 0)
    observed = divergent.draw("CASE-1", "evidence_retrieval_success")
    assert observed == expected


def test_draw_inventory_is_sorted_and_deduplicated() -> None:
    stream = KeyedRandomStream("SEED-1")
    second = stream.draw("CASE-2", "notice_delivery")
    first = stream.draw("CASE-1", "notice_delivery")
    assert stream.draw("CASE-1", "notice_delivery") is first
    assert stream.draws() == (first, second)


@pytest.mark.parametrize(
    "key",
    (
        ("", "initiation", 0),
        ("CASE-1", "not-a-family", 0),
        ("CASE-1", "initiation", -1),
        ("CASE-1", "initiation", True),
        (1, "initiation", 0),
    ),
)
def test_invalid_draw_keys_fail_with_stable_diagnostic(key: tuple[object, object, object]) -> None:
    with pytest.raises(ContractError, match="RANDOM_DRAW_KEY_INVALID"):
        DrawKey(*key)


def test_manifest_closes_keyed_draw_family_ids() -> None:
    model = PAYLOAD_MODELS["KeyedDraw"]
    valid = model(
        keyed_draw_id="DRAW-1", case_id="CASE-1", event_family_id="initiation", draw_index=0,
        distribution_parameter_refs=(), seed_id="SEED-1", value={"kind": "decimal", "value": "0.5"},
    )
    assert valid.event_family_id in DRAW_FAMILY_IDS
    with pytest.raises(ValidationError):
        model(
            keyed_draw_id="DRAW-2", case_id="CASE-1", event_family_id="queue_position", draw_index=0,
            distribution_parameter_refs=(), seed_id="SEED-1", value={"kind": "decimal", "value": "0.5"},
        )


def test_manifest_rejects_duplicate_draw_family_id() -> None:
    from uncertainty_permission_simulation.schemas import MANIFEST, validate_model_manifest_inventory

    family_ids = MANIFEST["closed_draw_family_ids"]
    family_ids.append(family_ids[0])
    try:
        with pytest.raises(ContractError, match="closed draw-family inventory"):
            validate_model_manifest_inventory()
    finally:
        family_ids.pop()


def test_decimal_rendering_preserves_integer_zeroes() -> None:
    assert normalized_decimal(Decimal("10")) == "10"
    assert normalized_decimal(Decimal("10.5000")) == "10.5"
    assert normalized_decimal(Decimal("-0")) == "0"
