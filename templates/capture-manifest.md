# Capture and fault-injection manifest

Filled example: `fixtures/heading.candump`, original synthetic frame, MIT. Format:
SocketCAN candump log, raw eight-byte CAN payload; UTC capture timestamp; source 35,
PGN 127250. Expected heading/deviation/variation: 1.0/-0.1/0.2 radians. No vessel,
radio, device serial or real position was observed. SHA-256 is in fixtures/manifest.json.

For a new capture record:

- Artifact/hash/size/license and collection authorization:
- Raw frames versus assembled messages; format/dialect:
- Tool/version/adapter/firmware, filters and dropped-frame counters:
- Measurement time versus arrival time, clock synchronization/rollover:
- Source identity/instances and address-claim history:
- Known independent input/oracle and expected output:
- Fault injected, seed/position/order and expected rejection:
- Redactions, recomputed checksums and relationship to private original:
- Consumer observation, result, limits and next decisive measurement:
