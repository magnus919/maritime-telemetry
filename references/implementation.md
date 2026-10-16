# Build paths: ESP32, Raspberry Pi and bench integration

These are self-contained design recipes. No companion agent skills are required.
Select actual hardware and pin the dependencies before converting a recipe into
flashable code. No hardware, firmware compilation or live network operation has
been performed merely by installing this skill.

## ESP32 sensor published on N2K

Use the NMEA2000 C++ library with a compatible controller backend. Its examples and
message setters are preferable to hand-packing fields. Record core library,
backend, Arduino/ESP-IDF and board-package versions as one tested combination.
[NMEA2000 project](https://github.com/ttlappalainen/NMEA2000) and
[message API](https://ttlappalainen.github.io/NMEA2000/_n2k_messages_8h.html).

1. Identify the exact ESP32 variant and board revision. Check controller support,
   GPIO restrictions, boot straps, flash/PSRAM connections and peripheral conflicts.
   Verify the transceiver's supply and RX logic levels against the MCU.
2. Draw the bus interface, isolation and power domains. Include programming USB
   and sensor ground; neither should accidentally bypass isolation.
3. Start with a sensor-only acquisition test. Record calibration, physical units,
   range, uncertainty, settling time and open/short/disconnected behavior.
4. Choose the PGN and data instance from the receiving instrument's capabilities.
   Freeze a unique device identity and document nonvolatile configuration ownership.
5. Construct immutable samples with measurement time/validity. Convert once at the
   API boundary and use the library's missing-data representation on sensor failure.
6. Service the stack frequently and use a monotonic scheduler. Avoid blocking
   sensor reads, sleeps or Wi-Fi reconnect loops in the CAN processing path.
7. On an isolated bench, test boot/discovery, measurement scaling, duplicate
   preferred addresses, power cycle, sensor loss and recoveries. Verify no queued
   stale bursts are sent after a pause or bus recovery.
8. Compile and save the binary hash/build log before requesting any flash action.
   Establish bootloader/recovery access, saved settings and a known-good image.

Illustrative application logic, deliberately not board-specific firmware:

```text
setup:
  load validated identity/configuration
  configure stack and supported PGNs
  start sensor and bus only in the authorized test mode
loop:
  service CAN stack
  if sensor acquisition ready: commit sample(value, units, valid, sampled_at)
  if transmit deadline:
    if sample invalid or expired: encode unavailable using selected PGN API
    else: encode physical value and reference/instance
    queue within bounded capacity; record failures
```

Do not replace the stack's address-claim handling with a fixed CAN source byte.
Do not leave copy-pasted example manufacturer/product identifiers in a distributed
product; obtain the applicable assignments and requirements.

## ESP32 sensor over Wi-Fi

If only software consumers need the measurement, SensESP can provide a direct
Signal K path without adding a CAN node. That does not automatically make the
measurement available to an N2K display: an explicit, supported output bridge
would still be needed. Treat Wi-Fi loss, provisioning, credentials and reconnect
freshness as acceptance cases. [SensESP](https://signalk.org/SensESP/).

## Raspberry Pi gateway or chartplotter

Default to a documented isolated marine USB interface for initial integration;
choose a CAN HAT when its schematic, driver, power design and OS support are known.
A bare Pi GPIO header is not an 0183 or N2K connector. Record Pi model, OS image,
architecture, kernel, adapter, firmware and device-tree overlay/oscillator settings.
Use stable serial device paths and explicit permissions, not broad root access.

Plan vessel power conversion, fuse, startup peaks, shutdown/UPS behavior, storage
wear and thermal limits. Do not assume desktop USB power measurements establish
reliable boat operation. Keep recoverable OS media and exported application config.
OpenPlotter can package parts of this ecosystem, but check its current supported
board/OS combinations; historical CAN HAT instructions are not current pinout proof.
[OpenPlotter CAN documentation, historical 2.x](https://openplotter.readthedocs.io/2.x.x/can/can_app.html).

SocketCAN exposes CAN devices as network interfaces. Normal receiving sockets do
not make a controller passive. Configure and verify listen-only at the interface
when the adapter/driver supports it; inspect counters and driver state.
[Linux SocketCAN](https://docs.kernel.org/networking/can.html).

The following is a **reviewable Linux setup pattern**, not a command to run against
an unidentified interface. Changing interface state requires authorization and a
saved prior configuration; stop if listen-only is unsupported.

```sh
ip -details -statistics link show can0
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 250000 listen-only on
sudo ip link set can0 up
ip -details -statistics link show can0
```

Read-only capture then uses the selected adapter's documented tool. Never replace
listen-only with “no application sends” and call it equivalent. A bench containing
only one transmitter and silent listeners may have no node supplying CAN ACK;
provide an intentional normal-mode bench receiver or document that limitation.
Rollback means restoring the recorded state, not always bringing the interface up.

## First end-to-end experiment

For a water-temperature sensor: declare the supported PGN/path, feed three known
values including a fractional value, then unplug the sensor. Compare independent
measurement → sensor sample → encoded bytes → decoder → Signal K → display.
Require correct units/source/instance at all points and explicit unavailable/stale
behavior after unplugging. Record firmware versions and the consumer's actual
support. A complete bench chain remains unverified for vessel environmental use.
