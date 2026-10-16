#!/usr/bin/env python3
"""Worked-example arithmetic; no wiring, calibration acquisition or device access."""
import math


def path_drop(segments):
    """Each tuple: one-way metres, ohms/metre per conductor, downstream amperes."""
    total=0.0
    for length,resistance,current in segments:
        if any(not math.isfinite(x) or x<0 for x in (length,resistance,current)):
            raise ValueError('finite nonnegative segment inputs required')
        total+=2*length*resistance*current
    return total


def interpolate(points, raw):
    """Piecewise calibration. No extrapolation, clamping or monotonic-output assumption."""
    if len(points)<2 or not math.isfinite(raw):
        raise ValueError('two calibration points and finite sample required')
    if any(not math.isfinite(x) or not math.isfinite(y) for x,y in points):
        raise ValueError('finite calibration points required')
    if any(b[0]<=a[0] for a,b in zip(points,points[1:])):
        raise ValueError('raw calibration coordinates must increase strictly')
    if not points[0][0]<=raw<=points[-1][0]:
        raise ValueError('outside calibrated range')
    for (x0,y0),(x1,y1) in zip(points,points[1:]):
        if x0<=raw<=x1:return y0+(raw-x0)*(y1-y0)/(x1-x0)
    raise ValueError('no calibration interval')


def below_keel(depth_below_transducer, transducer_below_surface, keel_below_surface):
    if any(not math.isfinite(x) or x<0 for x in (depth_below_transducer,transducer_below_surface,keel_below_surface)):
        raise ValueError('finite nonnegative geometry required')
    return depth_below_transducer+transducer_below_surface-keel_below_surface
