# Reproduce the AIS/N2K software experiments

These are original synthetic records, not captured vessel traffic. The Class A and
Class B nominal vectors reuse an MMSI to test separate encoding families; this is
not a claim that one real station simultaneously belongs to both classes.

## Dependencies and first useful run

Python3.10+ standard library is enough for fixture generation, target-state and
repository tests. Optional upstream experiments need a C++ compiler, separately
obtained pinned checkouts, Node/npm and pyais3.3.1. No public demo, API key, adapter
or radio is required. npm installs packages from the registry; the probe itself
opens no sockets/devices. This skill does not require the research service.

```sh
python3 scripts/ais_fixture.py --format index
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Fixtures include13 messages: modern Class A/B position and Class B static A/B,
five legacy-tail variants, zero longitude, unavailable position, second target and
own-information. `fixtures/ais-n2k.raw` contains **assembled** payloads;
`fixtures/ais-n2k.candump` contains their **fast-packet CAN frames**. Neither is a
script for sending to a live network.

## Encoding and two independent decoder paths

Set `NMEA_STUDY_SOURCE` to checkout
`5b7b9fc3ccc18e30ebfba92da6486cffc6251595` of ttlappalainen/NMEA2000.
Set `CANBOAT_BIN` to the built binaries from CANboat
`ed1052d80596a4e6eaa56907dfeb215fac61287d` (analyzer8.3.0).
On the recorded macOS arm64 run these were `rel/darwin-arm64` binaries.

```sh
c++ -std=c++11 -I "$NMEA_STUDY_SOURCE/src" examples/ais_n2k_oracle.cpp \
  "$NMEA_STUDY_SOURCE"/src/*.cpp -o /tmp/ais-n2k-oracle
/tmp/ais-n2k-oracle > /tmp/ais-n2k-library.raw
python3 scripts/verify_ais_decode.py \
  --analyzer "$CANBOAT_BIN/analyzer" \
  --converter "$CANBOAT_BIN/candump2analyzer" \
  --library-output /tmp/ais-n2k-library.raw
"$CANBOAT_BIN/analyzer" -json -si -camel -empty \
  < fixtures/ais-n2k.raw > /tmp/ais-n2k-decoded.jsonl
```

The verifier compares four library payloads with independently calculated scaled
integers/string padding, then runs both assembled and raw-frame paths three times.
It requires13 messages per path and equal decoded fields; checks units, MMSI,
static values, legacy SID absence, zero, unavailable and own-information marker.
A mismatch raises an error and exits nonzero, including under optimized Python.
C++ output generation alone is not an oracle comparison. The host compile in this
run suppressed upstream Clang VLA extension warnings; no CAN backend is opened.

CANboat `-camel` emits an object keyed by PGN identifier plus a separate version
record. The verifier unwraps it and checks SI mode; the Node probe discards the
version record. Do not pass the wrapper itself to a mapper expecting `pgn/fields`.

## Signal K mapping and 0183 translation

```sh
npm ci --prefix examples/ais-n2k-lab --ignore-scripts --no-audit --no-fund
node examples/ais-n2k-lab/probe.cjs /tmp/ais-n2k-decoded.jsonl > /tmp/ais-integration.json
python3 -m venv /tmp/ais-decode-venv
/tmp/ais-decode-venv/bin/pip install pyais==3.3.1
/tmp/ais-decode-venv/bin/python examples/ais_n2k_0183_probe.py /tmp/ais-integration.json
```

Use a new temporary venv path if that path already belongs to other work.
The lock pins `@signalk/n2k-signalk4.7.0`, schema1.8.2 and
`signalk-n2kais-to-nmea0183 2.0.3` plus transitive packages. Node26.10.0 was used.
The fake app declares server2.33.0 solely for the plugin's field-naming contract;
this run does **not** boot a server. Actual plugin start/stop hooks are tested on an
in-process EventEmitter, twice per trial, verifying no listener remains after stop.

## Observed results and actionable limitations

| Boundary | Executed observation | Implication |
|---|---|---|
| N2K encoding | Four library outputs match independent payloads | Scoped encoding evidence, not radio/physical conformance |
| CANboat | All13 cases decode on both input paths, repeated3 times | These length/unit/identity cases verified on this revision |
| Signal K mapper | Nominal position/SI values and MMSI context pass schema; static updates have no position | Metadata and position must be aged independently |
| Zero longitude | mapper4.7.0 drops `navigation.position` for longitude0 | Regression gate for upgrades; use validated patched mapping if operating on zero meridians/equator; do not perturb coordinates |
| Unavailable position | Mapper omits position rather than emitting a clearing null | Existing cached position needs its own expiry; message arrival cannot renew it |
| Own target | 0183 converter suppresses configured own MMSI and own-information by default; explicit `sendSelf` enables it | Verify own MMSI/config; suppression does not mean RF control |
| Class A0183 | Input type1 becomes type3; COG1rad becomes57°, heading0.5rad becomes29°, SOG5m/s becomes9.7kn | It is re-encoding with rounding, not transparent forwarding |
| Class A metadata | Report second30 becomes60/unavailable; high position accuracy becomes false | Do not claim original timestamp/accuracy is preserved |
| Class B static | Name/callsign/dimensions retained; vendor string absent in0183 output | Static field loss must be accepted or addressed |
| Class B positions | Type18 retained; report second becomes60 | Freshness must use defensible receipt/observation policy |
| Missing position0183 | Becomes longitude181/latitude91 unavailable sentinels | Never plot those as geographic coordinates |
| PGN129040 to0183 | Converter2.0.3 returns no output for this PGN | Do not advertise extended Class B conversion merely from generic AIS support |
| Plugin lifecycle | start→event→stop twice yields exactly2 outputs and zero retained input listeners | Local hook evidence only; server config reload/network delivery untested |

The `passed` keys in evidence mean **the recorded behavior was reproduced**. They
do not mean all behavior is desirable or lossless. The zero-coordinate omission is
an unresolved dependency defect. No upstream issue/change was submitted in this task.
Use exact package versions when reproducing; don't assume the finding applies to a
future release or every AIS PGN. RF timing, AtoN/SAR rendering, multipart type5,
all sentinel flags, duplicate-source fusion and actual chartplotter acceptance are
not established by this set.

Detailed original outputs and source/claim provenance are linked from the
[research report](../research/runs/ais-n2k.md). No complete normative AIS/NMEA
specification or third-party source body is redistributed.
