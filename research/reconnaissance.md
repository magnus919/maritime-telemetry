# Bounded source reconnaissance

Date: 2026-10-16. Scope frozen in [reconnaissance scope](reconnaissance-scope.md).
Completed: **4 discovery queries and 8 page retrievals through GroktoCrawl**.
No autonomous research jobs, firmware builds, application integrations or hardware
experiments were run in this reconnaissance. The repository's existing 17 Python
tests and validator were separately re-run successfully during the audit.

## Retrieval log and preservation

The shell initially selected a stale service address and failed to connect. An
explicit configured endpoint then rejected the shell's credential. Loading the
existing matching Hermes credential in memory resolved authentication; no credential
was printed or written into this repository. The authenticated capabilities read
advertised live research. Search and scrape calls then completed successfully.
Private service addresses and credentials are intentionally not part of the skill.

The [machine-readable ledger](source-ledger.json) retains exact queries, candidate
URLs, retrieval hashes, lengths, extraction quality flags and disposition. Full
retrieval JSON was temporarily inspected locally; it is **not retained in Git**.
Hashes identify the retrieved responses, but without retained full content they
cannot independently reproduce that snapshot. Durable evidence here consists of
original source-level findings, stable URLs where available, and explicit follow-up
questions. Future runs should retain permitted snapshots or immutable upstream
source references when a claim requires stronger reproducibility. Retrieval success
or a crawler's quality score does not certify completeness or correctness.

Searches returned only three candidates per query, with additional results omitted.
They are discovery samples, not exhaustive literature searches. Search 1 also found
historical Signal K 1.5.0 security documentation; prefer the explicit 1.7.0 page for
this comparison. OpenCPN PDF exports were not retrieved: the focused HTML priority
page was more relevant. Bot review comments in the CANboat PR were excluded as
behavioral evidence; a merged patch still requires release pinning and execution.

## Source-level findings and decisions

| ID | Retrieved source | Finding and interpretation | Next action |
|---|---|---|---|
| S01 | [Signal K 1.7.0 subscriptions](https://signalk.org/specification/1.7.0/doc/subscription_protocol.html) | Describes subscription policies, metadata and multiple-source handling. Cached/resend behavior makes arrival frequency an insufficient freshness oracle. This is a specification snapshot, not a server test. | R06 exercise actual server behavior; R11 preserve measurement age. |
| S02 | [Signal K 1.7.0 security](https://signalk.org/specification/1.7.0/doc/security.html) | Describes TLS, token lifecycle and access requests; warns against redistributing credentials. It does not establish the deployed server's feature completeness. | R06/R14 test permissions, expiry and credential leakage. |
| S03 | [CANboat repository](https://github.com/canboat/canboat) | Retrieved README distinguishes C and Rust tools, gateway-specific behavior and capture dialects. Some interface paths claim addresses or configure adapters. A moving README is not a reproducible binary contract. | R04 pin code/help and test offline dialects; inspect side effects before live use. |
| S04 | [CANboat PR 1031](https://github.com/canboat/canboat/pull/1031) | Retrieval reports merged 2026-10-10, adding an Angstrom-style candump reader and malformed-length handling. This is a concrete regression-test lead, not proof that an installed release contains it. | R04 identify containing release/commit and reproduce fixtures. |
| S05 | [OpenCPN data priorities](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:manual_basic:set_options:connections:data_priority) | Describes navigation priority, persistence/failover and separate Dashboard rules for some instruments. Generic “set source priority” guidance misses consumer-specific behavior. | R07 verify both views on one named release/platform. |
| S06 | [SensESP getting started](https://signalk.org/SensESP/pages/getting_started/) | Provides a PlatformIO template and authorization flow, but also advises disabling server SSL for the described setup. That creates an applicability/security question against S02; it is not a reason to disable TLS universally. | R09/R14 inspect exact SensESP version and supported secure deployment. |
| S07 | [Signal K latest entry](https://signalk.org/specification/latest/) | Returned only a redirect-link page to 1.7.0. Crawler completeness/boilerplate checks failed. This establishes the retrieved link, not the newest schema release. | R01 compare repository tags/schema/package metadata and resolve version naming. |
| S08 | [Signal K Server introduction](https://demo.signalk.org/documentation/) | Establishes server/provider/plugin orientation, but is too broad for configuration or API implementation claims. No data was sent to the demo. | R06 retrieve specific plugin/security/API documentation and matching source. |

## Confidence and open questions

High confidence in the repository inventory and test results; they are direct local
observations. Moderate confidence that the retrieved documentation exposes useful
research gaps; release-specific behavior has not been reproduced. No confidence
rating here represents calibrated probability.

Unresolved: current schema/server compatibility, exact versions containing decoder
fixes, supported TLS path for a selected SensESP build, OpenCPN behavior on the
chosen OS, current Pi/OpenPlotter matrix, available commercial test hardware and
access to normative standards. These become campaign inputs, not silent assumptions.
