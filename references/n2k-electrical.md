# NMEA 2000: backbone, power and isolation

## Draw the actual topology

N2K uses a linear backbone with short device drops and termination at the two
ends. Diagram every T, termination, power feed, adapter and device; include hidden
terminators on hobby CAN boards. Manufacturer connector systems such as SeaTalkng
require their documented adapters. Original SeaTalk is a different protocol, not
a passive cable conversion. The connector shape alone proves nothing about PGNs.
[Garmin planning guide](https://www8.garmin.com/manuals/webhelp/GUID-1415AAD0-FE63-42A6-8F8D-DB713D616122/EN-US/GUID-5A5B475A-AFE1-4949-9B48-DF1A86BB228F.html).

For a conventional Micro network, Garmin specifies at most 100 m between any two network points (accounting for
end-device drops), 6 m individual drops, 78 m aggregate drops and 50 devices. Cable classes
and arrangements matter; the CAN source-address space is not the permitted
physical node count. Check these against the selected cable system's manual and
licensed standard before approving a design. Use two 120-ohm end terminators.
With power removed and the measurement setup verified, their parallel resistance
is approximately 60 ohms across CAN-H/CAN-L. This is a useful check, not proof of
signal integrity. [Garmin technical reference](https://www8.garmin.com/manuals/webhelp/GUID-1415AAD0-FE63-42A6-8F8D-DB713D616122/EN-US/Technical_Reference_for_Garmin_NMEA_2000_Products_EN-US.pdf).

Do not guess an M12 pinout from a sketch: mating-face and wire-side views mirror
each other. Obtain the connector manufacturer's drawing, verify continuity while
unpowered, and record CAN-H, CAN-L, NET-S, NET-C and shield separately. Preserve
strain relief, environmental sealing and a documented shield/ground arrangement.

## Power is a network design problem

Use the specified nominal 12 V marine network feed with suitable switching and
fusing; do not connect a 24 V vessel supply directly. Inventory devices that may
already feed the backbone before adding power. Multiple supplies require a
manufacturer-supported power-isolation design. Power isolation is not necessarily
galvanic data isolation. Garmin's reference explicitly covers feed positioning and
power isolators; use the actual devices' supply limits rather than a generic CAN
voltage assumption. [Garmin technical reference](https://www8.garmin.com/manuals/webhelp/GUID-1415AAD0-FE63-42A6-8F8D-DB713D616122/EN-US/Technical_Reference_for_Garmin_NMEA_2000_Products_EN-US.pdf).

Use declared LEN (one LEN represents 50 mA) for the network budget, then measure
worst-case behavior of the prototype. Treat display backlights, Wi-Fi bursts,
startup capacitance and relay power separately. Do not assume a Pi can draw its
full power from an arbitrary drop; a separately protected supply may be needed.

Original engineering calculation method:

- Partition the network into feed-to-load segments. Record each segment's
  conductor resistance and worst-case downstream current.
- Compute voltage loss along each complete supply-and-return path:
  `drop = sum(segment_current × segment_loop_resistance)`.
- Add connector/fuse losses and supply tolerance. If the cable specification is
  resistance per conductor, double it for equal supply/return lengths exactly once.
- Compare minimum terminal voltage with each device's documented operating limit
  and the network vendor's voltage-drop limit; label missing values as unresolved.

Example with hypothetical measured/specification inputs: a 10 m segment has
0.05 ohm/m **per conductor** and carries 0.40 A. Its loop resistance is 1 ohm and
drop is 0.40 V. An additional 4 m drop at the same conductor resistance carrying
0.10 A adds 0.04 V. From an 11.5 V feed that device sees at most 11.06 V before
connector losses. This establishes a conditional calculation, not acceptance.

## MCU and Pi interface review

A CAN controller handles arbitration/framing; a transceiver interfaces to the
physical pair. An SPI CAN controller board often contains both, but inspect its
schematic, logic levels, oscillator and termination. An ESP32's TWAI capability
varies by exact part; an external transceiver is still required for the documented
ESP32 interface. [Espressif TWAI documentation](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-reference/peripherals/twai.html).

For an isolated design, draw both data and power isolation barriers. An isolated
transceiver powered from an inappropriate shared rail may leave a galvanic path.
Check USB, programming headers, oscilloscope earth and enclosure grounds. Review
transient protection, reverse polarity, thermal and EMC decisions against component
datasheets. A cheap module that works on a bench is not an accepted marine
interface. Keep bare CAN hardware off the vessel until these paths are reviewed.

Unpowered checks precede controlled power checks. Stop if polarity, fuse sizing,
shield/return separation or supply identity is unresolved. Never make a resistance
measurement on an energized backbone. When observing waveforms, use an appropriate
probe and grounding arrangement; do not bridge an isolation barrier with a grounded
scope clip. Record the instrument configuration with the result.

## Worked implementation

See the [fortification guide](electrical-worked-design.md) for worked examples and explicit execution boundaries.
