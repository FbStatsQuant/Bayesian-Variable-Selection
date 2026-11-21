#!/usr/bin/env python3
"""gc_tier1.py -- Tier-1 cleanup of the 1M block's NOTS scratch (HQ H-56): builds the deletion plan on Owls from (V1-V4: the detached V4 result of gc_v4_check.py on NOTS; V5: crews/offload/desktop_verified.txt; A / A+: the desktop unit's
SHA256SUMS) and runs the fenced deleter (gc_fence.py) on NOTS. Called by `nots_wave_hygiene_check.py --plan-gc-tier1 | --apply-gc-tier1`. Never touches anything outside the fence (gc_fence.fence_kind); Tier 2 (calib / data / raw / non-A+ setup) is not in the plan.
A fit's islands are in the plan only if: its V4 passed (all 16 island files info --verify'd, content hash == island sidecar == fit.bin.json inputs, sizes = headers), its merge / eval stages are COMPLETED and the eval record has logZ_r of length 16 (V1 / V2), and its unit AND its batch unit are in desktop_verified.txt (V5)."""
import json, os, subprocess, sys, time
H = "/home/fb31/SMC_Engineering_Department"; REC = H + "/records"; DV = H + "/crews/offload/desktop_verified.txt"; HERE = H + "/crews/home_hygiene"
STG = H + "/staging/gc1m"; sys.path.insert(0, HERE)
import gc_fence

def ssh(cmd, timeout=900):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "nots", "nice -n19 bash -s"], input=cmd, capture_output=True, text=True, timeout=timeout)

def v1_v2(unit_dir, batch_unit, run_id):
    """V1: merge and eval COMPLETED (cost record), fit.bin.json status completed; V2: eval logZ_r length 16 and finite"""
    c = json.load(open(os.path.join(batch_unit, "cost", "cost_%s.json" % run_id)))
    st = c["stages"]; ok1 = all(st[k]["states"] == ["COMPLETED"] for k in ("merge", "eval")) and json.load(open(os.path.join(unit_dir, "fit.bin.json"))).get("status") == "completed"
    lz = json.load(open(os.path.join(unit_dir, "eval.bin.json")))["evidence"]["logZ_r"]
    return ok1, len(lz) == 16 and all(isinstance(x, (int, float)) and x == x and abs(x) != float("inf") for x in lz)

def build_plan(v4, dv, rec=REC, stg=STG):
    rows, notes = [], []
    for br, r in sorted(v4.items()):
        b, run = br.split("/"); unit = "gc1m/%s/%s" % (b, run); bunit = "gc1m/%s/_batch_%s" % (b, b)
        ud, bd = os.path.join(rec, unit), os.path.join(rec, bunit)
        v5 = unit in dv and bunit in dv
        try: ok1, ok2 = v1_v2(ud, bd, run)
        except Exception as e: ok1 = ok2 = False; notes.append("%s: V1/V2 unreadable (%s)" % (br, e))
        isl = bool(r.get("ok")) and ok1 and ok2 and v5
        notes.append("%s: V1 %s V2 %s V4 %s V5 %s -> islands %s" % (br, ok1, ok2, "OK" if r.get("ok") else "FAIL: %s" % r.get("problems", [])[:1], v5, "IN the plan" if isl else "NOT in the plan"))
        if isl:
            for f, (size, mt) in sorted(r["files"].items()):
                rows.append({"rel": "%s/%s/%s" % (b, run, f), "kind": "island", "size": size, "mtime_ns": mt, "why": "class C: V1-V5 pass (V4 info --verify 1 on NOTS; unit + batch unit desktop-verified)"})
        if v5:
            sums = {}
            for l in open(os.path.join(ud, "SHA256SUMS")):
                h, _, f = l.rstrip("\n").partition("  ")
                if "/" not in f: sums[f] = h
            for f in ("fit.bin", "law.bin", "eval.bin", "setup.bin"):
                if f not in sums or not os.path.isfile(os.path.join(ud, f)): continue
                kind = gc_fence.fence_kind("%s/%s/%s" % (b, run, f))
                if kind is None: continue   # setup.bin of a non-A+ run, or not in the fence: never in the plan
                rows.append({"rel": "%s/%s/%s" % (b, run, f), "kind": kind, "size": os.path.getsize(os.path.join(ud, f)), "sha256": sums[f], "why": "%s: NOTS copy of a file with a sha-verified desktop copy (unit SHA256SUMS)" % kind})
    # the T2THR re-run island: its unit is verified and t2thr.json says ok; the island file itself is on Owls staging (sha compared on NOTS)
    t2 = "gc1m/T2THR"; sp = os.path.join(stg, "_t2thr", "6-AR-n200-r01-V-s1", "island_1.bin")
    if t2 in dv and os.path.isfile(sp) and json.load(open(os.path.join(rec, t2, "t2thr.json"))).get("ok"):
        h = gc_fence.sha256(sp); rows.append({"rel": "GC_T2THR/6-AR-n200-r01-V-s1/island_1.bin", "kind": "island", "size": os.path.getsize(sp), "sha256": h, "why": "class C: the T2THR re-run island (unit desktop-verified, t2thr.json ok, bit-identical to the pilot's island 1; Owls staging copy sha-equal)"})
        notes.append("T2THR: unit verified, t2thr.json ok, Owls staging copy %s -> island in the plan" % h[:12])
    else: notes.append("T2THR: NOT in the plan (unit not verified or no staging copy)")
    return rows, notes

def run(apply, only=None):
    dv = set(l.strip() for l in open(DV))
    r = ssh("cat %s/scratch/gc_v4_result.json" % H); v4 = json.loads(r.stdout)
    if only: v4 = {k: v for k, v in v4.items() if k.split("/")[0] in only}
    rows, notes = build_plan(v4, dv)
    bad = [x for x in rows if gc_fence.fence_kind(x["rel"]) is None]
    assert not bad, "the plan contains rows outside the fence: %s" % bad[:3]
    plan = STG + "/gc_tier1_plan%s.json" % ("_" + "_".join(sorted(only)) if only else ""); json.dump(rows, open(plan, "w"), indent=1)
    gb = sum(x["size"] for x in rows) / 1e9
    print("\n".join(notes)); print("plan: %d files, %.2f GB (%s)" % (len(rows), gb, "APPLY" if apply else "dry run")); print("by kind:", {k: round(sum(x["size"] for x in rows if x["kind"] == k) / 1e9, 2) for k in sorted({x["kind"] for x in rows})})
    # ship the fence + plan; run detached on NOTS; poll
    tag = time.strftime("%Y%m%dT%H%M%S")
    ssh("cat > %s/scratch/gc_fence.py <<'EOF_F'\n%s\nEOF_F\ncat > %s/scratch/gc_tier1_plan_%s.json <<'EOF_P'\n%s\nEOF_P\n" % (H, open(HERE + "/gc_fence.py").read(), H, tag, json.dumps(rows)))
    out = "%s/scratch/gc_tier1_result_%s.json" % (H, tag)
    ssh("cd %s/scratch && setsid nohup bash -c 'nice -n 19 ionice -c3 python3 -I gc_fence.py --plan gc_tier1_plan_%s.json %s > %s 2> %s.err; echo $? > %s.rc' > /dev/null 2>&1 < /dev/null &\n" % (H, tag, "--apply" if apply else "", out, out, out))
    for _ in range(120):
        time.sleep(150); rc = ssh("cat %s.rc 2>/dev/null" % out).stdout.strip()
        if rc != "": break
    if rc != "0": sys.exit("NOTS deleter did not finish cleanly (rc '%s'): see %s.err" % (rc, out))
    res = json.loads(ssh("cat %s" % out).stdout)
    from collections import Counter
    c = Counter(x["status"] for x in res); sz = Counter()
    for x in res: sz[x["status"]] += x.get("size") or 0
    print("result:", dict(c), {k: round(v / 1e9, 2) for k, v in sz.items()}); refused = [x for x in res if x["status"] == "REFUSED"]
    for x in refused[:10]: print("REFUSED", x["rel"], x["reason"])
    json.dump(res, open(STG + "/gc_tier1_result_%s.json" % tag, "w"), indent=1)
    if apply:
        with open(HERE + "/nots_scratch_removals.tsv", "a") as f:
            for x in res:
                if x["status"] == "DELETED": f.write("\t".join([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "1", "gc-tier1", "%s/scratch/runs/%s" % (H, x["rel"]), str(x["size"]), "-", "-", "GC tier-1 (V1-V5 / desktop sha) H-56"]) + "\n")
    return res
