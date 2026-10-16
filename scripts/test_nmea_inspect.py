#!/usr/bin/env python3
"""Offline regression cases with independent known vectors and adversarial input."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import nmea_inspect as inspector


class SentenceTests(unittest.TestCase):
    VECTOR = "$GPGLL,4916.45,N,12311.12,W,225444,A,*1D"

    def test_known_vector_and_empty_field(self):
        result = inspector.sentence(self.VECTOR)
        self.assertEqual(result["checksum"], "1D")
        self.assertEqual(result["fields"][-1], "")
        self.assertEqual(result["talker"], "GP")
        self.assertEqual(result["payload_semantics"], "not_assessed")

    def test_sentence_length_boundary(self):
        self.assertTrue(inspector.sentence("$PABC," + "A" * 71 + "*7D")["accepted"])
        with self.assertRaises(ValueError):
            inspector.sentence("$PABC," + "A" * 72 + "*3C")

    def test_log_endings(self):
        for ending in ("", "\n", "\r\n"):
            with self.subTest(ending=ending):
                self.assertTrue(inspector.sentence(self.VECTOR + ending)["accepted"])

    def test_corruption_and_unsupported_profiles(self):
        cases = [
            self.VECTOR[:-2] + "00",
            self.VECTOR[:-3],
            self.VECTOR + "X",
            self.VECTOR + "\r",
            self.VECTOR + "\r\n\r\n",
            "",
            "\\s:source*00\\" + self.VECTOR,
            "$GPGLL," + "x" * 80 + "*00",
            "$GPGLL,é*00",
            "$GPGLL,\x00*00",
            "$GPGLL,foo*GG",
            "$GPGLL,foo**00",
            "$GP,foo*00",
            "$GPGLL,$x*00",
        ]
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                inspector.sentence(value)

    def test_proprietary_opaque(self):
        # PABC, XOR = 0x3c; no claim about proprietary field semantics.
        result = inspector.sentence("$PABC,*3C")
        self.assertTrue(result["proprietary"])
        self.assertIsNone(result["formatter"])

    def test_ais_envelope_only(self):
        # Synthetic, empty encapsulated payload; framing accepted, payload unassessed.
        result = inspector.sentence("!AIVDM,1,1,,A,,0*26")
        self.assertEqual(result["formatter"], "VDM")
        self.assertEqual(result["payload_semantics"], "not_assessed")


class IdentifierTests(unittest.TestCase):
    def test_heading_broadcast(self):
        result = inspector.can_id("0x09F11223")
        self.assertEqual(
            (
                result["pgn"],
                result["source"],
                result["priority"],
                result["destination"],
            ),
            (127250, 35, 2, 255),
        )

    def test_addressed_request(self):
        result = inspector.can_id("0x18EA232A")
        self.assertEqual(
            (result["pgn"], result["source"], result["destination"]), (59904, 42, 35)
        )

    def test_pf_boundary(self):
        self.assertEqual(inspector.can_id("0x18EF232A")["pgn"], 61184)
        self.assertEqual(inspector.can_id("0x18F0232A")["pgn"], 61475)
        self.assertEqual(inspector.can_id("0x18F0232A")["destination"], 255)

    def test_decimal(self):
        self.assertEqual(inspector.can_id("166793763")["pgn"], 127250)

    def test_flags_reserved_and_bad_input(self):
        for value in (
            "-1",
            "0x80000000",
            "0x20000000",
            "0x02000000",
            "abc",
            "0x",
            "1.0",
            "１２",
            " 12",
            "0x" + "0" * 100,
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                inspector.can_id(value)


class FileAndCliTests(unittest.TestCase):
    def test_mixed_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "capture.nmea"
            path.write_bytes(SentenceTests.VECTOR.encode() + b"\r\n\xff\n\n")
            result = inspector.capture(path)
            self.assertFalse(result["accepted"])
            self.assertEqual(result["rejected"], 2)
            self.assertEqual(len(result["records"]), 3)

    def test_limits_and_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "capture.nmea"
            for data in (
                b"",
                b"x" * (inspector.MAX_CAPTURE_BYTES + 1),
                b"\n" * (inspector.MAX_RECORDS + 1),
            ):
                path.write_bytes(data)
                with self.assertRaises(ValueError):
                    inspector.capture(path)

    def test_refuses_nonregular(self):
        with tempfile.TemporaryDirectory() as folder, self.assertRaises(OSError):
            inspector.capture(Path(folder))

    def test_json_and_exit_statuses(self):
        for args, expected in (
            (["can-id", "0x09F11223"], 0),
            (["sentence", "invalid"], 1),
            (["file", "/nonexistent/maritime-fixture"], 2),
        ):
            with (
                self.subTest(args=args),
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                self.assertEqual(inspector.main(args), expected)
                result = json.loads(out.getvalue())
                self.assertEqual(result["accepted"], expected == 0)


if __name__ == "__main__":
    unittest.main()
