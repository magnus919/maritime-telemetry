# Radar and adjacent protocol decision guide

## Radar support is a model/version question

The retrieved [radar_pi upstream README](https://github.com/opencpn-radar-pi/radar_pi)
(2026-10-16) lists the following support families. These are maintainer claims,
not hardware tests in this repository; freeze the plugin release and consult its
model-specific instructions before purchase or connection.

| Family | README-listed status | What to resolve on the target |
|---|---|---|
| Garmin HD / xHD | Listed | Exact scanner/firmware, interface and plugin build |
| Navico BR24 / 3G / 4G | Listed | Interface addressing and selected scanner |
| Navico HALO 20, 20+, 24, 4, 6, 8 | Listed | Model-specific networking and control support |
| Raymarine, including Quantum Q24C/Q24D | Some models listed | Exact model; not all Raymarine scanners |
| Garmin xHD2 / Fantom; Furuno; unlisted models | README explicitly excludes these families | Do not infer compatibility from Ethernet alone |

Keep imagery transport, scanner commands and target reports separate. AIS targets
come from radio reports, not radar returns. A display labeled “AIS radar” can be a
polar target view without any radar scanner. N2K telemetry may supply heading for
overlay but does not make the radar imagery an N2K stream.

## Overlay diagnostic sequence

First establish scanner connectivity using the documented network interface and
multicast/broadcast requirements. Record adapter/IP/route, competing VPNs/firewalls,
and packet counters without changing several variables at once. Then establish
own-ship position and heading source, true/magnetic reference, age and update rate.
Finally inspect antenna alignment, installation offsets and display/plugin settings.
Compare a fixed known feature at the dock before interpreting a moving-target
misalignment as a protocol fault. No numerical alignment tolerance is universal;
use the scanner manual and intended use. Avoid enabling transmission or scanner
control while doing read-only network research.

## Adjacent families: route by actual interface

| Interface named by user | First decision | Boundary |
|---|---|---|
| J1939 engine bus | Exact engine/gateway manuals, speed, PGNs/SPNs and allowed direction | Shared CAN ancestry does not authorize connecting raw buses |
| SeaTalk1 | Determine electrical/signaling contract and supported converter | Not interchangeable with an N2K connector |
| SeaTalkng | Verify adapter wiring, power and supported device semantics | Connector adaptation alone does not prove every feature |
| IEC 61162 IP variants | Identify exact part/edition/profile and target implementation | UDP carrying sentence text is not automatically conformance |
| NMEA OneNet | Owner specification plus exact certified device/gateway support | Separate Ethernet-oriented architecture; not Signal K or arbitrary radar IP |
| DSC/AIS messages | Exact radio output profile, consumer support and validity | Receiving decoded data is separate from RF transmission/approval |

These are triage routes, not newly implemented protocol support. The OneNet owner
page could not be retrieved in this execution pass; retain the existing owner link
and unresolved normative dependency. No autopilot, proprietary radar, J1939 or
SeaTalk command mapping was invented to fill a table.
