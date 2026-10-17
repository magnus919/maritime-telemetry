# Contributing to Maritime Telemetry

Contributions are welcome from boat owners, developers, electronics builders and
technical writers. A clearer explanation, corrected source, reproducible bug report
or carefully documented hardware result can be as useful as new code. Please follow
our [Code of Conduct](CODE_OF_CONDUCT.md).

## Find a useful starting point

- Report a bug or confusing instruction using the [issue forms](https://github.com/magnus919/maritime-telemetry/issues/new/choose).
- Suggest a use case, worked example or missing interoperability topic.
- Correct a claim with a specific source, version and proposed wording.
- Improve an existing reference, template, fixture or example.

For vulnerabilities, use the private route in [SECURITY.md](SECURITY.md).
Search existing issues and the [research roadmap](research/README.md) first. For a
large change, open an issue to discuss the problem and intended outcome before
investing in an implementation. Small fixes can go straight to a pull request.
You do not need access to a boat, paid API, licensed standards or hardware to help.

## Make your first pull request

1. Fork this repository on GitHub and clone your fork.
2. Create a branch for one focused change.
3. Make the change and run the offline checks below.
4. Push your branch and open a pull request against `main`. Explain the problem,
   resulting behavior and evidence. Link a related issue with `Fixes #N` when the
   change resolves it.
5. Respond to review feedback and keep validation results current after edits.

For example, after cloning your fork:

```sh
cd maritime-telemetry
git switch -c improve-ais-guide
python3 scripts/validate_skill.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The checks require Python 3.10+ and its standard library. Optional C++, Node,
PlatformIO and pyais experiments have separate instructions in their references;
run only the ones relevant to your change. No hosted provider calls are part of CI.
A documentation-only contribution does not need a hardware experiment.

## Keep the skill useful and self-contained

Core instructions belong in `SKILL.md`; focused technical detail belongs in
`references/`, worked project artifacts in `templates/`, and runnable examples in
`examples/`. Add depth to the existing topic before introducing a competing guide.
This repository has no required companion skill catalog or personal infrastructure.

Keep `SKILL.md` below 500 lines and 5,000 tokens. Reference files must stay at or
below 60,000 characters. Preserve relative links and keep the human-facing README
concise. The validator checks this repository's restricted frontmatter shape, local
links, reference size and eval contract; it is not a full Agent Skills conformance tool.

New Python script tests belong in `scripts/test_*.py`. Add meaningful regression
coverage when changing executable behavior. Preserve the dependency-free first run;
never add device, network or subprocess effects to the offline inspector. Keep
optional dependencies explicit and versioned.

## Bring evidence that matches the claim

Source normative claims from the standards owner or licensed text available to the
reviewer; do not commit licensed specifications. Source implementation behavior
from exact manufacturer/project versions. Label community interpretation, proposals
and measurements. Update research dates only for sources actually revisited.

For protocol or interoperability changes, include independent expected values and
reproduction steps where possible. Distinguish simulated, decoded, compiled,
bench-tested and vessel-tested results. Record the actual receiver, firmware and
configuration for hardware observations, plus tests you did not perform. A successful
build or checksum does not establish consumer acceptance or certification.

Use synthetic or explicitly authorized, redacted captures. Remove private vessel
locations, real MMSIs, serial numbers and credentials before posting public issues,
logs or attachments. Synthetic identifiers must be labeled. Document transformations
that change checksums, identity or timing. Review any shared screenshot as well as
its accompanying text.

Do not connect, flash, replay data to or actuate someone else's equipment as part
of reproducing an issue without authorization for that target and scope. Keep the
rollback path and test boundary explicit.

## Evaluation cases

`evals/evals.json` uses a local v1 output-quality contract: top-level
`schema_version`, `skill_name`, and `evals`; each case has a stable `id`, realistic
`prompt`, case-level `expected_output` and separately checkable `assertions`.
Preserve IDs when revising rubrics. Include satisfying, contradictory and missing
examples in `evals/rubric-review.md`. Trigger probes live separately.

Structural validation and authored rubric examples are not evidence that an agent
passed the cases. Report model runs with model/revision/output provenance and
independent review limits. Do not edit a rubric merely to obtain a favorable score.

## Review and licensing

Maintainers review scope, clarity, source quality and applicable checks. Review may
ask for a narrower change or additional evidence; there is no guaranteed response
schedule. A report without a proposed fix is still welcome.

Original contributions are made under this repository's [MIT License](LICENSE).
Only submit material you have the right to contribute. Keep third-party attribution
and license notices, and identify separately licensed dependencies or material.
