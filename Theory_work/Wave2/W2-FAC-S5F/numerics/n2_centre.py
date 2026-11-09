"""n2_centre.py -- N2: along uncapped LS0 paths (S5, exact Gram), record the global-centre offset delta_T,
the level (chosen deletion statistic, standardized), the hole bound (max add statistic over the hole, standardized),
the per-class (u) counts and signed sums, and the deletion/addition thresholds.  Standardized units: Z^2_std =
dquad * s^2 / (n sigma^2) (so that a fixed-set statistic is chi^2_1).
Centre: c_bar = a B/(1+aW) with ghat_G = sqrt(a) eta + ytilde_G, ytilde_G = sqrt(b) zeta_G + sqrt(c) mean_{T cap G} xi.
delta_T := a sum_hit ytilde_G/d_G / (1 + a W)  (the bias part of the centre; d_G = b + c/u_G).
Output: N2_raw.jsonl (one record per path, with per-step arrays subsampled), N2_summary.md."""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bcs_core as bcs

A, B, C, Q = 0.3, 0.4, 0.3, 5
grid = [(2000, 10 ** 4), (2000, 10 ** 6), (2000, 10 ** 12), (5000, 10 ** 4), (5000, 10 ** 8), (10000, 2 * 10 ** 4), (10000, 10 ** 10)]
seeds = range(3)
here = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(here, "N2_raw.jsonl"), "w")
t0 = time.time()
summary = []
for (p, n) in grid:
    for seed in seeds:
        rng = np.random.default_rng(7000 + 13 * seed + p + int(math.log10(n)))
        th = bcs.study_layout(p, c=1.0, s0=4)
        P = bcs.BCS(p, Q, A, B, C, th, n, rng)
        S0 = set(P.S0)
        sc_fac = P.s ** 2 / n  # Z^2_std = dquad * s^2/(n sigma^2), sigma^2 = 1
        H = math.sqrt(2 * math.log(p))
        rec = dict(p=p, n=n, seed=seed, A=math.log(p) / math.log(n), eta=P.eta, steps=[])
        ytil_full = math.sqrt(B) * P.zeta + math.sqrt(C) * np.bincount(P.grp, weights=P.xi, minlength=P.J) / np.bincount(P.grp, minlength=P.J)

        def record(P, T, sc, info):
            k = len(T)
            u = sc["u"]
            Tarr = np.asarray(T)
            hit = u >= 1
            xi_sum = np.bincount(P.grp[Tarr], weights=P.xi[Tarr], minlength=P.J)
            ytil = np.zeros(P.J)
            ytil[hit] = math.sqrt(B) * P.zeta[hit] + math.sqrt(C) * xi_sum[hit] / u[hit]
            d = np.full(P.J, np.inf)
            d[hit] = B + C / u[hit]
            W = float((1.0 / d[hit]).sum())
            delta = A * float((ytil[hit] / d[hit]).sum()) / (1.0 + A * W)
            st = dict(k=k, move=info.get("move"), delta=delta, delta_H=delta / H, W=W,
                      offset=math.sqrt(A) * P.eta / (1.0 + A * W),
                      hist=np.bincount(u.astype(int), minlength=Q + 1).tolist())
            # per-class signed sums of ytil/d (imbalance)
            st["class_sum"] = [float((ytil[hit & (u == uu)] / d[hit & (u == uu)]).sum()) for uu in range(1, Q + 1)]
            st["class_abs"] = [float((np.abs(ytil[hit & (u == uu)]) / d[hit & (u == uu)]).sum()) for uu in range(1, Q + 1)]
            if np.size(sc["Zsq_del"]):
                isN = np.array([t not in S0 for t in T])
                zd = sc["Zsq_del"] * sc_fac
                st["level"] = float(zd[isN].min()) if isN.any() else None
                st["kept_max"] = float(zd[isN].max()) if isN.any() else None
            if np.size(sc["Zsq_add"]):
                za = sc["Zsq_add"] * sc_fac
                O = sc["O"]
                i = int(np.argmax(za))
                st["hole_max"] = float(za[i])
                st["hole_u"] = int(u[P.grp[O[i]]])
            # thresholds (standardized): deletion improving iff Z^2 < Theta_del ; addition improving iff Z^2 > Theta_add
            # Theta_del = del_size / Mfac where lik gain ~ Mfac * Z^2_std, Mfac = nu*n/((n^2-1) psi) * (n sigma^2/s^2) ... use exact small-Z slope
            psi = 0.02 + sc["Q"]
            Mfac = P.nu * n / ((n * n - 1.0) * psi) * (n / P.s ** 2)
            st["M"] = Mfac
            if np.size(sc["del"]):
                st["Theta_del"] = float(np.max(sc["del_size"])) / Mfac
            if np.size(sc["add"]) and np.isfinite(sc["add"]).any():
                st["Theta_add"] = float(-np.max(sc["add_size"])) / Mfac
            rec["steps"].append(st)

        r = bcs.ls0_path(P, range(p), record=record, want_swaps=False)
        moves = [s["move"] for s in r["steps"] if s.get("move")]
        rec["moves"] = r["moves"]
        rec["final_is_S0"] = r["final_is_S0"]
        rec["pure_deletion"] = all(m == "-N" for m in moves)
        S = rec["steps"]
        rec["max_abs_delta_H"] = max(abs(s["delta_H"]) for s in S)
        rec["max_abs_delta_H_bulk"] = max(abs(s["delta_H"]) for s in S if s["k"] >= 50)
        rec["max_hole_over_level"] = max(s["hole_max"] / s["level"] for s in S if s.get("hole_max") and s.get("level"))
        rec["max_hole_minus_level"] = max(s["hole_max"] - s["level"] for s in S if s.get("hole_max") and s.get("level"))
        rec["max_hole_over_thr"] = max(s["hole_max"] / s["Theta_add"] for s in S if s.get("hole_max") and s.get("Theta_add"))
        rec["max_level_over_thr"] = max(s["level"] / s["Theta_del"] for s in S if s.get("level") and s.get("Theta_del"))
        # subsample steps for storage
        keep = sorted(set(list(range(0, len(S), max(1, len(S) // 60))) + list(range(max(0, len(S) - 30), len(S)))))
        rec["steps"] = [S[i] for i in keep]
        out.write(json.dumps(rec) + "\n"); out.flush()
        line = (f"p={p} n={n:.0e} seed={seed} A={rec['A']:.2f}: moves={r['moves']} pure={rec['pure_deletion']} final=S0:{rec['final_is_S0']} "
                f"max|delta|/H={rec['max_abs_delta_H']:.3f} (bulk k>=50: {rec['max_abs_delta_H_bulk']:.3f}) "
                f"max hole/level={rec['max_hole_over_level']:.2f} max(hole-level)={rec['max_hole_minus_level']:.2f} "
                f"max hole/Theta_add={rec['max_hole_over_thr']:.3f} max level/Theta_del={rec['max_level_over_thr']:.3f} [{time.time()-t0:.0f}s]")
        print(line, flush=True)
        summary.append(line)
out.close()
with open(os.path.join(here, "N2_summary.md"), "w") as f:
    f.write("## N2: centre offset, level and hole bound along S5 LS0 paths from [p] (script n2_centre.py; raw N2_raw.jsonl)\n\n")
    f.write("H = sqrt(2 log p); delta_T = a*sum_hit ytilde_G/d_G/(1+aW) (bias part of the global centre, xi-scale); level = chosen "
            "deletion's standardized Z^2 (min over kept nulls); hole = max standardized add statistic over the hole; "
            "Theta_add / Theta_del = standardized thresholds (addition improves iff Z^2 > Theta_add; deletion improves iff Z^2 < Theta_del).\n\n")
    for line in summary:
        f.write("- " + line + "\n")
