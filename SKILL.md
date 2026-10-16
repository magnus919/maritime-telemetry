---
name: maritime-telemetry
description: >-
  Design, build, decode, bridge, and troubleshoot open maritime telemetry and device interoperability
  using NMEA 0183 and NMEA 2000 (N2K). Use for DIY boat sensors, actuators,
  chartplotter telemetry, AIS sentence handling, CAN PGNs, marine gateways,
  and Raspberry Pi or ESP32 integration with commercial instruments through
  Signal K, CANboat, or OpenCPN. Do not use for generic automotive CAN,
  standalone electronics or firmware work, radar RF design, or claims of
  NMEA certification without formal evidence.
license: MIT
---

# Maritime telemetry and interoperability

Help a builder turn a sensor reading or software feature into correctly interpreted
information on a particular boat. Own the maritime protocol contract across the
wire, gateway, source selection, display, and control boundary. This is one
maritime interoperability workflow spanning wire protocols, open data models,
decoding tools and chartplotter consumers. CANboat and OpenCPN are software
projects; Signal K specifies an open data model and APIs; NMEA standards are licensed.

## Working contract

- Identify the exact instruments, firmware, interfaces, intended consumer and
  required behavior. “NMEA compatible” is not a sufficient interface contract.
- Start with offline captures, then an isolated bench network, then passive vessel
  observation. A CAN receiver in normal mode may acknowledge frames even when
  the application never calls send. Confirm controller-level listen-only mode.
- Before wiring, powering, flashing, changing network configuration, transmitting,
  or enabling a control bridge: **Confirm the target, scope, and rollback path
  before acting. Read-only discovery may proceed without confirmation.** Existing
  explicit authorization can satisfy this gate; do not ask again for the same scope.
- Distinguish published standard requirements, manufacturer requirements,
  community interpretations, design recommendations, and measurements. Obtain
  licensed standards for normative conformance decisions; do not reproduce them.
- A decoded packet, valid checksum, or visible device name does not prove the
  intended display or actuator works. Name the tested receiver and firmware.
- Keep control disabled until the user authorizes the exact actuator and bounded
  test. Never replay unknown captures into a live boat or bypass an interlock.

## Route by task

Read only the relevant resources:

| Task | Read | Deliver |
|---|---|---|
| Choose architecture or verify a claim | [Sources and authority](references/sources.md) | Evidence-backed scope and uncertainty |
| Serial wiring, sentences, GNSS or AIS | [NMEA 0183](references/nmea0183.md) | Port and sentence contract |
| Backbone design or power fault | [N2K electrical design](references/n2k-electrical.md) | Drawing and electrical budget |
| PGN decoding, identity, transport or publishing | [N2K protocol](references/n2k-protocol.md) | PGN and identity contract |
| Implement N2K directly or inspect library internals | [Pinned source walkthrough](references/nmea2000-source-study.md) | Layered protocol design and independent vectors |
| ESP32 sensor or Raspberry Pi gateway | [Implementation paths](references/implementation.md) | Versioned build and integration plan |
| CANboat captures and decoder workflow | [CANboat](references/canboat.md) | Pinned decode evidence and unknown-field ledger |
| Build a configurable ESP32 instrument display | [Signal K display case study](references/signalk-display-case.md) | Display contract and scoped adaptation plan |
| Signal K data model, APIs and server integration | [Signal K](references/signalk.md) | Source-aware application contract |
| OpenCPN connections, chartplotters and radar | [OpenCPN](references/opencpn.md) | Verified consumer configuration |
| Translation, chartplotters, radar or software UI | [Gateways and applications](references/gateways.md) | Semantic mapping and source policy |
| Digital switching, autopilot or other control | [Actuator boundaries](references/control.md) | Command/state/interlock contract |
| Commissioning or diagnosis | [Acceptance and fault isolation](references/acceptance.md) | Bounded test evidence |

Start a substantial project with [device contract](templates/device-contract.md).
Use [translation matrix](templates/translation-matrix.csv) for bridges and
[commissioning record](templates/commissioning.md) for bench/vessel work.

For a direct implementation, use [protocol worksheet](templates/protocol-implementation.md).
The optional [host encoding probe](examples/heading_oracle.cpp) and
[executed evidence](evidence/nmea2000-heading-study.md) show how to check independent
byte vectors against a pinned upstream implementation without opening a bus.

## Workflow

1. **Discover the actual boundary.** Record connector and pin labels, voltage,
   isolation, port direction and speed, protocol edition where known, supported
   receive/transmit sentences or PGNs, firmware and source-selection behavior.
   Classify feature as observation, publication, configuration, or actuation.
   If manuals are missing, advance the abstract design but stop pin-specific work.
2. **Choose the smallest useful path.** Prefer an isolated existing gateway for a
   first Pi display; an MCU plus a verified transceiver and mature N2K stack for a
   sensor. Do not write a new bus stack merely to publish one measurement.
   Use NMEA 0183 for a required serial consumer and N2K for the shared CAN backbone;
   use Signal K above gateways for application data and provenance.
3. **Freeze the semantic contract.** Specify units, reference frame, invalid values,
   update cadence, timeout, source/instance and consumer support. Never convert
   unavailable values to zero, magnetic heading to true heading without variation,
   or ground speed to water speed. Define loss and ambiguity in every conversion.
4. **Prove offline behavior.** Retain raw data, timestamps, decoder revision and
   expected values. Test invalid/truncated frames, missing fragments, nulls,
   source changes and stale data. Run the bundled inspector for framing checks;
   use a pinned CANboat decoder for payload interpretation.
5. **Verify on the bench.** Check electrical conditions, boot behavior, discovery,
   transmission rate, unit conversions and failure handling with the intended
   consumer. Include power cycles and multiple sensors of the same type.
6. **Commission progressively.** Observe baseline network health, add one device,
   compare physical measurement, decoded message and actual display. Enable only
   the approved publication/control paths. Preserve a physical removal and saved
   configuration rollback route.
7. **Close with evidence.** State implemented, unit-tested, simulated, bench-tested,
   vessel-tested and not assessed separately. Deliver captures and an acceptance
   decision scoped to the tested hardware/firmware, not universal compatibility.

## Offline tool

Run from this skill's directory; Python 3.10+, standard library only:

```sh
python3 scripts/nmea_inspect.py sentence '$GPGLL,4916.45,N,12311.12,W,225444,A,*1D'
python3 scripts/nmea_inspect.py can-id 0x09F11223
python3 scripts/nmea_inspect.py file capture.nmea
python3 scripts/test_nmea_inspect.py
```

The inspector outputs JSON and never opens a bus, serial device or socket. It
checks a deliberately strict checksum-bearing, untagged sentence profile and
extracts CAN identifier fields. It does not decode AIS payloads, reassemble fast
packets, validate navigation truth, or establish standards conformance. See the
0183 and N2K references for limits. Exit 0 = accepted framing, 1 = rejected data,
2 = usage/I/O failure. A file report may contain accepted and rejected records.

## Scope boundaries

This repository is self-contained and has no required companion skills. Use exact
board, component, operating-system and application documentation for implementation.

- For electronics, establish the electrical contract, protection, isolation and
  measurement plan described in the electrical and implementation references.
- For ESP32 work, verify the exact SoC, GPIO restrictions, framework/driver versions,
  build target and recovery path before flashing. Do not generalize board pinouts.
- For Raspberry Pi work, verify board/OS/adapter compatibility and follow the
  implementation reference; preserve configuration and recovery media.
- For application work, carry domain units, source, validity and freshness through
  the backend and UI. Follow the Signal K and gateway security requirements.
- Radar imagery, sonar imagery and chart files are not generic N2K telemetry.
  Verify exact Ethernet/plugin/proprietary support. RF transmitter construction
  and regulatory approval are outside this skill.

## Completion and stop conditions

Complete when the requested design, implementation or diagnosis has a reviewable
artifact and explicit evidence limits. Missing hardware does not block an offline
implementation, but it does block a claimed physical pass. Stop live work on
unexpected actuator movement, bus-off escalation, supply/isolation uncertainty,
loss of primary navigation data, or an unapproved command path. After three
non-converging diagnostic passes, report the ledger and smallest decisive next
measurement rather than trying random PGNs or changing several variables.
