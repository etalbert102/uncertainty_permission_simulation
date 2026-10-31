"""Study-specific command line interface."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import yaml

from .applications.robodebt import load_early_adapter
from .configuration import ParameterValue, ScenarioOverlaySpec, compile_configuration
from .formal_model import render_p0_report
from .metrics import trace_metrics
from .process_model import TraceSpec, execute_topology, run_trace
from .profiles import canonical_process, nonisomorphic_process, policy, smoke_overlay


ROOT = Path(__file__).resolve().parents[2]


def _specs() -> tuple[TraceSpec, ...]:
    return (
        TraceSpec("P0-E-PRESERVE", "U1", "preserve", True, review_delay=30),
        TraceSpec("P0-E-FALLBACK", "U1", "fallback", True),
        TraceSpec("P0-NO-CHANGE-PRESERVE", "U1", "preserve", False, force_scrutiny=True, review_delay=30),
        TraceSpec("P0-NO-CHANGE-FALLBACK", "U1", "fallback", False, force_scrutiny=True, review_delay=30),
        TraceSpec("GOLDEN-IMPUTE-NONRESPONSE", "U1"),
        TraceSpec("GOLDEN-U2C-QUEUE-HOLD", "U2C", review_delay=30),
        TraceSpec("GOLDEN-U2O-TIMEOUT", "U2O", review_delay=30),
        TraceSpec("GOLDEN-SUPPORTED-PROGRESSION", "U2C", response=True, action_evidence=True),
        TraceSpec("GOLDEN-PARTIAL-RESTORATION", "U1", external_exposure=True, correction=True),
    )


def run_smoke(config_path: Path) -> dict[str, object]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    compiled = [compile_configuration(configuration_id=f"SYNTH-{name}", process=canonical_process(), policy=policy(name), overlay=smoke_overlay(), evaluation_spec_id="P0-SIGMA-1") for name in ("U1", "U2C", "U2O")]
    results = {spec.trace_id: run_trace(spec) for spec in _specs()}
    report = render_p0_report(results["P0-E-PRESERVE"], results["P0-E-FALLBACK"])

    renamed = canonical_process("RENAMED-VOCABULARY@1")
    renamed_config = compile_configuration(configuration_id="RENAMED-U2C", process=renamed, policy=policy("U2C"), overlay=smoke_overlay("RENAMED-OVERLAY@1"), evaluation_spec_id="P0-SIGMA-1")
    canary_spec = TraceSpec("CANARY-RENAMED", "U2C", review_delay=30)
    original_canary = run_trace(TraceSpec("CANARY-ORIGINAL", "U2C", review_delay=30))
    renamed_canary = run_trace(canary_spec)
    noniso_events = execute_topology(("CASE_ARRIVAL", "ROUTING_COMPLETED", "EVIDENCE_REQUESTED", "REVIEW_QUEUED", "CASE_CLOSED"))
    compile_configuration(configuration_id="NONISO-U2C", process=nonisomorphic_process(), policy=policy("U2C"), overlay=smoke_overlay("NONISO-OVERLAY@1"), evaluation_spec_id="P0-SIGMA-1")

    early_process, early_policy = load_early_adapter(ROOT / "data/sources/robodebt/r_oci_early.yaml")
    adapter_overlay = ScenarioOverlaySpec(
        overlay_id="R-OCI-EARLY-SMOKE-OVERLAY@1",
        parameters=(
            ParameterValue(slot_id="notice_delay", value="1", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
            ParameterValue(slot_id="review_capacity", value="1", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
            ParameterValue(slot_id="review_service_time", value="30", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
        ),
    )
    adapter = compile_configuration(configuration_id="R-OCI-EARLY-SMOKE", process=early_process, policy=early_policy, overlay=adapter_overlay, evaluation_spec_id="P0-SIGMA-1", application_mapping_id="R-OCI-EARLY-MAPPING@1")
    output = {
        "schema_version": 1,
        "config_id": config["config_id"],
        "compiled_configuration_ids": [item.configuration_id for item in compiled],
        "traces": {trace_id: {"events": [event.event_type_id for event in result.events], "route": result.route, "action": result.final_action, "metrics": trace_metrics(result)} for trace_id, result in results.items()},
        "p0_report": report,
        "isomorphic_canary": {"semantic_projection_equal": original_canary.semantic_projection == renamed_canary.semantic_projection, "artifact_identity_differs": renamed_config.configuration_id != compiled[1].configuration_id},
        "nonisomorphic_canary": {"profile_id": nonisomorphic_process().profile_id, "events": noniso_events},
        "robodebt_adapter": {"configuration_id": adapter.configuration_id, "receipt_slots": [receipt.slot_id for receipt in adapter.receipts], "kernel_case_branch": False},
    }
    output_path = ROOT / config["output_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    trace = subparsers.add_parser("trace")
    trace.add_argument("config", type=Path)
    args = parser.parse_args()
    if args.command == "trace":
        result = run_smoke(args.config)
        print(json.dumps({"status": "ok", "traces": len(result["traces"]), "output": result["config_id"]}, sort_keys=True))


if __name__ == "__main__":
    main()
