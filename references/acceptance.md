# Commissioning and fault isolation

These are recommended acceptance practices. Select thresholds before the test
from actual device requirements and the intended function; do not invent a universal
safe bus utilization, freshness timeout or acceptable actuator latency.

## Evidence ladder

| Stage | What it establishes | What remains unproven |
|---|---|---|
| Static review | Design and source consistency | Execution |
| Unit tests | Specific parser/logic cases | Wiring and target compatibility |
| Offline replay | Behavior on that recording | Live timing, loss and electrical health |
| Bench integration | Named devices under stated conditions | Boat power/EMC/environment |
| Vessel observation | Recorded behavior on that network | Unobserved faults and future upgrades |
| Formal certification | Scope actually certified | Every application-specific outcome |

Keep firmware, dependency and configuration hashes with evidence. A green test
runner is not proof that an agent's whole design is correct. Missing hardware is
“not tested,” never an inferred pass.

## Minimal acceptance roster

- Nominal low/mid/high physical inputs and boundary values map to correct units,
  reference and instance in an independent decoder and the intended consumer.
- Missing/invalid sensor values are explicit; stale data expires in the consumer.
- Boot, restart ordering, brownout recovery and persistence do not change identity
  unexpectedly or create a transmission burst.
- Two equivalent devices coexist with separate identities/data instances.
- Truncated/checksum-failed 0183 records and incomplete N2K assemblies never produce
  accepted fabricated measurements.
- Input loss, reconnect, gateway restart and duplicate bridge paths do not relabel
  old data as fresh or multiply traffic.
- Network health remains within the project's predefined baseline/limits, with
  monitored errors, drops, queue age and device availability.
- For controls, authorization, wrong-target rejection, timeout, manual override
  and independent physical feedback have separate evidence rows.

## Diagnose in layers

| Symptom | Hypothesis | Smallest useful next observation |
|---|---|---|
| No serial bytes | Wiring/direction/speed/adapter | Port identity, configured framing, bounded raw capture |
| Gibberish serial | Speed/polarity/level mismatch | Manual plus measured waveform with suitable interface |
| CAN errors appear with new device | Termination, power, bit timing, wiring | Baseline comparison, unpowered topology check, terminal supply |
| Device listed but no reading | Unsupported PGN/instance/source selection | Receiver support list and actual transmitted PGN |
| Reading numerically wrong | Units/reference/sentinel/calibration | Known physical stimulus and raw-to-screen trace |
| Intermittent large values | Reassembly loss or buffer interleaving | Fragment sequence/source log and drop counts |
| Data flips between values | Competing sources | NAME/source/instance history and source policy |
| Data stops at reboot | Identity/persistence/address assumption | Address-claim trace before/after and configured source binding |
| Network flood after bridge | Feedback loop or queued retransmission | Directed edge counts, output settings and queue age |
| Control accepted but no movement | Handler/interlock/wrong target/physical fault | Request lifecycle plus independent physical feedback |

Change one variable per pass. Preserve the original capture and annotate the
changed condition. A terminator resistance check or clear controller error count
alone is insufficient to establish wire quality. Conversely, a correct waveform
does not prove the PGN semantics.

## Stop and restore

Define the physical way to unplug the prototype without removing a backbone
terminator or powering down unrelated equipment. Save original configurations
before changing sources or output routes. Stop on new bus-off events, repeated
resets, unexplained supply drop, loss of primary navigation or unexpected actuation.
Restore the original arrangement and verify baseline recovery.

After three non-converging passes, deliver the fault ledger: observation,
hypothesis, test, outcome, rejected hypotheses, remaining alternatives and one
specific next measurement. Do not repeat scans or try random configuration values.

Before publishing captures, remove location/MMSI/serial information or obtain the
owner's publication authorization. Retain byte-level originals privately if needed
for reproducibility; a redacted capture may no longer preserve checksums or identity
relationships and must be labeled accordingly.
