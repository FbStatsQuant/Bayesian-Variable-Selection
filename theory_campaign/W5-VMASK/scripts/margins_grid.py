"""Task 4: PXN P6 margin c2 vs T38FULL LH-LAT margin m0 vs the brute-force population minimum, on LH exact Gram.

Population residual Delta(T) = theta' Sigma theta - theta' Sigma[:,T] Sigma_TT^{-1} Sigma[T,:] theta, which is the
in-sample Delta of 00_COMMON exactly when X'X = (n-1) Sigma. Design: c pairs + v visible groups + one null group,
groups of size g (margins do not depend on g >= 3 or on the number of null groups: every neighbour class is present).

For each parameter setting and each lattice state S = S° u M' (M' a proper subset of M) we compute
  brute(S) = min_{B in N(S) u {S}} Delta(B) - min_{A in P(S)} Delta(A)     (P = progress, N = non-progress)
and report
  brute_phi2 = min over states with Phi >= 2  (what LH-LAT / LS-score need)   vs  m0 (T38FULL)
  brute_all  = min over all states            (what PXN P6 / Thm A(A3) need)  vs  c2 (PXN)
  brute_L    = min over deletions/swaps B of S0 of Delta(B)                   vs  c2 (PXN's (L) deletion part)
A discrepancy is any closed form that EXCEEDS the brute-force value (an invalid bound), or a claimed-sharp m0 that
is strictly below brute_phi2 (not sharp). No randomness. Output: ../results/margins_grid.txt
"""
import itertools, math
import numpy as np
from vm_core import unit_cov_pair, unit_cov_group


def build(g, rhos_a, rhos_b, psis, betas, vis, rho_vis, rho_null):
    c = len(psis)
    blocks, theta_parts = [], []
    for i in range(c):
        blocks.append(unit_cov_pair_het(g, rhos_a[i], rhos_b[i], psis[i]))
        t = np.zeros(2 * g); t[0] = betas[i]; t[g] = -psis[i] * betas[i]
        theta_parts.append(t)
    for k, bv in enumerate(vis):
        blocks.append(unit_cov_group(g, rho_vis)); t = np.zeros(g); t[0] = bv; theta_parts.append(t)
    blocks.append(unit_cov_group(g, rho_null)); theta_parts.append(np.zeros(g))
    p = sum(b.shape[0] for b in blocks)
    Sig = np.zeros((p, p)); off = 0
    for b in blocks:
        k = b.shape[0]; Sig[off:off + k, off:off + k] = b; off += k
    theta = np.concatenate(theta_parts)
    hubs_a = [2 * i * g for i in range(c)]
    hubs_b = [(2 * i + 1) * g for i in range(c)]
    hubs_v = [(2 * c + k) * g for k in range(len(vis))]
    return Sig, theta, hubs_a, hubs_b, hubs_v


def unit_cov_pair_het(g, ra, rb, psi):
    Sa = np.full((g, g), ra); np.fill_diagonal(Sa, 1.0)
    Sb = np.full((g, g), rb); np.fill_diagonal(Sb, 1.0)
    u, v = Sa[:, 0], Sb[:, 0]
    return np.block([[Sa, psi * np.outer(u, v)], [psi * np.outer(v, u), Sb]])


def Delta(Sig, theta, T):
    tot = theta @ Sig @ theta
    if not T:
        return tot
    T = list(T)
    a = Sig[T] @ theta
    return tot - a @ np.linalg.solve(Sig[np.ix_(T, T)], a)


def brute(Sig, theta, ha, hb, hv):
    p = len(theta)
    S0 = set(ha + hb + hv)
    Sref = ha + hv
    c = len(hb)
    res_all, res_2 = np.inf, np.inf
    for mask in range(2 ** c - 1):
        S = set(Sref + [hb[i] for i in range(c) if (mask >> i) & 1])
        phi = len(S ^ S0)
        prog, non = [], [Delta(Sig, theta, S)]
        for l in range(p):
            if l in S:
                continue
            T = S | {l}
            (prog if len(T ^ S0) < phi else non).append(Delta(Sig, theta, T))
        for t in S:
            T = S - {t}
            non.append(Delta(Sig, theta, T))
            for l in range(p):
                if l in S:
                    continue
                T2 = (S - {t}) | {l}
                (prog if len(T2 ^ S0) < phi else non).append(Delta(Sig, theta, T2))
        m = min(non) - min(prog)
        res_all = min(res_all, m)
        if phi >= 2:
            res_2 = min(res_2, m)
    # (L) deletion / swap part at S0
    L = np.inf
    for t in S0:
        L = min(L, Delta(Sig, theta, S0 - {t}))
        for l in range(p):
            if l not in S0:
                L = min(L, Delta(Sig, theta, (S0 - {t}) | {l}))
    return res_all, res_2, L


def m0_T38(rhos_b, psis, betas, vis):
    R = [b * b * s * s * (1 - s * s) for b, s in zip(betas, psis)]
    kap = [rb * rb * (1 - s * s) / (1 - s * s * rb * rb) for rb, s in zip(rhos_b, psis)]
    t2 = [b * b * (1 - s * s) ** 2 for b, s in zip(betas, psis)]
    return min([(1 - max(kap)) * min(R)] + t2 + [v * v for v in vis])


def c2_PXN(rho, psis, betas, vis):
    """PXN PROOF §9.3 margin list (common rho), lambda_0 from (F4): (1 - max|psi|)(1 - rho)."""
    G = [b * b * s * s * (1 - s * s) for b, s in zip(betas, psis)]
    eta = [rho * rho * (1 - s * s) / (1 - s * s * rho * rho) for s in psis]
    lam0 = (1 - max(abs(s) for s in psis)) * (1 - rho)
    c4 = min([b * b * (1 - s * s) ** 2 for b, s in zip(betas, psis)] + [b * b * (1 - s * s) for b, s in zip(betas, psis)]
             + G + [v * v for v in vis])
    items = [min(G), min(G) * (1 - max(eta)), c4]
    items += [v * v * (1 - rho * rho) for v in vis]
    items += [Gi * (1 - e) for Gi, e in zip(G, eta)]
    items += [lam0 * b * b for b in betas] + [lam0 * b * b * (1 + s * s) for b, s in zip(betas, psis)]
    items += [b * b * (1 - s * s) ** 2 for b, s in zip(betas, psis)]
    return min(items)


lines = []
hdr = "c rho psis betas vis | c2(PXN) brute_all brute_L | m0(T38) brute_phi2 | flags"
lines.append(hdr)
nflag = 0
nrows = 0
worst_c2 = (np.inf, None); worst_m0 = (np.inf, None)
g = 3
grid = []
for c in (1, 2, 3):
    for rho in (0.4, 0.7, 0.85):
        for psi in sorted(set([0.1, 0.3, 0.5, round(rho - 0.05, 2), round(rho + 0.05, 2), 0.95])):
            for beta in (0.5, 1.0, 2.0):
                grid.append((c, rho, [psi] * c, [beta * (-1) ** i for i in range(c)], [1.0]))
# heterogeneous pairs (argmax R != argmax kappa possible; T38FULL allows rho_b per group)
rng = np.random.default_rng(424242)
het = []
for k in range(40):
    c = int(rng.integers(2, 4))
    rho = float(rng.choice([0.4, 0.7, 0.85]))
    psis = [float(np.round(rng.uniform(0.05, 0.95), 2)) * float(rng.choice([-1, 1])) for _ in range(c)]
    betas = [float(np.round(rng.uniform(0.3, 2.5), 2)) * float(rng.choice([-1, 1])) for _ in range(c)]
    het.append((c, rho, psis, betas, [float(np.round(rng.uniform(0.3, 2), 2))]))
for (c, rho, psis, betas, vis) in grid + het:
    Sig, theta, ha, hb, hv = build(g, [rho] * c, [rho] * c, psis, betas, vis, rho, rho)
    ba, b2, bL = brute(Sig, theta, ha, hb, hv)
    c2 = c2_PXN(rho, psis, betas, vis)
    m0 = m0_T38([rho] * c, psis, betas, vis) if c >= 2 else float('nan')
    inside = all(abs(s) < rho for s in psis)
    flags = []
    if c2 > ba + 1e-12:
        flags.append("c2>brute_all(INVALID)")
    if c2 > bL + 1e-12:
        flags.append("c2>brute_L(INVALID)")
    if c >= 2 and m0 > b2 + 1e-12:
        flags.append("m0>brute_phi2(INVALID)")
    if c >= 2 and m0 < b2 - 1e-9:
        flags.append(f"m0 not sharp (ratio {m0 / b2:.3f})")
    if ba <= 0 or (c >= 2 and b2 <= 0):
        flags.append("NONPOSITIVE population margin")
    if not inside:
        flags.append("outside |psi|<rho")
    nrows += 1
    if any("INVALID" in f or "NONPOS" in f for f in flags):
        nflag += 1
    if inside and ba < worst_c2[0]:
        worst_c2 = (ba, (c, rho, psis, betas, vis))
    lines.append(f"{c} {rho} {psis} {betas} {vis} | {c2:.5f} {ba:.5f} {bL:.5f} | {m0:.5f} {b2:.5f} | {'; '.join(flags)}")

# g sensitivity: one case at g = 9 vs g = 3
chk = []
for gg in (3, 9):
    Sig, theta, ha, hb, hv = build(gg, [0.7] * 2, [0.7] * 2, [0.5, 0.3], [1.0, -1.4], [1.0], 0.7, 0.7)
    chk.append(brute(Sig, theta, ha, hb, hv))
lines.append(f"g-sensitivity (c=2, rho=.7, psi=(.5,.3), beta=(1,-1.4)): g=3 {chk[0]}, g=9 {chk[1]}")
nsharp = sum(1 for l in lines if "not sharp" in l)
summ = [f"rows: {nrows}; rows with an INVALID closed form or a nonpositive margin: {nflag}",
        f"rows where T38FULL's m0 is strictly below the brute-force Phi>=2 minimum (m0 valid but not sharp): {nsharp}",
        f"smallest brute_all inside |psi|<rho: {worst_c2[0]:.5f} at {worst_c2[1]}"]
open("../results/margins_grid.txt", "w").write("\n".join(summ + [""] + lines) + "\n")
print("\n".join(summ))
print(lines[-1])
