#!/usr/bin/env python3
"""Dependency-free repository checks; not a general Agent Skills validator."""

import json
import re
import sys
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors = []
    required = [
        "SKILL.md",
        "README.md",
        "LICENSE",
        "evals/evals.json",
        "evals/trigger-cases.json",
        "evals/rubric-review.md",
    ]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"missing {name}")
    if errors:
        return errors
    skill = (root / "SKILL.md").read_text()
    match = re.match(
        r"\A---\nname: maritime-telemetry\ndescription: >-\n((?:  .+\n)+)license: MIT\n---\n",
        skill,
    )
    if not match:
        errors.append(
            "frontmatter differs from this repository's supported name/description/license shape"
        )
    else:
        description = " ".join(line.strip() for line in match[1].splitlines())
        if (
            len(description) > 1024
            or not description.startswith("Design,")
            or "Do not use" not in description
        ):
            errors.append("invalid description length or trigger boundaries")
    if len(skill.splitlines()) >= 500:
        errors.append("SKILL.md exceeds line budget")
    for path in root.rglob("*.md"):
        if set(path.relative_to(root).parts) & {".git", "node_modules", ".pio", ".venv", "__pycache__"}:
            continue
        content = path.read_text()
        if path.parent.name == "references" and len(content) > 60000:
            errors.append(f"oversized reference {path.name}")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not (path.parent / target).exists():
                errors.append(f"broken local link in {path.name}: {target}")
    readme = (root / "README.md").read_text()
    for heading in [
        "Why Install This Skill",
        "What You Get",
        "Quick Start",
        "Triggers",
        "Requirements",
    ]:
        if f"## {heading}" not in readme:
            errors.append(f"missing README section {heading}")
    try:
        manifest = json.loads((root / "evals/evals.json").read_text())
        if not isinstance(manifest, dict):
            errors.append("manifest must be an object")
            return errors
        if set(manifest) != {"schema_version", "skill_name", "evals"}:
            errors.append("unexpected manifest fields")
        if (
            type(manifest.get("schema_version")) is not int
            or manifest.get("schema_version") != 1
            or manifest.get("skill_name") != "maritime-telemetry"
        ):
            errors.append("wrong manifest version or skill name")
        cases = manifest.get("evals", [])
        if not isinstance(cases, list) or len(cases) < 5:
            errors.append("at least five eval cases required")
            return errors
        ids = set()
        for case in cases:
            if not isinstance(case, dict) or set(case) != {
                "id",
                "prompt",
                "expected_output",
                "assertions",
            }:
                errors.append("unexpected eval case fields")
                continue
            ident = case["id"]
            if (
                not isinstance(ident, str)
                or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident)
                or len(ident) > 64
            ):
                errors.append("invalid case ID")
                continue
            if ident in ids:
                errors.append("duplicate case ID")
            ids.add(ident)
            for field in ("prompt", "expected_output"):
                if not isinstance(case[field], str) or not case[field].strip():
                    errors.append(f"empty {field}: {ident}")
            assertions = case["assertions"]
            if (
                not isinstance(assertions, list)
                or not assertions
                or any(not isinstance(a, str) or not a.strip() for a in assertions)
            ):
                errors.append(f"invalid assertions: {ident}")
            elif len(set(assertions)) != len(assertions):
                errors.append(f"duplicate assertions: {ident}")
    except (ValueError, TypeError, KeyError) as error:
        errors.append(f"invalid manifest: {error}")
    return errors


if __name__ == "__main__":
    findings = validate(Path(__file__).resolve().parent.parent)
    print(
        json.dumps(
            {
                "passed": not findings,
                "errors": findings,
                "behavioral_quality": "not_assessed",
            },
            indent=2,
        )
    )
    sys.exit(1 if findings else 0)
