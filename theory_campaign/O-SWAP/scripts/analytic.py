"""Analytic one-move miss probabilities (projection approximation PA of REPORT §2).
All quantities conditional on the design X; sigma = noise sd on the raw scale."""
import numpy as np
from scipy.stats import norm, chi2

_U = (np.arange(400) + 0.5) / 400          # midpoint quantile grid for chi^2_m
_GH_x, _GH_w = np.polynomial.hermite_e.hermegauss(60)   # probabilists' Gauss-Hermite
_GH_w = _GH_w / _GH_w.sum()


def p_add(lam, m, omega, n):
    """P( chi2_1 (1 - lam/(n+1)) > (lam-1)(chi2_m + omega) ), vectorised in lam."""
    E = chi2.ppf(_U, m)[None, :]
    lam = np.asarray(lam)[:, None]
    t2 = (lam - 1) * (E + omega) / (1 - lam / (n + 1))
    return (2 * norm.sf(np.sqrt(np.maximum(t2, 0)))).mean(1)


def p_drop(Lam, delta, m, omega, n):
    """P( (A/sig)^2 (1 - Lam/(n+1)) < (Lam-1)(chi2_m + omega) ), A/sig ~ N(delta,1)."""
    E = chi2.ppf(_U, m)[None, :]
    Lam = np.asarray(Lam)[:, None]; delta = np.abs(np.asarray(delta))[:, None]
    omega = np.asarray(omega)[:, None]
    t = np.sqrt(np.maximum((Lam - 1) * (E + omega) / (1 - Lam / (n + 1)), 0))
    return (norm.cdf(t - delta) - norm.cdf(-t - delta)).mean(1)


def p_swap_closed(delta, rho):
    """lambda = 1 closed form: P(B^2 > A^2) = Phi(-d-)Phi(d+) + Phi(d-)Phi(-d+)."""
    dm = np.abs(delta) * np.sqrt((1 - rho) / 2)
    dp = np.abs(delta) * np.sqrt((1 + rho) / 2)
    return norm.cdf(-dm) * norm.cdf(dp) + norm.cdf(dm) * norm.cdf(-dp)


def p_swap(lam, delta, rho, c0, n):
    """General lambda: P( (n/(n+1))(lam B^2 - A^2) - (lam-1)(s^2 + d^2 + c0) > 0 ),
    s ~ N(d+,1), d ~ N(-d-,1) independent, B = a s + b d, A = a s - b d,
    a = sqrt((1+rho)/2), b = sqrt((1-rho)/2). Gauss-Hermite in s, exact in d."""
    delta = np.abs(np.asarray(delta, float)); rho = np.asarray(rho, float)
    lam = np.asarray(lam, float); c0 = np.broadcast_to(np.asarray(c0, float), delta.shape)
    al = np.sqrt((1 + rho) / 2); be = np.sqrt((1 - rho) / 2)
    dp = delta * al; dm = delta * be
    k = n / (n + 1.0)
    out = np.zeros(delta.shape)
    for x, w in zip(_GH_x, _GH_w):
        s = dp + x
        # quadratic in d: a2 d^2 + a1 d + a0 > 0
        a2 = k * (lam - 1) * be ** 2 - (lam - 1)
        a1 = k * 2 * al * be * s * (lam + 1)
        a0 = k * (lam - 1) * al ** 2 * s ** 2 - (lam - 1) * (s ** 2 + c0)
        mu = -dm
        pr = np.empty(delta.shape)
        lin = np.abs(a2) < 1e-14
        # linear case: a1 d + a0 > 0
        with np.errstate(divide='ignore', invalid='ignore'):
            r = -a0 / a1
            plin = np.where(a1 > 0, norm.sf(r - mu), norm.cdf(r - mu))
            disc = a1 ** 2 - 4 * a2 * a0
            sq = np.sqrt(np.maximum(disc, 0))
            r1 = (-a1 - sq) / (2 * a2); r2 = (-a1 + sq) / (2 * a2)
            lo = np.minimum(r1, r2); hi = np.maximum(r1, r2)
            inside = norm.cdf(hi - mu) - norm.cdf(lo - mu)
            # a2 > 0: event outside roots (or everywhere if disc<0); a2 < 0: inside roots (or nowhere)
            pq = np.where(a2 > 0, np.where(disc > 0, 1 - inside, 1.0),
                          np.where(disc > 0, inside, 0.0))
        pr = np.where(lin, plin, pq)
        out += w * pr
    return out
