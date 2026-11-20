#!/usr/bin/env python3
"""Self-test of rung_readback.py: the rung C1 class table, completion count (>= 11 of 12), the T6 check (synthetic t6.json: PASS, a hash mismatch, a failed kill check), and the REAL G-B records
(AR r01 and ADJ-OPP r01 pilots: C1 OK against the rung models). python3 -I tests/test_rung_readback.py (scratch: PREC_TEST_TMP or here, never /tmp)"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); RG = os.path.dirname(HERE); SCRIPT = os.path.join(RG, "rung_readback.py")
F2 = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; GIB = 2 ** 30
REAL = os.path.expanduser("~/SMC_Engineering_Department/records/gb")


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def mk(self, rid, cost, N=10000, I=0):
        d = os.path.join(self.r, rid); os.makedirs(d)
        json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
        json.dump({"status": "completed", "fit_status": "completed", "binary": {"sha256": F2}, "evidence": {"logZ_r": [-230.0] * 16, "sigma_hat": 0.02, "logZ": -230.0, "logZ_occ": {"M1000": -230.0}},
                   "selection": {"hpm": [1, 2], "hpm_eq_S0": True, "F_S0": -230.9}, "pip": {"island_spread": {"max_sd": 0.0004, "target_met": True}, "eq_T_target_met": True},
                   "fit": {"meta": {"local_certified": True, "flags": {"E2": False}, "occ": [{"M": 1, "occ": 0.4}, {"M": 1000, "sd_log_Z_occ_r": 0.01}]}}}, open(os.path.join(d, "eval.bin.json"), "w"))
        json.dump({"meta": {"N": N, "refine_m": 1, "I_max": I, "I_used": 0, "rule": "bounded"}}, open(os.path.join(d, "calib_meta.json"), "w"))
        st = {s: {"billed_core_h": v, "wall_s_max": 60, "max_rss_bytes": int(1.0 * GIB), "states": ["COMPLETED"]} for s, v in zip(("setup", "calibrate", "islands", "merge", "eval"), cost)}
        json.dump({"run_id": rid, "stages": st}, open(os.path.join(self.c, "cost_%s.json" % rid), "w"))

    def go(self, extra=()):
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", self.r, "--cost-dir", self.c, "--out", os.path.join(self.t, "o")] + list(extra), capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        return json.load(open(os.path.join(self.t, "o", "rung_readback.json")))

    def full_rung(self, scale=1.0):
        from rung_readback import RUNG_IDS
        for rid in RUNG_IDS:
            self.mk(rid, [0.5, 1.5, 73.0 * scale, 0.8, 0.07])

    def t6(self, fh="0xabc", rh="0xabc", ok=True, extra_check=True):
        p = os.path.join(self.t, "t6.json")
        json.dump({"ok": ok, "checks": {"kill_1_sigkill": True, "kill_2_sigkill": True, "output_hash_equal": extra_check}, "kills": [{"kill": 1, "kind": "second_ckpt", "returncode": -9, "killed": True, "island_file_exists": False},
                   {"kill": 2, "kind": "during_write", "returncode": -9, "killed": True, "island_file_exists": False}], "final": {"output_hash": fh, "resumed_from_step": 12, "wall_s": 200}, "reference": {"output_hash": rh, "wall_s": 440}}, open(p, "w"))
        return p

    def test_models_and_completion(self):
        sys.path.insert(0, RG); self.full_rung(); j = self.go()
        self.assertEqual(j["rung"]["completion"]["rung_fits_delivered"], 12); self.assertTrue(j["rung"]["completion"]["PASS"]); self.assertEqual(j["rung"]["C1_hard_trips"], [])
        self.assertEqual(j["fits"]["5-AR-n400-r01-V-s1"]["C1"]["model_E"], 76); self.assertEqual(j["fits"]["5-ADJOPP-n200-r02-V-s1"]["C1"]["model_E"], 66)
        self.tearDown(); self.setUp(); self.full_rung(scale=2.0); j = self.go()
        self.assertTrue(len(j["rung"]["C1_soft_trips"]) + len(j["rung"]["C1_hard_trips"]) > 0)       # 2x islands (150) > soft 114 for AR, > 99 for ADJ-OPP
        self.tearDown(); self.setUp(); self.full_rung(scale=3.0); self.assertIn("5-AR-n200-r01-V-s1", self.go()["rung"]["C1_hard_trips"])   # 219 > hard 190

    def test_completion_threshold(self):
        sys.path.insert(0, RG)
        from rung_readback import RUNG_IDS
        for rid in RUNG_IDS[:10]:
            self.mk(rid, [0.5, 1.5, 73.0, 0.8, 0.07])
        j = self.go(); self.assertFalse(j["rung"]["completion"]["PASS"]); self.assertEqual(len(j["rung"]["completion"]["missing"]), 2)
        self.mk(RUNG_IDS[10], [0.5, 1.5, 73.0, 0.8, 0.07]); self.assertTrue(self.go()["rung"]["completion"]["PASS"])     # 11 of 12 passes

    def test_t6(self):
        self.mk("5-AR-n200-r01-V-s1", [0.5, 1.5, 73.0, 0.8, 0.07])
        self.assertTrue(self.go(["--t6", self.t6(), "--t6-ref-hash", "0xabc"])["t6"]["PASS"])
        self.assertFalse(self.go(["--t6", self.t6(fh="0xdef"), "--t6-ref-hash", "0xabc"])["t6"]["PASS"])       # resumed != reference
        self.assertFalse(self.go(["--t6", self.t6(), "--t6-ref-hash", "0x999"])["t6"]["PASS"])                  # == reference but != the fit's own island 1
        self.assertFalse(self.go(["--t6", self.t6(ok=False), "--t6-ref-hash", "0xabc"])["t6"]["PASS"])          # a failed p1m_t6 check
        self.assertTrue(self.go(["--t6", self.t6(), "--t6-ref-hash", ""])["t6"]["PASS"])                         # fallback source: no third equality

    def test_real_gb_pilots(self):
        if not os.path.isdir(REAL):
            self.skipTest("records not present"); return
        cd = os.path.join(self.t, "cost"); os.makedirs(cd)
        for f in __import__("glob").glob(os.path.join(REAL, "*", "_batch_*", "cost", "cost_5-*.json")):
            os.symlink(f, os.path.join(cd, os.path.basename(f)))
        rc = subprocess.run([sys.executable, "-I", SCRIPT, "--records", REAL, "--cost-dir", cd, "--out", os.path.join(self.t, "o")], capture_output=True, text=True); self.assertEqual(rc.returncode, 0, rc.stderr)
        j = json.load(open(os.path.join(self.t, "o", "rung_readback.json")))
        a, d = j["fits"]["5-AR-n200-r01-V-s1"]["C1"], j["fits"]["5-ADJOPP-n200-r01-V-s1"]["C1"]
        self.assertEqual((a["verdict"], d["verdict"]), ("OK", "OK")); self.assertAlmostEqual(a["billed"], 76.39, delta=0.01); self.assertAlmostEqual(d["billed"], 65.65, delta=0.01)
        self.assertEqual(j["rung"]["completion"]["rung_fits_delivered"], 2)


if __name__ == "__main__":
    sys.path.insert(0, RG)
    unittest.main(verbosity=2)
