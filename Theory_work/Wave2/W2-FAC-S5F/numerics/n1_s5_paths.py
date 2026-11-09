"""n1_s5_paths.py -- N1: exact-Gram S5 (a=.3,b=.4,c=.3,q=5), uncapped LS0 path from [p] at large n.
Records per path: pure deletion?, final = S0?, per-step (k, chosen Z^2, within/between decomposition, best add gain,
best swap gain, max hole add-statistic, u of deleted member's group, group-count histogram) -> N1_raw.jsonl.
Usage: python n1_s5_paths.py [quick]"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bcs_core as bcs

quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
A, B, C, Q = 0.3, 0.4, 0.3, 5
grid = []
for p in ([200, 1000] if quick else [200, 1000, 2000]):
    for n in [10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12]:
        if p > n // 2:
            continue
        for cc in [0.5, 1.0]:
            grid.append((p, n, cc))
seeds = range(3 if quick else 5)
out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "N1_raw.jsonl"), "a" if not quick else "w")
t0 = time.time()
for (p, n, cc) in grid:
    for seed in seeds:
        rng = np.random.default_rng(1000 * seed + p + int(math.log10(n)))
        th = bcs.study_layout(p, c=cc, s0=4)
        P = bcs.BCS(p, Q, A, B, C, th, n, rng)
        S0 = set(P.S0)
        rec = dict(p=p, n=n, c=cc, seed=seed, A=math.log(p) / math.log(n), steps=[])

        def record(P, T, sc, info):
            k = len(T)
            u = sc["u"]
            hist = np.bincount(u.astype(int), minlength=Q + 1).tolist()
            st = dict(k=k, move=info.get("move"), best_add=info["best_add"], best_swap=info["best_swap"],
                      best_del_N=info["best_del_N"], best_del_T=info["best_del_T"], hist=hist)
            if "j" in info and info.get("move", "").startswith("-"):
                j = info["j"]
                idx = list(sc["T"]).index(j)
                st["Zsq_del"] = float(sc["Zsq_del"][idx])
                st["u_j"] = int(u[P.grp[j]])
                # within / between decomposition of the deleted null (xi-scale): w = xi_j - mean xi over kept group
                G = P.grp[j]
                members = [t for t in sc["T"] if P.grp[t] == G]
                st["w_j"] = float(P.xi[j] - np.mean(P.xi[members]))
            if np.size(sc["Zsq_add"]):
                O = sc["O"]
                zs = sc["Zsq_add"]
                i = int(np.argmax(zs))
                st["max_Zsq_add"] = float(zs[i])
                st["u_add"] = int(u[P.grp[O[i]]])
            rec["steps"].append(st)

        r = bcs.ls0_path(P, range(p), record=record, want_swaps=(p <= 1000))
        moves = [s["move"] for s in r["steps"] if s.get("move")]
        rec["moves"] = r["moves"]
        rec["final_is_S0"] = r["final_is_S0"]
        rec["final_size"] = len(r["final"])
        rec["pure_deletion"] = all(m == "-N" for m in moves)
        rec["n_swap"] = sum(m.startswith("sw") for m in moves)
        rec["n_add"] = sum(m.startswith("+") for m in moves)
        rec["n_delT"] = sum(m == "-T" for m in moves)
        rec["max_best_add"] = max(s["best_add"] for s in rec["steps"])
        rec["max_best_swap"] = max(s["best_swap"] for s in rec["steps"])
        rec["min_del_gain"] = min(s["best_del_N"] for s in rec["steps"] if s.get("move", "") == "-N")
        rec["hist_path"] = [s["hist"] for s in rec["steps"][:: max(1, len(rec["steps"]) // 40)]]
        out.write(json.dumps(rec) + "\n")
        out.flush()
        print(f"p={p} n={n:.0e} c={cc} seed={seed} A={rec['A']:.2f}: moves={r['moves']} pure={rec['pure_deletion']} "
              f"final=S0:{rec['final_is_S0']} maxAdd/logn={rec['max_best_add']/math.log(n):.3f} "
              f"maxSwap/logn={rec['max_best_swap']/math.log(n):.3f} minDel/logn={rec['min_del_gain']/math.log(n):.3f} "
              f"[{time.time()-t0:.0f}s]", flush=True)
out.close()
