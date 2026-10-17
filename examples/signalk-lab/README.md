# Signal K full-server lab: quarantined

The optional full-server lab is suspended because its dependency graph has known
vulnerability advisories. The latest published server checked for this remediation
was2.33.0. Refreshing compatible packages still left18 affected package entries,
including critical-rated nested lodash and packages with no reported fix. See the
[remediation record](../../evidence/dependency-remediation.md).

The installer, lockfile and runner have been removed from the current skill so new
users do not install this graph through the documented workflow. Historical runs
remain evidence for their original snapshots; they are not current security passes.
The historical source is available at commit
[dd18cf8](https://github.com/magnus919/maritime-telemetry/tree/dd18cf83ebf6fe4b29ee56e85afdca3ff5968f8d/examples/signalk-lab).

The [AIS mapping lab](../ais-n2k-lab/package.json) remains runnable and covers real
N2K-to-Signal-K and AIS-to0183 mapping functions. It does not replace an actual
server integration test. Reintroduce a server lab only with a supported dependency
plan, passing advisory checks and reproduced server/security behavior. Do not use
unreviewed cross-major overrides or suppress advisories to reopen it.
