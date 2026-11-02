"""Is the study's n = 200 masking (median pi0(S0) ~ 1e-12 in S1/S3/S4/S6) weak-signal masking?

Simulates the dev generator (Scripts/Data_generators/gen_dev_data.R; numpy RNG, so distributionally equal,
not bitwise) for scenarios S1, S3, S4, S6, p in {500, 1000}, signal scale cc in {1, 0.5}, and computes exactly:
  * the v3 partition (B = 14), all block tables, pi0 by convolution: log pi0(S0), log pi0(R_2), start mode;
  * per true variable j (block b, T = S0 cap C_b minus j):
      LO0(j) = log pi0(S0) - log pi0(S0 - j)          (exact start odds of keeping j, given the rest of S0)
      LO1(j) = F(S0) - F(S0 - j)                      (exact posterior odds)
      V0(j) = -nu log(1 - x^blk_j)  with x^blk the partial R^2 of x_j on y given X_T (block view; total RSS)
      V1(j) = -nu log(1 - x^full_j) with x^full the partial R^2 given X_{S0 - j} (posterior view)
      V0pop(j) = population prediction (n-1) theta_j^2 Var(x_j | X_T) / (2 v_T) + 1/2,
                 v_T = sigma^2 + theta' Sigma theta - (signal captured by T) (population residual variance)
      the T27/CL(L) statistic L_j^2 := population delta^2_{T,j}/sigma^2-scale, i.e. (n-1) theta_j^2 Var(x_j|T)
  * start-masked truths := {j : LO0(j) < 0}.
Output: results/study_n200.jsonl.  Seeds: 30000000 + 100000*scen + 1000*(p==1000) + 10*cc_index + rep.
"""
import json, math, sys, time
import numpy as np
from pxn_core import *

N = 200


def sigma_scen(s, p):
    grp = np.arange(p) // 5
    H = grp[:, None] == grp[None, :]
    if s == 1:
        return np.eye(p)
    if s == 3:
        return 0.7 * H + 0.3 * np.eye(p)
    if s == 4:
        return 0.85 * H + 0.15 * np.eye(p)
    if s == 6:
        rho = 0.4 + 0.1 * (grp % 6)
        S = H * rho[:, None]
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError


def gen_X(s, p, rng, N=200):
    grp = np.arange(p) // 5
    if s == 1:
        return rng.standard_normal((N, p))
    rho = {3: np.full(p, 0.7), 4: np.full(p, 0.85), 6: 0.4 + 0.1 * (grp % 6)}[s]
    f = rng.standard_normal((N, p // 5))
    return np.sqrt(rho) * f[:, grp] + np.sqrt(1 - rho) * rng.standard_normal((N, p))


def truth(p):
    s0, step = 14, {500: 7, 1000: 13}[p]
    pos = [3, 2, 4, 1, 5, 3]
    pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0)
    block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1  # 0-based
    beta = np.array([pattern[i % 6] for i in k])
    return active, beta


def run(s, p, cc, rep, N=200):
    seed = 30000000 + 100000 * s + 1000 * (p == 1000) + 10 * [1.0, 0.5].index(cc) + rep + (0 if N == 200 else 7 * N)
    rng = np.random.default_rng(seed)
    X = gen_X(s, p, rng, N)
    act, beta = truth(p)
    th = np.zeros(p)
    th[act] = beta
    y = cc * (X @ th) + rng.standard_normal(N)
    D = Data(X, y)
    blocks = v3_blocks(D)
    T = Tables(D, blocks)
    L = StartLaw(T)
    S0 = sorted(act.tolist())
    rec = dict(scen=s, n=N, p=p, cc=cc, rep=rep, seed=seed, B=D.B)
    rec["log_pi0_S0"] = L.log_pi0(S0)
    rec["log_pi0_R2"] = L.log_mass_Rd(S0, 2)
    rec["log_pi0_R0"] = L.log_mass_Rd(S0, 0)
    mode, lm = L.start_mode()
    rec["mode_missing"] = sorted(set(S0) - set(mode))
    rec["mode_extras"] = sorted(set(mode) - set(S0))
    rec["log_pi0_mode"] = lm
    FS0 = log_F(D, [S0])[0]
    Sig = sigma_scen(s, p)
    thc = cc * th  # raw coefficients; columns have unit population variance so theta (standardised) ~ thc
    tSt = thc @ Sig @ thc
    per = []
    for j in S0:
        b = T.where[j][0]
        Tb = [k for k in blocks[b] if k in S0 and k != j]
        Sm = [k for k in S0 if k != j]
        lo0 = rec["log_pi0_S0"] - L.log_pi0(Sm)
        lo1 = FS0 - log_F(D, [Sm])[0]

        def partial_x(cond):
            Yc = D.y
            if cond:
                Xc = D.X[:, cond]
                P = Xc @ np.linalg.lstsq(Xc, np.column_stack([Yc, D.X[:, j]]), rcond=None)[0]
                ry, rx = Yc - P[:, 0], D.X[:, j] - P[:, 1]
            else:
                ry, rx = Yc, D.X[:, j]
            return (rx @ ry) ** 2 / ((rx @ rx) * (ry @ ry))
        xb, xf = partial_x(Tb), partial_x(Sm)
        # population: Var(x_j | T), signal captured by T (projection of mu on span X_T)
        if Tb:
            STT = Sig[np.ix_(Tb, Tb)]
            vj = Sig[j, j] - Sig[j, Tb] @ np.linalg.solve(STT, Sig[Tb, j])
            cT = Sig[Tb] @ thc
            capT = cT @ np.linalg.solve(STT, cT)
            cj = Sig[j] @ thc - Sig[j, Tb] @ np.linalg.solve(STT, cT)
        else:
            vj, capT, cj = Sig[j, j], 0.0, Sig[j] @ thc
        vT = 1.0 + tSt - capT
        delta2 = (N - 1) * cj ** 2 / vj  # population delta^2_{T,j} (raw scale)
        per.append(dict(j=j, beta=float(cc * th[j]), block=b, Tsize=len(Tb), LO0=lo0, LO1=lo1,
                        V0=-D.nu * math.log(1 - xb), V1=-D.nu * math.log(1 - xf),
                        V0pop=delta2 / (2 * vT) + 0.5, vT=vT, delta2=delta2))
    rec["per_truth"] = per
    return rec


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "nsweep":
    # n sweep at fixed p = 1000, scenario list, scale 0.5 (seed offset 7*N)
    scen = [int(a) for a in sys.argv[1].split(",")]
    R = int(sys.argv[2])
    out = open("../results/study_nsweep.jsonl", "a")
    for s in scen:
        for N in (400, 800, 1600):
            for rep in range(R):
                t0 = time.time()
                r = run(s, 1000, 0.5, rep, N)
                out.write(json.dumps(r) + "\n"); out.flush()
                nm = sum(1 for q in r["per_truth"] if q["LO0"] < 0)
                print(s, N, rep, "log10pi0S0 %.1f" % (r["log_pi0_S0"] / math.log(10)), "masked", nm,
                      "mode_missing", len(r["mode_missing"]), "%.0fs" % (time.time() - t0), flush=True)
    sys.exit(0)

if __name__ == "__main__":
    scen = [int(a) for a in sys.argv[1].split(",")]
    R = int(sys.argv[2])
    out = open("../results/study_n200.jsonl", "a")
    for s in scen:
        for p in (500, 1000):
            for cc in (1.0, 0.5):
                for rep in range(R):
                    t0 = time.time()
                    r = run(s, p, cc, rep)
                    out.write(json.dumps(r) + "\n")
                    out.flush()
                    nm = sum(1 for q in r["per_truth"] if q["LO0"] < 0)
                    print(s, p, cc, rep, "log10pi0S0 %.1f" % (r["log_pi0_S0"] / math.log(10)),
                          "pi0R2 %.2f" % math.exp(r["log_pi0_R2"]), "masked", nm, "%.0fs" % (time.time() - t0),
                          flush=True)
