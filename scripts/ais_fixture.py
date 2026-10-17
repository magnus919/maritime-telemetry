#!/usr/bin/env python3
"""Original synthetic AIS/N2K vectors. Stdout only; no hardware or networking."""
import argparse
import json
import struct


def cases():
    # Independent scaled integers: MMSI, longitude -2e7, latitude 1e7;
    # seconds30/accuracy1; COG10000, SOG500, heading5000. Little endian.
    prefix = struct.pack('<IiiBHH', 123456789, -20000000, 10000000, 121, 10000, 500)
    common = prefix + bytes.fromhex('ffff07') + struct.pack('<H', 5000)
    a = bytes([1]) + common + struct.pack('<h', 0) + bytes.fromhex('f0fc07')
    b = bytes([18]) + common + bytes.fromhex('ff04fe07')
    ident = bytes([24]) + struct.pack('<I', 123456789)
    part_a = ident + b'LAB TARGET'.ljust(20, b'@') + bytes.fromhex('e007')
    part_b = ident + bytes([36]) + b'LAB'.ljust(7,b'@') + b'LAB123'.ljust(7,b'@')
    part_b += struct.pack('<HHHHI',120,40,10,80,0) + bytes.fromhex('03e007')
    rows = [('class-a',129038,a), ('class-b',129039,b),
            ('static-a',129809,part_a), ('static-b',129810,part_b),
            ('class-a-legacy',129038,a[:-1]), ('class-b-legacy',129039,b[:-1]),
            ('static-a-legacy',129809,part_a[:-1]), ('static-b-legacy',129810,part_b[:33])]
    zero = bytearray(a); zero[5:13] = struct.pack('<ii',0,10000000)
    unavailable = bytearray(a); unavailable[5:13] = struct.pack('<ii',0x7fffffff,0x7fffffff)
    other = bytearray(a); other[1:5] = struct.pack('<I',234567890)
    own = bytearray(a); own[20] = 0x27  # 19-bit comm state; transceiver-info = 4
    rows += [('zero-longitude',129038,bytes(zero)), ('unavailable-position',129038,bytes(unavailable)),
             ('second-target',129038,bytes(other)), ('own-information',129038,bytes(own)), ('static-a-minimum',129809,part_a[:25])]
    return rows


def raw_rows():
    return ['2026-01-01T00:00:00.000Z,%d,%d,35,255,%d,%s' %
            (4 if pgn in (129038,129039) else 6,pgn,len(payload),','.join(f'{b:02x}' for b in payload))
            for _,pgn,payload in cases()]


def can_frames():
    """Explicit Fast PGNs only; unique sequence per message, wrap after eight."""
    for n,(_,pgn,data) in enumerate(cases()):
        priority = 4 if pgn in (129038,129039) else 6
        can_id = (priority<<26)|(pgn<<8)|35
        chunks=[bytes([len(data)])+data[:6]]+[data[i:i+7] for i in range(6,len(data),7)]
        for i,chunk in enumerate(chunks):
            frame=(bytes([((n%8)<<5)|i])+chunk).ljust(8,b'\xff')
            yield f'({1767225600+n/10+i/10000:.6f}) can0 {can_id:08X}#{frame.hex().upper()}'


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--format',choices=['raw','candump','index'],default='raw')
    args=parser.parse_args()
    if args.format=='index':
        print(json.dumps([{'id':i,'pgn':p,'length':len(d)} for i,p,d in cases()],indent=2))
    else:
        print('\n'.join(raw_rows() if args.format=='raw' else can_frames()))
