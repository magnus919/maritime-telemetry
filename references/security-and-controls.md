# Security, control and operational failure boundaries

## Trust model

Map four distinct boundaries: instrument bus, gateway host, local application
network, and optional remote access. An ordinary CAN identifier/source address is
not cryptographic authentication. A gateway that accepts Wi-Fi commands can extend
network access into physical actuation even if the original bus is isolated from IP.
A plugin runs with the host application's capabilities; installing one changes that
trust boundary. Keep observation and command routes separately inventoryable.

The [Signal K security specification](https://signalk.org/specification/1.7.0/doc/security.html)
describes transport protection and tokens. The live server's settings determine
actual enforcement. In the executed local lab, token security allowed read-only
access and rejected anonymous PUT with 401. That is not proof of TLS, authorization
for every path, revocation or protection on a vessel network.

Provision devices on a controlled local network; change public setup passwords,
minimize the time a provisioning AP remains available, and keep secrets out of
URLs, logs and shared configuration. Use the deployment's supported TLS path or a
documented constrained network architecture; do not disable TLS globally because
an older example could not connect. The [embedded build guide](embedded-recipes.md)
explains the SensESP version distinction found during research.

## Control state machine

The [PUT chapter](https://signalk.org/specification/1.7.0/doc/put.html) separates a
request to act from a delta reporting state. The lab's `RelayModel` is an original
application model, not the exact Signal K request-state enumeration:

```text
request → rejected / busy / accepted
accepted → achieved (fresh matching independent feedback)
accepted → timeout / overridden
same ID + same intent → prior result; no second action
same ID + changed intent → reject conflict
```

Freeze target/source, allowed range, expiry, interlocks, manual override and expected
feedback before implementing a command handler. Don't retry an uncertain command
as a new request ID: a delayed first command may still execute. Idempotency must be
implemented at a boundary that can actually prevent duplicate physical action;
an HTTP client's cache cannot establish that alone.

The [control worksheet](../templates/control-state.md) includes the replay ledger
and restart policy. The in-memory model expires requests, rejects conflicting IDs,
requires boolean feedback and stops on override. Its ledger is deliberately bounded
and refuses new requests when full. A deployed service needs durable identifiers,
retention rules, authorization and an independent feedback channel. The model's
caller-provided interlock/feedback values are test inputs, not trusted sensors.

## Fault tests and expected observations

| Fault | Required distinction / containment |
|---|---|
| Token expired/revoked | Authentication failure versus transport loss; no silent privilege fallback |
| Command response lost | Unknown action result versus failure; inspect feedback before retry |
| Feedback stuck at desired state | Old state versus post-command observation; require fresh correlated evidence |
| Host restarts | No replay of queued commands by default; reconstruct pending outcome deliberately |
| Wall clock jumps | Monotonic deadlines remain bounded; measurement-time errors exposed |
| Disk full | Bounded logging failure cannot stall bus servicing or hide command uncertainty |
| Bridge reconnect | No burst of expired commands; telemetry coalescing policy is not command policy |
| Manual override | Local authority wins; stale network command cannot immediately undo it |

These are acceptance requirements. Only the named model cases and anonymous PUT
check have executed evidence; token revocation, storage failure and physical watchdog
behavior need target-system tests.

## Capture privacy and recovery

Before sharing captures, identify position/time tracks, MMSI/NAME/serial identifiers,
credentials and user-defined labels. Prefer synthetic examples. If redacting a
sentence, recompute checksums and label it transformed; changing CAN payload bytes
without preserving scale/fragment consistency destroys diagnostic meaning. Keep
original hashes and transformation notes without publishing private originals.
Record configuration backup, restoration commands, verification observations and
rollback owner. Recovered application uptime alone does not prove sensor source,
units, freshness or actuator state have recovered correctly.
