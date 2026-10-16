# Translation and application architecture

The following is a recommended engineering design, not a normative standard.

## Separate the three boundaries

```text
physical instrument network
  NMEA 0183 serial | NMEA 2000 CAN
             ↓ isolated interface
  decoder and semantic/source mapping
             ↓  Signal K data model / API
  recorder | dashboard | OpenCPN
```

An interface can carry raw bytes without translating their meaning. A protocol
converter changes the representation and may lose precision, metadata or whole
message types. Signal K can unify data for applications; it cannot make an
unsupported commercial instrument understand a new measurement automatically.

For every conversion, specify input identity and field, output path/PGN/sentence,
units, reference, validity, rate, timeout, precedence and loss. Maintain separate
receive and transmit lists. Use the translation-matrix template and test one row
at a time before enabling a complete bridge.

## Preserve meaning

- Convert kelvin/°C, radians/degrees and m/s/knots once. For reference,
  `°C = K - 273.15`, `degrees = radians × 180/π`,
  `knots = (m/s) × 3600/1852`.
- Keep heading versus course, magnetic versus true, apparent versus true wind,
  water versus ground speed and transducer versus keel/surface depth distinct.
- Do not synthesize GNSS quality or current UTC from a rapid position packet
  alone. Carry unsupported quality as unknown; require the missing source message.
- Choose source precedence by intended measurement and quality, with explicit
  failover/hysteresis. “Last packet wins” can oscillate between disagreeing sensors.
- Resolve device identity/instance collisions before flattening values into a
  dashboard path. Preserve enough provenance to explain which tank or bank it is.
- Retain raw observations when useful for diagnosis, but bound retention and
  protect location tracks, MMSIs, device serials and credentials from publication.

Example bridge contract: serial RMC ground speed maps to
`navigation.speedOverGround`, converting knots to m/s, only for valid input. It
does not supply speed-through-water. A timestamp assembled from RMC's date/time
must pass the project's clock and rollover checks. The consuming UI applies its
own stale threshold without changing the original timestamp.

## Prevent feedback loops

Use a directed graph of ports/providers, not a flat list of connections. Label
which edges may transmit. For each datum, choose an authoritative input and a
single intended output route. Do not return a locally generated output to its
origin through another gateway. Preserve origin metadata where possible; use
explicit routing and allowlists where a wire format cannot preserve it.

Content-only deduplication can drop genuine constant readings. TTL alone only
slows some loops. Test the graph with two active bridges, a restart and a duplicate
input. Count messages at each edge: unexplained multiplication indicates a loop
or republishing bug. Rate limits are containment, not a substitute for fixing it.

A gateway from 250 kbit/s CAN to 4800-baud serial must select what to forward.
Bound queues by age as well as length. Prefer dropping superseded telemetry to
presenting old values as current, and expose drop/age counters. Control traffic
needs a separate handling policy; do not coalesce commands as if they were samples.

## Architecture decisions

| Requirement | Prefer | Evidence still needed |
|---|---|---|
| Observe existing boat instruments | Isolated input gateway and recorder | Capture health, data semantics, source identity |
| New wired sensor consumed by MFD | MCU with mature N2K stack | Receiver PGN/source support and bench behavior |
| New sensor consumed by web app | Signal K producer, e.g. SensESP | Schema path, security, freshness/reconnect |
| Legacy display | Explicit N2K/Signal K → 0183 mapping | Consumer sentences, throughput and loss |
| Chartplotter experience | OpenCPN supported input path | Actual instrument/connection/plugin support |
| Radar overlay | Model-specific Ethernet/plugin path | Scanner compatibility and heading alignment |

Keep a record of rejected alternatives and the condition that would change the
choice. A smaller prototype can be useful before a complete vessel redesign.

## Broader standards boundary

NMEA OneNet is a separate Ethernet-oriented standard; it is not synonymous with
Signal K, arbitrary IP-carried 0183, or a proprietary radar link. Use it as a
research route when a target explicitly supports OneNet. This skill does not
claim to implement OneNet. [NMEA OneNet](https://www.nmea.org/nmea-onenet.html).
Likewise, a CAN-equipped engine may speak J1939 or a proprietary bus rather than
N2K. Verify the engine gateway contract; do not bridge raw frames between buses
because both use CAN.
