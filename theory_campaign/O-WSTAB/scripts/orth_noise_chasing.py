"""N3: the noise-chasing obstruction (WS6) in the orthogonal design ORTH (zero cross-block correlation).

Part A (exact, p = 16): R = I (exact Gram), s0 = 3 truths theta = c(1, -1, 1) in distinct blocks, population
R^2 = 3c^2/(3c^2+1) in {0.25, 0.5, 0.75, 0.9}.  For each data set: exact chi2(pi||pi0), q_2(S0), pi0(S0), pi(S0), TV,
KL, and the null-singleton terms c_l = q_2(S0+l)/q_2(S0) against the prediction
    c_l ~ (s0+1)/(2p-s0-1) * n^{-1/2} * exp{(1+omega_l) Z_l^2 / 2},   omega_l = 1 - RSS(S0)/RSS(S0 cap C_b(l)),
with Z_l = x_l'eps/(sigma sqrt(n-1)).  Fitted exponent: regression of log c_l - log[(s0+1)/((2p-s0-1)sqrt n)] on Z_l^2/2.

Part B (closed form, large p, no enumeration): ORTH with p = n - 1, nulls in truth-free blocks.  The exact
null-singleton sum LB = sum_l c_l  (a lower bound for 1/q_2(S0) - 1, hence 1 + chi2 >= pi(S0)^2 (1 + LB), WS6)
is an O(p) closed form:  c_l = [w(s0+1)/w(s0)] n^{-1/2} (1 - t_l/Q0)^nu (1 - t_l/(Q0 - t_S0))^{-2 nu}.
Prediction: LB ~ n^{-1/2} p^{omega} (log p)^{-(1+omega)/2} -> infinity iff omega > 1/2 (p = n-1).

Usage: python orth_noise_chasing.py <outA.json> <outB.json>.   Seeds: 20261102 + 100*k + i.
"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from metrics import row_metrics
from wstab_core import A0, B0, Problem, Space, log_w, make_blocks, suff_exact_gram

R2S = [0.25, 0.5, 0.75, 0.9]


def part_a(out, reps=30):
    p, s0 = 16, 3
    Sig = np.eye(p)
    blocks = make_blocks(Sig, 4)
    S0 = [blocks[0][0], blocks[1][0], blocks[2][0]]
    space = Space(p, p)
    res = dict(p=p, blocks=blocks, S0=S0, rows=[])
    t0 = time.time()
    for k, R2 in enumerate(R2S):
        c = math.sqrt(R2 / (3 * (1 - R2)))
        theta = np.zeros(p)
        theta[S0] = c * np.array([1.0, -1.0, 1.0])
        for i, n in enumerate([200, 800, 3200, 12800, 51200]):
            rng = np.random.default_rng(20261102 + 100 * k + i)
            rows = []
            for rep in range(reps):
                R, r, ex = suff_exact_gram(Sig, theta, n, 1.0, rng)
                P = Problem(R, r, n, blocks=blocks, space=space)
                m = row_metrics(P, S0, theta=theta, grid=False, eps_models=False)
                # null-singleton terms
                lq2 = P.logq(2.0)
                i0 = P.space.idx(S0)
                Z = ex["Xteps"] / math.sqrt(n - 1)
                Q0 = 2 * B0 + n - 1
                tS0 = P.t[i0]
                blk = {j: b for b, C in enumerate(blocks) for j in C}
                terms = []
                for l in range(p):
                    if l in S0:
                        continue
                    U = [j for j in S0 if blk[j] == blk[l]]
                    tU = P.t[P.space.idx(U)]
                    omega = 1 - (Q0 - tS0) / (Q0 - tU)
                    logc = lq2[P.space.idx(sorted(S0 + [l]))] - lq2[i0]
                    pred = math.log((s0 + 1) / (2 * p - s0 - 1)) - 0.5 * math.log(n) + (1 + omega) * Z[l] ** 2 / 2
                    terms.append((l, float(Z[l]), float(omega), float(logc), float(pred)))
                sing = sum(math.exp(t[3]) for t in terms)
                m.update(R2=R2, n=n, rep=rep, null_terms=terms, single_sum=sing,
                         inv_q2_minus_1=1 / m["q2_S0"] - 1)
                rows.append(m)
            res["rows"].extend(rows)
            # exponent fit over all (rep, l)
            xs = np.array([t[1] ** 2 / 2 for x in rows for t in x["null_terms"]])
            ys = np.array([t[3] - (math.log((s0 + 1) / (2 * p - s0 - 1)) - 0.5 * math.log(n)) for x in rows
                           for t in x["null_terms"]])
            om = np.array([t[2] for x in rows for t in x["null_terms"]])
            slope = float(np.polyfit(xs, ys, 1)[0])
            err = float(np.max(np.abs(np.array([t[3] - t[4] for x in rows for t in x["null_terms"]]))))
            med = lambda key: float(np.median([x[key] for x in rows]))
            print(f"R2={R2:.2f} n={n:6d} | chi2={med('chi2'):.3g} 1/q2-1={med('inv_q2_minus_1'):.3g} "
                  f"single/total={np.median([x['single_sum']/x['inv_q2_minus_1'] for x in rows]):.3f} "
                  f"pi0={med('pi0_S0'):.4f} pi={med('pi_S0'):.4f} TV={med('tv'):.3g} KL={med('kl_pi_pi0'):.3g} "
                  f"slope={slope:.3f} (1+mean omega={1+om.mean():.3f}) max|logc-pred|={err:.3f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
            with open(out, "w") as f:
                json.dump(res, f)


def part_b(out, reps=200):
    s0 = 3
    res = dict(rows=[])
    for k, R2 in enumerate([0.3, 0.45, 0.55, 0.7, 0.9]):
        c = math.sqrt(R2 / (3 * (1 - R2)))
        for i, n in enumerate([10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]):
            p = n - 1
            rng = np.random.default_rng(20261102 + 7000 + 100 * k + i)
            nu = A0 + n / 2
            Q0 = 2 * B0 + n - 1
            lwr = log_w(s0 + 1, p) - log_w(s0, p)
            lbs = []
            for rep in range(reps):
                xi = rng.standard_normal(p)       # x_j'eps / sqrt(n-1), sigma = 1 (ORTH: iid)
                th = np.zeros(p)
                th[:s0] = c * np.array([1.0, -1.0, 1.0])
                chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
                YtY = (n - 1) * th @ th + 2 * math.sqrt(n - 1) * th @ xi + xi @ xi + chi
                sy = math.sqrt(YtY / (n - 1))
                z = ((n - 1) * th + math.sqrt(n - 1) * xi) / sy       # x_j'y on the standardised response
                t = z ** 2 / n                                         # ORTH: t_j = n z^2/((n+1)(n-1)+1) = z^2/n
                tS0 = t[:s0].sum()
                tn = t[s0:]
                logc = lwr - 0.5 * math.log(n) + nu * np.log1p(-tn / Q0) - 2 * nu * np.log1p(-tn / (Q0 - tS0))
                m = logc.max()
                lbs.append(float(m + math.log(np.exp(logc - m).sum())))
            lbs = np.array(lbs)
            pred = -0.5 * math.log(n) + R2 * math.log(p) - (1 + R2) / 2 * math.log(math.log(p))
            row = dict(R2=R2, n=n, p=p, logLB_q=np.quantile(lbs, [0.1, 0.5, 0.9]).tolist(), log_pred_scale=pred)
            res["rows"].append(row)
            print(f"R2={R2:.2f} n=p+1={n:8d} | log LB q10/med/q90 = "
                  f"{row['logLB_q'][0]:7.2f} {row['logLB_q'][1]:7.2f} {row['logLB_q'][2]:7.2f} | "
                  f"log[n^-1/2 p^R2 (log p)^-(1+R2)/2] = {pred:7.2f}", flush=True)
    with open(out, "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    part_b(sys.argv[2])
    part_a(sys.argv[1])
