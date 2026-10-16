# Learn the protocol from the NMEA2000 implementation

Use this reference when implementing N2K directly, porting to a new language or
controller, reviewing an encoder/decoder, or debugging behavior hidden by a library.
The study is pinned to upstream commit
`5b7b9fc3ccc18e30ebfba92da6486cffc6251595`, inspected 2026-10-16.
These are observations of that implementation, not a substitute for the licensed
standard. An independent implementation need not reproduce its architecture or
compatibility workarounds. NMEA2000 is MIT-licensed; retain upstream notices if
copying or adapting its code. This repository links to the source without vendoring it.

## Read in layers

All source links below are immutable commit links. Follow symbols within the pinned
file rather than assuming line numbers survive an upstream upgrade.

| Layer | File and symbols | Learn / inspect |
|---|---|---|
| Board selection | [NMEA2000_CAN.h](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/NMEA2000_CAN.h) | Backend selection, separate controller libraries; not electrical compatibility proof |
| Driver boundary | [NMEA2000.h](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/NMEA2000.h), `CANOpen`, `CANSendFrame`, `CANGetFrame` | What the transport core expects of the hardware driver |
| Header/transport/state | [NMEA2000.cpp](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/NMEA2000.cpp), `CanIdToN2k`, `N2ktoCanID`, `SendMsg`, `SetN2kCANBufMsg`, `ParseMessages` | Addressed/global IDs, fragmentation, receive assembly and service loop |
| Binary primitives | [N2kMsg.cpp](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kMsg.cpp), `SetBuf`, `GetBuf`, `Add2ByteDouble`, `GetBuf2ByteDouble` | Endianness, signedness, quantization, sentinels, bounds behavior |
| Constants/storage | [N2kMsg.h](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kMsg.h) | NA/out-of-range values, payload capacity, public API expectations |
| Typed PGN codec | [N2kMessages.cpp](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kMessages.cpp), `SetN2kPGN127250`, `ParseN2kPGN127250` | Trace one physical quantity all the way to bytes and back |
| Configuration requests | [N2kGroupFunction.cpp](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kGroupFunction.cpp) and [default handlers](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kGroupFunctionDefaultHandlers.cpp) | Dispatch by function/target PGN, selection fields and response obligations |
| Device discovery | [N2kDeviceList.cpp](https://github.com/ttlappalainen/NMEA2000/blob/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/src/N2kDeviceList.cpp) | Associate changing addresses with identity and discovered capabilities |
| Test examples | [test directory](https://github.com/ttlappalainen/NMEA2000/tree/5b7b9fc3ccc18e30ebfba92da6486cffc6251595/test) | Existing test scope, host clock stub and missing adversarial cases |

## 1. Build a frame boundary before a PGN decoder

Represent a CAN observation with interface, timestamp, extended identifier, frame
kind, DLC and bytes. Validate Classical CAN data-frame shape and remove adapter
flags before ID extraction. Do not confuse host gateway framing with bus payload.
Reject RTR/error frames as telemetry; retain them separately as diagnostics.

`CanIdToN2k` extracts priority/source and branches at PF=240. `N2ktoCanID` rejects
addressed PGNs with a nonzero low byte. For PDU1, destination goes into PS; for
PDU2, PS is part of the PGN. Thus `0x18EA232A` addresses PGN 59904 to node 35 from
42, while `0x09F11223` is global PGN 127250 from 35. Test both directions and the
PF=239/240 boundary. Do not simply shift a CAN ID and call the result a PGN.

## 2. Follow one measurement through the codec

The pinned heading setter selects PGN 127250 and priority 2, then writes:

| Byte offset | Value | Encoding observed in this implementation |
|---|---|---|
| 0 | SID | One byte |
| 1–2 | Heading | Unsigned 16-bit, little endian, 0.0001 rad/count |
| 3–4 | Deviation | Signed 16-bit, little endian, 0.0001 rad/count |
| 5–6 | Variation | Signed 16-bit, little endian, 0.0001 rad/count |
| 7 | Reference | Low two bits; setter fills upper six bits with ones |

For SID 7, heading 1 rad, deviation −0.1 rad, variation +0.2 rad, true reference:

```text
heading   1 / 0.0001 = 10000 = 0x2710 → 10 27
deviation -0.1 / 0.0001 = -1000       → 18 FC (two's complement)
variation 0.2 / 0.0001 = 2000         → D0 07
payload: 07 10 27 18 FC D0 07 FC
```

This arithmetic gives an independent expected vector, rather than asking an
encoder and its matching decoder to agree with each other's possible mistake.
The supplied host probe confirmed these exact bytes against the pinned upstream
setter. See the evidence record for the executed scope and warnings.

The implementation uses `N2kDoubleNA` as an API sentinel, not IEEE NaN. The heading
field encodes unavailable as `FFFF`; signed deviation/variation use `FF7F` on the
wire (`0x7FFF`). Its numeric setters round to nearest with half away from zero,
then use out-of-range codes when integer bounds fail. Python's default `round`
has different tie behavior; make quantization explicit in a port.

Crucially, the two-byte getters shown in `N2kMsg.cpp` recognize NA, while their
ordinary numeric path does not turn the OR sentinel into a distinct status. An
independent decoder should retain unavailable, out-of-range/reserved and measured
states according to its declared field contract instead of displaying an error
code as an angle. Inspect each field type; do not generalize these two sentinels
to every PGN or enumeration.

The heading parser returns false for the wrong PGN, but a true return is not a
complete validity judgment. Validate payload length, reference enumeration,
reserved/error encodings, physical range and freshness independently. Trace the
getter's behavior on a short buffer instead of assuming that parse success proves
all eight bytes existed.

## 3. Transport is selected by message definition

`SendMsg` uses a single frame only when length <=8 **and** the PGN is not classified
as fast packet. A short fast-packet PGN still has transport framing. Conversely,
seeing a small first byte is not sufficient to identify a fast packet.

For fast packets, the high three bits of byte zero are sequence and the low five
are frame index. Frame zero adds total length and six data bytes; subsequent
frames carry seven. Example synthetic ten-byte payload, sequence 3:

```text
payload 01 02 03 04 05 06 07 08 09 0A
frame 0 60 0A 01 02 03 04 05 06
frame 1 61 07 08 09 0A FF FF FF
```

Padding is excluded from payload length. Sequence wraps; it is not globally unique.
The pinned implementation maintains transmit sequence state and stops its send
loop on a frame failure. A failed multi-frame send can therefore leave a prefix
already sent. Do not assume message transmission is atomic or retry a trailing
fragment as a complete message.

On receive, `SetN2kCANBufMsg` finds continuation state using PGN/source (excluding
ISO-TP state when enabled) and requires the full frame-control byte to increment
by one. A mismatch frees the partial message. This is the observed implementation;
it is **not** a normative guarantee that PGN/source alone is an adequate key for
every traffic pattern. An independent receiver should define a stronger context
including interface, destination and sequence, bound buffers/timeouts, and specify
what happens on overlapping sequences, duplicates and out-of-order fragments.

Keep ISO multi-packet transport separate. The source's `StartSendTPMessage`,
`TestHandleTPMessage` and pending-send logic handle connection-management/data
transfer and broadcast versus addressed exchanges. Do not substitute automotive
ISO-TP or fast-packet reassembly for this path. Document unsupported transports
rather than quietly decoding their fragment bytes as measurements.

## 4. A transmitting node needs a state machine

Trace `StartAddressClaim`, `IsAddressClaimStarted`, `HandleISOAddressClaim` and
`SendMsg`. This version starts a 250 ms claim timer and withholds normal messages
while claiming. On a conflict, the lower numeric NAME retains the address; the
other node seeks another address. Source address is routing state, not persistent
identity. Test that an encoder reads the node's current address after reassignment.

For equal NAMEs during claiming, the library contains a device-instance adjustment
workaround. Do not infer that duplicate identities are acceptable or copy that
workaround as a universal protocol rule. Allocate distinct persistent identities
and expose a duplicate-identity fault in a new implementation.

An independent node design should expose initialization, claiming, ready,
cannot-claim and bus-fault/recovery states, with transmission eligibility per state.
Review address-claim replies, ISO requests, product/configuration information,
PGN lists, heartbeat and group-function behavior for the intended device class.
Being able to emit one correct heading frame does not complete those obligations.

## 5. Parsing also advances the node

`ParseMessages` drains outgoing queues and pending information, consumes at most
20 received frames per call in this revision, dispatches system/application
handlers and services heartbeat. That frame budget is an implementation scheduling
choice, not a standard rate. Long sensor reads or callbacks can starve both RX and
network-management work. Budget execution time, queue capacities and drop counters.

`SendFrame` can buffer a frame. `SendMsg` success is not application acknowledgment
from a chartplotter, nor proof of physical actuation. Separate encoded, queued,
controller-transmitted, recipient-consumed and physically-observed states.
The core's `N2km_ListenOnly` blocks its own send path; verify backend/controller
listen-only separately before claiming no ACK/error-frame influence on the wire.

## Independent implementation acceptance

Use the protocol worksheet to declare each layer's invariants and evidence. Start
with offline vectors and a fake clock/driver; add physical hardware only afterward.

- Header tests: addressed/global, destination masking, flag rejection, source change.
- Numeric tests: signed negative, byte order, half-step rounding, NA, OR/reserved,
  wrong length/PGN and reference enumerations. Use explicit status, never zero fill.
- Transport tests: short fast PGN, boundary lengths, interleaved sources, destination
  differences, duplicate/missing fragments, sequence wrap, timeout and buffer pressure.
- Node tests: two NAMEs competing for an address, equal NAME fault, request handling,
  no normal sends during claim, recovery and persistent configuration.
- Consumer tests: independently decode bytes, then confirm the intended instrument
  selects and displays the source. Include failure/staleness and restart behavior.

Differential tests against this library are valuable compatibility evidence, but
agreement can preserve the same bug or interpretation. Combine hand-calculated
vectors, a second implementation such as CANboat, licensed requirements when
available, and actual target-device observations. Report each evidence type separately.
