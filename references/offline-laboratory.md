# Offline interoperability laboratory

Use this route before opening a serial port, CAN controller or boat connection.
The lab has three levels: dependency-free teaching models; optional pinned upstream
software; and separately authorized hardware work. Only the first two were exercised
in this repository. See [execution evidence](../evidence/fortification-results.md).

## First useful result

From the skill root, with Python 3.10 or later:

```sh
python3 scripts/telemetry_lab.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The demo reports 10.0 knots from a synthetic 5.144444444 m/s sample, then explicitly
stale data. It opens no files beyond Python imports, devices, network or subprocesses.
The tests exercise strict stream chunk boundaries, reassembly faults, invalid samples,
source selection, replay and command/feedback state. They do not implement a
production marine gateway or establish NMEA conformance.

## Capture provenance

[Fixture manifest](../fixtures/manifest.json) identifies original MIT-licensed
synthetic records, hashes and independent expected values. `heading.candump` is
one extended CAN frame, not a decoded PGN CSV or a whole multi-frame message.
`ais-position.nmea` is a synthetic single-part type-1 report, never transmitted.
`signalk-deltas.jsonl` includes an actual null, not the string "null".

Retain format/dialect, capture tool, UTC versus monotonic clock basis, physical
interface, filters and whether the adapter already reassembled messages. A source
address is not durable identity: correlate NAME/address claims when available.
Raw captures can contain position, MMSI and serial identifiers. Release synthetic
fixtures by default; document transformations and consent for real captures.

## Executed CANboat recipe

Pinned source: [CANboat ed1052d](https://github.com/canboat/canboat/tree/ed1052d80596a4e6eaa56907dfeb215fac61287d).
Build `analyzer` and `candump2analyzer` in a separately obtained checkout. The
executed macOS ARM64 recipe used its `rel/darwin-arm64` directory; other platforms
have different output names. Neither command below opens a CAN interface:

```sh
"$CANBOAT_BIN/candump2analyzer" < fixtures/heading.candump > /tmp/heading.raw
"$CANBOAT_BIN/analyzer" -json -si < /tmp/heading.raw
```

Set `CANBOAT_BIN` to the inspected binaries' directory. Expected message: PGN 127250,
source 35, SID 7, heading 1.0 rad, deviation -0.1 rad, variation 0.2 rad, true
reference. The output also includes a version/units record; don't treat every JSON
line as a measurement. At this revision, **without `-si` the angular output was
rounded degrees** (57.3, -5.7, 11.5). Never assume that JSON implies SI units.

Scope: one nominal C-tool conversion was executed. Rust CLI parity, other vendor
formats and malformed-capture converter behavior are not established by that result.
Use exact CLI help from the chosen revision. `-clocksrc` can alter host time;
interface/server commands can claim addresses or configure gateways. These are
not part of this offline recipe. See CANboat's README for gateway/dialect details.

## Upstream NMEA2000 host probe

Use separately obtained commit `5b7b9fc3ccc18e30ebfba92da6486cffc6251595`:

```sh
c++ -std=c++11 -I "$NMEA_STUDY_SOURCE/src" examples/protocol_oracle.cpp \
  "$NMEA_STUDY_SOURCE"/src/*.cpp -o /tmp/maritime-protocol-oracle
/tmp/maritime-protocol-oracle
```

Unlike the earlier heading probe, this example supplies a controllable `millis()`
and, on Linux, a process-local `clock_gettime` adapter because the pinned library
uses that clock directly. Both are confined to this fake-CAN executable; no system
clock is set. Do not also link the upstream fixed-clock test stub. The fake CAN backend only
records in-memory frames. Four independent scaled-integer byte vectors cover depth,
rapid position, battery and wind. The lifecycle test observes address claiming,
publication held during claim, publication after the timer, and moving address after
a synthetic lower NAME conflict. The all-zero adversary NAME is a test input, not
a valid identity recommendation. No actual CAN timing, electrical ACK or bus-off
behavior is tested. Three upstream VLA extension warnings were observed on Clang.

## Teaching-model policies

`FastPacket` requires an explicitly classified PGN, eight-byte CAN frames and
ordered fragments. It keys state by interface/source/destination/PGN/sequence,
expires incomplete state, enforces a capacity bound and returns payload only when
complete. Its default 250 ms expiry is **lab policy**, not a standard requirement.
It intentionally excludes ISO TP, single-frame dispatch and retransmission policy.
It demonstrates what to test in a production library, not a replacement for one.

`Samples` requires explicit source selection and stores measurement age plus
monotonic elapsed time. Repeated/older timestamps cannot refresh a sample. Wrong
numeric types (including booleans), null, NaN and infinity are unavailable; old
samples are stale; excessive future timestamps signal clock error. It supports
numeric observations only, not arbitrary Signal K objects or complete schema checks.
Clock recovery/source replacement needs an explicit reset policy in a real system;
rejecting replays alone cannot solve a mis-set producer clock.

`RelayModel` has no hardware interface. Authorization and interlock are independent
inputs; acceptance is separate from achieved feedback. It rejects expired requests,
conflicting ID reuse and new requests beyond its bounded replay ledger. Feedback
must identify the active request and be sampled after issue. Timeout and manual
override terminate the request. A real actuator needs durable replay protection,
authenticated feedback, watchdogs and safe restart semantics absent from this model.
