#!/usr/bin/env python3
"""Offline framing checks, not a payload decoder or conformance validator."""

import argparse
import json
import re
import stat
import sys
from pathlib import Path

MAX_CAPTURE_BYTES = 1024 * 1024
MAX_RECORDS = 10000


def sentence(raw: str) -> dict:
    """Accept strict checksum-bearing ASCII sentences with optional log newline."""
    if raw.endswith("\r\n"):
        value = raw[:-2]
    elif raw.endswith("\n"):
        value = raw[:-1]
    else:
        value = raw
    if not value or any(ord(c) < 32 or ord(c) > 126 for c in value):
        raise ValueError("sentence must contain printable ASCII only")
    if len(value) + 2 > 82:
        raise ValueError("exceeds 82-byte sentence profile including CRLF")
    if value[0] not in "$!":
        raise ValueError("expected $ or !; tag blocks are not supported")
    if value.count("*") != 1:
        raise ValueError("expected exactly one checksum separator")
    body, supplied = value[1:].split("*")
    if not re.fullmatch(r"[0-9A-Fa-f]{2}", supplied):
        raise ValueError("checksum must be two hexadecimal digits")
    if any(c in body for c in "$!\\"):
        raise ValueError("embedded framing delimiter")
    header, separator, fields = body.partition(",")
    proprietary = header.startswith("P") and value.startswith("$")
    pattern = r"P[A-Z0-9]{3,}" if proprietary else r"[A-Z0-9]{5}"
    if not separator or not re.fullmatch(pattern, header):
        raise ValueError("unsupported sentence header")
    checksum = 0
    for c in body:
        checksum ^= ord(c)
    if int(supplied, 16) != checksum:
        raise ValueError(f"checksum mismatch: expected {checksum:02X}")
    return {
        "accepted": True,
        "profile": "untagged-ascii-checksum-82",
        "header": header,
        "talker": None if proprietary else header[:2],
        "formatter": None if proprietary else header[2:],
        "proprietary": proprietary,
        "fields": fields.split(","),
        "checksum": f"{checksum:02X}",
        "payload_semantics": "not_assessed",
    }


def can_id(value: str) -> dict:
    """Extract N2K extended identifier fields; input has no SocketCAN flags."""
    if not re.fullmatch(r"(?:0[xX][0-9a-fA-F]{1,8}|[0-9]{1,10})", value):
        raise ValueError("use decimal or 0x-prefixed hexadecimal identifier")
    identifier = int(value, 16 if value.lower().startswith("0x") else 10)
    if identifier > 0x1FFFFFFF:
        raise ValueError("identifier exceeds 29 bits; remove transport flags")
    if identifier & (1 << 25):
        raise ValueError("reserved N2K bit 25 must be zero")
    pf = (identifier >> 16) & 255
    ps = (identifier >> 8) & 255
    pgn = (identifier >> 8) & 0x1FFFF
    if pf < 240:
        pgn &= 0x1FF00
    return {
        "accepted": True,
        "identifier": f"0x{identifier:08X}",
        "priority": (identifier >> 26) & 7,
        "pgn": pgn,
        "source": identifier & 255,
        "destination": ps if pf < 240 else 255,
        "pdu": 1 if pf < 240 else 2,
        "payload_semantics": "not_assessed",
        "note": "Identifier fields only; PGN assignment and source validity not assessed",
    }


def capture(path: Path) -> dict:
    # Reject devices/FIFOs before opening: this tool must never open a bus device.
    if not stat.S_ISREG(path.stat().st_mode):
        raise OSError("capture must be a regular file")
    with path.open("rb") as stream:
        data = stream.read(MAX_CAPTURE_BYTES + 1)
    if len(data) > MAX_CAPTURE_BYTES:
        raise ValueError("capture exceeds 1 MiB offline limit; split it first")
    # Split only on LF, not every Unicode/control separator; retain CR for validation.
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    if not lines:
        raise ValueError("capture is empty")
    if len(lines) > MAX_RECORDS:
        raise ValueError("capture exceeds 10000 records; split it first")
    records = []
    for number, line in enumerate(lines, 1):
        try:
            # Appending LF restores a normalized log terminator.
            record = sentence((line + b"\n").decode("ascii"))
        except (ValueError, UnicodeError) as error:
            record = {"accepted": False, "error": str(error)}
        records.append({"line": number, **record})
    rejected = sum(not row["accepted"] for row in records)
    return {"accepted": rejected == 0, "rejected": rejected, "records": records}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sentence").add_argument("value")
    sub.add_parser("can-id").add_argument("value")
    sub.add_parser("file").add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "sentence":
            result = sentence(args.value)
        elif args.command == "can-id":
            result = can_id(args.value)
        else:
            result = capture(args.path)
    except OSError as error:
        print(json.dumps({"accepted": False, "error": str(error)}))
        return 2
    except ValueError as error:
        print(json.dumps({"accepted": False, "error": str(error)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main())
