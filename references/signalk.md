# Signal K: open application data and APIs

Signal K provides an open vessel data model and API specification. The Signal K
Server is an implementation and plugin host, not the specification itself. It can
collect different marine inputs and expose JSON to local applications. SensESP
provides an ESP32-oriented sensor path. [Server documentation](https://demo.signalk.org/documentation/)
and [SensESP documentation](https://signalk.org/SensESP/).

## Contract before configuration

Record the schema/API version, server release, input-provider versions and
output-plugin versions separately. Map each measurement to an existing key in the
selected schema before inventing a custom path. Confirm units using key metadata:
angles typically use radians, speeds m/s and temperatures kelvin; position uses
latitude/longitude degrees. Apply display conversions at the presentation boundary.
[Signal K specification entry point](https://signalk.org/specification/latest/).

The full model represents current state; deltas carry updates in a vessel context.
Preserve source and timestamps through transformations. Do not give an old value a
new measurement timestamp merely because a bridge forwarded it. Receipt time can
be retained separately. Source selection and freshness must be explicit; a cached
value is not automatically current. [Full and delta models](https://signalk.org/specification/1.7.0/doc/data_model.html)
and [source representation](https://signalk.org/specification/1.7.0/doc/sources.html).

Original illustrative delta for a bench fixture (not live vessel data):

```json
{
  "context": "vessels.self",
  "updates": [{
    "source": {"label": "bench-temperature"},
    "timestamp": "2026-10-16T12:00:00Z",
    "values": [{"path": "environment.water.temperature", "value": 293.15}]
  }]
}
```

Confirm context resolution and the path against the deployed schema. This is
20 °C, not 293.15 °C. Use a source label that identifies the actual provider and
retain N2K identity/instance or 0183 input information where supported. Do not map
a cabin sensor to water temperature just because the display supports that path.

## Read-only application bring-up

1. On a local instance selected by the user, discover endpoints with `GET /signalk`.
   Use advertised URLs and API versions; do not assume every server uses port 3000.
2. Fetch a known path from the advertised HTTP API and inspect value, metadata,
   source and timestamp. Separate “path absent” from null/unavailable and stale.
3. Open the advertised WebSocket endpoint and inspect hello/version/self identity.
   Start with `subscribe=none`, then subscribe to only required paths. Cached
   initial values need their original age checked.
4. Exercise reconnect with bounded backoff. Clear any “live” indicator on loss,
   and rebuild subscriptions deliberately. Do not queue control requests for
   automatic delivery after reconnect.
5. Verify the application presents units, source and stale/invalid state correctly
   before enabling an outbound converter or configuring control support.

Read-only example against an already-authorized local server:

```sh
curl --fail --silent --show-error http://localhost:3000/signalk
```

The port is an example. Supply credentials through the deployed client's secure
mechanism, keep them out of command transcripts, and never send private vessel
captures to a public demo. [REST discovery](https://signalk.org/specification/1.7.0/doc/rest_api.html),
[streaming API](https://signalk.org/specification/1.7.0/doc/streaming_api.html).

## Server connection and plugin design

Recommended integration procedure: back up configuration; name each input by
physical source; enable one input; verify the data browser; apply source priorities;
then add one consumer. Install only the needed, pinned providers/converters.
Inspect their permissions, output direction and startup defaults. A second plugin
may create a loop even when the first connection is input-only. Recheck behavior
after server restart and plugin upgrade. Server management procedures should follow
the installed release's documentation. [Signal K Server](https://github.com/SignalK/signalk-server).

A dashboard update is not an actuator command. The PUT/request-response interface
is a separate path with permissions, request identity and possibly asynchronous
completion. Require the actual target handler and independently observed device
state; an HTTP success or accepted request alone does not prove relay movement.
Reject unsupported/ambiguous sources rather than broadcasting commands.
[PUT requests](https://signalk.org/specification/1.7.0/doc/put.html).

Keep the server's write capability off untrusted Wi-Fi and public networks. Apply
least privilege to plugins and clients; review the deployment and authentication configuration against the installed
server documentation. Save a rollback snapshot before enabling conversion
or control, and verify that rollback also disables any persistent output service.

## Practical consumer example

See [the ESP32 display case study](signalk-display-case.md) for a configurable
Signal K consumer, pinned upstream source observations, a wind-display example
and the tests needed to adapt it to other instrument panels.

## Worked implementation

See the [fortification guide](signalk-implementation.md) for worked examples and explicit execution boundaries.
