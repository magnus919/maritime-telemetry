# Measurement meaning and calibration

These are engineering calculations and domain contracts, not new NMEA definitions.
Use exact sensor manuals and the target PGN/path definitions to bind them to devices.
The [worked calibration worksheet](../templates/calibration.md) separates acquired
measurements from synthetic examples. Arithmetic helpers are in
[scripts/engineering_math.py](../scripts/engineering_math.py).

## Three worked calculations

**Depth:** transducer reports 4.2 m below itself; transducer is 0.4 m below surface;
keel is 1.8 m below surface. Surface depth is 4.6 m; below-keel clearance is 2.8 m.
With independent bounded errors of ±0.10 m, ±0.03 m and ±0.05 m, conservative summed
uncertainty is ±0.18 m. RSS ≈0.116 m is appropriate only if independent random-error
assumptions are justified. Do not apply the transducer offset twice when a gateway
or display already applies it. Preserve which reference the transmitted field uses.

**Tank:** synthetic calibration points `(raw count, litres)` are (0,0), (100,20),
(200,60). At count 150, piecewise interpolation yields 40 L, not 45 L from a naive
percentage of a different tank capacity. Counts outside the calibrated range are
flagged rather than extrapolated. Real calibration must sample known added volumes,
include heel/trim and sender hysteresis, and record repeatability/residuals. A
reverse-acting sender needs sorted raw coordinates and appropriately decreasing
volume values; don't reject it merely because volume decreases with raw count.

**Heading:** define east variation positive for this calculation. Magnetic heading
350° plus +15° variation yields true heading 5° after modulo 360. Keep deviation
(compass/instrument error) separate from magnetic variation (location/time model).
A negative 10° wind angle may represent 350° on a circular display but retains its
signed relative meaning. Document bow zero, clockwise sense and wrap behavior.
These arithmetic examples have tests; no physical sensor was calibrated.

## Domain contracts

| Domain | Preserve | Common misleading substitution |
|---|---|---|
| GNSS | Fix quality, datum, antenna location, UTC/date, age, satellites/precision where provided | Rapid lat/lon alone implies trustworthy current navigation |
| Time | Measurement clock versus gateway arrival; timezone; rollover evidence | Correcting every old capture as a GPS rollover |
| Speed/course | Through-water versus over-ground; course versus heading | Course at very low ground speed as compass heading |
| Wind | Apparent/true reference, angle convention, required boat-motion inputs, alignment | Rename apparent data “true” or combine asynchronous inputs without age checks |
| Depth | Below transducer/surface/keel, offsets and acoustic validity | Reapply offset already applied upstream |
| Engine | Instance, RPM representation, temperature/pressure units and sensor status | Treat all engine PGNs as the same instance |
| Battery | Bank instance, current sign, calibrated shunt, voltage/current/temp | Infer reliable state of charge from voltage alone |
| Tank | Fluid type/instance, capacity, sender curve, trim/heel | Linear percentage means linear volume for irregular geometry |

The [NMEA2000 source study](nmea2000-source-study.md) gives concrete codec symbols;
[Signal K schema source](https://github.com/SignalK/specification/tree/fb628fb4ee569149fd3810b271d0f987428b4703/schemas)
provides path semantics. Neither replaces reference-instrument measurements.

## Calibration workflow

Record the raw signal before conversion. Freeze reference instrument accuracy,
range, temperature, mounting and units. Acquire at least enough points to expose
the expected nonlinearity; choose point count by the sensor model, not a fixed
checklist. Fit only within the sampled range. Retain residuals and a separate check
point not used in fitting. Preserve unavailable, open/short and implausible-rate
states independently from a measured zero. Version coefficients and make rollback
to the prior calibration possible. Recalibrate after relevant sensor, mounting or
reference changes; never silently change historical recorded values.
