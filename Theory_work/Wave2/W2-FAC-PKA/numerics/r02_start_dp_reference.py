"""R02 scratch: independent closed-form exact-CS start-mode DP (block tables by full 2^b enumeration; size-capped
knapsack; prior w(k)); tests L1 saturation |start| = K at large n. Contiguous blocks of size b (a deterministic
partition allowed by L1). Cross-validated against bvs_core.start_mode at small n."""
import sys, math, json, time
from pathlib import Path
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import gammaln

def data(rho, theta, n, rng, sigma=1.0):
    p = len(theta)
    xi = rng.standard_normal(p); eta = rng.standard_normal()
    chi = rng.chisquare(n-1-p) if n-1-p > 0 else 0.0
    g = math.sqrt(rho)*eta + math.sqrt(1-rho)*xi
    tb = theta.sum(); Sth = (1-rho)*theta + rho*tb
    gSg = (g@g - rho/(1-rho+p*rho)*g.sum()**2)/(1-rho)
    h = n-1.0
    s2 = (h*(theta@Sth) + 2*sigma*math.sqrt(h)*(theta@g) + sigma**2*(gSg+chi))/h
    return (h*Sth + sigma*math.sqrt(h)*g)/math.sqrt(s2)

def logm(u, A, B, n, rho):  # up to the common constant; u array
    a = (n*n-1.0)*(1-rho)+1; b = (n*n-1.0)*rho; a2 = (n-1.0)*(1-rho)+1; b2 = (n-1.0)*rho
    nu = .01 + n/2.0
    um = np.maximum(u, 1)
    ldH = np.where(u > 0, (um-1)*math.log(a)+np.log(a+um*b), 0.0)
    ldG = np.where(u > 0, (um-1)*math.log(a2)+np.log(a2+um*b2), 0.0)
    quad = np.where(u > 0, (A - b/(a+u*b)*B**2)/a, 0.0)
    return -0.5*(ldH-ldG) - nu*np.log(.02 + (n-1.0) - n*quad)

def tables(z, blocks, n, rho):
    out = []
    cache = {}
    for C in blocks:
        bsz = len(C)
        if bsz not in cache:
            M = ((np.arange(2**bsz)[:, None] >> np.arange(bsz)[None, :]) & 1).astype(float)
            u = M.sum(1).astype(int); order = np.argsort(u, kind='stable'); starts = np.searchsorted(u[order], np.arange(bsz+1))
            cache[bsz] = (M, u, order, starts)
        M, u, order, starts = cache[bsz]
        zb = z[C]
        lm = logm(u, M@(zb*zb), M@zb, n, rho) - logm(np.array(0), 0.0, 0.0, n, rho)
        out.append(np.maximum.reduceat(lm[order], starts))
    return out

def start_size(z, blocks, n, rho, K, p):
    NEG = -np.inf
    V = np.full(K+1, NEG); V[0] = 0.0
    for t in tables(z, blocks, n, rho):
        W = np.full(K+1, NEG)
        for u, val in enumerate(t):
            if u > K: break
            np.maximum(W[u:], V[:K+1-u] + val, out=W[u:])
        V = W
    k = np.arange(K+1)
    lw = -math.log(2) - (gammaln(2*p) - gammaln(k+1) - gammaln(2*p-k))
    tot = V + lw
    kstar = int(np.argmax(tot))
    srt = np.sort(tot)[::-1]
    return kstar, float(tot[K]-tot[:K].max()) if K > 0 else 0.0

if __name__ == '__main__':
    rows = []
    rho = .5
    for n, ratio, design in [(800, .85, 'N1pos'), (20000, .85, 'N1pos'), (20000, .51, 'N1pos'), (20000, .85, 'single2'),
                             (20000, .9999, 'single2'), (20000, .85, 'N1mixed'), (100000, .85, 'N1mixed'), (100000, .85, 'N1pos')]:
        p = n-1 if ratio > .99 else int(n*ratio); K = n//2; b = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
        blocks = [list(range(j, min(j+b, p))) for j in range(0, p, b)]
        for seed in range(2):
            theta = np.zeros(p)
            if design == 'single2': theta[0] = 2.0
            elif design == 'N1pos': theta[[2, 26, 53, 75]] = .5*np.array([1.4, 1, 1.8, 1.2])
            else: theta[[2, 26, 53, 75]] = .5*np.array([1.4, -1, 1.8, -1.2])
            z = data(rho, theta, n, np.random.default_rng(seed))
            t0 = time.time(); k, gap = start_size(z, blocks, n, rho, K, p)
            row = dict(n=n, p=p, K=K, b=b, design=design, theta_bar=float(theta.sum()), seed=seed, start_size=k, saturated=(k == K),
                       logF_K_minus_best_smaller=gap, secs=round(time.time()-t0, 1))
            rows.append(row); print(json.dumps(row), flush=True)
    Path('start_dp_out.json').write_text(json.dumps(rows, indent=1))
