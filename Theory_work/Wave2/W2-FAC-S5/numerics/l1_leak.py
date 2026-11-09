"""L1.4 leakage check (R02 item 1; R06 item 7). For a null j and T ⊇ S0 (R = T minus j):
(1) exact reconstruction t_tilde = (sigma sqrt(n-1)/s)(tau + eps) with the three-term eps;
(2) signal-leakage component L := sqrt(n-1) sigma_j/(sigma sqrt(v_tilde)), computed STABLY via sigma_j = a^-1 beta_tilde' theta^R
    (no subtraction of O(1) terms), reported as n^{3/2} L and as the ratio to its bound sqrt(k)||theta|| sqrt(n-1)/(a d sigma sqrt(v_tilde));
(3) total |eps| divided by the two-term rate (1+|tau|+max|g|) k/n^2 + sqrt(k)/n^{3/2} (should stay bounded)."""
import math, numpy as np
rng = np.random.default_rng(3); rows = []
for n in [10**4, 10**6, 10**8]:
    rec = dict(n=n, max_rel_reconstruction_err=0.0, n32_leak_max=0.0, leak_over_bound_max=0.0, eps_over_rate_max=0.0)
    for it in range(50):
        q, G = 3, 6; rb, rw = .3, .7; b, d = rw - rb, 1 - rw
        grp = np.repeat(np.arange(G), q); p = len(grp)
        S = rb + b * (grp[:, None] == grp[None, :]) + d * np.eye(p)
        th = np.zeros(p); th[[0, 7]] = [1.4, -1.0]
        g = np.linalg.cholesky(S) @ rng.standard_normal(p)
        a = n * n - 1.0; sig = 1.0
        s = math.sqrt(th @ S @ th + 1.0)
        z = ((n - 1) * S @ th + sig * math.sqrt(n - 1) * g) / s
        j = 4; R = np.array([i for i in range(p) if i != j]); k = len(R) + 1
        St = S + np.eye(p) / a
        bt = np.linalg.solve(St[np.ix_(R, R)], S[R, j]); vt = St[j, j] - S[j, R] @ bt
        tt = (z[j] - bt @ z[R]) / math.sqrt(vt)
        be = np.linalg.solve(S[np.ix_(R, R)], S[R, j]); v = S[j, j] - S[j, R] @ be
        tau = (g[j] - be @ g[R]) / math.sqrt(v)
        sj = (bt @ th[R]) / a                          # stable: sigma_j = a^-1 beta_tilde' theta^R
        leak = math.sqrt(n - 1) * sj / (sig * math.sqrt(vt))
        eps = (math.sqrt(v / vt) - 1) * tau + (be - bt) @ g[R] / math.sqrt(vt) + leak
        rec["max_rel_reconstruction_err"] = max(rec["max_rel_reconstruction_err"], abs(tt - sig * math.sqrt(n - 1) / s * (tau + eps)) / abs(tt))
        rec["n32_leak_max"] = max(rec["n32_leak_max"], n ** 1.5 * abs(leak))
        bound = math.sqrt(k) * np.linalg.norm(th) * math.sqrt(n - 1) / (a * d * sig * math.sqrt(vt))
        rec["leak_over_bound_max"] = max(rec["leak_over_bound_max"], abs(leak) / bound)
        rate = (1 + abs(tau) + np.max(np.abs(g))) * k / n ** 2 + math.sqrt(k) / n ** 1.5
        rec["eps_over_rate_max"] = max(rec["eps_over_rate_max"], abs(eps) / rate)
    rows.append(rec); print(rec)
