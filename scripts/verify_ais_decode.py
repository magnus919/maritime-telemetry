#!/usr/bin/env python3
"""Verify synthetic AIS/N2K against explicitly supplied offline CANboat binaries."""
import argparse
import json
import subprocess
from pathlib import Path
from ais_fixture import cases, raw_rows, can_frames


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decoded(text):
    result=[]
    for line in text.splitlines():
        item=json.loads(line)
        if 'version' in item:
            require(item['units']=='si','decoder must use SI');continue
        if 'pgn' not in item:  # -camel wraps the measurement under its identifier
            require(len(item)==1,'unexpected decoder wrapper')
            item=next(iter(item.values()))
        result.append(item)
    return result


def verify(rows):
    require(len(rows)==len(cases()),'missing or extra decoded records')
    for (ident,pgn,_),row in zip(cases(),rows):
        require(row['pgn']==pgn and row['src']==35,f'{ident}: PGN/source')
        f=row['fields']; mmsi='234567890' if ident=='second-target' else '123456789'
        require(str(f['userId'])==mmsi,f'{ident}: MMSI')
        if pgn in (129038,129039):
            require(f['sog']==5 and f['cog']==1 and f['heading']==.5,f'{ident}: SI motion')
            if ident=='unavailable-position':
                require(f.get('longitude') is None and f.get('latitude') is None,'NA position must not become zero')
            else:
                require(f['longitude']==(0 if ident=='zero-longitude' else -2) and f['latitude']==1,f'{ident}: position')
        if pgn==129809: require(f['name']=='LAB TARGET',f'{ident}: name')
        if pgn==129810:
            require((f['length'],f['beam'],f['callsign'])==(12,4,'LAB123'),f'{ident}: static B')
        if ident.endswith('legacy') or ident=='static-a-minimum':
            require(f.get('sequenceId') is None,f'{ident}: absent SID fabricated')
        if ident=='own-information':
            require(f['aisTransceiverInformation']=='Own information not broadcast','own marker')
    return {'decoded_cases':len(rows),'checks':['PGNs','receiver-vs-MMSI','SI-units','legacy-lengths','zero-coordinate','NA-position','own-marker','static-parts']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analyzer',required=True)
    parser.add_argument('--converter',required=True)
    parser.add_argument('--library-output',type=Path,required=True)
    args=parser.parse_args()
    require(args.library_output.read_text().splitlines()==raw_rows()[:4], 'library bytes differ from independent vectors')
    def run(argv,data):
        return subprocess.run(argv,input=data,text=True,capture_output=True,check=True,timeout=20).stdout
    command=[args.analyzer,'-json','-si','-camel','-empty']
    runs=[]
    for _ in range(3):
        direct=decoded(run(command,'\n'.join(raw_rows())+'\n'))
        converted=run([args.converter],'\n'.join(can_frames())+'\n')
        framed=decoded(run(command,converted))
        verify(direct);verify(framed)
        require([r['fields'] for r in direct]==[r['fields'] for r in framed],'CAN-frame and assembled decodes differ')
        runs.append({'direct':verify(direct),'fast_packet':verify(framed)})
    print(json.dumps({'passed':True,'scope':'synthetic offline software only','library_vectors':4,'runs':runs},indent=2))


if __name__=='__main__':
    main()
