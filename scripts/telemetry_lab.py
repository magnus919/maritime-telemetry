#!/usr/bin/env python3
"""Offline teaching models, not production protocol stacks or actuator drivers."""
import json
import math
from datetime import datetime
from nmea_inspect import sentence


class SentenceStream:
    """Strict untagged profile. New delimiters resync; LF completes; bounded memory."""
    def __init__(self):
        self.buffer = bytearray()
        self.dropped = 0

    def feed(self, chunk):
        result = []
        for byte in chunk:
            if byte in (36, 33):
                if self.buffer:
                    self.dropped += 1
                self.buffer = bytearray([byte])
            elif self.buffer:
                self.buffer.append(byte)
                if byte == 10:
                    try:
                        result.append(sentence(self.buffer.decode('ascii')))
                    except (ValueError, UnicodeError) as error:
                        result.append({'accepted': False, 'error': str(error)})
                    self.buffer.clear()
                elif len(self.buffer) > 81:
                    self.buffer.clear()
                    self.dropped += 1
        return result


class FastPacket:
    """Explicitly classified PGNs only; strict ordered, bounded reassembly model.

    Timeout is experiment policy, not a normative protocol value. Single-frame
    PGNs and ISO TP are deliberately outside this class.
    """
    def __init__(self, pgns, timeout=0.25, capacity=16):
        if timeout <= 0 or capacity < 1:
            raise ValueError('invalid resource limits')
        self.pgns, self.timeout, self.capacity = set(pgns), timeout, capacity
        self.pending, self.last_time = {}, float('-inf')

    def feed(self, interface, source, destination, pgn, data, now):
        if not math.isfinite(now) or now < self.last_time:
            raise ValueError('monotonic time required')
        self.last_time = now
        self.pending = {k: v for k, v in self.pending.items() if now-v[3] < self.timeout}
        if pgn not in self.pgns:
            raise ValueError('PGN not explicitly classified as fast packet')
        if len(data) != 8:
            raise ValueError('lab profile requires eight-byte CAN frames')
        sequence, index = data[0] >> 5, data[0] & 31
        key = (interface, source, destination, pgn, sequence)
        if index == 0:
            length = data[1]
            self.pending.pop(key, None)
            if not 1 <= length <= 223:
                raise ValueError('invalid payload length')
            if len(self.pending) >= self.capacity:
                raise ValueError('assembly capacity exhausted')
            payload = bytearray(data[2:2+min(6, length)])
            if len(payload) == length:
                return bytes(payload)
            self.pending[key] = [length, payload, 1, now]
            return None
        state = self.pending.pop(key, None)
        if state is None or index != state[2]:
            raise ValueError('missing, duplicate, expired or out-of-order fragment')
        length, payload, _, _ = state
        payload.extend(data[1:1+min(7, length-len(payload))])
        if len(payload) == length:
            return bytes(payload)
        self.pending[key] = [length, payload, index+1, now]
        return None


def utc_seconds(text):
    parsed = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamp needs timezone')
    return parsed.timestamp()


class Samples:
    """Numeric own-vessel sample store; explicit source, timestamp and expiry.

    Deliberately not a full Signal K validator. Caller resolves source object into
    stable identity before passing rows; no last-arrival-wins source arbitration.
    """
    def __init__(self, expiry=3.0, future_tolerance=1.0):
        if expiry <= 0 or future_tolerance < 0:
            raise ValueError('invalid time policy')
        self.expiry, self.future_tolerance = expiry, future_tolerance
        self.rows = {}
        self.last_mono = float('-inf')

    def _clock(self, mono):
        if not math.isfinite(mono) or mono < self.last_mono:
            raise ValueError('monotonic time required')
        self.last_mono = mono

    def update(self, path, source, value, timestamp, arrival, wall):
        self._clock(arrival)
        if not path or not source or not math.isfinite(wall):
            raise ValueError('path, source and wall clock required')
        stamp = utc_seconds(timestamp)
        key = (path, source)
        old = self.rows.get(key)
        if old and old['status'] != 'clock-error' and stamp <= old['stamp']:
            return False  # duplicate/replayed timestamps cannot refresh age
        age = wall-stamp
        valid_number = type(value) in (int, float) and math.isfinite(value)
        status = 'valid' if valid_number else 'unavailable'
        if age < -self.future_tolerance:
            status = 'clock-error'
        elif age >= self.expiry:
            status = 'stale'
        self.rows[key] = dict(value=value if valid_number else None, stamp=stamp,
                              arrival=arrival, age=max(0, age), status=status)
        return True

    def read(self, path, source, now):
        self._clock(now)
        row = self.rows.get((path, source))
        if row is None:
            return {'status': 'missing', 'value': None}
        status = row['status']
        age = row['age'] + now-row['arrival']
        if status == 'valid' and age >= self.expiry:
            status = 'stale'
        return {'status': status, 'value': row['value'] if status == 'valid' else None,
                'source': source, 'age': age}


class RelayModel:
    """In-memory command/feedback model: never opens devices or sends commands."""
    def __init__(self, feedback_timeout=2.0, capacity=100):
        if feedback_timeout <= 0 or capacity < 1:
            raise ValueError('invalid limits')
        self.timeout, self.capacity = feedback_timeout, capacity
        self.requests, self.active = {}, None
        self.last_time = float('-inf')

    def tick(self, now):
        if not math.isfinite(now) or now < self.last_time:
            raise ValueError('monotonic time required')
        self.last_time = now
        if self.active:
            row = self.requests[self.active]
            if now >= row['deadline']:
                row['state'], self.active = 'timeout', None

    def request(self, ident, desired, now, expires, authorized=False, interlock=False):
        self.tick(now)
        if not isinstance(ident, str) or not ident or type(desired) is not bool:
            raise ValueError('request ID and boolean desired state required')
        if ident in self.requests:
            row = self.requests[ident]
            if row['desired'] != desired:
                raise ValueError('request ID reused with different intent')
            return row['state']
        if len(self.requests) >= self.capacity:
            raise ValueError('ledger full; do not discard replay protection implicitly')
        if not authorized or not interlock or not math.isfinite(expires) or expires <= now:
            state = 'rejected'
        elif self.active:
            state = 'busy'
        else:
            state, self.active = 'accepted', ident
        self.requests[ident] = {'desired': desired, 'state': state,
                               'deadline': min(expires, now+self.timeout), 'issued': now}
        return state

    def feedback(self, ident, observed, sampled, now):
        self.tick(now)
        if type(observed) is not bool or not math.isfinite(sampled):
            raise ValueError('typed feedback with time required')
        if ident != self.active:
            return False
        row = self.requests[ident]
        if not row['issued'] <= sampled <= now or observed != row['desired']:
            return False
        row['state'], self.active = 'achieved', None
        return True

    def override(self, now):
        self.tick(now)
        if self.active:
            self.requests[self.active]['state'] = 'overridden'
            self.active = None


def demo():
    samples = Samples()
    samples.update('environment.wind.speedApparent', 'fixture', 5.144444444,
                   '2026-01-01T00:00:00Z', 0, utc_seconds('2026-01-01T00:00:00Z'))
    fresh = samples.read('environment.wind.speedApparent', 'fixture', 1)
    stale = samples.read('environment.wind.speedApparent', 'fixture', 4)
    return {'scope': 'synthetic offline model', 'fresh': fresh, 'stale': stale,
            'knots': round(fresh['value']*3600/1852, 1)}

if __name__ == '__main__':
    print(json.dumps(demo(), sort_keys=True, allow_nan=False))
