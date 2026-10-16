# Maritime instrument display contract

## Target and provenance

- User/station and decision supported:
- Board, revision, screen, enclosure and power interface:
- Upstream project/commit; application, asset and dependency reuse terms:
- Framework/dependency locks; build result/artifact hash:
- Data route: sensor → gateway → server → display:
- Scope: read-only / separately authorized control. Rollback:

## One row per displayed datum

| Widget | Path/PGN | Type/source/instance | Native → shown units | Reference | Validity | Cadence/expiry | Label/metadata fallback |
|---|---|---|---|---|---|---|---|
| Example wind number | environment.wind.speedApparent | numeric; declared source | m/s → kn | apparent | finite, valid sample | bench 1 Hz / provisional 3 s | explicit apparent wind label |

The example cadence is a bench assumption, not a standard. Record measurement and
arrival time separately. Define null, missing, wrong type, source change, old
replayed timestamp and metadata-change behavior. Specify graph gaps/downsampling,
angle wrap, scale and whether alarms operate on native or displayed units.

## Connection and rendering lifecycle

- Endpoint discovery, auth/transport and provisioning:
- Active-screen subscriptions and background collection:
- Disconnect/reconnect, configuration pause and stale indication:
- Bounded queue/history; heap/render/network measurements:
- Day/night contrast, touch operation and alarm presentation:
- Alarm threshold/hysteresis/acknowledgment versus physical control:

## Evidence

- Independent nominal and boundary vectors:
- Null/wrong-type/stopped-path/heartbeat-only/replay/source-change outcomes:
- Screen switch, long history, bursts, server restart and revoked-access outcomes:
- Compiled / simulated / bench-observed / vessel-observed / not assessed:
- Physical power, enclosure and readability evidence:
- Remaining assumptions and next decisive test:
