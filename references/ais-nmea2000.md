# AIS over NMEA 2000

Use this guide for an AIS receiver/transponder attached to a boat backbone, a DIY
traffic display, or a gateway into Signal K/OpenCPN. AIS target reports are native
N2K PGNs; they do not require an intermediate NMEA 0183 connection. The physical
AIS radio link, N2K transport and application target model are separate layers.

## Choose and verify the path

```text
AIS radio receiver/transponder → N2K backbone → compatible MFD
                                            → isolated CAN gateway → CANboat
                                                → Signal K target contexts → client
                                                → AIS-to-0183 converter → VDM consumer
```

The [Garmin AIS800 transmit-PGN table](https://www8.garmin.com/manuals/webhelp/GUID-61A42529-ECEC-4B79-9F77-A5D87D90A579/EN-US/GUID-F6E8195D-CFA3-40B7-9BEA-68EDD00813E7.html)
is concrete manufacturer evidence that commercial AIS equipment publishes AIS
reports over N2K. Its receive table is different: **transmitting a target PGN onto
N2K does not instruct this transponder to broadcast that target over AIS radio**.
Likewise a chartplotter's N2K connector alone does not prove every AIS PGN is accepted.
Record exact producer/consumer model, firmware and receive/transmit tables.

Use an existing isolated gateway first. Record whether it supplies raw eight-byte
CAN frames or already assembled PGN messages. Reading an attached gateway can still
involve address claiming or CAN acknowledgments; verify its operating mode. The
bundled examples are offline and never open a device or radio.

## PGN and AIS-message mapping

These are community implementation mappings, supported by the pinned
[CANboat database](https://github.com/canboat/canboat/tree/ed1052d80596a4e6eaa56907dfeb215fac61287d/database/pgns)
and manufacturer lists, not a substitute for licensed NMEA requirements.

| PGN | AIS report / radio message family | Application responsibility |
|---|---|---|
| 129038 | Class A position, types1/2/3 | MMSI, position, ground motion, true heading, ROT, navigation state |
| 129039 | Class B position, type18 | Same target identity; preserve class/capability flags where supported |
| 129040 | Extended Class B position, type19 | Position plus static details; do not assume all converters implement it |
| 129794 | Class A static/voyage, type5 | Name, callsign, IMO, dimensions, destination/draft/ETA where available |
| 129809 / 129810 | Class B type24 parts A/B | Join name and other static details by target MMSI; tolerate either order |
| 129041 | Aids to navigation, type21 | Preserve aid identity, virtual/off-position flags; not an ordinary moving vessel |
| 129793 | UTC/date reports, types4/11 | Reporting station's time; not permission to set the host clock |
| 129798 | SAR aircraft position, type9 | Distinct target semantics; don't silently treat altitude as vessel data |
| 129795 / 129797 | Addressed/broadcast binary, types6/8 | Application identifiers and payload schema needed; not arbitrary sensor data |
| 129801 / 129802 | Addressed/broadcast safety text, types12/14 | Retain addressing and message provenance; not an authenticated command |
| 129813 | Long-range broadcast, type27 | Lower-resolution/limited report; support depends on receiver/decoder |

The four core PGNs129038/129039/129809/129810 have executed fixtures here.
Other rows are orientation and source inspection, not end-to-end tested profiles.
129813 is in CANboat's database; it is not listed in the retrieved AIS800 table.

## Receiver identity is not target identity

A transponder at CAN source35 may report hundreds of MMSIs. Keep three identities:

1. Bus/interface plus receiver NAME/address mapping: observed transport provenance.
2. Target MMSI: the identity carried inside the AIS report. Normalize its representation
   without replacing it with the receiver address, PGN sequence number or own MMSI.
3. Application entity: Signal K vessel or aid context. Preserve own-versus-other status.

Use `(entity type, MMSI)` to correlate target fields, with source-specific observations
underneath it. For duplicate receivers, retain provenance and select a source or
apply an explicit fusion policy. Last arrival is not automatically newest measurement.
Address reuse after restart must not silently inherit the previous receiver's identity.
MMSI and CAN NAME are identifiers, not cryptographic proof of who sent the report.

Class B static A/B is **not** N2K fast-packet fragmentation: these are separate PGNs
which each may span CAN frames. Retain either static half without waiting to show a
valid position. Never attach one target's callsign/name to another because both came
from the same CAN source. Never use static arrival to refresh position age.

## Wire decoding and legacy lengths

Reassemble fast packets before decoding the PGN. Key assemblies by interface,
source, destination, PGN and transport sequence; bound lifetime and memory. Do not
use a PGN's payload SID as the fast-packet sequence counter. Dropping a middle CAN
frame is different from receiving a complete older-layout PGN with no optional tail.

At the pinned CANboat revision, the following payload lengths are understood:

| PGN | Modern fixture | Accepted older fixture(s) | Missing tail |
|---|---|---|---|
| 129038 | 28 bytes | 27 | SID |
| 129039 | 27 bytes | 26 | SID |
| 129809 | 27 bytes | 26 and25 | SID; in25-byte form also transceiver information |
| 129810 | 35 bytes | 33 | Transceiver information and SID |

All those exact fixture lengths were decoded. This is version-scoped implementation
behavior, informed by [CANboat PR848](https://github.com/canboat/canboat/pull/848), not
permission to accept arbitrary truncation. Validate minimum/known layout lengths.
Preserve absent tail fields as unknown; absence does not establish reception channel
or own-vessel status. The NMEA2000 library probe emits the modern forms.

## Units, validity and clocks

- CANboat C `-si` gives these position PGNs' COG/heading in radians, SOG in m/s,
  position in degrees and ROT in rad/s. Its JSON mode alone does not promise SI.
  N2K encoding resolution and AIS radio encoding resolution differ.
- Convert decoded units once. Raw AIS radio ROT uses a nonlinear representation;
  do not apply that transformation again to already-decoded N2K rad/s.
- True heading and COG are different observations; zero is a valid heading,
  longitude, latitude or speed. Validate presence/type/range, not truthiness.
- Preserve unavailable positions/angles instead of zero. In the executed N2K vector,
  signed-position `0x7fffffff` decodes as null under `-empty`; the 0183 converter emits
  AIS's unavailable lon181/lat91. These must never become map coordinates.
- An AIS report second is not a complete UTC timestamp. CANboat's `TIME_STAMP`
  lookup treats60 as unavailable,61 as manual input,62 as dead reckoning and63 as
  inoperative positioning. Keep original second/status, gateway receipt time and
  any trustworthy full observation timestamp separately.
- Use monotonic elapsed time for local expiry. Choose thresholds by report class,
  motion and intended display; there is no universal “all AIS every two seconds”
  rule. Store per-path/group freshness: name/ship dimensions and position have
  different update schedules. A live socket or new static report cannot revive a fix.

The [target-state model](../scripts/ais_targets.py) demonstrates bounded source-aware
position ageing, static separation, replay suppression, own-target exclusion and
future-clock recovery. Its60-second default is lab policy, not a navigation standard.
It excludes AtoNs/SAR, fusion, persistent state, threat detection and CPA/TCPA decisions.

## Signal K and OpenCPN paths

The [Signal K model](https://signalk.org/specification/1.7.0/doc/data_model.html)
places other vessels in contexts such as `vessels.urn:mrn:imo:mmsi:123456789`.
The inspected n2k-signalk mapper uses `atons.urn:mrn:imo:mmsi:…` for129041.
Never write every received AIS target into `vessels.self`. Check the real mapper's
own-MMSI handling; the offline mapper itself still emits an MMSI vessel context for
an own-information fixture. The input gateway/server must supply its own routing policy.

There are three distinct consumer options:

| Consumer path | Configuration evidence to collect |
|---|---|
| OpenCPN native Signal K connection | Exact OpenCPN release, discovered server endpoint/auth, other-vessel target rendering and supported fields |
| OpenCPN/legacy app consuming 0183 | Enable a dedicated AIS conversion plugin and its output route; inspect emitted VDM/multipart behavior |
| Direct N2K-capable OpenCPN interface/plugin | Exact platform/adapter/plugin version and receive-PGN table; do not infer support from a generic CAN connection |

The [OpenCPN Signal K manual](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:manual_basic:set_options:connections:singnalk)
distinguishes native Signal K from converted0183 and explicitly calls for an AIS
plugin on the conversion path. Its “not over TCP” phrasing concerns the generic
NMEA TCP connection option; WebSocket itself uses TCP. The
[TwoCan project](https://github.com/TwoCanPlugIn/TwoCanPlugIn) is another documented
N2K integration path; check its build/platform support, not historical screenshots.
No OpenCPN GUI or physical MFD was tested in this run.

Do not enable native Signal K targets and a converted duplicate feed without a
source/deduplication policy. Prevent output from feeding the original input through
another gateway. Filter by allowed PGNs/context/source/direction; an event name or
TCP port is not a loop-prevention policy. Keep synthetic targets on the offline lab.

## Observed conversion limits and commissioning

Read the [executed lab and limitations](ais-n2k-laboratory.md) before recommending
these pinned packages. They decode useful data, but conversion is not lossless.
Use the [mapping worksheet](../templates/ais-mapping.csv) and
[target acceptance record](../templates/ais-acceptance.md). Verify target identity,
static joins, expiry, source changes, unavailable/zero positions and own-ship
suppression on the **actual consumer** before calling the integration accepted.
