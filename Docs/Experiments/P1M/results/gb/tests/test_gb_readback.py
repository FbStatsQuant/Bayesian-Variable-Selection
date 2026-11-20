#!/usr/bin/env python3
"""Self-test of gb_readback.py: synthetic records, a T5-shaped record (the measured T5 stage costs and RSS), the continuity-twin report, and a parse check on a REAL mini-leg eval
record (skipped if absent). python3 -I tests/test_gb_readback.py  (scratch under PREC_TEST_TMP or the tests dir, never /tmp)"""
import json, math, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); GB = os.path.dirname(HERE); SCRIPT = os.path.join(GB, "gb_readback.py")
F2 = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"
GIB = 2 ** 30
REAL = os.path.expanduser("~/SMC_Engineering_Department/records/vn_minileg/V0/4-AR-n200-r01-P-N10000-m1-c1-s1")


def run(args):
    p = subprocess.run([sys.executable, "-I", SCRIPT] + args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def mk(self, rid, N=10000, I=0, m1=0.01, m2=0.0004, m3=0.02, cost=None, rss=None, certified=True, logZ=-233.0, gap=0.0, hpm=(1, 2, 3), sha=F2, F_S0=-233.4, met=True, R=16):
        d = os.path.join(self.r, rid); os.makedirs(d)
        json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
        sig = m3
        ev = {"status": "completed", "fit_status": "completed", "binary": {"sha256": sha}, "evidence": {"logZ_r": [logZ] * R, "sigma_hat": sig, "logZ": logZ, "logZ_minus_logZ_T": 0.1, "logZ_occ": {"M1000": logZ + gap}},
              "selection": {"hpm": list(hpm), "hpm_eq_S0": True, "F_S0": F_S0}, "pip": {"island_spread": {"max_sd": m2, "target_met": met}, "eq_T_target_met": True, "max_abs_eq_minus_T": 0.003, "eq_T_target": 0.12,
                                                                                    "eq": {"sup_null": 0.01, "min_true": 0.99}},
              "fit": {"meta": {"local_certified": certified, "flags": {"E1": False, "E2": False, "E3": False, "low_empirical_ESS": False, "checks_passed_final": True, "occ_inhomogeneous": False},
                               "occ": [{"M": 1, "occ": 0.49, "sd_log_Z_occ_r": m1}, {"M": 1000, "sd_log_Z_occ_r": m1}], "mem_estimate": {"sacct_upper": 4 * GIB}}}}
        json.dump(ev, open(os.path.join(d, "eval.bin.json"), "w"))
        json.dump({"meta": {"N": N, "refine_m": 1, "I_max": I, "I_used": min(I, 3), "rule": "bounded", "flags": {"grid_unconverged": True}}}, open(os.path.join(d, "calib_meta.json"), "w"))
        if cost is not None:
            rss = rss or {}
            st = {s: {"billed_core_h": v, "wall_s_max": 60, "max_rss_bytes": int(rss.get(s, 1.0) * GIB), "states": ["COMPLETED"]} for s, v in cost.items()}
            json.dump({"run_id": rid, "stages": st}, open(os.path.join(self.c, "cost_%s.json" % rid), "w"))

    def go(self, extra=()):
        rc, so, se = run(["--records", self.r, "--cost-dir", self.c, "--out", os.path.join(self.t, "o")] + list(extra)); self.assertEqual(rc, 0, so + se)
        return json.load(open(os.path.join(self.t, "o", "gb_readback.json")))

    COST108 = {"setup": 0.41, "calibrate": 1.1, "islands": 105.9, "merge": 0.8, "eval": 0.07}

    def test_pass(self):
        self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, rss={"setup": 1.4, "calibrate": 8, "islands": 4.5, "merge": 6, "eval": 2})
        rj = os.path.join(self.t, "rule.json"); json.dump({"outcome": "PASS"}, open(rj, "w"))
        j = self.go(["--rule", rj]); f = j["fits"]["5-AR-n200-r01-V-s1"]
        self.assertEqual(f["C1"]["verdict"], "OK"); self.assertEqual(f["C2"]["verdict"], "PASS"); self.assertEqual(f["C3"]["verdict"], "PASS"); self.assertEqual(j["G-B"]["G-B"], "PASS")
        self.assertAlmostEqual(f["science"]["pi_hat_S0"], math.exp(-233.4 + 233.0), places=12)

    def test_c1_soft_and_hard(self):
        for scale, want in ((1.6, "SOFT"), (2.6, "HARD")):
            self.tearDown(); self.setUp()
            self.mk("5-AR-n200-r01-V-s1", cost={k: v * scale for k, v in self.COST108.items()})
            j = self.go(); self.assertEqual(j["fits"]["5-AR-n200-r01-V-s1"]["C1"]["verdict"], want)
            self.assertNotEqual(j["G-B"]["G-B"], "PASS")
        self.assertTrue(j["G-B"]["G-B"].startswith("STOP"))

    def test_c2_fail_and_not_evaluated(self):
        self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, m2=0.006, met=False); self.assertEqual(self.go()["fits"]["5-AR-n200-r01-V-s1"]["C2"]["verdict"], "FAIL")
        self.tearDown(); self.setUp(); self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, gap=1.0, m3=0.02)     # |logZ - logZ_occ| = 1 >> 3 se
        self.assertEqual(self.go()["fits"]["5-AR-n200-r01-V-s1"]["C2"]["verdict"], "FAIL")
        self.tearDown(); self.setUp(); self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, certified=None)
        self.assertEqual(self.go()["fits"]["5-AR-n200-r01-V-s1"]["C2"]["verdict"], "NOT_EVALUATED")

    def test_c3_advisory_and_fail(self):
        self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, rss={"merge": 20.5}); self.assertEqual(self.go()["fits"]["5-AR-n200-r01-V-s1"]["C3"]["verdict"], "ADVISORY")   # 85 % of 24 G
        self.tearDown(); self.setUp(); self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, rss={"islands": 12.0}); j = self.go()
        self.assertEqual(j["fits"]["5-AR-n200-r01-V-s1"]["C3"]["verdict"], "FAIL"); self.assertNotEqual(j["G-B"]["G-B"], "PASS")

    def test_t5_shaped(self):
        """T5 (results/T5_1e5.md): setup 0.41, calibrate 10.56, islands 28.10, merge 0.74, eval 0.07 = 39.88 billed (N 2,500, I_max 3); peak RSS islands 4.5 GB, calibrate 11 GB."""
        self.mk("5-AR-n200-r01-V-s1", N=2500, I=3, cost={"setup": 0.41, "calibrate": 10.56, "islands": 28.10, "merge": 0.74, "eval": 0.07},
                rss={"setup": 1.4, "calibrate": 11e9 / GIB, "islands": 4.5e9 / GIB, "merge": 3.0, "eval": 1.0})
        f = self.go(["--branch", "pass"])["fits"]["5-AR-n200-r01-V-s1"]
        self.assertEqual(f["C1"]["model_E"], 40); self.assertAlmostEqual(f["C1"]["billed"], 39.88, places=6); self.assertEqual(f["C1"]["verdict"], "OK")
        self.assertEqual(f["C3"]["verdict"], "PASS"); self.assertAlmostEqual(f["C3"]["max_pct"], 100 * 11e9 / GIB / 16, places=6)

    def test_continuity_twin(self):
        self.mk("5-AR-n200-r01-V-s1", cost=self.COST108, logZ=-233.0, m1=0.007, m2=0.0002, m3=0.011)
        self.mk("5-AR-n200-r01-VN25-s1", N=2500, I=0, cost={"setup": 0.41, "calibrate": 1.1, "islands": 28.1, "merge": 0.74, "eval": 0.07}, logZ=-233.01, m1=0.014, m2=0.0004, m3=0.022)
        c = self.go()["continuity_twins"][0]
        self.assertTrue(c["hpm_equal"]); self.assertAlmostEqual(c["dlogZ(N1e4 - N2500)"], 0.01, places=9); self.assertAlmostEqual(c["f_billed_islands"], 105.9 / 28.1, places=9)
        self.assertAlmostEqual(c["r_N(M1,M2,M3)"][0], 0.5, places=9)

    def test_real_record_parse(self):
        if not os.path.isdir(REAL):
            self.skipTest("record not present"); return
        rc, so, se = run(["--records", REAL, "--cost-dir", os.path.join(os.path.dirname(REAL), "_batch_VN_V0_1", "cost"), "--out", os.path.join(self.t, "o"), "--id-regex", r"^4-AR-n200-r01-P-N10000-m1-c1-s1$"])
        self.assertEqual(rc, 0, so + se)
        f = json.load(open(os.path.join(self.t, "o", "gb_readback.json")))["fits"]["4-AR-n200-r01-P-N10000-m1-c1-s1"]
        self.assertAlmostEqual(f["C2"]["M1"], 0.006880036947792842, places=12); self.assertAlmostEqual(f["C2"]["M2"], 0.00024041574483946892, places=12)
        self.assertAlmostEqual(f["C2"]["M3"], 0.01341427854270742, places=12); self.assertTrue(f["C2"]["evidence_consistent"]); self.assertTrue(f["C2"]["local_certified"])
        self.assertAlmostEqual(f["science"]["pi_hat_S0"], math.exp(-177.9723069625954 + 177.25803035338768), places=12); self.assertEqual(f["R'"], 64)
        self.assertEqual(f["recorded_arm"]["N"], 10000); self.assertAlmostEqual(f["stages"]["merge"]["max_rss_gib"], 1709342720 / GIB, places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
