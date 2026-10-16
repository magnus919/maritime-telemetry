# Executed software evidence — 2026-10-16

Host: macOS arm64. Baseline skill commit: `3f5903eab4350111299adc593986b59fc23f2ad7`.
All sensor data are original synthetic fixtures. No vessel, CAN adapter, serial
port, actuator, ESP32 upload or public Signal K demo was used.

| Experiment | Observed result | Limits |
|---|---|---|
| NMEA2000 host probe | Independent depth, position, battery and wind byte vectors match; initial address claim, delayed publication and lower-NAME conflict exercised | Fake CAN and controlled clock, not a physical bus or exhaustive transport test |
| CANboat C pipeline | candump converter plus analyzer decodes PGN127250, source35, SID7; `-si` yields heading1 rad, deviation−0.1 rad, variation0.2 rad, True reference | One nominal synthetic frame; no Rust parity or proprietary-field validation |
| pyais3.3.1 | Type1 fixture yields MMSI123456789, lat1, lon−2, speed10kn, course90°, heading90°, second30 | Single-part only; no RF or complete multipart acceptance claim |
| Signal K server2.33.0 / schema1.8.2 | Discovery, schema check, REST value/source/time, explicit WebSocket subscription, unauthenticated PUT401, reconnect, null and recovery passed | Synthetic app.handleMessage injection; no hardware provider, TLS, token revocation or plugin lifecycle proof |
| ESP32 N2K | PlatformIO6.1.19, espressif32@6.9.0, esp32dev Arduino: compile success; RAM21632/327680, flash277053/1310720 | Bus disabled by compile guard; no upload, wiring or timing measurement |
| ESP32 Signal K | SensESP3.5.0 on espressif32@6.9.0 esp32dev: compile success | Synthetic publisher; no upload/provisioning/server connection/TLS verification |
| Dependency-free suite | 39 tests pass in normal and optimized Python; run `python3 -m unittest discover -s scripts -p 'test_*.py'` and repeat with `python3 -O`; CI runs Python3.10/3.12/3.14 | Model tests and artifact validation do not establish hardware compatibility or agent behavior |

## Pinned source and commands

- NMEA2000 `5b7b9fc3ccc18e30ebfba92da6486cffc6251595`.
- NMEA2000_esp32 `15cc30887f0e629fbee0821c5b1de03d130728ac`.
- CANboat `ed1052d80596a4e6eaa56907dfeb215fac61287d`, analyzer identifies8.3.0.
- Signal K specification source `fb628fb4ee569149fd3810b271d0f987428b4703`
  advertises1.8.4; registry's available package was1.8.2. Documentation1.7.0 is
  a third, separately scoped artifact. Never infer publication from source metadata.
- SensESP template source `f9c209b67784fecaa00c23cf3892c0a4caa592d6`.
- Node26.10.0 ran the lab; server warned its recommended major is24. This is a
  local observation, not a production Node support recommendation.

Reproduction commands and dependency requirements are in
[offline laboratory](../references/offline-laboratory.md),
[Signal K implementation](../references/signalk-implementation.md), and
[embedded recipes](../references/embedded-recipes.md). The npm lock retains resolved
package integrity; embedded transitive ranges remain a reproducibility limitation.
The Signal K harness forces loopback binding in its own process and verifies the
actual ephemeral port; upstream startup text still prints its default address.

## Failed attempts and corrections

- Installing schema1.8.4 failed with ETARGET; queried available package and pinned1.8.2.
- Initial server interface names yielded discovery404; changed to actual `rest`/`ws`.
- Server imports retained process handles after stop; harness now terminates after
  awaiting stop and cleaning its disposable configuration. Earlier owned processes
  were stopped. No personal server configuration was changed.
- Fake-CAN address-claim recognition initially used an incorrect PDU1 PGN mask;
  corrected the harness's PF recognition. This was not an upstream protocol defect.
- First SensESP build exited unsuccessfully without a useful diagnostic; verbose
  retry completed successfully. No assertion that the first failure was diagnosed.
- Validator scanned generated dependency READMEs after npm/PIO installation;
  excludes named generated directories now, with a regression case ensuring authored
  broken links still fail. Missing evidence links were completed.
- Clock-error samples could suppress later corrected timestamps; they no longer set
  the ordering barrier for subsequent samples. This model still requires a trusted
  clock/source recovery policy for production.

## What remains unproved

Licensed-standard conformance, electrical design approval, EMC, saltwater robustness,
real bus-off recovery, actual chartplotter acceptance, OpenCPN GUI source switching,
Pi image restore, radar overlay alignment, sensor calibration, durable actuator
replay protection and independently reviewed agent quality. Consult the
[run ledger](../research/runs/fortification.md); no software pass promotes these.
