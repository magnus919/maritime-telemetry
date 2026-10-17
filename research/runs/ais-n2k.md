# AIS-over-N2K research and implementation report

Date: 2026-10-16 America/New_York; probes continued after00:00UTC October17.
Baseline: d74daebeb97cc8c672d3fcbba74647cd9444a422.
Scope/independent expected values were recorded in [execution scope](ais-n2k-scope.md).

## Findings and recommendation

AIS-over-NMEA2000 is a practical supported integration path. The skill now treats
it as a first-class route, with target identity, static joins, freshness, wire
fragments, older payload layouts and consumer-specific translation contracts.
Commercial output support does not imply radio transmit control or universal
consumer acceptance. Choose one route and verify the actual device/application.

Use [AIS over NMEA2000](../../references/ais-nmea2000.md) for design and
[reproduction guide](../../references/ais-n2k-laboratory.md) for experiments.
The existing serial AIS work remains useful but is not a prerequisite bridge.

## Gather and evaluate

GroktoCrawl performed3 searches and8 page retrievals, within the first bounded
slice. All8 pages supplied relevant content; a generic low boilerplate score on
the manufacturer page did not override manual inspection of its usable PGN table.
Search coverage was explicitly partial (top3 hits per query), not an exhaustive
web review. Discovery hits for translated duplicate PDFs and the older OpenCPN
Windows setup tutorial were not used for current configuration claims.

The [source-level extraction log](ais-n2k-sources.json) contains exact URLs, response
hashes, per-source claims, dispositions and search coverage. Code/package inspection
resolved questions the README pages could not. No paid autonomous/model research,
private vessel capture, AIS radio operation or public demo interaction was used.
Third-party source bodies are not copied into this repository.

| Claim | Primary evidence | Strength / limit |
|---|---|---|
| Commercial N2K AIS publication | GarminAIS source's transmit table | Manufacturer documentation; no hardware observation |
| MMSI target vs CAN source | NMEA2000 source UserID encoding, CANboat fields, Signal K model and mapper | Cross-implementation plus executed two-MMSI fixture |
| Four core payload encodings | Independent scaled-integer generator vs pinned NMEA2000 setters | Four exact byte comparisons; not full standards conformance |
| Older trailing fields can be absent | CANboat PGN YAML/minLength and PR848 | Community implementation rule plus five executed short forms |
| Modern and short decoding | CANboat8.3.0 raw/assembled paths |13 cases ×2 paths ×3 repetitions |
| Signal K zero-coordinate omission | mapper4.7.0 position filter and executed longitude0 fixture | Confirmed dependency limitation on tested PGN129038 |
| Unavailable position not emitted | Null-position fixture through mapper | No clearing delta; stale cached fix must expire independently |
| Converter support is a subset | converter2.0.3 switch and129040 probe | No129040 output; not a claim about future versions |
| Re-encoding is lossy | converter output independently decoded by pyais3.3.1 | Specific rounding/type/time/accuracy/vendor losses observed |
| Plugin cleanup | Real start/stop hooks on EventEmitter | Twice per trial,3 trials; not server/TCP/GUI lifecycle |
| AtoNs use separate entity family | mapper129041 source | `atons` context inspected; no full AtoN fixture/GUI proof |

## Reproductions and retained evidence

Pinned source: NMEA2000 `5b7b9fc3ccc18e30ebfba92da6486cffc6251595`,
CANboat `ed1052d80596a4e6eaa56907dfeb215fac61287d` (C analyzer8.3.0).
Executed on macOS arm64, Node26.10.0, Python3.14.7. npm dependencies are locked in
[lab package lock](../../examples/ais-n2k-lab/package-lock.json); mapper4.7.0,
AIS converter2.0.3, schema1.8.2. pyais3.3.1 ran in a separate existing test venv.

- [CANboat decoder verdicts](../../evidence/ais-n2k-decoder-results.json): identical
  field results for raw-frame and assembled paths on all3 repetitions.
- [Decoded synthetic fields](../../evidence/ais-n2k-decoded.json): normalized original
  fixture output; version/header handling documented in the verifier.
- [Signal K and plugin outputs](../../evidence/ais-n2k-integration-results.json): all
  deltas, converted sentences, three trials and explicit known limitations.
- [Independent0183 inspection](../../evidence/ais-n2k-0183-results.json): all decoded
  converter sentences from each trial, including changed/lost fields.
- [Fixture provenance](../../fixtures/manifest.json): original MIT synthetic records,
  generated assembled PGNs and raw fast-packet frames; no real vessel locations.

All three trials matched each experiment's behavioral oracle. No throughput/latency
benchmark is claimed. `passed` means the assertions about **observed behavior**
held; it does not promote known conversion defects to acceptable navigation behavior.

## Failures, adaptations and unresolved claims

- Initial temporary app stub lacked `config.version`; converter's naming helper
  threw. Added a declared server-version contract to the stub. This was a harness
  error, not a converter defect, and no real server was implied by the stub.
- CANboat camel-case mode wraps PGNs under an identifier. Unwrapped it explicitly
  before invoking the mapper; never treated the version header as a measurement.
- npm emitted deprecated transitive-dependency warnings. The experiment pins the
  tested set; it is not a dependency-security audit or production recommendation.
- mapper4.7.0 omits valid zero longitude. This remains unresolved upstream; the
  teaching target model preserves zero but does not silently patch the real mapper.
- Converter2.0.3 changes type1 to3 and rounds angles, loses report seconds and some
  accuracy/static metadata. See the guide before promising compatibility.
- The first shell branch-switch ran in the temporary parent directory and failed;
  repeated in the cloned repository. No source checkout state was changed by it.

Open questions: full129794/type5 multipart conversion; AtoN/SAR and emergency
semantics; all unavailable/error encodings; actual gateway source naming and own
routing; duplicate-receiver fusion; GUI target display/CPA/TCPA; physical network
behavior and licensed-standard compliance. No synthetic test closes these gates.

## Validation and maintenance decision

50 dependency-free tests pass locally, including11 new AIS tests. The existing CI
matrix verifies Python3.10/3.12/3.14; optional C/Node/pyais runs are recorded above,
not silently required on first installation. Five output-quality cases were added
with reviewable near misses, but no agent generation or independent adjudication
was executed. Neither the skill nor its dependencies are claimed certified.

Re-run the scoped probes when mapper/converter/CANboat versions change. The known
zero-coordinate assertion intentionally flags changed dependency behavior for review;
a future fix should update the recorded observation, then add a desired-behavior gate.
Next physical acceptance starts with one named receiver, adapter and consumer and
uses the [AIS acceptance record](../../templates/ais-acceptance.md).
