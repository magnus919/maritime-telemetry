# NMEA 2000: identifiers, transport, identity and observations

## Decode the correct layer

Use Classical CAN at 250 kbit/s with extended 29-bit identifiers. A raw CAN ID
contains priority, page bits, PDU format/specific fields and source. For PF < 240,
PS is destination and the PGN's low byte is zero; for PF >= 240, PS belongs to the
PGN and destination is global. Do not include SocketCAN EFF/RTR/error flags in the
29-bit ID supplied to the bundled inspector. Bit 25 is reserved for N2K; the tool
rejects it when set. Identifier extraction does not establish payload validity.
[CANboat protocol explanation](https://canboat.github.io/canboat/canboat.html).

Example: `0x09F11223` means priority 2, PGN 127250, source 35, global destination.
`0x18EA232A` is PGN 59904 addressed to 35 from 42; retaining destination as part of
the PGN would incorrectly produce 59939. Unit tests lock these independently
calculated examples and the PF=239/240 boundary.

## Transport before field decoding

A Classical CAN frame has at most eight data bytes. Fast-packet messages use a
3-bit sequence and 5-bit frame index; the initial frame adds a length byte and
carries six payload bytes, subsequent frames seven, up to 223 total. ISO transport
is distinct from fast packet; select transport from the PGN definition, not an
arbitrary payload-byte heuristic. [CANboat framing reference](https://canboat.github.io/canboat/canboat.html).

Recommended reassembly contract:

- Key state by interface, source, destination, PGN and sequence. Different sources
  can interleave the same PGN; a single global buffer will corrupt observations.
- Validate announced length, fragment indices and duplicates. Bound concurrent
  assemblies, age and storage. Reset safely at sequence reuse and address changes.
- On loss, timeout or conflicting fragments, discard the incomplete observation
  with a reason. Never pad missing bytes with zero and deliver a plausible value.
- Preserve transport errors separately from field errors. A gateway export may
  already contain reassembled PGNs; do not strip transport headers twice.
- Document out-of-order policy and exercise it with fixtures. A decoder's tolerant
  acceptance does not imply every commercial receiver accepts the same ordering.

Use a mature stack for encoding and transport. CANboat definitions carry incomplete
or uncertain interpretations, particularly for proprietary traffic. Pin the database
release and record the selected definition; inspect manufacturer selectors and
length constraints. Unknown bytes remain unknown.

## Device identity and network management

A source address can change. Maintain identity using the 64-bit NAME/address-claim
relationship and distinguish device, system and data instances. Two battery data
instances may coexist within a device; they are not two CAN addresses. Use unique
persistent identity for each manufactured unit. Do not copy another vendor's
manufacturer code to trick a display into accepting a prototype.
[NMEA2000 identity and instance guide](https://ttlappalainen.github.io/NMEA2000/md_7_glossary.html).

For a transmitting node, review address claiming (60928), requests (59904), product
information (126996), configuration information (126998), PGN lists (126464), group
functions (126208) and applicable heartbeat behavior (126993). This is a design
checklist, not the exhaustive mandatory set for every device class. The actual
standard/stack version and declared functionality determine obligations. Confirm
which behaviors the library implements and which persistence, handlers and
configuration remain application-owned. The library's certification discussion
explicitly leaves responsibilities with the developer.
[NMEA2000 implementation responsibilities](https://ttlappalainen.github.io/NMEA2000/md_7_glossary.html).

Test duplicate preferred addresses, unique NAMEs, restart ordering, changed
instances and loss of persistent storage. Observe discovery on the actual MFD;
its device list and selected data source are separate acceptance points. A raw
replay can impersonate an existing source, so perform replay only on an isolated
bench with a declared identity policy.

## Plan the measurement contract

These are navigation aids for finding definitions, not complete field layouts:

| Need | Candidate PGN(s) | Question before implementing |
|---|---|---|
| Heading | 127250 | True or magnetic? Deviation/variation available? |
| Position and GNSS quality | 129025, 129029 | Rapid position vs full fix context; stale/no-fix behavior? |
| COG/SOG | 129026 | Reference and ground-relative motion preserved? |
| Depth | 128267 | Transducer reference and offset applied where? |
| Wind | 130306 | Apparent/true and reference enumeration correct? |
| Temperature | 130312, 130316 | Which PGN, source enum and instance does the consumer accept? |
| Fluid level | 127505 | Tank type, instance, calibrated fraction and capacity? |
| Battery status | 127508 | Bank instance, current sign and unavailable fields? |
| Engine | 127488, 127489 | Engine instance and rapidly/slowly changing data split? |
| Switching | 127501, 127502 | Status vs command, supported bank/channel and authorization? |

Check field types, scaling and units in the pinned decoder or setters. Library
helpers use physical units; do not pre-scale a value that the helper already
scales. Missing-data sentinels are field-specific, including signed values and
enumerations; all-ones is not a universal substitute. Do not use float NaN as a
wire encoding unless the API explicitly supports it.
[NMEA2000 message API](https://ttlappalainen.github.io/NMEA2000/_n2k_messages_8h.html).

Maintain a table of sample rate, transmit rate, priority, expiry and bandwidth per
PGN. Do not elevate all traffic to priority zero or transmit at sensor sampling
speed by default. Bound queues and count drops. Synchronize related observations
from one sample when using SID; SID is not a clock or a substitute for freshness.
