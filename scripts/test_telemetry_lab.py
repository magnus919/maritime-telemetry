import unittest
from telemetry_lab import SentenceStream, FastPacket, Samples, RelayModel, utc_seconds


class StreamTests(unittest.TestCase):
    raw = b'$GPGLL,4916.45,N,12311.12,W,225444,A,*1D\r\n'

    def test_every_split(self):
        for split in range(len(self.raw)+1):
            s = SentenceStream()
            result = s.feed(self.raw[:split])+s.feed(self.raw[split:])
            self.assertEqual(len(result), 1)
            self.assertTrue(result[0]['accepted'])

    def test_noise_corruption_and_recovery(self):
        s = SentenceStream()
        result = s.feed(b'noise$broken'+self.raw+self.raw.replace(b'*1D', b'*00'))
        self.assertEqual([r['accepted'] for r in result], [True, False])
        self.assertEqual(s.dropped, 1)

    def test_bound_and_partial(self):
        s = SentenceStream()
        self.assertEqual(s.feed(b'$'+b'x'*100000), [])
        self.assertLessEqual(len(s.buffer), 81)
        self.assertTrue(s.feed(self.raw)[0]['accepted'])


class PacketTests(unittest.TestCase):
    def frame(self, seq, ix, payload):
        return bytes([(seq << 5)|ix])+payload+b'\xff'*(7-len(payload))

    def test_interleaved_and_interface_isolation(self):
        f = FastPacket([126996])
        for source in (1,2):
            self.assertIsNone(f.feed('can0',source,255,126996,self.frame(7,0,b'\x0aABCDEF'),0))
        self.assertEqual(f.feed('can0',2,255,126996,self.frame(7,1,b'GHIJ'),.1),b'ABCDEFGHIJ')
        with self.assertRaises(ValueError):
            f.feed('can1',1,255,126996,self.frame(7,1,b'GHIJ'),.1)
        self.assertEqual(f.feed('can0',1,255,126996,self.frame(7,1,b'GHIJ'),.2),b'ABCDEFGHIJ')

    def test_short_classified_packet(self):
        f = FastPacket([126996])
        self.assertEqual(f.feed('c',1,255,126996,self.frame(0,0,b'\x03ABC'),0),b'ABC')
        with self.assertRaises(ValueError): f.feed('c',1,255,127250,b'12345678',0)

    def test_gap_timeout_and_duplicate(self):
        for ix,now in [(2,.1),(1,.3)]:
            f=FastPacket([126996]);f.feed('c',1,255,126996,self.frame(0,0,b'\x14ABCDEF'),0)
            with self.assertRaises(ValueError): f.feed('c',1,255,126996,self.frame(0,ix,b'GHIJKLM'),now)
            self.assertEqual(f.pending,{})
        f=FastPacket([126996]);f.feed('c',1,255,126996,self.frame(0,0,b'\x14ABCDEF'),0)
        f.feed('c',1,255,126996,self.frame(0,1,b'GHIJKLM'),.1)
        with self.assertRaises(ValueError):f.feed('c',1,255,126996,self.frame(0,1,b'GHIJKLM'),.2)

    def test_restart_capacity_and_length(self):
        f=FastPacket([126996],capacity=1)
        f.feed('c',1,255,126996,self.frame(0,0,b'\x0aABCDEF'),0)
        with self.assertRaises(ValueError):f.feed('c',2,255,126996,self.frame(0,0,b'\x0aABCDEF'),0)
        self.assertEqual(f.feed('c',1,255,126996,self.frame(0,0,b'\x01Z'),0),b'Z')
        with self.assertRaises(ValueError):f.feed('c',1,255,126996,self.frame(0,0,b'\x00'),0)

    def test_max_length_and_sequence_wrap(self):
        f=FastPacket([126996]);payload=bytes(range(223))
        for seq in (7,0):
            f.feed('c',1,255,126996,self.frame(seq,0,bytes([223])+payload[:6]),0)
            for ix,start in enumerate(range(6,223,7),1):
                result=f.feed('c',1,255,126996,self.frame(seq,ix,payload[start:start+7]),0)
            self.assertEqual(result,payload)


class SampleTests(unittest.TestCase):
    stamp='2026-01-01T00:00:00Z'
    wall=utc_seconds(stamp)

    def test_source_selection_and_expiry(self):
        s=Samples();s.update('wind','A',5,self.stamp,0,self.wall)
        s.update('wind','B',9,self.stamp,1,self.wall)
        self.assertEqual(s.read('wind','A',1)['value'],5)
        self.assertEqual(s.read('wind','A',3)['status'],'stale')
        self.assertEqual(s.read('wind','missing',3)['status'],'missing')

    def test_types_and_null(self):
        for value in (None, True, '3', {}, float('nan'), float('inf')):
            s=Samples();s.update('p','s',value,self.stamp,0,self.wall)
            self.assertEqual(s.read('p','s',0)['status'],'unavailable')
        s=Samples();s.update('p','s',0,self.stamp,0,self.wall)
        self.assertEqual(s.read('p','s',0)['value'],0)

    def test_duplicate_does_not_refresh(self):
        s=Samples();s.update('p','s',1,self.stamp,0,self.wall)
        self.assertFalse(s.update('p','s',2,self.stamp,2,self.wall+2))
        self.assertEqual(s.read('p','s',3)['status'],'stale')

    def test_corrected_clock_recovers(self):
        s=Samples()
        s.update('p','s',1,'2026-01-01T01:00:00Z',0,self.wall)
        self.assertEqual(s.read('p','s',0)['status'],'clock-error')
        self.assertTrue(s.update('p','s',2,self.stamp,1,self.wall))
        self.assertEqual(s.read('p','s',1)['value'],2)

    def test_old_future_and_monotonic(self):
        for wall,status in [(self.wall+10,'stale'),(self.wall-10,'clock-error')]:
            s=Samples();s.update('p','s',1,self.stamp,0,wall)
            self.assertEqual(s.read('p','s',0)['status'],status)
            with self.assertRaises(ValueError):s.read('p','s',-1)
        with self.assertRaises(ValueError):utc_seconds('2026-01-01T00:00:00')


class ControlTests(unittest.TestCase):
    def test_permission_and_feedback(self):
        r=RelayModel()
        self.assertEqual(r.request('denied',True,0,5),'rejected')
        self.assertEqual(r.request('ok',True,0,5,True,True),'accepted')
        self.assertFalse(r.feedback('ok',True,-1,.5))
        self.assertFalse(r.feedback('ok',False,.5,.5))
        self.assertTrue(r.feedback('ok',True,1,1))
        self.assertEqual(r.requests['ok']['state'],'achieved')

    def test_replay_and_conflict(self):
        r=RelayModel();r.request('x',True,0,5,True,True)
        self.assertEqual(r.request('x',True,1,10,True,True),'accepted')
        with self.assertRaises(ValueError):r.request('x',False,1,10,True,True)
        r.tick(2)
        self.assertEqual(r.request('x',True,3,10,True,True),'timeout')

    def test_override_busy_expired(self):
        r=RelayModel();self.assertEqual(r.request('old',True,0,0,True,True),'rejected')
        r.request('a',True,0,10,True,True)
        self.assertEqual(r.request('b',False,0,10,True,True),'busy')
        r.override(1);self.assertEqual(r.requests['a']['state'],'overridden')
        self.assertFalse(r.feedback('a',True,1,1))

    def test_capacity_and_typed_feedback(self):
        r=RelayModel(capacity=1);r.request('a',True,0,5,True,True)
        with self.assertRaises(ValueError):r.request('b',True,0,5,True,True)
        with self.assertRaises(ValueError):r.feedback('a',1,0,0)

if __name__=='__main__':unittest.main()
