"""fna_check.py -- F-NA / F-SHARP: NA over the full lattice for exact-Gram compound symmetry, via the exact 1-D formulas
(cs1d.CS1D).  For each (a, s0, n, alpha): p = round(n^alpha); draw z (exactly, except that for n-1-p >= 1e9 the
chi^2_{n-1-p} variate is replaced by its normal approximation -- APPROXIMATE branch, R04 item 7); scan the one-sided lattice sets
T = S0 ∪ {top-m nulls by idiosyncratic noise h} for m = 0..p-s0-1 (and the mirror bottom-m) and random sets;
report max over these T of max_l [F(T∪l) - F(T)]: a positive value is a certified witness of NA failure; a
nonpositive maximum means only 'no witness found among the scanned sets'.
Gains computed from the exact identity Q(T∪l) = Q(T) - (n/A)(N/(N+1))(z_l - L_T/N)^2, N = |T| + A/B  (no cancellation).
-> FNA_raw.jsonl, FNA_summary.md"""
import math, json, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import bvs_core as bc


def draw(a, s0, p, n, rng):
    pat = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
    th = np.zeros(p); th[:s0] = pat[np.arange(s0) % 6]
    n1 = n - 1.0
    h = rng.standard_normal(p); h0 = rng.standard_normal()
    Sth = (1 - a) * th + a * th.sum()
    noise = math.sqrt(1 - a) * h + math.sqrt(a) * h0
    Sinv_noise = (noise - (a / (1 - a + p * a)) * noise.sum()) / (1 - a)
    pe = float(noise @ Sinv_noise)
    chi = rng.chisquare(n - 1 - p) if n - 1 - p < 1e9 else (n - 1 - p) + math.sqrt(2 * (n - 1 - p)) * rng.standard_normal()
    Y2 = n1 * float(th @ Sth) + 2 * math.sqrt(n1) * float(th @ noise) + pe + chi
    z = (n1 * Sth + math.sqrt(n1) * noise) * math.sqrt(n1) / math.sqrt(Y2)
    return z, h


def add_gains(a, z, n, p, K, logw, T_mask):
    n1 = n - 1.0
    A = (n + 1.0) * n1 * (1 - a) + 1.0; B = (n + 1.0) * n1 * a
    A2 = n1 * (1 - a) + 1.0; B2 = n1 * a
    k = int(T_mask.sum())
    zT = z[T_mask]
    P, L = float((zT ** 2).sum()), float(zT.sum())
    b = B / (A + k * B)
    Q = 0.02 + n1 - (n / A) * (P - b * L * L)
    N = k + A / B
    zo = z[~T_mask]
    dQ = (n / A) * (N / (N + 1.0)) * (zo - L / N) ** 2
    nu = 0.01 + n / 2.0
    def Dk(kk):
        if kk == 0: return 0.0
        return -0.5 * ((kk - 1) * math.log(A) + math.log(A + kk * B) - (kk - 1) * math.log(A2) - math.log(A2 + kk * B2))
    g = (logw[k + 1] - logw[k]) + (Dk(k + 1) - Dk(k)) - nu * np.log1p(-dQ / Q)
    return g


def run(job):
    a, s0, n, alpha, seed = job
    p = max(s0 + 3, int(round(n ** alpha)))
    rng = np.random.default_rng(91 + 1000 * seed + int(1e3 * alpha) + 7 * s0)
    z, h = draw(a, s0, p, n, rng)
    K = min(p, int(n // 2)); logw = bc.log_prior_w(p, K)
    nulls = np.arange(s0, p)
    best = -np.inf; best_m = None; nfail = 0; nsets = 0
    for sgn in (1, -1):
        order = nulls[np.argsort(-sgn * h[nulls])]
        for m in range(0, len(nulls)):
            T = np.zeros(p, bool); T[:s0] = True; T[order[:m]] = True
            if T.sum() >= K: continue
            g = add_gains(a, z, n, p, K, logw, T)
            mx = float(g.max()); nsets += 1
            if mx > 0: nfail += 1
            if mx > best: best, best_m = mx, sgn * m
    rnd_fail = 0
    for _ in range(50):
        m = int(rng.integers(0, len(nulls)))
        T = np.zeros(p, bool); T[:s0] = True; T[rng.choice(nulls, size=m, replace=False)] = True
        if T.sum() >= K: continue
        rnd_fail += float(add_gains(a, z, n, p, K, logw, T).max()) > 0
    return dict(a=a, s0=s0, n=n, alpha=alpha, p=p, seed=seed, onesided_max_gain=best, argmax_m=best_m,
                onesided_fail_sets=nfail, onesided_sets=nsets, NA_fail=(nfail > 0), rand_fail=rnd_fail)


if __name__ == "__main__":
    As = [0.3, 0.7]; s0s = [1, 4]; ns = [1e6, 1e9, 1e12]; alphas = [0.10, 0.14, 0.18, 0.22, 0.30]; seeds = 10
    jobs = [(a, s0, n, al, s) for a in As for s0 in s0s for n in ns for al in alphas for s in range(seeds)]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(run, jobs, chunksize=4))
    with open("FNA_raw.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    L = ["# F-NA / F-SHARP: full-lattice NA on one-sided sets, exact-Gram CS (fna_check.py)", "",
         "Note (R04/R06): rows with n = 1e12 replace the chi^2_{n-1-p} variate by its normal approximation (approximate draws). A positive max add gain is a certified witness of NA failure; a nonpositive one means no witness among the scanned sets.", "",
         "| a | s0 | n | alpha=log p/log n | p | runs | runs with NA failure on a one-sided set | median max add gain | random sets failing |",
         "|---|---|---|---|---|---|---|---|---|"]
    for a in As:
        for s0 in s0s:
            for n in ns:
                for al in alphas:
                    rr = [r for r in rows if r["a"] == a and r["s0"] == s0 and r["n"] == n and r["alpha"] == al]
                    L.append("| %.1f | %d | %.0e | %.2f | %d | %d | %d | %.2f | %d/%d |" % (a, s0, n, al, rr[0]["p"], len(rr),
                             sum(r["NA_fail"] for r in rr), float(np.median([r["onesided_max_gain"] for r in rr])),
                             sum(r["rand_fail"] for r in rr), 50 * len(rr)))
    open("FNA_summary.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("done", round(time.time() - t0, 1))
