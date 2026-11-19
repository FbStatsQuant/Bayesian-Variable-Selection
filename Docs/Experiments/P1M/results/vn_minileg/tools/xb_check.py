#!/usr/bin/env python3
"""xb_check.py --a <XB unit> --b <overlap unit> [--info-bin smcbvs4] [--show-dropped]  -- A0 XB cross-build bit check (LEG_PLAN §6.4 (9), R7).
A = records/precision1e4/A0/4-AR-n200-r01-V-XB-s1 (the leg build), B = records/overlap1e4/W0/4-AR-n200-r01-V-s1 (the overlap fit; also run against W0's ...V-s1.V2).
Same data, seed, config, plan. Checks (each printed PASS/FAIL with the evidence):
  1 all 16 evidence.logZ_r (eval.bin.json) bit-equal (float64 repr);  2 selection.hpm equal;  3 every island output_hash (island_r.bin.json, r = 1..16) equal;
  4 every *.bin.json sidecar and truth.json, flattened, EXACTLY equal after dropping provenance keys (binary block, git_commit, input file hashes, paths, batch names,
    timings / seconds / cost / host / threads, mem plans; the dropped key paths are listed with --show-dropped) = the identical() comparison of all non-provenance fields;
  5 with --info-bin: fit.bin and eval.bin sections (name, dtype, dims, sha256, all but `meta`) equal through `smcbvs4 info <file> --meta 1 --record` (the freeze_check_1e5.sh method).
Exit 0 = bit-identical outside provenance, 1 = a difference. Stdlib only. Scratch for the info records: $PREC_TEST_TMP or <records>/../.xb_tmp (removed)."""
import argparse, glob, importlib.util, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cc", "/home/fb31/SMC_Engineering_Department/staging/overlap1e4/tools/cross_check_V.py")
cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
import re
_norm0 = cc.norm
def _norm(v):   # a path value is provenance: scratch/runs/<batch>/<run_id>/ differs by design between the two batches (e.g. raw.bin.json "raw")
    v = _norm0(v)
    return re.sub(r"scratch/runs/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/", "scratch/runs/<BATCH>/<RUN>/", v) if isinstance(v, str) else v
cc.norm = _norm

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--a", required=True); ap.add_argument("--b", required=True)
    ap.add_argument("--info-bin"); ap.add_argument("--show-dropped", action="store_true"); ap.add_argument("--tmp", default=None)
    a = ap.parse_args(); A, B = a.a.rstrip("/"), a.b.rstrip("/"); res = []
    def rep(name, ok, ev): res.append(ok); print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, ev))
    ea, eb = json.load(open(A + "/eval.bin.json")), json.load(open(B + "/eval.bin.json"))
    la, lb = ea["evidence"]["logZ_r"], eb["evidence"]["logZ_r"]
    rep("1 evidence.logZ_r bit-equal", len(la) == len(lb) == 16 and all(repr(x) == repr(y) for x, y in zip(la, lb)), "%d vs %d values; equal %d/16; first %r vs %r" % (len(la), len(lb), sum(repr(x) == repr(y) for x, y in zip(la, lb)), la[0], lb[0]))
    rep("2 selection.hpm equal", ea["selection"]["hpm"] == eb["selection"]["hpm"], "%s vs %s" % (ea["selection"]["hpm"], eb["selection"]["hpm"]))
    ha = {int(os.path.basename(p)[7:-9]): json.load(open(p)).get("output_hash") for p in glob.glob(A + "/island_*.bin.json")}
    hb = {int(os.path.basename(p)[7:-9]): json.load(open(p)).get("output_hash") for p in glob.glob(B + "/island_*.bin.json")}
    rep("3 island output_hash r = 1..16", sorted(ha) == sorted(hb) == list(range(1, 17)) and ha == hb, "%d islands vs %d; equal %d; e.g. r1 %s vs %s" % (len(ha), len(hb), sum(ha[r] == hb.get(r) for r in ha), ha.get(1), hb.get(1)))
    nfile = ndrop = bad = 0; diffs = []
    for p in sorted(glob.glob(A + "/*.json") + glob.glob(A + "/*/*.json")):
        f = os.path.relpath(p, A)
        if f.startswith(("log/", "cost/", "manifests/")) or f in ("run_manifest.json", "calib_meta.json"):
            continue
        q = os.path.join(B, f)
        if not os.path.exists(q):
            diffs.append("%s: absent in B" % f); continue
        x = dict(cc.flat(json.load(open(p)))); y = dict(cc.flat(json.load(open(q))))
        kx = {k for k in x if not cc.DROP.search(k)}; ky = {k for k in y if not cc.DROP.search(k)}
        dropped = sorted((set(x) | set(y)) - (kx | ky)); ndrop += len(dropped); nfile += 1
        if a.show_dropped: print("  dropped in %s: %s" % (f, ", ".join(dropped)[:300]))
        for k in sorted(kx | ky):
            if cc.norm(x.get(k, "<absent>")) != cc.norm(y.get(k, "<absent>")):
                diffs.append("%s %s: %r != %r" % (f, k, x.get(k, "<absent>"), y.get(k, "<absent>"))); bad += 1
    fb = {os.path.relpath(p, B) for p in glob.glob(B + "/*.json") + glob.glob(B + "/*/*.json") if not os.path.relpath(p, B).startswith(("log/", "cost/", "manifests/")) and os.path.relpath(p, B) not in ("run_manifest.json", "calib_meta.json")}
    fa = {os.path.relpath(p, A) for p in glob.glob(A + "/*.json") + glob.glob(A + "/*/*.json") if not os.path.relpath(p, A).startswith(("log/", "cost/", "manifests/")) and os.path.relpath(p, A) not in ("run_manifest.json", "calib_meta.json")}
    diffs += ["%s: only in %s" % (f, "A" if f in fa else "B") for f in sorted(fa ^ fb)]
    rep("4 sidecars identical outside provenance", not diffs and nfile >= 20, "%d json files compared (fit, eval, calib, setup, data, truth, 16 islands); %d provenance keys dropped; %d differing field(s)%s" % (nfile, ndrop, bad, "".join("\n      " + d for d in diffs[:12])))
    if a.info_bin:
        tmp = a.tmp or os.path.join(os.path.dirname(os.path.abspath(A)), ".xb_tmp"); os.makedirs(tmp, exist_ok=True)
        for fn in ("fit.bin", "eval.bin"):
            sa, ha_ = cc.sections(a.info_bin, os.path.join(A, fn), tmp); sb, hb_ = cc.sections(a.info_bin, os.path.join(B, fn), tmp)
            d = sorted(k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k))
            rep("5 %s sections (all but meta) equal via info" % fn, not d and ha_ == hb_ and len(sa) > 0, "%d sections; output_hash %s vs %s; differing: %s" % (len(sa), ha_, hb_, d or "none"))
        shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT:", "BIT-IDENTICAL outside provenance" if all(res) else "DIFFERENCE FOUND"); sys.exit(0 if all(res) else 1)
if __name__ == "__main__":
    main()
