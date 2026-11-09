"""Falsification numerics for the inequality chain of L2.2(iii) at finite n (the asymptotic threshold a_n is never
reached at simulable n, so each link is tested with the actual most extreme outside null):
for size-K sets T containing S0: |x_T| <= 2; some retained null with |tau| <= 3.5; M_T >= 1/2 (1 - 3 n^{-1/3});
for l = most extreme outside null and j = retained null nearest x_T:
  V_jl >= (1-g)tau_l^2 - 2g|tau_l||tau_j| - (1+g) tau_j^2   and   best swap gain >= G_sw(j,l) >= M_T V_jl;
and the implication  M_T V_jl > Delta_K  =>  best neighbour is a swap.  usage: python l2_chain.py OUT.jsonl"""
import sys, json, math
import numpy as np
import pk_core as pk
out = open(sys.argv[1], "w")
cnt = dict(rows=0, x_ok=0, j_ok=0, M_ok=0, V_ok=0, G_ok=0, impl_applicable=0, impl_ok=0)
for (rho, n, frac, co, seed) in [(0.5, 20000, 0.95, (1.4, 1.0, 1.8, 1.2), 0), (0.5, 20000, 0.6, (1.4, 1.0, 1.8, 1.2), 1),
                                 (0.8, 8000, "max", (1.0,), 3), (0.95, 8000, 0.8, (-1.4, -1.0, -1.8, 1.2), 4),
                                 (0.2, 8000, 0.8, (1.4, 1.0, 1.8, 1.2), 6), (0.5, 40000, 0.9, (1.4, 1.0, 1.8, 1.2), 5)]:
    p = n - 1 if frac == "max" else int(round(frac * n))
    S0 = [2, 26, 53, 75][:len(co)]
    th = np.zeros(p); th[S0] = co
    P = pk.make_cs(rho, th, n, seed)
    K = P.K; z = P.z; nu, al, be = P.nu, P.al, P.be; k1 = pk.xi_units(P)
    isS0 = np.zeros(p, bool); isS0[S0] = True; nulls = np.flatnonzero(~isS0)
    sm = pk.start_mode_cs(P, pk.cs_partition(p, 16))
    rng = np.random.default_rng(7 + seed)
    sets = []
    if sm["size"] == K: sets.append(("start", sorted(sm["mode"])))
    for r in range(4): sets.append((f"rand{r}", sorted(S0 + rng.choice(nulls, K - len(S0), replace=False).tolist())))
    xs = P.xi
    sets.append(("adv_absxi", sorted(S0 + nulls[np.argsort(-np.abs(xs[nulls]))[:K - len(S0)]].tolist())))
    sets.append(("low", sorted(S0 + nulls[np.argsort(xs[nulls])[:K - len(S0)]].tolist())))
    sets.append(("high", sorted(S0 + nulls[np.argsort(-xs[nulls])[:K - len(S0)]].tolist())))
    for name, T in sets:
        inT = np.zeros(p, bool); inT[T] = True
        k = K; A = float((z[inT] ** 2).sum()); B = float(z[inT].sum())
        g = lambda u: be / (al + u * be)
        gk = g(k)
        quad = (A - gk * B * B) / al; psi = 0.02 + (n - 1.0) - n * quad
        c = gk * B
        tau = (z - c) / k1
        xT = float(np.median(xs[nulls] - tau[nulls]))
        MT = nu * n * k1 ** 2 / (al * psi)
        rn = nulls[inT[nulls]]; on = nulls[~inT[nulls]]
        j = rn[np.argmin(np.abs(tau[rn]))]; l = on[np.argmax(np.abs(tau[on]))]
        V = tau[l] ** 2 - tau[j] ** 2 - gk * (tau[l] - tau[j]) ** 2
        Vlb = (1 - gk) * tau[l] ** 2 - 2 * gk * abs(tau[l] * tau[j]) - (1 + gk) * tau[j] ** 2
        Gjl = -nu * math.log1p(-MT * V / nu)
        # best swap over all (exact): for each retained, best outside is an extreme of tau
        tin = z[inT] - c; tout = z[~inT] - c
        ext = [int(np.argmin(tout)), int(np.argmax(tout))]
        Dq = tout[ext][None, :] ** 2 - tin[:, None] ** 2 - gk * (tout[ext][None, :] - tin[:, None]) ** 2
        Gs = float((-nu * np.log1p(-n * Dq / (al * psi))).max())
        LD = float(pk._ldet(P, k)); dK = P.lw[k - 1] - P.lw[k] - 0.5 * (float(pk._ldet(P, k - 1)) - LD)
        Gd = float((dK - nu * np.log1p(n * (1 + g(k - 1)) * tin ** 2 / (al * psi))).max())
        rec = dict(n=n, p=p, rho=rho, seed=seed, kind=name, xT=xT, min_abs_tau_ret=float(abs(tau[j])), MT=MT,
                   MT_bound=0.5 * (1 - 3 * n ** (-1 / 3)), tau_l=float(tau[l]), V=float(V), Vlb=float(Vlb), Gjl=Gjl,
                   MTV=MT * V, best_swap=Gs, best_del=Gd, Delta_K=float(dK))
        cnt["rows"] += 1; cnt["x_ok"] += abs(xT) <= 2; cnt["j_ok"] += abs(tau[j]) <= 3.5; cnt["M_ok"] += MT >= rec["MT_bound"]
        cnt["V_ok"] += V >= Vlb - 1e-9; cnt["G_ok"] += (Gs >= Gjl - 1e-9) and (Gjl >= MT * V - 1e-9)
        if MT * V > dK:
            cnt["impl_applicable"] += 1; cnt["impl_ok"] += Gs > max(Gd, 0)
        out.write(json.dumps(rec) + "\n")
print(json.dumps({k: int(v) for k, v in cnt.items()}))
