# Calibration record — synthetic tank example

Example only: not acquired measurements. Sensor ID: synthetic sender. Units: raw
counts and litres. Curve: piecewise linear, no extrapolation.

| Raw | Known volume |
|---:|---:|
| 0 | 0 L |
| 100 | 20 L |
| 200 | 60 L |

Check point: raw 150 → calculated 40 L. No physical residual or uncertainty can be
claimed because no reference measurement was made. Out-of-range input is flagged.

For a real calibration record:

- Sensor/firmware/mounting, fluid type, tank instance and capacity:
- Reference instrument/known-volume method, uncertainty and date:
- Temperature, heel/trim and stabilization time:
- Repeated raw/reference pairs, rising/falling hysteresis:
- Curve fit and residuals; held-back verification samples:
- Valid range, unavailable/open/short/implausible-rate policy:
- Coefficient version/hash, prior version and rollback:
- Independent display/PGN/path observation:
- Recalibration trigger and owner:
