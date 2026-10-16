# Embedded examples and build boundaries

## NMEA2000 codec on ESP32

[ESP32 project](../examples/esp32-n2k/platformio.ini) pins Espressif platform 6.9.0,
NMEA2000 core `5b7b9fc3ccc18e30ebfba92da6486cffc6251595` and ESP32 backend
`15cc30887f0e629fbee0821c5b1de03d130728ac`. It was compiled for `esp32dev` without
uploading. The default does not open CAN or publish messages; attempts to enable the
bus flag fail compilation pending an explicit live-mode implementation review.

```sh
pio run -d examples/esp32-n2k
```

The original source builds a synthetic battery message once per second. This proves
headers/dependency compatibility and codec compilation, not a complete sensor node.
The GPIO values passed to the constructor are an example, not a verified board wiring
assignment. To create a live sensor: choose actual transceiver/pins, assigned identity,
consumer PGNs, scheduling, acquisition validity and recovery, then implement the live
mode and bench-test it. Preserve unavailable values; don't substitute a constant
when acquisition fails. Service the stack frequently and bound Wi-Fi/sensor work.

## SensESP synthetic producer

[Signal K project](../examples/esp32-signalk/platformio.ini) uses SensESP 3.5.0 and a
synthetic kelvin-valued water-temperature producer. Its source acquires no GPIO and
contains no credentials. If flashed and provisioned it is an actual publisher, so
keep it on a labeled lab server; don't mingle constant synthetic data with navigation.
Compile only with `pio run -d examples/esp32-signalk`. Compilation succeeded in
this run; see the execution record for scope. Resolved dependencies included
ReactESP3.3.1, ArduinoJson7.4.3, elapsedMillis1.0.6 and AceButton1.10.1.

The [current upstream template](https://github.com/SensESP/SensESP-project-template/tree/f9c209b67784fecaa00c23cf3892c0a4caa592d6)
explains an important split: its plain Arduino/core-2 environment does not provide
its TLS path, while ESP-IDF/Arduino builds from source enable the memory settings
needed for the described TLS configuration. It pins an ESP WebSocket component and
uses dynamic mbedTLS buffers. The older [getting-started page](https://signalk.org/SensESP/pages/getting_started/)
advises disabling server SSL for its described setup. Do not turn that historical
advice into a general security recommendation. The small compile recipe here is
for the plain isolated lab path; TLS hardware behavior is not tested.

## Dependency and hardware ledger

A top-level library version is not a complete lock. Record resolved transitive
libraries, platform, framework and compiler versions from the build output; archive
hashes when reproducibility matters. The source walkthrough and `platformio.ini`
are not permission to flash a board. Before upload, identify the exact DUT and
ports, save prior settings/firmware, confirm bootloader recovery, and establish the
physical power/isolation contract. Keep compile results, bench observations and
vessel observations as separate evidence levels.

Sensor and display projects have different loads: LVGL frame buffers, SD assets,
network clients and metadata can compete for heap/internal DMA memory. Use the
[display case study](signalk-display-case.md) when building a consumer; test per-path
staleness during configuration pauses and long history windows, not just frame rate.
