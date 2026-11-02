"""O-DILUTE design-level prediction of log pi0(S0) and pi0(R_d) from population quantities only (no data).

Model ("dilution formula", REPORT §3):
  truth j:  r_jy has population correlation rho_j (rho_j^2 = (1-kappa_j) x_j, the diluted share);
            atanh(r_jy) ~ N(atanh rho_j, 1/(n-3)) (Fisher), independent across truths (population BO);
            lambda_j = log BF({j})(r_jy) + log t,  t = (s0+1)/(2p-s0-1).
  nulls:    r_ly^2 ~ Beta(1/2, (n-2)/2) exactly (x_l independent of y), p - s0 of them;
            competition C_null = sum_l log(1 + t BF({l})).
  size:     N = sum_j Bern(sigma(lambda_j)) + sum_l Bern(t BF_l/(1+t BF_l));
            log A_t = -log E[e^{g(N)} 1{N<=K}],  g(k) = log w(k) - log w(s0) - (k-s0) log t.
  prediction: log pi0(S0) = -sum_j softplus(-lambda_j) - C_null + log A_t   (Corollary E1 with product blocks).
  pi0(R_d): P(#null inclusions <= d) under the same product law (Poisson-binomial), tilted to the size law.
Seed 20261102. Usage: python predict.py > ../results/predict.txt
"""
import numpy as np
from scipy.special import logsumexp
import dilute as D

n = 200; s0 = 14; K = 100; NU = D.A0 + n / 2
H = (n + 1) * (n - 1) + 1

def log_bf1(r2):
    Q = (n - 1) * (1 - n * (n - 1) * r2 / H)
    return -0.5 * np.log(H / n) - NU * (np.log(0.02 + Q) - np.log(0.02 + n - 1))

def pois_binom(probs):
    dist = np.zeros(len(probs) + 1); dist[0] = 1.0
    for q in probs:
        dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q; dist[0] *= (1 - q)
    return dist

def main():
    rng = np.random.default_rng(20261102)
    print("design-level dilution-formula predictions (MC = 400 draws; medians)")
    print("%5s %2s %4s | %8s %8s %8s %8s | %8s %8s | %s" % ("p", "S", "c", "lg10pi0", "-V", "-Cnull", "logA",
                                                         "pi0R2", "Enull", "visible truths (det.)"))
    for p in (500, 1000):
        act, beta = D.truth(p)
        t = (s0 + 1) / (2 * p - s0 - 1); lt = np.log(t)
        kk = np.arange(K + 1); g = D.log_w(kk, p) - D.log_w(s0, p) - (kk - s0) * lt
        for s in range(1, 7):
            Sig = D.scenario_covariance(s, p)
            b = np.zeros(p); b[act] = beta
            bS = Sig @ b
            for c in (1.0, 0.5):
                vary = c * c * b @ bS + 1.0
                rho = c * bS[act] / np.sqrt(vary)
                lam_det = log_bf1(rho ** 2) + lt
                res = []
                for m in range(400):
                    r = np.tanh(np.arctanh(rho) + rng.standard_normal(s0) / np.sqrt(n - 3))
                    lam = log_bf1(r ** 2) + lt
                    V = np.logaddexp(0, -lam).sum()
                    x0 = rng.beta(0.5, (n - 2) / 2, size=p - s0)
                    tb = np.exp(log_bf1(x0) + lt)
                    Cn = np.log1p(tb).sum()
                    qn = tb / (1 + tb); qt = 1 / (1 + np.exp(-lam))
                    dn = pois_binom(qn)[: K + 1]; dt = pois_binom(qt)
                    dN = np.convolve(dt, dn)[: K + 1]
                    logA = -logsumexp(g + np.log(np.maximum(dN, 1e-300)))
                    # pi0(#nulls <= 2) under the size-tilted product law
                    joint = np.outer(dt, dn)                      # (truths i, nulls j)
                    ii, jj = np.meshgrid(np.arange(len(dt)), np.arange(len(dn)), indexing="ij")
                    kij = ii + jj; ok = kij <= K
                    wgt = np.where(ok, np.exp(g[np.minimum(kij, K)]), 0.0) * joint
                    wgt /= wgt.sum()
                    R2 = wgt[:, :3].sum(); En = (wgt.sum(0) * np.arange(len(dn))).sum()
                    res.append((-V - Cn + logA, -V, -Cn, logA, R2, En))
                res = np.array(res); med = np.median(res, 0)
                vis = int((lam_det > 0).sum())
                print("%5d %2d %4.1f | %8.2f %8.2f %8.2f %8.2f | %8.3f %8.2f | %d/14" % (
                    p, s, c, med[0] / np.log(10), med[1], med[2], med[3], med[4], med[5], vis))
    # scale-free ceiling: c -> infinity
    print("\nc -> infinity (shares omega_j = theta_j^2 Var-adj / theta' Sigma theta), S1:")
    for p in (500, 1000):
        act, beta = D.truth(p); t = (s0 + 1) / (2 * p - s0 - 1)
        om = beta ** 2 / (beta @ beta)
        lam = log_bf1(om) + np.log(t)
        print(" p=%d  lambda_inf = %s ; sum softplus(-lambda_inf) = %.2f nats (log10 %.2f); visible %d/14" % (
            p, np.round(lam, 2), np.logaddexp(0, -lam).sum(), -np.logaddexp(0, -lam).sum() / np.log(10),
            (lam > 0).sum()))
    # n needed for every share to clear the threshold, S1, c = 1
    print("\nthreshold n (deterministic, S1): smallest n with min_j lambda_j(rho_j) > 0")
    for p in (500, 1000):
        for c in (1.0, 0.5):
            act, beta = D.truth(p)
            for nn in range(200, 4000, 10):
                Hn = (nn + 1) * (nn - 1) + 1; nu = 0.01 + nn / 2
                rho2 = c * c * beta ** 2 / (c * c * beta @ beta + 1)
                Q = (nn - 1) * (1 - nn * (nn - 1) * rho2 / Hn)
                lam = -0.5 * np.log(Hn / nn) - nu * (np.log(0.02 + Q) - np.log(0.02 + nn - 1)) + np.log((s0 + 1) / (2 * p - s0 - 1))
                if lam.min() > 0:
                    print("  p=%d c=%.1f: n* = %d" % (p, c, nn)); break

if __name__ == "__main__":
    main()
