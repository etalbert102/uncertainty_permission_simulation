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


class ParameterBinding(StrictModel):
    parameter_id: str
    value_kind: Literal["literal", "record_ref", "record_ref_set", "input_field"]
    value: Any


class RuleInputSpec(StrictModel):
    role_id: str
    accepted_schema_refs: tuple[SchemaRef, ...]
    cardinality: Literal["one", "optional", "many"]


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
        "closed_rule_implementation_id": "closed_rule_implementations",
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
    if kind == "parameter_binding_list":
        return tuple[ParameterBinding, ...]
    if kind == "list_rule_input_spec":
        return tuple[RuleInputSpec, ...]
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


REFERENCE_CONTAINER_TYPES = {
    "typed_value",
    "nullable_typed_diagnostic_value",
    "parameter_binding_list",
    "list_projection_fact",
    "expected_disposition_spec",
    "list_expected_assessment_spec",
    "list_evaluation_input_binding",
    "list_assessment_component_binding",
    "list_event_rule_execution",
    "list_gate_requirement",
}


def _field_type(field_spec: Any) -> str:
    return field_spec if isinstance(field_spec, str) else field_spec.get("type", "any")


def _reference_field_names(spec: dict[str, Any]) -> set[str]:
    return {
        field_name
        for field_name, field_spec in spec["fields"].items()
        if "record_ref" in _field_type(field_spec) or _field_type(field_spec) in REFERENCE_CONTAINER_TYPES
    }


def _validate_target_declaration(source: str, field_name: str, declaration: Any, payload_kinds: set[str]) -> None:
    if declaration == "any":
        return
    if not isinstance(declaration, list) or not declaration or len(declaration) != len(set(declaration)):
        raise ContractError("SCHEMA_MANIFEST_DRIFT", f"{source}.{field_name} requires `any` or a nonempty unique target-kind list")
    unknown = set(declaration) - payload_kinds
    if unknown:
        raise ContractError("SCHEMA_MANIFEST_DRIFT", f"{source}.{field_name} names unknown target kinds: {sorted(unknown)}")


def validate_model_manifest_inventory() -> None:
    if set(PAYLOAD_MODELS) != set(MANIFEST["payload_kinds"]):
        raise ContractError("SCHEMA_MANIFEST_DRIFT", "payload model inventory differs from manifest")
    payload_kinds = set(MANIFEST["payload_kinds"])
    role_declarations = MANIFEST.get("reference_target_roles", {})
    reference_field_names: set[str] = set()
    for source_kind, spec in MANIFEST["payload_kinds"].items():
        reference_fields = _reference_field_names(spec)
        reference_field_names.update(reference_fields)
        overrides = spec.get("reference_targets", {})
        missing = reference_fields - set(role_declarations) - set(overrides)
        if missing:
            raise ContractError("SCHEMA_MANIFEST_DRIFT", f"{source_kind} reference fields lack target declarations: {sorted(missing)}")
        for path, allowed_kinds in spec.get("reference_targets", {}).items():
            if "/" in path.strip("/") or path not in reference_fields:
                raise ContractError("SCHEMA_MANIFEST_DRIFT", f"{source_kind} reference-target field {path} is undeclared or not reference-bearing")
            _validate_target_declaration(source_kind, path, allowed_kinds, payload_kinds)
    unused_roles = set(role_declarations) - reference_field_names
    if unused_roles:
        raise ContractError("SCHEMA_MANIFEST_DRIFT", f"unused reference-target roles: {sorted(unused_roles)}")
    for field_name, declaration in role_declarations.items():
        _validate_target_declaration("reference_target_roles", field_name, declaration, payload_kinds)


def _rule_error(message: str) -> None:
    raise ContractError("SCHEMA_EXECUTABLE_RULE_INVALID", message)


def _validate_record_ref(value: Any, parameter_id: str) -> None:
    try:
        RecordRef.model_validate(value)
    except (TypeError, ValueError) as exc:
        _rule_error(f"parameter {parameter_id} is not a RecordRef: {exc}")


def _validate_input_field(value: Any, parameter_id: str, role_ids: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != {"input_role_id", "field_path"}:
        _rule_error(f"parameter {parameter_id} requires an InputFieldBinding")
    if value["input_role_id"] not in role_ids:
        _rule_error(f"parameter {parameter_id} names undeclared input role {value['input_role_id']}")
    if not isinstance(value["field_path"], str) or not value["field_path"].startswith("/"):
        _rule_error(f"parameter {parameter_id} requires a JSON-pointer field_path")


def _validate_rule_parameter(
    binding: ParameterBinding,
    declaration: dict[str, Any],
    role_ids: set[str],
) -> None:
    parameter_type = declaration["type"]
    record_set_types = {"list_record_ref", "mapping_string_to_record_ref", "mapping_string_to_record_ref_list"}
    input_field_types = {"input_field_binding", "list_input_field_binding"}
    expected_kind = (
        "record_ref" if parameter_type == "record_ref"
        else "record_ref_set" if parameter_type in record_set_types
        else "input_field" if parameter_type in input_field_types
        else "literal"
    )
    if binding.value_kind != expected_kind:
        _rule_error(f"parameter {binding.parameter_id} value_kind must be {expected_kind}")
    value = binding.value
    if parameter_type == "record_ref":
        _validate_record_ref(value, binding.parameter_id)
    elif parameter_type == "list_record_ref":
        if not isinstance(value, (list, tuple)):
            _rule_error(f"parameter {binding.parameter_id} requires a RecordRef list")
        for item in value:
            _validate_record_ref(item, binding.parameter_id)
    elif parameter_type == "mapping_string_to_record_ref":
        if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
            _rule_error(f"parameter {binding.parameter_id} requires a string-to-RecordRef mapping")
        for item in value.values():
            _validate_record_ref(item, binding.parameter_id)
    elif parameter_type == "mapping_string_to_record_ref_list":
        if not isinstance(value, dict) or not all(isinstance(key, str) and isinstance(items, (list, tuple)) for key, items in value.items()):
            _rule_error(f"parameter {binding.parameter_id} requires a string-to-RecordRef-list mapping")
        for items in value.values():
            for item in items:
                _validate_record_ref(item, binding.parameter_id)
    elif parameter_type == "input_field_binding":
        _validate_input_field(value, binding.parameter_id, role_ids)
    elif parameter_type == "list_input_field_binding":
        if not isinstance(value, (list, tuple)):
            _rule_error(f"parameter {binding.parameter_id} requires InputFieldBindings")
        for item in value:
            _validate_input_field(item, binding.parameter_id, role_ids)
    elif parameter_type in {"enum", "enum_set"}:
        values = declaration["values"]
        candidates = value if parameter_type == "enum_set" else (value,)
        if parameter_type == "enum_set" and (not isinstance(value, (list, tuple)) or len(value) != len(set(value))):
            _rule_error(f"parameter {binding.parameter_id} requires a duplicate-free enum set")
        if any(candidate not in values for candidate in candidates):
            _rule_error(f"parameter {binding.parameter_id} contains a value outside its closed enum")
    elif parameter_type == "string_set":
        if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value) or len(value) != len(set(value)):
            _rule_error(f"parameter {binding.parameter_id} requires a duplicate-free string set")
    elif parameter_type in {"string", "json_pointer", "closed_event_type_id"}:
        if not isinstance(value, str):
            _rule_error(f"parameter {binding.parameter_id} requires a string")
        if parameter_type == "json_pointer" and not value.startswith("/"):
            _rule_error(f"parameter {binding.parameter_id} requires a JSON pointer")
        if parameter_type == "closed_event_type_id" and value not in MANIFEST["closed_event_type_ids"]:
            _rule_error(f"parameter {binding.parameter_id} is not a closed event type")
    elif parameter_type == "nullable_normalized_decimal_string":
        if value is not None and (not isinstance(value, str) or not re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", value)):
            _rule_error(f"parameter {binding.parameter_id} requires a normalized decimal string or null")


def validate_executable_rule(payload: BaseModel) -> None:
    """Validate one rule record against the closed manifest signature."""

    implementation_id = getattr(payload, "implementation_id", None)
    declaration = MANIFEST["closed_rule_implementations"].get(implementation_id)
    if declaration is None:
        _rule_error(f"unknown implementation_id {implementation_id}")
    if payload.rule_kind != declaration["kind"]:
        _rule_error(f"{implementation_id} kind must be {declaration['kind']}")
    if payload.implementation_version != declaration["version"]:
        _rule_error(f"{implementation_id} version must be {declaration['version']}")

    role_specs = {spec.role_id: spec for spec in payload.input_role_specs}
    if len(role_specs) != len(payload.input_role_specs):
        _rule_error("input_role_specs contains duplicate role IDs")
    declared_roles = declaration["input_roles"]
    if set(role_specs) != set(declared_roles):
        _rule_error("input role IDs differ from the declared signature")
    for role_id, role_declaration in declared_roles.items():
        spec = role_specs[role_id]
        if spec.cardinality != role_declaration["cardinality"]:
            _rule_error(f"input role {role_id} cardinality drift")
        actual_schemas = {(item.schema_id, item.schema_version) for item in spec.accepted_schema_refs}
        expected_schemas = {(item["schema_id"], item["schema_version"]) for item in role_declaration["accepted_schema_refs"]}
        if len(actual_schemas) != len(spec.accepted_schema_refs) or actual_schemas != expected_schemas:
            _rule_error(f"input role {role_id} schema drift")

    bindings = {binding.parameter_id: binding for binding in payload.parameters}
    if len(bindings) != len(payload.parameters):
        _rule_error("parameters contains duplicate parameter IDs")
    parameter_declarations = declaration["parameters"]
    required = {name for name, spec in parameter_declarations.items() if spec.get("required", True)}
    if not required.issubset(bindings):
        _rule_error(f"missing required parameters: {sorted(required - set(bindings))}")
    if not set(bindings).issubset(parameter_declarations):
        _rule_error(f"undeclared parameters: {sorted(set(bindings) - set(parameter_declarations))}")
    for parameter_id, binding in bindings.items():
        _validate_rule_parameter(binding, parameter_declarations[parameter_id], set(role_specs))

    try:
        output_ref = SchemaRef.model_validate(payload.output_schema_ref)
    except (TypeError, ValueError) as exc:
        _rule_error(f"{implementation_id} output schema is invalid: {exc}")
    output = (output_ref.schema_id, output_ref.schema_version)
    expected_outputs = {(item["schema_id"], item["schema_version"]) for item in declaration["output_schema_refs"]}
    if output not in expected_outputs:
        _rule_error(f"{implementation_id} output schema drift")


def validate_rule_registry_manifest() -> None:
    """Prove the manifest and static callable registry are a closed, hash-pinned set."""

    from .rules import RULE_IMPLEMENTATIONS, implementation_code_hash

    declarations = MANIFEST["closed_rule_implementations"]
    if set(RULE_IMPLEMENTATIONS) != set(declarations):
        raise ContractError("SCHEMA_EXECUTABLE_RULE_INVALID", "callable registry differs from manifest inventory")
    for implementation_id, declaration in declarations.items():
        expected_hash = declaration["code_artifact_hash"]
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise ContractError("SCHEMA_EXECUTABLE_RULE_INVALID", f"{implementation_id} has no immutable code hash")
        if implementation_code_hash(implementation_id) != expected_hash:
            raise ContractError("SCHEMA_EXECUTABLE_RULE_INVALID", f"{implementation_id} code-artifact hash drift")


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


def _normalize_set_path(value: Any, parts: list[str]) -> None:
    if not parts:
        if isinstance(value, list):
            value.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
        return
    head, *tail = parts
    if head == "*" and isinstance(value, list):
        for item in value:
            _normalize_set_path(item, tail)
    elif isinstance(value, dict) and head in value:
        _normalize_set_path(value[head], tail)


def canonical_bytes(meta: RecordMeta, payload: BaseModel) -> bytes:
    meta_value = _canonical(meta)
    meta_value["source_refs"] = sorted(meta_value["source_refs"], key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    payload_value = _canonical(payload)
    spec = MANIFEST["payload_kinds"][payload.__class__.__name__]
    paths = sorted(spec.get("set_semantics_paths", []), key=lambda path: path.count("/"), reverse=True)
    for path in paths:
        _normalize_set_path(payload_value, path.strip("/").split("/"))
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
        if self.payload.__class__.__name__ == "ExecutableRule":
            validate_executable_rule(self.payload)
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

    def _validate_reference_targets(self, record: StoredRecord) -> None:
        source_kind = record.payload.__class__.__name__
        spec = MANIFEST["payload_kinds"][source_kind]
        overrides = spec.get("reference_targets", {})
        roles = MANIFEST["reference_target_roles"]
        for field_name in _reference_field_names(spec):
            allowed_kinds = overrides.get(field_name, roles[field_name])
            if allowed_kinds == "any":
                continue
            value = getattr(record.payload, field_name)
            for ref in self._refs(value):
                target = self.resolve(ref)
                target_kind = target.payload.__class__.__name__
                if target_kind not in allowed_kinds:
                    raise ContractError(
                        "SCHEMA_REFERENCE_TARGET_INVALID",
                        f"{source_kind}.{field_name} permits {allowed_kinds}, not {target_kind} at {ref.object_id}@{ref.object_version}",
                    )
                target_spec = MANIFEST["payload_kinds"][target_kind]
                schemas = target_spec.get("schema_variants", [target_spec.get("schema")])
                allowed_schemas = {(schema["schema_id"], schema["schema_version"]) for schema in schemas if schema}
                if (target.meta.schema_id, target.meta.schema_version) not in allowed_schemas:
                    raise ContractError(
                        "SCHEMA_REFERENCE_TARGET_INVALID",
                        f"{source_kind}.{field_name} resolved to an invalid {target_kind} schema",
                    )

    def validate_closure(self) -> None:
        edges: dict[tuple[str, int], set[tuple[str, int]]] = {}
        for key, record in self._records.items():
            refs = set(record.meta.source_refs) | set(self._refs(record.payload))
            edge_keys = {(ref.object_id, ref.object_version) for ref in refs}
            for ref in refs:
                self.resolve(ref)
            self._validate_reference_targets(record)
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

    def reference_target_receipt(self) -> dict[str, int | str]:
        typed_target_refs = 0
        polymorphic_refs = 0
        records_with_typed_targets = 0
        for record in self._records.values():
            source_kind = record.payload.__class__.__name__
            spec = MANIFEST["payload_kinds"][source_kind]
            overrides = spec.get("reference_targets", {})
            record_typed_refs = 0
            for field_name in _reference_field_names(spec):
                declaration = overrides.get(field_name, MANIFEST["reference_target_roles"][field_name])
                ref_count = len(self._refs(getattr(record.payload, field_name)))
                if declaration == "any":
                    polymorphic_refs += ref_count
                else:
                    typed_target_refs += ref_count
                    record_typed_refs += ref_count
            if record_typed_refs:
                records_with_typed_targets += 1
        return {
            "status": "valid",
            "declared_reference_fields": sum(
                len(_reference_field_names(spec)) for spec in MANIFEST["payload_kinds"].values()
            ),
            "reference_target_roles": len(MANIFEST["reference_target_roles"]),
            "explicit_polymorphic_roles": sum(
                declaration == "any" for declaration in MANIFEST["reference_target_roles"].values()
            ),
            "typed_target_refs_validated": typed_target_refs,
            "polymorphic_refs_resolved": polymorphic_refs,
            "records_with_typed_targets": records_with_typed_targets,
        }

    def records(self) -> tuple[StoredRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))


validate_model_manifest_inventory()
validate_rule_registry_manifest()
