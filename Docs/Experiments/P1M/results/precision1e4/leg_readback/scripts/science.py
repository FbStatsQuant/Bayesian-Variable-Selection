#!/usr/bin/env python3
"""science.py -- descriptive read-back of the 10^4 science (PREREG section 5) for the precision1e4 leg.  NO pass/fail; no thresholds.

  python3 -I science.py --records ~/SMC_Engineering_Department/records/precision1e4 --costs costs.json --out OUT

READ-ONLY on the records.  Reads the engine eval record (eval.bin.json), truth.json, calib_meta.json, island_1.bin.json and, for the paired
comparisons (A3, second seed), the fit.bin section pip_eq through the UNCHANGED reader of compare_overlap_v2.py (sha 4f402e51...,
read_sections, verify off: sha256sum -c of every unit was already done at collection).
Unit of inference = the DATASET (design, n, rep): fits of one dataset (the two engine seeds at AR n = 200) are averaged first.
  continuous quantities : mean over datasets, sd, 95% t interval (df = datasets - 1, scipy.stats.t), min/max
  proportions           : dataset-level fractions averaged; Wilson 95% interval with n = number of datasets (fractional successes)
  slope of log d_H^2 on log n : OLS on log(mean over datasets) per n; 95% percentile interval of a dataset bootstrap within each n
                          (B = 4000, numpy default_rng seed 20261119)
  reliability curve     : pooled over fits; observed frequency per bin with a percentile interval of a dataset-cluster bootstrap
Science cells = tags V and VF (all run at the frozen configuration N 2,500, m 1, I_max 0); the A3 fits (tags A3, A3F) are analysed
separately against the default-partition fit of the same dataset and engine seed 1.
"""
import argparse, csv, glob, importlib.util, json, math, os, re, sys
import numpy as np
from scipy import stats

CO = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/overlap1e4/compare_overlap_v2.py"
RUN = re.compile(r"^4-(?P<design>AR|ARweak|IND|BLK|ADJOPP|NULL)-n(?P<n>\d+)-r(?P<rep>\d+)-(?P<tag>V|VF|A3F|A3)(?:-exactlink)?-s(?P<seed>\d+)$")
WAVES = ["S%d" % i for i in range(1, 11)]
DESIGNS = ["AR", "ARweak", "IND", "BLK", "ADJOPP", "NULL"]
NAMES = {"AR": "AR-strong", "ARweak": "AR-weak", "IND": "IND", "BLK": "BLK", "ADJOPP": "ADJ-OPP", "NULL": "NULL"}
RNG_SEED = 20261119
B_BOOT = 4000


# ------------------------------------------------------------------ statistics helpers (self-tested in test_science_helpers.py)
def tci(vals):
    """mean, sd, lo, hi of the 95% t interval over the given (dataset-level) values."""
    v = [x for x in vals if x is not None and math.isfinite(x)]
    n = len(v)
    if n == 0:
        return None
    m = sum(v) / n
    if n == 1:
        return {"n": 1, "mean": m, "sd": None, "lo": None, "hi": None, "min": m, "max": m}
    s = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1))
    h = stats.t.ppf(0.975, n - 1) * s / math.sqrt(n)
    return {"n": n, "mean": m, "sd": s, "lo": m - h, "hi": m + h, "min": min(v), "max": max(v)}


def wilson(p, n, z=1.959964):
    """Wilson score interval for a (fractional) proportion p on n clusters."""
    if n == 0:
        return (None, None)
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def ols_slope(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    xm, ym = xs.mean(), ys.mean()
    return float(((xs - xm) * (ys - ym)).sum() / ((xs - xm) ** 2).sum())


def boot_slope(by_n, rng, B=B_BOOT):
    """by_n: {n: [dataset-level values]}.  Point slope of log(mean) on log n and the percentile interval of a dataset bootstrap within each n."""
    ns = sorted(by_n)
    if len(ns) < 2 or any(len(by_n[n]) == 0 or min(by_n[n]) <= 0 for n in ns):
        return None
    lx = [math.log(n) for n in ns]
    pt = ols_slope(lx, [math.log(float(np.mean(by_n[n]))) for n in ns])
    arr = {n: np.asarray(by_n[n], float) for n in ns}
    sl = np.empty(B)
    for b in range(B):
        ly = [math.log(float(rng.choice(arr[n], size=len(arr[n]), replace=True).mean())) for n in ns]
        sl[b] = ols_slope(lx, ly)
    return {"slope": pt, "lo": float(np.percentile(sl, 2.5)), "hi": float(np.percentile(sl, 97.5)), "ns": ns, "datasets": {n: len(by_n[n]) for n in ns}}


def cluster_boot_ratio(clusters, rng, B=B_BOOT):
    """clusters: list of (n_true, n) per dataset for ONE bin.  Observed frequency sum(n_true)/sum(n) and a dataset-cluster bootstrap interval."""
    a = np.asarray(clusters, float)
    tot = a[:, 1].sum()
    if tot == 0:
        return None
    pt = a[:, 0].sum() / tot
    k = len(a)
    out = []
    for _ in range(B):
        idx = rng.integers(0, k, size=k)
        d = a[idx, 1].sum()
        if d > 0:
            out.append(a[idx, 0].sum() / d)
    return {"obs": float(pt), "lo": float(np.percentile(out, 2.5)), "hi": float(np.percentile(out, 97.5))} if out else {"obs": float(pt), "lo": None, "hi": None}


def fmt(x, nd=4, sci=False):
    if x is None:
        return "NA"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    if sci or (x != 0 and abs(x) < 10 ** -(nd - 1)):
        return "%.*e" % (max(nd - 2, 1), x)
    return "%.*f" % (nd, x)


def ci_str(t, nd=4, sci=False):
    if t is None:
        return "NA"
    if t["lo"] is None:
        return "%s" % fmt(t["mean"], nd, sci)
    return "%s [%s, %s]" % (fmt(t["mean"], nd, sci), fmt(t["lo"], nd, sci), fmt(t["hi"], nd, sci))


# ------------------------------------------------------------------ record reading
def jload(p):
    with open(p) as fh:
        return json.load(fh)


def dig(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d


def load_fits(recs_root, costs):
    cost = {r["rid"]: r for r in costs}
    fits = []
    for w in WAVES:
        for n in sorted(os.listdir(os.path.join(recs_root, w))):
            m = RUN.match(n)
            if not m:
                continue
            dp = os.path.join(recs_root, w, n)
            ev = jload(os.path.join(dp, "eval.bin.json"))
            tr = jload(os.path.join(dp, "truth.json"))
            cm = jload(os.path.join(dp, "calib_meta.json"))["meta"]
            isl = jload(os.path.join(dp, "island_1.bin.json"))
            sel, pipd, dist, evd = ev["selection"], ev["pip"], ev["dist"], ev["evidence"]
            fl = dig(ev, "fit", "meta", "flags", default={})
            T = dist["T"]
            s0 = tr["spec"]["s0"] if tr["spec"].get("a", 1) != 0 else 0
            f = {"run_id": n, "wave": w, "dir": dp, "design": m["design"], "n": int(m["n"]), "rep": int(m["rep"]), "tag": m["tag"], "seed": int(m["seed"]),
                 "s0": len(tr["S0"]), "p": tr["spec"]["p"], "status_ok": ev["status"] == "completed" and ev["fit_status"] == "completed",
                 "cfg": (cm["N"], cm["refine_m"], cm["I_max"], cm["I_used"], cm["rule"]), "island_T": isl["T"], "build": dig(ev, "binary", "sha256"),
                 # C2
                 "outcome": sel["outcome_class"], "hpm_eq": bool(sel["hpm_eq_S0"]), "mpm_eq": bool(sel["mpm_eq_S0"]), "hpm_ham": sel["hpm_hamming"], "mpm_ham": sel["mpm_hamming"],
                 "hpm_tp": sel["hpm_tp"], "hpm_fp": sel["hpm_fp"], "hpm_fn": sel["hpm_fn"], "mpm_tp": sel["mpm_tp"], "mpm_fp": sel["mpm_fp"], "mpm_fn": sel["mpm_fn"],
                 "hpm_size": sel["hpm_size"], "S0_in_store": sel["S0_in_store"], "dF_hpm_S0": sel["F_hpm_minus_F_S0"], "phase": sel["prov_hpm_phase"], "mech": sel["prov_hpm_mech"],
                 "F_hpm": sel["F_hpm"], "hpm": sel["hpm"], "mpm": sel["mpm"],
                 # C4
                 "sup_null_eq": dig(pipd, "eq", "sup_null"), "min_true_eq": dig(pipd, "eq", "min_true"), "sup_null_Z": dig(pipd, "Z", "sup_null"), "min_true_Z": dig(pipd, "Z", "min_true"),
                 "brier_eq": dig(pipd, "eq", "brier"), "n_null_gt_0.1": dig(pipd, "eq", "n_null_gt_0.1"), "n_null_gt_0.5": dig(pipd, "eq", "n_null_gt_0.5"),
                 "max_Z_minus_eq": pipd.get("max_abs_Z_minus_eq"), "isl_pip_max_sd": dig(pipd, "island_spread", "max_sd"), "reliability": dig(pipd, "eq", "reliability"),
                 # C5
                 "h2_H": dig(dist, "H", "plugin", "h2"), "h2_M": dig(dist, "M", "plugin", "h2"), "h2_T": dig(T, "predictive", "h2"), "h2_T_se_x": dig(T, "predictive", "h2_se_x"),
                 "h2_T_se_tail": dig(T, "predictive", "h2_se_tail"), "h2_oracle": dig(dist, "oracle", "predictive", "h2"), "post_q05": dig(T, "post_dH", "q05"),
                 "post_q50": dig(T, "post_dH", "q50"), "post_q95": dig(T, "post_dH", "q95"), "post_mean": dig(T, "post_dH", "mean"),
                 "mse_T": dig(T, "test", "mse"), "mlpd_T": dig(T, "test", "mlpd"), "mse_or": dig(dist, "oracle", "test", "mse"), "mlpd_or": dig(dist, "oracle", "test", "mlpd"),
                 "ratio_h2_T": dig(dist, "ratio_to_oracle", "T", "predictive_h2"), "omitted_mass": dig(T, "law_truncation", "omitted_mass"), "dropped_mass_T": T.get("dropped_mass"),
                 "pred_exact": dig(T, "predictive", "exact"),
                 # C7
                 "logZ": evd["logZ"], "logZ_T": evd["logZ_T"], "logZ_minus_T": evd.get("logZ_minus_logZ_T"), "sigma_hat": evd["sigma_hat"], "sigma_rob": evd.get("sigma_hat_robust"),
                 "max_minus_med": evd.get("max_minus_median"), "R_eff": evd.get("R_eff"), "Rp": dig(ev, "fit", "meta", "Rp"), "occ_sd1000": dig(evd, "logZ_occ", "sd_over_islands", "M1000"),
                 "logZ_occ1000": dig(evd, "logZ_occ", "M1000"), "logZ_r": evd["logZ_r"],
                 "flags": {k: v for k, v in fl.items()}, "calib_flags": cm.get("flags", {}), "pi_T_hat": dig(ev, "store", "pi_T_hat"),
                 "core_h": cost[n]["core_h"] if n in cost else None, "stage_h": cost[n]["stages"] if n in cost else None,
                 "wall": cost[n]["wall"] if n in cost else None, "rss": cost[n]["rss"] if n in cost else None}
            f["occ_inhom"] = bool(fl.get("occ_inhomogeneous"))
            fits.append(f)
    return fits


def load_co():
    sp = importlib.util.spec_from_file_location("co", CO)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def pip_eq(co, dp):
    s = co.read_sections(os.path.join(dp, "fit.bin"), ["pip_eq"], verify=False)
    return list(s["pip_eq"][0])


# ------------------------------------------------------------------ aggregation
def by_dataset(fits, key, fn=None):
    """dataset-level mean of key (or fn(fit)) over the fits of a dataset."""
    g = {}
    for f in fits:
        v = fn(f) if fn else f[key]
        if v is None:
            continue
        g.setdefault(f["rep"], []).append(float(v))
    return {r: sum(v) / len(v) for r, v in g.items()}


def prop(fits, fn):
    d = by_dataset(fits, None, lambda f: 1.0 if fn(f) else 0.0)
    n = len(d)
    if n == 0:
        return None
    p = sum(d.values()) / n
    lo, hi = wilson(p, n)
    return {"p": p, "n_ds": n, "lo": lo, "hi": hi, "k_fits": sum(1 for f in fits if fn(f)), "n_fits": len(fits)}


def pstr(x):
    return "NA" if x is None else "%.2f [%.2f, %.2f] (%d/%d fits; %d ds)" % (x["p"], x["lo"], x["hi"], x["k_fits"], x["n_fits"], x["n_ds"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--costs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = np.random.default_rng(RNG_SEED)
    co = load_co()
    fits = load_fits(a.records, jload(a.costs))
    sci = [f for f in fits if f["tag"] in ("V", "VF")]
    a3 = [f for f in fits if f["tag"] in ("A3", "A3F")]
    res = {"n_fits_read": len(fits), "science_V_VF": len(sci), "A3": len(a3)}
    L = []
    P = L.append

    # ---------- 0. inventory + identity
    cfgs = {}
    for f in fits:
        cfgs[f["cfg"]] = cfgs.get(f["cfg"], 0) + 1
    builds = {}
    for f in fits:
        builds[f["build"]] = builds.get(f["build"], 0) + 1
    P("## S0. Inventory and identity (read from the eval / calib_meta records)")
    P("fits read: %d (V/VF %d, A3/A3F %d); not completed: %d; recorded arm (N, m, I_max, I_used, rule): %s; binary sha256: %s" % (
        len(fits), len(sci), len(a3), sum(1 for f in fits if not f["status_ok"]), cfgs, {k[:12]: v for k, v in builds.items()}))
    cells = {}
    for f in sci:
        cells.setdefault((f["design"], f["n"]), []).append(f)
    P("")
    P("| design | n | fits | datasets | tags | s0 | engine seeds |")
    P("|---|---|---|---|---|---|---|")
    order = [(d, n) for d in DESIGNS for n in (100, 200, 400, 800) if (d, n) in cells]
    for d, n in order:
        fs = cells[(d, n)]
        P("| %s | %d | %d | %d | %s | %s | %s |" % (NAMES[d], n, len(fs), len({f["rep"] for f in fs}), ",".join("%s %d" % (t, sum(1 for f in fs if f["tag"] == t)) for t in sorted({f["tag"] for f in fs})),
                                                   sorted({f["s0"] for f in fs}), sorted({f["seed"] for f in fs})))
    res["cells"] = {"%s n%d" % (d, n): len(cells[(d, n)]) for d, n in order}

    # ---------- 1. C2
    P("")
    P("## S1. C2 reported model = S0 (per cell; dataset-clustered; NULL: S0 = empty)")
    P("| design | n | P(HPM = S0) | outcome classes (fits) | mean Hamming HPM | HPM TP / FP / FN (mean per fit) | P(MPM = S0) | MPM TP / FP (mean) | HPM phase (fits) |")
    P("|---|---|---|---|---|---|---|---|---|")
    c2 = {}
    for d, n in order:
        fs = cells[(d, n)]
        oc = {}
        for f in fs:
            oc[f["outcome"]] = oc.get(f["outcome"], 0) + 1
        ph = {}
        for f in fs:
            ph[f["phase"]] = ph.get(f["phase"], 0) + 1
        ham = tci(list(by_dataset(fs, "hpm_ham").values()))
        m = lambda k: sum(f[k] for f in fs) / len(fs)
        c2["%s n%d" % (d, n)] = {"P_hpm": prop(fs, lambda f: f["hpm_eq"]), "P_mpm": prop(fs, lambda f: f["mpm_eq"]), "outcomes": oc, "phase": ph, "hamming": ham,
                                   "hpm_tp_fp_fn": [m("hpm_tp"), m("hpm_fp"), m("hpm_fn")], "mpm_tp_fp": [m("mpm_tp"), m("mpm_fp")]}
        r = c2["%s n%d" % (d, n)]
        P("| %s | %d | %s | %s | %s | %.2f / %.2f / %.2f | %s | %.2f / %.2f | %s |" % (NAMES[d], n, pstr(r["P_hpm"]), ", ".join("%s %d" % kv for kv in sorted(oc.items())), ci_str(ham, 2),
                                                                                       *r["hpm_tp_fp_fn"], pstr(r["P_mpm"]), *r["mpm_tp_fp"], ", ".join("%s %d" % kv for kv in sorted(ph.items()))))
    res["C2"] = c2
    # HPM != S0 detail
    P("")
    P("Fits whose HPM is not S0 (design, n, rep, seed, tag: |HPM|, TP, FP, FN, F(HPM) - F(S0), S0 in store, MPM = S0):")
    miss = [f for f in sci if not f["hpm_eq"] and f["design"] != "NULL"]
    for f in sorted(miss, key=lambda f: (f["design"], f["n"], f["rep"], f["seed"])):
        P("- %s n%d r%02d s%d %s: |HPM| %d, TP %d, FP %d, FN %d, dF %+.3f, S0 in store %s, MPM=S0 %s, outcome %s" % (NAMES[f["design"]], f["n"], f["rep"], f["seed"], f["tag"], f["hpm_size"], f["hpm_tp"], f["hpm_fp"], f["hpm_fn"],
                                                                                                          f["dF_hpm_S0"], f["S0_in_store"], f["mpm_eq"], f["outcome"]))
    res["hpm_not_S0"] = len(miss)

    # ---------- 2. C4
    P("")
    P("## S2. C4 PIP consistency (per cell; mean over datasets [95% t interval]; equal-weight PIP = primary, PIP_Z beside it)")
    P("| design | n | sup null PIP (eq) | min PIP over S0 (eq) | sup null (Z) | min over S0 (Z) | Brier (eq) | #null PIP > 0.1 (mean per fit; fits with >= 1) | #null PIP > 0.5 (fits with >= 1) | max abs(PIP_Z - PIP_eq) (max) |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    c4 = {}
    for d, n in order:
        fs = cells[(d, n)]
        t = lambda k: tci(list(by_dataset(fs, k).values()))
        g1 = [f["n_null_gt_0.1"] for f in fs]
        g5 = [f["n_null_gt_0.5"] for f in fs]
        c4["%s n%d" % (d, n)] = {"sup_eq": t("sup_null_eq"), "min_eq": t("min_true_eq"), "sup_Z": t("sup_null_Z"), "min_Z": t("min_true_Z"), "brier": t("brier_eq"),
                                   "gt01": [sum(g1) / len(g1), sum(1 for x in g1 if x >= 1)], "gt05": [sum(g5) / len(g5), sum(1 for x in g5 if x >= 1)], "maxZ": max(f["max_Z_minus_eq"] for f in fs)}
        r = c4["%s n%d" % (d, n)]
        P("| %s | %d | %s | %s | %s | %s | %s | %.2f; %d/%d | %d/%d | %s |" % (NAMES[d], n, ci_str(r["sup_eq"], 3), ci_str(r["min_eq"], 3) if d != "NULL" else "n/a (S0 empty)", ci_str(r["sup_Z"], 3),
                                                                             ci_str(r["min_Z"], 3) if d != "NULL" else "n/a", ci_str(r["brier"], 5, True), r["gt01"][0], r["gt01"][1], len(fs), r["gt05"][1], len(fs), fmt(r["maxZ"], 2, True)))
    res["C4"] = c4
    # distribution of min PIP over S0: fraction of fits with min_true > 0.5
    P("")
    P("Active-variable detection (fits with min PIP over S0 > 0.5 / > 0.9, equal-weight), per cell:")
    for d, n in order:
        if d == "NULL":
            continue
        fs = cells[(d, n)]
        P("- %s n%d: > 0.5 in %d/%d fits, > 0.9 in %d/%d; median min PIP %.3f; fits with min PIP < 0.1: %d" % (NAMES[d], n, sum(1 for f in fs if f["min_true_eq"] > 0.5), len(fs), sum(1 for f in fs if f["min_true_eq"] > 0.9), len(fs),
                                                                                                           float(np.median([f["min_true_eq"] for f in fs])), sum(1 for f in fs if f["min_true_eq"] < 0.1)))

    # ---------- 2b. reliability curve AR-weak
    P("")
    P("## S2b. PIP reliability curve, AR-weak arm (equal-weight PIP; a repeated-sampling diagnostic under a fixed truth, MANIFEST_CELLS section 4; NOT a calibration of any single posterior)")
    aw = [f for f in sci if f["design"] == "ARweak"]
    nb = 20
    # per dataset (cluster) per bin: (sum n_true, sum n, sum n*mean_pip) pooled over the fits of the dataset (dataset = (n, rep))
    cl = {}
    for f in aw:
        for bi, b in enumerate(f["reliability"]):
            e = cl.setdefault((f["n"], f["rep"]), [[0.0, 0.0, 0.0] for _ in range(nb)])
            e[bi][0] += b["n_true"]
            e[bi][1] += b["n"]
            e[bi][2] += b["n"] * (b["mean_pip"] if isinstance(b["mean_pip"], (int, float)) else 0.0)   # empty bins carry mean_pip "NaN" (a string)
    keys = sorted(cl)
    P("| bin | variables n (all AR-weak fits) | mean PIP (predicted frequency) | observed frequency of S0 | 95% dataset-cluster bootstrap | n_true (active) | datasets with >= 1 variable | observed by n (100 / 200 / 400 / 800) |")
    P("|---|---|---|---|---|---|---|---|")
    rel = []
    for bi in range(nb):
        tot_n = sum(cl[k][bi][1] for k in keys)
        if tot_n == 0:
            continue
        lo, hi = aw[0]["reliability"][bi]["lo"], aw[0]["reliability"][bi]["hi"]
        pred = sum(cl[k][bi][2] for k in keys) / tot_n
        cb = cluster_boot_ratio([(cl[k][bi][0], cl[k][bi][1]) for k in keys], rng)
        ntrue = int(sum(cl[k][bi][0] for k in keys))
        per_n = []
        for nn in (100, 200, 400, 800):
            kk = [k for k in keys if k[0] == nn]
            tn = sum(cl[k][bi][1] for k in kk)
            per_n.append("%s (%d/%d)" % (("%.3f" % (sum(cl[k][bi][0] for k in kk) / tn)) if tn else "-", int(sum(cl[k][bi][0] for k in kk)), int(tn)))
        rel.append({"bin": [lo, hi], "n": int(tot_n), "pred": pred, "obs": cb["obs"], "lo": cb["lo"], "hi": cb["hi"], "n_true": ntrue})
        P("| %.2f-%.2f | %d | %.4f | %.4f | [%s, %s] | %d | %d | %s |" % (lo, hi, tot_n, pred, cb["obs"], fmt(cb["lo"], 4), fmt(cb["hi"], 4), ntrue, sum(1 for k in keys if cl[k][bi][1] > 0), " / ".join(per_n)))
    res["reliability_ARweak"] = rel

    # ---------- 3. C5
    P("")
    P("## S3. C5 distribution (per cell; mean over datasets [95% t interval]; d_H^2 = Hellinger^2 to the true predictive)")
    P("| design | n | d_H^2 HPM plug-in | d_H^2 MPM plug-in | d_H^2 store-BMA predictive | oracle d_H^2 (known-S0 fit) | ratio to oracle (BMA / oracle) | n d_H^2 (BMA) | n d_H^2 / (s0 log p) (BMA) | post. median d_H | test MSE - oracle | mlpd - oracle |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    c5 = {}
    for d, n in order:
        fs = cells[(d, n)]
        s0 = fs[0]["s0"]
        slp = s0 * math.log(fs[0]["p"]) if s0 > 0 else None
        t = lambda k: tci(list(by_dataset(fs, k).values()))
        tf = lambda fn: tci(list(by_dataset(fs, None, fn).values()))
        r = {"h2_H": t("h2_H"), "h2_M": t("h2_M"), "h2_T": t("h2_T"), "h2_or": t("h2_oracle"), "ratio": tf(lambda f: f["h2_T"] / f["h2_oracle"] if f["h2_oracle"] else None), "nh2": tf(lambda f: f["n"] * f["h2_T"]),
             "nh2s": tf(lambda f: f["n"] * f["h2_T"] / slp) if slp else None, "q50": t("post_q50"), "dmse": tf(lambda f: f["mse_T"] - f["mse_or"]), "dmlpd": tf(lambda f: f["mlpd_T"] - f["mlpd_or"])}
        c5["%s n%d" % (d, n)] = r
        P("| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (NAMES[d], n, ci_str(r["h2_H"], 4), ci_str(r["h2_M"], 4), ci_str(r["h2_T"], 4), ci_str(r["h2_or"], 4), ci_str(r["ratio"], 3), ci_str(r["nh2"], 3),
                                                                           ci_str(r["nh2s"], 4) if r["nh2s"] else "n/a (s0 = 0)", ci_str(r["q50"], 4), ci_str(r["dmse"], 4), ci_str(r["dmlpd"], 4)))
    res["C5"] = c5
    P("")
    P("Fitted slope of log d_H^2 on log n (OLS on the log of the dataset-mean per n; 95 percent percentile interval of a dataset bootstrap within each n; B = %d, seed %d). The reference exponent of a rate d_H^2 proportional to 1/n is -1; no claim is made from it." % (B_BOOT, RNG_SEED))
    P("| design | n values (datasets) | slope, store-BMA predictive d_H^2 | slope, HPM plug-in d_H^2 | slope, oracle d_H^2 |")
    P("|---|---|---|---|---|")
    slopes = {}
    for d in DESIGNS:
        if d == "NULL":
            continue
        ns = [n for (dd, n) in order if dd == d]
        if len(ns) < 2:
            continue
        row = []
        for key in ("h2_T", "h2_H", "h2_oracle"):
            by_n = {n: list(by_dataset(cells[(d, n)], key).values()) for n in ns}
            s = boot_slope(by_n, rng)
            row.append(s)
        slopes[d] = row
        P("| %s | %s | %s | %s | %s |" % (NAMES[d], ", ".join("%d (%d)" % (n, len(by_dataset(cells[(d, n)], "h2_T"))) for n in ns),
                                          *["%.2f [%.2f, %.2f]" % (s["slope"], s["lo"], s["hi"]) if s else "NA (a zero d_H^2 in a cell)" for s in row]))
    res["slopes"] = {NAMES[d]: [({k: v for k, v in s.items() if k != "datasets"} if s else None) for s in row] for d, row in slopes.items()}

    # ---------- 4. C7
    P("")
    P("## S4. C7 evidence / merge (per cell)  [log Z-hat: dataset-mean over fits]")
    P("| design | n | log Z-hat (mean; range) | sigma-hat of Z_r (mean [CI]; max) | robust sigma-hat (mean) | max - median of log Z_r (mean; max) | R_eff / R' (min) | log Z-hat - log Z_T (mean; max) | omitted store mass (max) | island PIP sd, max (max) | sd of log Z-hat_occ(1000) over islands (max) |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    c7 = {}
    for d, n in order:
        fs = cells[(d, n)]
        t = lambda k: tci(list(by_dataset(fs, k).values()))
        sg = t("sigma_hat")
        lz = [f["logZ"] for f in fs]
        r = {"logZ": [sum(lz) / len(lz), min(lz), max(lz)], "sigma": sg, "sigma_max": max(f["sigma_hat"] for f in fs), "sig_rob": sum(f["sigma_rob"] for f in fs) / len(fs), "mm": [sum(f["max_minus_med"] for f in fs) / len(fs), max(f["max_minus_med"] for f in fs)],
             "reff": min(f["R_eff"] / f["Rp"] for f in fs), "dZT": [sum(f["logZ_minus_T"] for f in fs) / len(fs), max(f["logZ_minus_T"] for f in fs)], "omit": max(f["omitted_mass"] for f in fs),
             "isl_sd": max(f["isl_pip_max_sd"] for f in fs), "occ_sd": max(f["occ_sd1000"] for f in fs)}
        c7["%s n%d" % (d, n)] = r
        P("| %s | %d | %.1f (%.1f to %.1f) | %s; %s | %s | %.3f; %.3f | %.3f | %.4f; %.4f | %s | %s | %s |" % (NAMES[d], n, *r["logZ"], ci_str(sg, 4), fmt(r["sigma_max"], 4), fmt(r["sig_rob"], 4), *r["mm"], r["reff"], *r["dZT"], fmt(r["omit"], 2, True), fmt(r["isl_sd"], 5), fmt(r["occ_sd"], 4)))
    res["C7"] = c7
    P("")
    P("Flag frequencies over the science fits (all run at I_max = 0). At I_max = 0 the calibration rebuild loop never runs: E1 / E2 of the CALIBRATION are NOT EVALUATED (not 0 %), `grid_unconverged` = True, `checks_passed_calibration` = False and `I_used` = 0 are CONSTANTS (PREREG section 7, last bullet; CAMPAIGN_FREEZE_ADDENDUM section 2). Reported here as constants, outside any quality aggregate:")
    nsci = len(sci)
    cons = {"grid_unconverged True": sum(1 for f in sci if f["calib_flags"].get("grid_unconverged")), "checks_passed_calibration False": sum(1 for f in sci if f["calib_flags"].get("checks_passed_calibration") is False),
            "I_used = 0": sum(1 for f in sci if f["cfg"][3] == 0), "escalated": sum(1 for f in sci if f["calib_flags"].get("escalated")), "forced_pilot_steps > 0": sum(1 for f in sci if (f["calib_flags"].get("forced_pilot_steps") or 0) > 0)}
    P("- calibration constants / pilot-only flags, %d fits: %s" % (nsci, cons))
    trig = {}
    for f in sci:
        trig[tuple(f["calib_flags"].get("triggers_fired", []))] = trig.get(tuple(f["calib_flags"].get("triggers_fired", [])), 0) + 1
    P("- calibration triggers fired (list of triggers: fits): %s" % {",".join(k) or "none": v for k, v in trig.items()})
    fk = ["E1", "E2", "E3", "checks_passed_final", "final_local_limit", "local_limit", "low_empirical_ESS", "ls0_hpm_changed", "ls0_improved", "ls0_local_limit", "near_tie_truncated", "occ_inhomogeneous"]
    P("- FINAL-stage flags in `fit.meta.flags` (frequency over %d fits; computed on the final islands / merge; E1 and E2 here are the eval-record fields, which at I_max = 0 are not driven by a rebuild loop and must be read as 'not evaluated' when False): " % nsci +
      ", ".join("%s %d" % (k, sum(1 for f in sci if f["flags"].get(k) is True)) for k in fk))
    by_cell_flags = {}
    for d, n in order:
        fs = cells[(d, n)]
        by_cell_flags["%s n%d" % (d, n)] = {k: sum(1 for f in fs if f["flags"].get(k) is True) for k in ("occ_inhomogeneous", "low_empirical_ESS", "local_limit", "final_local_limit", "near_tie_truncated", "ls0_hpm_changed", "ls0_improved") if any(f["flags"].get(k) is True for f in fs)}
    P("- cells with any of occ_inhomogeneous / low_empirical_ESS / local_limit / final_local_limit / near_tie_truncated / ls0_hpm_changed / ls0_improved: %s" % ({k: v for k, v in by_cell_flags.items() if v} or "none"))
    P("- island spread analogue of E2 (sd of log Z_r over the R' = 16 final islands = sigma-hat of log; > 1 would be the analogue): max over fits of the sd of log Z_r = %.4f" % max(float(np.std(f["logZ_r"], ddof=1)) for f in sci))
    res["flags"] = {"calibration_constants": cons, "triggers": {",".join(k) or "none": v for k, v in trig.items()}, "final_flags": {k: sum(1 for f in sci if f["flags"].get(k) is True) for k in fk}, "by_cell": by_cell_flags,
                    "max_sd_logZ_r": max(float(np.std(f["logZ_r"], ddof=1)) for f in sci)}
    gu = tci([float(f["island_T"]) for f in sci])
    P("- island stage count T of the frozen preliminary grid (mean over fits): %.1f; by n: %s" % (gu["mean"], ", ".join("n%d %.1f" % (n, np.mean([f["island_T"] for f in sci if f["n"] == n])) for n in (100, 200, 400, 800))))

    # ---------- 5. A3
    P("")
    P("## S5. A3 partition: exact (`partition exact`, tag A3 / A3F) vs the default truncated partition, paired by dataset (engine seed 1)")
    default = {(f["design"], f["n"], f["rep"], f["seed"]): f for f in sci}
    rows = []
    for f in sorted(a3, key=lambda f: (f["design"], f["rep"])):
        dflt = default.get((f["design"], f["n"], f["rep"], 1))
        if dflt is None:
            rows.append({"a3": f, "dflt": None})
            continue
        pa, pd_ = pip_eq(co, f["dir"]), pip_eq(co, dflt["dir"])
        assert len(pa) == len(pd_)
        dd = [abs(x - y) for x, y in zip(pa, pd_)]
        mj = max(range(len(dd)), key=lambda j: dd[j])
        rows.append({"a3": f, "dflt": dflt, "max_dpip": max(dd), "argmax": mj, "dlogZ": f["logZ"] - dflt["logZ"]})
    P("| pair (dataset) | default tag | HPM equal | HPM = S0 (A3 / default) | F(HPM) A3 - default | max abs(PIP_A3 - PIP_default) | log Z-hat A3 - default | island s.e. of the difference | d_H^2 BMA A3 / default | core-h A3 / default |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    ok = [r for r in rows if r["dflt"] is not None]
    for r in ok:
        f, g = r["a3"], r["dflt"]
        sef = math.sqrt(sum(((np.std(x["logZ_r"], ddof=1) / math.sqrt(len(x["logZ_r"]))) ** 2) for x in (f, g)))
        r["sedif"] = sef
        P("| %s n%d r%02d | %s | %s | %s / %s | %+.2e | %.2e | %+.5f | %.5f | %.5f / %.5f | %.2f / %.2f |" % (NAMES[f["design"]], f["n"], f["rep"], g["tag"], set(f["hpm"]) == set(g["hpm"]), f["hpm_eq"], g["hpm_eq"], f["F_hpm"] - g["F_hpm"],
                                                                                                                r["max_dpip"], r["dlogZ"], sef, f["h2_T"], g["h2_T"], f["core_h"], g["core_h"]))
    A3 = {"pairs": len(ok), "hpm_equal": sum(1 for r in ok if set(r["a3"]["hpm"]) == set(r["dflt"]["hpm"])), "hpm_S0_a3": sum(1 for r in ok if r["a3"]["hpm_eq"]), "hpm_S0_dflt": sum(1 for r in ok if r["dflt"]["hpm_eq"]),
          "max_dpip_all": max(r["max_dpip"] for r in ok), "dlogZ": tci([r["dlogZ"] for r in ok]), "dlogZ_max_abs": max(abs(r["dlogZ"]) for r in ok),
          "dlogZ_in_se": [abs(r["dlogZ"]) / r["sedif"] for r in ok], "cost_a3": tci([r["a3"]["core_h"] for r in ok]), "cost_dflt": tci([r["dflt"]["core_h"] for r in ok]),
          "dh2": tci([r["a3"]["h2_T"] - r["dflt"]["h2_T"] for r in ok]), "dF_max_abs": max(abs(r["a3"]["F_hpm"] - r["dflt"]["F_hpm"]) for r in ok), "unpaired": len(rows) - len(ok)}
    for k in ("AR", "BLK"):
        sub = [r for r in ok if r["a3"]["design"] == k]
        A3[k] = {"pairs": len(sub), "hpm_equal": sum(1 for r in sub if set(r["a3"]["hpm"]) == set(r["dflt"]["hpm"])), "max_dpip": max(r["max_dpip"] for r in sub), "dlogZ_max_abs": max(abs(r["dlogZ"]) for r in sub),
                 "dlogZ_mean": sum(r["dlogZ"] for r in sub) / len(sub)}
    P("")
    P("Summary: %d pairs, HPM identical in %d, HPM = S0 in %d (A3) / %d (default); max over pairs and variables of abs(dPIP) = %.2e; dlogZ (A3 - default) mean %s, largest abs %.5f, largest abs in island s.e. of the difference %.2f; cost A3 %s vs default %s core-h; pi_0(S0) NOT AVAILABLE (B4, HQ Q6); d_H between the two partitions' predictives NOT COMPUTABLE (the default-partition fits have no law.bin: law.bin was kept for the precision and A3 fits only)." % (
        A3["pairs"], A3["hpm_equal"], A3["hpm_S0_a3"], A3["hpm_S0_dflt"], A3["max_dpip_all"], ci_str(A3["dlogZ"], 5), A3["dlogZ_max_abs"], max(A3["dlogZ_in_se"]), ci_str(A3["cost_a3"], 2), ci_str(A3["cost_dflt"], 2)))
    res["A3"] = A3

    # ---------- 6. second seed
    P("")
    P("## S6. Second seed: AR-strong n = 200, engine seeds 1 and 2 on 10 datasets (the yardstick for any other V comparison)")
    ss = []
    for rep in range(1, 11):
        a_ = default.get(("AR", 200, rep, 1))
        b_ = default.get(("AR", 200, rep, 2))
        if a_ and b_:
            p1, p2 = pip_eq(co, a_["dir"]), pip_eq(co, b_["dir"])
            dd = [abs(x - y) for x, y in zip(p1, p2)]
            ss.append({"rep": rep, "hpm_equal": set(a_["hpm"]) == set(b_["hpm"]), "hpm1": a_["hpm_eq"], "hpm2": b_["hpm_eq"], "max_dpip": max(dd), "dlogZ": a_["logZ"] - b_["logZ"], "h2_1": a_["h2_T"], "h2_2": b_["h2_T"],
                       "sig1": a_["sigma_hat"], "sig2": b_["sigma_hat"], "dF": a_["F_hpm"] - b_["F_hpm"]})
    P("| dataset | HPM equal | HPM = S0 (s1 / s2) | max abs(PIP_s1 - PIP_s2) | log Z-hat s1 - s2 | d_H^2 BMA s1 / s2 |")
    P("|---|---|---|---|---|---|")
    for r in ss:
        P("| AR n200 r%02d | %s | %s / %s | %.2e | %+.5f | %.5f / %.5f |" % (r["rep"], r["hpm_equal"], r["hpm1"], r["hpm2"], r["max_dpip"], r["dlogZ"], r["h2_1"], r["h2_2"]))
    sdz = math.sqrt(sum(r["dlogZ"] ** 2 for r in ss) / (2 * len(ss)))
    P("")
    P("Summary: HPM equal in %d/%d datasets; max abs(dPIP) %.2e (median %.2e); seed-to-seed sd of log Z-hat (pooled, sqrt(mean d^2 / 2)) = %.5f; largest abs(dlogZ) %.5f; seed-to-seed d_H^2 difference: mean abs %.2e." % (
        sum(1 for r in ss if r["hpm_equal"]), len(ss), max(r["max_dpip"] for r in ss), float(np.median([r["max_dpip"] for r in ss])), sdz, max(abs(r["dlogZ"]) for r in ss), float(np.mean([abs(r["h2_1"] - r["h2_2"]) for r in ss]))))
    res["second_seed"] = {"n": len(ss), "hpm_equal": sum(1 for r in ss if r["hpm_equal"]), "max_dpip": max(r["max_dpip"] for r in ss), "median_max_dpip": float(np.median([r["max_dpip"] for r in ss])),
                          "sd_logZ": sdz, "max_abs_dlogZ": max(abs(r["dlogZ"]) for r in ss), "rows": ss}

    # ---------- 7. NULL
    P("")
    P("## S7. NULL control (n = 200, S0 empty; 5 datasets, one fit each)")
    nl = [f for f in sci if f["design"] == "NULL"]
    P("| run | n_null PIP > 0.5 | n_null PIP > 0.1 | sup PIP (eq) | HPM size | outcome | log Z-hat | sigma-hat |")
    P("|---|---|---|---|---|---|---|---|")
    for f in sorted(nl, key=lambda f: f["rep"]):
        P("| %s | %s | %s | %.4f | %d | %s | %.3f | %.4f |" % (f["run_id"], f["n_null_gt_0.5"], f["n_null_gt_0.1"], f["sup_null_eq"], f["hpm_size"], f["outcome"], f["logZ"], f["sigma_hat"]))
    res["NULL"] = {"fits": len(nl), "n_null_gt_0.5_zero": sum(1 for f in nl if f["n_null_gt_0.5"] == 0), "max_sup": max(f["sup_null_eq"] for f in nl), "hpm_empty": sum(1 for f in nl if f["hpm_size"] == 0)}
    P("")
    P("n_null_gt_0.5 = 0 in %d of %d NULL fits; HPM empty in %d of %d; largest sup PIP %.4f." % (res["NULL"]["n_null_gt_0.5_zero"], len(nl), res["NULL"]["hpm_empty"], len(nl), res["NULL"]["max_sup"]))
    nz = [f for f in sci if f["design"] != "NULL" and (f["n_null_gt_0.5"] or 0) > 0]
    P("Non-NULL fits with a null-variable PIP > 0.5 (n_null_gt_0.5 > 0): %d (%s)" % (len(nz), "; ".join("%s: %s" % (f["run_id"], f["n_null_gt_0.5"]) for f in nz[:20])))
    res["nonnull_null_gt_half"] = len(nz)

    # ---------- 8. n-trend table
    P("")
    P("## S8. n-trend summary (the same numbers as S1-S3, one line per design)")
    P("| design | n | P(HPM = S0) | min PIP over S0 (mean) | sup null PIP (mean) | d_H^2 BMA (mean) | n d_H^2 / (s0 log p) | sigma-hat (mean) |")
    P("|---|---|---|---|---|---|---|---|")
    for d, n in order:
        k = "%s n%d" % (d, n)
        P("| %s | %d | %.2f | %s | %s | %s | %s | %s |" % (NAMES[d], n, c2[k]["P_hpm"]["p"], fmt(c4[k]["min_eq"]["mean"], 3) if d != "NULL" else "n/a", fmt(c4[k]["sup_eq"]["mean"], 3), fmt(c5[k]["h2_T"]["mean"], 4),
                                                         fmt(c5[k]["nh2s"]["mean"], 3) if c5[k]["nh2s"] else "n/a", fmt(c7[k]["sigma"]["mean"], 4)))

    open(os.path.join(a.out, "science_tables.md"), "w").write("\n".join(L) + "\n")
    json.dump(res, open(os.path.join(a.out, "science_summary.json"), "w"), indent=1, default=str)
    with open(os.path.join(a.out, "science_per_fit.csv"), "w", newline="") as fh:
        cols = ["run_id", "wave", "design", "n", "rep", "tag", "seed", "outcome", "hpm_eq", "mpm_eq", "hpm_size", "hpm_ham", "hpm_tp", "hpm_fp", "hpm_fn", "mpm_tp", "mpm_fp", "sup_null_eq", "min_true_eq", "sup_null_Z", "min_true_Z", "brier_eq",
                "n_null_gt_0.1", "n_null_gt_0.5", "h2_H", "h2_M", "h2_T", "h2_oracle", "post_q50", "mse_T", "mse_or", "mlpd_T", "mlpd_or", "logZ", "logZ_T", "sigma_hat", "sigma_rob", "R_eff", "island_T", "core_h", "phase", "occ_inhom"]
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for f in fits:
            w.writerow(f)
    print("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
