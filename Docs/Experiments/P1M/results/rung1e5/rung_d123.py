#!/usr/bin/env python3
"""rung_d123.py -- the option-D gate evaluation at the 10^5 rung read-back (GB_PLAN section 6, adopted VERBATIM by HQ H-40 (c)); the D1 / D2 inputs and the clustered interval. READ-ONLY,
stdlib, deterministic (the bootstrap uses a fixed seed). Registered BEFORE the first rung submission (L-8 carry rule).

  python3 -I rung_d123.py --records ROOT [ROOT ...] --out OUTDIR [--boot 10000] [--seed 20261120]

WHICH FITS ENTER: the AR-strong fits `5-AR-n200-r0{1..5}-V-s1` (n 200, five datasets; r01 = the G-B pilot, read from records/gb) and `5-AR-n400-r0{1..3}-V-s1` (n 400, three datasets), whose RECORDED arm
(calib_meta.json) is N 10000, m 1, I_max 0. ADJ-OPP, IND, the I_max 3 twins and the continuity twins (VN25) do NOT enter D1 / D2. The dataset is the independent unit (every fit has its own dataset).
D1 (the theorem premise holds at 10^5): P-hat(HPM = S0) over the fits, `selection.hpm_eq_S0`: n 200: >= 4 of 5, n 400: 3 of 3. PASS iff both.
D2 (the expected trend): pi-hat(S0) = exp(selection.F_S0 - evidence.logZ) (the estimated posterior probability of S0; the terminal occupancy fit.meta.occ[M=1].occ is reported beside it); D2 PASS iff
   mean(n 400) >= mean(n 200) (a difference of -1e-12 or more counts as equality: floating-point roundoff only, not a tolerance on the science). IT IS A COMPARISON OF MEANS WITH NO TOLERANCE (5 against 3 datasets), judged only here, at the rung read-back. REPORTED, NOT GATING: the difference with (a) the Welch 95 %
   t-interval for two independent means (df = Welch-Satterthwaite) and (b) a percentile cluster bootstrap (datasets resampled within each n level, B draws), plus every per-dataset value.
D3 (budget): position + D <= 28.3k at the re-sized unit cost: NOT computed here (the read-back's budget script, from the measured per-fit costs).
BESIDE (no threshold, a flag to HQ if the N effect looks large): the continuity twins (`...-VN25-s1`, N 2,500): pi-hat(S0) at N 2,500 against N 10^4 on the same data and seeds (AR r01 and ADJ-OPP r01).
"""
import argparse, json, math, os, random, re, sys

AR = re.compile(r"^5-AR-n(?P<n>200|400)-r(?P<r>\d+)-V-s1$")
VN = re.compile(r"^5-(?P<d>AR|ADJOPP)-n200-r01-VN25-s1$")
EVAL = ("eval.bin.json", "eval.json")
SKIP = ("_batch_", "manifests", "scripts", "refused_", "rescue_", "cost", "log")


def jl(p):
    return json.load(open(p))


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1e-300 if abs(d) < 1e-300 else d; d = 1.0 / d; h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1e-300 if abs(d) < 1e-300 else d; c = 1.0 + aa / c; c = 1e-300 if abs(c) < 1e-300 else c; d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1e-300 if abs(d) < 1e-300 else d; c = 1.0 + aa / c; c = 1e-300 if abs(c) < 1e-300 else c; d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < 3e-16:
            break
    return h


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1.0) / (a + b + 2.0) else 1.0 - bt * betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t); p = 0.5 * betai(df / 2.0, 0.5, x)
    return 1.0 - p if t > 0 else p


def t_quantile(p, df):
    lo, hi = 0.0, 1.0
    while t_cdf(hi, df) < p:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if t_cdf(mid, df) < p else (lo, mid)
    return 0.5 * (lo + hi)


def find(roots):
    out = {}
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if not d.startswith(SKIP)]
            ef = next((os.path.join(dp, n) for n in EVAL if n in fns), None)
            if ef is None:
                continue
            try:
                ev = jl(ef)
            except Exception:
                continue
            rid = jl(os.path.join(dp, "run_manifest.json")).get("run_id") if "run_manifest.json" in fns else os.path.basename(dp)
            if "evidence" in ev and rid and (AR.match(rid) or VN.match(rid) or re.match(r"^5-(AR|ADJOPP)-n200-r01-V-s1$", rid)):
                out[rid] = (dp, ev)
            dns[:] = []
    return out


def arm(dp):
    try:
        p = os.path.join(dp, "calib_meta.json")
        m = jl(p); m = m.get("meta", m)
        return int(m["N"]), int(m["refine_m"]), int(m["I_max"])
    except Exception:
        return None


def quantities(ev):
    fs0, lz = (ev.get("selection") or {}).get("F_S0"), (ev.get("evidence") or {}).get("logZ")
    o1 = next((e for e in ((ev.get("fit") or {}).get("meta") or {}).get("occ", []) if e.get("M") == 1), {})
    return {"hpm_eq_S0": (ev.get("selection") or {}).get("hpm_eq_S0"), "pi_hat_S0": (math.exp(fs0 - lz) if fs0 is not None and lz is not None else None), "occ_top1": o1.get("occ"),
            "ok": ev.get("status") == "completed" and ev.get("fit_status", "completed") == "completed"}


def mean(x):
    return sum(x) / len(x)


def var(x):
    m = mean(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--out", required=True); ap.add_argument("--boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=20261120)
    a = ap.parse_args(argv)
    runs = find(a.records)
    lev = {200: {}, 400: {}}; bad = {}
    for rid, (dp, ev) in sorted(runs.items()):
        g = AR.match(rid)
        if not g:
            continue
        ar = arm(dp)
        if ar != (10000, 1, 0):
            bad[rid] = "recorded arm %s != (10000, 1, 0)" % (ar,); continue
        q = quantities(ev)
        if not q["ok"] or q["pi_hat_S0"] is None or q["hpm_eq_S0"] is None:
            bad[rid] = "not delivered or field missing"; continue
        lev[int(g["n"])][rid] = q
    need = {200: 5, 400: 3}
    rep = {"script": "rung_d123.py", "fits": {str(n): lev[n] for n in lev}, "excluded": bad, "D1": None, "D2": None}
    if any(len(lev[n]) < need[n] for n in need):
        rep["verdict"] = "NOT_EVALUABLE: delivered AR fits n200 %d of 5, n400 %d of 3" % (len(lev[200]), len(lev[400]))
    else:
        k200 = sum(1 for q in lev[200].values() if q["hpm_eq_S0"]); k400 = sum(1 for q in lev[400].values() if q["hpm_eq_S0"])
        d1 = k200 >= 4 and k400 == 3
        rep["D1"] = {"n200_hpm_eq_S0": "%d/5" % k200, "n400_hpm_eq_S0": "%d/3" % k400, "rule": ">= 4/5 at n 200 and 3/3 at n 400", "PASS": d1}
        x2 = [q["pi_hat_S0"] for q in lev[200].values()]; x4 = [q["pi_hat_S0"] for q in lev[400].values()]
        diff = mean(x4) - mean(x2)
        se2 = var(x2) / len(x2) + var(x4) / len(x4)
        se = math.sqrt(se2)
        df = se2 ** 2 / ((var(x2) / len(x2)) ** 2 / (len(x2) - 1) + (var(x4) / len(x4)) ** 2 / (len(x4) - 1)) if se2 > 0 else float("nan")
        tq = t_quantile(0.975, df) if se2 > 0 else float("nan")
        rng = random.Random(a.seed); bs = []
        for _ in range(a.boot):
            b2 = [x2[rng.randrange(len(x2))] for _ in x2]; b4 = [x4[rng.randrange(len(x4))] for _ in x4]
            bs.append(mean(b4) - mean(b2))
        bs.sort()
        o2 = [q["occ_top1"] for q in lev[200].values() if q["occ_top1"] is not None]; o4 = [q["occ_top1"] for q in lev[400].values() if q["occ_top1"] is not None]
        rep["D2"] = {"mean_pi_hat_n200": mean(x2), "mean_pi_hat_n400": mean(x4), "difference_n400_minus_n200": diff, "rule": "difference >= 0 (a comparison of means, NO tolerance; reported interval does not gate)",
                     "PASS": diff >= -1e-12, "welch_df": df, "welch_95_ci": [diff - tq * se, diff + tq * se], "cluster_bootstrap_95_ci": [bs[int(0.025 * len(bs))], bs[int(0.975 * len(bs)) - 1]], "bootstrap_draws": a.boot,
                     "bootstrap_seed": a.seed, "occupancy_beside": {"mean_n200": mean(o2) if o2 else None, "mean_n400": mean(o4) if o4 else None},
                     "expert_band_note": "OWNER_SHEET 0.3-0.45 at n 200 is a p = 10^6 draw, not a 10^5 band"}
        rep["D3"] = "NOT computed here: position + D <= 28.3k at the re-sized unit cost, from the read-back's budget script"
        rep["verdict"] = "D1 %s, D2 %s (D3 pending the budget script)" % ("PASS" if d1 else "FAIL", "PASS" if diff >= -1e-12 else "FAIL")
    cont = []
    for rid, (dp, ev) in sorted(runs.items()):
        g = VN.match(rid)
        if not g:
            continue
        base = runs.get(rid.replace("-VN25-", "-V-"))
        qa, qb = (quantities(base[1]) if base else None), quantities(ev)
        cont.append({"twin": rid, "pi_hat_S0_N2500": qb["pi_hat_S0"], "pi_hat_S0_N10000": (qa or {}).get("pi_hat_S0"), "difference_N10000_minus_N2500": ((qa["pi_hat_S0"] - qb["pi_hat_S0"]) if qa and None not in (qa["pi_hat_S0"], qb["pi_hat_S0"]) else None),
                     "note": "no threshold; a flag to HQ if the N effect looks large (D runs at N 2,500, the trend is measured at N 10^4)"})
    rep["continuity_pi_hat_S0"] = cont
    os.makedirs(a.out, exist_ok=True)
    json.dump(rep, open(os.path.join(a.out, "rung_d123.json"), "w"), indent=1, default=str)
    print(json.dumps({"verdict": rep["verdict"], "D1": rep["D1"], "D2": rep["D2"], "continuity": cont}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
