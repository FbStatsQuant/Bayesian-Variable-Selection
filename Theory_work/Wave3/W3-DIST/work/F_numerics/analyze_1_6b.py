"""Aggregate items 1 and 6b from out/item1_n*.npz -> out/analysis_item1_6b.md.   DRAFT (by this seat, unchecked)"""
import sys, math
sys.dont_write_bytecode = True
import numpy as np
from math import lgamma, log, exp, sqrt
from scipy.special import gammaln
P = 12
def logw(k, q): return math.log(0.5) - (gammaln(2*q) - gammaln(k+1) - gammaln(2*q-k))
def logq(k, q): return gammaln(q+1) - gammaln(k+1) - gammaln(q-k+1) + logw(k, q)
out = []
def pr(*a): out.append(" ".join(str(x) for x in a))
TS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16]
for n in (100, 400):
    Z = np.load(f"out/item1_n{n}.npz"); tg = Z["tgrid"]; tail = Z["tail"]; R = tail.shape[0]; nd = int(Z["ndraw"])
    ln = math.log(n)
    pr(f"\n### Item 1, n = {n}: distribution over R = {R} data sets of Π(n·d² > t | D)   ({nd} posterior draws per data set; d² exact given the draw)")
    pr(f"Resolution per data set: 1/{nd} = {1/nd:.0e}.  log n = {ln:.2f}; 2 log n = {2*ln:.2f}; 3 log n = {3*ln:.2f}.  `frac>0` = share of data sets with at least one exceeding draw.\n")
    pr("| t | q0.5 | q0.9 | q0.99 | max | mean (=pooled) | frac>0 | #sets with Π>0.01 | #sets with Π>0.05 |"); pr("|---|---|---|---|---|---|---|---|---|")
    ts = TS + [math.floor(m*ln/0.25)*0.25 for m in (1, 2, 3)]
    for t in sorted(set(ts)):
        j = int(round((t - 0.25) / 0.25)); v = tail[:, j]
        lab = f"{t:g}" + ("  (≈ log n)" if abs(t-math.floor(ln/.25)*.25) < 1e-9 else "  (≈ 2 log n)" if abs(t-math.floor(2*ln/.25)*.25) < 1e-9 else "  (≈ 3 log n)" if abs(t-math.floor(3*ln/.25)*.25) < 1e-9 else "")
        pr(f"| {lab} | {np.quantile(v,.5):.2e} | {np.quantile(v,.9):.2e} | {np.quantile(v,.99):.2e} | {v.max():.2e} | {v.mean():.2e} | {np.mean(v>0):.3f} | {(v>0.01).sum()} | {(v>0.05).sum()} |")
    qs = Z["qs"]
    pr(f"\nPer-data-set posterior quantiles of n·d² (rows: posterior level; columns: distribution over data sets):\n")
    pr("| posterior level | q0.5 | q0.9 | q0.99 | max over data sets |"); pr("|---|---|---|---|---|")
    for i, lv in enumerate((0.5, 0.9, 0.99, 0.999)):
        v = qs[:, i]; pr(f"| {lv} | {np.quantile(v,.5):.2f} | {np.quantile(v,.9):.2f} | {np.quantile(v,.99):.2f} | {v.max():.2f} |")
    pr(f"\nSample interface quantities: ‖μ‖²/n median {np.median(Z['mu2n']):.3f} (max {Z['mu2n'].max():.3f}); ‖θ*‖²/n median {np.median(Z['th2n']):.4f} (max {Z['th2n'].max():.4f}); π(S₀) median {np.median(Z['pi0']):.3f}, min {Z['pi0'].min():.3f}.")
    # failure frequencies for DIST-1 form  P*[Π(n d² > C² t) > exp(-c t)]
    pr(f"\n**DIST-1 form, empirical failure frequency** F(C²,c,t) = share of the {R} data sets with Π(n·d² > C²t | D) > e^{{-ct}}  vs the bound 3e^{{-ct}}  (tail read at the largest grid point ≤ C²t, i.e. conservative; `<res` means e^{{-ct}} is below the 1/{nd} resolution, so a single exceeding draw counts):\n")
    pr("| (C², c) | t = log n | t = 2 log n | t = 3 log n |"); pr("|---|---|---|---|")
    for (C2, c) in [(1, .5), (1, 1), (2, .5), (2, 1), (3, 1), (4, 1)]:
        cells = []
        for m in (1, 2, 3):
            t = m*ln; x = C2*t; j = int(math.floor(x/0.25)) - 1
            if j >= len(tg): cells.append("n/a (beyond grid)"); continue
            thr = exp(-c*t); fr = np.mean(tail[:, j] > thr)
            cells.append(f"{fr:.3f} vs 3e^-ct={min(3*thr,1):.3f}" + (" <res" if thr < 1/nd else ""))
        pr(f"| ({C2}, {c}) | " + " | ".join(cells) + " |")
    # ---------------- item 6b: Lemma S cutoff ------------------
    sz = Z["szlaw"]; logD0 = Z["logD0"]
    tailS = 1 - np.cumsum(sz, axis=1)       # P(|S| > m)  m=0..12
    tailS = np.clip(tailS, 0, 1)
    pr(f"\n### Item 6b, n = {n}: π(|S| > m) on the same {R} exact enumerations (p = 12, K = 12, S₀ = {{1,2,3}}) vs the cutoff inequality of Lemma S")
    K = min(P, n//2); s0 = 3; kap0 = 0.5
    def mn(t): return min(K, s0 + math.ceil((s0*math.log(2*P) + (s0+2)/2*math.log(n+1) + 3*t)/math.log(2)))
    pr(f"Cutoff m_n(t) of STATEMENT §0 at t = log n: {mn(ln)}; at t = 2 log n: {mn(2*ln)}; K = {K}.  **m_n(t) = K for every t ≥ log n here, so the statement at m = m_n(t) is vacuous (π(|S| > K) = 0)**; the table below tests the *inequality* for every m < K instead, with the exact R^T_m, exact log D_S₀ and t* = the largest t ∈ [1, n^{{1−κ₀}}] (κ₀ = ½) with  log R_m + ½ log D_S₀ + ½ log n + C·[1+√t+t/√n] ≤ −2t  (C is an unspecified constant of the lemma; C ∈ {{0, 1, 3}}).\n")
    lw3 = logw(3, P)
    Rm = np.array([np.exp(np.logaddexp.reduce([logq(k, P) for k in range(m+1, P+1)]) - lw3) if m < P else 0.0 for m in range(P+1)])
    pr(f"R^T_m (exact, |T| = 3): " + ", ".join(f"m={m}:{Rm[m]:.3g}" for m in range(0, 13)))
    bound = np.array([2*(2*P)**3 * 2.0**(-m) for m in range(P+1)])
    pr(f"Check R_m ≤ 2(2p)^{{s₀}}2^{{−m}}: max ratio R_m / bound over m ≤ 11 = {np.max(Rm[:12]/bound[:12]):.3g} (≤ 1 ⇒ holds).  Check D_S₀ ≤ (n+1)^{{s₀}}: max over data sets of log D_S₀ − 3 log(n+1) = {np.max(logD0 - 3*math.log(n+1)):.3f} (≤ 0 ⇒ holds); log D_S₀ range [{logD0.min():.2f}, {logD0.max():.2f}].\n")
    for C in (0,):
        pr(f"\n**C = {C}**\n"); pr("| m | log R_m + ½log D_S₀ + ½log n (median over sets) | t*(m) median | π(|S|>m) median | π(|S|>m) max | e^{-t*} median | #sets with π(|S|>m) > e^{-t*} | smallest e^{-t*} over sets for which t* ≥ 1 |"); pr("|---|---|---|---|---|---|---|---|")
        for m in range(0, 12):
            L0 = math.log(Rm[m]) + 0.5*logD0 + 0.5*math.log(n)
            tstar = np.zeros(R) - 1.0
            for r in range(R):
                f = lambda t: L0[r] + C*(1+sqrt(t)+t/sqrt(n)) + 2*t
                lo, hi = 1.0, sqrt(n)
                if f(lo) > 0: tstar[r] = -1.0; continue
                if f(hi) <= 0: tstar[r] = hi; continue
                for _ in range(60):
                    mid = 0.5*(lo+hi)
                    if f(mid) <= 0: lo = mid
                    else: hi = mid
                tstar[r] = lo
            ok = tstar >= 1
            if ok.sum() == 0:
                pr(f"| {m} | {np.median(L0):.2f} | inequality fails at t = 1 for all sets | {np.median(tailS[:,m]):.3g} | {tailS[:,m].max():.3g} | – | – | – |"); continue
            viol = ((tailS[:, m] > np.exp(-tstar)) & ok).sum()
            pr(f"| {m} | {np.median(L0):.2f} | {np.median(tstar[ok]):.2f} ({ok.sum()}/{R} sets admissible) | {np.median(tailS[:,m]):.3g} | {tailS[:,m].max():.3g} | {np.exp(-np.median(tstar[ok])):.2e} | {viol}/{ok.sum()} | {np.exp(-tstar[ok]).min():.2e} |")
    pr("\n(C = 1 and C = 3 give the same verdict: the inequality fails at t = 1 for every m ≤ 11 because its left side is positive; only m = 12 = K, where R_12 = 0, satisfies it.)")
    pr(f"\n**Unclamped cutoff m_n(t) of STATEMENT §0 versus the empirical size tail** (exact π(|S| > m)): m_emp(t) := min{{m : π(|S| > m) ≤ e^{{-t}}}} per data set; distribution over the {R} data sets.\n")
    pr("| t | unclamped m_n(t) (before min with K) | m_emp(t) q0.5 | q0.9 | q0.99 | max |"); pr("|---|---|---|---|---|---|")
    for t in (1, ln, 2*ln, 3*ln, 5*ln):
        mu_ = s0 + math.ceil((s0*math.log(2*P) + (s0+2)/2*math.log(n+1) + 3*t)/math.log(2))
        me = np.array([next((m for m in range(P+1) if tailS[r, m] <= math.exp(-t)), P+1) for r in range(R)])
        pr(f"| {t:.2f} | {mu_} | {np.quantile(me,.5):.0f} | {np.quantile(me,.9):.0f} | {np.quantile(me,.99):.0f} | {me.max()} |")
    pr("(m_emp = 13 would mean π(|S| > 12) = 0 > e^{-t} is impossible, so it never occurs; the formula's m_n(t) exceeds K = 12 and therefore the statement at m = m_n(t) holds trivially in this p = 12 setting.)")
open("out/analysis_item1_6b.md", "w").write("\n".join(out)); print("\n".join(out))
