#!/usr/bin/env python3
"""Reconcile the PROD-L benchmark wave: 2,400 cases x 8 methods, ledgers of bench + benchretry, exceptions, CLOSED (Python 3.9 stdlib).

Derived from PROD_L's reconcile_prodl.py (REUSE.md): same outcomes, exceptions.tsv, STATUS line and exits
0 CLEAN / 4 COMPLETE WITH n HQ-ACKNOWLEDGED EXCEPTIONS / 1 INCOMPLETE OR UNRESOLVED / 2 input error or tampering. No P5, no truth.
A case is done only when all 8 method units are valid (bench_verify.verify_case). A committed failed rule is a scientific outcome:
the case stays done and the rule is counted in the rule-status table (per method: ok / warning / failed rule rows)."""
import argparse
import collections
import csv
import hashlib
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # works under `python3 -I`
from bench_verify import METHODS, verify_case  # noqa: E402

PIECE = 'bench'
OUTCOMES = ('done', 'deferred', 'unit_failed', 'killed_timeout', 'killed_external', 'not_run')
RULE_STATUSES = ('ok', 'warning', 'failed')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def ledger(logs, unit):
    """Outcome of the latest started attempt over both pieces; else deferred / not_run."""
    starts = []
    for piece in ('bench', 'benchretry'):
        d = logs / 'ledger' / piece / unit
        if d.is_dir():
            starts += list(d.glob('*.start'))
    if starts:
        def key(p):
            try:
                kv = dict(x.split('=', 1) for x in p.read_text(encoding='utf-8').split() if '=' in x)
                return (kv.get('start_utc', ''), p.stat().st_mtime_ns, str(p))
            except OSError:
                return ('', 0, str(p))
        start = max(starts, key=key)
        end = start.with_suffix('.end')
        piece = start.parent.parent.name
        if not end.exists():
            return 'killed_external', 'piece=%s; attempt=%s; attempts=%d' % (piece, start.stem, len(starts))
        kv = dict(x.split('=', 1) for x in end.read_text(encoding='utf-8').split() if '=' in x)
        outcome = kv.get('outcome', '')
        if outcome in ('unit_failed', 'killed_timeout'):
            return outcome, 'piece=%s; attempt=%s; attempts=%d' % (piece, start.stem, len(starts))
        return 'not_run', 'piece=%s; attempt=%s; end=%s without a valid case' % (piece, start.stem, outcome or 'invalid')
    for piece in ('bench', 'benchretry'):
        d = logs / 'ledger' / piece / unit
        if d.is_dir() and any(d.glob('*.deferred')):
            return 'deferred', 'deadline'
    return 'not_run', 'no started attempt'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stamp')
    ap.add_argument('--home-root', type=Path, default=Path('/home/fb31/projects/BVS/New_Campaign'))
    ap.add_argument('--scr-root', type=Path, default=Path('/scratch/fb31/New_Campaign'))
    ap.add_argument('--results-root', type=Path, help='folder holding <STAMP>_lowp_benchres (e.g. a downloaded results folder)')
    ap.add_argument('--logs-root', type=Path, help='folder holding <STAMP>_lowp_bench (logs)')
    ap.add_argument('--lists', type=Path, default=Path(__file__).resolve().parent / 'lists/units.tsv')
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    if not re.fullmatch(r'\d{8}T\d{4}Z', a.stamp):
        ap.error('STAMP must be YYYYMMDDTHHMMZ')
    rid = a.stamp + '_lowp_bench'
    results = (a.results_root or a.scr_root / 'results') / (a.stamp + '_lowp_benchres')
    logs = (a.logs_root or a.scr_root / 'logs') / rid
    if (a.results_root or a.logs_root) and a.out is None:
        ap.error('--out is required with --results-root/--logs-root')
    run_home = a.home_root / 'runs' / rid
    out = a.out or (run_home / 'inventory_final')
    try:
        with a.lists.open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter='\t')
            if not reader.fieldnames or not {'piece', 'task', 'unit', 'dataset', 'scale', 'repeat'} <= set(reader.fieldnames):
                raise ValueError('invalid units.tsv header')
            units = [u for u in reader]
        if not units or any(u['piece'] != PIECE for u in units):
            raise ValueError('units.tsv must list bench units only')
        seen = set()
        for u in units:
            if not re.fullmatch(r'p00(?:20|30)_S[1-6]_r\d{3}', u['dataset']) or u['scale'] not in ('c100', 'c050') or \
               u['unit'] != u['dataset'] + '_' + u['scale'] or u['unit'] in seen:
                raise ValueError('invalid or duplicate unit: ' + str(u))
            seen.add(u['unit'])
        out.mkdir(parents=True, exist_ok=True)
        (out / 'inventory').mkdir(exist_ok=True)
        counts, rules, exceptions, rows = collections.Counter(), collections.Counter(), [], []

        def exception(kind, item, detail):
            exceptions.append((PIECE, kind, str(item), str(detail)))
        manifests = run_home / 'manifests'
        marker = manifests / (PIECE + '.CLOSED')
        closed = marker.exists()
        if closed:
            text = marker.read_text(encoding='utf-8')
            m = re.search(r'\binventory_sha256=([0-9a-f]{64})\b', text)
            saved = manifests / (PIECE + '.inventory.tsv')
            if not m or digest(saved) != m.group(1):
                raise ValueError('closed inventory hash mismatch')
            with saved.open(newline='', encoding='utf-8') as f:
                saved_rows = list(csv.reader(f, delimiter='\t'))
            if not saved_rows or saved_rows[0] != ['piece', 'unit', 'outcome', 'detail'] or \
               len(saved_rows) - 1 != len(units) or {r[1] for r in saved_rows[1:] if len(r) == 4} != seen:
                raise ValueError('closed inventory does not match units')
            for r in saved_rows[1:]:
                rows.append(tuple(r)); counts[r[2]] += 1
                if r[2] == 'done':
                    mr = re.search(r'(?:^|; )rules=([^;]*)', r[3])
                    if not mr:
                        raise ValueError('missing closed rule statuses: ' + r[1])
                    for tok in filter(None, mr.group(1).split(',')):
                        mm = re.fullmatch(r'((?:F[1-5]|A[1-3])):(ok|warning|failed)=(\d+)', tok)
                        if not mm:
                            raise ValueError('invalid closed rule token: ' + tok)
                        rules[(mm.group(1), mm.group(2))] += int(mm.group(3))
            em = re.search(r'\bexceptions_sha256=([0-9a-f]{64})\b', text)
            saved_ex = manifests / (PIECE + '.exceptions.tsv')
            if not em or digest(saved_ex) != em.group(1):
                raise ValueError('closed exceptions hash mismatch')
            with saved_ex.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                if reader.fieldnames != ['piece', 'kind', 'item', 'detail']:
                    raise ValueError('invalid closed exceptions')
                for e in reader:
                    if e['piece'] != PIECE or None in e or any(v is None for v in e.values()):
                        raise ValueError('invalid closed exception row')
                    exception(e['kind'], e['item'], e['detail'] + '; acknowledged=yes')
        else:
            expected_dirs = set()
            for u in units:
                folder = results / u['dataset'][:5] / u['unit']
                expected_dirs.add(folder)
                ok, per = verify_case(folder, u['unit']) if folder.is_dir() else (False, None)
                if ok:
                    c = collections.Counter()
                    for mid in METHODS:
                        for r in per[mid][2]:
                            c[(mid, r['status'])] += 1
                    rules.update(c)
                    tokens = ','.join('%s:%s=%d' % (mid, st, c[(mid, st)]) for mid in METHODS for st in RULE_STATUSES if c[(mid, st)])
                    outcome, detail = 'done', 'rules=' + tokens
                else:
                    outcome, detail = ledger(logs, u['unit'])
                    if per is not None:
                        bad = ['%s:%s' % (mid, per[mid][1]) for mid in METHODS if not per[mid][0]]
                        good = [mid for mid in METHODS if per[mid][0]]
                        detail += '; invalid=' + ','.join(bad)
                        # some methods valid and others missing/invalid: an operational partial case (resubmission completes it); a
                        # method unit that EXISTS but is malformed is a malformed record
                        for mid in METHODS:
                            if not per[mid][0] and per[mid][1] != 'missing or empty file':
                                exception('malformed_record', u['unit'] + '/' + mid, per[mid][1])
                        if good and outcome not in ('killed_external', 'killed_timeout', 'unit_failed', 'deferred'):
                            exception('partial_case', u['unit'], 'valid=' + ','.join(good))
                rows.append((PIECE, u['unit'], outcome, detail)); counts[outcome] += 1
            unexpected_parents = {f.parent for f in expected_dirs}
            if results.is_dir():
                for pdir in sorted(results.iterdir()):
                    if pdir.name == 'MANIFEST.sha256' and pdir.is_file():
                        continue   # written by make_manifests.sh at closing; revalidated there, not a result (tester MM31/MM33)
                    if pdir not in unexpected_parents:
                        exception('unexpected_output', pdir, 'unexpected entry in the results folder'); continue
                    for entry in sorted(pdir.iterdir()):
                        if entry not in expected_dirs:
                            exception('unexpected_output', entry, 'unexpected entry')
                            continue
                        for f in sorted(entry.iterdir()):
                            if not re.fullmatch(r'(F[1-5]|A[1-3])\.(rds|csv|sha256|done)', f.name):
                                exception('unexpected_output', f, 'unexpected file in a case folder')
        with (out / 'inventory' / (PIECE + '.tsv')).open('w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(('piece', 'unit', 'outcome', 'detail')); w.writerows(rows)
        with (out / 'exceptions.tsv').open('w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(('piece', 'kind', 'item', 'detail')); w.writerows(exceptions)
        complete = counts['done'] == len(units)
        unack = [e for e in exceptions if not e[3].endswith('acknowledged=yes')]
        status = ('INCOMPLETE OR UNRESOLVED' if not complete or unack else
                  ('COMPLETE WITH %d HQ-ACKNOWLEDGED EXCEPTIONS' % len(exceptions) if exceptions else 'CLEAN'))
        with (out / 'INVENTORY.md').open('w', encoding='utf-8', newline='\n') as f:
            f.write('# PROD-L benchmark inventory: ' + a.stamp + '\n\n| Piece | ' + ' | '.join(OUTCOMES) + ' |\n|---|' + '---:|' * len(OUTCOMES) + '\n')
            f.write('| bench | ' + ' | '.join(str(counts[o]) for o in OUTCOMES) + ' |\n')
            f.write('\nClosed: ' + ('yes' if closed else 'no') + '.\n\nSTATUS: ' + status + '\n')
            f.write('\n## Rule statuses per method (rule rows of done cases)\n\n| Method | ok | warning | failed |\n|---|---:|---:|---:|\n')
            for mid in METHODS:
                f.write('| %s | %d | %d | %d |\n' % (mid, rules[(mid, 'ok')], rules[(mid, 'warning')], rules[(mid, 'failed')]))
            f.write('\nD54.3: the ABESS exact size check is deferred and disclosed; it is not part of this reconciliation.\n')
            f.write('\n## Exceptions\n\n' + (''.join('- `' + ' / '.join(e).replace('`', "'") + '`\n' for e in exceptions) if exceptions else 'None.\n'))
        print('STATUS: ' + status)
        return 1 if status == 'INCOMPLETE OR UNRESOLVED' else (4 if exceptions else 0)
    except (OSError, UnicodeError, ValueError, KeyError, csv.Error) as e:
        print('reconcile_bench: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
