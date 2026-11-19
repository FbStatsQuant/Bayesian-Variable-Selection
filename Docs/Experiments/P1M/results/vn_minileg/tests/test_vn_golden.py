#!/usr/bin/env python3
"""Self-tests of precision_freeze_vn.py (V-N mini-leg). python3 -I tests/test_vn_golden.py
 (1) GOLDEN: on the leg's REAL FZ records (if present on this machine) the V-N copy with default arguments gives the same identity / decisions / detail / targets as the
     registered precision_freeze.py (sha 7cdd69a1...), unedited. The test is skipped, loudly, only if the records are absent.
 (2) SYNTHETIC: the N arm at the frozen configuration (10^4, m 1, I_max 0) against the N = 2,500 I_max = 0 baseline: ADOPT / KEEP / INCOMPLETE / cost-batch file skipped;
     the registered script gives NOT_RUN for that cell (why a parameterised copy exists), and scores the I_max = 3 N arm verbatim.
Scratch under PREC_TEST_TMP or the tests dir (never /tmp)."""
import json, os, re, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); VN = os.path.join(os.path.dirname(HERE), "precision_freeze_vn.py")
REG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "precision1e4", "precision_freeze.py")
DS = ("AR", "ARweak", "ADJOPP")
FZ_R = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4"); FZ_C = os.path.expanduser("~/SMC_Engineering_Department/tmp/20261119-fz/cost")


def mk(root, cdir, ds, tag, m1, m2, m3, isl, hpm=(1, 2, 3)):
    g = re.match(r"N(\d+)-m(\d+)(?:-I(\d))?-c\d", tag).groups(); rec = (int(g[0]), int(g[1]), int(g[2]) if g[2] is not None else 3)
    rid = "4-%s-n200-r01-P-%s-s1" % (ds, tag); d = os.path.join(root, rid); os.makedirs(d)
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": "completed", "fit_status": "completed", "evidence": {"sigma_hat": m3, "sigma_hat_robust": m3}, "selection": {"hpm": list(hpm)}, "pip": {"island_spread": {"max_sd": m2, "target_met": m2 <= 0.005}},
               "fit": {"meta": {"occ": [{"M": 1000, "sd_log_Z_occ_r": m1}], "flags": {"occ_inhomogeneous": False}}}}, open(os.path.join(d, "eval.bin.json"), "w"))
    json.dump({"run_id": rid, "stages": {"islands": {"billed_core_h": isl}}}, open(os.path.join(cdir, "cost_%s.json" % rid), "w"))
    json.dump({"meta": {"N": rec[0], "refine_m": rec[1], "I_max": rec[2], "I_used": min(rec[2], 3), "rule": "bounded", "flags": {"grid_unconverged": True}}}, open(os.path.join(d, "calib_meta.json"), "w"))


def run(script, records, cdirs, out, *extra):
    r = subprocess.run([sys.executable, "-I", script, "--records", *records, "--cost-dir", *cdirs, "--out", out, *extra], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.load(open(os.path.join(out, "freeze.json")))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t)

    def build(self, ratio_I0, ratio_I3, cost_ratio=3.85):
        for ds in DS:
            for c in (1, 2):
                for I, ratio in ((0, ratio_I0), (3, ratio_I3)):
                    t0 = "N2500-m1-I0-c%d" % c if I == 0 else "N2500-m1-c%d" % c
                    t1 = "N10000-m1-I0-c%d" % c if I == 0 else "N10000-m1-c%d" % c
                    mk(self.r, self.c, ds, t0, 0.02, 0.0004, 0.025, 5.0)
                    mk(self.r, self.c, ds, t1, 0.02 * ratio, 0.0004 * ratio, 0.025 * ratio, 5.0 * cost_ratio)

    def test_golden_equals_registered_on_the_real_fz_records(self):
        roots = [os.path.join(FZ_R, w) for w in ("A0", "P1", "P2", "P3", "P4")]
        if not (all(os.path.isdir(x) for x in roots) and os.path.isdir(FZ_C)):
            self.skipTest("FZ records not on this machine: GOLDEN NOT CHECKED")
        a = run(REG, roots, [FZ_C], os.path.join(self.t, "a")); b = run(VN, roots, [FZ_C], os.path.join(self.t, "b"))
        for k in ("datasets", "cells", "identity", "decisions", "detail", "targets_per_fit"):
            self.assertEqual(a[k], b[k], k)
        self.assertEqual(a["decisions"]["m=4"], "KEEP"); self.assertEqual(a["decisions"]["I_max=0"], "ADOPT")

    def test_N_at_frozen_config_adopt_and_keep(self):
        self.build(0.45, 0.45)                       # bar 1/sqrt(3.85) = 0.510
        o = run(VN, [self.r], [self.c], os.path.join(self.t, "o"), "--baseline", "2500,1,0", "--knob", "N=10000 (m=1,I0):10000,1,0:up")
        self.assertEqual(o["decisions"]["N=10000 (m=1,I0)"], "ADOPT"); self.assertAlmostEqual(o["detail"]["N=10000 (m=1,I0)"]["cost_ratio"], 3.85, places=9)
        shutil.rmtree(self.t); self.setUp(); self.build(0.60, 0.60)
        self.assertEqual(run(VN, [self.r], [self.c], os.path.join(self.t, "o"), "--baseline", "2500,1,0", "--knob", "N=10000 (m=1,I0):10000,1,0:up")["decisions"]["N=10000 (m=1,I0)"], "KEEP")

    def test_registered_script_cannot_score_the_I0_N_arm_but_scores_the_I3_arm_verbatim(self):
        self.build(0.45, 0.45)
        o = run(REG, [self.r], [self.c], os.path.join(self.t, "o"))
        self.assertEqual(o["decisions"]["N=10000 (m=1)"], "ADOPT")              # the I_max = 3 N arm: verbatim registered rule
        self.assertNotIn("N=10000 (m=1,I0)", o["decisions"])
        shutil.rmtree(self.t); self.setUp(); self.build(0.45, 0.60)
        self.assertEqual(run(REG, [self.r], [self.c], os.path.join(self.t, "o"))["decisions"]["N=10000 (m=1)"], "KEEP")

    def test_cost_batch_file_is_skipped_and_identity_failure_is_incomplete(self):
        self.build(0.45, 0.45)
        json.dump({"batch": "x", "billed_core_h": 9.0}, open(os.path.join(self.c, "cost_batch.json"), "w"))     # no `stages` key: the registered script would raise KeyError
        k = ("--baseline", "2500,1,0", "--knob", "N=10000 (m=1,I0):10000,1,0:up")
        self.assertEqual(run(VN, [self.r], [self.c], os.path.join(self.t, "o"), *k)["decisions"]["N=10000 (m=1,I0)"], "ADOPT")
        p = os.path.join(self.r, "4-AR-n200-r01-P-N10000-m1-I0-c1-s1", "calib_meta.json"); j = json.load(open(p)); j["meta"]["N"] = 2500; json.dump(j, open(p, "w"))   # recorded N contradicts the plan arm
        o = run(VN, [self.r], [self.c], os.path.join(self.t, "o2"), *k)
        self.assertEqual(o["decisions"]["N=10000 (m=1,I0)"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
