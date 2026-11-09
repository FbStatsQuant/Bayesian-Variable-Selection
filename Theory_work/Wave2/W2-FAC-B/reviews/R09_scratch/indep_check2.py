import numpy as np, sys
sys.path.insert(0, '.')
from indep_check import run
cfgs = [
  (10**8, 40, 0.5, (3, 17, 30), (1.0, -0.6, 0.8), False, 8),     # FS-b equality at u=1 (l=17, V=S0)
  (10**8, 40, 0.5, (3, 17, 30), (1.0, -0.57, 0.8), False, 8),    # generic
  (10**8, 48, 0.7, (5, 20, 41), (0.5, -0.35, 0.9), False, 8),    # generic
  (10**8, 48, 0.7, (5, 20, 41), (0.5, -0.5, 0.9), False, 8),     # FS-a violated (0.5-0.5=0)
  (10**6, 56, 0.5, (0, 9, 33, 50), (0.8, -1.1, 0.6, 1.3), True, 8),
]
for (n, p, rho, S0, vt, ex, bs) in cfgs:
    for seed in range(3):
        r = run(n, p, rho, S0, np.array(vt), 1.0, 2000+seed, ex, bs); r['seed']=seed; r['vt']=vt
        print(r, flush=True)
