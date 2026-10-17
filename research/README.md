# Maritime telemetry research campaign

A plan to turn a careful reference skill into a reproducible maritime
interoperability workbench. Prepared 2026-10-16 against commit
`bb9dfec4fbeb250b7ade07077b4ffa0d69535c16`.

- [Audit](audit.md): strengths, thin areas, weak evidence and template backlog.
- [Campaign](campaign.md): 16 prioritized runs, dependencies, questions, sources,
  deliverables, acceptance criteria and execution bounds.
- [Reconnaissance](reconnaissance.md): four GroktoCrawl searches, eight retrieved
  sources, findings, limitations and unresolved questions.
- [Source ledger](source-ledger.json): query/results metadata and retrieval hashes.
- [Frozen reconnaissance scope](reconnaissance-scope.md).
- [Run worksheet](run-template.md): copy for each actual research run.

## Current execution status

The initial audit/reconnaissance above was a historical17-test snapshot. Subsequent
work delivered runnable protocol and AIS experiments, templates, source claims and
broader regression tests. Use the dated execution ledgers for actual results:

- [Fortification run](runs/fortification.md): software/domain coverage and per-run gates.
- [AIS/N2K run](runs/ais-n2k.md):13 synthetic cases and observed mapping/conversion limits.
- [Dependency remediation](../evidence/dependency-remediation.md): current server-lab
  quarantine and the clean supported mapping lab.

The full R01–R16 campaign remains partial. Physical interoperability, licensed
normative review and independent agent-output evaluation are still uncompleted.
Current CI checks code, coverage and selected software integrations; firmware and
hardware acceptance remain separate evidence. This directory is maintainer material,
not a runtime dependency of the installed skill.

## Concrete case-study input

The [Boating with the Baileys ESP32 display study](../references/signalk-display-case.md)
adds an upstream Signal K consumer example to R06/R09/R11/R12/R14/R16. Transcript
and selected source were inspected; firmware compilation and hardware validation
remain outstanding.
