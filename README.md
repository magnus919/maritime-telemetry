# Maritime Telemetry

Build DIY marine devices and software that speak to the instruments on your boat.

## Why Install This Skill

A temperature sensor can send perfectly valid CAN frames and still show nothing
on a chartplotter. Successful integration depends on wiring, device identity,
message semantics, source selection and the receiving instrument's capabilities.
This skill connects those pieces across NMEA 0183, NMEA 2000, CANboat, Signal K and OpenCPN.

Your agent can help design an ESP32 sensor, connect a Raspberry Pi dashboard,
translate legacy serial instruments, investigate missing readings, and plan
bounded actuator tests. It includes researched references and practical acceptance
records, with clear distinctions between a working prototype and certification.

## What You Get

| Contents | Provides |
|---|---|
| `SKILL.md` | Self-contained project and hardware integration workflow |
| `references/` | Focused guides covering protocols, wiring, calibration, software, controls and verification |
| `templates/` | Contracts, power budgets, calibration, capture, control and recovery worksheets |
| `scripts/` | Offline inspector, fault models, engineering calculations and regression tests |
| `examples/`, `evidence/` | C++ protocol probes, two ESP32 builds, AIS mapping lab and scoped historical results |
| `evals/` | Output-quality scenarios and separate trigger/rubric review examples |

## Quick Start

Clone this repository into your agent client's skill directory (this example uses
`~/.agents/skills`; use your client's supported location):

```sh
git clone https://github.com/magnus919/maritime-telemetry.git ~/.agents/skills/maritime-telemetry
cd ~/.agents/skills/maritime-telemetry
```

The repository root is the skill. It has no dependency on other skills.
From that directory, with no hardware or API key:

```sh
python3 scripts/nmea_inspect.py can-id 0x09F11223
```

The JSON reports PGN `127250`, source `35`, priority `2`, and global destination
`255`. This inspects an identifier; it does not interpret a heading measurement.

Try: “Design an ESP32 water-temperature sensor for my N2K chartplotter. Start with
an offline contract and a bench test plan.” Supply the chartplotter model and
firmware when available.

## Triggers

- NMEA 0183 / NMEA 2000 wiring, sentences, PGNs and device discovery
- AIS targets over N2K, Signal K and legacy0183, including identity and stale-data faults
- DIY boat sensors, digital switching and instrument gateways
- Raspberry Pi, Signal K, CANboat and OpenCPN interoperability
- Incorrect units, missing data, duplicate sources or bridge loops

## Requirements

Python 3.10+ for the bundled offline tool; no third-party packages. Hardware work
needs the actual device manuals and suitable isolated interfaces. Firmware and
application dependencies vary by project. Formal conformance requires the relevant
licensed standards and certification process; this package supplies neither.

## Research and validation

See the [source register](references/sources.md) for the standards-owner,
manufacturer and open-source project references, and [contributing guide](CONTRIBUTING.md)
for offline checks. The authored evaluation scenarios are not claimed
model-run results. Hardware interoperability and formal certification remain
project-specific tests.

The [executed research report](research/runs/fortification.md) links the new recipes,
source decisions and remaining equipment-dependent tests. Start the dependency-free
lab with `python3 scripts/telemetry_lab.py`; it reports a fresh value and then its
stale state without opening any device or network connection.

For AIS projects, start with [AIS over NMEA 2000](references/ais-nmea2000.md) and its
[reproducible lab](references/ais-n2k-laboratory.md), including measured translation limits.

## Community and license

New contributors are welcome. Start with [Contributing](CONTRIBUTING.md); project
participation follows our [Code of Conduct](CODE_OF_CONDUCT.md). Use the
[issue forms](https://github.com/magnus919/maritime-telemetry/issues/new/choose) for
bugs, ideas or evidence corrections, and [Security](SECURITY.md) for private
vulnerability reports. Agent contributors should read [AGENTS.md](AGENTS.md).
Original repository content is available under the [MIT License](LICENSE).

The former [full-server lab](examples/signalk-lab/README.md) is quarantined while
upstream dependency advisories remain. The [AIS mapping lab](references/ais-n2k-laboratory.md)
remains runnable and CI-tested. Code PRs require relevant docs/tests, passing
integration checks and at least 85% combined Python coverage.
