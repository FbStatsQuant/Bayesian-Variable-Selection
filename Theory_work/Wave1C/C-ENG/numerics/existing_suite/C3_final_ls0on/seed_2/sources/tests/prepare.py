"""Audit/source preparation only; not a numerical workload. Run remotely by runner."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def inventory(root):
    root = Path(root).resolve()
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and not any(part in {'.cpp_cache', '__pycache__'} for part in p.relative_to(root).parts)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['prepare', 'finish'])
    parser.add_argument('out')
    parser.add_argument('--prototype')
    parser.add_argument('--production')
    parser.add_argument('--tests')
    parser.add_argument('--index', type=int)
    a = parser.parse_args()
    out = Path(a.out).resolve()
    if a.operation == 'prepare':
        if out.exists():
            raise SystemExit(f'Refusing to overwrite evidence directory: {out}')
        out.mkdir(parents=True)
        sources = {}
        for label, path in [('prototype', a.prototype), ('production', a.production), ('tests', a.tests)]:
            source = Path(path).resolve()
            target = out / 'sources' / label
            before = inventory(source)
            shutil.copytree(source, target, ignore=shutil.ignore_patterns('.cpp_cache', '__pycache__'))
            after = inventory(source)
            if before != after or before != inventory(target):
                raise SystemExit(f'Source changed during freeze: {source}; discard this freeze')
            sources[label] = {'path': str(source), 'sha256': before}
        rows = (out / 'sources/tests/seeds.tsv').read_text().splitlines()
        matches = [line.split('\t') for line in rows[1:] if int(line.split('\t')[0]) == a.index]
        if len(matches) != 1:
            raise SystemExit('Unknown seed index')
        manifest = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                    'command': sys.argv, 'index': a.index, 'seed': int(matches[0][1]),
                    'source_snapshots': sources, 'platform': platform.platform(),
                    'pid': os.getpid(), 'priority': os.getpriority(os.PRIO_PROCESS, 0),
                    'execution': 'Owls sequential persistent runner (AMENDMENT 1)',
                    'environment': {k: os.environ.get(k) for k in ['LOADEDMODULES', 'CC', 'CXX', 'CXX17',
                        'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'R_LIBS_USER']}}
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        with (out / 'environment.txt').open('w') as log:
            for cmd in [['uname', '-a'], ['R', '--version'], ['g++', '--version'], ['lscpu']]:
                log.write('$ ' + ' '.join(cmd) + '\n'); log.flush()
                subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)
    else:
        manifest = json.loads((out / 'manifest.json').read_text())
        checks = {}
        for label, src in manifest['source_snapshots'].items():
            checks[label] = {'original_unchanged': inventory(src['path']) == src['sha256'],
                             'snapshot_unchanged': inventory(out / 'sources' / label) == src['sha256']}
        (out / 'source_validation.json').write_text(json.dumps(checks, indent=2) + '\n')
        sums = inventory(out)
        # Do not checksum the inventory file itself or a changing terminal log.
        sums.pop('output_sha256.json', None)
        (out / 'output_sha256.json').write_text(json.dumps(sums, indent=2) + '\n')
        if not all(all(v.values()) for v in checks.values()):
            raise SystemExit('Source preservation check failed; inspect source_validation.json')


if __name__ == '__main__':
    main()
