"""bcs_selftest.py -- closed-form block-CS scanner (bcs_core) vs FAC-B's general exact-Gram scanner (fac_core.scan):
all deletion / addition / swap gains on random sets, S5 and other (a,b,c,q), n in {1e4, 1e6, 1e8}; plus path agreement."""
import sys, os, math, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "W2-FAC-B", "numerics"))
import bcs_core as bcs
import fac_core as fc
import bvs_core as bc

rng = np.random.default_rng(20261109)
worst = 0.0
rows = []
for (a, b, c, q) in [(0.3, 0.4, 0.3, 5), (0.5, 0.0, 0.5, 1), (0.0, 0.6, 0.4, 5), (0.2, 0.5, 0.3, 3), (0.3, 0.4, 0.3, 7)]:
    for n in [10 ** 4, 10 ** 6, 10 ** 8]:
        p = 40 if q != 7 else 42
        th = np.zeros(p); th[[2, 11, 23]] = [1.4, -1.0, 1.8]
        P = bcs.BCS(p, q, a, b, c, th, n, rng)
        # general scorer object sharing the same sufficient statistics
        grp = P.grp
        H = (grp[:, None] == grp[None, :]).astype(float)
        Sigma = a * np.ones((p, p)) + b * H + c * np.eye(p)
        G = types.SimpleNamespace(n=n, p=p, K=P.K, XtX=(n - 1.0) * Sigma, Xty=P.z, yty=P.yty, nu=P.nu,
                                  logw=P.logw, logm0=-P.nu * math.log(0.02 + P.yty))
        for trial in range(6):
            k = int(rng.integers(1, p))
            T = tuple(sorted(rng.choice(p, size=k, replace=False).tolist()))
            s1 = P.scan(T)
            s2 = fc.scan(G, T)
            FT = s2["FT"]
            e_del = np.max(np.abs(s1["del"] - (s2["del"] - FT))) if k >= 1 else 0.0
            e_add = np.max(np.abs(s1["add"] - (s2["add"] - FT))) if len(s1["O"]) and k < P.K else 0.0
            e_sw = np.max(np.abs(s1["swap"] - (s2["swap"] - FT))) if s1["swap"].size else 0.0
            # also absolute F
            e_F = abs(P.F(T) - FT)
            scale = max(1.0, np.max(np.abs(s2["del"] - FT)) if k >= 1 else 1.0)
            worst = max(worst, e_del, e_add, e_sw)
            rows.append((a, b, c, q, n, k, e_del, e_add, e_sw, e_F, abs(FT)))
        # path agreement from [p]
        r1 = bcs.ls0_path(P, range(p))
        r2 = fc.ls0_path(G, tuple(range(p)), P.S0)
        rows.append(("path", a, b, c, q, n, r1["final"] == tuple(r2["final"]), r1["moves"], r2["moves"]))
print("gain comparisons (abs error of gains, closed form vs general scorer):")
mx = {}
for r in rows:
    if r[0] != "path":
        a, b, c, q, n, k, ed, ea, es, eF, aF = r
        key = (a, b, c, q, n)
        m = mx.get(key, [0, 0, 0, 0, 0])
        mx[key] = [max(m[0], ed), max(m[1], ea), max(m[2], es), max(m[3], eF), aF]
for key, m in mx.items():
    print(f"  (a,b,c,q)={key[:4]} n={key[4]:.0e}: max|err| del={m[0]:.2e} add={m[1]:.2e} swap={m[2]:.2e} |F|err={m[3]:.2e} (|F|~{m[4]:.2e})")
print("paths from [p] (same final set?, moves closed-form, moves general):")
for r in rows:
    if r[0] == "path":
        print(f"  (a,b,c,q)={r[1:5]} n={r[5]:.0e}: same_final={r[6]} moves={r[7]} vs {r[8]}")
print(f"WORST gain error: {worst:.3e}")
