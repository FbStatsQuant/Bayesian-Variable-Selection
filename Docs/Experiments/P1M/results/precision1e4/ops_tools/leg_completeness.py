#!/usr/bin/env python3
"""leg_completeness.py -- LEG completeness table and the ONE-build check (OPS_PREC; manager 11-19). Read-only, stdlib only.
Per wave: planned fits (waves.json; B1 from its two plans) vs DELIVERED. Delivered = the unit records/precision1e4/<wave>/<run_id>/ exists, exactly one SHA256SUMS and
`sha256sum -c` OK, fit.bin present (no INCOMPLETE.txt), eval.bin.json status and fit_status completed, every stage of the fit COMPLETED in the batch cost record, and
evidence.logZ_r has R' finite values. Build identity: every `binary.sha256` in every json record of every unit (log/, cost/, manifests/ excluded) equals the leg's V build
(first BUILD line of deploy_leg.log); B1's T fits equal the BUILD_T line. Prints the science total delivered / 170 (PREREG §2: >= 95 %)."""
import glob, hashlib, json, os, subprocess, sys
REC = "/home/fb31/SMC_Engineering_Department/records/precision1e4"; STG = "/home/fb31/SMC_Engineering_Department/staging/precision1e4"
ORDER = ["A0", "P1", "P2", "P3", "P4", "B1", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
leg = {}
for l in open(STG + "/deploy_leg.log"):
    f = l.rstrip("\n").split("\t")
    if len(f) > 3 and f[2] in ("BUILD", "BUILD_T") and f[2] not in leg: leg[f[2]] = f[3]
planned = {w: [] for w in ORDER}
for w, x in json.load(open(STG + "/waves.json")).items():
    if w in planned:
        for b in x["batches"]: planned[w] += [(f["run_id"], f["Rp"], b["batch"]) for f in b["fits"]]
for b in ("PL_B1_1", "PL_B1_2"):
    p = json.load(open("%s/current/scripts/%s/plan.resolved.json" % (STG, b))); planned["B1"] += [(f["run_id"], f["Rp"], b) for f in p["fits"]]
def sha_ok(u):
    r = subprocess.run(["sha256sum", "--quiet", "-c", "SHA256SUMS"], cwd=u, capture_output=True)
    n = sum(1 for _, _, fs in os.walk(u) for f in fs if f.startswith("SHA256SUMS"))
    return r.returncode == 0 and n == 1
print("%-4s %7s %9s %-9s  %s" % ("wave", "planned", "delivered", "build ok", "not delivered / issues"))
tot_p = tot_d = sci_p = sci_d = vf_p = vf_d = 0; allbad = []
for w in ORDER:
    d = ok_b = 0; issues = []
    for rid, rp, b in planned[w]:
        u = "%s/%s/%s" % (REC, w, rid); why = None
        if not os.path.isdir(u): why = "no unit"
        elif not sha_ok(u): why = "sha256sum -c / SHA256SUMS count"
        elif os.path.exists(u + "/INCOMPLETE.txt") or not os.path.exists(u + "/fit.bin"): why = "no fit.bin"
        else:
            ev = json.load(open(u + "/eval.bin.json"))
            lz = (ev.get("evidence") or {}).get("logZ_r") or []
            cj = "%s/_batch_%s/cost/cost_%s.json" % (REC + "/" + w, b, rid)
            states = {s for v in json.load(open(cj))["stages"].values() for s in v["states"]} if os.path.exists(cj) else {"missing cost record"}
            if ev.get("status") != "completed" or ev.get("fit_status") != "completed": why = "eval status %s / %s" % (ev.get("status"), ev.get("fit_status"))
            elif len(lz) != rp or not all(abs(x) < 1e9 for x in lz): why = "logZ_r length %d != R' %d" % (len(lz), rp)
            elif states != {"COMPLETED"}: why = "stage states %s" % sorted(states)
        if why: issues.append("%s: %s" % (rid, why))
        else: d += 1
        # build identity: every binary.sha256 in the unit's json records
        want = leg["BUILD_T"] if (w == "B1" and "-T-" in rid) else leg["BUILD"]; seen = set()
        if os.path.isdir(u):
            for p in glob.glob(u + "/*.json") + glob.glob(u + "/*/*.json"):
                if "/log/" in p or "/cost/" in p or "/manifests/" in p: continue
                def walk(o):
                    if isinstance(o, dict):
                        if isinstance(o.get("binary"), dict) and "sha256" in o["binary"]: seen.add(o["binary"]["sha256"])
                        for v in o.values(): walk(v)
                    elif isinstance(o, list):
                        for v in o: walk(v)
                walk(json.load(open(p)))
        if seen == {want}: ok_b += 1
        else: allbad.append((w, rid, sorted(x[:12] for x in seen)))
    tot_p += len(planned[w]); tot_d += d
    if w.startswith("S"): sci_p += len(planned[w]); sci_d += d; vf_p += sum('-VF-' in r for r, _, _ in planned[w]); vf_d += sum(('-VF-' in r) and not any(i.startswith(r + ':') for i in issues) for r, _, _ in planned[w])
    print("%-4s %7d %9d %-9s  %s" % (w, len(planned[w]), d, "%d/%d" % (ok_b, len(planned[w])), "; ".join(issues) or "-"))
print("\nTOTAL planned %d, delivered %d (A0 + P1-P4 + B1 + S1-S10)" % (tot_p, tot_d))
print("SCIENCE (S1-S10): delivered %d / planned %d (the plan's 170 = 156 new + 14 VF) = %.1f %% (PREREG §2: >= 95 %% = >= 162 of 170 needed)" % (sci_d, sci_p, 100.0 * sci_d / sci_p))
print("   of which new fits %d / %d (PREREG §2 wording: >= 95 %% of the 156 new fits = >= 149) and the VF re-runs %d / %d" % (sci_d - vf_d, sci_p - vf_p, vf_d, vf_p))
print("BUILD: V BUILD %s.. (every non-T fit), BUILD_T %s.. (B1 T fits); units whose binary.sha256 set differs: %d" % (leg["BUILD"][:16], leg["BUILD_T"][:16], len(allbad)))
for x in allbad[:10]: print("  ", x)
