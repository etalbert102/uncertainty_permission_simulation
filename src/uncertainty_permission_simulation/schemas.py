"""Closed, manifest-backed record contracts for the study."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt, SerializeAsAny, create_model, model_validator
import yaml


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data/model/schema_manifest_v1.yaml"
MANIFEST: dict[str, Any] = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


class ContractError(ValueError):
    """Stable contract failure with a closed diagnostic code."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RecordRef(StrictModel):
    object_id: str
    object_version: int = Field(gt=0)


class SchemaRef(StrictModel):
    schema_id: str
    schema_version: int = Field(gt=0)


class RecordMeta(StrictModel):
    object_id: str
    object_version: int = Field(gt=0)
    schema_id: str
    schema_version: int = Field(gt=0)
    canonicalization_id: Literal["UPS-CANONICAL-JSON"] = "UPS-CANONICAL-JSON"
    canonicalization_version: Literal[1] = 1
    owner_id: str
    provenance_status: Literal["documented", "hypothetical", "simulated", "derived"]
    source_basis: Literal["versioned_sources", "synthetic_no_external_source"]
    source_refs: tuple[RecordRef, ...] = ()

    @model_validator(mode="after")
    def source_contract(self) -> "RecordMeta":
        if self.source_basis == "versioned_sources" and not self.source_refs:
            raise ValueError("versioned_sources requires source_refs")
        if self.source_basis == "synthetic_no_external_source" and self.source_refs:
            raise ValueError("synthetic_no_external_source forbids source_refs")
        if self.provenance_status in {"documented", "derived"} and self.source_basis != "versioned_sources":
            raise ValueError("documented/derived records require versioned sources")
        return self


def _annotation(spec: Any) -> Any:
    if isinstance(spec, str):
        kind = spec
        detail: dict[str, Any] = {}
    else:
        detail = spec or {}
        kind = detail.get("type", "any")
    if "enum" in detail:
        values = tuple(detail["enum"])
        return Literal.__getitem__(values)
    if "values" in detail:
        values = tuple(detail["values"])
        return Literal.__getitem__(values)
    if "const" in detail:
        return Literal[detail["const"]]
    closed = {
        "closed_property_or_helper_id": "closed_property_or_helper_ids",
        "closed_diagnostic_code": "closed_diagnostic_codes",
        "closed_diagnostic_category": "closed_diagnostic_categories",
        "closed_diagnostic_owning_layer": "closed_diagnostic_owning_layers",
        "closed_event_type_id": "closed_event_type_ids",
        "closed_run_status_id": "closed_run_status_ids",
        "closed_scenario_validity_status_id": "closed_scenario_validity_status_ids",
    }
    if kind in closed:
        return Literal.__getitem__(tuple(MANIFEST[closed[kind]]))
    if kind in {"string", "json_pointer", "simulation_time_string", "normalized_decimal_string", "record_ref_or_stable_role_id", "sha256_lower_hex"}:
        return str
    if kind == "nullable_string":
        return str | None
    if kind == "positive_integer":
        return PositiveInt
    if kind == "nonnegative_integer":
        return NonNegativeInt
    if kind == "integer":
        return int
    if kind == "boolean":
        return bool
    if kind == "record_ref":
        return RecordRef
    if kind == "nullable_record_ref":
        return RecordRef | None
    if kind == "schema_ref":
        return SchemaRef
    if kind in {"list_record_ref", "list_evaluation_input_binding", "list_assessment_component_binding", "list_event_rule_execution", "list_gate_requirement"}:
        return tuple[RecordRef, ...] if kind == "list_record_ref" else tuple[dict[str, Any], ...]
    if kind in {"string_list", "list_closed_diagnostic_code"}:
        return tuple[str, ...]
    if kind == "list_schema_ref":
        return tuple[SchemaRef, ...]
    if kind.startswith("nullable_"):
        return Any | None
    if kind.startswith("list_"):
        return tuple[Any, ...]
    if kind.startswith("mapping_"):
        return dict[str, Any]
    return Any


def _field_definition(spec: Any) -> tuple[Any, Any]:
    detail = spec if isinstance(spec, dict) else {}
    annotation = _annotation(spec)
    required = detail.get("required", True)
    if "const" in detail:
        return annotation, detail["const"]
    if required:
        return annotation, ...
    return annotation | None, None


def _build_payload_models() -> dict[str, type[StrictModel]]:
    models: dict[str, type[StrictModel]] = {}
    for name, spec in MANIFEST["payload_kinds"].items():
        discriminator_field, discriminator = next(iter(spec["discriminator"].items()))
        fields: dict[str, tuple[Any, Any]] = {
            discriminator_field: (Literal[discriminator], discriminator)
        }
        fields.update({field_name: _field_definition(field_spec) for field_name, field_spec in spec["fields"].items()})
        models[name] = create_model(name, __base__=StrictModel, **fields)
    return models


PAYLOAD_MODELS = _build_payload_models()


def validate_model_manifest_inventory() -> None:
    if set(PAYLOAD_MODELS) != set(MANIFEST["payload_kinds"]):
        raise ContractError("SCHEMA_MANIFEST_DRIFT", "payload model inventory differs from manifest")


def _canonical(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python", exclude_none=False))
    if isinstance(value, dict):
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, float):
        raise ContractError("SCHEMA_CANONICALIZATION_INVALID", "binary floats are forbidden")
    return value


def canonical_bytes(meta: RecordMeta, payload: BaseModel) -> bytes:
    meta_value = _canonical(meta)
    meta_value["source_refs"] = sorted(meta_value["source_refs"], key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    payload_value = _canonical(payload)
    spec = MANIFEST["payload_kinds"][payload.__class__.__name__]
    for path in spec.get("set_semantics_paths", []):
        parts = path.strip("/").split("/")
        if len(parts) == 1 and isinstance(payload_value.get(parts[0]), list):
            payload_value[parts[0]] = sorted(payload_value[parts[0]], key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    value = {"meta": meta_value, "payload": payload_value}
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def content_hash(meta: RecordMeta, payload: BaseModel) -> str:
    return sha256(canonical_bytes(meta, payload)).hexdigest()


class StoredRecord(StrictModel):
    meta: RecordMeta
    payload: SerializeAsAny[BaseModel]
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def envelope_contract(self) -> "StoredRecord":
        spec = MANIFEST["payload_kinds"].get(self.payload.__class__.__name__)
        if spec is None:
            raise ValueError("payload model absent from manifest")
        domain_id = getattr(self.payload, spec["domain_id_field"])
        if domain_id != self.meta.object_id:
            raise ValueError("payload domain ID differs from envelope object ID")
        schemas = spec.get("schema_variants", [spec.get("schema")])
        valid_schemas = {(schema["schema_id"], schema["schema_version"]) for schema in schemas if schema}
        if (self.meta.schema_id, self.meta.schema_version) not in valid_schemas:
            raise ValueError("schema identity differs from manifest")
        if self.content_hash != content_hash(self.meta, self.payload):
            raise ValueError("content hash mismatch")
        required_basis = spec.get("source_basis")
        if required_basis and self.meta.source_basis != required_basis:
            raise ValueError("source basis differs from manifest")
        required_provenance = spec.get("provenance_status")
        if required_provenance and self.meta.provenance_status != required_provenance:
            raise ValueError("provenance status differs from manifest")
        return self

    @classmethod
    def create(cls, *, meta: RecordMeta, payload: BaseModel) -> "StoredRecord":
        return cls(meta=meta, payload=payload, content_hash=content_hash(meta, payload))


class RecordStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, int], StoredRecord] = {}

    def add(self, record: StoredRecord) -> None:
        key = (record.meta.object_id, record.meta.object_version)
        prior = self._records.get(key)
        if prior and prior.content_hash != record.content_hash:
            raise ContractError("SCHEMA_CANONICALIZATION_INVALID", f"identity collision: {key}")
        self._records[key] = record

    def resolve(self, ref: RecordRef) -> StoredRecord:
        try:
            return self._records[(ref.object_id, ref.object_version)]
        except KeyError as exc:
            raise ContractError("SCHEMA_REFERENCE_UNRESOLVED", ref.object_id) from exc

    @staticmethod
    def _refs(value: Any) -> tuple[RecordRef, ...]:
        found: list[RecordRef] = []
        if isinstance(value, RecordRef):
            found.append(value)
        elif isinstance(value, BaseModel):
            for field_value in value.__dict__.values():
                found.extend(RecordStore._refs(field_value))
        elif isinstance(value, dict):
            if set(value) == {"object_id", "object_version"}:
                found.append(RecordRef.model_validate(value))
            else:
                for field_value in value.values():
                    found.extend(RecordStore._refs(field_value))
        elif isinstance(value, (tuple, list)):
            for field_value in value:
                found.extend(RecordStore._refs(field_value))
        return tuple(found)

    def validate_closure(self) -> None:
        edges: dict[tuple[str, int], set[tuple[str, int]]] = {}
        for key, record in self._records.items():
            refs = set(record.meta.source_refs) | set(self._refs(record.payload))
            edge_keys = {(ref.object_id, ref.object_version) for ref in refs}
            for ref in refs:
                self.resolve(ref)
            edges[key] = edge_keys
        visiting: set[tuple[str, int]] = set()
        visited: set[tuple[str, int]] = set()

        def visit(key: tuple[str, int]) -> None:
            if key in visiting:
                raise ContractError("SCHEMA_REFERENCE_CYCLE", key[0])
            if key in visited:
                return
            visiting.add(key)
            for target in edges[key]:
                visit(target)
            visiting.remove(key)
            visited.add(key)

        for key in edges:
            visit(key)

    def records(self) -> tuple[StoredRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))


validate_model_manifest_inventory()
