"""PC2: adversarial hill-climb for a counterexample to D14's osc d <= D_* (R1_C §E).
Maximises osc d / D_* over (X, y) at p = 4..6, small n, arbitrary 2-3 block partitions, keeping a, dA, dH, r < 1.
Fixed seeds 1..8; ~1-2 minutes."""
import numpy as np
from bvs_common import suff_from_data, d_table, card_Dstar


def score(X, y, blocks, K):
    G, z, Y, n = suff_from_data(X, y)
    cs = card_Dstar(G, z, Y, n, blocks, K)
    if not cs['ok']:
        return -1.0, cs, None
    _, d, _ = d_table(G, z, Y, n, blocks, K)
    return float(d.max() - d.min()) / cs['Dstar'], cs, float(d.max() - d.min())


best_overall = 0
for seed in range(1, 9):
    rng = np.random.default_rng(seed)
    p = int(rng.integers(4, 7))
    n = int(rng.integers(p + 3, 30))
    K = min(p, n // 2)
    blocks = [list(range(0, p // 2)), list(range(p // 2, p))]
    X = rng.standard_normal((n, p))
    y = rng.standard_normal(n)
    cur, cs, osc = score(X, y, blocks, K)
    for it in range(400):
        step = 0.3 * (0.995 ** it)
        X2 = X + step * rng.standard_normal(X.shape)
        y2 = y + step * rng.standard_normal(n)
        s2, cs2, osc2 = score(X2, y2, blocks, K)
        if s2 > cur:
            X, y, cur, cs, osc = X2, y2, s2, cs2, osc2
    best_overall = max(best_overall, cur)
    print(f"seed {seed} p={p} n={n} K={K}: max osc/D* = {cur:.4f}  (osc={osc}, D*={cs.get('Dstar')}, a={cs['a']:.3g},"
          f" dA={cs['dA']:.3g}, dH={cs['dH']:.3g})")
print("overall max ratio:", best_overall, "-> counterexample" if best_overall > 1 else "-> no counterexample")
