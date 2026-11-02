"""Summaries of results/sweep.jsonl and the dilution-threshold predictor (goal 3). Seed 7 (Monte Carlo for M_p).
Writes results/sweep_summary.txt and results/threshold.txt.

Population plug-in predictor of log pi0(S0) (median level; REPORT §4.4, PROOF §11):
  v = sigma^2 + sum_k theta_k^2 (independent unit-variance truths, one per group; dilution);
  V_j = -(n/2) log(1 - theta_j^2/v)                      (block keep statistic of truth j);
  O_del_j = ((2p - s0)/s0) sqrt(n+1) exp(-V_j)            (start odds of S0 - j against S0);
  O_swp_j = (g-1) exp(-(n/2) log((v - rho_j^2 theta_j^2)/(v - theta_j^2)))  (same-group proxy swaps);
  N_add   = ((s0+1)/(2p-s0-1)) (p-s0) (n+1)^{-1/2} M(p,n),  M = median of the mean of (1-B)^{-nu}, B ~ Beta(1/2,(n-3)/2);
  log pi0(S0) ~ (s0+1) log(1 - N_add/(s0+1)) - sum_j log(1 + O_del_j + O_swp_j).
"""
import json, math, sys
from collections import defaultdict
import numpy as np
import fav_core as fc

rows = [json.loads(l) for l in open("../results/sweep.jsonl")]
rng = np.random.default_rng(7)
_M = {}


NGRID = np.exp(np.linspace(math.log(150), math.log(40000), 25))


def _Mexact(p, n, sims=400):
    nu = 0.01 + n / 2
    s0 = 14
    B = rng.beta(0.5, (n - 3) / 2, size=(sims, p - s0))
    return float(np.median(np.exp(-nu * np.log1p(-B)).mean(1)))


def Mpn(p, n):
    """median of the mean of (1-B)^{-nu}; Monte Carlo on a 25-point log grid in n, linear interpolation in log n."""
    if p not in _M:
        _M[p] = np.array([_Mexact(p, int(x)) for x in NGRID])
    return float(np.interp(math.log(n), np.log(NGRID), _M[p]))


def predict(scen, p, scale, n, parts=False):
    _, beta, grp = fc.truth(p)
    th = scale * beta
    s0 = len(th)
    v = 1.0 + (th ** 2).sum()
    rho = fc.group_rho(scen, p)[grp] if scen != 1 else np.zeros(s0)
    g = 5
    V = -(n / 2) * np.log1p(-th ** 2 / v)
    Od = ((2 * p - s0) / s0) * math.sqrt(n + 1) * np.exp(-V)
    Os = (g - 1) * np.exp(-(n / 2) * np.log((v - rho ** 2 * th ** 2) / (v - th ** 2)))
    Nadd = (s0 + 1) / (2 * p - s0 - 1) * (p - s0) / math.sqrt(n + 1) * Mpn(p, n)
    lnull = (s0 + 1) * math.log(max(1e-300, 1 - Nadd / (s0 + 1)))
    ltr = -np.log1p(Od + Os).sum()
    if parts:
        return lnull, ltr, Nadd, Od, Os
    return lnull + ltr


def nstar(scen, p, scale, target):
    """smallest n (on a fine log grid) with predicted log pi0 >= target."""
    for n in np.unique(np.round(np.exp(np.linspace(math.log(150), math.log(40000), 400)))).astype(int):
        if predict(scen, p, scale, int(n)) >= target:
            return int(n)
    return None


def med(x):
    x = [v for v in x if v is not None]
    return float(np.median(x)) if x else float("nan")


cells = defaultdict(list)
for r in rows:
    cells[(r["scen"], r["p"], r["scale"], r["n"])].append(r)

L = []
P = lambda s="": L.append(s)
P("# W5-FAVIID sweep summary (exact start law; 20 replicates per cell unless stated)")
P("cols: scen p scale n | reps | Q_n held | max m_real | med log10 pi0(S0) | frac pi0>1/2 | med q | med N_add | "
  "mean #masked (LO<0) | T22(i) bound >= 1-pi0 (count) | med bound | Thm B: max q/Q_real | med Q0/Q_real | "
  "pred log10 pi0 | med decomposition log10 (exact one-change odds)")
viol = 0
allq = []
for key in sorted(cells):
    rs = cells[key]
    scen, p, scale, n = key
    lp = [r["log10_pi0_S0"] for r in rs]
    frac = np.mean([x > math.log10(0.5) for x in lp])
    one_m = [1 - 10 ** x for x in lp]
    ok = sum(b >= om - 1e-12 for b, om in zip([r["T22i_bound"] for r in rs], one_m))
    viol += len(rs) - ok
    masked = np.mean([sum(1 for x in r["LO"] if x < 0) for r in rs])
    qr = [r["q"] / r["Qreal"] for r in rs if r["Qreal"]]
    q0 = [r["Q0"] / r["Qreal"] for r in rs if r["Qreal"]]
    s0 = 14
    dec = []
    for r in rs:
        Nadd = math.exp(r["log_Nadd"])
        lnull = (s0 + 1) * math.log(max(1e-300, 1 - Nadd / (s0 + 1))) if Nadd < s0 + 1 else -np.inf
        ltr = -sum(math.log1p(math.exp(-lo) + (math.exp(ls) if np.isfinite(ls) else 0.0)) for lo, ls in zip(r["LO"], r["LSW"]))
        dec.append((lnull + ltr) / math.log(10))
    P("S%d %4d %.1f %4d | %2d | %2d/%2d | %d | %7.2f | %.2f | %.3f | %.3f | %5.2f | %2d/%2d | %.3g | %s | %s | %7.2f | %7.2f" % (
        scen, p, scale, n, len(rs), sum(r["unions"] for r in rs), len(rs), max(r["m_real"] for r in rs), med(lp), frac,
        med([r["q"] for r in rs]), med([math.exp(r["log_Nadd"]) for r in rs]), masked, ok, len(rs),
        med([r["T22i_bound"] for r in rs]), ("%.3f" % max(qr)) if qr else "  -  ", ("%.3f" % med(q0)) if q0 else "  -  ",
        predict(scen, p, scale, n) / math.log(10), med(dec)))
P()
P("T22(i) bound violations (must be 0): %d" % viol)
open("../results/sweep_summary.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))

# rate checks at large n: sqrt(n/log n)(1 - pi0), and ratio to the sharp first-order prediction (s0+1)M/(2 sqrt(n+1))
T = []
Q = lambda s="": T.append(s)
Q("# Rate and sharp-constant check: median of sqrt(n/log n)(1 - pi0(S0)) and of (1-pi0(S0)) / [(s0+1) M(p,n) p/(2p) / sqrt(n+1)]")
for key in sorted(cells):
    scen, p, scale, n = key
    if n < 800:
        continue
    rs = cells[key]
    om = np.array([1 - 10 ** r["log10_pi0_S0"] for r in rs])
    pred = 15 * (p - 14) / (2 * p - 15) * Mpn(p, n) / math.sqrt(n + 1)
    Q("S%d %4d %.1f %4d | sqrt(n/log n)(1-pi0) = %.2f | (1-pi0)/(1-exp(-N_add pred)) = %.2f | med q/xi_n(eps0=0) = %.2f" % (
        scen, p, scale, n, np.median(om) * math.sqrt(n / math.log(n)), np.median(om) / (-math.expm1(-pred)),
        np.median([r["q"] for r in rs]) / math.sqrt(math.log(p * 2 ** min(16, int(math.isqrt(n)))) / (n + 1))))
Q()
Q("# Thresholds (population plug-in predictor): n*_half = first n with predicted pi0(S0) >= 1/2;")
Q("# n*_hit = first n with predicted Q_f^min pi0(S0) >= 3, Q_f^min = 4 N0 (L+6) (final-run iid draws, T >= 1).")
Q("# Also the null-only threshold n*_null (deletions and swaps ignored) and the deletion-only n*_del.")
for scen in (1, 3, 4, 6):
    for p in (500, 1000):
        for scale in (0.5, 1.0):
            nh = nstar(scen, p, scale, math.log(0.5))
            nn = None
            for n in range(150, 40000, 10):
                lnull, ltr, Nadd, Od, Os = predict(scen, p, scale, n, parts=True)
                if nn is None and lnull >= math.log(0.5):
                    nn = n
            nd = None
            for n in range(150, 40000, 10):
                lnull, ltr, Nadd, Od, Os = predict(scen, p, scale, n, parts=True)
                if ltr >= math.log(0.5):
                    nd = n
                    break
            nhit = None
            for n in range(150, 40000, 10):
                N0 = max(2500, n, p)
                Lr = max(4, math.ceil(math.log2(n + 1)))
                if predict(scen, p, scale, n) >= math.log(3.0 / (4 * N0 * (Lr + 6))):
                    nhit = n
                    break
            Q("S%d p=%4d scale=%.1f: n*_half = %s, n*_null = %s, n*_del = %s, n*_hit = %s" % (scen, p, scale, nh, nn, nd, nhit))
open("../results/threshold.txt", "w").write("\n".join(T) + "\n")
print("\n".join(T))
