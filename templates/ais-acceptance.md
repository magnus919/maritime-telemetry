# AIS target integration acceptance record

Filled lab baseline: synthetic MMSI123456789; second target234567890; own987654321;
receiver CAN address35. Real installation values must be separately recorded.

- Producer model/firmware and manual transmit PGNs: **pending**.
- Gateway/adapter/driver/version, isolation and operating mode: **pending**.
- Consumer model/OpenCPN release/plugin and receive PGNs: **pending**.
- Route selected: native N2K / native Signal K / converted0183: **pending**.
- Rollback: disable new input/output, restore saved config, physically remove added
  drop if authorized; preserve existing primary navigation path.
- Capture provenance: bus, receiver NAME/address, gateway timestamp basis, filters,
  format raw CAN versus assembled PGN, privacy/redaction decision.

| Test | Lab expectation | Actual consumer observation |
|---|---|---|
| Two MMSIs from one CAN address | Two distinct targets | Pending |
| Static A then B / B then A | Fields join by MMSI; position remains independent | Pending |
| Position stops, names continue | Position expires despite fresh metadata | Pending |
| Longitude/latitude zero | Valid zero survives mapping and display | Pending; mapper4.7.0 defect recorded |
| Position unavailable | No new false fix; old position expires/clears visibly | Pending |
| Own MMSI / own-information flag | Explicit self policy; no duplicate danger target | Pending |
| Second receiver / address reassignment | Provenance retained, no cross-target merge | Pending |
| Partial fast packet vs older short PGN | Incomplete transport rejected; supported older layout decoded | Pending |
| Reconnect/replay / clock correction | No false freshness or duplicate alarms | Pending |
| Converted0183 | Field loss and rounding accepted explicitly; plugin output reaches app | Pending |
| Dual feeds / gateway return route | No duplication or loop amplification | Pending |

Lab pass is not installation acceptance. Record UTC, captures, expected/actual
values, software versions, independent observer and unresolved mismatches. Treat
CPA/TCPA alarms as a separate acceptance scope requiring trustworthy own navigation,
target age, coordinate/time alignment and actual consumer behavior.
