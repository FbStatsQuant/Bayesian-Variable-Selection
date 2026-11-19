#!/usr/bin/env python3
"""Self-test of precision_freeze.py on SYNTHETIC records. python3 -I tests/test_precision_freeze.py  (scratch under PREC_TEST_TMP or the tests dir, never /tmp)"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); SCRIPT = os.path.join(os.path.dirname(HERE), "precision_freeze.py")
DS = ("AR", "ARweak", "ADJOPP")


def mk(root, cdir, ds, tag, m1, m2, m3, isl, hpm=(1, 2, 3), rec=None, how="meta"):
    """rec = the RECORDED arm (N, m, I_max); default = the arm named by the tag. how: meta (calib_meta.json) | settings (calib.bin.json) | none"""
    rid = "4-%s-n200-r01-P-%s-s1" % (ds, tag); d = os.path.join(root, rid); os.makedirs(d)
    if rec is None:
        import re
        g = re.match(r"N(\d+)-m(\d+)(?:-I(\d))?-c\d", tag).groups(); rec = (int(g[0]), int(g[1]), int(g[2]) if g[2] is not None else 3)
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": "completed", "fit_status": "completed", "evidence": {"sigma_hat": m3, "sigma_hat_robust": m3}, "selection": {"hpm": list(hpm)}, "pip": {"island_spread": {"max_sd": m2, "target_met": m2 <= 0.005}},
               "fit": {"meta": {"occ": [{"M": 1000, "sd_log_Z_occ_r": m1}], "flags": {"occ_inhomogeneous": False}}}}, open(os.path.join(d, "eval.bin.json"), "w"))
    json.dump({"run_id": rid, "stages": {"islands": {"billed_core_h": isl}}}, open(os.path.join(cdir, "cost_%s.json" % rid), "w"))
    N, m, I = rec
    if how == "meta":
        json.dump({"meta": {"N": N, "refine_m": m, "I_max": I, "I_used": min(I, 3), "rule": "bounded", "flags": {"grid_unconverged": False}}}, open(os.path.join(d, "calib_meta.json"), "w"))
    elif how == "settings":
        json.dump({"tier_final": 0, "settings": {"rule": "bounded", "refine_m": m, "I_max": I, "tiers": [{"N_final": N}]}}, open(os.path.join(d, "calib.bin.json"), "w"))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.r = os.path.join(self.t, "r"); self.c = os.path.join(self.t, "c"); os.makedirs(self.r); os.makedirs(self.c)

    def tearDown(self):
        shutil.rmtree(self.t)

    def build(self, m4_ratio, i0_ratio, m4_cost=2.0, hpm_bad_arm=None, m4_rec=None, i0_hpm_bad_ds=None, how="meta", norec_m4=False):
        for ds in DS:
            for c in (1, 2):
                mk(self.r, self.c, ds, "N2500-m1-c%d" % c, 0.02, 0.0004, 0.025, 1.0, how=how)
                mk(self.r, self.c, ds, "N2500-m4-c%d" % c, 0.02 * m4_ratio, 0.0004 * m4_ratio, 0.025 * m4_ratio, m4_cost,
                   hpm=((1, 2, 4) if hpm_bad_arm == "m4" and ds == "AR" else (1, 2, 3)), rec=(m4_rec if (m4_rec and ds == "AR" and c == 1) else None), how=("none" if norec_m4 and ds == "AR" and c == 1 else how))
                mk(self.r, self.c, ds, "N2500-m1-I0-c%d" % c, 0.02 * i0_ratio, 0.0004 * i0_ratio, 0.025 * i0_ratio, 1.0,
                   hpm=((1, 2, 4) if i0_hpm_bad_ds == ds else (1, 2, 3)), how=how)

    def run_(self):
        o = os.path.join(self.t, "o")
        r = subprocess.run([sys.executable, "-I", SCRIPT, "--records", self.r, "--cost-dir", self.c, "--out", o], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        return json.load(open(os.path.join(o, "freeze.json")))

    def test_adopt_when_gain_beats_extra_islands(self):
        self.build(0.6, 1.05, 2.0); d = self.run_()["decisions"]               # limit 1/sqrt(2) = 0.707 >= 0.6
        self.assertEqual(d["m=4"], "ADOPT"); self.assertEqual(d["I_max=0"], "ADOPT"); self.assertEqual(d["N=10000 (m=1)"], "NOT_RUN"); self.assertIn("not tested", d["resampling"])

    def test_keep_when_gain_is_small_or_cost_large(self):
        self.build(0.8, 1.4, 2.0); d = self.run_()["decisions"]                # 0.8 > 0.707; I_max=0 is 40% worse
        self.assertEqual(d["m=4"], "KEEP"); self.assertEqual(d["I_max=0"], "KEEP")
        shutil.rmtree(self.t); self.setUp(); self.build(0.6, 1.0, 4.0); self.assertEqual(self.run_()["decisions"]["m=4"], "KEEP")   # cost x4 needs r <= 0.5

    def test_hpm_disagreement_in_the_knobs_own_arm_blocks_adoption(self):
        self.build(0.5, 1.0, 2.0, hpm_bad_arm="m4"); self.assertEqual(self.run_()["decisions"]["m=4"], "KEEP")

    def test_R1_hpm_check_is_per_knob(self):
        # one HPM difference in an I_max = 0 fit must not flip m = 4 (plan review R1)
        self.build(0.5, 1.0, 2.0, i0_hpm_bad_ds="ARweak"); d = self.run_()["decisions"]
        self.assertEqual(d["m=4"], "ADOPT"); self.assertEqual(d["I_max=0"], "KEEP")

    def test_R2_recorded_arm_contradicting_the_plan_is_an_identity_failure(self):
        self.build(0.5, 1.0, 2.0, m4_rec=(2500, 1, 3)); o = self.run_()                       # run id says m4, the calib record says refine_m 1 (the silent no-op)
        self.assertEqual(o["decisions"]["m=4"], "INCOMPLETE")
        self.assertTrue(any("ARM_MISMATCH" in x for r in o["identity"].values() for x in r["reasons"]))

    def test_R2_identity_failure_in_the_baseline_makes_every_knob_incomplete(self):
        self.build(0.5, 1.0, 2.0, how="settings")
        d0 = os.path.join(self.r, "4-AR-n200-r01-P-N2500-m1-c1-s1"); j = json.load(open(os.path.join(d0, "calib.bin.json"))); j["settings"]["refine_m"] = 4; json.dump(j, open(os.path.join(d0, "calib.bin.json"), "w"))
        d = self.run_()["decisions"]; self.assertEqual(d["m=4"], "INCOMPLETE"); self.assertEqual(d["I_max=0"], "INCOMPLETE")

    def test_fallback_to_calib_settings_and_missing_record(self):
        self.build(0.6, 1.05, 2.0, how="settings"); self.assertEqual(self.run_()["decisions"]["m=4"], "ADOPT")      # calib.bin.json settings suffice
        shutil.rmtree(self.t); self.setUp(); self.build(0.6, 1.05, 2.0, norec_m4=True); self.assertEqual(self.run_()["decisions"]["m=4"], "INCOMPLETE")   # no record = cannot verify

    def test_I_used_above_I_max_is_an_identity_failure(self):
        self.build(0.6, 1.0, 2.0)
        p = os.path.join(self.r, "4-AR-n200-r01-P-N2500-m1-I0-c1-s1", "calib_meta.json"); j = json.load(open(p)); j["meta"]["I_used"] = 2; json.dump(j, open(p, "w"))
        self.assertEqual(self.run_()["decisions"]["I_max=0"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
