# R01 statement-lock check: absolute vs relative (whitened) deviation of the
# standardized sample correlation R_hat from Sigma = (1-rho)I + rho 11' (iid Gaussian rows),
# and for one-factor unequal loadings Sigma = diag(1-lam^2) + lam lam'.
import numpy as np, sys
rng = np.random.default_rng(20261109)
def stats(n, p, Sig, reps=3):
    L = np.linalg.cholesky(Sig)
    w, V = np.linalg.eigh(Sig); Sm12 = V @ np.diag(w**-0.5) @ V.T
    out = []
    for _ in range(reps):
        Xr = rng.standard_normal((n, p)) @ L.T
        X = Xr - Xr.mean(0); X /= X.std(0, ddof=1)
        R = X.T @ X / (n - 1)
        D = R - Sig
        a = np.linalg.norm(D, 2)
        r = np.linalg.norm(Sm12 @ D @ Sm12, 2)
        row = np.sqrt((D**2).sum(1)).max()
        mx = np.abs(D).max()
        one = np.ones(p) / np.sqrt(p)
        q1 = one @ D @ one  # spike-direction quadratic form
        out.append((a, r, row, mx, q1))
    return np.array(out).mean(0)
print("design n p | abs_op  p/sqrt(n)  sqrt(p/n) | whitened_op | max_row_l2 | max_entry sqrt(log p/n) | 1'D1/p")
for n, p in [(4000, 50), (4000, 200), (16000, 200), (16000, 400), (64000, 400)]:
    for name in ["CS0.5", "1F"]:
        if name == "CS0.5":
            Sig = 0.5*np.eye(p) + 0.5*np.ones((p, p))
        else:
            lam = np.linspace(0.3, 0.9, p)
            Sig = np.outer(lam, lam); np.fill_diagonal(Sig, 1.0)
        a, r, row, mx, q1 = stats(n, p, Sig)
        print(f"{name:5s} {n:6d} {p:4d} | {a:6.3f} {p/np.sqrt(n):6.3f} {np.sqrt(p/n):6.3f} | {r:6.3f} | {row:6.3f} | {mx:6.4f} {np.sqrt(np.log(p)/n):6.4f} | {q1:+7.3f}")
