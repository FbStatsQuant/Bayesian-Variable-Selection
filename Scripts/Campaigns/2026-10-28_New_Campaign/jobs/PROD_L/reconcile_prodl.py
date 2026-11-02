#!/usr/bin/env python3
"""Reconcile PROD-L results and the atomic per-unit ledger (Python 3.9)."""
import argparse
import collections
import csv
import hashlib
import re
import sys
from pathlib import Path
# the shared validator lives beside this file; add that folder explicitly so the tool also works under `python3 -I` (isolated mode drops it)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prodl_verify import verify, digest  # noqa: E402

PIECES = ('enum20', 'enum30', 'smc', 'smcrep')
OUTCOMES = ('done', 'deferred', 'unit_failed', 'killed_timeout', 'killed_external', 'not_run')

def scan_table(path, piece):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if not reader.fieldnames or reader.fieldnames == ['""']:
            return []
        if not {'case_id', 'repeat_m', 'base', 'primary_v3_status', 'retry_state', 'eligible'} <= set(reader.fieldnames):
            raise ValueError('invalid scan header: ' + str(path))
        rows = list(reader)
    seen = set()
    for r in rows:
        key = r['case_id'] + (('_rep' + r['repeat_m']) if piece == 'smcrep' else '')
        base = 'SMCBVS_rep' + r['repeat_m'] if piece == 'smcrep' else 'SMCBVS'
        if key in seen or r['base'] != base or (piece == 'smc' and r['repeat_m'] != '0'):
            raise ValueError('invalid or duplicate scan row: ' + key)
        seen.add(key)
    return rows

def scan_phases(run_home, logs):
    jobs = {}
    path = run_home / 'JOBIDS.tsv'
    if path.exists():
        with path.open(newline='', encoding='utf-8') as f:
            for r in csv.reader(f, delimiter='\t'):
                if len(r) >= 3 and r[0].startswith('p5scan_') and r[1] == 's5_p5scan' and r[2].isdigit():
                    jobs[r[0][7:]] = int(r[2])
    return sorted((job, phase) for phase, job in jobs.items() if (logs / 'p5' / ('scan_' + phase + '.ok')).is_file())

def statuses(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {'status', 'v3_status'} <= set(reader.fieldnames):
            raise ValueError('CSV missing status or v3_status')
        rows = list(reader)
        if not rows:
            raise ValueError('CSV has no rows')
        return {k: sorted({r.get(k, '') or 'NA' for r in rows}) for k in ('v3_status', 'status')}

def ledger(folder):
    records = list(folder.glob('*.start')) if folder.is_dir() else []
    if records:
        # start_utc is authoritative; mtime and name break ties or handle legacy records.
        def key(p):
            try:
                fields = dict(x.split('=', 1) for x in p.read_text(encoding='utf-8').split() if '=' in x)
                return (fields.get('start_utc', ''), p.stat().st_mtime_ns, p.name)
            except OSError:
                return ('', 0, p.name)
        start = max(records, key=key)
        end = start.with_suffix('.end')
        if not end.exists():
            return 'killed_external', 'attempt=' + start.stem
        fields = end.read_text(encoding='utf-8').split()
        pairs = dict(x.split('=', 1) for x in fields if '=' in x)
        # The positional fallback supports historical ledger fixtures.
        outcome = pairs.get('outcome', fields[2] if len(fields) > 2 else '')
        if outcome in ('unit_failed', 'killed_timeout'):
            return outcome, 'attempt=' + start.stem
        return 'not_run', 'attempt=' + start.stem + '; end=' + (outcome or 'invalid') + ' without verified result'
    if folder.is_dir() and any(folder.glob('*.deferred')):
        return 'deferred', 'deadline'
    return 'not_run', 'no started attempt'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stamp')
    ap.add_argument('--home-root', type=Path, default=Path('/home/fb31/projects/BVS/New_Campaign'))
    ap.add_argument('--scr-root', type=Path, default=Path('/scratch/fb31/New_Campaign'))
    ap.add_argument('--results-root', type=Path)
    ap.add_argument('--logs-root', type=Path)
    ap.add_argument('--lists', type=Path, default=Path(__file__).resolve().parent / 'lists/units.tsv')
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    if not re.fullmatch(r'\d{8}T\d{4}Z', a.stamp):
        ap.error('STAMP must be YYYYMMDDTHHMMZ')
    roots_given = any(x in sys.argv for x in ('--home-root', '--scr-root', '--results-root', '--logs-root'))
    results = a.results_root or a.scr_root / 'results'
    logs = (a.logs_root or a.scr_root / 'logs') / (a.stamp + '_lowp_prodL')
    # never write into whatever the current directory happens to be: with explicit roots (a downloaded tree) --out is required
    if roots_given and a.out is None and (a.results_root or a.logs_root):
        ap.error('--out is required with --results-root/--logs-root')
    out = a.out or (a.home_root / 'runs' / (a.stamp + '_lowp_prodL') / 'inventory_final')
    try:
        with a.lists.open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter='\t')
            if not reader.fieldnames or not {'piece', 'task', 'unit', 'dataset', 'scale', 'repeat'} <= set(reader.fieldnames):
                raise ValueError('invalid units.tsv header')
            units = list(reader)
        if not units:
            raise ValueError('empty unit list')
        seen = set()
        for u in units:
            piece, unit, dataset = u['piece'], u['unit'], u['dataset']
            if piece not in PIECES or not re.fullmatch(r'p00(?:20|30)_S[1-6]_r\d{3}', dataset):
                raise ValueError('invalid piece or dataset: ' + str(u))
            expected = dataset if piece.startswith('enum') else dataset + '_' + u['scale'] + (('_rep' + u['repeat']) if piece == 'smcrep' else '')
            if unit != expected or (piece, unit) in seen or (piece == 'enum20' and not dataset.startswith('p0020')) or (piece == 'enum30' and not dataset.startswith('p0030')) or (not piece.startswith('enum') and (u['scale'] not in ('c100', 'c050') or (piece == 'smcrep' and u['repeat'] not in ('1','2','3','4','5')))):
                raise ValueError('invalid or duplicate unit: ' + str(u))
            seen.add((piece, unit))
        out.mkdir(parents=True, exist_ok=True)
        inv = out / 'inventory'
        inv.mkdir(exist_ok=True)
        counts, native, exceptions, expected_dirs = collections.Counter(), collections.Counter(), [], collections.defaultdict(set)
        def exception(piece, kind, item, detail):
            exceptions.append((piece, kind, str(item), str(detail)))
        rows = collections.defaultdict(list)
        p5_expected_path = a.home_root / 'runs' / (a.stamp + '_lowp_prodL') / 'p5' / 'expected.tsv'
        p5_expected = None
        if p5_expected_path.exists():
            with p5_expected_path.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                if reader.fieldnames != ['piece', 'task', 'unit', 'dataset', 'scale', 'repeat', 'base_piece']:
                    raise ValueError('invalid P5 expected header')
                p5_expected = list(reader)
        closed = set()
        manifests = a.home_root / 'runs' / (a.stamp + '_lowp_prodL') / 'manifests'
        for piece in PIECES:
            marker = manifests / (piece + '.CLOSED')
            if marker.exists():
                m = re.search(r'\binventory_sha256=([0-9a-f]{64})\b', marker.read_text(encoding='utf-8'))
                saved = manifests / (piece + '.inventory.tsv')
                if not m or digest(saved) != m.group(1):
                    raise ValueError('closed inventory hash mismatch: ' + piece)
                with saved.open(newline='', encoding='utf-8') as f:
                    saved_rows = list(csv.reader(f, delimiter='\t'))
                if not saved_rows or saved_rows[0] != ['piece', 'unit', 'outcome', 'detail']:
                    raise ValueError('invalid closed inventory: ' + piece)
                expected = {u['unit'] for u in units if u['piece'] == piece}
                if len(saved_rows)-1 != len(expected) or {r[1] for r in saved_rows[1:] if len(r) == 4 and r[0] == piece} != expected:
                    raise ValueError('closed inventory does not match units: ' + piece)
                rows[piece] = [tuple(r) for r in saved_rows[1:]]
                for r in rows[piece]:
                    counts[(piece, r[2])] += 1
                    if piece in ('smc', 'smcrep') and r[2] == 'done':
                        mstatus = re.search(r'(?:^|; )v3_status=([^;]+)', r[3])
                        if not mstatus: raise ValueError('missing closed native status: ' + r[1])
                        native[(piece, mstatus.group(1))] += 1
                em = re.search(r'\bexceptions_sha256=([0-9a-f]{64})\b', marker.read_text(encoding='utf-8'))
                saved_ex = manifests / (piece + '.exceptions.tsv')
                if not em or digest(saved_ex) != em.group(1): raise ValueError('closed exceptions hash mismatch: ' + piece)
                with saved_ex.open(newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter='\t')
                    if reader.fieldnames != ['piece', 'kind', 'item', 'detail']: raise ValueError('invalid closed exceptions: ' + piece)
                    for e in reader:
                        if e['piece'] != piece or None in e or any(v is None for v in e.values()): raise ValueError('invalid closed exception row: ' + piece)
                        exception(piece, e['kind'], e['item'], e['detail'] + '; acknowledged=yes')
                closed.add(piece)
        for u in units:
            piece, unit, dataset = u['piece'], u['unit'], u['dataset']
            if piece in closed: continue
            case = dataset if piece.startswith('enum') else dataset + '_' + u['scale']
            folder = results / (a.stamp + '_lowp_' + piece) / dataset[:5] / case
            expected_dirs[piece].add(folder)
            prefix = 'EXACT' if piece.startswith('enum') else 'SMCBVS' + (('_rep' + u['repeat']) if piece == 'smcrep' else '')
            valid, why = verify(folder, prefix)
            detail = []
            if p5_expected is None and piece in ('smc', 'smcrep'):
                detail.append('p5_scan_pending')
            if valid:
                outcome = 'done'
                if not piece.startswith('enum'):
                    try:
                        st = statuses(folder / (prefix + '.csv'))
                        detail += [k + '=' + ','.join(st[k]) for k in ('v3_status', 'status')]
                        native[(piece, ','.join(st['v3_status']))] += 1
                    except (OSError, UnicodeError, ValueError, csv.Error) as e:
                        detail.append('CSV exception=' + str(e))
                        exception(piece, 'malformed_record', unit, 'CSV ' + str(e))
            else:
                outcome, note = ledger(logs / 'ledger' / piece / unit)
                detail.append(note)
                if folder.exists():
                    detail.append('result=' + why)
                    exception(piece, 'malformed_record', unit, why)
            retry = folder / 'P5_retry' / (prefix + '_p5retry')
            if any(retry.parent.glob(retry.name + '.*')) if retry.parent.is_dir() else False:
                retry_ok, retry_why = verify(retry.parent, retry.name)
                detail.append('P5_retry=' + ('verified' if retry_ok else retry_why))
                if retry_ok:
                    try:
                        st = statuses(retry.with_suffix('.csv'))
                        detail.extend('p5_' + k + '=' + ','.join(st[k]) for k in ('v3_status', 'status'))
                    except (OSError, UnicodeError, ValueError, csv.Error) as e:
                        exception(piece, 'malformed_record', unit, 'P5 CSV ' + str(e))
                else:
                    exception(piece, 'malformed_record', unit, 'P5 ' + retry_why)
            rows[piece].append((piece, unit, outcome, '; '.join(detail)))
            counts[(piece, outcome)] += 1
        if p5_expected is not None:
            known = {(u['piece'], u['unit']): u for u in units}
            seen_p5 = set()
            closed_p5 = {}
            for u in p5_expected:
                piece, unit = u['base_piece'], u['unit']
                original = known.get((piece, unit))
                if piece not in ('smc', 'smcrep') or u['piece'] != 'p5' or not original or (piece, unit) in seen_p5 or any(u[k] != original[k] for k in ('dataset', 'scale', 'repeat')):
                    raise ValueError('invalid P5 expected unit: ' + unit)
                seen_p5.add((piece, unit))
                if piece in closed:
                    if piece not in closed_p5:
                        saved_p5 = manifests / (piece + '.p5.tsv')
                        marker_text = (manifests / (piece + '.CLOSED')).read_text(encoding='utf-8')
                        m = re.search(r'\bp5_inventory_sha256=([0-9a-f]{64})\b', marker_text)
                        if not m or digest(saved_p5) != m.group(1):
                            raise ValueError('closed P5 inventory hash mismatch: ' + piece)
                        with saved_p5.open(newline='', encoding='utf-8') as f:
                            saved_rows = list(csv.DictReader(f, delimiter='\t'))
                        indexed = {r['unit']: r for r in saved_rows}
                        if len(indexed) != len(saved_rows):
                            raise ValueError('duplicate closed P5 unit: ' + piece)
                        closed_p5[piece] = indexed
                    r = closed_p5[piece].get(unit)
                    if r is None: raise ValueError('missing closed P5 unit: ' + unit)
                    rows['p5'].append(('p5', unit, r['outcome'], r['detail'])); continue
                case = u['dataset'] + '_' + u['scale']
                folder = results / (a.stamp + '_lowp_' + piece) / u['dataset'][:5] / case / 'P5_retry'
                prefix = 'SMCBVS' + (('_rep' + u['repeat']) if piece == 'smcrep' else '') + '_p5retry'
                ok, why = verify(folder, prefix)
                if ok: outcome, detail = 'done', 'verified'
                else:
                    # the ledger says HOW the attempt ended (killed_external: start without end; unit_failed / killed_timeout from .end);
                    # an attempt record whose ledger shows no started-and-ended failure is a consumed attempt without a valid retry
                    outcome, detail = ledger(logs / 'ledger' / 'p5' / unit)
                    # P5 vocabulary (R1 fix plan F2.4): a consumed attempt without a valid retry is attempt_failed (the ledger's own outcome
                    # is kept in the detail), except a start without an end, which stays killed_external
                    if (logs / 'p5_attempts' / unit).exists() and outcome != 'killed_external':
                        outcome, detail = 'attempt_failed', 'ledger=' + outcome + '; ' + why
                rows['p5'].append(('p5', unit, outcome, detail))
            with (inv / 'p5.tsv').open('w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter='\t', lineterminator='\n')
                writer.writerow(('piece', 'unit', 'outcome', 'detail')); writer.writerows(rows['p5'])
        unexpected = []
        for piece in PIECES:
            root = results / (a.stamp + '_lowp_' + piece)
            if root.is_dir() and piece not in closed:
                expected_parents = {folder.parent for folder in expected_dirs[piece]}
                for pdir in sorted(root.iterdir()):
                    if pdir.is_dir():
                        if pdir not in expected_parents:
                            unexpected.append(str(pdir)); exception(piece, 'unexpected_output', pdir, 'unexpected result folder')
                            continue
                        for folder in sorted(pdir.iterdir()):
                            if folder.is_dir() and folder not in expected_dirs[piece]:
                                unexpected.append(str(folder)); exception(piece, 'unexpected_output', folder, 'unexpected result folder')
            with (inv / (piece + '.tsv')).open('w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter='\t', lineterminator='\n')
                writer.writerow(('piece', 'unit', 'outcome', 'detail'))
                writer.writerows(rows[piece])
        run_home = a.home_root / 'runs' / (a.stamp + '_lowp_prodL')
        phases = scan_phases(run_home, logs)
        phase = phases[-1][1] if phases else None
        listed = {(r['base_piece'], r['unit']) for r in (p5_expected or [])}
        if phase:
            for piece in ('smc', 'smcrep'):
                if piece in closed: continue
                for r in scan_table(logs / 'p5' / ('scan_' + phase + '_' + piece + '.tsv'), piece):
                    unit = r['case_id'] + (('_rep' + r['repeat_m']) if piece == 'smcrep' else '')
                    if r['primary_v3_status'] == 'resource_limit':
                        if (piece, unit) not in listed: exception(piece, 'p5_unlisted_eligible', unit, 'scan=' + phase)
                        if r['retry_state'] in ('locked', 'incomplete', 'invalid_inspect'): exception(piece, 'p5_unsafe_state', unit, 'scan=' + phase + '; retry_state=' + r['retry_state'])
        complete = p5_expected is not None and all(r[2] == 'done' for rs in rows.values() for r in rs)
        unack = [e for e in exceptions if e[0] not in closed]
        status = ('INCOMPLETE OR UNRESOLVED' if not complete or unack else
                  ('COMPLETE WITH %d HQ-ACKNOWLEDGED EXCEPTIONS' % len(exceptions) if exceptions else 'CLEAN'))
        with (out / 'exceptions.tsv').open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(('piece', 'kind', 'item', 'detail')); writer.writerows(exceptions)
        with (out / 'INVENTORY.md').open('w', encoding='utf-8', newline='\n') as f:
            f.write('# PROD-L inventory: ' + a.stamp + '\n\n| Piece | ' + ' | '.join(OUTCOMES) + ' |\n|---|' + '---:|' * len(OUTCOMES) + '\n')
            for p in PIECES:
                f.write('| ' + p + ' | ' + ' | '.join(str(counts[(p, o)]) for o in OUTCOMES) + ' |\n')
            f.write('\nClosed pieces: ' + (', '.join(sorted(closed)) or 'none') + '.\n')
            f.write('\nSTATUS: ' + status + '\n')
            f.write('\nP5 check scan phase: ' + (phase or 'none') + '.\n')
            f.write('\n## P5\n\n' + ('PENDING: initial scan inventory missing.\n' if p5_expected is None else 'Expected: %d; done: %d.\n' % (len(p5_expected), sum(r[2] == 'done' for r in rows['p5']))))
            f.write('\n## SMC native status counts (units)\n\n| Piece | v3_status | Units |\n|---|---|---:|\n')
            for (p, native_status), n in sorted(native.items()):
                f.write('| ' + p + ' | ' + native_status.replace('|', '\\|') + ' | ' + str(n) + ' |\n')
            for title, values in [('Unexpected result folders', unexpected), ('Exceptions', [' / '.join(e) for e in exceptions])]:
                f.write('\n## ' + title + '\n\n')
                f.write(''.join('- `' + v.replace('`', "'") + '`\n' for v in values) if values else 'None.\n')
        return 1 if status == 'INCOMPLETE OR UNRESOLVED' else (4 if exceptions else 0)
    except (OSError, UnicodeError, ValueError, KeyError, csv.Error) as e:
        print('reconcile_prodl: ' + str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
