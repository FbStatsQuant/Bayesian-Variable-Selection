#!/usr/bin/env python3
"""test_reconcile.py -- strict case validation and exit codes of reconcile_bench.py (PROD_L_BENCH DESIGN.md sections 5-6).  py -3 test_reconcile.py [WORKDIR]

A case is DONE iff ALL 8 methods F1..F5, A1..A3 have a valid unit: <M>.sha256 exactly two lines '<64 hex>  <M>.rds' and '<64 hex>  <M>.csv' (basenames, no duplicates, no escaping),
both files non-empty and matching; <M>.done first line starts 'status '; the CSV parses with columns rule_id role status method_id case_id, >= 1 row, every status in {ok, warning, failed},
method_id == M, case_id == the case. A committed failed rule stays done. Anything else: not done (+ a malformed_record exception where the file is unreadable / ill-formed).
Exits 0 CLEAN, 1 INCOMPLETE OR UNRESOLVED (also any unexpected output folder), 2 tampering / input errors; <out>/exceptions.tsv header `piece kind item detail`.
The close / pull / acknowledged-exception flows use the real make_manifests.sh (test_manifests.sh).
"""
import hashlib
import os
import shutil
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.environ.get('PRODL_B_SRC') or os.path.dirname(HERE)
ROOT = 'C:/Users/felip/AppData/Local/Temp/prodl_tests'
WORK = ROOT + '/test_reconcile'
STAMP = '20261030T1500Z'
RID = STAMP + '_lowp_bench'
METHODS = ['F1', 'F2', 'F3', 'F4', 'F5', 'A1', 'A2', 'A3']
STATUS_COLS = ('outcome', 'status', 'state', 'class', 'result')


def case_id(i):
    return 'p0020_S1_r%03d_c100' % i


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


class Tree:
    def __init__(self, name, ncases):
        self.base = os.path.join(WORK, name).replace('\\', '/')
        shutil.rmtree(self.base, ignore_errors=True)
        self.home = self.base + '/home/New_Campaign'
        self.scr = self.base + '/scr/New_Campaign'
        self.runh = '%s/runs/%s' % (self.home, RID)
        self.bundle = self.runh + '/code/prod_l_bench'
        self.res = '%s/results/%s_lowp_benchres' % (self.scr, STAMP)
        self.logs = '%s/logs/%s' % (self.scr, RID)
        os.makedirs(self.res + '/p0020')
        os.makedirs(self.logs + '/ledger')
        os.makedirs(self.runh + '/manifests')
        shutil.copytree(B, self.bundle, ignore=shutil.ignore_patterns('tests', 'review', '__pycache__', 'BUILD_NOTES*.md', 'PROGRESS.md'))
        self.n = ncases
        with open(self.bundle + '/lists/units.tsv', 'w', newline='\n') as fh:
            fh.write('piece\ttask\tunit\tdataset\tscale\trepeat\n')
            for i in range(1, ncases + 1):
                fh.write('bench\t0\t%s\tp0020_S1_r%03d\tc100\t0\n' % (case_id(i), i))
        with open(self.runh + '/JOBIDS.tsv', 'w', newline='\n') as fh:
            fh.write('wave\tstep\tjobid\tarray\tdependency\nmain\ts1_bench\t7002\t0-0\t-\n')

    def cdir(self, i):
        return '%s/p0020/%s' % (self.res, case_id(i))

    def method(self, i, m, status='ok', cid=None, mid=None):
        d = self.cdir(i)
        os.makedirs(d, exist_ok=True)
        open(d + '/%s.rds' % m, 'w').write('rds %s %s' % (i, m))
        with open(d + '/%s.csv' % m, 'w', newline='\n') as fh:
            fh.write('rule_id,role,status,method_id,case_id\n')
            fh.write('r1,primary,%s,%s,%s\n' % (status, mid or m, cid or case_id(i)))
            fh.write('r2,sensitivity,ok,%s,%s\n' % (mid or m, cid or case_id(i)))
        self.seal(i, m)
        open(d + '/%s.done' % m, 'w', newline='\n').write('status %s,ok\nfinished_utc 2026-10-30T13:00:00Z\n' % status)

    def seal(self, i, m):
        d = self.cdir(i)
        with open(d + '/%s.sha256' % m, 'w', newline='\n') as fh:
            fh.write('%s  %s.rds\n%s  %s.csv\n' % (sha(d + '/%s.rds' % m), m, sha(d + '/%s.csv' % m), m))

    def full_case(self, i, status='ok'):
        for m in METHODS:
            self.method(i, m, status)

    def run(self):
        out = self.base + '/out'
        shutil.rmtree(out, ignore_errors=True)
        cmd = [sys.executable, '-I', self.bundle + '/reconcile_bench.py', STAMP, '--home-root', self.home, '--scr-root', self.scr,
               '--lists', self.bundle + '/lists/units.tsv', '--out', out]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        self.rc, self.out = p.returncode, p.stdout + p.stderr
        return self

    def outcomes(self):
        p = self.base + '/out/inventory/bench.tsv'
        if not os.path.isfile(p):
            raise AssertionError('inventory/bench.tsv was not written: ' + self.out[-400:])
        lines = [ln.rstrip('\r\n').split('\t') for ln in open(p, encoding='utf-8') if ln.strip()]
        head = [h.strip().lower() for h in lines[0]]
        ui = head.index('unit')
        oi = next(head.index(c) for c in STATUS_COLS if c in head)
        return {r[ui]: (r[oi], r) for r in lines[1:] if len(r) > max(ui, oi)}

    def exceptions(self):
        p = self.base + '/out/exceptions.tsv'
        if not os.path.isfile(p):
            return None
        return [ln.rstrip('\r\n').split('\t') for ln in open(p, encoding='utf-8') if ln.strip()]

    def status_text(self):
        for ln in open(self.base + '/out/INVENTORY.md', encoding='utf-8', errors='replace'):
            if 'STATUS' in ln.upper():
                return ln.strip()
        return ''


class TestStrict(unittest.TestCase):
    """Case 1..14: one defect each (on method A2 unless stated); 15 = valid with a committed failed rule; 16 = all valid."""

    @classmethod
    def setUpClass(cls):
        t = Tree('strict', 16)
        for i in range(1, 17):
            t.full_case(i)
        d = t.cdir(1)                                                   # 1 missing RDS, sidecar for another file
        os.remove(d + '/A2.rds')
        open(d + '/unrelated.bin', 'w').write('x')
        open(d + '/A2.sha256', 'w').write('%s  unrelated.bin\n%s  A2.csv\n' % (sha(d + '/unrelated.bin'), sha(d + '/A2.csv')))
        d = t.cdir(2)                                                   # 2 one-line sidecar
        open(d + '/A2.sha256', 'w').write('%s  A2.rds\n' % sha(d + '/A2.rds'))
        d = t.cdir(3)                                                   # 3 duplicate name
        open(d + '/A2.sha256', 'w').write('%s  A2.rds\n%s  A2.rds\n' % (sha(d + '/A2.rds'), sha(d + '/A2.rds')))
        d = t.cdir(4)                                                   # 4 a name escaping the folder
        open(d + '/../escape.rds', 'w').write('e')
        open(d + '/A2.sha256', 'w').write('%s  ../escape.rds\n%s  A2.csv\n' % (sha(d + '/../escape.rds'), sha(d + '/A2.csv')))
        open(t.cdir(5) + '/A2.done', 'w').write('garbage marker\n')     # 5 malformed .done
        d = t.cdir(6)                                                   # 6 CSV without method_id / case_id
        open(d + '/A2.csv', 'w').write('rule_id,role,status\nr1,primary,ok\n')
        t.seal(6, 'A2')
        d = t.cdir(7)                                                   # 7 a status outside {ok, warning, failed}
        open(d + '/A2.csv', 'w').write('rule_id,role,status,method_id,case_id\nr1,primary,bogus,A2,%s\n' % case_id(7))
        t.seal(7, 'A2')
        t.method(8, 'A2', mid='A1')                                     # 8 method_id mismatch
        t.method(9, 'A2', cid=case_id(1))                               # 9 case_id mismatch
        d = t.cdir(10)                                                  # 10 zero rows
        open(d + '/A2.csv', 'w').write('rule_id,role,status,method_id,case_id\n')
        t.seal(10, 'A2')
        d = t.cdir(11)                                                  # 11 empty RDS with a matching sidecar
        open(d + '/A2.rds', 'w').close()
        t.seal(11, 'A2')
        shutil.rmtree(t.cdir(12))                                       # 12 only 3 methods
        for m in METHODS[:3]:
            t.method(12, m)
        d = t.cdir(13)                                                  # 13 tampered RDS after the sidecar
        open(d + '/A2.rds', 'a').write('tampered')
        d = t.cdir(14)                                                  # 14 sidecar order swapped / extra third line
        open(d + '/A2.sha256', 'a').write('%s  A2.done\n' % sha(d + '/A2.done'))
        t.method(15, 'F4', status='failed')                             # 15 committed failed rule: valid
        t.run()
        cls.t = t
        cls.err = None
        try:
            cls.out = t.outcomes()
        except AssertionError as exc:
            cls.err = str(exc)

    def outcome(self, i):
        if self.err:
            self.fail(self.err)
        return self.out[case_id(i)][0]

    def test_SV01_defects_are_not_done(self):
        why = {1: 'missing RDS with a sidecar for another file', 2: 'one-line sidecar', 3: 'duplicate name', 4: 'name escaping the folder', 5: 'malformed .done',
               6: 'CSV without method_id/case_id', 7: 'status outside the set', 8: 'method_id mismatch', 9: 'case_id mismatch', 10: 'zero rows', 11: 'empty RDS',
               12: 'only 3 methods', 13: 'tampered RDS', 14: 'three-line sidecar'}
        for i, w in why.items():
            self.assertNotEqual(self.outcome(i), 'done', 'case %d (%s)' % (i, w))

    def test_SV02_valid_cases_are_done(self):
        self.assertEqual(self.outcome(15), 'done', 'a committed failed rule stays done')
        self.assertEqual(self.outcome(16), 'done')

    def test_SV03_exit_nonzero_and_status(self):
        self.assertEqual(self.t.rc, 1, self.t.out[-300:])
        self.assertIn('INCOMPLETE OR UNRESOLVED', self.t.status_text())

    def test_SV04_malformed_record_exceptions(self):
        rows = self.t.exceptions()
        self.assertIsNotNone(rows, 'exceptions.tsv is written')
        self.assertEqual(rows[0], ['piece', 'kind', 'item', 'detail'])
        kinds = {r[1] for r in rows[1:]}
        self.assertIn('malformed_record', kinds, 'unreadable / ill-formed method records are reported as malformed_record: %s' % sorted(kinds))

    def test_SV05_every_case_exactly_once(self):
        self.assertEqual(sorted(self.out), sorted(case_id(i) for i in range(1, 17)))


class TestExits(unittest.TestCase):
    def test_EX01_clean(self):
        t = Tree('clean', 3)
        for i in (1, 2, 3):
            t.full_case(i)
        t.run()
        self.assertEqual(t.rc, 0, t.out[-400:])
        self.assertIn('CLEAN', t.status_text())
        rows = t.exceptions()
        self.assertEqual(rows, [['piece', 'kind', 'item', 'detail']])
        self.assertEqual({v[0] for v in t.outcomes().values()}, {'done'})

    def test_EX02_unexpected_output_alone_makes_the_exit_nonzero(self):
        t = Tree('unexpected', 2)
        for i in (1, 2):
            t.full_case(i)
        t.run()
        self.assertEqual(t.rc, 0, 'control: ' + t.out[-300:])
        d = t.res + '/p0020/ZZ_unexpected_case'
        os.makedirs(d)
        open(d + '/F1.rds', 'w').write('x')
        t.run()
        self.assertEqual(t.rc, 1, 'all expected cases done + an unexpected output folder: exit 1. ' + t.out[-300:])
        rows = t.exceptions() or []
        self.assertTrue([r for r in rows[1:] if r[0] == 'bench' and r[1] == 'unexpected_output' and 'ZZ_unexpected_case' in r[2]], rows)
        self.assertIn('INCOMPLETE OR UNRESOLVED', t.status_text())

    def test_EX03_not_run_cases_are_listed_and_exit_nonzero(self):
        t = Tree('notrun', 3)
        t.full_case(1)
        t.run()
        self.assertNotEqual(t.rc, 0)
        out = t.outcomes()
        self.assertEqual(out[case_id(1)][0], 'done')
        self.assertEqual({out[case_id(2)][0], out[case_id(3)][0]}, {'not_run'})

    def test_EX04_failed_rules_are_counted_in_the_rule_status_table(self):
        t = Tree('failedrules', 2)
        t.full_case(1)
        t.full_case(2)
        t.method(1, 'F4', status='failed')
        t.method(2, 'F4', status='failed')
        t.method(2, 'A3', status='warning')
        t.run()
        self.assertEqual(t.rc, 0, t.out[-300:])
        md = open(t.base + '/out/INVENTORY.md', encoding='utf-8', errors='replace').read()
        rows = {}
        header = None
        for ln in md.splitlines():
            if ln.startswith('|'):
                cells = [c.strip() for c in ln.strip().strip('|').split('|')]
                if cells and cells[0].lower() == 'method':
                    header = [c.lower() for c in cells]
                elif header and cells[0] in METHODS:
                    rows[cells[0]] = dict(zip(header, cells))
        self.assertTrue(rows, 'a "Rule statuses per method" table (| Method | ok | warning | failed |)')
        self.assertEqual(int(rows['F4']['failed']), 2, rows.get('F4'))
        self.assertEqual(int(rows['A3']['warning']), 1, rows.get('A3'))

    def test_EX05_ledger_both_pieces_by_case(self):
        t = Tree('ledger', 3)
        d = t.logs + '/ledger/benchretry/' + case_id(1)
        os.makedirs(d)
        open(d + '/7010_0.start', 'w').write('unit=%s piece=benchretry task=0 job_tag=7010_0 host=h start_utc=2026-10-30T13:00:00Z deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' % case_id(1))
        d = t.logs + '/ledger/bench/' + case_id(2)
        os.makedirs(d)
        open(d + '/7002_0.deferred', 'w').write('unit=%s reason=deadline now_epoch=1 deadline_epoch=1 need_s=1 end_source=x end_epoch=1\n' % case_id(2))
        t.run()
        out = t.outcomes()
        self.assertEqual(out[case_id(1)][0], 'killed_external', 'a start without an end in the benchretry ledger')
        self.assertEqual(out[case_id(2)][0], 'deferred')
        self.assertEqual(out[case_id(3)][0], 'not_run')

    def test_EX06_inventory_rows_use_the_documented_header(self):
        t = Tree('header', 1)
        t.full_case(1)
        t.run()
        head = open(t.base + '/out/inventory/bench.tsv', encoding='utf-8').readline().rstrip('\r\n').split('\t')
        self.assertEqual(head[:4], ['piece', 'unit', 'outcome', 'detail'])


def load_workdir():
    global WORK
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if args:
        base = args[0].replace('\\', '/')
        if not base.startswith(ROOT + '/') or '..' in base:
            sys.stderr.write('REFUSED: work dir must be under %s\n' % ROOT)
            sys.exit(64)
        WORK = base
    sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]


if __name__ == '__main__':
    load_workdir()
    if not os.path.isfile(B + '/reconcile_bench.py'):
        print('FAIL reconcile_bench.py not found')
        print('test_reconcile: 0 passed, 1 failed')
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    failed = len(res.failures) + len(res.errors) + len(res.skipped)
    print('test_reconcile: %d passed, %d failed' % (res.testsRun - failed, failed))
    sys.exit(0 if failed == 0 else 1)
