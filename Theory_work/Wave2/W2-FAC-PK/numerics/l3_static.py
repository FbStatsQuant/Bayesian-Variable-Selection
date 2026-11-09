"""Falsification numerics for L3 (static gain bounds on T >= S0) and L3.4 (budget).
For each data set: many sets T with S0 <= T, |T| <= K, of several kinds and sizes m = |T minus S0|:
random subsets; two-sided extreme tails (the m nulls with largest |xi|); one-sided tails (m largest / smallest xi);
central cluster (m nulls nearest 0); mixed (tails + some central); sets on the actual LS0 path.
Record best deletion gain (exact, gain form) / log n, the nearest distance d_T, M_T, and whether any neighbour improves.
Claims: m <= m_e: best null-deletion gain >= (c_D - eps) log n asymptotically; m > m_e: >= (1/2 - eps) log n.
Budget: F(S0) - F(S~0) <= K (0.5 log n + 2.4); path moves m* vs K.
usage: python l3_static.py OUT.jsonl"""
import sys, json, math
import numpy as np
import pk_core as pk

def gains(P, T):
    n, p, K = P.n, P.p, P.K
    z = P.z; nu, al, be = P.nu, P.al, P.be
    inT = np.zeros(p, bool); inT[list(T)] = True
    k = int(inT.sum()); A = float((z[inT] ** 2).sum()); B = float(z[inT].sum())
    g = lambda u: be / (al + u * be)
    quad = (A - g(k) * B * B) / al; psi = 0.02 + (n - 1.0) - n * quad
    c = g(k) * B
    k1 = pk.xi_units(P)
    isS0 = np.zeros(p, bool); isS0[list(P.S0)] = True
    rn = np.flatnonzero(inT & ~isS0)
    tin = z[rn] - c
    LD = float(pk._ldet(P, k)); dw = P.lw[k - 1] - P.lw[k] - 0.5 * (float(pk._ldet(P, k - 1)) - LD)
    Gd = dw - nu * np.log1p(n * (1 + g(k - 1)) * tin ** 2 / (al * psi))
    MT = nu * n * k1 ** 2 / (al * psi)
    return float(Gd.max()), float(np.min(np.abs(tin)) / k1), float(MT), float(dw)

def Fset(P, T):
    return P.F(sorted(T))

def main():
  out = open(sys.argv[1], "w")
  summary = []
  for (rho, n, frac, co, seed) in [(0.5, 20000, 0.95, (1.4, 1.0, 1.8, 1.2), 0), (0.5, 20000, 0.6, (1.4, 1.0, 1.8, 1.2), 1),
                                   (0.8, 8000, "max", (1.0,), 3), (0.95, 8000, 0.8, (-1.4, -1.0, -1.8, 1.2), 4),
                                   (0.2, 20000, 0.8, (1.4, -1.0, 1.8, -1.2), 6), (0.5, 60000, 0.9, (1.4, 1.0, 1.8, 1.2), 5)]:
      p = n - 1 if frac == "max" else int(round(frac * n))
      S0 = [2, 26, 53, 75][:len(co)]
      th = np.zeros(p); th[S0] = co
      P = pk.make_cs(rho, th, n, seed)
      K = P.K; ln = math.log(n); me = math.ceil(ln ** 2)
      kap = (1 - rho) / rho; cD = 0.5 - 1 / (len(S0) + 1 + kap)
      isS0 = np.zeros(p, bool); isS0[S0] = True; nulls = np.flatnonzero(~isS0)
      sgn = 1.0 if sum(co) > 0 else -1.0
      xs = P.xi
      rng = np.random.default_rng(11 + seed)
      ms = sorted(set([1, 2, 3, 5, 10, 30, me // 2, me, me + 1, 2 * me, 10 * me, K // 20, K // 4, K // 2, K - len(S0)]))
      ms = [m for m in ms if 1 <= m <= K - len(S0)]
      rows = []
      for m in ms:
          kinds = {"rand": rng.choice(nulls, m, replace=False), "tails2": nulls[np.argsort(-np.abs(xs[nulls]))[:m]],
                   "top": nulls[np.argsort(-xs[nulls])[:m]], "bottom": nulls[np.argsort(xs[nulls])[:m]],
                   "central": nulls[np.argsort(np.abs(xs[nulls]))[:m]]}
          if m >= 4:
              half = m // 2
              kinds["tails_plus_central"] = np.concatenate([nulls[np.argsort(-np.abs(xs[nulls]))[:half]], nulls[np.argsort(np.abs(xs[nulls]))[:m - half]]])
              kinds["top_and_one_low"] = np.concatenate([nulls[np.argsort(-xs[nulls])[:m - 1]], nulls[np.argsort(xs[nulls])[:1]]])
          for name, R in kinds.items():
              T = set(S0) | set(int(v) for v in R)
              gd, d, MT, dw = gains(P, T)
              r = dict(n=n, p=p, rho=rho, seed=seed, m=m, m_e=me, kind=name, best_del_over_logn=gd / ln, d=d, MT=MT,
                       claim=(cD if m <= me else 0.5), cD=cD)
              rows.append(r); out.write(json.dumps(r) + "\n")
      # path sets + budget
      sm = pk.start_mode_cs(P, pk.cs_partition(p, 16))
      path_sets = []
      def cb(dd):
          if dd["nmoves"] % max(1, K // 25) == 0 or dd["k"] - len(S0) <= 40:
              path_sets.append(set(int(v) for v in np.flatnonzero(dd["inT"])))
      rr = pk.path_from(P, sm["mode"], callback=cb)
      for T in path_sets:
          if set(S0) <= T and len(T) > len(S0):
              m = len(T) - len(S0)
              gd, d, MT, dw = gains(P, T)
              r = dict(n=n, p=p, rho=rho, seed=seed, m=m, m_e=me, kind="path", best_del_over_logn=gd / ln, d=d, MT=MT,
                       claim=(cD if m <= me else 0.5), cD=cD)
              rows.append(r); out.write(json.dumps(r) + "\n")
      budget = Fset(P, S0) - Fset(P, sm["mode"]) if sm["size"] == K else None
      s = dict(n=n, p=p, rho=rho, seed=seed, K=K, start=sm["size"], moves=rr["n_moves"], moves_over_K=rr["n_moves"] / K,
               final_is_S0=rr["final_is_S0"], budget=budget, budget_bound=K * (0.5 * ln + 2.4),
               min_ratio_small=min([r["best_del_over_logn"] for r in rows if r["m"] <= me]),
               min_ratio_large=min([r["best_del_over_logn"] for r in rows if r["m"] > me]),
               cD=cD, worst_small=min([r for r in rows if r["m"] <= me], key=lambda r: r["best_del_over_logn"])["kind"],
               worst_large=min([r for r in rows if r["m"] > me], key=lambda r: r["best_del_over_logn"])["kind"])
      summary.append(s); print(json.dumps(s), flush=True)


if __name__ == "__main__":
    main()
