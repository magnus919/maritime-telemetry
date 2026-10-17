#!/usr/bin/env python3
"""Independently inspect the optional converter's output using pyais3.3.1."""
import json
import sys
from pyais import decode


def check(ok, why):
    if not ok:
        raise ValueError(why)


report=json.load(open(sys.argv[1]))
trials=[]
for trial in report['trials']:
    rows=[decode(s).asdict() if s else None for s in trial['sentences']]
    a,b,part_a,part_b=rows[:4]
    check((a['mmsi'],a['lon'],a['lat'])==(123456789,-2,1),'class A position')
    check((b['mmsi'],b['lon'],b['lat'])==(123456789,-2,1),'class B position')
    check(a['msg_type']==3 and b['msg_type']==18,'observed type conversion')
    check(a['speed']==9.7 and a['course']==57 and a['heading']==29,'observed rounding')
    check(a['second']==60 and not a['accuracy'],'observed Class A metadata loss')
    check(part_a['shipname']=='LAB TARGET' and part_b['callsign']=='LAB123','static parts')
    check((part_b['to_bow'],part_b['to_stern'],part_b['to_port'],part_b['to_starboard'])==(8,4,3,1),'geometry')
    check(part_b['vendorid']=='','observed vendor loss')
    check(rows[8]['lon']==0 and rows[9]['lon']==181 and rows[9]['lat']==91,'zero vs unavailable')
    check(rows[11] is None,'own report not suppressed')
    trials.append(rows)
print(json.dumps({'passed':True,'meaning':'recorded behavior reproduced, not lossless interoperability',
                  'pyais':'3.3.1','trials':trials},indent=2))
