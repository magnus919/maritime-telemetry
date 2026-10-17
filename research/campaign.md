# Research and fortification campaign

Status: **software and documentary fortification executed; full campaign partial**.
See the [execution ledger](runs/fortification.md) for results and remaining gates.
The subsequent [AIS/N2K run](runs/ais-n2k.md) deepens R02–R06/R11 with native AIS
fixtures, conversion evidence and target-state handling; physical acceptance remains open. Run IDs are stable. Planning baseline and
findings: [audit](audit.md). Discovery evidence: [reconnaissance](reconnaissance.md).
This campaign is self-contained; no companion agent skills are runtime dependencies.

## Delivery order

| Wave | Runs | Exit artifact |
|---|---|---|
| Foundation | R01, R02, R16 design | Claim registry, licensed fixture corpus, frozen evaluation protocol |
| Wire and data | R03, R04, R05, R06 | Tested protocol behaviors, offline decoder pipeline, local Signal K lab |
| Build and consume | R08, R09, R10, R07, R11 | Three reproducible recipes and a versioned compatibility matrix |
| Domain and assurance | R12, R13, R14, R16 execution | Calibrated measurement examples, control simulator, recovery/security tests, evaluated agent outputs |
| Specialized expansion | R15 | Supported advanced profiles with explicit unresolved boundaries |

R01 feeds every run. R02 supplies fixtures to R03–R07 and R11. R08 precedes
hardware integration in R09/R10; compile-only work can proceed earlier. R11 joins
R04/R06/R07/R09/R10. R13 requires R06/R11 contracts before any actuator experiment.
R14 threat modeling starts with R01; its execution uses the finished applications.
R16 designs the evaluation before improvements and executes after each wave.
Dependencies are artifact requirements, not instructions to spawn parallel agents.

## Research execution contract

For every run, copy [run worksheet](run-template.md), freeze the question and
acceptance criteria, then use GroktoCrawl **search → retrieve → inspect → targeted
follow-up**. Start at official documentation/source; use community discussions to
find failures, then verify with the relevant release or an experiment. Follow
links to concrete sections, commits and component manuals, not only homepages.

Use the configured GroktoCrawl service without baking its address or credentials
into this repository. Inspect live capabilities before using its autonomous
research API. On 2026-10-16 it advertised 3 searches, 8 sources, 256,000 source
bytes, 180 seconds and 64 model calls per admitted run. These are service limits,
not proof of research completeness and not a dollar-price estimate. The CLI's
`research create` accepts an objective and idempotency key; do not invent budget
flags. Verify whether tighter bounds in an objective are actually enforceable.
If they are not, use manually bounded search/retrieval instead.

**Default research slice:** at most 3 search queries and 8 retrieved sources,
then a synthesis checkpoint. Each run below allows at most two slices (6 searches,
16 source retrievals) before a scope/review decision. This is a campaign cap of
96 searches/256 retrievals if every run uses both slices, not a target. Repeated
retrievals count. A source-code checkout is separately recorded with commit and
files inspected; don't crawl an entire repository to bypass the source cap.

Do not start billable model research without a recorded cost ceiling and a way to
observe/enforce it. No dollar ceiling or provider spend is authorized by this
planning document. Manual retrieval can remain useful independently. Retain run
IDs, actual counters and termination reasons. Poll with bounded waits and use
status/resume after interruptions; never duplicate an uncertain admission under a
new idempotency key. Cap technical reproductions at one selected version/platform
initially and three non-converging diagnostic attempts. Missing hardware or a
licensed standard produces a scoped partial result, not a simulated physical pass.

Every completed run delivers: focused reference changes, a claim/source ledger,
one worked artifact, its verification evidence, relevant output-quality cases,
and an explicit list of unresolved claims. A source count or crawler quality score
never closes a technical question. Keep third-party licensing and attribution;
store original analysis and licensed fixtures, not bulk copied specifications.

## R01 — Authority, version and claim baseline (P0)

**Question/hypothesis:** can each consequential recommendation be traced to an
applicable authority and version? Today the source table cannot answer that alone.

**Research:** query NMEA's current owner pages for editions/errata and certification
boundaries; resolve Signal K schema/docs tags separately from server releases;
inspect OpenCPN, CANboat, SensESP and OpenPlotter release documentation. Start from
[existing sources](../references/sources.md). Search angles: `Signal K specification
release schema version`, `OpenPlotter current documentation supported Raspberry Pi`,
`NMEA 2000 certification manufacturer code official`. Inspect licenses before
extracting code or fixtures. Record unavailable normative requirements rather than
inventing them from community definitions.

**Deliver:** `sources.md` renewal, claim ledger, version matrix, conflict log and
refresh policy. Add component/manual sources as downstream runs identify targets.
**Acceptance:** each high-consequence electrical, transmission, control and semantic
claim has a specific section/symbol or an explicit unresolved flag. Resolve or
bound the current Signal K latest redirect, historical OpenPlotter and ESP-IDF
applicability. “Licensed source needed” is a valid unresolved dependency, not closure.
**Stop:** inaccessible authoritative text remains flagged after one alternate
primary route; do not seek unauthorized copies.

## R02 — Capture corpus and experiment framework (P0)

**Question/hypothesis:** can one dataset drive independent, repeatable checks across
wire decoders, gateway semantics and consumers?

**Research:** inspect CANboat samples/tests, NMEA2000 host tests and Signal K sample
streams; determine capture dialect and timestamp semantics. Identify reuse licenses
and cases requiring original synthetic fixtures. Include raw CAN frames versus
assembled PGNs, 0183 chunks and Signal K deltas with separate manifest types.

**Deliver:** small offline fixture corpus, capture/provenance manifest, expected
semantic results and a fault ledger. Preserve synthetic status and deterministic
seeds; include raw and redacted hashes where lawful and keep private originals out
of Git. Add missing/truncated/checksum-invalid/out-of-order/duplicate/expired/source-
change cases. Define clock basis and arrival versus measurement time.
**Acceptance:** independent expected values for nominal cases; deterministic rejection
or explicit uncertainty for negative cases; repeatable commands return nonzero on
mismatches, including optimized execution. Test corruption of an expected output.
**Stop:** ambiguous capture format is quarantined, not silently auto-converted.

## R03 — N2K protocol implementation laboratory (P1)

**Question/hypothesis:** does the pinned source study generalize beyond heading
encoding to transport and node lifecycle under faults?

**Research:** follow NMEA2000 message codecs, CAN header helpers, receive assembly,
ISO transport, address claiming, requests/product information and group-function
handlers. Compare scoped CANboat interpretations; map each finding to symbols and
commit. Study destination rules, NAME conflicts, address changes, queue pressure,
sequence wrap, short fast packets, timeouts and sentinel encodings.

**Deliver:** fake-CAN backend and controllable monotonic clock; layer-separated
vectors and state traces; extended direct-implementation worksheet. Expand codecs
first to representative position, depth, wind and battery/temperature messages,
not every PGN. Distinguish absent support from failed support.
**Acceptance:** exact independent header/field vectors; interleaved transport,
missing fragments, repeated starts, sequence wrap, malformed lengths and bounded
state; duplicate preferred-address and request lifecycle traces. Test time progression
rather than using the existing fixed clock stub. Label implementation choices
separately from normative requirements. No physical pass from this harness.
**Stop:** unresolved wire interpretation becomes an explicit uncertainty case.

## R04 — CANboat decoder and capture-dialect workflow (P1)

**Question/hypothesis:** can a newcomer reproduce a decode while preserving raw
versus assembled boundaries, timestamps and definition uncertainty?

**Research:** pin a release/commit and inspect C versus Rust CLI help and converters,
sample provenance and decoder definitions. Use the discovered Angstrom-format fix
and vendor `$MXPGN` dialect differences as regression candidates, not assumptions
about all releases. Inspect connect-time side effects separately from offline tools.

**Deliver:** executable offline conversion recipes, dialect-identification table,
normalized result manifest and disagreement ledger. Include one supported serial
adapter envelope and candump forms; no live interface needed for the first slice.
**Acceptance:** exact fixture values/source/PGN and timestamp handling; malformed
length rejection; same capture compared with the selected NMEA2000 codec where
meaningful. Unknown/proprietary fields remain qualified. All commands run on pinned
binaries; C and Rust differences documented, not flattened away.
**Stop:** discrepancy without an independent oracle remains unresolved.

## R05 — 0183 streaming, GNSS and AIS profiles (P1)

**Question/hypothesis:** can the skill handle real byte streams without confusing
framing validity with navigational validity?

**Research:** exact device manuals plus GPSD source/docs and a maintained AIS
implementation. Study chunked/concatenated sentences, empty fields, talker IDs,
checksum policy, CRLF, length profiles, tag blocks and multipart AIS channel/sequence
context. Research RMC/GGA/GSA/GSV, heading, wind and depth mappings only as needed.

**Deliver:** stream-parser recipe and fixture tests; GNSS/AIS profile tables;
multipart assembly and semantic translation examples. Keep the existing strict
inspector contract separate from optional expanded profiles.
**Acceptance:** split-at-every-byte parsing; resynchronization after noise; bounded
buffers; AIS fragment loss/interleaving/empty sequence identifiers; invalid fixes,
midnight/date rollover and unavailable values. Compare AIS payloads against an
independent maintained decoder and known decoded values; RF transmission excluded.
**Stop:** undocumented extended sentences are recorded as vendor-specific.

## R06 — Signal K application and server laboratory (P1)

**Question/hypothesis:** can a producer and client retain meaning and freshness
through authentication, subscriptions and reconnects?

**Research:** pin schema, server and plugins independently. Inspect REST discovery,
deltas/full model, multiple sources, metadata, notifications, WebSocket subscriptions,
device access requests, permissions, plugin lifecycle and PUT request states.
Separate protocol promises from actual server implementation. Follow the subscription
and security sources discovered in reconnaissance into code/tests.

**Deliver:** local-only server fixture with explicit dependency locks, a producer,
a small display/client and plugin/configuration examples; no private captures or
public demo writes. Include a read-only default and separate simulated control route.
**Acceptance:** schema-checked deltas; units/source preserved; no-data versus null
versus stale; duplicate subscriptions, cached-value replay and reconnect; revoked/
expired credentials and unauthorized writes rejected; metadata source changes shown.
Command acceptance remains distinct from actuator feedback. Record actual unsupported
subscription options rather than claiming spec parity.
**Stop:** unsupported feature becomes an explicit compatibility row.

## R07 — OpenCPN consumer verification (P1)

**Question/hypothesis:** does the same input produce the intended navigation and
Dashboard result under competing sources and failover?

**Research:** pin OpenCPN/platform and relevant Dashboard/plugin versions; inspect
connection, priority and filter documentation plus matching source. Choose one OS
first. Research serial/network 0183, Signal K and supported N2K adapter paths.

**Deliver:** one verified setup walkthrough, sanitized settings, screenshots/logs,
consumer compatibility rows and expected display observations. Select a second OS
only as a separately bounded expansion.
**Acceptance:** synthetic known position/heading/depth, source precedence, preferred
source loss/recovery, restart persistence, filters and units. Verify navigation and
Dashboard separately; configuration success alone is insufficient. Use simulation
labels so the examples cannot be mistaken for navigation fixes.
**Stop:** unavailable desktop/adapter path remains documented but untested.

## R08 — Electrical designs and power budget (P1)

**Question/hypothesis:** can a builder turn the physical guidance into an inspectable
circuit and quantitatively justified network layout?

**Research:** exact cable/connector manuals, two selected interface/transceiver
candidate datasheets, isolation/DC-DC documentation, Garmin and Actisense guides.
Trace 0183 differential interfaces versus TTL/RS-232 and N2K backbone/drop topology.
Study supply transients, reverse polarity, fuse sizing, standby/peak loads, shield
paths, termination and USB-induced isolation bypass.

**Deliver:** one worked isolated interface design, BOM with alternatives/ratings,
connector-view drawing and power/voltage-drop worksheet with explicit assumptions.
Provide an 0183 interface variant as a distinct contract rather than sharing pinouts.
**Acceptance:** arithmetic independently checked, datasheet limits traceable,
all power/ground paths visible, and a bench measurement plan for recessive/dominant
levels, termination, startup and supply faults. Simulation/calculation is not EMC,
environmental qualification or physical safety certification.
**Stop:** no wiring-specific recommendation without exact connector/board evidence.

## R09 — Buildable ESP32 N2K and SensESP sensors (P1)

**Question/hypothesis:** can two minimal, pinned projects build and preserve invalid/
stale semantics without blocking protocol service?

**Research:** selected SoC datasheet/TWAI driver, NMEA2000 controller backend and
SensESP template/upgrade docs. Inspect event loops, watchdogs, sensor scheduling,
identity persistence and Wi-Fi reconnect. Resolve the retrieved SensESP TLS guidance
against the exact version; do not globally disable security to follow an old tutorial.

**Deliver:** compile-only N2K sensor and SensESP producer projects with dependency
locks, synthetic sensor mode, build records and a hardware/flash recovery worksheet.
Use one declared board initially; no universal GPIO mapping.
**Acceptance:** clean builds from pinned dependencies; negative/missing/expired
samples tested in host or simulator where possible; build logs and binary hashes.
Bench verification additionally requires actual sensor disconnect, reboot, source
identity and independent display observations. Clearly separate those evidence levels.
**Stop:** toolchain failures after three diagnostic passes get a reproducible issue.

## R10 — Raspberry Pi/OpenPlotter deployment and recovery (P1)

**Question/hypothesis:** can a fresh documented Pi installation reliably recover
its gateway identity, configuration and data after restart or interface loss?

**Research:** current official Pi OS/OpenPlotter matrix, SocketCAN and exact adapter
manuals, stable device naming, permissions, service lifecycle, storage/power/shutdown.
Evaluate packaged OpenPlotter versus a minimal direct install with explicit tradeoffs.

**Deliver:** one supported deployment recipe, stable device/config examples, service
and log limits, backup/restore and rollback runbook. Pin image/architecture/kernel,
interface firmware and software; record the physical power design from R08.
**Acceptance:** installation/build check as available; on actual Pi verify adapter
renumbering/replug, service restart, bounded logs, restoration and startup ordering.
A desktop container is only application evidence, not Pi/HAT or power-loss evidence.
**Stop:** absent hardware leaves those rows not assessed.

## R11 — End-to-end gateways and commercial compatibility (P1)

**Question/hypothesis:** does a source retain its value, reference, identity and
freshness through a real chain without loops or stale bursts?

**Research:** exact receive/transmit manuals for selected consumers and adapters,
Signal K conversions, CANboat definitions and OpenCPN consumption. Choose one
commercial MFD/gateway pair based on available hardware, then broaden deliberately.
Do not choose brands purely to fill a table.

**Deliver:** three golden recipes: offline capture → decoder → Signal K client;
ESP32 → N2K → named consumer; Pi gateway → OpenCPN. Fill the translation matrix,
versioned compatibility matrix and commissioning/fault ledger for each.
**Acceptance:** fractional and boundary values, independent physical or synthetic
oracle, source/instance changes, stale/invalid data, loop graph with two bridges,
4800-baud bottleneck, bounded age/queues and restart. Consumer observation is required
for a compatibility pass; manual-listed support remains a separate evidence category.
**Stop:** no commercial-device access means recipe prepared, compatibility untested.

## R12 — Measurement semantics and calibration (P1)

**Question/hypothesis:** can a user distinguish protocol-correct data from a
physically meaningful measurement?

**Research:** chosen sensor/instrument manuals and domain definitions. Split into
follow-up slices if needed: navigation time/GNSS datum/antenna offsets and heading;
wind/depth reference geometry; tanks/batteries/engine instances and calibration.
Study low-speed course, true/magnetic variation, apparent/true wind inputs, depth
reference offsets, non-linear tank geometry and battery current sign conventions.

**Deliver:** domain reference tables, three filled calibration/error-budget examples
and mapping fixtures. Start with depth offset, tank calibration and heading reference;
record remaining domain questions explicitly for later slices.
**Acceptance:** independent calculations, residuals/uncertainty and fault behavior;
no claim of true wind without required inputs or state of charge from voltage alone.
Protocol validity, sensor accuracy and display interpretation remain separate.
**Stop:** insufficient reference measurements yield a calibration plan, not coefficients.

## R13 — Control simulator and bounded actuator profiles (P1)

**Question/hypothesis:** can the control contract withstand duplicates, lost feedback,
stale commands, reconnects and source changes without inferring success?

**Research:** Signal K PUT/server handler behavior, selected switching and autopilot
manufacturer integration manuals, upstream examples and explicit interlock semantics.
Start with a simulated relay; choose one documented real profile only later.

**Deliver:** command/feedback state machine, simulator, audit trail, control template
and test scenarios. Separate requested, accepted, executing, achieved and failed
states; define manual override, watchdog and restart policy.
**Acceptance:** unauthorized, duplicate, delayed, expired and replayed commands;
feedback timeout; disconnect/reconnect; manual override. A success claim requires
independent feedback. No automatic live autopilot test or inferred permission from
read-only research; actual actuation remains scoped to user authorization.
**Stop:** undocumented proprietary commands remain unsupported, not guessed.

## R14 — Security, privacy and operational resilience (P1)

**Question/hypothesis:** are data provenance and command boundaries preserved when
the network, credentials, clock or storage fails?

**Research:** Signal K authentication/access controls and actual server defaults,
SensESP provisioning/TLS behavior, selected gateway security manuals. Model trust
between instrument bus, Wi-Fi clients, plugins and remote access. CAN framing is
not sender authentication. Inspect capture metadata privacy and offline operation.

**Deliver:** threat model, minimal-permission configuration, credential lifecycle,
redaction/capture release checklist and recovery runbook. Keep network segmentation
and remote access optional; no mandatory cloud dependency.
**Acceptance:** unauthorized writes/revoked tokens, accidental credential logging,
reconnect replay, disk-full handling, clock jumps and restore from saved config.
Verify private captures are not sent to public demos or research services by default.
**Stop:** a platform lacking required controls gets a constrained deployment profile.

## R15 — Radar and adjacent interoperability (P2)

**Question/hypothesis:** which extensions are useful enough and sufficiently
specified to support without diluting the core workflow?

**Research:** radar_pi supported scanner/firmware/platform documentation; imagery
versus target reports, heading timing, alignment, multicast and network adapters.
Then investigate demand-driven J1939 engine gateways, SeaTalk1 versus SeaTalkng,
IEC 61162 IP variants, OneNet and DSC/AIS target inputs from exact owner/vendor docs.
Treat each family as a separate scoped follow-up, not one enormous crawl.

**Deliver:** supported-model matrix and radar overlay diagnostic plan; decision
records for adjacent profiles: support now, research later, or out of scope.
**Acceptance:** traceable model/version/transport requirements and one reproduced
offline/plugin case where possible. Never infer generic Ethernet interchangeability,
CAN compatibility or RF approval. No imagery-over-N2K claim.
**Stop:** two-slice cap means prioritize radar first and explicitly backlog other families.

## R16 — Agent quality, installation and maintenance evidence (P0/P1)

**Question/hypothesis:** do the enriched artifacts make agents measurably more
correct and useful on representative build/diagnosis tasks?

**Design before enrichment:** freeze baseline commit, prompts, rubric revision and
fixture versions. Keep current stable eval IDs; add realistic tasks for competing
sources, wrong firmware/manual, power budgets, protocol faults, fresh installation,
recovery and contradictory upstream guidance. Hold back cases from author tuning.
Record model/harness/version/settings and exact skill snapshots.

**Deliver:** a runnable offline verification entrypoint; reproducible agent comparison
protocol and retained outputs when generation is authorized; independently reviewed
assertion-level evidence; first-run installation trial. Extend CI for new executable
examples and local-link/manifest checks without making paid model calls automatic.
**Acceptance:** each required assertion records met/not met/not shown with visible
support. Deterministic checks verify artifacts/outputs, not merely matching words.
Semantic review records reviewer identity/kind and disagreement; model suggestions
are advisory, not human labels. Report baseline/candidate on identical tasks plus
held-out results, counts, failures and limitations. Predeclare zero tolerated new
unsafe live-transmission/actuation recommendations on the reviewed set; report
inconclusive when required evidence is missing. No global accuracy claim from a
small suite. Schema-valid manifests remain distinct from behavioral passes.
**Stop:** absent inference authorization or independent review leaves behavioral
quality not assessed; complete deterministic checks and the protocol anyway.

## Promotion and maintenance

Land one coherent run or tightly related artifact group per reviewed PR. Preserve
failed experiments and unresolved-source decisions. The original references remain
usable while new routes appear only when their files exist. Avoid a sprawling
entrypoint or required personal services. Each claim carries its version scope;
recheck on upstream release/API changes, broken links, conflicting user reports or
new hardware firmware. Link health alone does not establish factual freshness.

Campaign completion means the selected core recipes reproduce, each priority claim
has evidence or a visible unresolved dependency, the compatibility matrix states
what was actually observed, and agent-output quality has been evaluated under the
frozen protocol. Hardware/standards blockers may leave the campaign partial. Neither
all sixteen documents existing nor all research API jobs succeeding is completion.
