# AIS over NMEA 2000 — execution scope

Started 2026-10-16; baseline d74daebeb97cc8c672d3fcbba74647cd9444a422.
Question: how can a DIY application consume AIS target reports from an N2K
backbone without confusing vessel identity, source identity, time, units or
own-vessel reports, and what survives translation to Signal K/OpenCPN?

Use GroktoCrawl bounded search/retrieval plus pinned upstream code. First slice:
three searches and up to eight pages; second slice only for unresolved claims.
No paid model research jobs, live network replay, flashing or AIS radio transmission.
Durable outputs: focused reference, mapping/commissioning worksheet, original
synthetic fixtures, executable decoder/target-state tests and source/claim ledger.

Independent oracle before implementation: Class A/B position uses MMSI123456789,
longitude−2°, latitude1°, COG1rad, SOG5m/s, true heading0.5rad. Static parts A/B
must join by target MMSI, never CAN source address. A second MMSI on the same CAN
source stays separate. Static updates must not renew position age. Missing position
must not become (0,0); a null or future observation must not revive an old fix.
NMEA2000 encoding and CANboat decoding are compared with independent scaled bytes
and expected units. Optional Signal K converter behavior is tested at an exact
version; unsupported PGNs and loss remain explicit. Repeat technical probes three
times; no performance claims. Physical receiver/OpenCPN GUI acceptance remains
unverified without hardware and observed consumer behavior.
