"""Falsification numerics for L1 (start structure) and L2 (static scan bounds at size K), exact-Gram CS, p > K.
L1: on each data set check (a) |S~0| = K, (b) blockwise order in truth-free blocks, (c) |u_b - u_b'| <= 1 over regular
blocks, (d) no regular block full, and record min over regular blocks of u_b.
L2: for size-K sets T of several kinds (start mode; uniformly random; random containing S0; 'adversarial' = S0 + the
K - s0 nulls with largest |xi|; 'low' = S0 + lowest-xi nulls), compute exactly (closed form, gain form):
  max deletion gain vs the bound Delta_K and vs 0.5 log n + 1.2; best swap gain; whether best neighbour is a swap;
  for T containing S0: whether an outside null with xi <= -a_n exists, and the swap gain lower bound check;
  N_n = number of regular-block minima <= -a_n.
usage: python l12_check.py OUT.jsonl"""
import sys, json, math
import numpy as np
import pk_core as pk

def scan_gains(P, T):
    n, p, K = P.n, P.p, P.K
    z = P.z; nu, al, be = P.nu, P.al, P.be
    inT = np.zeros(p, bool); inT[list(T)] = True
    k = int(inT.sum()); A = float((z[inT] ** 2).sum()); B = float(z[inT].sum())
    g = lambda u: be / (al + u * be)
    quad = (A - g(k) * B * B) / al; psi = 0.02 + (n - 1.0) - n * quad
    c = g(k) * B
    tin = z[inT] - c; tout = z[~inT] - c
    LD = float(pk._ldet(P, k))
    dw = P.lw[k - 1] - P.lw[k] - 0.5 * (float(pk._ldet(P, k - 1)) - LD)
    Gd = dw - nu * np.log1p(n * (1 + g(k - 1)) * tin ** 2 / (al * psi))
    ext = [int(np.argmin(tout)), int(np.argmax(tout))]
    tl = tout[ext]
    Dq = tl[None, :] ** 2 - tin[:, None] ** 2 - g(k) * (tl[None, :] - tin[:, None]) ** 2
    Gs = -nu * np.log1p(-n * Dq / (al * psi))
    MT = nu * n * pk.xi_units(P) ** 2 / (al * psi)
    return dict(Delta_K=float(dw), max_del=float(Gd.max()), max_swap=float(Gs.max()), MT=float(MT))

out = open(sys.argv[1], "w")
for (rho, n, frac, lay, seed) in [(0.5, 20000, 0.95, "aligned", 0), (0.5, 20000, 0.6, "aligned", 1), (0.2, 8000, 0.8, "mixed", 2),
                                  (0.8, 8000, "max", "s0=1", 3), (0.95, 8000, 0.8, "negtot", 4), (0.5, 40000, 0.9, "aligned", 5)]:
    p = n - 1 if frac == "max" else int(round(frac * n))
    LAY = {"aligned": (1.4, 1.0, 1.8, 1.2), "mixed": (1.4, -1.0, 1.8, -1.2), "s0=1": (1.0,), "negtot": (-1.4, -1.0, -1.8, 1.2)}
    co = LAY[lay]; S0 = [2, 26, 53, 75][:len(co)]
    th = np.zeros(p); th[S0] = co
    P = pk.make_cs(rho, th, n, seed)
    sgn = 1.0 if sum(co) > 0 else -1.0
    xs = sgn * P.xi        # sign-corrected coordinates: theta_bar > 0 convention
    blocks = pk.cs_partition(p, 16)
    sm = pk.start_mode_cs(P, blocks)
    S = set(sm["mode"]); K = P.K
    isS0 = np.zeros(p, bool); isS0[S0] = True
    reg = [b for b in blocks if len(b) == 16 and not isS0[b].any()]
    tf = [b for b in blocks if not isS0[b].any()]
    ok_b = all((min([xs[j] for j in b if j in S], default=np.inf) > max([xs[j] for j in b if j not in S], default=-np.inf)) for b in tf)
    ub = [sum(1 for j in b if j in S) for b in reg]
    an = 2 + math.sqrt(math.log(n) + 30)
    Nn = sum(1 for b in reg if xs[b].min() <= -an)
    rec = dict(test="L1", rho=rho, n=n, p=p, K=K, lay=lay, seed=seed, a_size_is_K=(len(S) == K), b_order=ok_b,
               c_spread=(max(ub) - min(ub)), d_no_full=(max(ub) <= 15), u_min=min(ub), u_max=max(ub), N_n=Nn,
               ell_plus_s0_plus2=pk.ell_cap(n, p) + len(S0) + 2, S0_in_start=set(S0) <= S)
    out.write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
    rng = np.random.default_rng(100 + seed)
    nulls = np.flatnonzero(~isS0)
    kinds = {"start": sorted(S)}
    for r in range(3):
        kinds[f"uniform{r}"] = sorted(rng.choice(p, K, replace=False).tolist())
        kinds[f"withS0_{r}"] = sorted(S0 + rng.choice(nulls, K - len(S0), replace=False).tolist())
    kinds["adv_absxi"] = sorted(S0 + nulls[np.argsort(-np.abs(xs[nulls]))[:K - len(S0)]].tolist())
    kinds["low_xi"] = sorted(S0 + nulls[np.argsort(xs[nulls])[:K - len(S0)]].tolist())
    kinds["high_xi"] = sorted(S0 + nulls[np.argsort(-xs[nulls])[:K - len(S0)]].tolist())
    kinds["start_minus_truth"] = sorted((S - {S0[0]}) | {int(nulls[np.flatnonzero(~np.isin(nulls, list(S)))[0]])}) if S0[0] in S else sorted(S)
    for name, T in kinds.items():
        Ts = set(T)
        g_ = scan_gains(P, T)
        has = set(S0) <= Ts
        ext_out = bool(np.any((xs <= -an) & ~np.isin(np.arange(p), T) & ~isS0))
        rec = dict(test="L2", n=n, p=p, lay=lay, seed=seed, kind=name, S0_in_T=has, extreme_outside=ext_out,
                   i_del_le_DeltaK=g_["max_del"] <= g_["Delta_K"] + 1e-9, DeltaK_minus_bound=g_["Delta_K"] - (0.5 * math.log(n) + 1.2),
                   best_is_swap=g_["max_swap"] > max(g_["max_del"], 0.0), max_swap=g_["max_swap"], max_del=g_["max_del"],
                   iii_bound_ok=(g_["max_swap"] >= 0.5 * math.log(n) + 2) if (has and ext_out) else None,
                   ii_order_n=(g_["max_swap"] / n) if not has else None, MT=g_["MT"])
        out.write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
