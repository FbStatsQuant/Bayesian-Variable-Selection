#!/usr/bin/env python3
"""test_ceiling.py -- acceptance tests of ceiling_check.py (DESIGN.md section 7, D47.4, Sol finding 6). Python 3 stdlib unittest:  py -3 test_ceiling.py [WORKDIR]

CLI under test (DESIGN section 7): --profile alone|withH  --plan plan.tsv (rows: step, cpus, max_concurrent_tasks, phase; tab separated, no header)
--squeue FILE|-   (rows  id|name|state|cpus  = squeue -h -u fb31 -o '%i|%j|%T|%C')  --own-ids a,b,c  --receipt FILE.   Exit 0 admitted, 2 refused.
billed(c) = 2*ceil(c/2).  PROD-L peak: alone 4 + 4*16 + 32*2 = 132 ; withH 4 + 2*16 + 16*2 = 68.  Refused if: alone and a _prodH row is present;
PROD-L peak > 132 (alone) / 68 (withH); others' potential peak + PROD-L peak > 192.
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
SCRIPT = os.path.join(B, 'ceiling_check.py')
ROOT = 'C:/Users/felip/AppData/Local/Temp/prodl_tests'
WORK = None


def plan(enum30, smc, extra_fit_rep=None):
    """Main-wave plan. smc and smcrep never overlap (smcrep is afterany smc): smcrep gets its own phase."""
    rows = [('s0_build', 2, 1, 'pre'), ('s0_verify', 1, 1, 'pre'), ('s0_truthlock', 1, 1, 'pre'), ('s0_lock', 1, 1, 'pre'),
            ('s1_enum20', 4, 1, 'fit'), ('s1_enum30', 16, enum30, 'fit'), ('s2_smc', 1, smc, 'fit'),
            ('s3_smcrep', 1, smc if extra_fit_rep is None else extra_fit_rep, 'fit_rep'),
            ('s8_unlock', 1, 1, 'post'), ('s9_collect', 1, 1, 'post')]
    return 'step\tcpus\tmax_concurrent_tasks\tphase\n' + ''.join('%s\t%d\t%d\t%s\n' % r for r in rows)


PLAN_ALONE = plan(4, 32)
PLAN_WITHH = plan(2, 16)


def row(i, name, state, cpus):
    return '%s|%s|%s|%s\n' % (i, name, state, cpus)


def plain(n, cpus=1, state='PENDING', name='other_job', start=9100):
    return ''.join(row(start + k, name, state, cpus) for k in range(n))


def running(n, cpus=1, name='filler', start=9500):
    return plain(n, cpus, 'RUNNING', name, start)


class Base(unittest.TestCase):
    def run_check(self, profile, plan_text, squeue_text, own_ids=None, stdin=False):
        os.makedirs(WORK, exist_ok=True)
        self.n = getattr(self, 'n', 0) + 1
        tag = '%s_%d' % (self.id().split('.')[-1], self.n)
        pf, sf, rf = (os.path.join(WORK, '%s.%s' % (tag, e)) for e in ('plan.tsv', 'squeue.txt', 'receipt.txt'))
        with open(pf, 'w', newline='\n') as fh:
            fh.write(plan_text)
        with open(sf, 'w', newline='\n') as fh:
            fh.write(squeue_text)
        cmd = [sys.executable, '-I', SCRIPT, '--profile', profile, '--plan', pf, '--squeue', '-' if stdin else sf, '--receipt', rf]
        if own_ids:
            cmd += ['--own-ids', own_ids]
        p = subprocess.run(cmd, input=squeue_text if stdin else None, capture_output=True, text=True, timeout=60)
        receipt = open(rf, encoding='utf-8').read() if os.path.exists(rf) else None
        return p.returncode, receipt, p.stdout + p.stderr

    def admitted(self, *a, **k):
        rc, rec, out = self.run_check(*a, **k)
        self.assertEqual(rc, 0, 'expected ADMITTED (exit 0), got %s; output: %s; receipt: %s' % (rc, out[-400:], (rec or '')[-400:]))
        return rec

    def refused(self, *a, **k):
        rc, rec, out = self.run_check(*a, **k)
        self.assertEqual(rc, 2, 'expected REFUSED (exit 2), got %s; output: %s; receipt: %s' % (rc, out[-400:], (rec or '')[-400:]))
        return rec


class TestPeak(Base):
    def test_C01_empty_alone_admitted_peak_132(self):
        rec = self.admitted('alone', PLAN_ALONE, '')
        self.assertIsNotNone(rec, 'no receipt written')
        self.assertIn('132', rec, 'receipt must carry the PROD-L peak 132')

    def test_C02_empty_withH_admitted_peak_68(self):
        rec = self.admitted('withH', PLAN_WITHH, '')
        self.assertIn('68', rec, 'receipt must carry the PROD-L peak 68')

    def test_C03_alone_plan_exceeding_132_refused(self):
        self.refused('alone', plan(5, 32), '')          # 4 + 5*16 + 64 = 148
        self.refused('alone', plan(4, 33), '')          # 4 + 64 + 66 = 134

    def test_C04_withH_with_the_alone_plan_refused(self):
        self.refused('withH', PLAN_ALONE, '')           # 132 > 68

    def test_C05_withH_plan_exceeding_68_refused(self):
        self.refused('withH', plan(2, 17), '')          # 4 + 32 + 34 = 70

    def test_C06_peak_at_the_limit_admitted(self):
        self.admitted('alone', plan(4, 32), '')
        self.admitted('withH', plan(2, 16), '')

    def test_C07_pre_phase_counts_in_the_maximum(self):
        # a pre phase far above the fit phase must dominate the peak (max over phases)
        big = PLAN_WITHH + 's0_extra\t16\t5\tpre\n'      # pre = 8 + 80 = 88 > 68 only if the rows of a phase are summed
        self.refused('withH', big, '')


class TestOthers(Base):
    def test_C10_prodH_present_alone_refused(self):
        rec = self.refused('alone', PLAN_ALONE, row('9001', 'bvs_prodH_s2', 'RUNNING', 2))
        low = (rec or '').lower()
        self.assertTrue('prodh' in low or 'prod-h' in low or 'prod_h' in low, 'receipt must name the PROD-H reason')

    def test_C11_prodH_name_anywhere_alone_refused(self):
        self.refused('alone', PLAN_ALONE, row('9001', 'x_prodH', 'PENDING', 1))
        self.refused('alone', PLAN_ALONE, row('9002_[1-10%5]', 'lowpH_prodH_s2', 'PENDING', 1))

    def test_C12_prodH_arrays_200_billed_withH_refused(self):
        sq = row('9001_[1-600%50]', 'bvs_prodH_s2', 'PENDING', 1) + row('9002_[601-1200%50]', 'bvs_prodH_s2', 'PENDING', 1)
        rec = self.refused('withH', PLAN_WITHH, sq)
        self.assertIn('200', rec, 'receipt must carry the others\' potential peak 200')

    def test_C13_prodH_124_billed_plus_68_is_192_admitted(self):
        sq = row('9001_[1-600%31]', 'bvs_prodH_s2', 'PENDING', 1) + row('9002_[601-1200%31]', 'bvs_prodH_s2', 'PENDING', 1)
        rec = self.admitted('withH', PLAN_WITHH, sq)
        self.assertIn('124', rec)

    def test_C14_prodH_withH_one_more_task_refused(self):
        sq = row('9001_[1-600%32]', 'bvs_prodH_s2', 'PENDING', 1) + row('9002_[601-1200%31]', 'bvs_prodH_s2', 'PENDING', 1)   # 126 + 68 = 194
        self.refused('withH', PLAN_WITHH, sq)

    def test_C15_running_rows_count_billed_2_per_1cpu(self):
        self.admitted('withH', PLAN_WITHH, running(62, 1, 'bvs_prodH_x'))        # 124 + 68 = 192
        self.refused('withH', PLAN_WITHH, running(63, 1, 'bvs_prodH_x'))         # 126 + 68 = 194

    def test_C16_array_without_throttle_counts_all_pending_tasks(self):
        self.admitted('withH', PLAN_WITHH, row('9005_[1-62]', 'other_job', 'PENDING', 1))     # 62 tasks * 2 = 124
        self.refused('withH', PLAN_WITHH, row('9005_[1-63]', 'other_job', 'PENDING', 1))      # 126

    def test_C17_array_throttle_caps_the_pending_tasks(self):
        self.admitted('withH', PLAN_WITHH, row('9005_[1-600%62]', 'other_job', 'PENDING', 1))   # min(600, 62) * 2 = 124
        self.refused('withH', PLAN_WITHH, row('9005_[1-600%63]', 'other_job', 'PENDING', 1))    # 126

    def test_C18_running_tasks_of_the_array_reduce_the_pending_allowance(self):
        # per array: 5 running (10) + min(595 pending, 31 - 5) * 2 (52) = 62 ; two arrays = 124 -> admitted. Ignoring the running tasks would give 144.
        sq = ''
        for aid, lo in (('9001', 6), ('9002', 6)):
            sq += ''.join(row('%s_%d' % (aid, k), 'other_job', 'RUNNING', 1) for k in range(1, 6))
            sq += row('%s_[%d-600%%31]' % (aid, lo), 'other_job', 'PENDING', 1)
        self.admitted('withH', PLAN_WITHH, sq)

    def test_C19_range_lists_are_counted_task_by_task(self):
        # '[1,3,5-9%4]' = 7 pending tasks, throttle 4 -> 4 * 2 = 8 billed ; plus 58 plain pending 1-CPU jobs (116) = 124
        base = row('9005_[1,3,5-9%4]', 'other_job', 'PENDING', 1)
        self.admitted('withH', PLAN_WITHH, base + plain(58))
        self.refused('withH', PLAN_WITHH, base + plain(59))

    def test_C20_pending_plain_job_counts_billed_cpus(self):
        self.admitted('withH', PLAN_WITHH, plain(62))
        self.refused('withH', PLAN_WITHH, plain(63))
        self.admitted('withH', PLAN_WITHH, plain(31, cpus=3))        # billed(3) = 4 -> 124
        self.refused('withH', PLAN_WITHH, plain(32, cpus=3))         # 128

    def test_C21_own_run_ids_are_ignored(self):
        own = row('7007_[0-95%32]', 'lowpL_s2_smc', 'PENDING', 1) + row('7008_[0-479%32]', 'lowpL_s3_smcrep', 'PENDING', 1) \
            + ''.join(row('7005_%d' % k, 'lowpL_s1_enum30', 'RUNNING', 16) for k in range(4))
        self.refused('withH', PLAN_WITHH, own)                        # 64 + 64 + 64 = 192 others + 68
        self.admitted('withH', PLAN_WITHH, own, own_ids='7005,7007,7008')

    def test_C22_partial_own_ids(self):
        own = row('7007_[0-95%32]', 'lowpL_s2_smc', 'PENDING', 1) + row('7008_[0-479%32]', 'lowpL_s3_smcrep', 'PENDING', 1) \
            + ''.join(row('7005_%d' % k, 'lowpL_s1_enum30', 'RUNNING', 16) for k in range(4))
        self.admitted('withH', PLAN_WITHH, own, own_ids='7005,7007')    # only 7008 (64) + 68 = 132 <= 192

    def test_C23_unparsable_row_refused(self):
        self.refused('withH', PLAN_WITHH, 'this is not a squeue row\n')
        self.refused('withH', PLAN_WITHH, row('9001', 'x', 'RUNNING', 'many'))
        self.refused('withH', PLAN_WITHH, row('9001_[a-b%3]', 'x', 'PENDING', 1))
        self.refused('alone', PLAN_ALONE, '9001|only|three\n')

    def test_C24_squeue_from_stdin(self):
        self.admitted('withH', PLAN_WITHH, '', stdin=True)
        self.refused('withH', PLAN_WITHH, running(63), stdin=True)

    def test_C25_receipt_written_for_a_refusal(self):
        rec = self.refused('withH', PLAN_WITHH, running(70))
        self.assertTrue(rec and rec.strip(), 'a refusal must leave a receipt with the numbers used')

    def test_C26_alone_without_prodH_but_others_over_60_refused(self):
        # alone: PROD-L 132, so others may use at most 60
        self.admitted('alone', PLAN_ALONE, running(30))      # 60
        self.refused('alone', PLAN_ALONE, running(31))       # 62


class TestBilled(Base):
    """billed(c) = 2*ceil(c/2) tested at the boundary 124 = 192 - 68 (withH): N rows of c CPUs plus 1-CPU filler rows (billed 2 each) hit 124 exactly."""
    CASES = {1: (62, 0), 2: (62, 0), 3: (30, 2), 4: (31, 0), 16: (7, 6)}   # c: (rows of c CPUs, filler rows)

    def test_C30_billed_boundaries(self):
        for c, (n, fill) in self.CASES.items():
            with self.subTest(cpus=c):
                sq = running(n, c, 'rowc', 9100) + running(fill, 1, 'filler', 9800)
                self.admitted('withH', PLAN_WITHH, sq)                           # exactly 124
                self.refused('withH', PLAN_WITHH, sq + running(1, 1, 'filler', 9900))   # 126

    def test_C31_odd_cpu_requests_bill_the_next_even_number(self):
        # c=5 bills 6: 20 rows = 120 (+ 2 filler rows = 124) admitted ; one more filler refused
        sq = running(20, 5, 'rowc') + running(2, 1, 'filler', 9800)
        self.admitted('withH', PLAN_WITHH, sq)
        self.refused('withH', PLAN_WITHH, sq + running(1, 1, 'filler', 9900))


def load_workdir():
    global WORK
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    base = args[0] if args else ROOT + '/test_ceiling'
    base = base.replace('\\', '/')
    if not base.startswith(ROOT + '/') or '..' in base:
        sys.stderr.write('REFUSED: work dir must be under %s\n' % ROOT)
        sys.exit(64)
    WORK = base
    sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]


class _Result(unittest.TextTestResult):
    pass


if __name__ == '__main__':
    load_workdir()
    if not os.path.isfile(SCRIPT):
        print('FAIL ceiling_check.py not found at ' + SCRIPT)
        print('0 passed, 1 failed')
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2, resultclass=_Result).run(suite)
    failed = len(res.failures) + len(res.errors) + len(res.skipped)
    passed = res.testsRun - failed
    print('test_ceiling: %d passed, %d failed' % (passed, failed))
    sys.exit(0 if failed == 0 else 1)
