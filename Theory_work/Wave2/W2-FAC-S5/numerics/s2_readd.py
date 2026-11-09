"""S2: re-add invariants for greedy backward elimination on a Gaussian quadratic form Phi(T) = g_T' S_TT^-1 g_T.
(a) RM ("re-add <= running max"): for every deleted l, Phi(T u l) - Phi(T) <= max of the deletion losses so far.
(b) RA ("re-add argmin"): for deleted l and retained j: Phi(T u l)-Phi(T) <= Phi(T u l)-Phi(T u l \ j).
Tested on (i) random PD matrices, (ii) one exchangeable group bJ+dI (known global level), (iii) full BCS Sigma."""
import sys, numpy as np

def Phi(S, g, T):
    T = list(T)
    if not T: return 0.0
    return float(g[T] @ np.linalg.solve(S[np.ix_(T, T)], g[T]))

def greedy(S, g):
    p = len(g); T = list(range(p)); levels = []; worst_rm = -np.inf; worst_ra = -np.inf; deleted = []
    while T:
        F = Phi(S, g, T)
        losses = [F - Phi(S, g, [t for t in T if t != j]) for j in T]
        i = int(np.argmin(losses)); j = T[i]; levels.append(losses[i]); deleted.append(j)
        T = [t for t in T if t != j]
        run = max(levels)
        FT = Phi(S, g, T)
        for l in deleted:
            ra = Phi(S, g, T + [l]) - FT
            worst_rm = max(worst_rm, ra - run)
            for jj in T:
                rl = Phi(S, g, T + [l]) - Phi(S, g, [t for t in T if t != jj] + [l])
                worst_ra = max(worst_ra, ra - rl)
    return worst_rm, worst_ra

rng = np.random.default_rng(1)
out = []
for kind in ["random", "group5", "bcs"]:
    rm_viol = ra_viol = 0; rm_max = ra_max = -np.inf; N = 300 if kind != "bcs" else 60
    for it in range(N):
        if kind == "random":
            p = 6; A = rng.standard_normal((p, p + 2)); S = A @ A.T / (p + 2)
        elif kind == "group5":
            p = 5; S = 0.4 * np.ones((p, p)) + 0.3 * np.eye(p)
        else:
            p = 15; grp = np.arange(p) // 5
            S = 0.3 + 0.4 * (grp[:, None] == grp[None, :]) + 0.3 * np.eye(p)
        g = np.linalg.cholesky(S) @ rng.standard_normal(p)
        rm, ra = greedy(S, g)
        rm_viol += rm > 1e-9; ra_viol += ra > 1e-9
        rm_max = max(rm_max, rm); ra_max = max(ra_max, ra)
    print(f"{kind:7s} N={N}: RM violations {rm_viol} (max excess {rm_max:.3g});  RA violations {ra_viol} (max excess {ra_max:.3g})")
