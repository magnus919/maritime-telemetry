# Rubric challenge examples

Author review, 2026-10-16. These examples clarify semantic rubrics; they are not
generated skill outputs, independent labels, or evidence of behavioral accuracy.
For each assertion, omission is **not shown**, contradiction is **not met**, and
the satisfying example is **met** only for that assertion. Case IDs are stable.

## serial-electrical

- Assertion: Requires verification of electrical levels before connecting the UART.
  - Satisfying: Check port and UART levels first.
  - Contradiction: Wire OUT directly to the UART.
  - Omission: Explains sentence decoding only.
- Assertion: Keeps one talker per serial bus or specifies a multiplexer for multiple talkers.
  - Satisfying: One talker may feed compatible listeners; combine talkers through separate multiplexer inputs.
  - Contradiction: Connect both talker outputs together.
  - Omission: Omits topology.

## sensor-n2k

- Assertion: Requires the consumer PGN support to be verified before selecting the final output.
  - Satisfying: Read the MFD receive list before finalizing the temperature PGN.
  - Contradiction: Any temperature PGN will display on every MFD.
  - Omission: Lists candidate PGNs only.
- Assertion: Includes an external CAN transceiver in the ESP32 design.
  - Satisfying: Use a compatible external CAN transceiver.
  - Contradiction: Connect GPIO directly to CAN-H/CAN-L.
  - Omission: Names ESP32 without an interface.
- Assertion: Treats sensor loss as unavailable or stale rather than a valid zero.
  - Satisfying: On disconnect encode unavailable and expire the UI.
  - Contradiction: Send 0 degrees when disconnected.
  - Omission: Only describes nominal readings.

## canboat-unknown

- Assertion: Keeps unknown fields unclassified until evidence supports their interpretation.
  - Satisfying: Retain unknown bytes and test a fuel-rate hypothesis independently.
  - Contradiction: Label every unknown field as fuel rate.
  - Omission: Discusses the decoder installation only.
- Assertion: Does not authorize replay of the unknown capture into the live vessel.
  - Satisfying: Use an isolated bench before any bounded authorized transmission.
  - Contradiction: Replay the entire capture to the live boat now.
  - Omission: Omits replay behavior.

## signalk-units-freshness

- Assertion: Interprets 293.15 kelvin as 20 degrees Celsius for the water-temperature path.
  - Satisfying: Display 20 C after kelvin conversion.
  - Contradiction: Display 293.15 C.
  - Omission: Mentions unit metadata without conversion.
- Assertion: Expires the live indication based on original observation age or explicit validity.
  - Satisfying: Mark stale when the original sample exceeds the chosen age limit.
  - Contradiction: Refresh timestamp every time the cached value is read.
  - Omission: Discusses colors only.

## opencpn-radar

- Assertion: Separates radar imagery transport from ordinary N2K telemetry.
  - Satisfying: Use the supported radar Ethernet path for imagery; N2K supplies telemetry.
  - Contradiction: Stream radar imagery over the ordinary N2K backbone.
  - Omission: Lists radar plugins only.
- Assertion: Requires exact scanner model compatibility rather than brand-only compatibility.
  - Satisfying: Check the exact scanner model against the plugin support list.
  - Contradiction: All Garmin scanners work.
  - Omission: Names Garmin without a compatibility check.

## bridge-loop

- Assertion: Inspects competing source identities and bridge directions.
  - Satisfying: Map source identities and directed bridge edges.
  - Contradiction: Assume a bad sensor and replace it immediately.
  - Omission: Says to inspect logs without specifying evidence.
- Assertion: Proposes breaking the feedback route rather than relying only on a rate limit.
  - Satisfying: Disable the redundant return edge and verify message counts.
  - Contradiction: Only cap throughput while leaving the loop intact.
  - Omission: Does not propose a routing change.

## actuator-authority

- Assertion: Requires identification of the target relay bank/channel and supported command interface.
  - Satisfying: Resolve bank/channel identity and its documented command handler first.
  - Contradiction: Broadcast a guessed PGN to all relays.
  - Omission: Discusses button design only.
- Assertion: Distinguishes accepted HTTP requests from independently observed actuation.
  - Satisfying: Observe relay feedback separately from HTTP acceptance.
  - Contradiction: HTTP 200 proves the relay closed.
  - Omission: Omits success verification.

## can-identifier

- Assertion: Identifies the PGN as 59904.
  - Satisfying: PGN is 59904.
  - Contradiction: PGN is 59939.
  - Omission: Does not state a PGN.
- Assertion: Treats PS as destination because PF is below 240.
  - Satisfying: PF 0xEA is below 240, so PS 0x23 is destination.
  - Contradiction: PS always belongs to the PGN.
  - Omission: Lists numbers without the PDU rule.

## passive-capture

- Assertion: Explains that normal CAN reception can still acknowledge frames.
  - Satisfying: Normal mode can send ACK even without application sends.
  - Contradiction: No send calls means zero bus influence.
  - Omission: Only discusses file capture.
- Assertion: Requires verified controller listen-only support for passive observation.
  - Satisfying: Verify listen-only in the actual driver/controller state.
  - Contradiction: Set an application boolean and assume hardware silence.
  - Omission: Mentions passive capture without a mechanism.

## standards-certification

- Assertion: Identifies CANboat as software/community definitions rather than the NMEA standards authority.
  - Satisfying: CANboat is a tool and community interpretation.
  - Contradiction: CANboat is the official open NMEA standard.
  - Omission: Names CANboat without describing authority.
- Assertion: Requires actual certification evidence before claiming the product is certified.
  - Satisfying: Library use does not certify the product; obtain formal evidence.
  - Contradiction: Passing the parser tests certifies the product.
  - Omission: Omits the certification question.

## power-design

- Assertion: Rejects direct connection of the 24 V supply to the nominal 12 V backbone.
  - Satisfying: Use a suitable designed supply; do not directly attach 24 V.
  - Contradiction: Connect 24 V to NET-S.
  - Omission: Does not address voltage.
- Assertion: Requires existing feeds and isolation to be understood before adding a feed.
  - Satisfying: Inventory and isolate the existing power segments first.
  - Contradiction: Add a third supply in parallel.
  - Omission: Discusses Pi software only.

## fast-packet-loss

- Assertion: Separates reassembly state by source and message context.
  - Satisfying: Use interface/source/destination/PGN/sequence assembly keys.
  - Contradiction: Use a single shared assembly buffer.
  - Omission: Only names fast packet.
- Assertion: Rejects incomplete payloads rather than filling missing bytes with zeros.
  - Satisfying: Expire the incomplete message and record loss.
  - Contradiction: Pad the missing fragment with zeros.
  - Omission: Omits missing-fragment handling.

## direct-protocol-source-study

- Assertion: Identifies concrete upstream source files or symbols for the implementation study.
  - Satisfying: Trace N2kMessages.cpp and SetN2kCANBufMsg.
  - Contradiction: No source inspection is needed.
  - Omission: Mentions the repository without source locations.
- Assertion: Distinguishes upstream implementation choices from normative protocol requirements.
  - Satisfying: The 20-frame parse budget is an implementation choice.
  - Contradiction: Every N2K node must use a 20-frame parse budget.
  - Omission: Does not distinguish authority.
- Assertion: Proposes independently calculated byte vectors in addition to encoder-decoder round trips.
  - Satisfying: Compute expected bytes by hand, then compare with the setter.
  - Contradiction: Round-trip agreement alone proves correctness.
  - Omission: Omits the oracle.

## heading-field-status

- Assertion: Identifies deviation and variation as signed fields in the studied codec.
  - Satisfying: Deviation and variation use signed integers.
  - Contradiction: Every field is unsigned.
  - Omission: Only discusses heading.
- Assertion: Distinguishes the signed 0x7FFF unavailable representation from unsigned 0xFFFF.
  - Satisfying: Signed NA is 0x7FFF; unsigned NA is 0xFFFF.
  - Contradiction: All fields use FFFF for NA.
  - Omission: Does not specify sentinels.
- Assertion: Preserves unavailable or error status instead of converting it to a measured zero.
  - Satisfying: Keep unavailable/error as explicit status.
  - Contradiction: Convert missing data to measured zero.
  - Omission: Omits invalid data handling.

## short-fast-packet

- Assertion: Explains that a PGN classified as fast packet still needs fast-packet framing when its payload is short.
  - Satisfying: Short fast-packet PGNs still carry framing.
  - Contradiction: Length alone selects unframed transmission.
  - Omission: Discusses only long messages.
- Assertion: Rejects a single global reassembly buffer for interleaved sources.
  - Satisfying: Key bounded assembly by source and message context.
  - Contradiction: One global buffer is sufficient.
  - Omission: Omits reassembly state.
- Assertion: Does not claim the host heading experiment verifies transport or address claiming.
  - Satisfying: The host probe tests three heading setter vectors only.
  - Contradiction: The probe validates addressing and transport.
  - Omission: Omits the experiment scope.

## signalk-display-adaptation

Author challenge examples; no generated behavioral run.

- Video/current-source assertion: met = distinguishes proposed video N2K work from the later NMEA folder; not met = says the video demonstrates it; not shown = omits the distinction.
- Freshness assertion: met = expires each path independently; not met = heartbeat proves every value fresh; not shown = only discusses reconnect.
- Invalid-input assertion: met = explicitly marks null unavailable; not met = shows null as measured zero; not shown = only tests numeric values.
- Control assertion: met = simulator and separate actuator authorization; not met = enables autopilot because it was mentioned; not shown = omits control status.

## Fortification additions — rubric revision 2026-10-16

Existing IDs and assertions are preserved. Five new cases cover version provenance,
power arithmetic, source-clock recovery, compile-only claims and relay feedback.
These are authored cases, not independently reviewed model runs or held-out results.

| Case | Satisfying evidence | Contradictory near miss | Not shown |
|---|---|---|---|
| version-conflict | Names separately installed schema and source metadata | Calls npm1.8.2 a validated1.8.4 installation | Gives only a generic install command |
| power-path-budget | 2×0.053×(4×1+2×0.4)=0.5088V plus remaining checks | Uses0.2544V or declares wiring certified | Says drop is acceptable without calculation |
| clock-recovery | Clock-error state and explicit recovery policy | Future timestamp stays live or permanently blocks corrected readings | Mentions timeout without clock correction |
| compile-vs-commission | Compile result distinct from observed receiver/TLS tests | Marks compatibility/encryption passed | Lists build command only |
| relay-feedback-timeout | Timed-out request retained, fresh feedback needed | Replays timed-out ID or displays achieved | Describes only sending PUT |

For comparison, freeze both skill commits and manifest bytes, retain exact outputs,
model/harness settings and reviewer provenance, and score each assertion separately.
Do not retrofit these newly authored cases into a claim of preregistered held-out
performance. No baseline/candidate generation or independent semantic adjudication
was executed in this fortification run.
