"""Stream F helpers. Reuses ../numerics/common.py (exact posterior, enumeration). DRAFT (by this seat, unchecked)."""
import os, sys
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "numerics"))
import common as C   # exact posterior etc. (read-only reuse)

def ar_sigma(p, r=0.5):
    return r ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))

def gauss_d2(d, B, sig2, bstar, Sigma_raw):
    """EXACT (no fresh-x Monte Carlo) joint Hellinger^2 d_H^2(f_draw, f*) for x ~ N(0, Sigma_raw), sigma*=1, alpha*=0.
    Delta(x)=a+x'delta ~ N(a, s2), s2=delta' Sigma delta.  H^2 = 1 - c * E exp(-kappa Delta^2),
    c=sqrt(2 sqrt(v w)/(v+w)), kappa=1/(4(v+w)), E exp(-kappa Delta^2) = (1+2 kappa s2)^(-1/2) exp(-kappa a^2/(1+2 kappa s2))."""
    nd = B.shape[0]
    v = d.sy ** 2 * sig2
    braw = np.zeros((nd, d.p0))
    braw[:, d.keep] = d.sy * B / d.sd
    a = d.ybar - braw @ d.xbar0
    delta = braw - bstar[None, :]
    s2 = np.einsum('ij,ij->i', delta @ Sigma_raw, delta)
    w = 1.0
    kap = 1.0 / (4 * (v + w))
    cc = np.sqrt(2 * np.sqrt(v * w) / (v + w))
    den = 1 + 2 * kap * s2
    E = den ** -0.5 * np.exp(-kap * a * a / den)
    return 1 - cc * E

def exact_posterior_draws(Xr, yr, ndraw, rng):
    """prep + enumerate all 2^q models (q<=14) + draw ndraw posterior samples.  Returns d, idx, lp(normalised pi), sizes, B, sig2."""
    d = C.prep(Xr, yr)
    d.Xraw = Xr
    idx, lp, Q, sz = C.exact_family(d)
    B, sig2, mid = C.sample_posterior(d, idx, lp, Q, ndraw, rng)
    pi = np.exp(lp - lp.max()); pi /= pi.sum()
    return d, idx, pi, sz, Q, B, sig2

def sample_quantities(d, bstar):
    """||mu||^2/n and ||theta*||^2/n  (sigma*=1), sample versions: mu = C X^r beta*, theta*_j = shat_j beta*_j on retained columns."""
    n = d.n
    # d.X is standardised (||x_j||^2=n-1, sd=d.sd) ; centred raw columns = d.X * d.sd
    th = d.sd * bstar[d.keep]
    mu = (d.X * d.sd) @ bstar[d.keep]
    return float(mu @ mu) / n, float(th @ th) / n

def log_det_ratio(d, S):
    """log D_S = log det((n+1)G_S+I) - log det(G_S+I)"""
    S = list(S)
    if not S: return 0.0
    G = d.G[np.ix_(S, S)]; I = np.eye(len(S))
    return np.linalg.slogdet((d.n + 1) * G + I)[1] - np.linalg.slogdet(G + I)[1]
