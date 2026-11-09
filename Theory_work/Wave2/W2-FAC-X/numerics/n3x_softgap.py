"""N3X: falsification test of lemmas/X3 (deterministic soft-gap lemma).
Random N(0,1) configurations, random B, kappa'; at each step the deleted point is chosen among all kept points
satisfying rule (R_beta) by one of several adversarial policies (random / farthest-allowed / same-side-farthest /
opposite-side). Checks at every step: (iii) crossing => omega < 4 beta; (viii) D_i subset of (a_i - 4.3b, b_i + 4.3b)
and interval part subset of D_i (when the (vii) assumption holds); (vii) i0 <= Q. Output: N3X_out.txt"""
import numpy as np, sys

def run(m, beta, B, kap, policy, rng, stop=3):
    xi = rng.standard_normal(m)
    srt = np.sort(xi)
    # Q = max # points in a closed interval of length 9 beta
    j = np.searchsorted(srt, srt + 9 * beta, side="right")
    Q = int((j - np.arange(m)).max())
    assume = 4 * Q * beta / (m - Q - 1 + kap) <= beta / 10
    kept = np.ones(m, bool)
    S = xi.sum()
    viol = dict(cross=0, contain=0, interval=0, i0=0, centre=0, window=0)
    x0 = (S + B) / (m + kap)
    i0 = None
    ncross = 0
    i = 0
    while kept.sum() > stop:
        K = kept.sum()
        x = (S + B) / (K + kap)
        kv = np.flatnonzero(kept)
        d = np.abs(xi[kv] - x)
        allowed = kv[d <= d.min() + 2 * beta]
        below = xi[kv][xi[kv] < x]; above = xi[kv][xi[kv] > x]
        a = below.max() if len(below) else -np.inf
        b = above.min() if len(above) else np.inf
        om = b - a
        if i0 is None and om >= 4 * beta:
            i0 = i
        if assume and i0 is None and abs(x - x0) > beta / 10 + 1e-15:
            viol["centre"] += 1   # (vii): |x_i - x_0| <= varpi/10 for i <= M
        # containment check (viii)
        D = ~kept
        if assume and D.any():
            if not np.all((xi[D] > a - 4.3 * beta) & (xi[D] < b + 4.3 * beta)):
                viol["contain"] += 1
        inside = (xi > a) & (xi < b)
        if np.any(inside & kept):
            viol["interval"] += 1
        # choose
        if policy == "random":
            jj = rng.choice(allowed)
        elif policy == "far":
            jj = allowed[np.argmax(np.abs(xi[allowed] - x))]
        elif policy == "side_up":
            up = allowed[xi[allowed] > x]
            jj = up[np.argmax(xi[up])] if len(up) else allowed[0]
        else:  # side_down
            dn = allowed[xi[allowed] < x]
            jj = dn[np.argmin(xi[dn])] if len(dn) else allowed[0]
        if assume and i0 is None and abs(xi[jj] - x0) > 4.1 * beta + 1e-15:
            viol["window"] += 1   # (vii): deletions before M lie in [x0 - 4.1 varpi, x0 + 4.1 varpi]
        kept[jj] = False
        S -= xi[jj]
        x2 = (S + B) / (K - 1 + kap)
        lo, hi = min(x, x2), max(x, x2)
        kv2 = np.flatnonzero(kept)
        if np.any((xi[kv2] > lo) & (xi[kv2] < hi)):
            ncross += 1
            if not (om < 4 * beta):
                viol["cross"] += 1
        i += 1
    if assume and (i0 if i0 is not None else i) > Q:
        viol["i0"] += 1   # (vii) prefix form: M = min(i0, I) <= Q
    return viol, assume, Q, i0, ncross

if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    tot = dict(cross=0, contain=0, interval=0, i0=0, centre=0, window=0); runs = 0; nass = 0; maxcross = 0
    for m in [50, 300, 2000, 5000]:
        for beta in [0.0002, 0.001, 0.01, 0.05, 0.2]:
            for policy in ["random", "far", "side_up", "side_down"]:
                for rep in range(6):
                    B = rng.normal() * 3; kap = 1.0 + rng.exponential(2.0)
                    v, ass, Q, i0, nc = run(m, beta, B, kap, policy, rng)
                    runs += 1; nass += ass; maxcross = max(maxcross, nc)
                    for k in tot: tot[k] += v[k]
    lines = [f"runs {runs}; runs where the (vii) assumption holds: {nass}",
             f"violations: crossing with omega >= 4beta: {tot['cross']}; containment (viii): {tot['contain']}; "
             f"kept point inside (a,b): {tot['interval']}; M=min(i0,I) > Q: {tot['i0']}; "
             f"(vii) centre |x_i-x_0| > varpi/10 before M: {tot['centre']}; (vii) deletion outside x0 +- 4.1 varpi before M: {tot['window']}",
             f"max number of crossings in a run: {maxcross}"]
    open("N3X_out.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
