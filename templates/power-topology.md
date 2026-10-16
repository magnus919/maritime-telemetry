# Topology and power review — filled arithmetic example

Status: synthetic calculation only; no approved physical design.

```text
feed → segment A (10 m, 0.5 A) → tap (0.3 A) → segment B (5 m, 0.2 A) → load
```

| Segment | One-way length | Per-conductor resistance | Downstream current | Round-trip drop |
|---|---:|---:|---:|---:|
| A | 10 m | 0.053 Ω/m | 0.5 A | 0.530 V |
| B | 5 m | 0.053 Ω/m | 0.2 A | 0.106 V |
| Farthest path | | | | 0.636 V |

Before adapting, replace assumptions with exact cable data, temperature, contact
resistance, drops, shared feed/inrush and measured loads. Record allowable drop and
minimum device voltage from applicable manuals. The calculation uses amperes, not LEN.

- Vessel voltage and approved power conversion/fuse:
- Connector part/revision and mating-face drawing:
- Backbone ends/terminators, drops and existing feeds:
- Shield/ground/isolation diagram including USB and sensors:
- Selected transceiver/converter ratings and datasheet sections:
- Voltage at feed/farthest device during startup and maximum load:
- Instrument/probe grounding and measured bus levels:
- Faults, rollback and unresolved requirements:
