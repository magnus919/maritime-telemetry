# Deployment and recovery record

Filled example scope: local Signal K lab, version 2.33.0; temporary configuration,
loopback-only listeners, synthetic source, no hardware providers. Recovery is
re-running the isolated lab; production configuration is never overwritten.

For an actual Pi/gateway installation:

| Artifact | Record |
|---|---|
| OS/image | Filename, hash, architecture, kernel, board revision |
| Interface | Adapter serial/firmware, stable device path, permissions, controller mode |
| Software | Server/schema/plugin/OpenCPN versions and dependency locks |
| Configuration | Private backup location/hash; redacted shareable example |
| Identity | Device NAME/instances/source labels; duplicate prevention |
| Power/storage | Conversion/fuse, shutdown plan, log rotation/retention |
| Restore | Exact target, commands, prior image and rollback owner |
| Outcome | Source/units/freshness/priority verified after restore |

Tests: boot without interface, unplug/replug, restart, Wi-Fi loss, clock jump,
disk full, restore onto spare media and unexpected power interruption on a safe bench.
Record not-assessed cases explicitly. A successful process start is not a complete
recovery result.
