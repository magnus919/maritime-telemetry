import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from check_change_contract import assess, changed_paths, main


class ChangeContractTests(unittest.TestCase):
    def test_documentation_only(self):
        self.assertTrue(assess(['references/signalk.md'])['passed'])

    def test_code_requires_both_documentation_and_tests(self):
        for paths in (['scripts/ais_targets.py'],
                      ['scripts/ais_targets.py', 'README.md'],
                      ['scripts/ais_targets.py', 'scripts/test_ais.py']):
            self.assertFalse(assess(paths)['passed'], paths)
        self.assertTrue(assess(['scripts/ais_targets.py', 'README.md', 'scripts/test_ais.py'])['passed'])

    def test_dependency_and_ci_changes_are_code(self):
        for path in ('examples/signalk-lab/package-lock.json', '.github/workflows/validate.yml',
                     'examples/esp32-n2k/platformio.ini', '.github/policies/main-protection.json',
                     '.github/dependabot.yml', 'scripts/check.sh', 'requirements-dev.txt', '.coveragerc'):
            self.assertFalse(assess([path])['passed'])
            self.assertTrue(assess([path, 'CONTRIBUTING.md', 'scripts/test_change_contract.py'])['passed'])

    def test_optional_integration_tests(self):
        for test in ('examples/ais-n2k-lab/probe.cjs', 'examples/protocol_oracle.cpp'):
            self.assertTrue(assess(['examples/esp32-n2k/src/main.cpp', 'references/embedded-recipes.md', test])['passed'])
        for artifact in ('evals/evals.json', 'evidence/run.json'):
            self.assertFalse(assess(['scripts/telemetry_lab.py', 'README.md', artifact])['passed'])

    def test_real_git_diff_includes_deletions_and_unusual_names(self):
        with tempfile.TemporaryDirectory() as folder:
            def git(*args):
                return subprocess.check_output(['git', '-C', folder, *args], text=True).strip()
            git('init', '-q'); git('config', 'user.name', 'Contract Test')
            git('config', 'user.email', 'synthetic@example.invalid')
            p = Path(folder) / 'old.py'; p.write_text('old\n')
            git('add', '.'); git('commit', '-qm', 'base'); base = git('rev-parse', 'HEAD')
            p.unlink(); (Path(folder) / 'new file\nname.py').write_text('new\n')
            git('add', '.'); git('commit', '-qm', 'candidate'); head = git('rev-parse', 'HEAD')
            with patch('check_change_contract.subprocess.run', wraps=subprocess.run) as run:
                # Run the real parser from a repository working directory.
                import os
                previous = os.getcwd()
                try:
                    os.chdir(folder)
                    self.assertEqual(set(changed_paths(base, head)), {'old.py', 'new file\nname.py'})
                finally:
                    os.chdir(previous)
            self.assertEqual(run.call_count, 1)

    def test_cli_exit_status_tracks_failure(self):
        with patch('check_change_contract.changed_paths', return_value=['scripts/ais_targets.py']), \
             patch('builtins.print'):
            self.assertEqual(main(['--base', 'base']), 1)
        with patch('check_change_contract.changed_paths', return_value=['README.md']), \
             patch('builtins.print'):
            self.assertEqual(main(['--base', 'base']), 0)


if __name__ == '__main__':
    unittest.main()
