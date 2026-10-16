# Maritime device / feature contract

- Intended user outcome:
- Scope: observation / publication / configuration / actuation
- Hardware models, revisions, firmware, OS and dependencies:
- Intended consumer and documented receive capability:
- Evidence authority: licensed standard / manufacturer / project source / inference
- Missing facts that block pin-specific or live work:

## Physical network

- Diagram: backbone, drops, terminators, feeds, gateway and isolation barriers
- Connector drawing and viewing direction; verified signal/power/shield labels
- 0183 direction, baud, framing, isolation and receiver loading
- N2K cable system, lengths, node count, declared LEN and power path calculation
- Protection, USB/programmer paths, environmental and recovery provisions

## Data contract

| Physical quantity | Source/identity/instance | Sentence/PGN/Signal K path | Units/reference | Valid/invalid | Sample/transmit rate | Expiry | Consumer evidence |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

- Source precedence and failover:
- Mapping loss, precision and unsupported metadata:
- Queue bounds, drop behavior and counters:
- Identity/configuration persistence:
- Directed bridge graph and loop prevention:

## Control contract (only when applicable)

- Explicit target, authority, arming and manual override:
- Command vs accepted state vs independent physical feedback:
- Bounds, interlocks, duplicate/stale/reconnect rejection:
- Function-specific failure state:

## Acceptance and rollback

- Predeclared thresholds and physical oracle:
- Offline cases, bench cases, vessel observation scope:
- Authorized target, scope and rollback evidence:
- Removal path that preserves backbone termination and original equipment:
- Saved settings/images and restoration verification:
- Conclusion: accepted for stated conditions / conditional / rejected / not tested
