#!/usr/bin/env python3
"""Self-test of gc_readback.py: the 1M class table, the G-C2 pilot verdict (PASS; identity FAIL; cost over the hard line -> STOP; a kill-rule trip -> STOP; memory FAIL), and a parse check on the REAL
11-17 1M record (records/F1M_pilot: M1 0.0171, M2 0.0029, HPM = S0, I_max 3 from calib.bin.json). python3 -I tests/test_gc_readback.py (scratch: PREC_TEST_TMP or here, never /tmp)"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); GC = os.path.dirname(HERE); SCRIPT = os.path.join(GC, "gc_readback.py")
F2 = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; GIB = 2 ** 30
REAL = os.path.expanduser("~/SMC_Engineering_Department/records/F1M_pilot")
PILOT = "6-AR-n200-r01-V-s1"


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def mk(self, rid=PILOT, N=2500, I=0, cost=(15.25, 24.0, 269.25, 17.0, 0.4), rss=(14, 55, 30, 40, 2), m2=0.003, met=True, merge_peak_kb=26 * 2 ** 20, state="COMPLETED", setup_peak_mb=13546.0):
        d = os.path.join(self.r, rid); os.makedirs(d)
        json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
        json.dump({"status": "completed", "fit_status": "completed", "binary": {"sha256": F2}, "evidence": {"logZ_r": [-245.0] * 16, "sigma_hat": 0.03, "logZ": -245.0, "logZ_occ": {"M1000": -245.0}},
                   "selection": {"hpm": [1, 2], "hpm_eq_S0": True, "F_S0": -245.9}, "pip": {"island_spread": {"max_sd": m2, "target_met": met}, "eq_T_target_met": True, "max_abs_eq_minus_T": 0.003, "eq_T_target": 0.2},
                   "fit": {"meta": {"local_certified": True, "flags": {"E2": False}, "occ": [{"M": 1, "occ": 0.4}, {"M": 1000, "sd_log_Z_occ_r": 0.017}]}}}, open(os.path.join(d, "eval.bin.json"), "w"))
        json.dump({"meta": {"N": N, "refine_m": 1, "I_max": I, "I_used": 0, "rule": "bounded"}}, open(os.path.join(d, "calib_meta.json"), "w"))
        json.dump({"peak_rss_kb": merge_peak_kb}, open(os.path.join(d, "fit.bin.json"), "w")); json.dump({"peak_rss_mb": setup_peak_mb}, open(os.path.join(d, "setup.bin.json"), "w"))
        st = {s: {"billed_core_h": v, "wall_s_max": 700 if s == "islands" else 100, "max_rss_bytes": int(g * GIB), "states": [state if s == "merge" else "COMPLETED"]} for s, v, g in zip(("setup", "calibrate", "islands", "merge", "eval"), cost, rss)}
        json.dump({"run_id": rid, "stages": st}, open(os.path.join(self.c, "cost_%s.json" % rid), "w"))

    def ident(self, ok=True):
        p = os.path.join(self.t, "id.json"); json.dump({"IDENTITY": "PASS" if ok else "FAIL"}, open(p, "w")); return p

    def go(self, args=()):
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", self.r, "--cost-dir", self.c, "--out", os.path.join(self.t, "o")] + list(args), capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        return json.load(open(os.path.join(self.t, "o", "gc_readback.json")))

    def test_pilot_pass(self):
        self.mk(); j = self.go(["--identity", self.ident()]); p = j["pilot"]; self.assertEqual(p["G-C2"], "PASS"); self.assertAlmostEqual(j["fits"][PILOT]["C1"]["billed"], 325.9, places=1)
        self.assertEqual(j["fits"][PILOT]["C1"]["model_E"], 326); self.assertAlmostEqual(j["fits"][PILOT]["C3"]["merge_process_peak_gib"], 26.0, places=6)

    def test_identity_fail_and_missing(self):
        self.mk(); self.assertTrue(self.go(["--identity", self.ident(False)])["pilot"]["G-C2"].startswith("NOT_PASSED: identity"))
        self.assertTrue(self.go()["pilot"]["G-C2"].startswith("NOT_PASSED"))     # no identity record -> not passed

    def test_soft_is_not_pass_and_hard_is_stop(self):
        self.mk(cost=(15.25, 24.0, 520.0, 17.0, 0.4)); j = self.go(["--identity", self.ident()]); self.assertEqual(j["fits"][PILOT]["C1"]["verdict"], "SOFT"); self.assertTrue(j["pilot"]["G-C2"].startswith("NOT_PASSED: C1"))
        self.tearDown(); self.setUp(); self.mk(cost=(15.25, 24.0, 800.0, 17.0, 0.4)); j = self.go(["--identity", self.ident()]); self.assertEqual(j["fits"][PILOT]["C1"]["verdict"], "HARD"); self.assertTrue(j["pilot"]["G-C2"].startswith("STOP"))

    def test_kill_rule(self):
        self.mk(cost=(15.25, 40.0, 269.25, 17.0, 0.4)); j = self.go(["--identity", self.ident()]); self.assertFalse(j["fits"][PILOT]["kill"]["trip"])      # 40 < 2 x 24 = 48: no trip (was a trip at the old 2 x 16)
        self.tearDown(); self.setUp(); self.mk(cost=(15.25, 55.0, 269.25, 17.0, 0.4)); j = self.go(["--identity", self.ident()]); self.assertTrue(j["fits"][PILOT]["kill"]["trip"]); self.assertTrue(j["pilot"]["G-C2"].startswith("STOP"))

    def test_memory_process_basis_and_precision_fail(self):
        # sacct counts page cache: a merge at 130 GiB sacct but a 26 GiB process, COMPLETED, is ADVISORY, not FAIL
        self.mk(rss=(14, 55, 30, 130, 2)); j = self.go(["--identity", self.ident()]); self.assertEqual(j["fits"][PILOT]["C3"]["verdict"], "ADVISORY"); self.assertEqual(j["pilot"]["G-C2"], "PASS")
        # a process peak at the request FAILS
        self.tearDown(); self.setUp(); self.mk(merge_peak_kb=130 * 2 ** 20); j = self.go(["--identity", self.ident()]); self.assertEqual(j["fits"][PILOT]["C3"]["verdict"], "FAIL"); self.assertTrue(j["pilot"]["G-C2"].startswith("NOT_PASSED: C3"))
        # an OUT_OF_MEMORY stage FAILS
        self.tearDown(); self.setUp(); self.mk(state="OUT_OF_MEMORY"); self.assertEqual(self.go(["--identity", self.ident()])["fits"][PILOT]["C3"]["verdict"], "FAIL")
        self.tearDown(); self.setUp(); self.mk(m2=0.006, met=False); self.assertTrue(self.go(["--identity", self.ident()])["pilot"]["G-C2"].startswith("NOT_PASSED: C2"))

    def test_option_d_requests(self):
        # eval at n = 1,000 reads an 8 GB data.bin: 20 GiB sacct is 62 % of the D request (32 G) and would exceed the pilot's 16 G
        self.mk("6-AR-n1000-r01-V-s1", cost=(55.0, 30.0, 700.0, 22.0, 1.0), rss=(30, 80, 45, 60, 20)); c3 = self.go()["fits"]["6-AR-n1000-r01-V-s1"]["C3"]
        self.assertEqual((c3["requests_gib"]["eval"], c3["requests_gib"]["setup"]), (32, 64)); self.assertEqual(c3["verdict"], "PASS")

    def test_class_table(self):
        self.mk("6-ADJOPP-n200-r01-V-s1", cost=(15.25, 16.0, 290.0, 17.0, 0.4)); self.mk("6-AR-n200-r01-VN10K-s1", N=10000, cost=(15.25, 16.0, 700.0, 17.0, 0.4)); self.mk("6-AR-n1000-r01-V-s1", cost=(50.0, 20.0, 900.0, 17.0, 0.4))
        j = self.go()["fits"]
        self.assertEqual((j["6-ADJOPP-n200-r01-V-s1"]["C1"]["model_E"], j["6-AR-n200-r01-VN10K-s1"]["C1"]["model_E"], j["6-AR-n1000-r01-V-s1"]["C1"]["model_E"]), (339, 783, 1087))

    def test_real_11_17_record_parse(self):
        if not os.path.isdir(REAL):
            self.skipTest("records not present"); return
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", os.path.dirname(REAL), "--out", os.path.join(self.t, "o")], capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        f = json.load(open(os.path.join(self.t, "o", "gc_readback.json")))["fits"][PILOT]
        self.assertAlmostEqual(f["C2"]["M1"], 0.0171029525813884, places=12); self.assertAlmostEqual(f["C2"]["M2"], 0.0029046438757469755, places=12); self.assertTrue(f["science"]["hpm_eq_S0"])
        self.assertEqual((f["recorded_arm"]["N"], f["recorded_arm"]["I"]), (2500, 3)); self.assertTrue(f["C2"]["evidence_consistent"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
