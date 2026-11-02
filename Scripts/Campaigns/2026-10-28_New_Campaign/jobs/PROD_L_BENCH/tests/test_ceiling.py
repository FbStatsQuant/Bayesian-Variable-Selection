#!/usr/bin/env python3
"""test_ceiling.py -- ceiling_check.py (PROD-L's, unchanged) with the BENCHMARK wave's plan (DESIGN.md section 4, D47.4).  py -3 test_ceiling.py [WORKDIR]

Plan (header step cpus max_concurrent_tasks phase): s0_verify 1x1 pre ; s1_bench 1 CPU x 32 (alone) / 16 (withH) fit ; s9_collect 1x1 post.  billed(c) = 2*ceil(c/2).
Bench peak: alone 2*32 = 64 ; withH 2*16 = 32.  Refused: alone with a _prodH job; PROD-L peak > 132 (alone) / 68 (withH); others' potential peak + bench peak > 192.
Others = every squeue row not of this run (PROD-H, PROD-L's lowpL_ jobs, BENCH_F3, anything of fb31).
"""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.environ.get('PRODL_B_SRC') or os.path.dirname(HERE)
SCRIPT = os.path.join(B, 'ceiling_check.py')
ROOT = 'C:/Users/felip/AppData/Local/Temp/prodl_tests'
WORK = None


def plan(n):
    rows = [('s0_verify', 1, 1, 'pre'), ('s1_bench', 1, n, 'fit'), ('s9_collect', 1, 1, 'post')]
    return 'step\tcpus\tmax_concurrent_tasks\tphase\n' + ''.join('%s\t%d\t%d\t%s\n' % r for r in rows)


PLAN_ALONE = plan(32)
PLAN_WITHH = plan(16)


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
        self.assertEqual(rc, 0, 'expected ADMITTED, got %s; output: %s; receipt: %s' % (rc, out[-300:], (rec or '')[-300:]))
        return rec

    def refused(self, *a, **k):
        rc, rec, out = self.run_check(*a, **k)
        self.assertEqual(rc, 2, 'expected REFUSED (2), got %s; output: %s; receipt: %s' % (rc, out[-300:], (rec or '')[-300:]))
        return rec


class TestBenchPlan(Base):
    def test_B01_empty_alone_peak_64(self):
        rec = self.admitted('alone', PLAN_ALONE, '')
        self.assertIsNotNone(rec)
        self.assertIn('64', rec, 'receipt carries the bench peak 64')

    def test_B02_empty_withH_peak_32(self):
        rec = self.admitted('withH', PLAN_WITHH, '')
        self.assertIn('32', rec, 'receipt carries the bench peak 32')

    def test_B03_plan_caps(self):
        self.admitted('alone', plan(66), '')       # 132
        self.refused('alone', plan(67), '')        # 134 > 132
        self.admitted('withH', plan(34), '')       # 68
        self.refused('withH', plan(35), '')        # 70 > 68

    def test_B04_unthrottled_pre_post_phases_do_not_add(self):
        self.admitted('alone', PLAN_ALONE + 's0_extra\t1\t1\tpre\n', '')     # pre = 4, fit = 64: the maximum over phases, not the sum

    def test_B05_prodH_alone_refused_withH_allowed(self):
        self.refused('alone', PLAN_ALONE, row('9001', 'bvs_prodH_s2', 'RUNNING', 2))
        self.admitted('withH', PLAN_WITHH, row('9001', 'bvs_prodH_s2', 'RUNNING', 2))

    def test_B06_combined_192_alone(self):
        self.admitted('alone', PLAN_ALONE, running(64))        # 64 + 128 = 192
        self.refused('alone', PLAN_ALONE, running(65))         # 194

    def test_B07_combined_192_withH(self):
        self.admitted('withH', PLAN_WITHH, running(80))        # 32 + 160
        self.refused('withH', PLAN_WITHH, running(81))

    def test_B08_prodH_task_guard_style_arrays_count_throttles(self):
        sq = row('9001_[1-600%31]', 'bvs_prodH_s2', 'PENDING', 1) + row('9002_[601-1200%31]', 'bvs_prodH_s2', 'PENDING', 1)    # 124 billed
        self.admitted('withH', PLAN_WITHH, sq)                                                                             # 124 + 32 = 156
        sq = row('9001_[1-600%50]', 'bvs_prodH_s2', 'PENDING', 1) + row('9002_[601-1200%50]', 'bvs_prodH_s2', 'PENDING', 1)  # 200
        self.refused('withH', PLAN_WITHH, sq)

    def test_B09_prodl_and_other_work_of_fb31_counts_as_others(self):
        self.admitted('alone', PLAN_ALONE, row('9001_[1-96%32]', 'lowpL_s2_smc', 'PENDING', 1))     # 64 + 64 = 128 <= 192
        self.refused('alone', PLAN_ALONE, row('9001_[1-96%32]', 'lowpL_s2_smc', 'PENDING', 1) + row('9002_[1-96%32]', 'lowpL_s3_smcrep', 'PENDING', 1) + running(1))   # 64+64+2 > 128
        self.refused('alone', PLAN_ALONE, row('9003_[1-96%65]', 'BENCH_F3_x', 'PENDING', 1))        # 130 others
        self.admitted('alone', PLAN_ALONE, row('9003_[1-96%64]', 'BENCH_F3_x', 'PENDING', 1))       # 128

    def test_B10_own_ids_ignored(self):
        own = row('7002_[0-95%32]', 'lowpB_s1_bench', 'PENDING', 1) + ''.join(row('7002_%d' % k, 'lowpB_s1_bench', 'RUNNING', 1) for k in range(32))
        self.refused('alone', PLAN_ALONE, own + running(50))                       # own 64 + 100 > 128 when counted as others
        self.admitted('alone', PLAN_ALONE, own + running(50), own_ids='7002')      # 100 <= 128 once ignored

    def test_B11_array_throttle_and_running_adjust(self):
        sq = ''
        for aid in ('9001', '9002'):
            sq += ''.join(row('%s_%d' % (aid, k), 'other_job', 'RUNNING', 1) for k in range(1, 6))
            sq += row('%s_[6-600%%31]' % aid, 'other_job', 'PENDING', 1)
        self.admitted('withH', PLAN_WITHH, sq)

    def test_B12_unparsable_refused_and_stdin_and_receipt(self):
        self.refused('alone', PLAN_ALONE, 'this is not a squeue row\n')
        self.refused('withH', PLAN_WITHH, row('9001', 'x', 'RUNNING', 'many'))
        self.admitted('withH', PLAN_WITHH, '', stdin=True)
        rec = self.refused('withH', PLAN_WITHH, running(90), stdin=True)
        self.assertTrue(rec and rec.strip(), 'a refusal leaves a receipt')


class TestBilled(Base):
    """billed(c) = 2*ceil(c/2) at the boundary: others 160 (withH, bench peak 32): N rows of c CPUs plus 1-CPU fillers (2 each) hit 160 exactly."""
    CASES = {1: (80, 0), 2: (80, 0), 3: (40, 0), 4: (40, 0), 5: (26, 2), 16: (10, 0)}

    def test_B20_billed_boundaries(self):
        for c, (n, fill) in self.CASES.items():
            with self.subTest(cpus=c):
                sq = running(n, c, 'rowc', 9100) + running(fill, 1, 'filler', 9800)
                self.admitted('withH', PLAN_WITHH, sq)
                self.refused('withH', PLAN_WITHH, sq + running(1, 1, 'filler', 9900))


def load_workdir():
    global WORK
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    base = (args[0] if args else ROOT + '/test_ceiling').replace('\\', '/')
    if not base.startswith(ROOT + '/') or '..' in base:
        sys.stderr.write('REFUSED: work dir must be under %s\n' % ROOT)
        sys.exit(64)
    WORK = base
    sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]


if __name__ == '__main__':
    load_workdir()
    if not os.path.isfile(SCRIPT):
        print('FAIL ceiling_check.py not found at ' + SCRIPT)
        print('test_ceiling: 0 passed, 1 failed')
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    failed = len(res.failures) + len(res.errors) + len(res.skipped)
    print('test_ceiling: %d passed, %d failed' % (res.testsRun - failed, failed))
    sys.exit(0 if failed == 0 else 1)
