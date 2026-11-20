#!/usr/bin/env python3
"""Self-test of gb_imax_rule.py. python3 -I tests/test_gb_imax_rule.py   (scratch under PREC_TEST_TMP or the tests dir, never /tmp).
(1) GOLDEN on the leg's REAL FZ records (needs ~/SMC_Engineering_Department/records/precision1e4; skipped with a message if absent): --ids precision --N 2500 --reps 2
    reproduces results/precision1e4/fz/freeze.json decisions['I_max=0'] = ADOPT -> PASS and its ratios to 1e-12.
(2) SYNTHETIC gb ids: PASS; FAIL on each of M1, M2, M3; FAIL on HPM; n = 1 (1.15 binds even at 1.20 < 1.30) and n = 2 (gmean vs per-dataset bar); NOT_EVALUATED (zero denominator,
    missing arm); INCOMPLETE (arm mismatch, no calibration record)."""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); GB = os.path.dirname(HERE); SCRIPT = os.path.join(GB, "gb_imax_rule.py")
REC = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4")
FZ = os.path.join(os.path.dirname(GB), "precision1e4", "fz", "freeze.json")


def run(args):
    p = subprocess.run([sys.executable, "-I", SCRIPT] + args, capture_output=True, text=True)
    return p.returncode, p.stdout


def mk(root, ds, arm, m1, m2, m3, N=10000, hpm=(1, 2, 3), rec=None, meta=True):
    rid = "5-%s-n200-r01-%s-s1" % (ds, arm); d = os.path.join(root, rid); os.makedirs(d)
    I = 0 if arm == "V" else 3
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": "completed", "fit_status": "completed", "evidence": {"sigma_hat": m3, "sigma_hat_robust": m3, "logZ": -233.0}, "selection": {"hpm": list(hpm)},
               "pip": {"island_spread": {"max_sd": m2, "target_met": True}}, "fit": {"meta": {"occ": [{"M": 1000, "sd_log_Z_occ_r": m1}], "flags": {"occ_inhomogeneous": False, "E2": False}}}},
              open(os.path.join(d, "eval.bin.json"), "w"))
    if meta:
        n, m, i = rec or (N, 1, I)
        json.dump({"meta": {"N": n, "refine_m": m, "I_max": i, "I_used": min(i, 3), "rule": "bounded", "flags": {"grid_unconverged": True}}}, open(os.path.join(d, "calib_meta.json"), "w"))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); os.makedirs(self.r)

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def pair(self, ds, r1=1.0, r2=1.0, r3=1.0, hpm0=(1, 2, 3), **kw):
        mk(self.r, ds, "VI3", 0.01, 0.0005, 0.02, **kw)
        mk(self.r, ds, "V", 0.01 * r1, 0.0005 * r2, 0.02 * r3, hpm=hpm0, **kw)

    def out(self, args=()):
        rc, so = run(["--records", self.r, "--N", "10000", "--out", os.path.join(self.t, "o")] + list(args)); self.assertEqual(rc, 0, so)
        return json.loads(so)

    def test_golden_real_fz_records(self):
        if not os.path.isdir(os.path.join(REC, "P1")):
            self.skipTest("records not present"); return
        rc, so = run(["--records"] + [os.path.join(REC, x) for x in ("A0", "P1", "P2", "P3", "P4")] + ["--N", "2500", "--reps", "2", "--ids", "precision", "--out", os.path.join(self.t, "g")])
        self.assertEqual(rc, 0, so); j = json.loads(so)
        ref = json.load(open(FZ))
        self.assertEqual(ref["decisions"]["I_max=0"], "ADOPT"); self.assertEqual(j["outcome"], "PASS")
        for k in ("M1", "M2", "M3"):
            self.assertAlmostEqual(j["ratios"][k], ref["detail"]["I_max=0"]["ratios"][k]["geo_mean"], places=12)
            for d, v in ref["detail"]["I_max=0"]["ratios"][k]["per_dataset"].items():
                self.assertAlmostEqual(j["per_dataset"][k][d], v, places=12)

    def test_pass_n1_and_n2(self):
        self.pair("AR", 1.0, 1.0, 1.10); self.assertEqual(self.out()["outcome"], "PASS")
        self.pair("ADJOPP", 1.0, 1.0, 1.05); j = self.out(); self.assertEqual(j["outcome"], "PASS"); self.assertEqual(j["datasets"], ["ADJOPP", "AR"])

    def test_fail_each_metric_n1_bar_is_115(self):
        for k, args in (("M1", (1.20, 1, 1)), ("M2", (1, 1.20, 1)), ("M3", (1, 1, 1.20))):
            self.tearDown(); self.setUp(); self.pair("AR", *args); self.assertEqual(self.out()["outcome"], "FAIL", k)

    def test_n2_geomean_vs_per_dataset(self):
        self.pair("AR", 1, 1, 0.90); self.pair("ADJOPP", 1, 1, 1.28)         # gmean 1.074 <= 1.15 and 1.28 <= 1.30 -> PASS
        self.assertEqual(self.out()["outcome"], "PASS")
        self.tearDown(); self.setUp(); self.pair("AR", 1, 1, 0.80); self.pair("ADJOPP", 1, 1, 1.35)   # gmean 1.039 but 1.35 > 1.30 -> FAIL
        self.assertEqual(self.out()["outcome"], "FAIL")
        self.tearDown(); self.setUp(); self.pair("AR", 1, 1, 1.14); self.pair("ADJOPP", 1, 1, 1.25)   # each <= 1.30 but gmean 1.1936 > 1.15 -> FAIL
        self.assertEqual(self.out()["outcome"], "FAIL")

    def test_hpm_mismatch_fails(self):
        self.pair("AR", hpm0=(1, 2, 4)); self.assertEqual(self.out()["outcome"], "FAIL")

    def test_not_evaluated(self):
        mk(self.r, "AR", "VI3", 0.01, 0.0, 0.02); mk(self.r, "AR", "V", 0.01, 0.0005, 0.02)      # M2 denominator 0
        self.assertEqual(self.out()["outcome"], "NOT_EVALUATED")
        self.tearDown(); self.setUp(); mk(self.r, "AR", "V", 0.01, 0.0005, 0.02)                    # twin missing
        self.assertEqual(self.out()["outcome"], "NOT_EVALUATED")

    def test_incomplete(self):
        self.pair("AR", rec=(2500, 1, 0)); self.assertEqual(self.out()["outcome"], "INCOMPLETE")      # recorded N 2500 != plan 10000
        self.tearDown(); self.setUp(); self.pair("AR", meta=False); self.assertEqual(self.out()["outcome"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
