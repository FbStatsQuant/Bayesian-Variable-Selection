#!/usr/bin/env python3
"""precision_freeze.py -- applies the pre-registered FREEZE RULE of the precision study (PREREG.md section 3) to the leg's records.
Stdlib only (python3.9), read-only, deterministic. It computes the rule's inputs and prints ADOPT / KEEP / NOT_RUN per knob; the Engineering
manager records the outcome, an independent review confirms it (PREREG section 6).

  precision_freeze.py --records ROOT [ROOT ...] --cost-dir DIR [DIR ...] --out OUTDIR

Precision fits only: run ids 4-<design>-n200-r01-P-N<N>-m<m>[-I<i>]-c<1|2>-s1 on the three datasets AR, ARweak, ADJOPP (R' = 64).
Per fit (engine eval record): M1 = fit.meta.occ[M = 1000].sd_log_Z_occ_r (sd over islands of log Z-hat_occ,r; spec target <= 0.05);
  M2 = pip.island_spread.max_sd (max over variables of the sd over islands of the PIP; target <= 0.005); M3 = evidence.sigma_hat (island sd of Z-hat_r / Z-hat; goal <= 0.5).
Per (dataset, cell) value = mean over the 2 replicates; ratio r_X = geometric mean over the datasets of value(X) / value(B), B = (N 2500, m 1, I_max 3).
Cost ratio c_X = mean over the fits of billed islands core-h(X) / the same for B (cost files cost_<run_id>.json, stage `islands`).
RULE (cost-raising knob X = m 4 or N 10^4): ADOPT iff for EACH of M1, M2, M3: r_X <= 1/sqrt(c_X) (the gain beats spending the same extra cost on more islands,
  whose pooled sd falls as 1/sqrt(R')) AND r_X < 1 in EVERY dataset AND the HPM set is the same in every fit of every dataset (X and B). Otherwise KEEP the baseline value.
RULE (cost-saving knob I_max = 0): ADOPT iff for EACH of M1, M2, M3: r <= 1.15 AND r <= 1.30 in every dataset AND HPM identical as above; otherwise KEEP I_max = 3.
Systematic resampling: not testable with the frozen binary (PREREG blocker B3): frozen OFF (D-14). N = 10^4 arms: NOT_RUN unless the fits exist (blocker B2).
"""
import argparse, csv, glob, hashlib, json, math, os, re, sys

RUN = re.compile(r"^4-(?P<d>ARweak|AR|ADJOPP)-n200-r01-P-N(?P<N>\d+)-m(?P<m>\d+)(?:-I(?P<I>\d))?-c(?P<c>[12])-s1$")
EVAL = ("eval.bin.json", "eval.json")


def jl(p):
    return json.load(open(p))


def gmean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def find(roots):
    out = {}
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if not d.startswith(("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log"))]
            ef = next((os.path.join(dp, n) for n in EVAL if n in fns), None)
            if ef is None:
                continue
            try:
                ev = jl(ef)
            except Exception:
                continue
            rid = jl(os.path.join(dp, "run_manifest.json")).get("run_id") if "run_manifest.json" in fns else os.path.basename(dp)
            if "evidence" in ev and RUN.match(rid or "") and (rid not in out or os.path.getmtime(ef) > os.path.getmtime(out[rid][0])):
                out[rid] = (ef, dp, ev)
            dns[:] = []
    return out


def fit_metrics(ev):
    fm = ev.get("fit", {}).get("meta", {})
    m1 = next((e.get("sd_log_Z_occ_r") for e in fm.get("occ", []) or [] if e.get("M") == 1000), None)
    return {"M1": m1, "M2": ev.get("pip", {}).get("island_spread", {}).get("max_sd"), "M3": ev.get("evidence", {}).get("sigma_hat"),
            "hpm": tuple(ev.get("selection", {}).get("hpm", [])), "ok": ev.get("status") == "completed" and ev.get("fit_status", "completed") == "completed",
            "target_pip": ev.get("pip", {}).get("island_spread", {}).get("target_met"), "inhom": ev.get("fit", {}).get("meta", {}).get("flags", {}).get("occ_inhomogeneous")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--cost-dir", nargs="*", default=[]); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    runs = find(a.records)
    cost = {}
    for d in a.cost_dir:
        for p in glob.glob(os.path.join(d, "cost_*.json")):
            j = jl(p); cost[j["run_id"]] = j["stages"].get("islands", {}).get("billed_core_h")
    fits = {}
    for rid, (ef, dp, ev) in runs.items():
        g = RUN.match(rid).groupdict()
        cell = (int(g["N"]), int(g["m"]), int(g["I"]) if g["I"] is not None else 3)
        x = fit_metrics(ev); x["cost"] = cost.get(rid)
        fits.setdefault((g["d"], cell), []).append(x)
    B = (2500, 1, 3)
    cells = sorted({c for _, c in fits})
    dss = sorted({d for d, _ in fits})
    report = {"script_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(), "datasets": dss, "cells": [list(c) for c in cells], "decisions": {}, "detail": {}}
    def val(d, c, k):
        xs = [f[k] for f in fits.get((d, c), []) if f["ok"] and f[k] is not None]
        return sum(xs) / len(xs) if len(xs) == 2 else None            # both replicates delivered, else the dataset is not evaluable
    hpm_all = {d: {f["hpm"] for c in cells for f in fits.get((d, c), []) if f["ok"]} for d in dss}
    hpm_same = all(len(v) == 1 for v in hpm_all.values()) and bool(hpm_all)
    def evaluate(c, kind):
        if c not in cells or B not in cells:
            return "NOT_RUN", {"reason": "arm or baseline fits missing"}
        det = {"hpm_identical": hpm_same}
        ok = hpm_same; rs = {}
        for k in ("M1", "M2", "M3"):
            per = {}
            for d in dss:
                x, b = val(d, c, k), val(d, B, k)
                if x is None or b is None or b <= 0:
                    return "NOT_EVALUATED", {"reason": "metric %s missing for %s" % (k, d)}
                per[d] = x / b
            rs[k] = {"per_dataset": per, "geo_mean": gmean(list(per.values()))}
        cx = None
        num = [f["cost"] for d in dss for f in fits.get((d, c), []) if f["cost"] is not None]
        den = [f["cost"] for d in dss for f in fits.get((d, B), []) if f["cost"] is not None]
        if kind == "up":
            if not num or not den:
                return "NOT_EVALUATED", {"reason": "island cost records missing"}
            cx = (sum(num) / len(num)) / (sum(den) / len(den)); lim = 1.0 / math.sqrt(cx)
            for k in rs:
                ok = ok and rs[k]["geo_mean"] <= lim and all(v < 1.0 for v in rs[k]["per_dataset"].values())
        else:
            for k in rs:
                ok = ok and rs[k]["geo_mean"] <= 1.15 and all(v <= 1.30 for v in rs[k]["per_dataset"].values())
        det.update({"ratios": rs, "cost_ratio": cx, "limit_geo": (1.0 / math.sqrt(cx) if cx else 1.15)})
        return ("ADOPT" if ok else "KEEP"), det
    for name, c, kind in (("m=4", (2500, 4, 3), "up"), ("N=10000 (m=1)", (10000, 1, 3), "up"), ("N=10000 (m=4)", (10000, 4, 3), "up"), ("I_max=0", (2500, 1, 0), "down")):
        r, det = evaluate(c, kind); report["decisions"][name] = r; report["detail"][name] = det
    report["decisions"]["resampling"] = "OFF (systematic not available in the frozen binary; D-14 default)"
    # targets of the baseline-or-adopted arm, reported per fit (spec 0-v2.3; never used to switch estimators)
    tg = {}
    for (d, c), fl in sorted(fits.items()):
        for f in fl:
            tg.setdefault(str(c), []).append({"dataset": d, "M1<=0.05": (f["M1"] <= 0.05) if f["M1"] is not None else None, "M2<=0.005": f["target_pip"], "M3<=0.5": (f["M3"] <= 0.5) if f["M3"] is not None else None, "occ_inhomogeneous": f["inhom"]})
    report["targets_per_fit"] = tg
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "freeze.json"), "w"), indent=1, default=str)
    print(json.dumps({"decisions": report["decisions"], "hpm_identical_everywhere": hpm_same, "script_sha256": report["script_sha256"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
