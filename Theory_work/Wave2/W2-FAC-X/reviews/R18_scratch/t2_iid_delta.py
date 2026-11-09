"""R18 t2: X9.1/X9.2 -- iid rows, general loadings. Exact sqrt(N) omega_j(T) from the rotation representation (Bartlett
factor of iid_core), reference s_j(T), and delta = sqrt(N) omega - s, maximised over random and adversarial T.
Also checks RSS_T = ||e||^2/(1+q_T) against direct projection."""
import sys, math, numpy as np
sys.path.insert(0, '../../numerics')
import iid_core as ic

rng = np.random.default_rng(1818)
print(" n        p   max|delta|   (p/sqrt n + sqrt(p log n/n) + sqrt(log n/n)) Hbar   ratio   maxRSSrelerr")
for n, p in [(10**4, 20), (10**4, 80), (10**5, 80), (10**5, 300), (10**6, 300), (10**6, 1000)]:
    worst = 0; rss_err = 0
    for rep in range(3):
        lam = rng.uniform(0.2, 0.9, p)
        beta = np.zeros(p); S0 = [0, 1]; beta[S0] = [1.0, -0.8]
        D = ic.IidData(lam, beta, n, rng)
        A = D.A; k = 1; N = n - 3
        xi = A[2:, 0]; eta = A[1, 0]; phi = A[1, 1]; a = A[2:, 1]
        Up = A[2:, 2:]                         # u_perp coordinates
        W = Up @ Up.T
        ell = lam / np.sqrt(1 - lam**2)
        v1 = xi + ell*eta; v2 = ell*phi + a
        nulls = np.arange(2, p)
        Hb = math.sqrt(2*math.log(2*(p-2)+2) + 2*math.log(math.log(n)))
        order = nulls[np.argsort(-xi[nulls]/ell[nulls])]
        sets = []
        for m in [1, 3, 10, p//4, p//2, p-2]:
            sets.append(order[:m]); sets.append(order[::-1][:m]); sets.append(rng.choice(nulls, m, replace=False))
        for K in sets:
            T = np.r_[S0, K].astype(int)
            AT = W[np.ix_(T,T)] + np.outer(v2[T], v2[T])
            Ai = np.linalg.inv(AT)
            om = (Ai @ v1[T]) / np.sqrt(np.diag(Ai))
            q = v1[T] @ Ai @ v1[T]
            kap0 = N/phi**2; rho = N*eta/phi**2
            DT = ell[T] @ ell[T] + kap0
            X = (ell[T] @ xi[T] - rho)/DT
            s = (xi[T] - ell[T]*X)/np.sqrt(1 - ell[T]**2/DT)
            delta = np.sqrt(N)*om - s
            worst = max(worst, np.abs(delta[2:]).max())
            if rep == 0 and len(K) in (3, p//2):
                # direct RSS from coordinates: columns g_j (coords), e = sigma*A[0]
                Xc = (lam[:,None]*A[1:2] + np.sqrt(1-lam**2)[:,None]*A[2:])[T]   # |T| x d
                e = A[0]
                Qm, _ = np.linalg.qr(Xc.T)
                rss = e @ e - np.sum((Qm.T @ e)**2)
                rss_err = max(rss_err, abs(rss - (e@e)/(1+q))/rss)
    bound = (p/math.sqrt(n) + math.sqrt(p*math.log(n)/n) + math.sqrt(math.log(n)/n))*Hb
    print("%-8d %-5d %.4e   %.4e                                       %.3f   %.1e" % (n, p, worst, bound, worst/bound, rss_err))
