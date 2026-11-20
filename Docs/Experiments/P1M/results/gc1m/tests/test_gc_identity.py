#!/usr/bin/env python3
"""Self-test of gc_identity.py on REAL records: positive control = the 11-17 1M record against itself, and the G-B 10^5 AR pair (I_max 0 fit vs its I_max 3 twin: same data, seed, setup and PILOT island,
different grid: the same structure as the 1M pair) -> PASS; negative controls = AR r01 vs ADJ-OPP r01 (different data) -> FAIL; a mutation of a trajectory counter (pairs, mean_S), a header mismatch or a missing row -> FAIL; the accounting counters (flips, offers, ...) differ between the identical 10^5 runs and are NOT gated.
python3 -I tests/test_gc_identity.py (scratch: PREC_TEST_TMP or here, never /tmp)"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__)); GC = os.path.dirname(HERE); SCRIPT = os.path.join(GC, "gc_identity.py")
R = os.path.expanduser("~/SMC_Engineering_Department/records")
OLD1M = os.path.join(R, "F1M_pilot"); G1A = os.path.join(R, "gb/GB_G1a/5-AR-n200-r01-V-s1"); G1B = os.path.join(R, "gb/GB_G1b/5-AR-n200-r01-VI3-s1"); G2A = os.path.join(R, "gb/GB_G2a/5-ADJOPP-n200-r01-V-s1")


def run(old, new, out):
    p = subprocess.run([sys.executable, "-I", SCRIPT, "--old", old, "--new", new, "--out", out], capture_output=True, text=True)
    return p.returncode, json.load(open(os.path.join(out, "gc_identity.json")))


class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(dir=os.environ.get("PREC_TEST_TMP", HERE))

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def test_1m_record_against_itself(self):
        if not os.path.isdir(OLD1M):
            self.skipTest("records not present"); return
        rc, j = run(OLD1M, OLD1M, os.path.join(self.t, "o")); self.assertEqual((rc, j["IDENTITY"]), (0, "PASS")); self.assertEqual(j["detail"]["I3"]["rows"], [34, 34])

    def test_gb_pair_same_data_seed_pilot(self):
        if not os.path.isdir(G1A):
            self.skipTest("records not present"); return
        rc, j = run(G1A, G1B, os.path.join(self.t, "o")); self.assertEqual((rc, j["IDENTITY"]), (0, "PASS"), j["detail"]["I3"])
        self.assertEqual(j["detail"]["I4_reported_not_gating"]["I_max_old_new"], [0, 3])

    def test_different_data_fails(self):
        if not os.path.isdir(G1A):
            self.skipTest("records not present"); return
        rc, j = run(G1A, G2A, os.path.join(self.t, "o")); self.assertEqual(rc, 1); self.assertFalse(j["checks"]["I1_data"]); self.assertFalse(j["checks"]["I3_pilot_counters"])

    def test_mutated_counter_and_header(self):
        if not os.path.isdir(G1A):
            self.skipTest("records not present"); return
        for mut in ("counter", "state", "header", "rows"):
            d = os.path.join(self.t, "new_" + mut); os.makedirs(os.path.join(d, "cost"))
            for f in ("truth.json", "setup.bin.json", "run_manifest.json", "calib.bin.json"):
                shutil.copy(os.path.join(G1B, f), d)
            L = open(os.path.join(G1B, "cost", "cost_pilot_t0_k0_r0.jsonl")).read().strip().split("\n")
            if mut == "counter":
                r = json.loads(L[5]); r["pairs"] += 100000; L[5] = json.dumps(r)
            elif mut == "state":
                r = json.loads(L[7]); r["mean_S"] += 0.01; L[7] = json.dumps(r)
            elif mut == "header":
                h = json.loads(L[0]); h["cost_header"]["G"] = 64; L[0] = json.dumps(h)
            else:
                L = L[:-1]
            open(os.path.join(d, "cost", "cost_pilot_t0_k0_r0.jsonl"), "w").write("\n".join(L) + "\n")
            rc, j = run(G1A, d, os.path.join(self.t, "o_" + mut)); self.assertEqual(rc, 1, mut); self.assertFalse(j["checks"]["I3_pilot_counters"], mut); self.assertTrue(j["checks"]["I1_data"] and j["checks"]["I2_setup"])

    def test_accounting_counters_not_gated(self):
        if not os.path.isdir(G1A):
            self.skipTest("records not present"); return
        rc, j = run(G1A, G1B, os.path.join(self.t, "o")); acc = j["detail"]["I3"]["accounting_counters_reported_not_gating"]
        self.assertGreater(acc["flips"]["rows_differing"], 0); self.assertLess(acc["flips"]["max_rel_diff"], 0.05); self.assertEqual(j["IDENTITY"], "PASS")

    def test_timing_differences_ignored(self):
        if not os.path.isdir(G1A):
            self.skipTest("records not present"); return
        d = os.path.join(self.t, "new_t"); os.makedirs(os.path.join(d, "cost"))
        for f in ("truth.json", "setup.bin.json", "run_manifest.json"):
            shutil.copy(os.path.join(G1B, f), d)
        L = open(os.path.join(G1B, "cost", "cost_pilot_t0_k0_r0.jsonl")).read().strip().split("\n")
        for i in range(1, len(L)):
            r = json.loads(L[i]); r["wall"] = r["wall"] * 1.7 + 1; r["t_phaseB"] = 123.0; r["rss_kb"] += 99; L[i] = json.dumps(r)
        open(os.path.join(d, "cost", "cost_pilot_t0_k0_r0.jsonl"), "w").write("\n".join(L) + "\n")
        rc, j = run(G1A, d, os.path.join(self.t, "o")); self.assertEqual(j["checks"]["I3_pilot_counters"], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
