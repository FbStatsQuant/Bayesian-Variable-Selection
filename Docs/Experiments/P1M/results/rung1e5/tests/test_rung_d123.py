#!/usr/bin/env python3
"""Self-test of rung_d123.py: the Student-t quantile against textbook values; D1 / D2 on synthetic records (PASS, D1 FAIL, D2 FAIL, an incomplete rung -> NOT_EVALUABLE, a wrong recorded arm
excluded); the Welch and bootstrap intervals against a hand computation; the continuity twin; a real G-B record parses. python3 -I tests/test_rung_d123.py (scratch: PREC_TEST_TMP or here, never /tmp)"""
import json, math, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); RG = os.path.dirname(HERE); SCRIPT = os.path.join(RG, "rung_d123.py")
sys.path.insert(0, RG)
import rung_d123 as R   # noqa: E402


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); os.makedirs(self.r)

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def mk(self, rid, pi, hpm_ok=True, N=10000, I=0, logZ=-230.0):
        d = os.path.join(self.r, rid); os.makedirs(d)
        json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
        json.dump({"status": "completed", "fit_status": "completed", "evidence": {"logZ": logZ}, "selection": {"hpm_eq_S0": hpm_ok, "F_S0": logZ + math.log(pi)},
                   "fit": {"meta": {"occ": [{"M": 1, "occ": pi}]}}}, open(os.path.join(d, "eval.bin.json"), "w"))
        json.dump({"meta": {"N": N, "refine_m": 1, "I_max": I, "rule": "bounded"}}, open(os.path.join(d, "calib_meta.json"), "w"))

    def rung(self, p200, p400, hpm200=(True,) * 5, hpm400=(True,) * 3):
        for i, (p, h) in enumerate(zip(p200, hpm200), 1):
            self.mk("5-AR-n200-r%02d-V-s1" % i, p, h)
        for i, (p, h) in enumerate(zip(p400, hpm400), 1):
            self.mk("5-AR-n400-r%02d-V-s1" % i, p, h)

    def go(self):
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", self.r, "--out", os.path.join(self.t, "o"), "--boot", "2000"], capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        return json.load(open(os.path.join(self.t, "o", "rung_d123.json")))

    def test_t_quantile(self):
        for df, q in ((2, 4.3027), (5, 2.5706), (10, 2.2281), (30, 2.0423)):
            self.assertAlmostEqual(R.t_quantile(0.975, df), q, places=3)

    def test_pass(self):
        self.rung([0.38, 0.40, 0.36, 0.42, 0.39], [0.45, 0.47, 0.43]); j = self.go()
        self.assertTrue(j["D1"]["PASS"]); self.assertTrue(j["D2"]["PASS"]); self.assertAlmostEqual(j["D2"]["mean_pi_hat_n200"], 0.39, places=12)
        x2 = [0.38, 0.40, 0.36, 0.42, 0.39]; x4 = [0.45, 0.47, 0.43]; m2 = sum(x2) / 5; m4 = sum(x4) / 3
        v2 = sum((v - m2) ** 2 for v in x2) / 4; v4 = sum((v - m4) ** 2 for v in x4) / 2; se = math.sqrt(v2 / 5 + v4 / 3)
        df = (v2 / 5 + v4 / 3) ** 2 / ((v2 / 5) ** 2 / 4 + (v4 / 3) ** 2 / 2); tq = R.t_quantile(0.975, df)
        self.assertAlmostEqual(j["D2"]["welch_95_ci"][0], (m4 - m2) - tq * se, places=12)
        lo, hi = j["D2"]["cluster_bootstrap_95_ci"]; self.assertTrue(lo < m4 - m2 < hi)

    def test_d1_fail(self):
        self.rung([0.38] * 5, [0.45] * 3, hpm200=(True, True, True, False, False)); self.assertFalse(self.go()["D1"]["PASS"])
        self.tearDown(); self.setUp(); self.rung([0.38] * 5, [0.45] * 3, hpm400=(True, True, False)); self.assertFalse(self.go()["D1"]["PASS"])
        self.tearDown(); self.setUp(); self.rung([0.38] * 5, [0.45] * 3, hpm200=(True, True, True, True, False)); self.assertTrue(self.go()["D1"]["PASS"])    # exactly 4/5 passes

    def test_d2_fail_no_tolerance(self):
        self.rung([0.40] * 5, [0.3999] * 3); j = self.go(); self.assertFalse(j["D2"]["PASS"])          # a tiny decrease fails: no tolerance
        self.tearDown(); self.setUp(); self.rung([0.40] * 5, [0.40] * 3); self.assertTrue(self.go()["D2"]["PASS"])   # equality passes (>=)

    def test_incomplete_and_wrong_arm(self):
        self.rung([0.38] * 5, [0.45] * 3); shutil.rmtree(os.path.join(self.r, "5-AR-n400-r03-V-s1")); self.assertTrue(self.go()["verdict"].startswith("NOT_EVALUABLE"))
        self.tearDown(); self.setUp(); self.rung([0.38] * 5, [0.45] * 3); self.mk("5-AR-n200-r06-V-s1", 0.2)
        self.tearDown(); self.setUp(); self.rung([0.38] * 4, [0.45] * 3); self.mk("5-AR-n200-r05-V-s1", 0.3, N=2500)
        j = self.go(); self.assertIn("5-AR-n200-r05-V-s1", j["excluded"]); self.assertTrue(j["verdict"].startswith("NOT_EVALUABLE"))

    def test_continuity(self):
        self.rung([0.38] * 5, [0.45] * 3); self.mk("5-AR-n200-r01-VN25-s1", 0.30, N=2500)
        c = self.go()["continuity_pi_hat_S0"][0]; self.assertAlmostEqual(c["difference_N10000_minus_N2500"], 0.08, places=12)

    def test_real_gb_record_incomplete(self):
        rec = os.path.expanduser("~/SMC_Engineering_Department/records/gb")
        if not os.path.isdir(rec):
            self.skipTest("records not present"); return
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", rec, "--out", os.path.join(self.t, "o")], capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        j = json.load(open(os.path.join(self.t, "o", "rung_d123.json")))
        self.assertTrue(j["verdict"].startswith("NOT_EVALUABLE: delivered AR fits n200 1 of 5, n400 0 of 3"), j["verdict"]); self.assertAlmostEqual(j["fits"]["200"]["5-AR-n200-r01-V-s1"]["pi_hat_S0"], 0.38654, places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
