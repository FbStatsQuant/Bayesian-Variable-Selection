#!/usr/bin/env python3
"""Stress test of the engine's heuristic error_bound() (v3_score.h:242) at large n, W7-SEC. Seed fixed.

Hypothesis tested: the heuristic eta_eng = 64 eps [nu (y'y/Q)(1 + k cond_H) + ...] has no factor growing with n in its
Q term, while the rounding error of the dot products z_j = x_j' y and y'y grows like u sqrt(n) (random) to u n
(worst case) relative to y'y. When y'y/Q is large (y highly correlated with the model), nu (y'y/Q) * that error can
exceed eta_eng. Uses the same harness and exact reference as t33_fp_check.py.
Usage: t33_engine_bound_stress.py HARNESS_BINARY
"""
import math, os, struct, subprocess, sys, tempfile
import numpy as np
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33_fp_check import standardise, Exact, bound

SEED = 20261104

def run(n, p, noise, models, harness, rng, label):
    X = rng.standard_normal((n, p))
    y = X[:, 0] + noise * rng.standard_normal(n)
    Xs = np.column_stack([standardise(X[:, j]) for j in range(p)]); ys = standardise(y)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as fh:
        fh.write(struct.pack("<ii", n, p)); fh.write(Xs.astype("<f8").tobytes(order="F")); fh.write(ys.astype("<f8").tobytes())
        fh.write(struct.pack("<i", len(models)))
        for S in models:
            fh.write(struct.pack("<i", len(S))); fh.write(struct.pack(f"<{len(S)}i", *S))
        path = fh.name
    res = subprocess.run([harness, path], capture_output=True, text=True, check=True).stdout.splitlines()
    os.unlink(path)
    hdr = dict(kv.split("=") for kv in res[0].split()[1:])
    ex = Exact(Xs, ys)
    logCn_err = float(abs(mp.mpf(float(hdr["logCn"])) - ex.logCn))
    out = []
    for line in res[2:]:
        t = line.split(); m, k = int(t[1]), int(t[2])
        logm_hat, F_hat, Q_hat = map(float, t[3:6]); eb = float(t[11])
        r = ex.score(models[m])
        err = float(abs(mp.mpf(logm_hat) - r["logm"]))
        eta, _ = bound(ex, models[m], r, logCn_err)
        out.append((label, n, k, float(ex.yty / r["Q"]), err, eb, err / eb, eta))
    return out

if __name__ == "__main__":
    harness = sys.argv[1]
    rng = np.random.default_rng(SEED)
    print(f"Engine heuristic error_bound stress test; seed {SEED}")
    print(f"{'case':>10} {'n':>9} {'k':>2} {'yty/Q':>10} {'|dlogm|':>10} {'engine eta':>10} {'ratio':>8} {'rigorous eta':>12}")
    rows = []
    for n in [10**4, 10**5, 10**6, 4 * 10**6]:
        for noise in [0.1, 0.01]:
            for rep in range(2):
                rows += run(n, 2, noise, [[0], [0, 1]], harness, rng, f"noise={noise}")
    for r in rows:
        print(f"{r[0]:>10} {r[1]:9d} {r[2]:2d} {r[3]:10.3e} {r[4]:10.3e} {r[5]:10.3e} {r[6]:8.3f} {r[7]:12.3e}")
    worst = max(rows, key=lambda r: r[6])
    print(f"\nmax |dlogm| / engine eta = {worst[6]:.3f} at n = {worst[1]}, k = {worst[2]}, yty/Q = {worst[3]:.3e}")
    print("all rigorous bounds hold:", all(r[4] <= r[7] for r in rows))
