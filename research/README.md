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

**Completed:** repository audit, bounded source reconnaissance and campaign design.
**Not completed:** R01–R16, new integrations, hardware tests or agent-output evaluation.
The current validator and all 17 Python tests passed during this audit. Their result
establishes the existing test scope, not end-to-end interoperability.

Start with R01/R02 and R16's evaluation design. Build the offline pipeline before
adding devices; then deliver the three tested recipes described in R11. Keep
hardware compatibility and normative-standard dependencies visible when unavailable.
This directory is maintainer planning material, not a runtime dependency of the skill.
