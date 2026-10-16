# Case study: a configurable ESP32 Signal K instrument display

## Provenance and evidence limits

Source: Boating with the Baileys, [DIY ESP32 Marine MFD — Square Multifunction Boat
Display using SignalK Data](https://www.youtube.com/watch?v=FAPvdz6oN7A).
Retrieved English transcript and description through GroktoCrawl on 2026-10-16;
this review did not visually inspect the video. Chapter markers supplied by the
author: 00:00 introduction, 02:45 display options, 07:20 configuration, 19:18 future
work. They are chapter references, not precise timestamps for every claim below.

Inspected the linked [Marine-Displays repository at commit
b3c440a932a624496e4da7f0adb17bcec51796aa](https://github.com/Boatingwiththebaileys/Marine-Displays/tree/b3c440a932a624496e4da7f0adb17bcec51796aa).
No firmware build, flash, electrical measurement or display test was performed.
Upstream code and artwork are not copied here. No project-wide license file was
found in the inspected checkout; bundled dependency licenses do not establish a
license for the author's application/artwork. Resolve reuse terms before vendoring
or distributing those materials. This guide is original analysis with attribution.

## The practical pattern

```text
boat instruments / DIY sensors
    → supported gateway or Signal K producer
    → Signal K server
    → Wi-Fi WebSocket values + REST metadata
    → ESP32-S3 / LVGL display
```

The video's core idea is a reusable instrument face: select paths and presentation
through a web UI instead of rebuilding the firmware for every measurement. The
transcript describes single/dual/quad numbers, gauges with a center value, and
one/two-series graphs. Labels and units come from Signal K metadata; presentation
converts SI values into selected display units. A configurable face can therefore
serve different stations while retaining the same data client.

This is an instrument repeater/application pattern. A Wi-Fi Signal K consumer does
not itself become an N2K node or a full chartplotter merely because it has a screen.

## Separate video-time features from current source

| Evidence | Supported conclusion | Limit |
|---|---|---|
| Video transcript | Configurable displays and metadata are described; buzzer coverage was incomplete at recording; CAN and control additions were discussed as future work | Do not present every proposed feature as demonstrated |
| Current square-display README | Additional navigation, position/time and AIS views are listed | Author documentation, not independently tested features |
| Separate `ESP32-S3_Square_Display-NMEA` folder/README at the pinned commit | A direct N2K variant now exists | Its advertised field count and wiring recipe are not verified interoperability or electrical certification |
| Manufacturer [board wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-4), retrieved through GroktoCrawl | Board-specific display/TWAI examples and configuration requirements exist | Match exact revision and schematic; example CAN support alone proves no N2K compatibility |

The transcript describes 7–36 V input and direct battery power. That claim was not
independently established for every board revision in this review. Do not generalize
it to USB, GPIO or backbone supply terminals. Use the electrical guide and exact
schematic to resolve voltage, fusing, transients, ground/isolation and termination.
Do not turn upstream shorthand about connecting CAN H/L into a complete boat wiring
instruction. An AIS target screen is also distinct from radar imagery.

## Source walkthrough and adaptation questions

Paths below are relative to the pinned upstream checkout, chiefly
`ESP32-S3_Square_Display/`. Read their exact revision before adapting.

| File / symbols | Inspected behavior | Reusable lesson / verification needed |
|---|---|---|
| `src/signalk_config.cpp`: `ws_begin_connection`, `wsEvent` | Opens `/signalk/v1/stream?subscribe=none`, then requests paths; metadata is fetched via REST on connection | Separate stream and metadata lifecycles; verify endpoint discovery, authentication and reconnect |
| Same: `get_active_screen_paths`, `subscribe_to_active_screen` | Collects active-screen paths plus background graph paths; deduplicates and replaces subscriptions | Bound traffic without starving graph history; test page switching and server subscription support |
| Same: `wsEvent` value loop | Special-cases position objects and datetime strings; other values use `as<float>()`; inspected loop does not retain update source/timestamp | Add explicit type/null/validity handling and per-path provenance/freshness tests; do not infer correctness from a moving number |
| Same: `pause_signalk_ws`, `resume_signalk_ws` | Intentionally pauses the stream around configuration UI memory pressure and defers reconnection | Configuration activity can interrupt telemetry; show stale state and measure recovery rather than hiding it |
| `src/unit_convert.cpp`: `convert_unit`, `infer_unit_from_path` | Central conversions and fallback unit inference from path substrings | Prefer schema/metadata or an explicit custom-path contract; ambiguous custom paths should not silently acquire guessed units |
| `platformio.ini` | Selects square-board settings and LVGL; some dependencies use ranges or no version pin | Pin resolved dependencies and board revision for reproduction; inspect pre-build scripts before executing |

These are source observations and test questions, not an exhaustive upstream bug or
security audit. In particular, a connection heartbeat is not proof that each sensor
is fresh. A null-to-float conversion needs an explicit fixture against the selected
JSON library before claiming its exact runtime result.

## Worked adaptation: wind repeater

Use the [display worksheet](../templates/display-contract.md). First implement a
read-only page with two explicit inputs:

| Role | Signal K path | Stored units | Display |
|---|---|---|---|
| Numeric apparent wind speed | `environment.wind.speedApparent` | m/s | knots, converted once using × 3600 / 1852 |
| Apparent wind angle needle | `environment.wind.angleApparent` | radians | degrees with a declared wrap/orientation convention |

For a synthetic input of 5.144444444 m/s and π/2 radians, expect approximately
10.0 kn and 90°. This is an independently calculated example, **not an executed
firmware test**. Label it apparent wind; selecting a true-wind path does not compute
true wind or establish that its upstream inputs are valid.

Keep a sample record with value/type, source, measurement time, arrival monotonic
time, validity and metadata. Choose expiry from actual producer cadence and display
purpose. For a bench fixture publishing at 1 Hz, a provisional 3-second timeout is
a test assumption, not a marine standard. A graph should show gaps for missing
samples; don't draw a flat line that implies continued measurement.

Acceptance cases before claiming the adaptation works:

1. Nominal/fractional values and unit conversions agree with independent expectations.
2. Null, wrong JSON type, absent metadata and unsupported path produce explicit
   unavailable/unknown state, not measured zero or guessed navigation meaning.
3. One sensor stops while other paths and WebSocket heartbeats continue: only that
   sensor expires. Replayed old timestamps do not make old data fresh.
4. Source change is visible or handled by a declared server/client selection policy.
5. Screen switching, graph background collection, long graph windows and a burst of
   deltas stay within measured memory/render/network budgets.
6. Wi-Fi loss, server restart and configuration-page pauses show disconnected/stale
   state; reconnect restores subscriptions and metadata without stale alarm bursts.
7. Day/night readability, glove/touch operation, alarm audibility, enclosure and
   physical power behavior are assessed on actual hardware separately from software.

## Extrapolate deliberately

| New use case | Reuse | Additional contract |
|---|---|---|
| Engine station | Numbers, gauges, graph and metadata | Engine instance, temperature/RPM units, sensor faults and alarm thresholds |
| Battery/energy panel | Quad layout and history | Bank identity, current sign, voltage/current versus estimated state of charge |
| Tank/depth repeater | Configurable numeric display | Tank calibration or transducer/keel/surface reference; missing values stay missing |
| Cabin environment | Small configurable instrument faces | Custom-path units, sensor calibration and independent per-path expiry |
| Anchor-watch display | Position/time presentation | GNSS quality/age, antenna position, geodesic distance and alarm failure policy |
| Switching/autopilot UI | Display and configuration mechanics only | Separate authorized command channel, interlocks, expiry and independent feedback |

Do not infer actuator support from a configurable button or a video roadmap. Start
with the controls guide and a simulator for command-capable adaptations.

## Research follow-through

Use this as a concrete case in campaign R06 (Signal K client semantics), R09 (ESP32
build), R11 (end-to-end recipe), R12 (domain meaning), R14 (provisioning/security)
and R16 (agent-output tests). It adds an **ESP32 consumer** alongside the planned
ESP32 sensor producer. The first experiment should be an offline/local synthetic
stream and compile-only build, then authorized bench work on the exact board.
Freeze firmware dependencies and resolve reuse terms before turning the upstream
project into a redistributed starter kit. This case study does not close those runs.
