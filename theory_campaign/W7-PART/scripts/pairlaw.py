"""Exact and bounded tail laws of the Pearson sample correlation r_hat of n iid bivariate normal pairs with
population correlation r (the law of r_hat depends on r and n only).

  dens(x; r, n)  Hotelling's exact density
       f(x) = (n-2) Gamma(n-1) (1-r^2)^{(n-1)/2} (1-x^2)^{(n-4)/2} / (sqrt(2 pi) Gamma(n-1/2) (1-r x)^{n-3/2})
              * 2F1(1/2, 1/2; n-1/2; (1+r x)/2)
  upper(t; r, n) = P(r_hat >= t),  lower(t; r, n) = P(r_hat <= t)   (mpmath quadrature of the density)
  ub_upper / ub_lower : the explicit bounds of Lemma 2 (PROOF.md §2):
       P_r(r_hat >= t) <= a_n (1+|r|)^{3/2}/(1-|r|) (1-t) Lambda_r(t)^{(n-4)/2}      (t >= r)
       P_r(r_hat <= t) <= a_n (1+|r|)^{3/2}/(1-|r|) (1+t) Lambda_r(t)^{(n-4)/2}      (t <= r)
       a_n = sqrt((n-2)/(2 pi)),  Lambda_r(t) = (1-r^2)(1-t^2)/(1-r t)^2.
  nct_upper : independent check through the regression representation
       T = sqrt(n-2) r_hat/sqrt(1-r_hat^2) = (Z + a sqrt(W)) / sqrt(V/(n-2)),  a = r/sqrt(1-r^2),
       Z ~ N(0,1), W ~ chi2_{n-1}, V ~ chi2_{n-2} independent  (PROOF.md §2, Lemma 1).
"""
import math
import mpmath as mp
import numpy as np
from scipy import stats, integrate

mp.mp.dps = 40


def log_dens(x, r, n):
    x = mp.mpf(x); r = mp.mpf(r)
    c = (mp.log(n - 2) + mp.loggamma(n - 1) - 0.5 * mp.log(2 * mp.pi) - mp.loggamma(n - mp.mpf(1) / 2))
    return (c + (n - 1) / mp.mpf(2) * mp.log(1 - r * r) + (n - 4) / mp.mpf(2) * mp.log(1 - x * x)
            - (n - mp.mpf(3) / 2) * mp.log(1 - r * x)
            + mp.log(mp.hyp2f1(0.5, 0.5, n - 0.5, (1 + r * x) / 2)))


def dens(x, r, n):
    return mp.e ** log_dens(x, r, n)


def upper(t, r, n):
    """P_r(r_hat >= t)."""
    if t >= 1:
        return mp.mpf(0)
    # split at the mode region to help quadrature
    pts = sorted(set([mp.mpf(t), mp.mpf(1)] + ([mp.mpf(r)] if t < r < 1 else [])))
    return mp.quad(lambda x: dens(x, r, n), pts)


def lower(t, r, n):
    """P_r(r_hat <= t)."""
    pts = sorted(set([mp.mpf(-1), mp.mpf(t)] + ([mp.mpf(r)] if -1 < r < t else [])))
    return mp.quad(lambda x: dens(x, r, n), pts)


def two_sided_upper(t, r, n):
    """P_r(|r_hat| >= t), t > 0."""
    return upper(t, r, n) + upper(t, -r, n)


def Lam(r, t):
    return (1 - r * r) * (1 - t * t) / (1 - r * t) ** 2


def ub_upper(t, r, n):
    a = math.sqrt((n - 2) / (2 * math.pi))
    return a * (1 + abs(r)) ** 1.5 / (1 - abs(r)) * (1 - t) * Lam(r, t) ** ((n - 4) / 2)


def ub_lower(t, r, n):
    a = math.sqrt((n - 2) / (2 * math.pi))
    return a * (1 + abs(r)) ** 1.5 / (1 - abs(r)) * (1 + t) * Lam(r, t) ** ((n - 4) / 2)


def ub_two_sided(t, r, n):
    """P_r(|r_hat| >= t) for |r| < t, via Lambda_{-|r|} <= Lambda_{|r|}."""
    return 2 * ub_upper(t, abs(r), n)


def nct_upper(t, r, n):
    """P_r(r_hat >= t) via E_W[ P(noncentral t_{n-2}(a sqrt W) >= tau) ], tau = sqrt(n-2) t / sqrt(1-t^2)."""
    k = n - 2
    tau = math.sqrt(k) * t / math.sqrt(1 - t * t)
    a = r / math.sqrt(1 - r * r)
    W = stats.chi2(n - 1)
    f = lambda w: W.pdf(w) * stats.nct.sf(tau, k, a * math.sqrt(w)) if a != 0 else W.pdf(w) * stats.t.sf(tau, k)
    lo, hi = W.ppf(1e-14), W.ppf(1 - 1e-14)
    v, _ = integrate.quad(f, lo, hi, limit=200, epsabs=0, epsrel=1e-10)
    return v


# Rate function and the balanced threshold (PROOF.md §3)
def rate(r, t):
    """I(t; r) = -1/2 log Lambda_r(t): P(r_hat beyond t) = exp(-n I + O(log n))."""
    return -0.5 * math.log(Lam(r, t))


def t_star(rho, psi):
    """Threshold equalising Lambda_rho(t) = Lambda_psi(t), psi < t < rho (both >= 0)."""
    q = math.sqrt((1 - psi * psi) / (1 - rho * rho))
    return (q - 1) / (q * rho - psi)


def I_star(rho, psi):
    return rate(psi, t_star(rho, psi))
