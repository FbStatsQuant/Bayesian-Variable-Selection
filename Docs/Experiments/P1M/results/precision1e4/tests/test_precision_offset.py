#!/usr/bin/env python3
"""Self-test of precision_offset.py on SYNTHETIC records (no real data is touched). python3 -I tests/test_precision_offset.py"""
import json, math, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); SCRIPT = os.path.join(os.path.dirname(HERE), "precision_offset.py")


def lse(xs):
    m = max(xs); return m + math.log(sum(math.exp(x - m) for x in xs))


def mk(root, rid, Rp, logZ_r, cell=None, arm="V", tier=0, status="completed", settings_override=None):
    d = os.path.join(root, rid); os.makedirs(d)
    logZ = lse(logZ_r) - math.log(Rp)
    json.dump({"run_id": rid}, open(os.path.join(d, "run_manifest.json"), "w"))
    json.dump({"status": status, "fit_status": "completed", "evidence": {"logZ_r": logZ_r, "logZ": logZ},
               "fit": {"meta": {"Rp": Rp, "tier": tier, "N": 2500, "occ": [{"M": 1000, "log_Z_occ": logZ + 0.001}]}}}, open(os.path.join(d, "eval.bin.json"), "w"))
    if arm == "V":
        N, m, I = cell
        st = {"rule": "bounded", "refine_m": m, "I_max": I, "tiers": [{"N_final": N}]}
        st.update(settings_override or {})
        json.dump({"settings": st, "tier_final": 0}, open(os.path.join(d, "calib.bin.json"), "w"))
    return logZ


def run(root, out, *extra):
    r = subprocess.run([sys.executable, "-I", SCRIPT, "--records", root, "--out", out, *extra], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.load(open(os.path.join(out, "offset.json")))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE)); self.root = os.path.join(self.t, "rec"); os.makedirs(self.root)

    def tearDown(self):
        shutil.rmtree(self.t)

    def build(self):
        # 3 datasets; T: 2 seeds, R'=4, logZ = base_d + 0.01 (s1), base_d - 0.01 (s2)  => Tbar_d = base_d
        # V overlap (2500,1,3) R'=16: island values base_d - 0.004 + e_r with e_r = +-0.02 alternating, so each 2-block of islands has mean offset exactly -0.004 in Z-space only approximately
        self.base = {"AR-r01": -177.0, "ARweak-r01": -150.0, "ADJOPP-r01": -220.0}
        for ds, b in self.base.items():
            des, rep = ds.split("-r")
            for s, e in ((1, 0.01), (2, -0.01)):
                mk(self.root, "4-%s-n200-r%s-T-s%d" % (des, rep, s), 4, [b + e] * 4, arm="T")
                mk(self.root, "4-%s-n200-r%s-V-s%d" % (des, rep, s), 16, [b - 0.004] * 16, cell=(2500, 1, 3))
            for c in (1, 2):
                mk(self.root, "4-%s-n200-r%s-P-N2500-m4-c%d-s1" % (des, rep, c), 64, [b + 0.002 * (1 if c == 1 else -1) + 0.001] * 64, cell=(2500, 4, 3))
                mk(self.root, "4-%s-n200-r%s-P-N2500-m1-c%d-s1" % (des, rep, c), 64, [b - 0.003] * 64, cell=(2500, 1, 3))

    def test_offsets_contrasts_and_blocks(self):
        self.build(); o = run(self.root, os.path.join(self.t, "o"))
        tab = {(t["N"], t["m"], t["I_max"], t["src"], t["k"]): t for t in o["table"]}
        # constant islands: every block mean equals the constant, so delta does not depend on k (the Jensen term vanishes)
        for k in (4, 8, 16):
            self.assertAlmostEqual(tab[(2500, 1, 3, "ovl", k)]["delta"], tab[(2500, 1, 3, "ovl", 16)]["delta"], places=10)
        # precision cell (2500,1,3) at k=64: replicates b - 0.003 against Tbar = b -> -0.003; overlap cell at k=16: -0.004 (kept as separate cells)
        self.assertAlmostEqual(tab[(2500, 1, 3, "prec", 64)]["delta"], -0.003, places=9)
        self.assertAlmostEqual(tab[(2500, 1, 3, "ovl", 16)]["delta"], -0.004, places=9)
        self.assertEqual(tab[(2500, 4, 3, "prec", 64)]["datasets"], 3)
        self.assertAlmostEqual(tab[(2500, 4, 3, "prec", 64)]["delta"], 0.001, places=9)          # replicates +0.003 and -0.001 -> mean +0.001
        cm = {c["contrast"]: c for c in o["contrasts"]}
        m4 = cm["m: (2500,4,3) - (2500,1,3) at k=64"]
        self.assertAlmostEqual(m4["mean"], 0.001 - (-0.003), places=9); self.assertEqual(m4["datasets"], 3)
        self.assertAlmostEqual(o["s_T_seed_to_seed"], 0.02 / math.sqrt(2), places=9)          # the two T seeds differ by 0.02 on every dataset

    def test_block_mean_uses_jensen(self):
        # islands alternate +-0.5 around 0: the 2-block mean of log-sum-exp is log cosh(0.5) < the island mean 0, and the 16-pool value is the fit's logZ
        for des, rep in (("AR", "01"), ("ARweak", "01")):
            for s in (1, 2):
                mk(self.root, "4-%s-n200-r%s-T-s%d" % (des, rep, s), 4, [-100.0] * 4, arm="T")
                mk(self.root, "4-%s-n200-r%s-V-s%d" % (des, rep, s), 16, [-100.0 + (0.5 if i % 2 == 0 else -0.5) for i in range(16)], cell=(2500, 1, 3))
        o = run(self.root, os.path.join(self.t, "o")); tab = {t["k"]: t for t in o["table"]}
        self.assertAlmostEqual(tab[16]["delta"], -100.0 + 0.0 + math.log(math.cosh(0.5)) + 100.0, places=9)   # logsumexp of +-0.5 pairs, k=16 blocks of 16
        self.assertAlmostEqual(tab[16]["delta"], tab[4]["delta"], places=9)           # alternating pattern: every even-sized block has the same mean
        self.assertLess(tab[16]["jensen_mean"], 0)

    def test_P2_span_contrast_with_jensen_prediction(self):
        # plan review R11: the headline R' contrast is the SPAN k_min -> k_max, with the Jensen prediction beside it and the slope minus it
        for des, rep in (("AR", "01"), ("ARweak", "01"), ("ADJOPP", "01")):
            for sd in (1, 2):
                mk(self.root, "4-%s-n200-r%s-T-s%d" % (des, rep, sd), 4, [-100.0] * 4, arm="T")
                mk(self.root, "4-%s-n200-r%s-V-s%d" % (des, rep, sd), 16, [-100.0 + (0.4 if i % 4 == 0 else -0.1) for i in range(16)], cell=(2500, 1, 3))
        o = run(self.root, os.path.join(self.t, "o")); cm = {c["contrast"]: c for c in o["contrasts"]}
        span = [c for c in o["contrasts"] if c["kind"] == "P2_span"]
        self.assertEqual(len(span), 1); self.assertIn("k 4 -> 16", span[0]["contrast"])
        steps = [c for c in o["contrasts"] if c["kind"] == "R_step"]; self.assertEqual(len(steps), 2)          # 4 -> 8, 8 -> 16
        self.assertGreater(span[0]["jensen_pred"], 0)                                                         # Jensen bias shrinks with k: log-mean rises
        self.assertAlmostEqual(span[0]["mean"], span[0]["minus_jensen_mean"] + span[0]["jensen_pred"], places=12)

    def test_arm_mismatch_and_manifest_eval_skipped(self):
        self.build()
        mk(self.root, "4-AR-n200-r01-P-N10000-m1-c1-s1", 64, [-177.0] * 64, cell=(10000, 1, 3), settings_override={"refine_m": 4})     # run id says m1, settings say m4
        os.makedirs(os.path.join(self.root, "_batch_X", "scripts", "manifests", "4-AR-n200-r01-V-s1"))
        json.dump({"command": "eval", "run_id": "4-AR-n200-r01-V-s1"}, open(os.path.join(self.root, "_batch_X", "scripts", "manifests", "4-AR-n200-r01-V-s1", "eval.json"), "w"))
        o = run(self.root, os.path.join(self.t, "o"))
        self.assertEqual([d["run_id"] for d in o["dropped"]], ["4-AR-n200-r01-P-N10000-m1-c1-s1"]); self.assertIn("ARM_MISMATCH", o["dropped"][0]["problems"][0])
        self.assertEqual(o["duplicates_resolved"], [])
        self.assertFalse(any(t["N"] == 10000 for t in o["table"]))

    def test_undelivered_and_only_full(self):
        self.build()
        mk(self.root, "4-NULL-n200-r01-V-s1", 16, [-1.0] * 16, cell=(2500, 1, 3), status="failed")
        o = run(self.root, os.path.join(self.t, "o2"), "--only-full")
        self.assertEqual(len(o["dropped"]), 1); self.assertTrue(o["only_full"])
        self.assertEqual(sorted({t["k"] for t in o["table"]}), [16, 64]); self.assertEqual(o["contrasts"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
