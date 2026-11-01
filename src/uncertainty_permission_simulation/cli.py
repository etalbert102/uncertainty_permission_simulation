"""Study-specific command line interface."""

from __future__ import annotations

import argparse
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import yaml

from .applications.robodebt import load_early_adapter
from .artifacts import build_bundle
from .configuration import ParameterValue, ScenarioOverlaySpec, compile_configuration
from .formal_model import render_p0_report
from .metrics import engagement_metrics, trace_metrics
from .policies import POLICY_IDS
from .process_model import TraceSpec, execute_topology, run_trace
from .profiles import canonical_process, nonisomorphic_process, policy, smoke_overlay, stochastic_process
from .random_streams import normalized_decimal
from .simulator import StochasticCohortSpec, StochasticInputOverlay, generate_stochastic_cohort, run_engagement_stage


ROOT = Path(__file__).resolve().parents[2]
KERNEL_SOURCE_PATHS = tuple(
    ROOT / "src/uncertainty_permission_simulation" / name
    for name in ("configuration.py", "events.py", "formal_model.py", "metrics.py", "process_model.py", "rules.py", "schemas.py")
)


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


def _configuration_hash(configuration: object) -> str:
    payload = configuration.model_dump(mode="json")
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _slice1_validation_observations(reference_u2c: object) -> dict[str, dict[str, object]]:
    renamed = canonical_process("RENAMED-VOCABULARY@1")
    renamed_config = compile_configuration(
        configuration_id="RENAMED-U2C", process=renamed, policy=policy("U2C"),
        overlay=smoke_overlay("RENAMED-OVERLAY@1"), evaluation_spec_id="P0-SIGMA-1",
    )
    original_canary = run_trace(TraceSpec("CANARY-ORIGINAL", "U2C", review_delay=30))
    renamed_canary = run_trace(TraceSpec("CANARY-RENAMED", "U2C", review_delay=30))

    nonisomorphic = nonisomorphic_process()
    nonisomorphic_config = compile_configuration(
        configuration_id="NONISO-U2C", process=nonisomorphic, policy=policy("U2C"),
        overlay=smoke_overlay("NONISO-OVERLAY@1"), evaluation_spec_id="P0-SIGMA-1",
    )
    nonisomorphic_events = execute_topology(
        ("CASE_ARRIVAL", "ROUTING_COMPLETED", "EVIDENCE_REQUESTED", "REVIEW_QUEUED", "CASE_CLOSED")
    )

    early_process, early_policy = load_early_adapter(ROOT / "data/sources/robodebt/r_oci_early.yaml")
    adapter_overlay = ScenarioOverlaySpec(
        overlay_id="R-OCI-EARLY-SMOKE-OVERLAY@1",
        parameters=(
            ParameterValue(slot_id="notice_delay", value="1", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
            ParameterValue(slot_id="review_capacity", value="1", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
            ParameterValue(slot_id="review_service_time", value="30", provenance="stylized", owner_id="R-OCI-EARLY-SMOKE-OVERLAY@1"),
        ),
    )
    adapter = compile_configuration(
        configuration_id="R-OCI-EARLY-SMOKE", process=early_process, policy=early_policy,
        overlay=adapter_overlay, evaluation_spec_id="P0-SIGMA-1",
        application_mapping_id="R-OCI-EARLY-MAPPING@1",
    )
    unsupported_slots = {
        parameter.slot_id for parameter in early_process.documented_parameters
        if parameter.provenance == "unsupported"
    }
    kernel_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in KERNEL_SOURCE_PATHS)

    return {
        "isomorphic_vocabulary": {
            "artifact_identity_differs": _configuration_hash(renamed_config) != _configuration_hash(reference_u2c),
            "event_order_equal": tuple(event.event_type_id for event in original_canary.events) == tuple(event.event_type_id for event in renamed_canary.events),
            "metrics_equal": trace_metrics(original_canary) == trace_metrics(renamed_canary),
            "semantic_projection_equal": original_canary.semantic_projection == renamed_canary.semantic_projection,
        },
        "nonisomorphic_topology": {
            "compiler_code_hash_equal": nonisomorphic_config.compiler_code_hash == reference_u2c.compiler_code_hash,
            "events": nonisomorphic_events,
            "profile_id": nonisomorphic.profile_id,
            "stage_ids": nonisomorphic.stage_ids,
            "topology_differs": nonisomorphic.stage_ids != reference_u2c.process_profile.stage_ids,
            "unresolved_parameter_slot_ids": nonisomorphic_config.unresolved_parameter_slot_ids,
        },
        "application_adapter": {
            "application_mapping_id": adapter.application_mapping_id,
            "compiler_code_hash_equal": adapter.compiler_code_hash == reference_u2c.compiler_code_hash,
            "configuration_id": adapter.configuration_id,
            "kernel_case_identifiers_absent": "robodebt" not in kernel_text and "r-oci" not in kernel_text,
            "receipt_provenance": {receipt.slot_id: receipt.provenance for receipt in adapter.receipts},
            "receipt_slots": tuple(receipt.slot_id for receipt in adapter.receipts),
            "unresolved_parameter_slot_ids": adapter.unresolved_parameter_slot_ids,
            "unsupported_defaults_used": any(
                receipt.slot_id in unsupported_slots and receipt.provenance == "documented"
                for receipt in adapter.receipts
            ),
        },
    }


def run_smoke(config_path: Path) -> dict[str, object]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    compiled = [compile_configuration(configuration_id=f"SYNTH-{name}", process=canonical_process(), policy=policy(name), overlay=smoke_overlay(), evaluation_spec_id="P0-SIGMA-1") for name in ("U1", "U2C", "U2O")]
    specs = _specs()
    results = {spec.trace_id: run_trace(spec) for spec in specs}
    report = render_p0_report(results["P0-E-PRESERVE"], results["P0-E-FALLBACK"])

    validation_observations = _slice1_validation_observations(compiled[1])
    output = {
        "schema_version": 1,
        "config_id": config["config_id"],
        "compiled_configuration_ids": [item.configuration_id for item in compiled],
        "traces": {trace_id: {"events": [event.event_type_id for event in result.events], "route": result.route, "action": result.final_action, "metrics": trace_metrics(result)} for trace_id, result in results.items()},
        "p0_report": report,
        "isomorphic_canary": validation_observations["isomorphic_vocabulary"],
        "nonisomorphic_canary": validation_observations["nonisomorphic_topology"],
        "robodebt_adapter": validation_observations["application_adapter"],
    }
    output_path = ROOT / config["output_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record_bundle = build_bundle(specs, results, validation_observations=validation_observations)
    if not all(comparison["match"] for comparison in record_bundle["comparisons"]):
        raise RuntimeError("golden expected-versus-actual comparison failed")
    if any(status != "match" for status in record_bundle["validation_receipt_status"].values()):
        raise RuntimeError("stored canary or adapter expected-versus-actual comparison failed")
    report_links: dict[str, dict[str, object]] = {"preserve": {}, "fallback": {}}
    for record in record_bundle["records"]:
        payload = record["payload"]
        if payload.get("payload_kind") != "assessment":
            continue
        assessment_id = payload["assessment_id"]
        arm = "preserve" if assessment_id.startswith("P0-E-PRESERVE") else "fallback" if assessment_id.startswith("P0-E-FALLBACK") else None
        if arm:
            report_links[arm][payload["property_or_helper_id"]] = {
                "assessment_ref": {"object_id": record["meta"]["object_id"], "object_version": record["meta"]["object_version"]},
                "diagnostic_refs": payload["diagnostic_refs"],
            }
    report["artifact_refs"] = report_links
    records_path = ROOT / config["records_output_path"]
    records_path.write_text(json.dumps(record_bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output["record_bundle"] = {"path": config["records_output_path"], "record_count": record_bundle["record_count"], "closure_status": record_bundle["closure_status"]}
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def run_stochastic_smoke(config_path: Path) -> dict[str, object]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cohort_size = config["cohort_size"]
    if not isinstance(cohort_size, int) or isinstance(cohort_size, bool) or cohort_size <= 0:
        raise ValueError("cohort_size must be a positive integer")
    spec = StochasticCohortSpec(
        scenario_id=config["scenario_id"], seed_id=config["seed_id"],
        case_ids=tuple(f"CASE-{index:04d}" for index in range(1, cohort_size + 1)),
        overlay=StochasticInputOverlay(
            overlay_id=config["overlay"]["overlay_id"], provenance=config["overlay"]["provenance"],
            initiation_window=Decimal(str(config["overlay"]["initiation_window"])),
            notice_delay=Decimal(str(config["overlay"]["notice_delay"])),
            response_deadline=Decimal(str(config["overlay"]["response_deadline"])),
            review_capacity=Decimal(str(config["overlay"]["review_capacity"])),
            review_service_time=Decimal(str(config["overlay"]["review_service_time"])),
            review_service_window=Decimal(str(config["overlay"]["review_service_window"])),
            extension_duration=Decimal(str(config["overlay"]["extension_duration"])),
            notice_delivery_probability=Decimal(str(config["overlay"]["notice_delivery_probability"])),
            administrative_access_probability=Decimal(str(config["overlay"]["administrative_access_probability"])),
            comprehension_probability=Decimal(str(config["overlay"]["comprehension_probability"])),
            record_availability_probability=Decimal(str(config["overlay"]["record_availability_probability"])),
            response_effort_limit=Decimal(str(config["overlay"]["response_effort_limit"])),
            assistance_effort_bonus=Decimal(str(config["overlay"]["assistance_effort_bonus"])),
            extension_effort_bonus=Decimal(str(config["overlay"]["extension_effort_bonus"])),
            extension_need_probability=Decimal(str(config["overlay"]["extension_need_probability"])),
            evidence_retrieval_success_probability=Decimal(str(config["overlay"]["evidence_retrieval_success_probability"])),
            evidence_retrieval_latency_scale=Decimal(str(config["overlay"]["evidence_retrieval_latency_scale"])),
        ),
    )
    cohort = generate_stochastic_cohort(spec)
    configured_policy_ids = tuple(config["policy_ids"])
    if len(configured_policy_ids) != len(POLICY_IDS) or set(configured_policy_ids) != set(POLICY_IDS):
        raise ValueError(f"policy_ids must contain each closed policy exactly once: {POLICY_IDS}")
    compiled_engagement = {
        policy_id: compile_configuration(
            configuration_id=f"{config['config_id']}-{policy_id}", process=stochastic_process(),
            policy=policy(policy_id), overlay=spec.overlay.to_compilation_overlay(),
            evaluation_spec_id="STOCHASTIC-ENGAGEMENT-QA@1",
        )
        for policy_id in POLICY_IDS
    }
    engagement_runs = {
        policy_id: run_engagement_stage(cohort, compiled_engagement[policy_id])
        for policy_id in POLICY_IDS
    }
    output = {
        "schema_version": 1,
        "config_id": config["config_id"],
        "scenario_id": cohort.scenario_id,
        "overlay": cohort.overlay.canonical_value(),
        "seed_id": cohort.seed_id,
        "cases": [
            {
                "case_id": case.case_id,
                "arrival_time": normalized_decimal(case.arrival_time),
                "draw_hash": case.draw_hash,
                "keyed_draws": [draw.canonical_value() | {"content_hash": draw.content_hash} for draw in case.keyed_draws],
            }
            for case in cohort.cases
        ],
        "telemetry": {
            "case_count": cohort.telemetry.case_count,
            "keyed_draw_count": cohort.telemetry.keyed_draw_count,
            "draw_family_counts": dict(cohort.telemetry.draw_family_counts),
            "duplicate_draw_key_count": cohort.telemetry.duplicate_draw_key_count,
            "cohort_hash": cohort.telemetry.cohort_hash,
        },
        "engagement_runs": {
            policy_id: {
                "compiled_configuration_id": compiled_engagement[policy_id].configuration_id,
                "cohort_hash": run.cohort_hash,
                "metrics": engagement_metrics(run),
                "telemetry": {
                    "case_count": run.telemetry.case_count,
                    "event_count": run.telemetry.event_count,
                    "response_count": run.telemetry.response_count,
                    "adequate_response_evidence_count": run.telemetry.adequate_response_evidence_count,
                    "assistance_count": run.telemetry.assistance_count,
                    "extension_count": run.telemetry.extension_count,
                    "retrieval_request_count": run.telemetry.retrieval_request_count,
                    "retrieved_evidence_count": run.telemetry.retrieved_evidence_count,
                    "review_queue_count": run.telemetry.review_queue_count,
                    "review_started_count": run.telemetry.review_started_count,
                    "review_completed_count": run.telemetry.review_completed_count,
                    "timely_review_count": run.telemetry.timely_review_count,
                    "late_review_count": run.telemetry.late_review_count,
                    "review_total_wait_time": normalized_decimal(run.telemetry.review_total_wait_time),
                    "review_max_wait_time": normalized_decimal(run.telemetry.review_max_wait_time),
                    "review_schedule_hash": run.telemetry.review_schedule_hash,
                    "event_hash": run.telemetry.event_hash,
                },
                "review_queue": {
                    "queue_id": run.review_queue.config.queue_id,
                    "capacity": run.review_queue.config.capacity,
                    "discipline": run.review_queue.config.discipline,
                    "visits": [
                        {
                            "request_id": visit.request_id,
                            "case_id": visit.case_id,
                            "server_id": visit.server_id,
                            "queued_at": normalized_decimal(visit.queued_at),
                            "started_at": normalized_decimal(visit.started_at),
                            "completed_at": normalized_decimal(visit.completed_at),
                            "service_time": normalized_decimal(visit.service_time),
                            "wait_time": normalized_decimal(visit.wait_time),
                            "deadline": normalized_decimal(visit.deadline),
                            "completed_by_deadline": visit.completed_by_deadline,
                        }
                        for visit in run.review_queue.visits
                    ],
                },
                "system_events": [
                    {
                        "case_id": event.case_id,
                        "event_type_id": event.event_type_id,
                        "timestamp": normalized_decimal(event.timestamp),
                        "causal_event_key": event.causal_event_key,
                    }
                    for event in run.system_events
                ],
                "traces": [
                    {
                        "case_id": trace.case_id,
                        "exogenous_draw_hash": trace.exogenous_draw_hash,
                        "decision": {
                            "assistance_used": trace.decision.assistance_used,
                            "extension_granted": trace.decision.extension_granted,
                            "responded": trace.decision.responded,
                            "adequate_response_evidence": trace.decision.adequate_response_evidence,
                            "proactive_retrieval_requested": trace.decision.proactive_retrieval_requested,
                            "retrieved_evidence": trace.decision.retrieved_evidence,
                        },
                        "events": [
                            {
                                "event_type_id": event.event_type_id,
                                "timestamp": normalized_decimal(event.timestamp),
                                "causal_event_key": event.causal_event_key,
                                "details": event.details,
                            }
                            for event in trace.events
                        ],
                        "event_hash": trace.event_hash,
                    }
                    for trace in run.traces
                ],
            }
            for policy_id, run in engagement_runs.items()
        },
        "claim_limit": "review-queue stochastic smoke artifact; no final action, empirical, or historical outcome",
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
    cohort = subparsers.add_parser("cohort")
    cohort.add_argument("config", type=Path)
    args = parser.parse_args()
    if args.command == "trace":
        result = run_smoke(args.config)
        print(json.dumps({"status": "ok", "traces": len(result["traces"]), "output": result["config_id"]}, sort_keys=True))
    elif args.command == "cohort":
        result = run_stochastic_smoke(args.config)
        print(json.dumps({"status": "ok", "cases": len(result["cases"]), "policies": len(result["engagement_runs"]), "output": result["config_id"]}, sort_keys=True))


if __name__ == "__main__":
    main()
