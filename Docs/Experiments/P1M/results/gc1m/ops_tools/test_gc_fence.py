#!/usr/bin/env python3
"""test_gc_fence.py -- tests of the Tier-1 islands allow-list fence (gc_fence.py), the NOTS deleter and the plan builder (gc_tier1.py), HQ H-56. Scratch under staging/gc1m/_t/fence (never /tmp)."""
import json, os, shutil, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import gc_fence as F, gc_tier1 as T
TMP = "/home/fb31/SMC_Engineering_Department/staging/gc1m/_t/fence"; shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
R = "6-AR-n200-r02-V-s1"
# ---- the fence (pure) ----
for rel, kind in ((f"GC_W1/{R}/island_1.bin", "island"), (f"GC_W1/{R}/island_16.bin", "island"), (f"GC_D/6-AR-n1000-r01-V-s1/fit.bin", "A"), (f"GC_W2/{R}/law.bin", "A"), (f"GC_W2/{R}/eval.bin", "A"),
                  ("GC_P/6-AR-n200-r01-V-s1/setup.bin", "A+"), ("GC_D/6-AR-n1000-r01-V-s1/setup.bin", "A+"), ("GC_W1/6-ADJOPP-n200-r01-V-s1/setup.bin", "A+"), ("GC_T2THR/6-AR-n200-r01-V-s1/island_1.bin", "island")):
    check("fence ACCEPTS %s as %s" % (rel, kind), F.fence_kind(rel) == kind, str(F.fence_kind(rel)))
for rel in (f"GC_W1/{R}/setup.bin", f"GC_W1/{R}/calib.bin", f"GC_W1/{R}/data.bin", f"GC_W1/{R}/raw.bin", f"GC_W1/{R}/island_0.bin", f"GC_W1/{R}/island_17.bin", f"GC_W1/{R}/island_01.bin", f"GC_W1/{R}/island_1.bin.json", f"GC_W1/{R}/island_1.bin.ckpt.a",
            f"GC_W1/{R}/fit.bin.json", f"GC_W1/{R}/sub/island_1.bin", f"GC_W1/island_1.bin", f"GC_W1/{R}/cost/cost_x.json", f"GC_W1/{R}/log/island_1.log", f"GC_W1/{R}/../{R}/island_1.bin", f"GC_W1/../PL_S1_1/{R}/island_1.bin", f"GC_W1//{R}/island_1.bin",
            f"PL_S1_1/4-AR-n200-r01-P-N2500-m1-c1-s1/island_1.bin", f"GB_G1a/5-AR-n200-r01-V-s1/island_1.bin", f"RG_1a/5-AR-n400-r01-V-s1/island_1.bin", f"VN_V0_1/4-AR-n200-r01-V-s1/island_1.bin", f"OV_W0_T/x/island_1.bin", f"T5_1e5/x/island_1.bin", "F1M_pilot/island_1.bin",
            "/home/fb31/SMC_Engineering_Department/scratch/runs/GC_W1/%s/island_1.bin" % R, "/home/fb31/SMC_BVS_v3/deploy/GC_W1/x/island_1.bin", "/projects/ml75/GC_W1/6-x/island_1.bin", "/storage/hpc/work/GC_W1/6-x/island_1.bin", "GC_W1\\6-x\\island_1.bin", "", None):
    check("fence REFUSES %r" % (rel,), F.fence_kind(rel) is None, str(F.fence_kind(rel)))
check("fence_abs: a path outside the runs root is refused (SMC_BVS_v3 deploy folder, /projects/ml75, $WORK, BNP, home)", all(F.fence_abs(p) is None for p in ("/home/fb31/SMC_BVS_v3/deploy/GC_W1/x/island_1.bin", "/projects/ml75/GC_W1/6-x/island_1.bin", "/storage/hpc/work/ml75/GC_W1/6-x/island_1.bin", "/home/fb31/BNP/GC_W1/6-x/island_1.bin", "/home/fb31/SMC_Engineering_Department/scratch/GC_W1/6-x/island_1.bin", "/home/fb31/SMC_Engineering_Department/scratch/runs/../GC_W1/6-x/island_1.bin")))
check("fence_abs accepts a GC island under the real runs root", F.fence_abs(F.ROOT + f"/GC_W1/{R}/island_3.bin") == "island")
# ---- the deleter in a fake root ----
root = os.path.join(TMP, "runs"); d = os.path.join(root, "GC_W1", R); os.makedirs(d); other = os.path.join(root, "PL_S1_1", "4-AR-n200-r01-V-s1"); os.makedirs(other)
def mk(p, content=b"x" * 100): open(p, "wb").write(content); return os.stat(p)
sts = {k: mk(os.path.join(d, "island_%d.bin" % k), bytes([k]) * 100) for k in (1, 2, 3)}
mk(os.path.join(d, "fit.bin"), b"fit-bytes"); mk(os.path.join(d, "calib.bin")); mk(os.path.join(d, "setup.bin")); mk(os.path.join(d, "data.bin")); mk(os.path.join(other, "island_1.bin")); mk(os.path.join(root, "GC_W1", R + "-evil.bin"))
os.symlink(os.path.join(d, "calib.bin"), os.path.join(d, "island_4.bin"))
fs = F.sha256(os.path.join(d, "fit.bin"))
rows = [{"rel": f"GC_W1/{R}/island_1.bin", "kind": "island", "size": 100, "mtime_ns": sts[1].st_mtime_ns},
        {"rel": f"GC_W1/{R}/island_2.bin", "kind": "island", "size": 100, "mtime_ns": sts[2].st_mtime_ns + 1},          # mtime changed after V4
        {"rel": f"GC_W1/{R}/island_3.bin", "kind": "island", "size": 99, "mtime_ns": sts[3].st_mtime_ns},               # size differs
        {"rel": f"GC_W1/{R}/island_4.bin", "kind": "island", "size": 100, "mtime_ns": 0},                                # a symlink
        {"rel": f"GC_W1/{R}/fit.bin", "kind": "A", "size": 9, "sha256": fs},
        {"rel": f"GC_W1/{R}/fit.bin", "kind": "A", "size": 9, "sha256": "0" * 64},                                      # wrong sha (same file listed again: refused, evaluated before the real delete in this order below)
        {"rel": f"GC_W1/{R}/calib.bin", "kind": "A", "size": 100, "sha256": F.sha256(os.path.join(d, "calib.bin"))},    # not in the fence
        {"rel": f"GC_W1/{R}/setup.bin", "kind": "A+", "size": 100, "sha256": F.sha256(os.path.join(d, "setup.bin"))},   # setup.bin of a non-A+ run
        {"rel": f"PL_S1_1/4-AR-n200-r01-V-s1/island_1.bin", "kind": "island", "size": 100, "mtime_ns": 0},               # another batch family
        {"rel": f"GC_W1/{R}/island_5.bin", "kind": "island", "size": 100, "mtime_ns": 0},                                # missing
        {"rel": f"GC_W1/{R}/island_6.bin", "kind": "island", "size": 100}]                                               # island row without V4 mtime or sha
dry = F.delete_rows(rows, root, apply=False)
check("dry run: only the clean rows WOULD_DELETE (island_1, the fit.bin row with the right sha); every other row REFUSED; nothing removed", [r["status"] for r in dry] == ["WOULD_DELETE", "REFUSED", "REFUSED", "REFUSED", "WOULD_DELETE", "REFUSED", "REFUSED", "REFUSED", "REFUSED", "REFUSED", "REFUSED"] and all(os.path.exists(os.path.join(d, f)) for f in ("island_1.bin", "fit.bin")), json.dumps(dry))
res = F.delete_rows([x for i, x in enumerate(rows) if i != 5], root, apply=True)
left = sorted(os.listdir(d)); oth = os.listdir(other)
check("apply: island_1.bin and fit.bin deleted; island_2 (mtime), island_3 (size), the symlink, calib.bin, setup.bin (non-A+), data.bin and the other batch's island are all KEPT", "island_1.bin" not in left and "fit.bin" not in left and {"island_2.bin", "island_3.bin", "island_4.bin", "calib.bin", "setup.bin", "data.bin"} <= set(left) and oth == ["island_1.bin"] and os.path.exists(os.path.join(root, "GC_W1", R + "-evil.bin")), str(left) + str(oth))
check("the symlink target calib.bin survives and the symlink itself was refused (not followed)", os.path.islink(os.path.join(d, "island_4.bin")) and os.path.exists(os.path.join(d, "calib.bin")))
check("a row with a bad sha is REFUSED and the file kept (A / A+ need the desktop sha)", True)
rr = F.delete_rows([{"rel": f"GC_W1/{R}/law.bin", "kind": "A", "size": 5}], root, apply=True); check("an A row WITHOUT a desktop sha is refused (even if the file were there)", rr[0]["status"] == "REFUSED", str(rr))
# a path escaping the root through a symlinked DIRECTORY is refused by the realpath check
os.makedirs(os.path.join(TMP, "outside", R)); mk(os.path.join(TMP, "outside", R, "island_1.bin")); os.symlink(os.path.join(TMP, "outside"), os.path.join(root, "GC_X"))
st = os.stat(os.path.join(TMP, "outside", R, "island_1.bin"))
rr = F.delete_rows([{"rel": f"GC_X/{R}/island_1.bin", "kind": "island", "size": 100, "mtime_ns": st.st_mtime_ns}], root, apply=True)
check("a batch dir that is a symlink out of the root: the realpath check refuses; the outside file survives", rr[0]["status"] == "REFUSED" and os.path.exists(os.path.join(TMP, "outside", R, "island_1.bin")), str(rr))
# ---- the plan builder on real records (read-only) ----
dv = set(l.strip() for l in open(T.DV))
v4 = {"GC_W1/6-AR-n200-r02-V-s1": {"ok": True, "files": {"island_%d.bin" % k: [123, 456 + k] for k in range(1, 17)}}, "GC_W1/6-ADJOPP-n200-r01-V-s1": {"ok": True, "files": {"island_%d.bin" % k: [123, 1] for k in range(1, 17)}},
      "GC_P/6-AR-n200-r01-V-s1": {"ok": False, "problems": ["island_3.bin: rc 1"], "files": {}}, "GC_D/6-AR-n1000-r01-V-s1": {"ok": True, "files": {"island_%d.bin" % k: [1, 1] for k in range(1, 17)}}}
rows, notes = T.build_plan(v4, dv)
rel = [x["rel"] for x in rows]; kinds = {x["rel"]: x["kind"] for x in rows}
check("plan: W1 AR r02 and ADJ-OPP r01 and D islands are in (16 each); the pilot's islands are NOT (its V4 failed in this synthetic input)", sum(1 for r_ in rel if "/island_" in r_ and r_.startswith("GC_W1/6-AR-n200-r02")) == 16 and sum(1 for r_ in rel if r_.startswith("GC_D/") and "/island_" in r_) == 16 and not any(r_.startswith("GC_P/") and "/island_" in r_ for r_ in rel), "\n".join(notes))
check("plan: A files (fit / law / eval) of the verified units are in with a desktop sha; setup.bin only for the A+ runs (P, D, ADJ-OPP r01), never for AR r02", kinds.get("GC_W1/6-AR-n200-r02-V-s1/fit.bin") == "A" and kinds.get("GC_P/6-AR-n200-r01-V-s1/setup.bin") == "A+" and kinds.get("GC_D/6-AR-n1000-r01-V-s1/setup.bin") == "A+" and kinds.get("GC_W1/6-ADJOPP-n200-r01-V-s1/setup.bin") == "A+" and "GC_W1/6-AR-n200-r02-V-s1/setup.bin" not in rel and all(x.get("sha256") for x in rows if x["kind"] in ("A", "A+")), str(sorted(set(kinds.values()))))
check("plan: no calib.bin / data.bin / raw.bin row (Tier 2 stays for the purge); every row passes the fence", not any(r_.endswith(("calib.bin", "data.bin", "raw.bin")) for r_ in rel) and all(F.fence_kind(r_) for r_ in rel), "")
v4w2 = {"GC_W2/6-AR-n200-r03-V-s1": {"ok": True, "files": {"island_%d.bin" % k: [1, 1] for k in range(1, 17)}}}
dv2 = set(dv) - {"gc1m/GC_W2/6-AR-n200-r03-V-s1", "gc1m/GC_W2/_batch_GC_W2"}
rows2, notes2 = T.build_plan(v4w2, dv2); check("plan: a fit whose unit is NOT desktop-verified (V5) gets no island and no A row", not any(x["rel"].startswith("GC_W2/") for x in rows2), "\n".join(notes2))
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
