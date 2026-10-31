"""Validate that the simulation study plan is complete and execution-ready.

This validator checks planning contracts only. Passing it does not imply that the
simulator, pilot, confirmatory study, or manuscript has been completed.
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

PLAN_FILES = {
    "README.md",
    "AGENTS.md",
    "docs/STUDY_PLAN.md",
    "docs/PREREGISTRATION.md",
    "docs/ARTICLE_OUTLINE.md",
    "docs/CONFIGURATION_COMPILATION.md",
    "docs/DEFERRED.md",
    "docs/EXECUTION_LEDGER.md",
    "docs/PLAN_COMPLETION_RECEIPT.md",
}


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(text: str, needles: tuple[str, ...], owner: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise ValueError(f"{owner} is missing required contracts: {missing}")


def slice_blocks(plan: str) -> dict[int, str]:
    matches = list(
        re.finditer(r"^### (?:Optional )?Slice (\d+):", plan, flags=re.MULTILINE)
    )
    blocks: dict[int, str] = {}
    for index, match in enumerate(matches):
        slice_id = int(match.group(1))
        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            following = re.search(r"^## ", plan[match.end() :], flags=re.MULTILINE)
            end = match.end() + following.start() if following else len(plan)
        blocks[slice_id] = plan[match.start() : end]
    return blocks


def validate_slice_contracts(plan: str) -> None:
    blocks = slice_blocks(plan)
    if set(blocks) != set(range(8)):
        raise ValueError(f"expected Slices 0-7 exactly; found {sorted(blocks)}")

    common_labels = (
        "**Purpose:**",
        "**Owns:**",
        "**Forbidden:**",
        "**Done when:**",
        "**Commit required:**",
    )
    for slice_id, block in blocks.items():
        require(block, common_labels, f"Slice {slice_id}")
        if not re.search(
            r"\*\*(?:Verification|Verification and execution):\*\*", block
        ):
            raise ValueError(f"Slice {slice_id} lacks an explicit verification block")
        if "```bash" not in block:
            raise ValueError(f"Slice {slice_id} lacks an executable command")

    for slice_id in range(7):
        if f"| {slice_id} |" not in plan:
            raise ValueError(f"Slice {slice_id} missing from file/mutation contract")
    if "| 7 |" not in plan:
        raise ValueError("optional Slice 7 missing from file/mutation contract")


def validate_word_budget(plan: str, outline: str) -> None:
    required_rows = {
        "Introduction and contribution": 700,
        "Mechanism, literature, and originality": 800,
        "Formal model and propositions": 1250,
        "Robodebt case and process mapping": 1100,
        "Dynamic simulation methods": 1200,
        "Results": 1850,
        "Practical protocol and governance implications": 1750,
        "Limitations and conclusion": 750,
    }
    for label, words in required_rows.items():
        pattern = rf"\| {re.escape(label)} \| {words:,} \|"
        if not re.search(pattern, plan):
            raise ValueError(f"study plan word-budget row missing: {label}={words}")
    if sum(required_rows.values()) != 9400:
        raise AssertionError("internal word-budget arithmetic error")
    require(
        plan,
        ("**Drafting subtotal** | **9,400**", "**Unallocated contingency** | **600**", "**Submission ceiling** | **10,000**"),
        "study plan word budget",
    )
    require(
        outline,
        ("9,400", "600-word", "10,000"),
        "article outline word budget",
    )


def validate_completion_audit(plan: str) -> None:
    audit_start = plan.index("## Final Completion Audit")
    questions = [
        int(number)
        for number in re.findall(
            r"^(\d+)\. ", plan[audit_start:], flags=re.MULTILINE
        )
    ]
    if questions != list(range(1, 40)):
        raise ValueError(f"final audit must contain questions 1-39; found {questions}")


def validate_preregistration(prereg: str) -> None:
    require(
        prereg,
        (
            "H1",
            "H2",
            "H3",
            "U0",
            "U1",
            "U2C",
            "U2O",
            "U3",
            "maximum no greater than 100 per family",
            "family-wide extension rule",
            "no pilot or confirmatory results inspected",
        ),
        "preregistration",
    )


def validate_deferred_register(deferred: str) -> None:
    ids = re.findall(r"^\| (D-\d{3}) \|", deferred, flags=re.MULTILINE)
    expected = [f"D-{number:03d}" for number in range(1, 10)]
    if ids != expected:
        raise ValueError(f"deferred register must contain ordered D-001..D-009: {ids}")
    for row in deferred.splitlines():
        if re.match(r"^\| D-\d{3} \|", row) and row.count("|") != 9:
            raise ValueError(f"malformed deferred-register row: {row}")


def validate_no_placeholders() -> None:
    marker = re.compile(r"\b(?:TBD|FIXME)\b|<fill(?:-| )?in>", re.IGNORECASE)
    for relative in PLAN_FILES:
        match = marker.search(read(relative))
        if match:
            raise ValueError(f"unresolved placeholder in {relative}: {match.group(0)}")


def main() -> None:
    missing = sorted(relative for relative in PLAN_FILES if not (ROOT / relative).is_file())
    if missing:
        raise ValueError(f"required planning files missing: {missing}")

    plan = read("docs/STUDY_PLAN.md")
    prereg = read("docs/PREREGISTRATION.md")
    outline = read("docs/ARTICLE_OUTLINE.md")
    deferred = read("docs/DEFERRED.md")
    ledger = read("docs/EXECUTION_LEDGER.md")
    readme = read("README.md")

    validate_slice_contracts(plan)
    validate_word_budget(plan, outline)
    validate_completion_audit(plan)
    validate_preregistration(prereg)
    validate_deferred_register(deferred)
    validate_no_placeholders()

    require(
        plan,
        (
            "The plan is complete when",
            "That does **not** mean the study is complete",
            "Slice file and mutation contract",
            "Runtime and escalation budget",
            "Environment and baseline entry gate",
            "diagnostic_id",
            "python3 scripts/validate_plan.py",
            "reconcile experiments/configs/confirmatory_v1.yaml",
            "evidence-packet experiments/configs/confirmatory_v1.yaml",
            "no greater than 24 wall-clock hours",
            "D-007",
            "generic latent-state and administrative-access attribute references",
        ),
        "study plan",
    )
    if "Verify this date" in plan:
        raise ValueError("venue date remains an unresolved prose instruction")
    if "`(schema_id = case, schema_version = 1)`: latent income" in plan:
        raise ValueError("case-specific field leaked into the kernel case contract")

    require(
        ledger,
        ("Plan-completeness audit", "python3 scripts/validate_plan.py"),
        "execution ledger",
    )
    require(
        readme,
        ("plan is execution-ready", "does not mean the study is complete"),
        "README status",
    )

    print(
        "PLAN_VALID slices=8 primary_hypotheses=3 policies=5 "
        "audit_questions=39 deferred_items=9 word_ceiling=10000"
    )


if __name__ == "__main__":
    main()
