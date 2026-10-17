import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from ais_fixture import raw_rows
from verify_ais_decode import decoded, main, verify

ROOT = Path(__file__).resolve().parent.parent


class AISVerifierTests(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads((ROOT / 'evidence/ais-n2k-decoded.json').read_text())

    def test_rejects_wrong_count_and_fields(self):
        with self.assertRaises(ValueError):
            verify(self.rows[:-1])
        for index, field, value in ((0, 'sog', 9.7), (0, 'userId', '1'),
                                    (3, 'callsign', 'WRONG'), (2, 'name', 'OTHER'),
                                    (8, 'longitude', None), (9, 'latitude', 0),
                                    (4, 'sequenceId', 7), (11, 'aisTransceiverInformation', 'Other')):
            rows = copy.deepcopy(self.rows)
            rows[index]['fields'][field] = value
            with self.assertRaises(ValueError):
                verify(rows)
        rows = copy.deepcopy(self.rows); rows[0]['src'] = 36
        with self.assertRaises(ValueError):
            verify(rows)

    def test_decoder_envelopes_and_units(self):
        self.assertEqual(decoded(json.dumps(self.rows[0])), [self.rows[0]])
        self.assertEqual(decoded(json.dumps({'identifier': self.rows[0]})), [self.rows[0]])
        self.assertEqual(decoded('{"version":"test","units":"si"}'), [])
        with self.assertRaises(ValueError):
            decoded('{"version":"test","units":"std"}')
        with self.assertRaises(ValueError):
            decoded('{"first":{},"second":{}}')

    def test_cli_runs_both_paths_and_rejects_encoder_mismatch(self):
        class Result:
            stdout = '\n'.join(json.dumps(row) for row in self.rows)
        with tempfile.TemporaryDirectory() as folder:
            fixture = Path(folder) / 'library.raw'
            fixture.write_text('\n'.join(raw_rows()[:4])+'\n')
            argv = ['--analyzer', 'analyzer', '--converter', 'converter', '--library-output', str(fixture)]
            with patch('verify_ais_decode.subprocess.run', return_value=Result()) as run, \
                 patch('sys.argv', ['verify_ais_decode.py', *argv]), \
                 contextlib.redirect_stdout(io.StringIO()) as stream:
                main()
            self.assertTrue(json.loads(stream.getvalue())['passed'])
            self.assertEqual(run.call_count, 9)
            self.assertTrue(all(call.kwargs['check'] for call in run.call_args_list))
            fixture.write_text('wrong payload\n')
            with patch('sys.argv', ['verify_ais_decode.py', *argv]), self.assertRaises(ValueError):
                main()


if __name__ == '__main__':
    unittest.main()
