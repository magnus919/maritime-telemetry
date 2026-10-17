# Streaming 0183, GNSS and AIS implementation profiles

## Separate framing and meaning

The original inspector accepts a declared strict untagged ASCII/checksum/82-byte
profile. `SentenceStream` in [the offline lab](../scripts/telemetry_lab.py) adds bounded
chunk accumulation and resynchronization. Tests split a valid sentence at every
byte boundary, concatenate records, inject noise/checksum failure and exceed the
buffer. LF completes a record; a new `$`/`!` delimiter abandons the incomplete one.
A final partial sentence remains incomplete. This is an explicit log/stream policy,
not support for all 0183 editions or tag blocks.

NMEA's [public overview](https://www.nmea.org/nmea-0183.html) identifies 4.30 and
separate 4800/38400 baud profiles. GPSD's [NMEA reference](https://gpsd.gitlab.io/gpsd/NMEA.html)
is an implementation-oriented secondary interpretation, not the licensed standard.
Use device manuals and a declared edition when empty fields, longer sentences,
new GNSS talker IDs or proprietary formats matter.

## GNSS semantic checklist

| Message family | Useful information | Do not infer |
|---|---|---|
| RMC | Date/time, status, position and ground motion in the declared profile | Speed through water or current compass heading |
| GGA | Fix-related position/quality/altitude details | Full calendar date from time-of-day alone |
| GSA / GSV | Solution/satellite information, possibly multipart/system-specific | Every satellite line describes the same epoch or constellation |
| Heading / wind / depth | Value plus message-specific reference and units | True/magnetic, apparent/true, keel/transducer equivalence |

Maintain a date/time association window across messages; don't join a new time-of-day
to an arbitrarily old date. Test midnight, invalid fix status, leap/rollover handling
and clock resets against the actual receiver. Avoid a global rollover correction
when reading old captures. Reject impossible coordinates and numeric non-finites
while keeping missing fields distinct from zero. Preserve talker/port provenance.

## AIS multipart boundary

AIS sentence checksum validates the transport envelope, not a target's position or
identity. Preserve channel, fragment count/number, sequence ID, fill bits and input
port. Reassembly must not mingle two simultaneous reports. Empty sequence IDs need
a conservative per-source/channel policy with expiry; when interleaving cannot be
disambiguated, discard/flag rather than invent an assembly. Bound total state and
reject inconsistent counts, missing fragments, invalid payload characters and
nonfinal fill-bit misuse. Decode the complete payload with a maintained decoder.

The [pyais project](https://github.com/M0r13n/pyais) documents individual/multipart
decode and stream interfaces. The optional [probe](../examples/ais_probe.py) was run
with pyais 3.3.1 against our independently bit-constructed type-1 fixture: MMSI
123456789, longitude -2°, latitude 1°, speed 10 kn, course/heading 90°, second 30.
The MMSI and position are synthetic. This corroborates those fields only; multipart,
AIS availability sentinels, tag blocks and all message types remain untested here.

```sh
python3 -m venv /tmp/maritime-ais
/tmp/maritime-ais/bin/pip install pyais==3.3.1
/tmp/maritime-ais/bin/python examples/ais_probe.py
```

Do not write an ad hoc bit decoder to replace a mature decoder merely because this
small vector passes. Report unavailable values according to each AIS field's
semantics; an unavailable coordinate must not become a target at (0,0). Track target
age separately from TCP liveness and own-ship age. This skill's AIS examples receive
and decode only; they do not transmit RF or configure a radio.

## AIS on the backbone

Use [AIS over NMEA 2000](ais-nmea2000.md) for native target PGNs, receiver/MMSI
identity, partial static data, Signal K contexts and consumer paths. The
[AIS laboratory](ais-n2k-laboratory.md) records tested cases and conversion losses.
