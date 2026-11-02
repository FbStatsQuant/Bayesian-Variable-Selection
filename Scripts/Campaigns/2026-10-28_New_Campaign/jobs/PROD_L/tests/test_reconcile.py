#!/usr/bin/env python3
"""test_reconcile.py -- acceptance tests of reconcile_prodl.py (DESIGN.md section 8).  py -3 test_reconcile.py [WORKDIR]

The tool runs on a fabricated downloaded tree:  reconcile_prodl.py STAMP --results-root <dir holding <STAMP>_lowp_<piece>> --logs-root <dir holding <RID>>.
Expected units come from lists/units.tsv next to the script; the test copies the bundle (without tests/) and swaps in a small list, so every class can be
fabricated cheaply.  Classes: done (verified .done/.sha256), deferred, unit_failed, killed_timeout, killed_external (start without end), not_run;
any result folder outside the expected set is reported as unexpected; exit 0 only if every expected unit is done; inventory/<piece>.tsv + INVENTORY.md written.
The inventory tables are parsed by header (a column named 'unit' and a status-like column), since the exact column set is not fixed by the spec.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.environ.get('PRODL_B_SRC') or os.path.dirname(HERE)      # PRODL_B_SRC: alternative bundle folder (used to smoke-test the tests themselves)
ROOT = 'C:/Users/felip/AppData/Local/Temp/prodl_tests'
WORK = ROOT + '/test_reconcile'
STAMP = '20261030T1500Z'
RID = STAMP + '_lowp_prodL'
STATUS_COLS = ('status', 'state', 'outcome', 'class', 'classification', 'result', 'unit_status')
CLASSES = ('done', 'deferred', 'unit_failed', 'killed_timeout', 'killed_external', 'not_run')


def ds(i):
    return 'p0020_S1_r%03d' % i


SCAN_HDR = '\t'.join(['case_id', 'base', 'repeat_m', 'primary_v3_status', 'primary_status', 'primary_mem_gb', 'primary_hours', 'primary_stop_where', 'primary_stop_phase',
                      'primary_stop_checkpoint', 'primary_stop_tier', 'primary_stop_iter', 'primary_stop_stage', 'primary_stop_elapsed_s', 'primary_stop_allocation_s',
                      'retry_state', 'retry_problem', 'retry_artefacts', 'retry_v3_status', 'retry_status', 'retry_stop_where', 'retry_stop_phase', 'retry_stop_checkpoint',
                      'eligible', 'launchable'])


def p5_scan_files(logrid, runh, units):
    """a complete successful scan phase (initial): one row per smc / smcrep unit, nothing eligible, and the JOBIDS rows that date it
    (R2 I1: reconcile reads the newest successful scan phase, ranked by recorded job id)"""
    os.makedirs(logrid + '/p5', exist_ok=True)
    os.makedirs(runh, exist_ok=True)
    with open(logrid + '/p5/scan_initial_smc.tsv', 'w', newline='\n') as fh:
        fh.write(SCAN_HDR + '\n')
        for u in units:
            if u[0] == 'smc':
                fh.write(scan_row(u[3] + '_c100', 'SMCBVS', 0, 'completed', 'none') + '\n')
    with open(logrid + '/p5/scan_initial_smcrep.tsv', 'w', newline='\n') as fh:
        fh.write(SCAN_HDR + '\n')
        for u in units:
            if u[0] == 'smcrep':
                fh.write(scan_row(u[3] + '_c100', 'SMCBVS_rep%s' % u[5], u[5], 'completed', 'none') + '\n')
    open(logrid + '/p5/scan_initial.ok', 'w').write('ok\n')
    with open(runh + '/JOBIDS.tsv', 'w', newline='\n') as fh:
        fh.write('wave\tstep\tjobid\tarray\tdependency\nmain\ts2_smc\t7002\t0-0\t-\np5scan_initial\ts5_p5scan\t7003\t-\t-\n')


def scan_row(case_id, base, repeat_m, v3, state):
    el = 'TRUE' if (v3 == 'resource_limit' and state != 'done') else 'FALSE'
    la = 'TRUE' if (v3 == 'resource_limit' and state == 'none') else 'FALSE'
    return '\t'.join([case_id, base, str(repeat_m), v3, 'failed', '2', '4'] + ['NA'] * 8 + [state] + ['NA'] * 7 + [el, la])


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


class Tree:
    """A fabricated downloaded tree + a copy of the bundle with a small units.tsv."""

    def __init__(self, name, units, p5=True):
        self.base = os.path.join(WORK, name).replace('\\', '/')
        shutil.rmtree(self.base, ignore_errors=True)
        self.p5 = p5          # True: a home root whose p5/expected.tsv has only the header row (zero eligible: P5 complete-with-none)
        if p5:
            os.makedirs('%s/home/runs/%s/p5' % (self.base, RID))
            with open('%s/home/runs/%s/p5/expected.tsv' % (self.base, RID), 'w', newline='\n') as fh:
                fh.write('piece\ttask\tunit\tdataset\tscale\trepeat\tbase_piece\n')
            p5_scan_files('%s/logs/%s' % (self.base, RID), '%s/home/runs/%s' % (self.base, RID), units)
        self.bundle = self.base + '/bundle'
        self.res = self.base + '/results'
        self.logs = self.base + '/logs'
        os.makedirs(self.res, exist_ok=True)
        os.makedirs(self.logs + '/' + RID, exist_ok=True)
        shutil.copytree(B, self.bundle, ignore=shutil.ignore_patterns('tests', 'review', '__pycache__', 'PROGRESS.md'))
        self.units = units          # list of (piece, task, unit, dataset, scale, repeat)
        with open(self.bundle + '/lists/units.tsv', 'w', newline='\n') as fh:
            fh.write('piece\ttask\tunit\tdataset\tscale\trepeat\n')
            for u in units:
                fh.write('\t'.join(str(x) for x in u) + '\n')

    # --- results
    def case_dir(self, piece, unit, dataset):
        d = unit if piece != 'smcrep' else unit.rsplit('_rep', 1)[0]
        return '%s/%s_lowp_%s/p0020/%s' % (self.res, STAMP, piece, d)

    def prefix(self, piece, unit):
        return 'EXACT' if piece.startswith('enum') else ('SMCBVS' if piece == 'smc' else 'SMCBVS_rep' + unit.rsplit('_rep', 1)[1])

    def done(self, piece, unit, dataset, v3='complete'):
        d = self.case_dir(piece, unit, dataset)
        p = self.prefix(piece, unit)
        os.makedirs(d, exist_ok=True)
        files = [p + '.rds']
        open(d + '/' + p + '.rds', 'w').write('rds ' + unit)
        if piece != 'enum20' and piece != 'enum30':
            open(d + '/' + p + '.csv', 'w').write('rule_id,v3_status,status\nhpm,%s,ok\npip05,%s,ok\n' % (v3, v3))
            files.append(p + '.csv')
        with open(d + '/' + p + '.sha256', 'w', newline='\n') as fh:
            for f in files:
                fh.write('%s  %s\n' % (sha(d + '/' + f), f))
        if piece.startswith('enum'):     # the real EXACT.done: the RDS hash on the first line, then the time (F6)
            open(d + '/' + p + '.done', 'w', newline='\n').write('%s\n2026-10-30T13:00:00Z\n' % sha(d + '/' + p + '.rds'))
        else:
            open(d + '/' + p + '.done', 'w', newline='\n').write('status ok,ok\nfinished_utc 2026-10-30T13:00:00Z\n')

    def junk_folder(self, piece, name):
        d = '%s/%s_lowp_%s/p0020/%s' % (self.res, STAMP, piece, name)
        os.makedirs(d, exist_ok=True)
        open(d + '/EXACT.rds', 'w').write('x')
        return d

    # --- ledger
    def rec(self, kind, piece, unit, tag, outcome='ok', rc=0):
        d = '%s/%s/ledger/%s/%s' % (self.logs, RID, piece, unit)
        os.makedirs(d, exist_ok=True)
        # DESIGN section 12: single-space separated key=value pairs
        if kind == 'start':
            line = 'unit=%s piece=%s task=0 job_tag=%s host=host1 start_utc=2026-10-30T13:00:00Z deadline_epoch=1700000000 need_s=14880\n' % (unit, piece, tag)
        elif kind == 'end':
            line = 'unit=%s rc=%d outcome=%s wall_s=5.0 cli_status=NA cli_skipped=NA end_utc=2026-10-30T13:00:09Z\n' % (unit, rc, outcome)
        else:
            line = 'unit=%s reason=deadline now_epoch=1700000000 deadline_epoch=1700000100 need_s=14880\n' % unit
        with open('%s/%s.%s' % (d, tag, kind), 'w', newline='\n') as fh:
            fh.write(line)

    def run(self):
        # with --results-root/--logs-root the tool requires --out (tables go to <out>/inventory/<piece>.tsv, plus <out>/INVENTORY.md)
        cmd = [sys.executable, '-I', self.bundle + '/reconcile_prodl.py', STAMP, '--results-root', self.res, '--logs-root', self.logs,
               '--lists', self.bundle + '/lists/units.tsv', '--out', self.base + '/out']
        if self.p5:
            cmd += ['--home-root', self.base + '/home']
        shutil.rmtree(self.base + '/out', ignore_errors=True)
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        self.rc, self.out = p.returncode, p.stdout + p.stderr
        return self

    # --- outputs
    def find_outputs(self):
        tsv, md = {}, []
        for dp, dn, fn in os.walk(self.base):
            if os.path.abspath(dp).replace('\\', '/').startswith(self.bundle):
                continue
            for f in fn:
                full = os.path.join(dp, f).replace('\\', '/')
                if f.endswith('.tsv') and '/inventory/' in full and os.path.basename(os.path.dirname(full)) == 'inventory':
                    tsv[f[:-4]] = full
                if f == 'INVENTORY.md':
                    md.append(full)
        # the bundle folder itself may also receive outputs (RUN_HOME style)
        for dp, dn, fn in os.walk(self.bundle):
            for f in fn:
                full = os.path.join(dp, f).replace('\\', '/')
                if f == 'INVENTORY.md':
                    md.append(full)
                if f.endswith('.tsv') and os.path.basename(os.path.dirname(full)) == 'inventory':
                    tsv[f[:-4]] = full
        return tsv, md

    def table(self, piece):
        tsv, _ = self.find_outputs()
        path = tsv.get(piece)
        if not path:
            raise AssertionError('inventory/%s.tsv was not written (found: %s)' % (piece, sorted(tsv)))
        lines = [ln.rstrip('\r\n').split('\t') for ln in open(path, encoding='utf-8') if ln.strip()]
        head = [h.strip().lower() for h in lines[0]]
        if 'unit' not in head:
            raise AssertionError('no "unit" column in %s header %s' % (path, head))
        sc = next((head.index(c) for c in STATUS_COLS if c in head), None)
        if sc is None:
            raise AssertionError('no status column among %s in %s' % (STATUS_COLS, head))
        ui = head.index('unit')
        return [(r[ui], r[sc], '\t'.join(r)) for r in lines[1:] if len(r) > max(ui, sc)]


def U(piece, i, task=0, m=None):
    d = ds(i)
    if piece.startswith('enum'):
        return (piece, task, d, d, '-', 0)
    if piece == 'smc':
        return (piece, task, d + '_c100', d, 'c100', 0)
    return (piece, task, '%s_c100_rep%d' % (d, m), d, 'c100', m)


class TestReconcile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(WORK, exist_ok=True)
        units = [U('enum20', i) for i in range(1, 9)] + [U('smc', i) for i in range(1, 7)] + [U('smcrep', 1, m=1), U('smcrep', 2, m=1)]
        t = Tree('mixed', units)
        # enum20
        t.done('enum20', ds(1), ds(1)); t.rec('start', 'enum20', ds(1), '8100_0'); t.rec('end', 'enum20', ds(1), '8100_0')
        t.rec('deferred', 'enum20', ds(2), '8100_0')
        t.rec('start', 'enum20', ds(3), '8100_0'); t.rec('end', 'enum20', ds(3), '8100_0', 'unit_failed', 3)
        t.rec('start', 'enum20', ds(4), '8100_0'); t.rec('end', 'enum20', ds(4), '8100_0', 'killed_timeout', 124)
        t.rec('start', 'enum20', ds(5), '8100_0')
        # enum20 unit 6: nothing at all
        t.rec('start', 'enum20', ds(7), '8100_0'); t.rec('end', 'enum20', ds(7), '8100_0', 'unit_failed', 1)          # failed first ...
        t.rec('start', 'enum20', ds(7), '8200_0'); t.rec('end', 'enum20', ds(7), '8200_0'); t.done('enum20', ds(7), ds(7))   # ... done later
        t.done('enum20', ds(8), ds(8))                                                                                    # done, no ledger at all
        # smc
        t.done('smc', U('smc', 1)[2], ds(1), v3='resource_limit'); t.rec('start', 'smc', U('smc', 1)[2], '8300_0'); t.rec('end', 'smc', U('smc', 1)[2], '8300_0')
        t.done('smc', U('smc', 2)[2], ds(2)); t.rec('start', 'smc', U('smc', 2)[2], '8300_0'); t.rec('end', 'smc', U('smc', 2)[2], '8300_0')
        t.rec('deferred', 'smc', U('smc', 3)[2], '8300_0')
        t.rec('start', 'smc', U('smc', 4)[2], '8300_1')
        # smc 5: nothing ; smc 6: a .done whose sidecar does not verify -> not done
        t.done('smc', U('smc', 6)[2], ds(6)); open(t.case_dir('smc', U('smc', 6)[2], ds(6)) + '/SMCBVS.rds', 'a').write('tampered')
        t.rec('start', 'smc', U('smc', 6)[2], '8300_2'); t.rec('end', 'smc', U('smc', 6)[2], '8300_2', 'unit_failed', 1)
        # smcrep
        t.done('smcrep', U('smcrep', 1, m=1)[2], ds(1)); t.rec('start', 'smcrep', U('smcrep', 1, m=1)[2], '8400_0'); t.rec('end', 'smcrep', U('smcrep', 1, m=1)[2], '8400_0')
        # (smcrep 2: nothing)
        cls.junk = t.junk_folder('enum20', 'ZZ_unexpected_unit')
        t.run()
        cls.t = t
        cls.tables = {}
        cls.err = None
        try:
            for p in ('enum20', 'smc', 'smcrep'):
                cls.tables[p] = t.table(p)
        except AssertionError as exc:
            cls.err = str(exc)

    def tab(self, piece):
        if self.err:
            self.fail(self.err)
        return {u: s for u, s, _ in self.tables[piece]}

    def test_RC01_exit_nonzero_when_not_everything_is_done(self):
        self.assertNotEqual(self.t.rc, 0, self.t.out[-500:])

    def test_RC02_inventory_files_written(self):
        tsv, md = self.t.find_outputs()
        self.assertTrue({'enum20', 'smc', 'smcrep'} <= set(tsv), 'inventory/<piece>.tsv written for each piece: %s' % sorted(tsv))
        self.assertTrue(md, 'INVENTORY.md written')

    def test_RC03_every_expected_unit_exactly_once(self):
        if self.err:
            self.fail(self.err)
        for piece in ('enum20', 'smc', 'smcrep'):
            want = sorted(u[2] for u in self.t.units if u[0] == piece)
            rows = [u for u, s, _ in self.tables[piece] if u in want]
            self.assertEqual(sorted(rows), want, '%s: every expected unit exactly once' % piece)

    def test_RC10_enum_classes(self):
        s = self.tab('enum20')
        self.assertEqual(s[ds(1)], 'done')
        self.assertEqual(s[ds(2)], 'deferred')
        self.assertEqual(s[ds(3)], 'unit_failed')
        self.assertEqual(s[ds(4)], 'killed_timeout')
        self.assertEqual(s[ds(5)], 'killed_external')
        self.assertEqual(s[ds(6)], 'not_run')

    def test_RC11_done_beats_an_earlier_failure(self):
        self.assertEqual(self.tab('enum20')[ds(7)], 'done')

    def test_RC12_done_without_any_ledger_record_is_done(self):
        self.assertEqual(self.tab('enum20')[ds(8)], 'done')

    def test_RC20_smc_classes(self):
        s = self.tab('smc')
        self.assertEqual(s[U('smc', 1)[2]], 'done')
        self.assertEqual(s[U('smc', 2)[2]], 'done')
        self.assertEqual(s[U('smc', 3)[2]], 'deferred')
        self.assertEqual(s[U('smc', 4)[2]], 'killed_external')
        self.assertEqual(s[U('smc', 5)[2]], 'not_run')

    def test_RC21_a_done_whose_sidecar_does_not_verify_is_not_done(self):
        self.assertNotEqual(self.tab('smc')[U('smc', 6)[2]], 'done')

    def test_RC22_smc_done_row_carries_the_native_status_from_the_csv(self):
        if self.err:
            self.fail(self.err)
        row = [r for u, s, r in self.tables['smc'] if u == U('smc', 1)[2]][0]
        self.assertIn('resource_limit', row, 'the native v3_status of a done SMC unit is reported')

    def test_RC30_smcrep_classes(self):
        s = self.tab('smcrep')
        self.assertEqual(s[U('smcrep', 1, m=1)[2]], 'done')
        self.assertEqual(s[U('smcrep', 2, m=1)[2]], 'not_run')

    def test_RC40_unexpected_folder_is_listed(self):
        tsv, md = self.t.find_outputs()
        blob = self.t.out
        for p in list(tsv.values()) + md:
            blob += open(p, encoding='utf-8', errors='replace').read()
        self.assertIn('ZZ_unexpected_unit', blob, 'a result folder outside the expected set must be listed (as unexpected)')
        self.assertIn('unexpected', blob.lower())

    def test_RC41_unexpected_folder_does_not_replace_or_hide_an_expected_unit(self):
        if self.err:
            self.fail(self.err)
        self.assertEqual(len([u for u, _, _ in self.tables['enum20'] if u == ds(1)]), 1)


class TestAllDone(unittest.TestCase):
    def test_RC50_exit_0_only_when_all_done(self):
        units = [U('enum20', i) for i in range(1, 4)] + [U('smc', 1), U('smc', 2)] + [U('smcrep', 1, m=1), U('smcrep', 1, m=2)]
        t = Tree('alldone', units)
        for u in units:
            t.done(u[0], u[2], u[3])
            t.rec('start', u[0], u[2], '8500_0')
            t.rec('end', u[0], u[2], '8500_0')
        t.run()
        self.assertEqual(t.rc, 0, t.out[-600:])
        s = {u: st for u, st, _ in t.table('enum20')}
        self.assertEqual(set(s.values()), {'done'})
        # one deferred unit flips the exit status
        shutil.rmtree(t.case_dir('smc', U('smc', 2)[2], ds(2)))
        t.rec('deferred', 'smc', U('smc', 2)[2], '8600_0')
        t.run()
        self.assertNotEqual(t.rc, 0, 'one unit not done must give a non-zero exit')

    def test_RC52_without_expected_tsv_an_all_done_tree_is_not_complete(self):
        """F2: a run is not complete before the initial P5 scan inventory exists: exit nonzero and INVENTORY.md says PENDING."""
        units = [U('enum20', 1), U('smc', 1), U('smc', 2)]
        t = Tree('alldone_nop5', units, p5=False)
        for u in units:
            t.done(u[0], u[2], u[3])
        t.run()
        self.assertNotEqual(t.rc, 0, 'no p5/expected.tsv: P5 PENDING must make the exit nonzero. ' + t.out[-300:])
        _, md = t.find_outputs()
        blob = ''.join(open(p, encoding='utf-8', errors='replace').read() for p in md) + t.out
        self.assertIn('PENDING', blob)
        t2 = Tree('alldone_p5', units)
        for u in units:
            t2.done(u[0], u[2], u[3])
        t2.run()
        self.assertEqual(t2.rc, 0, 'control: the same tree with a header-only expected.tsv is complete. ' + t2.out[-300:])

    def test_RC51_a_missing_result_root_is_not_a_clean_pass(self):
        units = [U('enum20', 1)]
        t = Tree('empty', units)
        t.run()
        self.assertNotEqual(t.rc, 0, 'no result at all: every expected unit is not_run, exit must not be 0')


class TestStrict(unittest.TestCase):
    """F6: exact completion validation. enum20 units 1-5 and smc units 1-6 are malformed in distinct ways; the rest are valid."""

    @classmethod
    def setUpClass(cls):
        units = [U('enum20', i) for i in range(1, 9)] + [U('smc', i) for i in range(1, 9)]
        t = Tree('strict', units)
        for u in units:
            t.done(u[0], u[2], u[3])
        # enum20: 1 missing RDS (sidecar names another file), 2 two-line sidecar, 3 .done carries another hash, 4 empty RDS, 5 sidecar names other.rds
        d = t.case_dir('enum20', ds(1), ds(1)); os.remove(d + '/EXACT.rds'); open(d + '/unrelated.bin', 'w').write('x')
        open(d + '/EXACT.sha256', 'w').write('%s  unrelated.bin\n' % sha(d + '/unrelated.bin'))
        d = t.case_dir('enum20', ds(2), ds(2)); h = sha(d + '/EXACT.rds'); open(d + '/EXACT.sha256', 'w').write('%s  EXACT.rds\n%s  EXACT.rds\n' % (h, h))
        d = t.case_dir('enum20', ds(3), ds(3)); open(d + '/EXACT.done', 'w').write('%s\nt\n' % ('0' * 64))
        d = t.case_dir('enum20', ds(4), ds(4)); open(d + '/EXACT.rds', 'w').close(); open(d + '/EXACT.sha256', 'w').write('%s  EXACT.rds\n' % sha(d + '/EXACT.rds'))
        open(d + '/EXACT.done', 'w').write('%s\nt\n' % sha(d + '/EXACT.rds'))
        d = t.case_dir('enum20', ds(5), ds(5)); open(d + '/EXACT.sha256', 'w').write('%s  other.rds\n' % sha(d + '/EXACT.rds'))
        # smc: 1 one-line sidecar, 2 duplicate name, 3 malformed .done, 4 CSV without status/v3_status, 5 CSV with 3 rows, 6 name escaping the folder, 7 committed failure (valid)
        def smc_dir(i):
            return t.case_dir('smc', U('smc', i)[2], ds(i))
        d = smc_dir(1); open(d + '/SMCBVS.sha256', 'w').write('%s  SMCBVS.rds\n' % sha(d + '/SMCBVS.rds'))
        d = smc_dir(2); open(d + '/SMCBVS.sha256', 'w').write('%s  SMCBVS.rds\n%s  SMCBVS.rds\n' % (sha(d + '/SMCBVS.rds'), sha(d + '/SMCBVS.rds')))
        d = smc_dir(3); open(d + '/SMCBVS.done', 'w').write('garbage marker\n')
        d = smc_dir(4); open(d + '/SMCBVS.csv', 'w').write('rule_id,foo\nhpm,1\npip05,2\n')
        open(d + '/SMCBVS.sha256', 'w').write('%s  SMCBVS.rds\n%s  SMCBVS.csv\n' % (sha(d + '/SMCBVS.rds'), sha(d + '/SMCBVS.csv')))
        d = smc_dir(5); open(d + '/SMCBVS.csv', 'w').write('rule_id,v3_status,status\nhpm,complete,ok\npip05,complete,ok\nx,complete,ok\n')
        open(d + '/SMCBVS.sha256', 'w').write('%s  SMCBVS.rds\n%s  SMCBVS.csv\n' % (sha(d + '/SMCBVS.rds'), sha(d + '/SMCBVS.csv')))
        d = smc_dir(6); open(d + '/../escape.rds', 'w').write('e')
        open(d + '/SMCBVS.sha256', 'w').write('%s  ../escape.rds\n%s  SMCBVS.csv\n' % (sha(d + '/../escape.rds'), sha(d + '/SMCBVS.csv')))
        d = smc_dir(7); open(d + '/SMCBVS.csv', 'w').write('rule_id,v3_status,status\nhpm,resource_limit,failed\npip05,resource_limit,failed\n')
        open(d + '/SMCBVS.sha256', 'w').write('%s  SMCBVS.rds\n%s  SMCBVS.csv\n' % (sha(d + '/SMCBVS.rds'), sha(d + '/SMCBVS.csv')))
        open(d + '/SMCBVS.done', 'w').write('status failed,failed\nfinished_utc t\n')
        t.run()
        cls.t = t
        cls.err = None
        cls.tab = {}
        try:
            for p in ('enum20', 'smc'):
                cls.tab[p] = {u: (s, r) for u, s, r in t.table(p)}
        except AssertionError as exc:
            cls.err = str(exc)

    def status(self, piece, unit):
        if self.err:
            self.fail(self.err)
        return self.tab[piece][unit][0]

    def test_SV01_enum_malformed_are_not_done(self):
        for i, why in ((1, 'missing RDS, sidecar for another file'), (2, 'two-line sidecar'), (3, '.done of another hash'), (4, 'empty RDS'), (5, 'sidecar names other.rds')):
            self.assertNotEqual(self.status('enum20', ds(i)), 'done', why)

    def test_SV02_enum_valid_are_done(self):
        for i in (6, 7, 8):
            self.assertEqual(self.status('enum20', ds(i)), 'done')

    def test_SV03_smc_malformed_are_not_done(self):
        for i, why in ((1, 'one-line sidecar'), (2, 'duplicate name'), (3, 'malformed .done'), (4, 'CSV without the columns'), (5, 'CSV with 3 rows'), (6, 'escaping name')):
            self.assertNotEqual(self.status('smc', U('smc', i)[2]), 'done', why)

    def test_SV04_committed_scientific_failure_stays_done_with_its_native_status(self):
        self.assertEqual(self.status('smc', U('smc', 7)[2]), 'done')
        self.assertIn('resource_limit', self.tab['smc'][U('smc', 7)[2]][1])

    def test_SV05_exit_nonzero(self):
        self.assertNotEqual(self.t.rc, 0)

    def test_SV06_unexpected_folder_alone_makes_the_exit_nonzero(self):
        units = [U('enum20', i) for i in range(1, 3)]
        t = Tree('unexp_only', units)
        for u in units:
            t.done(u[0], u[2], u[3])
        t.run()
        self.assertEqual(t.rc, 0, 'control: everything done, nothing unexpected: ' + t.out[-300:])
        t.junk_folder('enum20', 'ZZ_unexpected_unit')
        t.run()
        self.assertNotEqual(t.rc, 0, 'an unexpected result folder must make the exit status non-zero')

    def test_SV07_malformed_csv_alone_makes_the_exit_nonzero(self):
        units = [U('smc', 1), U('smc', 2)]
        t = make_home('bad_csv_only', units)
        t.run()
        self.assertEqual(t.rc, 0, 'control: ' + t.out[-300:])
        d = t.case_dir('smc', units[0][2], units[0][3]); open(d + '/SMCBVS.csv', 'w').write('not,a,csv\n"unterminated\n')
        t.run()
        self.assertNotEqual(t.rc, 0)


class HomeTree(Tree):
    """Home-root layout: HOME/runs/<RID>/{code/prod_l (bundle copy), manifests/}, SCR/{results,logs/<RID>}; the tool is run with --home-root/--scr-root."""

    def __init__(self, name, units):
        self.base = os.path.join(WORK, name).replace('\\', '/')
        shutil.rmtree(self.base, ignore_errors=True)
        self.home = self.base + '/home/New_Campaign'
        self.scr = self.base + '/scr/New_Campaign'
        self.runh = '%s/runs/%s' % (self.home, RID)
        self.bundle = self.runh + '/code/prod_l'
        self.res = self.scr + '/results'
        self.logs = self.scr + '/logs'
        os.makedirs(self.res)
        os.makedirs(self.logs + '/' + RID)
        os.makedirs(self.runh + '/manifests')
        shutil.copytree(B, self.bundle, ignore=shutil.ignore_patterns('tests', 'review', '__pycache__', 'PROGRESS.md'))
        self.units = units
        with open(self.bundle + '/lists/units.tsv', 'w', newline='\n') as fh:
            fh.write('piece\ttask\tunit\tdataset\tscale\trepeat\n')
            for u in units:
                fh.write('\t'.join(str(x) for x in u) + '\n')

    def run(self):
        shutil.rmtree(self.base + '/out', ignore_errors=True)
        cmd = [sys.executable, '-I', self.bundle + '/reconcile_prodl.py', STAMP, '--home-root', self.home, '--scr-root', self.scr,
               '--lists', self.bundle + '/lists/units.tsv', '--out', self.base + '/out']
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        self.rc, self.out = p.returncode, p.stdout + p.stderr
        return self

    def close_piece(self, piece):
        """what make_manifests.sh leaves behind: <piece>.inventory.tsv and <piece>.CLOSED carrying inventory_sha256="""
        tsv, _ = self.find_outputs()
        src = tsv[piece]
        dst = '%s/manifests/%s.inventory.tsv' % (self.runh, piece)
        shutil.copyfile(src, dst)
        h = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
        exf = '%s/manifests/%s.exceptions.tsv' % (self.runh, piece)      # R2 I2: the piece's exception rows (header only when clean), hash-bound in CLOSED
        with open(exf, 'w', newline='\n') as fh:
            fh.write('piece\tkind\titem\tdetail\n')
        eh = hashlib.sha256(open(exf, 'rb').read()).hexdigest()
        with open('%s/manifests/%s.CLOSED' % (self.runh, piece), 'w', newline='\n') as fh:
            fh.write('closed_utc=2026-10-30T14:00:00Z\ninventory_sha256=%s\nexceptions_sha256=%s\nacknowledged_exceptions=0\n' % (h, eh))
        return dst


def make_home(name, units):
    """a home-layout tree with every unit done and an EMPTY expected P5 inventory (so that P5 does not matter)"""
    t = HomeTree(name, units)
    for u in units:
        t.done(u[0], u[2], u[3])
    os.makedirs(t.runh + '/p5', exist_ok=True)
    open(t.runh + '/p5/expected.tsv', 'w').write('piece\ttask\tunit\tdataset\tscale\trepeat\tbase_piece\n')
    os.makedirs(t.logs + '/' + RID + '/p5', exist_ok=True)
    p5_scan_files(t.logs + '/' + RID, t.runh, units)
    return t


class TestClosedPieces(unittest.TestCase):
    """F7: a CLOSED piece is reconciled from its immutable inventory (hash-checked against <piece>.CLOSED), not from scratch."""

    def make(self, name):
        units = [U('enum20', i) for i in range(1, 4)] + [U('smc', 1), U('smc', 2)]
        return make_home(name, units)

    def test_CL01_close_move_away_reconcile_still_done(self):
        t = self.make('closed_move')
        t.run()
        self.assertEqual(t.rc, 0, 'control (home-root layout, everything done): ' + t.out[-500:])
        t.close_piece('enum20')
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/downloaded_enum20')       # pulled and deleted from scratch
        t.run()
        self.assertEqual(t.rc, 0, 'a CLOSED piece whose folder left scratch must stay done: ' + t.out[-500:])
        rows = {u: s for u, s, _ in t.table('enum20')}
        self.assertEqual(set(rows.values()), {'done'}, rows)
        self.assertEqual(sorted(rows), sorted(u[2] for u in t.units if u[0] == 'enum20'), 'every expected unit exactly once')

    def test_CL02_not_closed_piece_moved_away_is_not_run(self):
        t = self.make('open_move')
        t.run()
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/downloaded_enum20')
        t.run()
        self.assertNotEqual(t.rc, 0, 'control: without a CLOSED marker the missing folder is not_run')
        self.assertEqual({s for _, s, _ in t.table('enum20')}, {'not_run'})

    def test_CL03_tampered_inventory_exits_2(self):
        t = self.make('closed_tamper')
        t.run()
        inv = t.close_piece('enum20')
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/downloaded_enum20')
        with open(inv, 'a', newline='\n') as fh:
            fh.write('enum20\tp0020_S1_r099\tdone\tforged\n')
        t.run()
        self.assertEqual(t.rc, 2, 'an inventory whose sha256 differs from <piece>.CLOSED: exit 2. ' + t.out[-400:])

    def test_CL04_closed_piece_is_marked_closed_in_INVENTORY_md(self):
        t = self.make('closed_md')
        t.run()
        t.close_piece('enum20')
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/downloaded_enum20')
        t.run()
        _, md = t.find_outputs()
        blob = ''.join(open(p, encoding='utf-8', errors='replace').read() for p in md)
        self.assertIn('closed', blob.lower())

    def test_CL05_live_pieces_still_checked_against_scratch(self):
        t = self.make('closed_live')
        t.run()
        t.close_piece('enum20')
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/downloaded_enum20')
        os.remove(t.case_dir('smc', U('smc', 2)[2], ds(2)) + '/SMCBVS.done')
        t.run()
        self.assertNotEqual(t.rc, 0)
        self.assertNotEqual({u: s for u, s, _ in t.table('smc')}[U('smc', 2)[2]], 'done')
        self.assertEqual({s for _, s, _ in t.table('enum20')}, {'done'}, 'the closed piece is unaffected')

    def test_CL06_all_units_covered_in_one_final_inventory(self):
        t = self.make('closed_all')
        t.run()
        t.close_piece('enum20'); t.close_piece('smc')
        shutil.move('%s/%s_lowp_enum20' % (t.res, STAMP), t.base + '/dl1')
        shutil.move('%s/%s_lowp_smc' % (t.res, STAMP), t.base + '/dl2')
        t.run()
        self.assertEqual(t.rc, 0, t.out[-400:])
        n = sum(len(t.table(p)) for p in ('enum20', 'smc'))
        self.assertEqual(n, len(t.units))


class TestExceptionsLive(unittest.TestCase):
    """R2 I2 / I1.3: reconcile writes <out>/exceptions.tsv (piece kind item detail) and a STATUS line in INVENTORY.md:
    CLEAN (exit 0) | COMPLETE WITH n HQ-ACKNOWLEDGED EXCEPTIONS (exit 4) | INCOMPLETE OR UNRESOLVED (exit 1); exit 2 stays for input errors / tampering.
    (The closed-piece and acknowledged-exception flows use the real make_manifests.sh: test_manifests.sh X01-X32.)"""

    UNITS = [U('enum20', 1), U('enum20', 2), U('smc', 1), U('smc', 2), U('smcrep', 1, m=1)]

    def make(self, name):
        t = make_home(name, self.UNITS)
        return t

    @staticmethod
    def exceptions(t):
        p = t.base + '/out/exceptions.tsv'
        if not os.path.isfile(p):
            return None
        return [ln.rstrip('\r\n').split('\t') for ln in open(p, encoding='utf-8') if ln.strip()]

    @staticmethod
    def status(t):
        for p in (t.base + '/out/INVENTORY.md',):
            for ln in open(p, encoding='utf-8', errors='replace'):
                if 'STATUS' in ln.upper():
                    return ln.strip()
        return ''

    def test_EX01_clean(self):
        t = self.make('ex_clean').run()
        self.assertEqual(t.rc, 0, t.out[-400:])
        rows = self.exceptions(t)
        self.assertIsNotNone(rows, 'exceptions.tsv is written')
        self.assertEqual(rows[0], ['piece', 'kind', 'item', 'detail'])
        self.assertEqual(len(rows), 1, 'no exception rows')
        self.assertIn('CLEAN', self.status(t))

    def test_EX02_malformed_record_is_an_exception(self):
        t = self.make('ex_malformed')
        d = t.case_dir('smc', U('smc', 1)[2], ds(1))
        open(d + '/SMCBVS.csv', 'w').write('not,a,valid\n"x\n')
        t.run()
        self.assertEqual(t.rc, 1, t.out[-400:])
        rows = self.exceptions(t) or []
        self.assertTrue([r for r in rows[1:] if r[0] == 'smc' and r[1] == 'malformed_record'], rows)
        self.assertIn('INCOMPLETE OR UNRESOLVED', self.status(t))

    def test_EX03_unexpected_output_with_every_unit_done(self):
        t = self.make('ex_unexpected')
        t.junk_folder('enum20', 'ZZ_unexpected_unit')
        t.run()
        self.assertEqual(t.rc, 1, 'all expected units done, an unexpected folder: ' + t.out[-400:])
        rows = self.exceptions(t) or []
        self.assertTrue([r for r in rows[1:] if r[0] == 'enum20' and r[1] == 'unexpected_output' and 'ZZ_unexpected_unit' in r[2]], rows)
        self.assertIn('INCOMPLETE OR UNRESOLVED', self.status(t))

    def final_scan(self, t, smc_rows, rep_rows, job=7011):
        lp = t.logs + '/' + RID + '/p5'
        for name, rows in (('smc', smc_rows), ('smcrep', rep_rows)):
            with open('%s/scan_final_%s.tsv' % (lp, name), 'w', newline='\n') as fh:
                fh.write(SCAN_HDR + '\n')
                for r in rows:
                    fh.write(r + '\n')
        open(lp + '/scan_final.ok', 'w').write('ok\n')
        with open(t.runh + '/JOBIDS.tsv', 'a', newline='\n') as fh:
            fh.write('p5scan_final\ts5_p5scan\t%d\t-\t-\n' % job)

    def test_EX04_p5_unlisted_eligible_is_an_exception_and_names_the_scan_phase(self):
        t = self.make('ex_unlisted')
        self.final_scan(t, [scan_row(ds(1) + '_c100', 'SMCBVS', 0, 'completed', 'none'), scan_row(ds(2) + '_c100', 'SMCBVS', 0, 'resource_limit', 'none')],
                        [scan_row(ds(1) + '_c100', 'SMCBVS_rep1', 1, 'completed', 'none')])
        t.run()
        self.assertNotEqual(t.rc, 0, t.out[-400:])
        rows = self.exceptions(t) or []
        self.assertTrue([r for r in rows[1:] if r[1] == 'p5_unlisted_eligible' and ds(2) in r[2]], rows)
        md = open(t.base + '/out/INVENTORY.md', encoding='utf-8', errors='replace').read()
        self.assertIn('final', md.lower(), 'INVENTORY.md names the scan phase used (the newest successful one: final)')

    def test_EX05_unsafe_retry_state_is_an_exception(self):
        t = self.make('ex_unsafe')
        self.final_scan(t, [scan_row(ds(1) + '_c100', 'SMCBVS', 0, 'completed', 'none'), scan_row(ds(2) + '_c100', 'SMCBVS', 0, 'resource_limit', 'locked')],
                        [scan_row(ds(1) + '_c100', 'SMCBVS_rep1', 1, 'completed', 'none')])
        t.run()
        self.assertNotEqual(t.rc, 0, t.out[-400:])
        rows = self.exceptions(t) or []
        self.assertTrue([r for r in rows[1:] if r[1] == 'p5_unsafe_state'], rows)

    def test_EX06_newest_scan_phase_is_by_job_id(self):
        """the final scan has a LOWER job id than the initial one is impossible in practice; here the initial scan (7003) is older than r1 (7005): the check uses r1"""
        t = self.make('ex_newest')
        lp = t.logs + '/' + RID + '/p5'
        with open(lp + '/scan_r1_smc.tsv', 'w', newline='\n') as fh:
            fh.write(SCAN_HDR + '\n')
            fh.write(scan_row(ds(1) + '_c100', 'SMCBVS', 0, 'completed', 'none') + '\n')
            fh.write(scan_row(ds(2) + '_c100', 'SMCBVS', 0, 'resource_limit', 'none') + '\n')
        with open(lp + '/scan_r1_smcrep.tsv', 'w', newline='\n') as fh:
            fh.write(SCAN_HDR + '\n')
        open(lp + '/scan_r1.ok', 'w').write('ok\n')
        with open(t.runh + '/JOBIDS.tsv', 'a', newline='\n') as fh:
            fh.write('p5scan_r1\ts5_p5scan\t7005\t-\t-\n')
        t.run()
        rows = self.exceptions(t) or []
        self.assertTrue([r for r in rows[1:] if r[1] == 'p5_unlisted_eligible' and ds(2) in r[2]], 'r1 (job 7005) is newer than initial (7003): ' + str(rows))


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
    if not os.path.isfile(B + '/reconcile_prodl.py'):
        print('FAIL reconcile_prodl.py not found')
        print('test_reconcile: 0 passed, 1 failed')
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    failed = len(res.failures) + len(res.errors) + len(res.skipped)
    print('test_reconcile: %d passed, %d failed' % (res.testsRun - failed, failed))
    sys.exit(0 if failed == 0 else 1)
