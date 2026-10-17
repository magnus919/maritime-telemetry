import copy
import json
import unittest
from pathlib import Path
from ais_fixture import cases,raw_rows,can_frames
from ais_targets import Targets
from telemetry_lab import FastPacket,utc_seconds
from verify_ais_decode import verify

ROOT=Path(__file__).resolve().parent.parent


class AISFixtures(unittest.TestCase):
    def test_frozen_fixture_generation(self):
        self.assertEqual((ROOT/'fixtures/ais-n2k.raw').read_text().splitlines(),raw_rows())
        self.assertEqual((ROOT/'fixtures/ais-n2k.candump').read_text().splitlines(),list(can_frames()))

    def test_packet_reassembly(self):
        f=FastPacket([129038,129039,129809,129810]);out=[]
        for line in can_frames():
            when,_,frame=line.split();canid,data=frame.split('#');ident=int(canid,16)
            result=f.feed('can0',ident&255,255,(ident>>8)&0x3ffff,bytes.fromhex(data),float(when[1:-1]))
            if result is not None:out.append(result)
        self.assertEqual(out,[x[2] for x in cases()])

    def test_verifier_rejects_corrupt_semantics(self):
        rows=json.loads((ROOT/'evidence/ais-n2k-decoded.json').read_text())
        verify(rows)
        rows[0]['fields']['sog']=9.7
        with self.assertRaises(ValueError):verify(rows)


class AISTargets(unittest.TestCase):
    def setUp(self):
        self.wall=utc_seconds('2026-01-01T00:00:00Z')
        self.msg={'pgn':129038,'timestamp':'2026-01-01T00:00:00Z',
                  'fields':{'userId':'123456789','longitude':-2,'latitude':1}}
        self.t=Targets('987654321',expiry=3)

    def test_mmsi_not_receiver_is_target(self):
        self.t.ingest(self.msg,'bus1:NAME1',0,self.wall)
        m=copy.deepcopy(self.msg);m['fields']['userId']='234567890'
        self.t.ingest(m,'bus1:NAME1',0,self.wall)
        self.assertEqual(len(self.t.rows),2)

    def test_receiver_provenance_not_last_writer_wins(self):
        self.t.ingest(self.msg,'A',0,self.wall)
        m=copy.deepcopy(self.msg);m['fields']['latitude']=2
        self.t.ingest(m,'B',0,self.wall)
        self.assertEqual(self.t.position('123456789','A',0)['position']['latitude'],1)

    def test_static_does_not_refresh_position(self):
        self.t.ingest(self.msg,'A',0,self.wall)
        for pgn in (129809,129810):
            m=copy.deepcopy(self.msg);m['pgn']=pgn;m['timestamp']='2026-01-01T00:00:02Z'
            self.t.ingest(m,'A',2,self.wall+2)
        self.assertEqual(len(self.t.rows[('123456789','A')]),3)
        self.assertEqual(self.t.position('123456789','A',3)['status'],'stale')

    def test_zero_coordinate_and_unavailable_clear(self):
        self.msg['fields']['longitude']=0
        self.t.ingest(self.msg,'A',0,self.wall)
        self.assertEqual(self.t.position('123456789','A',0)['position']['longitude'],0)
        self.msg['timestamp']='2026-01-01T00:00:01Z';self.msg['fields']['latitude']=None
        self.t.ingest(self.msg,'A',1,self.wall+1)
        self.assertEqual(self.t.position('123456789','A',1)['status'],'unavailable')

    def test_replay_does_not_refresh(self):
        self.t.ingest(self.msg,'A',0,self.wall)
        self.assertEqual(self.t.ingest(self.msg,'A',2,self.wall+2),'replayed')
        self.assertEqual(self.t.position('123456789','A',3)['status'],'stale')

    def test_future_time_recovery(self):
        self.assertEqual(self.t.ingest(self.msg,'A',0,self.wall-3600),'clock-error')
        self.assertEqual(self.t.ingest(self.msg,'A',1,self.wall),'valid')

    def test_own_and_unsupported(self):
        self.msg['fields']['userId']='987654321'
        self.assertEqual(self.t.ingest(self.msg,'A',0,self.wall),'own-excluded')
        self.msg['fields']['userId']='123456789';self.msg['fields']['aisTransceiverInformation']='Own information not broadcast'
        self.assertEqual(self.t.ingest(self.msg,'A',0,self.wall),'own-excluded')
        self.msg['pgn']=129041
        with self.assertRaises(ValueError):self.t.ingest(self.msg,'A',0,self.wall)

    def test_invalid_identity_capacity_clock(self):
        for value in (0,True,'NaN',1234567890):
            with self.assertRaises(ValueError):Targets.mmsi(value)
        t=Targets('987654321',capacity=1);t.ingest(self.msg,'A',0,self.wall)
        with self.assertRaises(ValueError):t.ingest(self.msg,'B',0,self.wall)
        with self.assertRaises(ValueError):t.position('123456789','A',-1)

if __name__=='__main__':unittest.main()
