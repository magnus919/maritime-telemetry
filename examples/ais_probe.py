#!/usr/bin/env python3
"""Optional independent decoder check: pyais==3.3.1; no devices or networking."""
from pathlib import Path
import json
from pyais import decode
root=Path(__file__).resolve().parents[1]
m=decode((root/'fixtures/ais-position.nmea').read_bytes().strip()).asdict()
expected={'msg_type':1,'mmsi':123456789,'lon':-2.,'lat':1.,'speed':10.,'course':90.,'heading':90,'second':30}
errors={k:{'expected':v,'actual':m.get(k)} for k,v in expected.items() if m.get(k)!=v}
print(json.dumps({'passed':not errors,'errors':errors,'scope':'synthetic AIS type 1 single-part decode'}))
raise SystemExit(1 if errors else 0)
