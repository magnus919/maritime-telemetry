# OpenCPN: verify the chartplotter experience

OpenCPN is an open-source chartplotter/navigation application, not a wire protocol.
Its supported direct N2K adapters and input paths depend on version/platform.
Consult the current connection documentation and adapter support list before
choosing direct N2K versus a Signal K gateway. [OpenCPN N2K connection guide](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn%3Amanual_basic%3Aquick_start_guide%3Aconnect_to%3Anmea2000).

## Choose one authoritative path per datum

A useful first topology is instruments → isolated interface → Signal K → OpenCPN.
Direct serial or a supported N2K adapter is appropriate when it meets the exact
use case without extra conversion. Avoid simultaneously enabling direct GNSS,
a rebroadcast of that GNSS and a second bridge's copy. Record ownership of
position, heading, wind, depth and AIS separately; they need not share a provider.

Original configuration/acceptance workflow:

1. Record OpenCPN version, OS, connection types, adapter firmware and plugin
   versions. Export or back up the current configuration before edits.
2. Create one input-only connection for the selected transport. For serial, verify
   stable device naming, permissions and speed. For TCP/UDP, verify address, port,
   listener/client direction and what payload is actually carried. A TCP socket
   carrying 0183 text is not a Signal K WebSocket connection.
3. Inspect the incoming data/debug view and compare it with the gateway capture.
   Record input filtering and source priority. Leave all output paths disabled.
4. Check the visible own-ship position, heading/course distinction, instrument
   units and AIS identity. Compare a known event across capture, decoded data,
   application value and chart display.
5. Disconnect the source and verify stale/lost-input behavior; reconnect and
   restart the application. Confirm that duplicate connections did not appear.
6. Only if authorized, configure a specific output path, allowlisted sentences or
   supported control plugin. Verify the recipient and independently observed
   state; a displayed route does not prove the autopilot follows it.

Do not assume every supported input is available to every instrument/plugin.
If a value is present in Signal K but absent on screen, distinguish unsupported
path mapping, plugin capability, filtering, source preference and UI configuration
before changing the sensor's PGN.

## Charts, routes and control are distinct

Charts require suitable data, licensing, coverage and update management. NMEA
telemetry does not carry a chart database or establish chart accuracy. Treat
route planning, exporting a route and commanding navigation as separate actions.
A working chart display or plausible simulated track is not operational acceptance
of an autopilot or navigation system.

For a prototype dashboard alongside OpenCPN, label simulated data, show age and
source, and use explicit unavailable states. Do not silently keep the last-good
position “live.” The application should reveal source failover rather than conceal
it behind a continuous moving marker. Carry these domain acceptance requirements into the UI implementation.

## Radar: model-specific integration

The Radar PI project supports particular Navico, Garmin and Raymarine radars;
compatibility is model-specific. Radar imagery/control commonly travels over
Ethernet, with its own discovery and network requirements. NMEA heading/position
can support an overlay without carrying the image. Check the exact scanner against
the plugin's support list and documentation, not just the brand name.
[Radar PI project](https://github.com/opencpn-radar-pi/radar_pi).

Use a dedicated test plan for scanner power, network interface, multicast/routing,
heading alignment and control ownership. Do not activate RF transmission as a
side effect of testing a telemetry dashboard. On a bench, use a supported recorded
or simulated input when available. Distinguish tracked-target sentences from the
radar image: OpenCPN's radar-target documentation describes target integration,
which does not imply generic scanner support.
[Radar targets](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn%3Amanual_advanced%3Aais%3Aradar_targets).

Plugins extend capabilities but have their own releases and device constraints.
Use the application's supported plugin manager and pin/document the installed
version. Installation is not proof of interoperability.
[OpenCPN plugin catalog](https://opencpn.org/OpenCPN/info/downloadplugins.html).
