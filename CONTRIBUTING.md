# Contributing

Keep this skill self-contained. Add depth to the relevant reference rather than
requiring another agent-skill catalog. Core instructions belong in `SKILL.md`;
conditional technical detail belongs in `references/` and reviewable project
artifacts in `templates/`.

Source normative claims from the standards owner or licensed text available to the
reviewer; do not commit licensed text. Source implementation behavior from exact
manufacturer/project versions. Label community interpretation and proposed designs.
Update the research date only for sources actually revisited.

Run offline checks before a pull request:

```sh
python3 scripts/validate_skill.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The validator checks this repository's restricted frontmatter shape, local links,
reference size and eval contract. It is not a full Agent Skills conformance tool.
Keep the skill below 500 lines and 5,000 tokens. Scripts require only Python 3.10+.
Never add hardware/network effects to the offline inspector.

`evals/evals.json` uses a local v1 output-quality contract: top-level
`schema_version`, `skill_name`, and `evals`; each case has a stable `id`, realistic
`prompt`, case-level `expected_output` and separately checkable `assertions`.
Preserve IDs when revising rubrics. Include satisfying, contradictory and missing
examples in `evals/rubric-review.md`. Trigger probes live separately. Structural
validation and authored rubric examples are not evidence that an agent passed the
cases; report any future model runs with model/revision/output provenance and
independent review limits. No hosted provider calls are part of CI.

Use synthetic or explicitly authorized/redacted captures. Do not commit vessel
locations, MMSIs, serials or credentials. Document any redaction that changes
checksums, identity or timing. Add regression tests for script behavior and report
unperformed hardware tests as not tested.
