"""R11 (Opus council seat, round 2) independent checks. Read-only on the package; writes only to stdout.
1. N1/N3 aggregates quoted in STATEMENT §0.
2. Generic G1 (REPORT §6): for H = (n+1)G + I, the increment of L_U = log det H_U - log det(G_U + I) when one column is
   added is <= log(n+1) for ANY Gram matrix (and >= 0), and nested Q_U = y'y - n z_U' H_U^{-1} z_U is nonincreasing.
3. L2.2(iii) constants: V >= log n + 5 chain with |tau_j| <= 3.5, gamma_K -> 0.
"""
import json, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "..", "..", "numerics")

# ---- 1. aggregates
n1 = [json.loads(l) for l in open(os.path.join(NUM, "N1_raw.jsonl"), encoding="utf-8")]
sat = [r for r in n1 if r["saturated"]]
print("N1 rows", len(n1), "saturated", len(sat),
      "unsaturated starts", sorted(r["start"] for r in n1 if not r["saturated"]),
      "unsat (n,p)", sorted({(r["n"], r["p"]) for r in n1 if not r["saturated"]}))
mr1_miss = [r for r in n1 if not r["MR1_scores"]]
print("N1 MR1 misses", len(mr1_miss), "all saturated:", all(r["saturated"] for r in mr1_miss))
print("N1 cap_2K misses", sum(1 for r in n1 if r["moves"] > r["cap_2K"] or not r["final_is_S0"]))
print("N1 swaps after first deletion (max)", max(r["swaps_after_first_del"] for r in n1),
      "additions:", sum(r["counts"].get("+N", 0) + r["counts"].get("+T", 0) for r in n1))
for n in sorted({r["n"] for r in n1}):
    W = [r["lead_swaps"] for r in n1 if r["n"] == n and abs(r["p"] / r["n"] - 0.95) < 0.01]
    if W: print("  p/n=0.95 n=%d W range %s" % (n, (min(W), max(W))))
n3 = [json.loads(l) for l in open(os.path.join(NUM, "N3_raw_final360.jsonl"), encoding="utf-8")]
keys = sorted(n3[0].keys())
print("N3 rows", len(n3), "keys", keys)
nf = [r for r in n3 if not r.get("final_is_S0", True)]
print("N3 not ending at S0:", len(nf), sorted({(r.get("n"), r.get("rho"), r.get("layout", r.get("theta_bar"))) for r in nf}, key=str))
print("N3 swaps after first deletion (max)", max(r.get("swaps_after_first_del", 0) for r in n3))
if "cap_2K" in n3[0]:
    ok = sum(1 for r in n3 if r["moves"] <= r["cap_2K"] or r.get("final_is_S0") is False and r.get("S0_scored_2K", False))
    print("N3 moves <= cap_2K:", sum(1 for r in n3 if r["moves"] <= r["cap_2K"]))
ratio = [r["moves"] / r["K"] for r in n3 if "K" in r]
if ratio: print("N3 max m*/K %.3f" % max(ratio))

# ---- 2. generic G1
rng = np.random.default_rng(11)
worst_inc, worst_neg, worst_Q = -1e9, 1e9, -1e9
for trial in range(400):
    n = int(rng.integers(8, 60)); p = int(rng.integers(3, 40))
    X = rng.standard_normal((n, p)) @ (np.eye(p) + rng.uniform(-1, 1) * rng.standard_normal((p, p)) * rng.uniform(0, 1))
    X -= X.mean(0); X /= np.sqrt((X ** 2).sum(0) / (n - 1))
    y = rng.standard_normal(n) + X[:, :2] @ rng.standard_normal(2); y -= y.mean(); y *= np.sqrt((n - 1) / (y @ y))
    G = X.T @ X / (n - 1)          # correlation-scale Gram (diag 1)
    z = X.T @ y / np.sqrt(n - 1)
    def L(U):
        if not U: return 0.0
        GU = G[np.ix_(U, U)]
        return np.linalg.slogdet((n + 1) * GU + np.eye(len(U)))[1] - np.linalg.slogdet(GU + np.eye(len(U)))[1]
    def Q(U):
        if not U: return y @ y
        H = (n + 1) * G[np.ix_(U, U)] + np.eye(len(U))
        return y @ y - n * z[U] @ np.linalg.solve(H, z[U])
    order = list(rng.permutation(p)[: min(p, n - 2)])
    for k in range(1, len(order) + 1):
        inc = L(order[:k]) - L(order[:k - 1])
        worst_inc = max(worst_inc, inc - math.log(n + 1)); worst_neg = min(worst_neg, inc)
        worst_Q = max(worst_Q, Q(order[:k]) - Q(order[:k - 1]))
print("G1: max (L increment - log(n+1)) = %.3e (must be <= 0); min increment = %.3e (>= 0); max Q increase = %.3e (<= 0)"
      % (worst_inc, worst_neg, worst_Q))

# ---- 3. L2.2(iii) chain at moderate/large n (gamma_K ~ 1/K, |tau_l| <= Hbar + 2)
for n in [10**4, 10**6, 10**9, 10**15]:
    K = n // 2; p = n - 1; kappa = 1.0; g = 1 / (K + kappa)
    Lnn = math.log(math.log(n)); Hb = math.sqrt(2 * math.log(2 * p) + 2 * Lnn)
    tl2_min = math.log(n) + 30; tl_max = Hb + 2; tj = 3.5
    V = (1 - g) * tl2_min - 2 * g * tl_max * tj - (1 + g) * tj ** 2
    print("n=%.0e  V_lower - (log n + 5) = %.2f ; G_sw_lower - (0.5 log n + 2) = %.2f" %
          (n, V - (math.log(n) + 5), 0.5 * (1 - 3 * n ** (-1 / 3)) * (math.log(n) + 5) - (0.5 * math.log(n) + 2)))

# ---- 4. REPORT §5 heuristic: at size K the swap must beat Delta_K = log((2p-K)/K) + 0.5 log n; with M = 1/2 the number of
# nulls with M tau^2 > Delta_K is ~ p * Phi_bar(sqrt(2 Delta_K)) ~ K / (2 sqrt(n)) / polylog, NOT increasing with p.
from math import erfc, sqrt
for n in [10**4, 10**6]:
    K = n // 2
    for p in [n - 1, n ** 1.5, n ** 2, n ** 3]:
        D = math.log((2 * p - K) / K) + 0.5 * math.log(n)
        cnt = p * 0.5 * erfc(sqrt(2 * D) / sqrt(2))
        print("n=%.0e p=%.1e Delta_K=%.2f  expected #nulls with tau^2/2 > Delta_K: %.1f" % (n, p, D, cnt))
