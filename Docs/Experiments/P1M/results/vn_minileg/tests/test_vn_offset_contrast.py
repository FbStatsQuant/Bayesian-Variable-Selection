#!/usr/bin/env python3
"""Self-test of vn_offset_contrast.py on SYNTHETIC records: its I_max = 3 contrast must equal the registered precision_offset.py's own N contrast. python3 -I tests/test_vn_offset_contrast.py"""
import json, math, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); VC = os.path.join(os.path.dirname(HERE), "vn_offset_contrast.py")
REG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "precision1e4", "precision_offset.py")


def lse(xs):
    m = max(xs); return m + math.log(sum(math.exp(x - m) for x in xs))


def mk(root, rid, Rp, lr, cell=None, arm="V"):
    d = os.path.join(root, rid); os.makedirs(d)
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": "completed", "fit_status": "completed", "evidence": {"logZ_r": lr, "logZ": lse(lr) - math.log(Rp)}, "fit": {"meta": {"Rp": Rp, "tier": 0, "N": 2500, "occ": []}}}, open(os.path.join(d, "eval.bin.json"), "w"))
    if arm == "V":
        json.dump({"tier_final": 0, "settings": {"rule": "bounded", "refine_m": cell[1], "I_max": cell[2], "tiers": [{"N_final": cell[0]}]}}, open(os.path.join(d, "calib.bin.json"), "w"))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.root = os.path.join(self.t, "rec"); os.makedirs(self.root)

    def tearDown(self):
        shutil.rmtree(self.t)

    def test_I3_contrast_equals_registered_and_frozen_pair_is_computed(self):
        base = {"AR": -177.0, "ARweak": -150.0, "ADJOPP": -220.0}; shift = {"AR": 0.003, "ARweak": 0.005, "ADJOPP": 0.001}
        for ds, b in base.items():
            for s, e in ((1, 0.01), (2, -0.01)):
                mk(self.root, "4-%s-n200-r01-T-s%d" % (ds, s), 4, [b + e] * 4, arm="T")
            for c in (1, 2):
                for I in (0, 3):
                    tag = lambda N: "P-N%d-m1%s-c%d-s1" % (N, "-I0" if I == 0 else "", c)
                    mk(self.root, "4-%s-n200-r01-%s" % (ds, tag(2500)), 64, [b - 0.006 + 0.0005 * c] * 64, cell=(2500, 1, I))
                    mk(self.root, "4-%s-n200-r01-%s" % (ds, tag(10000)), 64, [b - 0.006 + 0.0005 * c + shift[ds]] * 64, cell=(10000, 1, I))
        o = os.path.join(self.t, "o")
        r = subprocess.run([sys.executable, "-I", REG, "--records", self.root, "--out", o], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        reg = {c["contrast"]: c for c in json.load(open(os.path.join(o, "offset.json")))["contrasts"]}
        n3 = reg["N: (10000,1,3) - (2500,1,3) at k=64"]
        v = os.path.join(self.t, "v")
        r = subprocess.run([sys.executable, "-I", VC, "--per-fit", os.path.join(o, "offset_per_fit.csv"), "--out", v], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        out = {c["pair"]: c for c in json.load(open(os.path.join(v, "vn_offset_contrast.json")))["contrasts"]}
        c3 = out["10000,1,3:2500,1,3"]["contrast"]; c0 = out["10000,1,0:2500,1,0"]["contrast"]
        self.assertAlmostEqual(c3["mean"], n3["mean"], places=8); self.assertAlmostEqual(c3["lo"], n3["lo95"], places=6); self.assertAlmostEqual(c3["hi"], n3["hi95"], places=6)
        self.assertAlmostEqual(c0["mean"], 0.003, places=9)                                   # (0.003 + 0.005 + 0.001) / 3
        self.assertAlmostEqual(out["10000,1,0:2500,1,0"]["H_N_prediction"], 0.75 * 0.006 - 0.75 * 0.0005 * 1.5, places=9)
        self.assertEqual(out["10000,1,0:2500,1,0"]["H0_by_CI"], "not excluded")      # t(2) half-width 0.0050 > 0.003


if __name__ == "__main__":
    unittest.main(verbosity=2)
