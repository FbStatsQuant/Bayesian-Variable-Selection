"""Validate saved Owls evidence; never infer a pass from process completion alone."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('evidence_root')
    parser.add_argument('--indices', default=','.join(map(str, range(1, 33))))
    a = parser.parse_args()
    root = Path(a.evidence_root)
    expected = [int(x) for x in a.indices.split(',')]
    rows = []
    for index in expected:
        path = root / f'seed_{index}'
        problems = []
        try:
            m = json.loads((path / 'manifest.json').read_text())
            if m['index'] != index:
                problems.append('manifest seed index mismatch')
            rc = dict(line.split('\t') for line in (path / 'exit_status.tsv').read_text().splitlines())
            if set(rc) != {'prototype', 'production', 'comparison'} or any(int(x) for x in rc.values()):
                problems.append(f'nonzero/missing exit status: {rc}')
            comparison = json.loads((path / 'comparison.json').read_text())
            if not comparison or not all(x['ok'] for x in comparison.values()):
                problems.append('comparison/unit failure')
            validation = json.loads((path / 'source_validation.json').read_text())
            if not all(all(x.values()) for x in validation.values()):
                problems.append('source preservation failed')
            sums = json.loads((path / 'output_sha256.json').read_text())
            for name, expected_hash in sums.items():
                p = path / name
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected_hash:
                    problems.append(f'output hash mismatch: {name}')
            rows.append({'index': index, 'seed': m['seed'], 'ok': not problems,
                         'pid': m.get('pid'), 'checks': len(comparison),
                         'problems': problems, 'path': str(path)})
        except (OSError, ValueError, KeyError, TypeError) as error:
            rows.append({'index': index, 'ok': False, 'problems': [str(error)], 'path': str(path)})
    report = {'complete': len(rows) == len(expected), 'ok': all(x['ok'] for x in rows), 'rows': rows}
    cache = root / 'shared_compile_cache'
    if cache.exists():
        cache_hashes = {p.relative_to(cache).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(cache.rglob('*')) if p.is_file()}
        (root / 'compile_cache_sha256.json').write_text(json.dumps(cache_hashes, indent=2) + '\n')
    (root / 'SUITE_SUMMARY.json').write_text(json.dumps(report, indent=2) + '\n')
    text = ['# A build multi-seed evidence', '', f"Overall: {'PASS' if report['ok'] else 'FAIL / INCOMPLETE'}", '',
            '| Seed index | Method seed | Owls audit PID | Inspected checks | Result |',
            '|---|---|---|---|---|']
    for row in rows:
        text.append(f"| {row['index']} | {row.get('seed', '?')} | {row.get('pid', '?')} | {row.get('checks', 0)} | "
                    f"{'PASS' if row['ok'] else 'FAIL'} |")
        for problem in row['problems']:
            text.append(f"\nSeed {row['index']}: {problem}\n")
    (root / 'SUITE_SUMMARY.md').write_text('\n'.join(text) + '\n')
    print(f"Inspected {len(rows)} requested saved shards; {'PASS' if report['ok'] else 'FAIL / INCOMPLETE'}")
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
