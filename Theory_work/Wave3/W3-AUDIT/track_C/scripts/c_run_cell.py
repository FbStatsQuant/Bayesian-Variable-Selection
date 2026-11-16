"""W3-AUDIT track C -- one task = (design, n, p) with reps 1..R.  Writes a long CSV
<outdir>/D<did>_n<n>_p<p>.csv with columns design,name,n,p,rep,placement,proxy,key,value (rep = 0: population layer).
Usage: python3 c_run_cell.py DID N P REPS OUTDIR [--fast]
Threads: run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 (1 CPU per task)."""
import csv
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_designs import make_design, draw_X, standardize, S0 as S0N   # noqa: E402
import c_proxies as P                                                   # noqa: E402

EPS = (0.5, 0.2, 0.1)
UMAX = 15
QCAP = 400


def main():
    did, n, p, reps, outdir = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    os.makedirs(outdir, exist_ok=True)
    fn = os.path.join(outdir, f"D{did:02d}_n{n}_p{p}.csv")
    rows = []
    d = make_design(did, p)
    A = math.log(p) / math.log(n)
    j0 = math.ceil((2 * A + 1) * S0N) + 1
    ms = P.msharp(n, p, S0N)
    rn = math.sqrt(math.log(n) / n)
    cap = min(QCAP, n // 2)

    def put(rep, plc, proxy, key, val):
        rows.append((did, d.name, n, p, rep, plc, proxy, key, val))

    T0 = time.time()
    # ---------------- population layer (n enters only through the leak threshold eps * r_n) -------------------
    t = time.time()
    put(0, "-", "meta", "A_cell", A); put(0, "-", "meta", "j0", j0); put(0, "-", "meta", "msharp", ms)
    put(0, "-", "P1P2pop", "lam_min_Sigma", d.lam_min_pop())
    po = P.PopOracle(d)
    pop = {}
    for plc, (S0, beta) in d.placements().items():
        S0 = list(map(int, S0)); theta = beta
        GS = po.rows(S0)
        gmu = GS.T @ theta; vmu = float(theta @ GS[:, S0] @ theta)
        put(0, plc, "P1pop", "lam_min_Sigma_S0", float(np.linalg.eigvalsh(GS[:, S0])[0]))
        _, lam = P.greedy_chain(po, S0, S0N + 16)
        for k in (1, 2, 4, 8, 16):
            put(0, plc, "P1pop", f"phi2_k{k}", lam[S0N + k])
        vis = [P.visibility_path(po, p, S0, theta, j, GS[jj], gmu, vmu, UMAX)[0].min() for jj, j in enumerate(S0)]
        put(0, plc, "P4pop", "min_delta2_pop", float(min(vis)))
        g = P.leakage_scores(po, p, S0, theta, gmu, vmu, UMAX)
        for e in EPS:
            put(0, plc, "P5pop", f"Qsize_eps{e}", int((g > e * rn).sum()))
        put(0, plc, "P5pop", "g_max_outside_S0", float(np.max(g[np.isfinite(g)])) if np.isfinite(g).any() else 0.0)
        Q = np.flatnonzero(g > 0.2 * rn)
        pop[plc] = (S0, theta, Q)
    put(0, "-", "time", "pop_sec", time.time() - t)

    # ---------------- sample layer ----------------------------------------------------------------------------------
    taus = (2 * rn, 0.3, 0.5)
    for rep in range(1, reps + 1):
        tr = time.time()
        X = draw_X(d, n, rep)
        sd = X.std(0, ddof=1)
        Z = standardize(X); del X
        so = P.SampleOracle(Z)
        t = time.time()
        Kg = max(ms, S0N + 16)
        cp = P.chunk_pass(Z, Kg, taus)
        put(rep, "-", "time", "chunk_sec", time.time() - t)
        for k in (2, 4, 8, 16, 20):
            if k in cp["gersh"]:
                put(rep, "-", "P1P2", f"gersh_LB_k{k}", cp["gersh"][k])
        put(rep, "-", "P1P2", "max_abs_r", cp["top"][0])
        for t_i, tau in zip(("2rn", "0.3", "0.5"), taus):
            put(rep, "-", "P6", f"deg_max_tau{t_i}", int(cp["deg"][list(taus).index(tau)].max()))
            put(rep, "-", "P6", f"deg_med_tau{t_i}", float(np.median(cp["deg"][list(taus).index(tau)])))
        # P2 unanchored chain to m#
        t = time.time()
        kmax2 = min(ms, n - 1, p)
        if kmax2 >= 2:
            _, lam2 = P.greedy_chain(so, [cp["top"][1], cp["top"][2]], kmax2)
            for k in (2, 4, 8, 16, 32, 64):
                if k in lam2:
                    put(rep, "-", "P2", f"lam_k{k}", lam2[k])
            put(rep, "-", "P2", "lam_msharp", lam2[kmax2]); put(rep, "-", "P2", "msharp_used", kmax2)
            put(rep, "-", "P2", "g_hat", (n - 1) * lam2[kmax2] / n)
        put(rep, "-", "time", "P2_sec", time.time() - t)
        # P10
        t = time.time()
        try:
            dn = P.op_norm_diff(Z, d.sigma_matvec)
            put(rep, "-", "P10", "op_norm", dn)
            put(rep, "-", "P10", "op_x_sqrt_p_loglogn", dn * math.sqrt(p * math.log(math.log(n))))
        except Exception as ex:                                          # pragma: no cover
            put(rep, "-", "P10", "error", str(ex)[:60])
        put(rep, "-", "time", "P10_sec", time.time() - t)
        rng = np.random.default_rng(777 + 10000 * did + rep)
        for plc, (S0, beta, Q) in pop.items():
            t = time.time()
            theta = beta * sd[S0]                                         # theta* = D_x beta*
            GS = so.rows(S0)
            gmu = GS.T @ theta; vmu = float(theta @ GS[:, S0] @ theta)
            # P7 energy, signal floor, margin
            put(rep, plc, "P7", "M_hat", vmu * (n - 1) / n)
            phi0 = float(np.linalg.eigvalsh(GS[:, S0])[0])
            put(rep, plc, "P1", "phi2_k0", phi0)
            put(rep, plc, "P7", "BM_rate", np.min(theta ** 2) * n * phi0 / math.log(n))
            mg = min(P.margin_path(so, p, S0, theta, j, gmu, vmu, j0) for j in S0)
            put(rep, plc, "P7", "margin_over_logn", (n - 1) * mg / math.log(n))
            # P1 anchored chain
            _, lam = P.greedy_chain(so, S0, S0N + 16)
            for k in (1, 2, 4, 8, 16):
                put(rep, plc, "P1", f"phi2_k{k}", lam[S0N + k])
            # P4 visibility
            vis = min(P.visibility_path(so, p, S0, theta, j, GS[jj], gmu, vmu, UMAX)[0].min()
                      for jj, j in enumerate(S0))
            put(rep, plc, "P4", "v_hat", (n - 1) * vis / math.log(n))
            # P8 Occam terms
            t1, t2 = P.occam_terms(Z, S0)
            put(rep, plc, "P8", "O1_over_rn", t1 / rn); put(rep, plc, "P8", "O12_over_rn", (t1 + t2) / rn)
            # P3 / P6 / P9 on Q_hat = Q_{0.2}(n)
            put(rep, plc, "P5", "Qsize", Q.size)
            if Q.size <= cap:
                RQ = so.rows(Q)
                vals, lQ = P.bordered_lmin(RQ[:, Q], RQ, exclude=Q)
                put(rep, plc, "P3", "lam_QQ", lQ); put(rep, plc, "P3", "min_l_lam_Ql", float(min(vals.min(), lQ)))
            else:
                put(rep, plc, "P3", "Q_over_cap", Q.size)
            sets = P.lattice_sets(Q, S0, cap, rng)
            nu, nu99, l1max, w0, tmax, tq99 = P.local_and_width(Z, so.rows, sets, 20, rng)
            for v in tmax:
                put(rep, plc, "P6", f"l1tail_nu{v}_max", tmax[v]); put(rep, plc, "P6", f"l1tail_nu{v}_q99", tq99[v])
            put(rep, plc, "P6", "nu_q99_L0.1", nu99[0.1]); put(rep, plc, "P6", "Tmax", max(len(T) for T in sets))
            put(rep, plc, "P6", "l1_coef_max", l1max)
            put(rep, plc, "P9", "w0_hat", w0)
            put(rep, plc, "P9", "Qminus_S0_over_logn", (Q.size - len(S0)) / math.log(n))
            put(rep, plc, "time", "plc_sec", time.time() - t)
        put(rep, "-", "time", "rep_sec", time.time() - tr)
    put(0, "-", "time", "task_sec", time.time() - T0)
    tmp = fn + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["design", "name", "n", "p", "rep", "placement", "proxy", "key", "value"])
        w.writerows(rows)
    os.replace(tmp, fn)
    print(f"done {fn} {time.time() - T0:.1f}s")


if __name__ == "__main__":
    main()
