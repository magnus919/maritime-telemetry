#!/usr/bin/env python3
"""Check code/documentation/test co-changes between two Git revisions.

This is a structural PR gate. Review must still assess relevance and test quality.
"""
import argparse
import json
from pathlib import PurePosixPath
import subprocess


CODE_SUFFIXES = {'.py', '.c', '.cpp', '.cxx', '.h', '.hpp', '.js', '.cjs', '.mjs', '.ts'}


def classify(path):
    p = PurePosixPath(path)
    docs = p.suffix == '.md' or path.startswith('templates/')
    tests = (path.startswith('scripts/test_') and p.suffix == '.py') or (
        path.startswith('examples/') and (p.name in {'probe.cjs', 'lab.cjs'} or p.name.endswith('_oracle.cpp'))
    )
    code = (path.startswith(('scripts/', 'examples/')) and (
        p.suffix in CODE_SUFFIXES or p.name in {'package.json', 'package-lock.json', 'platformio.ini'}
    )) or path.startswith('.github/workflows/') or path in {'requirements-dev.txt', '.coveragerc'}
    return code, docs, tests


def assess(paths):
    groups = {key: [] for key in ('code', 'docs', 'tests')}
    for path in sorted(set(paths)):
        for key, selected in zip(groups, classify(path)):
            if selected:
                groups[key].append(path)
    errors = []
    if groups['code']:
        if not groups['docs']:
            errors.append('Code/config/dependency changes require relevant documentation changes.')
        if not groups['tests']:
            errors.append('Code/config/dependency changes require test updates.')
    return {'passed': not errors, 'changed': groups, 'errors': errors,
            'scope': 'Co-change presence only; relevance, coverage and outcomes have separate checks.'}


def changed_paths(base, head):
    output = subprocess.run(
        ['git', 'diff', '--name-only', '-z', '--no-renames', base, head, '--'],
        check=True, capture_output=True
    ).stdout
    return [path.decode('utf-8') for path in output.split(b'\0') if path]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', default='HEAD')
    args = parser.parse_args(argv)
    result = assess(changed_paths(args.base, args.head))
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
