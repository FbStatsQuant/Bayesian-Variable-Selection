"""W7-SEP: stress test of Proposition GU (greedy universality) on random exact-Gram designs with an isolated
relevant set R (Sigma_{R,R^c} = 0), including combination look-alikes that violate PGD ([T37R] C3).

Design per replicate: r = |R| = 10 relevant variables, s0 in {2,..,5} truths among them; Sigma_R built from
  * truths with random correlations (random Gaussian factor model), and
  * look-alikes l = normalised (sum of 2-3 truths with random signs) + small idiosyncratic part (sd tau), which makes
    the first greedy move a non-progress move (PGD fails) when tau is small;
p - r = 4 independent nulls (p = 14). Coefficients fixed in [0.5, 1.5] with random signs.
Exact Gram (X'X = (n-1) Sigma), production local search from EVERY centre (2^14), exact scores.
Records: phi0^2 = lambda_min(Sigma_R), whether PGD fails at the empty set, fraction of centres C ⊆ R from which
S0 is scored, fraction certified at S0, and fraction of all centres. Seed fixed. Output: ../results/gu_stress.txt
"""
import math, json, numpy as np
from sep_core import scores, successor, near_mask, ls_scores_S0, mask_of, popcount_array

rng = np.random.default_rng(20261103)
p, r = 14, 10
lines = []

def make_design():
    s0 = int(rng.integers(2, 6))
    nl = r - s0
    # truths: factor model correlations
    Ft = rng.standard_normal((s0, 2)) * 0.6
    Ct = Ft @ Ft.T + np.eye(s0)
    dt = np.sqrt(np.diag(Ct)); Ct = Ct / np.outer(dt, dt)
    Lt = np.linalg.cholesky(Ct)
    # look-alikes as combinations of truths in a latent representation
    tau = float(rng.choice([0.15, 0.3, 0.6]))
    V = np.zeros((r, s0 + nl))
    V[:s0, :s0] = Lt
    for i in range(nl):
        k = int(rng.integers(1, 4)); idx = rng.choice(s0, size=min(k, s0), replace=False)
        v = (rng.choice([-1, 1], size=len(idx))[:, None] * Lt[idx]).sum(0)
        V[s0 + i, :s0] = v
        V[s0 + i, s0 + i] = tau * np.linalg.norm(v)
    SR = V @ V.T
    d = np.sqrt(np.diag(SR)); SR = SR / np.outer(d, d)
    Sig = np.eye(p); Sig[:r, :r] = SR
    theta = np.zeros(p)
    theta[:s0] = rng.uniform(0.5, 1.5, s0) * rng.choice([-1, 1], s0)
    return Sig, theta, s0, tau

def pgd_fails_at_empty(Sig, theta, s0):
    mu_cov = Sig @ theta  # population <x_j, mu>
    red = mu_cov ** 2      # reduction from adding j to the empty set (unit variances)
    return int(np.argmax(red[:r])) >= s0, float(red[:s0].max()), float(red[s0:r].max())

def build_generic(Sig, theta, n):
    L = np.linalg.cholesky(Sig)
    xi = rng.standard_normal(p)
    Xte = math.sqrt(n - 1) * L @ xi
    GX = (n - 1) * Sig
    Xty = GX @ theta + Xte
    yy = theta @ GX @ theta + 2 * theta @ Xte + xi @ xi + rng.chisquare(n - 1 - p)
    s = math.sqrt(yy / (n - 1))
    S0 = tuple(int(j) for j in np.flatnonzero(theta))
    return dict(p=p, n=n, GX=GX, z=Xty / s, yy=yy / s ** 2, S0=S0, blocks=[[j] for j in range(p)])

summary = {}
for rep in range(40):
    Sig, theta, s0, tau = make_design()
    phi2 = float(np.linalg.eigvalsh(Sig[:r, :r]).min())
    pgdfail, rt, rl = pgd_fails_at_empty(Sig, theta, s0)
    for n in (200, 1000, 5000, 50000, 500000):
        d = build_generic(Sig, theta, n)
        sc = scores(d); F, pc, K = sc["F"], sc["pc"], sc["K"]
        S0m = mask_of(d["S0"])
        ell = math.ceil(math.log2(n + p + 1))
        succ = successor(F, p, K, pc)
        near = near_mask(p, K, pc, S0m)
        hit, end, moves = ls_scores_S0(succ, near, ell)
        allm = np.arange(1 << p); inR = (allm >> r) == 0; feas = pc <= K
        cert = (end == S0m) & (succ[end] == end)
        rec = dict(rep=rep, n=n, s0=s0, tau=tau, phi0sq=round(phi2, 4), pgd_fails=pgdfail,
                   fracR_scored=float(hit[inR & feas].mean()), fracR_cert=float(cert[inR & feas].mean()),
                   frac_all_scored=float(hit[feas].mean()), maxmovesR=int(moves[inR & feas].max()),
                   piS0=float(math.exp(sc["log_pi"][S0m])))
        lines.append(json.dumps(rec)); print(lines[-1], flush=True)
        summary.setdefault(n, []).append(rec)

out = ["W7-SEP gu_stress.py, seed 20261103, p = 14, |R| = 10, 4 isolated nulls, 40 random designs", ""]
out.append("n | designs | PGD fails at ∅ | all C⊆R scored S0 (designs) | mean frac C⊆R scored | min frac | all C⊆R certified | mean frac all centres scored | median pi(S0)")
for n, recs in summary.items():
    out.append(f"{n} | {len(recs)} | {sum(x['pgd_fails'] for x in recs)} | {sum(x['fracR_scored'] == 1.0 for x in recs)} | "
               f"{np.mean([x['fracR_scored'] for x in recs]):.4f} | {min(x['fracR_scored'] for x in recs):.4f} | "
               f"{sum(x['fracR_cert'] == 1.0 for x in recs)} | {np.mean([x['frac_all_scored'] for x in recs]):.4f} | "
               f"{np.median([x['piS0'] for x in recs]):.3f}")
out.append(""); out.append("min phi0^2 over designs: %.4f" % min(x['phi0sq'] for x in summary[200]))
out += ["", "raw records:"] + lines
open("../results/gu_stress.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out[:12]))
