#!/usr/bin/env python3
"""Ensure damaged artifacts fail the repository's structural gate."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_skill import validate

ROOT = Path(__file__).resolve().parent.parent


class ValidationTests(unittest.TestCase):
    def test_repository(self):
        self.assertEqual(validate(ROOT), [])

    def test_broken_link_and_invalid_eval(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("SKILL.md", "README.md", "LICENSE"):
                shutil.copy(ROOT / name, root / name)
            shutil.copytree(ROOT / "evals", root / "evals")
            with (root / "README.md").open("a") as out:
                out.write("\n[Missing](missing.md)\n")
            manifest = json.loads((root / "evals/evals.json").read_text())
            manifest["evals"][0]["assertions"] = []
            (root / "evals/evals.json").write_text(json.dumps(manifest))
            errors = validate(root)
            self.assertTrue(any("missing.md" in error for error in errors))
            self.assertTrue(any("invalid assertions" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
