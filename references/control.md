# Actuators, digital switching and navigation control

This is a recommended control-design process. It is not a generic control protocol
or a promise that a given commercial product accepts an available PGN. NMEA's
public overview includes commands/status, but an individual device's supported
commands, ownership rules and interlocks remain essential.
[NMEA 2000 overview](https://www.nmea.org/nmea-2000.html).

## Observe, request, confirm

Separate three values: desired state, accepted command and observed physical
state. A decoded status PGN cannot safely be reused as a command. An accepted
network write is not proof that a motor moved or a relay energized. Establish the
command interface from the exact product/firmware documentation and supported
integration, particularly for autopilots and proprietary switching systems.

Before generating a control implementation, record:

- Target bank/channel/device and unambiguous identity; address changes must not
  redirect a command to a different device.
- Source of authority and operator mode: disabled, armed, local manual, remote
  authorized, faulted. Define precedence and transition rules.
- Range, rate, duration and freshness limits, plus behavior on duplicate, delayed,
  out-of-order and reconnect-delivered commands.
- Independent feedback: actual contact, current, position or vendor-reported state
  appropriate to the mechanism. Explain what each feedback signal cannot prove.
- Interlocks, timeout/watchdog and physical manual override. “Off” is not universally
  a safe fallback for bilge pumps or other essential equipment; decide per function.
- Recovery and rollback: hardware disable/removal, original controller, saved
  configuration and named person able to intervene.

For Signal K, implement control through the documented PUT/handler mechanism with
permissions and request tracking. Publishing a new telemetry value must not be
misrepresented as a physical action. Protect the write surface separately from
read-only dashboards. [Signal K PUT](https://signalk.org/specification/1.7.0/doc/put.html).

## Staged test plan

1. **Offline:** validate target binding, state transitions and rejection rules.
   Exercise stale command, wrong source, disabled state, repeated request and
   invalid range. No live gateway is attached.
2. **Dummy load:** use an isolated bench with a low-energy indicator or equivalent
   simulator. Log request, response and independent observation with time bounds.
3. **Fault injection:** disconnect network, reset the controller, drop feedback,
   duplicate the request and restore power. Verify no surprise command replay.
4. **Bounded physical test:** only after explicit authorization for the particular
   target, duration and recovery arrangement. Preserve manual control and stop on
   behavior outside the accepted envelope.
5. **Acceptance:** record expected versus observed state, latency and faults for
   the named firmware. Retain failures as evidence, not just successful toggles.

A generic example “turn channel 3 on” is not ready for transmission until bank,
source identity, units/encoding, authority and hardware role are known. Never
probe unknown PGNs or enumerate commands on a live vessel to discover behavior.

## Autopilots and essential systems

Treat navigation data output and mode/steering control separately. A plotter may
emit route guidance but the pilot can require operator engagement, proprietary
mode commands or source configuration. Confirm supported control plugin/model
and independent rudder/motor behavior; do not infer capability from heading display.

Avoid adding a prototype as the sole protective control for steering, propulsion,
bilge, fire suppression or other essential functions. This is a project architecture
constraint: preserve the existing independent function while proving the new path.
Stop on unexpected actuation, lost manual override or uncertain target identity.

## Worked implementation

See the [fortification guide](security-and-controls.md) for worked examples and explicit execution boundaries.
