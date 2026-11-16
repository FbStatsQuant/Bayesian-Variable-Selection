"""Aggregate items 2 and 3 -> out/analysis_item2.md, out/analysis_item3.md.   DRAFT (by this seat, unchecked)"""
import sys, math, pickle
sys.dont_write_bytecode = True
import numpy as np
def run(mode):
    D = pickle.load(open(f"out/item{mode}.pkl", "rb")); out = D["out"]; tg = D["tgrid"]; ms = D["ms"]; nd = D["ndraw"]; R = D["R"]
    L = []
    pr = lambda *a: L.append(" ".join(str(x) for x in a))
    ttl = "Item 2 — dangerous collinearity scale (6 null columns = x₁ + τ·noise)" if mode == 2 else "Item 3 — (A5) violated (two true columns, correlation 1 − 1/n, coefficients +B, −B)"
    pr(f"## {ttl}\n\nR = {R} data sets per cell, {nd} posterior draws per data set, p = 12 with exact enumeration of all 4096 models, d² exact given the draw. Gaussian design. "
       "n·d² statistics are means over data sets of per-data-set posterior quantiles (as in N4 of `work/numerics/RESULTS.md`), with the spread over data sets in brackets (min–max of the per-data-set 0.99-quantile).\n")
    pr("| n | " + ("τ²" if mode == 2 else "B") + " | n·d² med | q90 | q99 | q99: min–max over sets | n·d²/log n q99 | E[n·d²] | meanlogΠ M=1 | M=2 | M=4 | M=8 | ĉ (−slope/log n) | P(n·d²>6) | P(n·d²>12) | max over sets of P(n·d²>12) |")
    pr("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    keys = list(out.keys()); keys.sort(key=lambda k: (int(k.split("|")[0]), out[k]["par"]))
    sizes = []
    for k in keys:
        c = out[k]; n = int(k.split("|")[0]); ln = math.log(n)
        qs = c["qs"]; N = int(c["N"][0])
        floor = math.log(0.5 / N)
        lm = [np.mean(np.log(np.maximum(c["tailM"][:, i], 0.5 / N))) for i in range(len(ms))]
        pooled = c["tail"].mean(0)
        # c_t from pooled tail on integer-ish t with >=5 exceeding draws (pooled counts)
        sel = [(tg[j], pooled[j]) for j in range(len(tg)) if pooled[j] * N * R >= 5 and 2 <= tg[j] <= 32]
        if len(sel) >= 3:
            tt = np.array([a for a, b in sel]); lp = np.log([b for a, b in sel]); ct = -np.polyfit(tt, lp, 1)[0]
        else: ct = float("nan")
        j6 = list(tg).index(6.0); j12 = list(tg).index(12.0)
        par = f"{c['par']:.3g}" if mode == 2 else f"{c['par']:.3g}"
        lab = k.split("|")[1]
        pr(f"| {n} | {lab} ({par}) | {qs[:,0].mean():.2f} | {qs[:,1].mean():.2f} | {qs[:,2].mean():.2f} | {qs[:,2].min():.2f}–{qs[:,2].max():.2f} | {qs[:,2].mean()/ln:.3f} | {c['mean'].mean():.2f} | {lm[0]:.2f} | {lm[1]:.2f} | {lm[2]:.2f} | {lm[3]:.2f} | {ct/ln:.2f} | {pooled[j6]:.2e} | {pooled[j12]:.2e} | {c['tail'][:,j12].max():.2e} |")
    pr(f"\n(floor of log Π at {math.log(0.5/(nd)):.2f} when no draw exceeds; ĉ from pooled P(n·d²>t) on grid points with ≥ 5 exceeding draws pooled over data sets and 2 ≤ t ≤ 32 (≥ 3 points), NaN otherwise.)\n")
    pr("### Pooled P(n·d² > t) (mean over data sets)\n")
    cols = [4, 6, 8, 12, 16, 24, 32, 64, 128, 256, 512]
    pr("| n | " + ("τ²" if mode == 2 else "B") + " | " + " | ".join(f"t={t}" for t in cols) + " |"); pr("|---|---|" + "---|" * len(cols))
    for k in keys:
        c = out[k]; n = int(k.split("|")[0]); pooled = c["tail"].mean(0)
        pr(f"| {n} | {k.split('|')[1]} | " + " | ".join(f"{pooled[list(tg).index(float(t))]:.2e}" for t in cols) + " |")
    pr("\n### Law of |S| and selection (exact posterior over all 4096 models, mean over data sets)\n")
    if mode == 2:
        pr("`group` = {x₁, x₇,…,x₁₂} (x₁ and its 6 near-duplicates). s₀ = 3 true columns x₁,x₂,x₃.\n")
        pr("| n | τ² | E|S| | P(|S|≤2) | P(|S|=3) | P(|S|=4) | P(|S|=5) | P(|S|≥6) | P(|S|≥8) | incl x₁ | incl x₂ | incl x₃ | E #group cols in S | P(≥1 group col) approx via E |")
    else:
        pr("true columns x₁,x₂ (index 0,1), s₀ = 2.\n")
        pr("| n | B | E|S| | P(|S|≤1) | P(|S|=2) | P(|S|=3) | P(|S|=4) | P(|S|≥5) | P(|S|≥8) | incl x₁ | incl x₂ | max incl of a null column | E #group cols in S |")
    pr("|---|---|---|---|---|---|---|---|---|---|---|---|---|" + ("---|" if mode == 2 else "---|"))
    for k in keys:
        c = out[k]; n = int(k.split("|")[0]); sl = c["szlaw"].mean(0); es = (c["szlaw"] * np.arange(13)).sum(1).mean()
        inc = c["incl"].mean(0)
        if mode == 2:
            pr(f"| {n} | {k.split('|')[1]} | {es:.2f} | {sl[:3].sum():.3f} | {sl[3]:.3f} | {sl[4]:.3f} | {sl[5]:.3f} | {sl[6:].sum():.3f} | {sl[8:].sum():.4f} | {inc[0]:.3f} | {inc[1]:.3f} | {inc[2]:.3f} | {c['ngrp'].mean():.2f} | – |")
        else:
            pr(f"| {n} | {k.split('|')[1]} | {es:.2f} | {sl[:2].sum():.3f} | {sl[2]:.3f} | {sl[3]:.3f} | {sl[4]:.3f} | {sl[5:].sum():.3f} | {sl[8:].sum():.4f} | {inc[0]:.3f} | {inc[1]:.3f} | {inc[2:].max():.3f} | {c['ngrp'].mean():.2f} |")
    if mode == 3:
        pr("\n### Sample interface quantities (σ* = 1) and what they say about (E), (C)\n")
        pr("| n | B | ‖μ‖²/n median (min–max) | ‖θ*‖²/n median (min–max) | n·d² q50 / q99 (mean over sets) | n·d² q99 / n | n·d² q99 / log n |"); pr("|---|---|---|---|---|---|---|")
        for k in keys:
            c = out[k]; n = int(k.split("|")[0]); q = c["qs"]
            pr(f"| {n} | {k.split('|')[1]} | {np.median(c['mu2n']):.3g} ({c['mu2n'].min():.3g}–{c['mu2n'].max():.3g}) | {np.median(c['th2n']):.3g} ({c['th2n'].min():.3g}–{c['th2n'].max():.3g}) | {q[:,0].mean():.2f} / {q[:,2].mean():.2f} | {q[:,2].mean()/n:.3f} | {q[:,2].mean()/math.log(n):.2f} |")
    open(f"out/analysis_item{mode}.md", "w").write("\n".join(L)); print("\n".join(L))
for m in (2, 3): run(m)
