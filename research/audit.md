# Maritime telemetry skill audit

Date: 2026-10-16. Baseline: `bb9dfec4fbeb250b7ade07077b4ffa0d69535c16`.
Assessment: a useful, unusually careful foundation, but not yet a demonstrated
end-to-end interoperability workbench. The largest improvement is to connect its
advice to versioned, reproducible artifacts and independent observations.

## Evidence and method

Inspected the skill entrypoint, all twelve references, four templates, example,
experiment record, scripts, CI, and evaluation manifests. Re-ran the validator
and Python suite: validation passed; **17 tests passed**. There are **15 authored
output-quality scenarios and 34 assertions**. These are not 15 executed agent
experiments: the validator explicitly reports `behavioral_quality: not_assessed`.
One recorded host experiment covers three heading encodings against pinned
NMEA2000 source. No recorded hardware commissioning or commercial-display tests
were found. See [reconnaissance](reconnaissance.md) for the separately bounded
external source discovery. File sizes below describe coverage, not quality scores.

## What is worth preserving

- Clear distinction between licensed NMEA standards, community decoders, an open
  data model, and applications. No implied certification from library adoption.
- Strong source/units/reference/validity/freshness discipline; explicit boundaries
  around actuation, passive CAN observation and translating unavailable values.
- A pinned NMEA2000 source walkthrough with concrete symbols and three executed
  encoding vectors, including limits on what those experiments establish.
- A self-contained installation, offline standard-library inspector, progressive
  resource loading, and no required companion skills or private infrastructure.

## Gaps ranked by impact

Priority P0 = foundation needed for reliable expansion; P1 = core use cases;
P2 = specialized breadth. These are delivery priorities, not severity claims.

| Area and current evidence | Missing capability / consequence | Priority and research runs |
|---|---|---|
| [Source register](../references/sources.md): useful authority map, mostly moving pages; explicit historical links | Claim-level citations, actual resolved versions, upstream commits, conflict decisions and refresh triggers. A retrieval date does not pin every claim. | P0 R01 |
| [Acceptance](../references/acceptance.md), [experiment](../evidence/nmea2000-heading-study.md) | No reusable capture corpus, fault injector, event timeline or consumer result matrix. Can't reproduce the complete measurement-to-display chain. | P0 R02; P1 R11 |
| [N2K protocol](../references/n2k-protocol.md) and [source study](../references/nmea2000-source-study.md) | Fast-packet loss/interleaving, clock-driven address claims, ISO transport and bounded queues are inspected/advised, not exercised. Only one PGN encoder has host evidence. | P1 R03 |
| [CANboat](../references/canboat.md): 77 lines | No pinned, executed conversion pipeline or cross-decoder comparison; capture dialects, timestamps, C/Rust behavior and incomplete proprietary definitions need explicit tests. | P1 R04 |
| [NMEA 0183](../references/nmea0183.md): 89 lines; strict framing inspector | No streaming chunk tests, semantic parser, AIS multipart corpus, tag-block profile or sentence-to-path worked mappings. A checksum-valid sentence can still be unusable. | P1 R05 |
| [Signal K](../references/signalk.md): 89 lines, illustrative delta | No runnable producer/client/server fixture, authentication lifecycle, subscription/reconnect tests, metadata/notification examples or supported plugin configuration. | P1 R06 |
| [OpenCPN](../references/opencpn.md): 73 lines | No version/OS-specific connection recipe, captured selection/failover behavior, chartplotter acceptance artifact or named adapter compatibility evidence. | P1 R07 |
| [Electrical](../references/n2k-electrical.md): 77 lines | No worked cable/voltage-drop budget, schematic, component datasheet trace or measurement worksheet. Generic grounding advice cannot resolve a real isolation boundary. | P1 R08 |
| [Implementation](../references/implementation.md): 112 lines; pseudocode | No reproducible ESP32/SensESP project or pinned backend build; no current Pi/OpenPlotter service/recovery recipe. Buildability remains unproven. | P1 R09, R10 |
| [Gateways](../references/gateways.md), two-line translation CSV | No tested multi-source arbitration, bridge-loop containment, rate/age queue policy or complete round-trip loss table. | P1 R11 |
| Domain measurement depth dispersed across guides | Calibration, uncertainty, GNSS time/datum, heading/wind references, depth offsets, tank geometry and engine/battery instances need distinct worked cases. | P1 R12 |
| [Controls](../references/control.md): sound boundary, 66 lines | No executable command simulator, failure-state model, feedback contract or named switching/autopilot interoperability profile. | P1 R13, hardware later |
| Security is scattered | No unified trust-boundary diagram, token/permission negative tests, capture redaction method, offline-recovery or retention evidence. | P1 R14 |
| Radar and adjacent protocols are mostly boundaries | Supported scanner/plugin matrix, timing/alignment, AIS versus radar target paths; J1939/SeaTalk/OneNet adapters need targeted decisions, not universal compatibility claims. | P2 R15 |
| [Evals](../evals/evals.json), [rubric](../evals/rubric-review.md), [CI](../.github/workflows/validate.yml) | No actual agent runs, independent adjudication or first-run usability evidence. CI does not execute the optional C++ study or application stack. | P0 design / P1 execution R16 |

## Reference quality, specifically

The source register is responsible about authority but too coarse to answer
“which exact evidence supports this paragraph?” Garmin and Actisense are strong
physical-interface references within their product scope, not proof for every
third-party transceiver or cable. Add component datasheets, exact instrument
receive/transmit lists, and measured electrical conditions for each worked design.

Signal K 1.7.0 is explicitly historical, not falsely labeled latest. The recorded
latest-link ambiguity remains a research question. Resolve schema version, server
version and plugin version independently. OpenPlotter 2.x and Espressif v5.1 links
are orientation material until matched to the actual new build target. OpenCPN
wiki pages need release/platform applicability and stable revisions where available.

The NMEA2000 walkthrough is the strongest implementation reference. Extend its
method to CANboat, Signal K server, SensESP and OpenCPN only for concrete questions.
Avoid source tours that never produce a test or a consumer-facing result. Encoder
and decoder agreement is corroboration, not an independent oracle if both inherit
the same definition. Preserve unresolved proprietary fields as unresolved.

Public NMEA overviews cannot close normative field, timing, certification or
licensing questions. R01 must leave those dependencies visible; neither crawling
more community pages nor passing a simulator closes them.

## Template backlog

Each proposed template has an owning run and must ship with one filled example.
Do not add empty forms merely to increase the file count.

| Proposed artifact | Fields / worked output | Owner |
|---|---|---|
| Source and claim ledger | Claim ID, authority, section/symbol, version/hash, conflict, confidence, evidence level, refresh trigger | R01 |
| Capture manifest | Format/dialect, tool, timestamps/clock basis, raw versus assembled, redactions, license, checksum and expected outcomes | R02 |
| Compatibility matrix | Device/firmware/adapter, supported direction, PGN/sentence/path, selection behavior, test evidence, unknowns | R07/R11 |
| Topology and power worksheet | Connector view, lengths, conductor resistance, feeds, loads, fuse, worst-case drop, isolation paths, measurement points | R08 |
| Reproducible build record | Board/revision, toolchain/backend locks, artifact hashes, pins, compile log, flash/recovery boundaries | R09/R10 |
| Expanded translation matrix | Existing fields plus precision, clock provenance, loss, source failover, backpressure and independent oracle | R11 |
| Calibration record | Sensor/method/reference instrument, raw samples, curve, residuals, uncertainty, fault behavior and maintenance interval | R12 |
| Control state and test contract | Command/state/feedback, authorization, watchdog, interlocks, expiry, replay/idempotency, manual override | R13 |
| Threat model and recovery runbook | Trust boundary, credentials, permissions, offline operation, config backups, restoration and verification | R14 |
| Fault and commissioning ledger | Symptom, layer, hypothesis, one changed variable, observation, stop condition and rollback outcome | R02/R11 |
| Research-run worksheet | Question, bounds, source log, exclusions, claims, tests, unresolved dependencies, promotion decision | Available now: [worksheet](run-template.md) |

## Shape of the desired skill

Keep the entrypoint compact and task-oriented. Add deep references behind routes
for first capture, first sensor, first application, first commercial consumer and
first controlled actuator. Retain a quick useful result without hardware: parse a
known capture and explain source, units, age and limitations. Offer three tested
recipes: offline recorder/application, ESP32 sensor publication, and a Pi gateway
consumed by OpenCPN. Treat radar/control/engine integration as explicit advanced
profiles, not prerequisites for beginners.

“World-class” should mean a reader can reproduce a declared result, diagnose a
failure by layer, and see exactly where evidence stops. It should not mean the
largest PGN list, an unbounded collection of links, or a claim of universal vendor
interoperability. The [campaign](campaign.md) turns these gaps into bounded runs.
