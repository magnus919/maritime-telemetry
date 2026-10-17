# Raspberry Pi, OpenPlotter and consumer integration

## Choose and freeze the installation

The current [OpenPlotter download documentation](https://openplotter.readthedocs.io/latest/getting_started/downloading.html)
identifies the v4 family and its Debian 12 Bookworm / Ubuntu 22.04 base requirements;
it warns against forcing v4 over a v3/Bullseye installation. This supersedes the old
2.x orientation link for a new setup. Freeze the actual image filename/checksum,
board support list, architecture and package versions: the documentation page alone
does not establish that any named Pi revision works with every HAT.

Starting, Headless and Touchscreen editions differ in services and configuration.
Headless defaults in the retrieved page include an access point and remote access;
replace public defaults during commissioning. Desktop installation lacks some
GPIO-specific applications. Don't confuse “runs on Debian desktop” with tested Pi
power, GPIO, CAN oscillator or shutdown behavior. No Pi image was flashed here.

For a maintainable minimal gateway, inventory OS/kernel, interface serial/firmware,
CAN bitrate/controller mode, Signal K server/schema/plugins and OpenCPN/plugins.
Use stable `/dev/serial/by-id` identities where provided; record USB devices without
unique serials as an explicit ambiguity. Match udev rules narrowly and grant the
service only required device access. Do not solve a permission error by running
all applications as root or granting world-write on serial devices.

## Service and recovery contract

1. Capture installed versions, image hash and current configurations before updates.
2. Separate capture files from OS/application storage; define maximum retention,
   rotation and disk-full behavior. Record dropped samples instead of blocking the
   protocol loop behind slow disk writes.
3. Order startup so the application tolerates absent/replugged interfaces. A USB
   device can disappear after boot; startup dependencies alone do not handle that.
4. Restore configuration and identity together. A restored device must not duplicate
   another node's NAME, source label or instance. Back up credentials separately
   from the shareable configuration example.
5. Exercise restart, adapter removal/replug, no Wi-Fi, wrong system time and full
   storage on the bench. Measure power/UPS/shutdown behavior on actual hardware.

Use [deployment/recovery template](../templates/deployment-recovery.md). A service
restart that restores a process but silently changes source priority has not restored
the intended user outcome.

## OpenCPN connection and priority recipe

The [priority manual](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:manual_basic:set_options:connections:data_priority)
is the source for the following **documented, not locally GUI-tested** workflow.
Freeze OpenCPN, OS and Dashboard versions before recording screen-level instructions.

- Create one input connection of the documented type for the selected adapter/server.
  Initially disable output routes; identify the actual source and message in the
  connection/debug view before enabling a second input.
- Set Position Priority first. The manual describes position-linked ordering for
  speed/course, magnetic variation and satellite data; heading is configured
  separately. Verify each category after adjusting position.
- Stop the preferred synthetic source, observe fallback, then restore it and observe
  recovery. Restart OpenCPN to test saved ordering. Record source address/identity
  changes rather than assuming an old row still identifies the same device.
- Test Dashboard separately. The manual describes additional protocol/source
  selection for instruments outside OpenCPN's main navigation priorities. A heading
  selection test cannot prove depth/wind selection.
- For duplicate legacy data, use explicit input filters at the appropriate boundary;
  source filtering in Signal K may be needed before data reaches a consumer.

The same “depth” may arrive by N2K, Signal K and 0183 with different offsets. Compare
semantic values and source provenance before choosing a route. Don't turn on every
path because each connection individually works.

## Three integration recipes and their evidence levels

| Recipe | Concrete artifacts | Current evidence |
|---|---|---|
| Capture → CANboat → application semantics | Original heading capture, C-tool command, expected SI fields; historical server lab demonstrated delivery separately; now quarantined | Individual stages executed; full-server lab quarantined; no current complete server chain |
| ESP32 → N2K → commercial instrument | Pinned compile-only project; device/translation contracts | Firmware compile; bus disabled; no consumer pass |
| Pi gateway → OpenCPN | Current installation source, selection workflow, recovery and compatibility templates | Documentation-based; no Pi or GUI observation |

Use [compatibility matrix](../templates/compatibility.csv). A vendor manual's PGN
list earns `documented`, a source inspection earns `source-inspected`, and only an
actual receiver observation earns `bench-observed`. Do not collapse those categories.
