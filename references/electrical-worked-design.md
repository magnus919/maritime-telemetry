# Worked physical-interface design review

This is a reviewable architecture and arithmetic example, not a tested PCB or a
universal pinout. Use [power/topology worksheet](../templates/power-topology.md) and
exact connector drawings before wiring. Connector **mating face versus wire side**
changes how a diagram is read; never assign pins from cable colors alone.

## Two-domain CAN interface

```text
MCU/USB domain                         isolated bus domain
3.3 V logic ── TX/RX ── [ISO1042 isolation/transceiver] ── CAN H/L
logic ground ──────────|| barrier ||──────────────────── bus ground
logic supply ── [rated isolated DC/DC] ── regulated bus-side supply
                    no alternate ground bridge
```

[TI ISO1042](https://www.ti.com/product/ISO1042) is a candidate isolated CAN
transceiver; its isolation does not provide bus-side power. The vendor lists
reference/evaluation designs, including a separate isolated converter. Treat them
as design inputs. Select the exact package, supply range, common-mode limits,
creepage, decoupling, protection and converter load regulation from the datasheets.
The product page was retrieved; the PDF extraction failed in this research run,
so a package-level approved schematic is **not** claimed.

| BOM function | Candidate / selection condition | Verification before build |
|---|---|---|
| CAN isolation/transceiver | ISO1042 family, correct package/logic supply | Datasheet pinout, isolation and bus-side voltage |
| Isolated power | Converter matched to logic input and transceiver output load | Isolation rating, output tolerance at minimum/peak load, EMI |
| Bus protection | Protection network coordinated with transceiver limits | Clamp voltage/current, capacitance, fault-energy path |
| Backbone attachment | Rated drop connector/cable | Mating-face drawing, drop length, supply/ground/shield |
| Power entry | Fused regulated supply suitable for vessel system | Reverse polarity/transients, inrush, thermal margin |
| Termination | Backbone-end placement only | Existing termination inventory before adding anything |

A USB programming cable, oscilloscope ground or sensor ground can bridge the
isolation barrier. Draw those paths explicitly. Isolation also does not imply
waterproofing, corrosion resistance or EMC compliance. Do not connect an unregulated
24 V vessel supply directly to a nominal 12 V N2K feed.

## 0183 variant

[TI ISO1410](https://www.ti.com/product/ISO1410) is a half-duplex isolated RS-485/
RS-422 transceiver candidate, not a complete certified NMEA 0183 interface.
For a receive-only design, positively disable its driver and verify electrical
compatibility with the exact talker. Separate simultaneous input/output buses may
need separate transceivers; tying outputs together does not create a multiplexer.
Check older single-ended interfaces separately. A/B labels vary between vendors:
match documented signal polarity and terminal function, not letter names alone.
Do not transfer CAN termination values to an 0183 circuit by analogy.

## Worked voltage-drop calculation

For one power path, a 10 m segment carries 0.5 A; a subsequent 5 m segment carries
0.2 A. Assume **0.053 Ω/m per conductor**, uniform temperature and no connector
resistance. Round-trip drop is:

`2 × 0.053 × (10 × 0.5 + 5 × 0.2) = 0.636 V`.

That is a synthetic distributed-load example. Add shared-feed drop, device drop
cables, contacts and worst-case cable temperature. Do not double resistance if the
cable table already specifies loop resistance. Calculate each branch from its real
feed and downstream loads; a center feed is not automatically balanced.

Garmin's [power distribution guide](https://www8.garmin.com/manuals/webhelp/GUID-1415AAD0-FE63-42A6-8F8D-DB713D616122/EN-US/GUID-7803C22A-BA02-4E92-BF60-6038F30EB817.html)
uses its cable resistance and a 1.67 V design-drop limit, with a simplified
LEN-based equation. Its parameters apply to its described system; check the actual
cable/device manuals before using them. The arithmetic helper accepts amperes and
per-conductor resistance, so do not enter LEN directly or apply the loop factor twice.

## Bench observations still required

With power removed, verify topology and termination using an appropriate meter;
under load, measure feed and far-end voltage, startup peaks and thermal behavior.
Check recessive/dominant levels with a suitable isolated/differential measurement
arrangement. Verify controller listen-only support and counters before observation.
A single transmitter with only silent listeners lacks a CAN ACK source. Separate
that expected bench condition from a defective transceiver. Confirm no unexpected
power path appears when USB is connected. Record all conditions in commissioning.
