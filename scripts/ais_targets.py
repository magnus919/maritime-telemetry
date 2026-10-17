#!/usr/bin/env python3
"""Bounded offline target-state teaching model, not collision-avoidance software."""
import math
from telemetry_lab import utc_seconds


class Targets:
    """Separate receiver provenance, target MMSI and per-family observation age.

    Caller supplies stable receiver identity and trusted receipt clocks. AIS seconds
    alone cannot supply a full timestamp. Class A/B position and static A/B only.
    Expiry is application policy; source selection remains the caller's decision.
    """
    def __init__(self, own_mmsi, expiry=60, capacity=1024):
        self.own = self.mmsi(own_mmsi)
        if not math.isfinite(expiry) or expiry<=0 or capacity<1:
            raise ValueError('invalid bounds')
        self.expiry,self.capacity=expiry,capacity
        self.rows={}
        self.last_mono=float('-inf')

    @staticmethod
    def mmsi(value):
        if type(value) not in (str,int):raise ValueError('MMSI must be digits')
        text=str(value)
        if not text.isascii() or not text.isdigit() or not 1<=len(text)<=9 or int(text)==0:
            raise ValueError('invalid MMSI representation')
        return text.zfill(9)  # Syntax normalization, not proof of assigned identity.

    def clock(self,now):
        if not math.isfinite(now) or now<self.last_mono:raise ValueError('monotonic clock required')
        self.last_mono=now

    def ingest(self,message,receiver,now,wall):
        self.clock(now)
        if not isinstance(receiver,str) or not receiver or not math.isfinite(wall):
            raise ValueError('stable receiver identity and wall clock required')
        pgn=message['pgn'];f=message['fields'];mmsi=self.mmsi(f['userId'])
        if pgn not in (129038,129039,129809,129810):raise ValueError('unsupported PGN')
        if mmsi==self.own or f.get('aisTransceiverInformation')=='Own information not broadcast':
            return 'own-excluded'
        stamp=utc_seconds(message['timestamp']);age=wall-stamp
        if age < -1:return 'clock-error'  # Does not poison timestamp ordering.
        key=(mmsi,receiver)
        if key not in self.rows and len(self.rows)>=self.capacity:raise ValueError('target capacity exhausted')
        family='position' if pgn in (129038,129039) else str(pgn)
        row=self.rows.setdefault(key,{})
        if family in row and stamp<=row[family]['stamp']:return 'replayed'
        values=dict(f)
        status='valid'
        if family=='position':
            lon,lat=f.get('longitude'),f.get('latitude')
            good=lambda x: type(x) in (int,float) and math.isfinite(x)
            if not (good(lon) and good(lat) and -180<=lon<=180 and -90<=lat<=90):
                status='unavailable';values={'longitude':None,'latitude':None}
        row[family]={'stamp':stamp,'arrival':now,'age':max(0,age),'status':status,'values':values,'pgn':pgn}
        return status

    def position(self,mmsi,receiver,now):
        self.clock(now)
        row=self.rows.get((self.mmsi(mmsi),receiver),{}).get('position')
        if not row:return {'status':'missing','position':None}
        age=row['age']+now-row['arrival']
        status=row['status']
        if status=='valid' and age>=self.expiry:status='stale'
        return {'status':status,'age':age,'position':
                {k:row['values'][k] for k in ('latitude','longitude')} if status=='valid' else None}
