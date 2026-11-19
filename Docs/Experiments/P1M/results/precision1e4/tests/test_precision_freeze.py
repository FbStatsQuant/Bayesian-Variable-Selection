#!/usr/bin/env python3
"""Self-test of precision_freeze.py on SYNTHETIC records. python3 -I tests/test_precision_freeze.py"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); SCRIPT = os.path.join(os.path.dirname(HERE), "precision_freeze.py")
DS = ("AR", "ARweak", "ADJOPP")


def mk(root, cdir, ds, tag, m1, m2, m3, isl, hpm=(1, 2, 3)):
    rid = "4-%s-n200-r01-P-%s-s1" % (ds, tag); d = os.path.join(root, rid); os.makedirs(d)
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": "completed", "fit_status": "completed", "evidence": {"sigma_hat": m3}, "selection": {"hpm": list(hpm)}, "pip": {"island_spread": {"max_sd": m2, "target_met": m2 <= 0.005}},
               "fit": {"meta": {"occ": [{"M": 1000, "sd_log_Z_occ_r": m1}], "flags": {"occ_inhomogeneous": False}}}}, open(os.path.join(d, "eval.bin.json"), "w"))
    json.dump({"run_id": rid, "stages": {"islands": {"billed_core_h": isl}}}, open(os.path.join(cdir, "cost_%s.json" % rid), "w"))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t)

    def build(self, m4_ratio, i0_ratio, m4_cost=2.0, hpm_bad=False):
        for ds in DS:
            for c in (1, 2):
                mk(self.r, self.c, ds, "N2500-m1-c%d" % c, 0.02, 0.0004, 0.025, 1.0)
                mk(self.r, self.c, ds, "N2500-m4-c%d" % c, 0.02 * m4_ratio, 0.0004 * m4_ratio, 0.025 * m4_ratio, m4_cost, hpm=((1, 2, 4) if hpm_bad and ds == "AR" else (1, 2, 3)))
                mk(self.r, self.c, ds, "N2500-m1-I0-c%d" % c, 0.02 * i0_ratio, 0.0004 * i0_ratio, 0.025 * i0_ratio, 1.0)

    def run_(self):
        o = os.path.join(self.t, "o")
        r = subprocess.run([sys.executable, "-I", SCRIPT, "--records", self.r, "--cost-dir", self.c, "--out", o], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        return json.load(open(os.path.join(o, "freeze.json")))

    def test_adopt_when_gain_beats_extra_islands(self):
        self.build(0.6, 1.05, 2.0); d = self.run_()["decisions"]               # limit 1/sqrt(2) = 0.707 >= 0.6
        self.assertEqual(d["m=4"], "ADOPT"); self.assertEqual(d["I_max=0"], "ADOPT"); self.assertEqual(d["N=10000 (m=1)"], "NOT_RUN"); self.assertIn("OFF", d["resampling"])

    def test_keep_when_gain_is_small_or_cost_large(self):
        self.build(0.8, 1.4, 2.0); d = self.run_()["decisions"]                # 0.8 > 0.707; I_max=0 is 40% worse
        self.assertEqual(d["m=4"], "KEEP"); self.assertEqual(d["I_max=0"], "KEEP")
        shutil.rmtree(self.t); self.setUp(); self.build(0.6, 1.0, 4.0); self.assertEqual(self.run_()["decisions"]["m=4"], "KEEP")   # cost x4 needs r <= 0.5

    def test_hpm_disagreement_blocks_adoption(self):
        self.build(0.5, 1.0, 2.0, hpm_bad=True); self.assertEqual(self.run_()["decisions"]["m=4"], "KEEP")


if __name__ == "__main__":
    unittest.main(verbosity=2)
