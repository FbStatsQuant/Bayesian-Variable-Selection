"""n1_paths.py -- N1: uncapped LS0 paths from the full model [p] on exact-Gram multi-class designs.
Records per run: final set vs S0, #moves, move types, class-count trajectory, max |X_c| along the path, and the
end state per class (retained nulls, their xi signs).  Usage: python n1_paths.py <case> [seeds] -> N1_<case>.jsonl
Cases (see CASES): trap tests (truth-free class with small kappa, large log p/log n) and positive tests (truths in
every class).
"""
import sys, json, math, time, numpy as np
import mc_core as mc

CASES = {
    # name: dict(k, R, sizes, truths{class: [(pos_in_class, coef)]}, n)
    "A_trap_indep":  dict(R=[[0.5, 0.0], [0.0, 0.7]], sizes=[2000, 2000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]}, n=8000),
    "B_ctrl_indep":  dict(R=[[0.5, 0.0], [0.0, 0.3]], sizes=[2000, 2000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]}, n=8000),
    "C_trap_corr":   dict(R=[[0.5, 0.3], [0.3, 0.7]], sizes=[2000, 2000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]}, n=8000),
    "D_truth_both":  dict(R=[[0.5, 0.3], [0.3, 0.7]], sizes=[2000, 2000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8)], 1: [(76, -1.2)]}, n=8000),
    "E_n6_r07":      dict(R=[[0.5, 0.3], [0.3, 0.7]], sizes=[5000, 5000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]}, n=10 ** 6),
    "F_n6_r09":      dict(R=[[0.5, 0.3], [0.3, 0.9]], sizes=[5000, 5000], truths={0: [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]}, n=10 ** 6),
    "G_k3_truths":   dict(R=[[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], sizes=[1300, 1300, 1300],
                          truths={0: [(3, 1.4), (27, -1.0)], 1: [(54, 1.8)], 2: [(76, -1.2)]}, n=8000),
    "H_k3_n6":       dict(R=[[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], sizes=[3000, 3000, 3000],
                          truths={0: [(3, 1.4), (27, -1.0)], 1: [(54, 1.8)], 2: [(76, -1.2)]}, n=10 ** 6),
}


def build(case):
    c = CASES[case]
    sizes = c["sizes"]
    cls = np.concatenate([np.full(s, i) for i, s in enumerate(sizes)])
    D = mc.MCDesign(cls, np.array(c["R"], float))
    p = D.p
    th = np.zeros(p)
    off = np.cumsum([0] + sizes[:-1])
    S0 = []
    for cl, lst in c["truths"].items():
        for pos, coef in lst:
            j = int(off[cl] + pos)
            th[j] = coef
            S0.append(j)
    return D, th, sorted(S0), c["n"]


def run(case, seeds):
    D, th, S0, n = build(case)
    p = D.p
    assert p <= n // 2, 'class (P): p <= n/2 so that the full model is admissible (K = p)'
    out = open(f"N1_{case}.jsonl", "a")
    for seed in seeds:
        rng = np.random.default_rng(1000 + seed)
        P = mc.MCData(D, th, n, rng)
        t0 = time.time()
        maxX = np.zeros(D.k)
        traj = []

        def rec(P, T, sc, info):
            C, X = P.centre(T)
            np.maximum(maxX, np.abs(X), out=maxX)
            if len(traj) % max(1, p // 40) == 0 or info["size"] <= len(S0) + 12:
                traj.append(dict(size=info["size"], counts=info["counts"], X=[float(x) for x in X],
                                 move=info.get("move"), g_del=info["best_del_N"], g_add=info["best_add"],
                                 g_sw=info["best_swap"]))
        res = mc.ls0_path(P, list(range(p)), S0, record=rec)
        fin = set(res["final"])
        extras = sorted(fin - set(S0))
        moves = [s.get("move") for s in res["steps"] if s.get("move")]
        types = {}
        for m in moves:
            types[m] = types.get(m, 0) + 1
        ex_info = [dict(j=int(j), cls=int(D.cls[j]), xi=float(P.xi[j])) for j in extras]
        kap = D.kappa_eff(np.array([sum(1 for s in S0 if D.cls[s] == c) for c in range(D.k)], float))
        rec_out = dict(case=case, seed=seed, n=n, p=p, k=D.k, log_p_over_log_n=math.log(p) / math.log(n),
                       kappa_marg=D.kappa_marg.tolist(), kappa_eff_at_S0=kap.tolist(),
                       moves=res["moves"], final_size=len(fin), extras=len(extras), missing=len(set(S0) - fin),
                       scored_S0=res["scored_S0"], move_types=types, extras_info=ex_info,
                       maxX=maxX.tolist(), H=math.sqrt(2 * math.log(2 * p)), secs=time.time() - t0, traj=traj)
        out.write(json.dumps(rec_out) + "\n"); out.flush()
        print(f"{case} seed={seed} n={n} p={p}: moves={res['moves']} final={len(fin)} extras={len(extras)} "
              f"missing={rec_out['missing']} scoredS0={res['scored_S0']} types={types} maxX={np.round(maxX,3).tolist()} "
              f"kappa_eff={np.round(kap,3).tolist()} ({time.time()-t0:.0f}s)")
        if extras:
            print("   extras:", ex_info)
    out.close()


if __name__ == "__main__":
    case = sys.argv[1]
    seeds = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0, 1, 2]
    run(case, seeds)
