# Independent N2K implementation worksheet

- Intended scope: offline decoder / sensor publisher / full node / gateway
- Language, controller, driver and explicit unsupported features:
- Source study commit, normative sources available, license obligations:

| Layer | Invariant / declared policy | Evidence source | Positive vector | Contradictory or malformed case | Result |
|---|---|---|---|---|---|
| Frame boundary | Extended Classical CAN data frame, bounded DLC | | | RTR/error/flags | |
| Identifier | PF-dependent PGN/destination | | | Nonzero low byte in PDU1 PGN | |
| Numeric fields | Width, endian, signedness, scale, rounding, status | | | NA/OR/reserved/short buffer | |
| Transport | PGN classification and bounded assembly | | | Loss/interleaving/wrap/timeout | |
| Identity | Unique NAME; address is changeable | | | Conflict/equal NAME | |
| Node management | State-dependent transmission and request handling | | | Claim interval/restart/fault | |
| Scheduling | Bounded queues and service latency | | | Starvation/backpressure | |
| Consumer | Actual target behavior and source selection | | | Unsupported PGN/staleness | |

- Which behaviors are upstream choices rather than required protocol rules?
- Which expected vectors were computed independently of the implementation?
- What disagreement exists between hand vectors, upstream, another decoder and hardware?
- What has only been inspected, compiled, unit-tested, simulated, or physically tested?
- Remaining conformance requirements, uncertainties and next decisive test:
