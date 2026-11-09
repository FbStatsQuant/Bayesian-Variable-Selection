"""E-S5CC cost probe: per-step wall time of the s3_cc.py loop body (gains(swaps=False) + noise_tau + one deletion)
for the first K steps at size p (bcs_core from the ticket snapshot). Not a result; used only to plan the grid.
usage: python time_steps.py p n K"""
import os, sys, math, json, time, resource
sys.path.insert(0, (os.environ["TICKETS"] + "/Theory_work/Wave2/W2-FAC-S5/numerics") if os.environ.get("TICKETS") else os.environ["BCS_CORE_DIR"])
import numpy as np
import bcs_core as B
p, n, K = int(sys.argv[1]), int(float(sys.argv[2])), int(sys.argv[3])
rng = np.random.default_rng(10007 * 1 + p)
t0 = time.time()
P = B.BCS(n, np.arange(p) // 5, .3, .7, B.layout(p, 5, s0=4), rng)
isnull = np.ones(p, bool); isnull[P.S0] = False
path = B.Path(P, np.ones(p, bool)); t1 = time.time()
for s in range(K):
    G = path.gains(swaps=False); nt = path.noise_tau()
    Tidx = G["Tidx"]; retN = Tidx[isnull[Tidx]]
    _ = float(np.max(np.abs(nt["eR"][retN])))
    j = int(Tidx[int(np.argmax(G["gdel"]))]); path.apply("del", j=j)
t2 = time.time()
per = (t2 - t1) / K
print(json.dumps(dict(p=p, n=n, K=K, setup_s=round(t1 - t0, 3), s_per_step=per,
                      est_path_s_upper=per * p, maxrss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)))
