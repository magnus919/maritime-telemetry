# Fortification research synthesis — 2026-10-16

## Decision and scope

The skill now has practical implementation depth across the wire, gateway and UI
boundary, with original fixtures, executable fault models, two compiled MCU
examples and a real loopback Signal K lab. Use these to prepare an isolated bench
project. Do not treat the repository as certification or universal device support.
The campaign's full acceptance remains partial because physical commissioning,
licensed normative review and independent agent-output evaluation were not performed.

The [pre-execution scope](fortification-scope.md) froze baseline and permitted
software-only work. The [results](../../evidence/fortification-results.md) record
observations, failed attempts and limitations. No autonomous billable research/model
job was launched. GroktoCrawl supplied 23 bounded retrieval attempts and four
follow-up searches; source-code checkouts and package/build operations are separate.

## Source and claim ledger

The [retrieval register](source-retrievals.json) accounts for every scrape, including
errors returned with a successful command status. Retained raw response hashes are
identifiers, not publicly reproducible archives. No private captures or credentials
were submitted to research services. Only original analysis and fixtures are added.

| Claim / conflict | Evidence and scope | Decision |
|---|---|---|
| 0183 framing/serial profiles | NMEA owner page; GPSD implementation reference | Separate licensed normative requirements from community descriptions |
| Signal K version ambiguity | Pinned spec package.json1.8.4, npm available1.8.2, docs1.7.0 | Pin each layer separately; tested schema1.8.2 |
| PUT requests are actions | Official versioned PUT documentation; local unauthorized PUT401 | Separate request acceptance from physical feedback; no success inference |
| Multiple sources vs instances | Official multiple-values chapter | Preserve stable source identity independently from engine/battery instances |
| Plugins must clean up | Official server-plugin start/stop documentation | Contract documented; no executed lifecycle proof |
| SensESP TLS instructions conflict | Older getting-started vs pinned current platform template | Framework-specific advice only; compiled Arduino recipe does not prove TLS |
| OpenPlotter generation | Official downloading page v4 Debian12/Ubuntu22.04 | Do not mix v3 Bullseye packages; no inferred specific Pi-board certification |
| OpenCPN source priorities differ | Official Data Priorities page | Navigation/heading/Dashboard policies require individual checks; GUI untested |
| Isolation needs power design | TI ISO1042/ISO1410 product pages | Candidate components, separate bus power; no approved NMEA schematic |
| Power-drop limit | Garmin HTML voltage-drop section after PDF retrieval failed | Apply vendor's1.67V design limit within its stated scope; worked segment budget separately |
| Radar support is model-specific | radar_pi maintainer README | Supported-family orientation only; exact scanner/firmware remains prerequisite |
| CAN identifiers don't authenticate senders | Linux SocketCAN and protocol source | Treat bus provenance as observed identity, not authorization |

NMEA2000 and OneNet owner-page retrievals, Garmin/Actisense PDFs, alternate
OpenPlotter site and TI datasheet failed. The Signal K security page was a
`Cannot GET` error and rejected. OpenPlotter landing page was discovery only.
The four searches covered Pi5/Bookworm, alternate OpenPlotter docs, NMEA2000
edition/manufacturer-code ownership and Garmin voltage drop. The first two yielded
no useful hits; NMEA snippets remain discovery leads, not upgraded normative claims;
Garmin led to the retained HTML section. Component datasheets and licensed standards
remain prerequisites to a final circuit/compliance decision.

## Stable run status and remaining acceptance

| Run | Delivered | Status / remaining gate |
|---|---|---|
| R01 | Source/version/claim register and conflict decisions | Documentary slice complete; licensed requirements unresolved |
| R02 | Original heading, AIS and Signal K fixtures with hashes | Core corpus delivered; broader real-world corpus pending |
| R03 | C++ vectors and fake-CAN claim timing/conflict; fast-packet fault model | Partial; exhaustive source transport/ISO TP and physical faults pending |
| R04 | Built C decoder, converted/decoded original fixture in SI | Partial; Rust/dialect/unknown-field comparisons pending |
| R05 | Bounded serial stream tests and actual AIS decoder probe | Partial; executable multipart/tag-block/AIS profile matrix pending |
| R06 | Real local REST/WS/schema/null/reconnect/unauthorized-write lab | Partial; plugin lifecycle/TLS/token lifecycle pending |
| R07 | OpenCPN priority and integration runbook | Documentary only; GUI/receiver observation pending |
| R08 | Candidate isolated topology and tested power arithmetic | Documentary/model only; schematic review and measurements pending |
| R09 | Two compiled ESP32 examples, source pins and recovery boundaries | Compile complete; devices, provisioning and electrical tests pending |
| R10 | Pi/OpenPlotter generation and recovery plan | Documentary only; image install/restore pending |
| R11 | Compatibility matrix and staged integration recipe | Partial; separate stages verified, no end-to-end physical chain |
| R12 | Depth/tank/heading worked examples and arithmetic tests | Synthetic complete; actual calibration and wider domains pending |
| R13 | Relay simulator, duplicate/expiry/feedback/override cases | Model complete; persistent restart protection and real profile pending |
| R14 | Threat model, local write denial, source/clock/replay tests | Partial; TLS/revocation/disk-full/restore pending |
| R15 | Radar-family scope and adjacent-protocol decision reference | Documentary only; scanner/plugin reproduction pending |
| R16 | Extended scenarios, rubric challenges, offline validation | Structural evidence only; baseline/candidate behavioral comparison unexecuted |

## Maintenance and next decisive work

Advance hardware gates only with an exact board/adapter/receiver, versioned manual,
bench wiring and rollback contract. First useful physical run is one sensor through
one isolated adapter to one named consumer, testing unplug/reboot and source conflict.
For software assurance, prioritize Signal K plugin cleanup/token revocation and AIS
multipart adversarial fixtures. For agent assurance, retain generated outputs against
both frozen baseline and candidate with independent assertion-level review; schema
validity and passing utility tests are not substitutes.
