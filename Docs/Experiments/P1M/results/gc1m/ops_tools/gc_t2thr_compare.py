#!/usr/bin/env python3
"""gc_t2thr_compare.py -- GC_T2THR (HQ H-47, GC_PLAN §11 item 5): the 1M two-thread-count check, REPORT-ONLY. Compares island 1 of the GC_P pilot (96 threads, records/gc1m/GC_P) with the same island re-run at 48 threads
(GC_T2THR, same data.bin / setup.bin / calib.bin / manifest / seed / mem-budget / binary): output_hash, EVERY non-meta section (dtype, dims, sha256) via `smcbvs4 info --meta 1 --record`, the two sidecars outside provenance,
the manifests' recorded input hashes. Writes t2thr.json (ok, hashes, sections equal / differ, walls, cost). Usage: gc_t2thr_compare.py --pilot DIR --rerun DIR --info-bin smcbvs4 --out t2thr.json [--cost-json FILE] [--wall-s N]"""
import argparse, importlib.util, json, os, re, sys, tempfile
spec = importlib.util.spec_from_file_location("cc", "/home/fb31/SMC_Engineering_Department/staging/overlap1e4/tools/cross_check_V.py")
cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
ap = argparse.ArgumentParser(); ap.add_argument("--pilot", required=True); ap.add_argument("--rerun", required=True); ap.add_argument("--info-bin", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--cost-json"); ap.add_argument("--wall-s", type=float); a = ap.parse_args()
J = lambda p: json.load(open(p))
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(a.out)))
sp, hp = cc.sections(a.info_bin, os.path.join(a.pilot, "island_1.bin"), tmp)
sr, hr = cc.sections(a.info_bin, os.path.join(a.rerun, "island_1.bin"), tmp)
side_p, side_r = J(os.path.join(a.pilot, "island_1.bin.json")), J(os.path.join(a.rerun, "island_1.bin.json"))
diff_sec = sorted(k for k in set(sp) | set(sr) if sp.get(k) != sr.get(k))
x = dict(cc.flat(side_p)); y = dict(cc.flat(side_r))
kx = {k for k in x if not cc.DROP.search(k)}; ky = {k for k in y if not cc.DROP.search(k)}
diff_side = ["%s: %r != %r" % (k, x.get(k, "<absent>"), y.get(k, "<absent>")) for k in sorted(kx | ky) if cc.norm(x.get(k, "<absent>")) != cc.norm(y.get(k, "<absent>"))]
mp, mr = J(os.path.join(a.pilot, "manifests", "island_1.json")), J(os.path.join(a.rerun, "manifests", "island_1.json"))
inp_p = {os.path.basename(k): v for k, v in mp["inputs"].items()}; inp_r = {os.path.basename(k): v for k, v in mr["inputs"].items()}
chk = {
    "threads_pilot_96_rerun_48": (mp["params"]["threads"], mr["params"]["threads"]) == (96, 48),
    "same_manifest_params_except_threads": {k: v for k, v in mp["params"].items() if k != "threads"} == {k: v for k, v in mr["params"].items() if k != "threads"},
    "same_input_content_hashes": inp_p == inp_r,
    "output_hash_equal": bool(hp) and hp == hr and side_p.get("output_hash") == side_r.get("output_hash"),
    "sections_equal": not diff_sec and len(sp) > 0 and sorted(sp) == sorted(sr),
    "sidecars_equal_outside_provenance": not diff_side,
    "both_completed": side_p.get("status") == "completed" and side_r.get("status") == "completed",
}
rep = {"tool": "gc_t2thr_compare.py", "check": "two thread counts at 1M (GC_PLAN §11 item 5; ENGINEERING_SPEC §0-v2.6 pilot item)", "island": 1, "report_only": True,
       "pilot": {"threads": mp["params"]["threads"], "output_hash": hp, "sidecar_output_hash": side_p.get("output_hash"), "T": side_p.get("T"), "slurm_job_id": mp["machine"]["slurm_job_id"], "host": mp["machine"]["host"]},
       "rerun": {"threads": mr["params"]["threads"], "output_hash": hr, "sidecar_output_hash": side_r.get("output_hash"), "T": side_r.get("T"), "slurm_job_id": mr["machine"]["slurm_job_id"], "host": mr["machine"]["host"]},
       "checks": chk, "sections": {"n_pilot": len(sp), "n_rerun": len(sr), "differing_sections": diff_sec, "n_equal": len(set(sp) & set(sr)) - len(diff_sec)}, "sidecar_differing_fields": diff_side[:20],
       "input_content_hashes": inp_r, "ok": all(chk.values())}
if a.wall_s: rep["rerun_wall_s"] = a.wall_s
if a.cost_json and os.path.exists(a.cost_json): rep["rerun_cost"] = J(a.cost_json)
json.dump(rep, open(a.out, "w"), indent=1); open(a.out, "a").write("\n")
import shutil; shutil.rmtree(tmp, ignore_errors=True)
print("T2THR:", "PASS: bit-identical (output_hash %s = %s, %d sections equal)" % (hp, hr, len(sp)) if rep["ok"] else "FAIL / DIFFERENCE: " + json.dumps({k: v for k, v in chk.items() if not v}), "| differing sections: %s" % (diff_sec or "none"))
sys.exit(0 if rep["ok"] else 1)
