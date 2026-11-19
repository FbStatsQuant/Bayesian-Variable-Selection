#!/usr/bin/env python3
"""w1_projection.py -- re-projection of the 10^4 overlap rung after W1 (Monte Carlo; numpy). Same structure as REPROJECTION_W0.md
section 3: per-design Beta posterior for P(escalate), tier-1 rebuild count, per-fit cost model, wave and cumulative totals.
Inputs measured in W1 (W1_escalation.csv / this file's cost constants). Reproducible: python3 w1_projection.py (seed fixed)."""
import numpy as np, sys
rng = np.random.default_rng(20261119)
NS = 200_000
SPENT = 254.74 + 277.90          # W0 incl. 91.5 evidence + W1 (sacct)
SPENT_COUNTED = 163.24 + 277.90  # W0 counted only
# remaining fits (W2 plan, W3 per make_waves.py): design -> (n T fits in W2, n T fits in W3)
REM = {"AR": (1, 6), "ARweak": (2, 0), "ADJ": (3, 0)}
# prior P(esc) means from REPROJECTION_W0 section 1 (AR .85, ARweak .5, ADJ .3) with equivalent sample size 4, then the observed outcomes:
PRIOR = {"AR": 0.85, "ARweak": 0.5, "ADJ": 0.30}
ESS = 4.0
OBS = {"AR": (1, 1), "ARweak": (1, 2), "ADJ": (0, 1)}      # (escalated, fits) over W0 + W1 T fits of that design
# tier-1 convergence per rebuild r ~ Beta; prior Beta(3,2) + 3 converged fits (k1 = 1, 1, 3 => 3 successes, 2 failed rebuilds)
R_A, R_B = 3 + 3, 2 + 2
# cost model (core-h)
ESC_BASE = {"AR": 98.5, "ARweak": 54.1, "ADJ": 93.9}        # everything except tier-1 rebuilds, escalated fit
ESC_REB = {"AR": 11.6, "ARweak": 6.6, "ADJ": 10.8}          # one tier-1 rebuild
CAL_FIX = {"AR": 47.0 + 2.0, "ARweak": 27.4 + 1.2, "ADJ": 42.5 + 2.0}   # calibrate part that is not tier-1 rebuilds (for the 144 TIMEOUT line)
NOESC = {"AR": (50.0, 8.0), "ARweak": None, "ADJ": (48.3, 4.0)}
V_COST = {"AR": 2.46, "ARweak": 1.70, "ADJ": 2.38}


def fit_costs(design, n, p_esc, r, tail_scale=1.0):
    """n fits of one design: cost array (NS, n); also whether TIMEOUT (calibrate > 144 core-h)"""
    esc = rng.random((NS, n)) < p_esc[:, None]
    k1 = np.minimum(rng.geometric(r[:, None] * np.ones((1, n))), 14)
    c_esc = ESC_BASE[design] + ESC_REB[design] * k1 + rng.normal(0, 3.0, (NS, n))
    if NOESC[design] is None:      # ARweak tier 0: fast (k0 = 1) 9.3 or slow 28
        fast = rng.random((NS, n)) < 0.5
        c_no = np.where(fast, 9.3 + rng.normal(0, 0.5, (NS, n)), 28.0 + rng.normal(0, 4.0, (NS, n)))
    else:
        c_no = NOESC[design][0] + rng.normal(0, NOESC[design][1], (NS, n))
    cost = np.where(esc, c_esc, c_no)
    timeout = esc & ((CAL_FIX[design] + ESC_REB[design] * k1) > 144.0)
    return cost, esc, timeout


def run(mult=1.0, tailr=None, label=""):
    p = {}
    for d in PRIOR:
        m = min(0.99, PRIOR[d] * mult)
        a, b = m * ESS + OBS[d][0], (1 - m) * ESS + OBS[d][1] - OBS[d][0]
        p[d] = rng.beta(a, b, NS)
    ra, rb = (R_A, R_B) if tailr is None else tailr
    r = rng.beta(ra, rb, NS)
    W = {"W2": np.zeros(NS), "W3": np.zeros(NS)}
    anyfit172 = np.zeros(NS, bool); anyto = np.zeros(NS, bool); nesc = np.zeros(NS)
    for d, (n2, n3) in REM.items():
        for w, n in (("W2", n2), ("W3", n3)):
            if n == 0:
                continue
            c, e, to = fit_costs(d, n, p[d], r)
            W[w] += c.sum(1) + n * V_COST[d] + rng.normal(0, 0.3, NS) * np.sqrt(n)
            anyfit172 |= (c > 172).any(1); anyto |= to.any(1); nesc += e.sum(1)
    out = {}
    for basis, sp in (("W0+evidence", SPENT), ("counted only", SPENT_COUNTED)):
        tot = sp + W["W2"] + W["W3"]
        out[basis] = tot
    return W, out, anyfit172, anyto, nesc


def q(x, ps=(10, 50, 90)):
    return [float(np.percentile(x, v)) for v in ps]


if __name__ == "__main__":
    for label, kw in (("BASE", {}), ("all P(esc) x0.7", {"mult": 0.7}), ("all P(esc) x1.15", {"mult": 1.15}),
                      ("tier-1 convergence worse: r~Beta(3,4)", {"tailr": (3, 4)}), ("tier-1 convergence r~Beta(2,5) (mean 0.29)", {"tailr": (2, 5)})):
        W, out, a172, ato, nesc = run(**kw)
        print("=== %s" % label)
        for w in ("W2", "W3"):
            print("  %s expected %.0f  P10/50/90 %s" % (w, W[w].mean(), [round(v) for v in q(W[w])]))
        t = out["W0+evidence"]
        print("  rung total (W0+evidence 254.74 + W1 277.90 = %.2f spent): E %.0f  P10/50/90 %s ; P>1.6k %.2f  P>2.0k %.3f  P>2.1k %.3f  P>2.5k %.4f"
              % (SPENT, t.mean(), [round(v) for v in q(t)], (t > 1600).mean(), (t > 2000).mean(), (t > 2100).mean(), (t > 2500).mean()))
        t2 = out["counted only"]
        print("  counted only (W0 163.24): E %.0f  P10/50/90 %s ; P>1.6k %.2f" % (t2.mean(), [round(v) for v in q(t2)], (t2 > 1600).mean()))
        print("  after W2 (cum): E %.0f P90 %.0f ; P(any fit > 172) %.3f ; P(any calibrate TIMEOUT) %.4f ; escalations in the remaining 12 T fits: E %.1f P10-P90 %s"
              % ((SPENT + W["W2"]).mean(), np.percentile(SPENT + W["W2"], 90), a172.mean(), ato.mean(), nesc.mean(), q(nesc, (10, 90))))
        print("  wave stop (2 x quote; W2 quote 480 -> 960, W3 640 -> 1280): P(W2>960) %.4f, P(W3>1280) %.4f; W3 > 733 (W0 P90) %.2f"
              % ((W["W2"] > 960).mean(), (W["W3"] > 1280).mean(), (W["W3"] > 733).mean()))
