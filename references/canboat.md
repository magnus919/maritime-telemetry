# CANboat: inspect and explain the bus

CANboat is an open-source protocol-tool project with a community PGN database;
it is not a replacement standards body. Its utilities can both read and write
traffic, so identify the operation before execution. Pin the release and retain
its license/attribution if redistributing definitions. The upstream README lists
supported input formats and decoder workflows; format and executable names vary
across releases. [CANboat project](https://github.com/canboat/canboat).

Current upstream provides both C utilities and a Rust CLI. Live `canboat interface`
or `canboat server` operations can act as an N2K node, including address claiming.
Do not interpret their use as passive capture or assume `--no-claim` makes all
transmissions impossible. Select an offline converter for initial analysis.

## Default workflow: capture file to evidence

1. Obtain an authorized, bounded recording. Record gateway model, firmware,
   interface, capture command, wall clock/time zone, bus state and any dropped-frame
   counters. Hash the original and retain it unchanged.
2. Identify whether records are raw CAN frames or assembled PGNs. SocketCAN logs,
   Actisense text/binary, gateway RAW output and Signal K deltas are not equivalent.
   Examine a few records before selecting the importer. Preserve timestamps and
   interface identity during conversion.
3. Pin the CANboat release or commit, build from its release instructions, and
   inspect that version's help. For releases providing `analyzer`, the typical
   offline invocation is below. Confirm the input importer recognizes the format.
4. Decode into a separate artifact, inspect diagnostics as well as exit status,
   and count input records, decoded observations, unknown definitions and failures.
   A successful process with zero decoded observations is not an accepted capture.
5. Compare one physical event against the decoded time series and an independent
   expected value. Repeat for source changes, unavailable values and fragments.
6. Keep a compact evidence record: capture hash, tool/database revision, arguments,
   selected PGN definition, units, decoded sample, uncertainty and consumer result.

```sh
# Offline files only; capture.log must be a format accepted by this pinned version.
analyzer -json < capture.log > decoded.jsonl 2> decoder.log
```

This is a command pattern, not a claim that a local CANboat binary has been
installed or run. Do not substitute a device-opening utility, add a transmit pipe,
or replay the file to make the command “work.” Refer to the pinned README when
handling newer executable layouts or converting gateway-specific formats.
[Upstream workflow and formats](https://github.com/canboat/canboat/blob/master/README.md).

## Unknown does not mean arbitrary

For proprietary PGNs, record source NAME, manufacturer/industry selectors,
length and firmware alongside the candidate interpretation. A layout matching one
vendor may decode another vendor's bytes into plausible but false values.
Inspect completeness flags and field descriptions before presenting a measurement.
Keep unknown bytes in hex; do not turn them into engineering units by guessing.

Original reverse-engineering experiment pattern:

- State one hypothesis, such as “this field represents measured tank level.”
- Use a controllable bench condition and independently measured low/mid/high
  values. Keep other conditions steady and include an unchanged control interval.
- Compare candidate scaling, sign, offset and missing-data representations on a
  separate recording. Check whether it is a command, status, counter or checksum.
- Record evidence against the hypothesis, including contradictory frames.
- Keep the decoder experimental until a held-out capture and target behavior
  support it. Never discover actuator commands by brute-force bus injection.

## Troubleshooting decoder disagreement

| Symptom | Next evidence |
|---|---|
| Huge temperatures/angles | Raw bytes, scale, signedness, sentinel and conversion API |
| One vendor decodes, another does not | Manufacturer selector and PGN variant |
| Random fast-packet values | Capture loss, raw/assembled boundary, sequence/source interleaving |
| Values disappear after reboot | Source address/NAME association and decoder state reset |
| Different releases disagree | Same immutable capture through both pinned versions; field-definition diff |

A CANboat decode establishes what that implementation inferred. The next acceptance
step remains the intended consumer and the physical measurement. It does not
establish NMEA certification, timing compliance or a field-proven device.

## Worked implementation

See the [fortification guide](offline-laboratory.md) for worked examples and explicit execution boundaries.

## AIS on the backbone

Use [AIS over NMEA 2000](ais-nmea2000.md) for native target PGNs, receiver/MMSI
identity, partial static data, Signal K contexts and consumer paths. The
[AIS laboratory](ais-n2k-laboratory.md) records tested cases and conversion losses.
