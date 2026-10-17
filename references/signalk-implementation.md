# Signal K: implement and verify an application

## Version contract

On 2026-10-16, the inspected specification source commit
[fb628fb](https://github.com/SignalK/specification/tree/fb628fb4ee569149fd3810b271d0f987428b4703)
identified package version 1.8.4. The public latest-doc entry yielded 1.7.0. An npm
install of schema 1.8.4 failed because that version was not published; npm reported
1.8.2, which was installed for the lab. These are separate artifacts, not competing
claims that one number is the universally current Signal K version. Record schema
package, documentation snapshot, server release and plugins independently.

## Full-server lab status: quarantined

The former [full-server lab](../examples/signalk-lab/README.md) used server2.33.0,
schema1.8.2 and ws8.18.3. Its earlier discovery/REST/WebSocket/null/reconnect/PUT
results are historical software evidence, not a current security recommendation.
Compatible dependency refreshes left known advisories, so the current installer,
lockfile and runner were removed. Do not run the old `npm ci`/`node lab.cjs` recipe.
See the [remediation record](../evidence/dependency-remediation.md).

The [AIS mapping lab](ais-n2k-laboratory.md) remains executable and CI-tested with
a clean npm audit. It uses real mapping/converter functions and an event bus; it
does not boot a Signal K server or verify HTTP/WebSocket/authentication behavior.
Those server checks must be re-established after a supported remediation exists.

## Producer, metadata and client responsibilities

A producer sends a delta containing a context, source, timestamp and values. Use a
stable source label, genuine measurement time and native schema units. Use `null`
for unavailable observations where the path/schema allows it; suppressing a broken
sensor forever leaves clients needing their own expiry. Don't report an observation
with PUT: PUT requests an action. The [spec PUT chapter](https://signalk.org/specification/1.7.0/doc/put.html)
distinguishes these operations and describes source-disambiguation requirements.

Discover endpoints from `/signalk`; don't assume every deployment uses port 3000,
plain HTTP, or the same proxy path. For a bounded client, connect to the discovered
WebSocket endpoint with `subscribe=none`, then request explicit context/path subsets.
Read the server's actual supported subscription policies. A requested interval is
not sensor sampling cadence, and cached resend is not a new measurement. See the
[subscription protocol](https://signalk.org/specification/1.7.0/doc/subscription_protocol.html).

Store the tuple `(context, path, source, measurement time, arrival monotonic time,
value, validity, metadata version)`. Select a source before flattening to a widget.
Multiple instances (port/starboard engines) and multiple sources for the same path
are different problems. Preserve instance paths; don't merge banks just because
both report voltage. [Multiple values](https://signalk.org/specification/1.7.0/doc/data_model_multiple_values.html).

Fetch metadata for units/description and handle metadata changes explicitly. A
numeric temperature is kelvin only when the schema/custom-path contract says so.
A custom path containing “temperature” does not authorize guessing its units. Keep
structured position and datetime paths typed; don't cast every value to float.
Notifications need state, method and acknowledgment policy separate from the
underlying observation. Do not silently rearm an alarm on reconnect replay.

## Plugin lifecycle

The [server plugin contract](https://demo.signalk.org/documentation/develop/plugins/server_plugin.html)
provides identity/schema/start/stop hooks. Keep timer and subscription handles so
`stop()` can cancel them, close devices and complete asynchronous cleanup. Configuration
changes may stop/start a plugin; a second start must not leave duplicate publishers.
Use `app.handleMessage` for measured state. Register a PUT handler only for a
deliberately supported command path; return request state separately from physical
feedback. Configuration schemas validate settings, not the truth of sensor data.

Minimal original design sketch, not a deployed plugin:

```javascript
module.exports = app => {
  let timer;
  return {
    id: 'synthetic-example', name: 'Synthetic example',
    schema: () => ({type: 'object', properties: {}}),
    start: () => {
      clearInterval(timer);
      timer = setInterval(() => app.handleMessage('synthetic-example', {
        context: 'vessels.self', updates: [{
          timestamp: new Date().toISOString(),
          values: [{path: 'environment.water.temperature', value: 293.15}]
        }]
      }), 1000);
    },
    stop: () => { clearInterval(timer); timer = undefined; }
  };
};
```

The constant is explicitly synthetic; do not install it alongside real navigation
or sensor sources without labeling and source selection. The historical server lab exercised
input delivery, not this plugin's lifecycle; it is now quarantined.

## Reconnect and authorization matrix

| Event | Application response | Evidence needed |
|---|---|---|
| Connection closes | Mark affected stream disconnected; retain last value only as stale/history | Socket failure and expiry test |
| One path stops, socket lives | Expire that path independently | Heartbeat-only fixture |
| Reconnect with cached data | Evaluate original timestamp; refresh metadata/subscriptions | Old timestamp replay |
| Source changes | Apply declared precedence/hysteresis or expose selection | Two-source fixture |
| Token revoked/expired | Stop writes and reauthorize through supported flow | Actual auth lifecycle test |
| Server restart/config reload | Restore subscriptions once; no duplicate alarms/publishers | Restart and plugin-stop tests |

The lab verifies anonymous PUT denial but **not** token revocation, TLS, all policies,
notifications, metadata mutation or plugin restart. Those remain separate acceptance
cases. Never substitute a schema-valid delta for evidence of those behaviors.
