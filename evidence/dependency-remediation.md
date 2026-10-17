# Full-server lab quarantine and dependency remediation

Date:2026-10-16 America/New_York (2026-10-17 UTC during execution).
Baseline: dd18cf83ebf6fe4b29ee56e85afdca3ff5968f8d.

The audit found19 affected npm package entries in the optional Signal K full-server
lab, including1 critical,6 high and12 moderate. These counts include inherited
package advisories; they are not19 independently demonstrated exploits. The lab was
loopback-only; no exploit/reachability assessment was performed.

## Attempt and decision

The latest published server checked with `npm view signalk-server version` was2.33.0,
already the installed version. Its dependency contract still requests an old schema
line. Updating the direct ws client to8.22.0 and refreshing compatible packages
removed its advisory entry but left18 affected entries, including critical-rated
nested lodash. Some remaining entries had no reported fix. A current server version
alone was therefore insufficient to make the installed graph clean.

We did not use `npm audit fix --force` (which proposed an old server downgrade),
suppress advisories, or force incompatible transitive overrides and imply safety.
The current full-server lab installer, lockfile and runner are removed. The
[quarantine notice](../examples/signalk-lab/README.md) links the historical snapshot.
Existing dated results remain evidence of their original behavior, not security
passes or commands for the current skill. No production server was changed.

## Supported runnable example

The separate AIS/N2K mapping lab remains runnable. Its locked graph reported zero
advisories during remediation. Required PR CI installs it, checks moderate-or-higher
advisories and executes pinned C++/CANboat/mapping/pyais probes under Node24.
Weekly audits and Dependabot PRs provide ongoing visibility. Registry findings
change over time; zero at this date is not a guarantee of future security.

Reintroducing the full server requires a supported dependency remediation,
clean advisory policy and actual server REST/WebSocket/authentication tests on the
chosen version. A mapping function test does not substitute for those server tests.

## Sources and recorded outcomes

- [Critical lodash advisory](https://github.com/advisories/GHSA-jf85-cpcp-j695).
- [WebSocket denial-of-service advisory](https://github.com/advisories/GHSA-96hv-2xvq-fx4p).
- `npm view signalk-server version engines dependencies --json`:2.33.0, Node>=22,
  schema dependency1.0.x; the prior lab's installed nested schema/lodash differed
  from the separately pinned schema used by its own client assertions.
- Compatible-refresh audit:1 critical,5 high,12 moderate entries.
- Current AIS mapping audit and exact CI execution are visible on the PR/merge
  checks. The coverage/test count is produced by CI rather than hard-coded into a
  status page that can silently become stale.

## CI portability correction

The first expanded Ubuntu integration run failed the fake-CAN address lifecycle
assertion. Pinned NMEA2000 uses clock_gettime on Linux and millis on the recorded
macOS path. The host probe now supplies both deterministic test-clock adapters in
its own process. The original macOS observation remains historical; Linux acceptance
requires the updated PR job to pass. No upstream clock or live system time is changed.
