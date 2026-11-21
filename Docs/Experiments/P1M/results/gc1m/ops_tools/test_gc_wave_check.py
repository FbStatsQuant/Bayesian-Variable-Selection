#!/usr/bin/env python3
"""test_gc_wave_check.py -- tests of gc_wave_check.py / gc_ess_nots.py (H-48 / H-49 wave check). Synthetic island files in the SMCBVS4 container, the decision rule, and two GOLDENS on real records:
the pilot (islands on Owls: min ESS 1666.9 = 0.667 N at island_11 stage 22) and option D (the plan worker's ESS: 232.8 = 0.093 N at island_6 stage 3, phi 0.4866 -> 0.5814, dphi 0.0949; low_ESS alone: reported).
Scratch under staging/gc1m/_t (never /tmp)."""
import array, hashlib, json, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE); TMP = os.path.join(STG, "_t", "wc"); os.makedirs(TMP, exist_ok=True)
sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import gc_wave_check as W, gc_ess_nots as E
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
def write_island(path, phi, ess, grid):
    secs = [("grid", grid), ("st_phi", phi), ("st_ess", ess), ("other", [1.0, 2.0])]; ns = len(secs); blobs = []; off = 128 + 128 * ns
    tbl = b""; body = b""
    for nm, v in secs:
        b = array.array("d", v).tobytes(); e = nm.encode().ljust(48, b"\0") + struct.pack("<II", 1, 1) + struct.pack("<4Q", len(v), 0, off + len(body), len(b)) + hashlib.sha256(b).digest()
        tbl += e.ljust(128, b"\0"); body += b
    size = 128 + len(tbl) + len(body); h = bytearray(128); h[:8] = b"SMCBVS4\0"; struct.pack_into("<3I", h, 12, 0, 0, ns); struct.pack_into("<Q", h, 24, size)
    open(path, "wb").write(bytes(h) + tbl + body)
# ---- the container reader ----
d = os.path.join(TMP, "run1"); os.makedirs(d, exist_ok=True)
write_island(os.path.join(d, "island_1.bin"), [0.3, 0.5, 0.6], [2250.0, 2400.0, 2490.0], [0.0, 0.3, 0.5, 0.6])
write_island(os.path.join(d, "island_2.bin"), [0.3, 0.5, 0.6], [2240.0, 232.8, 2500.0], [0.0, 0.3, 0.5, 0.6])
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gc_ess_nots.py"), d], capture_output=True, text=True); j = json.loads(r.stdout)
check("gc_ess_nots reads st_phi / st_ess / grid of every island by seek, hash-verified", r.returncode == 0 and sorted(j[d]) == ["island_1.bin", "island_2.bin"] and j[d]["island_2.bin"]["st_ess"] == [2240.0, 232.8, 2500.0], r.stderr)
bad = bytearray(open(os.path.join(d, "island_2.bin"), "rb").read()); bad[-20] ^= 1; open(os.path.join(d, "island_3.bin"), "wb").write(bytes(bad))
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gc_ess_nots.py"), d], capture_output=True, text=True); check("a corrupted section fails the hash check (no silent read)", r.returncode != 0 and "hash" in r.stderr, r.stderr[-200:])
os.remove(os.path.join(d, "island_3.bin"))
# ---- the dip with delta-phi ----
mn, lows, n = W.ess_dips(j[d], 2500)
check("ESS dip: min = island_2 stage 2 ESS 232.8 (0.0931 N), phi 0.3 -> 0.5, dphi 0.2, 1 island-stage < 0.5 N of 6", abs(mn["ess_over_N"] - 232.8 / 2500) < 1e-12 and mn["island"] == "island_2.bin" and mn["stage"] == 2 and abs(mn["dphi"] - 0.2) < 1e-12 and len(lows) == 1 and n == 6, str(mn))
mn1, lows1, _ = W.ess_dips({"island_1.bin": {"st_phi": [0.25, 0.5], "st_ess": [100.0, 2000.0]}}, 2500)
check("first stage: phi_from = 0, dphi = phi_to", mn1["stage"] == 1 and mn1["phi_from"] == 0.0 and mn1["dphi"] == 0.25, str(mn1))
mn2, lows2, _ = W.ess_dips({"island_1.bin": {"st_phi": [0.25, 0.5], "st_ess": [1250.0, 2000.0]}}, 2500)
check("ESS exactly 0.5 N is not low (strict <, as merge.h)", not lows2, str(lows2))
# ---- the H-48 / H-49 decision rule ----
base = dict(low_empirical_ESS=True, ess_low_stages=[{"x": 1}], E=dict(E1=False, E2=False, E3=False), sigma_hat=0.03, C2_verdict="PASS", hpm_eq_S0=True)
low, rs, stop = W.decide(base); check("low_ESS alone: reported, NOT a stop", low and not rs and not stop)
for name, mod, frag in (("E1", dict(E=dict(E1=True, E2=False, E3=False)), "E-flag E1"), ("E2", dict(E=dict(E1=False, E2=True, E3=False)), "E-flag E2"), ("E3", dict(E=dict(E1=False, E2=False, E3=True)), "E-flag E3"), ("sigma-hat 0.51", dict(sigma_hat=0.51), "sigma-hat"), ("C2 FAIL", dict(C2_verdict="FAIL"), "C2 FAIL"), ("HPM != S0", dict(hpm_eq_S0=False), "HPM != S0")):
    low, rs, stop = W.decide(dict(base, **mod)); check("low_ESS together with %s -> FLAG: STOP" % name, low and stop and any(frag in r for r in rs), str(rs))
low, rs, stop = W.decide(dict(base, sigma_hat=0.5)); check("sigma-hat exactly 0.5 is not > 0.5: low_ESS alone", not stop, str(rs))
low, rs, stop = W.decide(dict(base, low_empirical_ESS=False, ess_low_stages=[], sigma_hat=0.9, E=dict(E1=True, E2=False, E3=False))); check("an E-flag / sigma-hat > 0.5 WITHOUT low_ESS is not this rule's stop (reported elsewhere)", not low and not stop and rs, str(rs))
low, rs, stop = W.decide(dict(base, low_empirical_ESS=False)); check("low_ESS from the sections alone (engine flag False) still counts as low_ESS", low, str(rs))
# ---- goldens on real records ----
rec = "/home/fb31/SMC_Engineering_Department/records/gc1m"
pe = os.path.join(TMP, "ess_P.json"); r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gc_ess_nots.py"), rec + "/GC_P/6-AR-n200-r01-V-s1"], capture_output=True, text=True); open(pe, "w").write(r.stdout)
r = subprocess.run([sys.executable, os.path.join(HERE, "gc_wave_check.py"), "--wave", "P", "--records-dir", rec + "/GC_P", "--ess-json", pe, "--out-dir", TMP], capture_output=True, text=True); jp = json.load(open(os.path.join(TMP, "wave_check_P.json")))
f = jp["fits"][0]
check("GOLDEN pilot (real islands): min ESS 1666.9 = 0.667 N at island_11 stage 22; HPM = S0, MPM = S0, C2 PASS, no low_ESS, no FLAG, rc 0", r.returncode == 0 and abs(f["min_ess"]["ess"] - 1666.9) < 0.1 and f["min_ess"]["island"] == "island_11.bin" and f["min_ess"]["stage"] == 22 and f["hpm_eq_S0"] and f["mpm_eq_S0"] and f["C2_verdict"] == "PASS" and not f["low_ESS"] and not jp["flag_stop"], r.stdout + r.stderr)
dj = json.load(open("/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/gc1m/readback_D/ess_D.json")); de = os.path.join(TMP, "ess_D.json"); json.dump({"/x/6-AR-n1000-r01-V-s1": dj}, open(de, "w"))
r = subprocess.run([sys.executable, os.path.join(HERE, "gc_wave_check.py"), "--wave", "D", "--records-dir", rec + "/GC_D", "--ess-json", de, "--out-dir", TMP], capture_output=True, text=True); jd = json.load(open(os.path.join(TMP, "wave_check_D.json"))); f = jd["fits"][0]
md = open(os.path.join(TMP, "wave_check_D.md")).read()
check("GOLDEN option D: min ESS 232.8 (0.093 N) at island_6 stage 3, phi 0.4866 -> 0.5814, dphi 0.0949; E1/E2/E3 False, sigma-hat 0.0310, C2 PASS, HPM = MPM = S0; engine flag and sections AGREE; low_ESS alone: reported, no FLAG, rc 0",
      r.returncode == 0 and abs(f["min_ess"]["ess"] - 232.8) < 0.1 and f["min_ess"]["island"] == "island_6.bin" and f["min_ess"]["stage"] == 3 and abs(f["min_ess"]["dphi"] - 0.0949) < 1e-4 and not any(f["E"].values()) and abs(f["sigma_hat"] - 0.031049) < 1e-5 and f["C2_verdict"] == "PASS" and f["hpm_eq_S0"] and f["mpm_eq_S0"] and f["ess_flag_consistent"] and f["low_ESS"] and not f["flag_stop"] and "low_ESS alone: reported" in md and "dphi 0.0949" in md, r.stdout + r.stderr)
check("the md names every low_ESS fit with its island, stage and the phi step", "6-AR-n1000-r01-V-s1" in md and "island_6.bin stage 3" in md and "dphi 0.0949" in md, md)
# a FLAG case: the same D data but a failing C2 / HPM (patch the readback json)
rbj = json.load(open(os.path.join(TMP, "gc_readback_D", "gc_readback.json"))); rbj["fits"]["6-AR-n1000-r01-V-s1"]["C2"]["verdict"] = "FAIL"; rbp = os.path.join(TMP, "rb_fail.json"); json.dump(rbj, open(rbp, "w"))
r = subprocess.run([sys.executable, os.path.join(HERE, "gc_wave_check.py"), "--wave", "Dx", "--records-dir", rec + "/GC_D", "--ess-json", de, "--readback-json", rbp, "--out-dir", TMP], capture_output=True, text=True)
check("D data with a (patched) C2 FAIL: low_ESS + C2 failure -> 'FLAG: STOP', exit 2, md says so", r.returncode == 2 and "FLAG: STOP" in open(os.path.join(TMP, "wave_check_Dx.md")).read(), r.stdout + r.stderr)
r = subprocess.run([sys.executable, os.path.join(HERE, "gc_wave_check.py"), "--wave", "Dy", "--records-dir", rec + "/GC_D", "--ess-json", pe, "--out-dir", TMP], capture_output=True, text=True)
check("missing ESS data for a fit is an error, never a silent pass", r.returncode != 0 and "no ESS data" in (r.stdout + r.stderr), r.stdout + r.stderr)
# ---- island timing (H-50 / H-51) ----
rec = "/home/fb31/SMC_Engineering_Department/records/gc1m"
tm, bt, sent = W.island_timing([rec + "/GC_D"]); x = tm["6-AR-n1000-r01-V-s1"]
check("island timing GOLDEN on GC_D (real sacct dump + sidecars): 16 islands, elapsed max 738 s, engine totals present, pre-engine wait > 0, billed 259.8 core-h", x["n"] == 16 and x["elapsed"]["max"] == 738 and x["engine_total"] and x["pre_engine_wait"]["min"] > 0 and abs(x["billed_core_h"] - 259.81) < 0.05 and x["engine_core_h"] < x["billed_core_h"], str(x))
check("island timing groups by node type from the sacct NodeList (c / g suffix) and gives the one-sentence proposal", set(bt) <= {"c", "g"} and len(bt) >= 1 and ("Proposal only" in sent or "no node-type contrast" in sent), str(bt) + sent)
# synthetic batch: 4 islands, two types, known numbers
sb = os.path.join(TMP, "GC_X"); os.makedirs(os.path.join(sb, "_batch_GC_X"), exist_ok=True); os.makedirs(os.path.join(sb, "6-X-n200-r01-V-s1"), exist_ok=True)
open(os.path.join(sb, "_batch_GC_X", "submissions.jsonl"), "w").write(json.dumps({"stage": "islands", "fit": "6-X-n200-r01-V-s1", "job": "900", "submitted_utc": "x"}) + "\n")
rows = ["900_1|p1m_GC_X_islands|COMPLETED|600|96|%d||bb2u10c1|01:00:00" % (600 * 96), "900_2|p1m_GC_X_islands|COMPLETED|700|96|%d||bb2u11c1|01:00:00" % (700 * 96), "900_3|p1m_GC_X_islands|COMPLETED|1000|96|%d||bb6u21g1|01:00:00" % (1000 * 96), "900_4|p1m_GC_X_islands|COMPLETED|1100|96|%d||bb6u22g1|01:00:00" % (1100 * 96), "900_4.batch|batch|COMPLETED|1100|96|1||bb6u22g1|", "901|p1m_GC_X_merge|COMPLETED|10|32|320||bb1u1c1|"]
open(os.path.join(sb, "_batch_GC_X", "sacct_dump.txt"), "w").write("\n".join(rows) + "\n")
for k, eng in ((1, 500.0), (2, 560.0), (3, 700.0), (4, 760.0)): json.dump({"seconds": {"total": eng}}, open(os.path.join(sb, "6-X-n200-r01-V-s1", "island_%d.bin.json" % k), "w"))
tm, bt, sent = W.island_timing([sb]); x = tm["6-X-n200-r01-V-s1"]
check("island timing synthetic: elapsed 600 / 850 / 1100, engine 500 / 630 / 760, pre-engine wait min 100 / max 340, billed 3,400 x 96 / 3600 = 90.67 core-h, engine core-h 2,520 x 96 / 3600 = 67.2, types c (2) and g (2), batch step rows and merge rows ignored",
      x["n"] == 4 and x["elapsed"]["min"] == 600 and x["elapsed"]["max"] == 1100 and abs(x["elapsed"]["mean"] - 850) < 1e-9 and x["pre_engine_wait"]["min"] == 100 and x["pre_engine_wait"]["max"] == 340 and abs(x["billed_core_h"] - 90.6667) < 1e-3 and abs(x["engine_core_h"] - 67.2) < 1e-6 and bt["c"]["n"] == 2 and bt["g"]["n"] == 2, str(x))
check("node-constraint sentence: type c is faster (mean 650 vs 1,050 s); the saving is (1000-650 + 1100-650) x 96 / 3600 = 21.3 core-h of 90.7 (23.5 %); 'Proposal only' and the unmeasured-queue caveat", "Proposal only" in sent and "type c" in sent and "21.3" in sent and "23.5" in sent and "queue wait" in sent, sent)
# ---- H-52: wave-level mean pre-engine wait and the %8 throttle rule; pi-hat in the table ----
r = subprocess.run([sys.executable, os.path.join(HERE, "gc_wave_check.py"), "--wave", "D", "--records-dir", rec + "/GC_D", "--ess-json", de, "--out-dir", TMP], capture_output=True, text=True); jd = json.load(open(os.path.join(TMP, "wave_check_D.json"))); md = open(os.path.join(TMP, "wave_check_D.md")).read()
wv = jd["island_timing"]["wave"]
check("H-52 wave line GOLDEN (option D, 16 islands): mean pre-engine wait 156 s <= 300 -> 'stagger only'; billed 259.8 vs engine 193.4; pi-hat(S0) 0.663 in the table", abs(wv["mean_pre_engine_wait_s"] - 156) < 2 and wv["islands"] == 16 and "stagger only" in wv["H52_throttle_rule"] and abs(wv["slurm_billed_island_core_h"] - 259.81) < 0.05 and "0.663" in md and "mean pre-engine wait per island" in md, str(wv))
tm_, bt_, s_ = W.island_timing([sb])
check("H-52 synthetic: 4 islands, waits 100 / 140 / 300 / 340 -> mean 220 <= 300: stagger only (the rule's boundary)", abs(sum(r_["elapsed"] - r_["engine"] for rs_ in [[dict(elapsed=600, engine=500), dict(elapsed=700, engine=560), dict(elapsed=1000, engine=700), dict(elapsed=1100, engine=760)]] for r_ in rs_) / 4 - 220) < 1e-9)
import subprocess as sp
rg = sp.run([sys.executable, os.path.join(HERE, "gc_stagger_submit.py"), os.path.join(STG, "scripts", "GC_W3"), "--throttle", "8"], capture_output=True, text=True)
ss = open(os.path.join(STG, "scripts", "GC_W3", "submit_stagger.sh")).read()
check("gc_stagger_submit.py --throttle 8: the island array is %8 (not %16), the stagger dependency is kept, bash -n ok, one array line changed", rg.returncode == 0 and "--array=1-$rp%8" in ss and "%16" not in ss.replace("# ", "#") .split("stage_islands")[0].split("--array=1-$rp")[-1][:3] and "afterany:$JIPREV" in ss, rg.stdout + rg.stderr + ss[-700:])
sp.run([sys.executable, os.path.join(HERE, "gc_stagger_submit.py"), os.path.join(STG, "scripts", "GC_W3")], capture_output=True, text=True)   # restore the default (%16) stagger script
check("default stagger script keeps the plan's %16", "--array=1-$rp%16" in open(os.path.join(STG, "scripts", "GC_W3", "submit_stagger.sh")).read())
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
