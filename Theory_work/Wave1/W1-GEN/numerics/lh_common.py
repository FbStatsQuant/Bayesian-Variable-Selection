"""LH / LH-iid design builders and population checks shared by E2, E3, E4(iii)."""
import math
from functools import lru_cache
import numpy as np
import bvs_core as bc
import exp_common as ec

G_DEFAULT, g_DEFAULT = 12, 9


def lh_spec(G, g, rho, psi, c, n, shrink=False, nvis=1):
    psis = [psi] * c
    Sigma, info = bc.lh_sigma(G, g, rho, psis, nvis=nvis)
    beta = n ** -0.25 if shrink else 1.0
    th = bc.lh_theta(G * g, info, psis, [beta] * c, beta)
    S0 = tuple(int(j) for j in np.flatnonzero(th != 0))
    ref = tuple(sorted(set(S0) - set(info["b_hubs"])))
    V = tuple(sorted(j for gr in info["signal_groups"] for j in gr))
    return dict(Sigma=Sigma, theta=th, groups=info["groups"], S0=S0, V=V, ref_Sstar=ref, sigma2=1.0,
                info=info, beta=beta)


_X_CACHE = {}


def exact_X(G, g, rho, psi, c, n, nvis=1):
    key = (G, g, rho, psi, c, n, nvis)
    if key not in _X_CACHE:
        Sigma, _ = bc.lh_sigma(G, g, rho, [psi] * c, nvis=nvis)
        rng = np.random.default_rng(777 + n)
        _X_CACHE[key] = bc.exact_gram_design(Sigma, n, rng)
    return _X_CACHE[key]


_SPEC_CACHE = {}


def spec_cached(G, g, rho, psi, c, n, shrink):
    key = (G, g, rho, psi, c, n, shrink)
    if key not in _SPEC_CACHE:
        _SPEC_CACHE[key] = lh_spec(G, g, rho, psi, c, n, shrink)
    return _SPEC_CACHE[key]


def population_checks(spec, n):
    """VIS margin, NL leakage, SEP (zeta, ratio), Lemma-3 decrement with blocks = groups."""
    pop = bc.Pop(spec["Sigma"], spec["theta"], n)
    blocks = [list(gr) for gr in spec["groups"]]
    Us = pop.block_minimisers(blocks)
    Sstar = tuple(sorted(j for U in Us for j in U))
    vis, vis_arg = pop.vis_margin(blocks, Us)
    nl, nl_arg = pop.nl_leak(blocks, Us)
    sp = bc.sep_and_decrement(pop, spec["V"], S0=spec["S0"])
    return dict(n=n, Sstar_pop=list(Sstar), Sstar_eq_ref=(Sstar == tuple(spec["ref_Sstar"])),
                VIS_margin=vis, NL_leak=nl, zeta=sp["zeta"], zeta_ratio=sp["zeta_ratio"],
                dec=sp["dec"], dec_over_logn=sp["dec"] / math.log(n), sep_exhaustive=sp["exhaustive"],
                theta_min=pop.theta_min, n_theta2=n * pop.theta_min ** 2, logn=math.log(n))


def job_exact(job):
    G, g, rho, psi, c, n, seed, shrink = job
    spec = spec_cached(G, g, rho, psi, c, n, shrink)
    X = exact_X(G, g, rho, psi, c, n)
    rng = np.random.default_rng(1000 * seed + n)
    y = bc.make_y_std(X, spec["theta"], 1.0, rng)
    key = ("lh_exact", G, g, rho, psi, c, n, shrink)
    r = ec.analyse(X, y, spec, key, sweep=10, rng=np.random.default_rng(seed))
    r.update(dict(design="exact", rho=rho, psi=psi, c=c, seed=seed, shrink=shrink, G=G, g=g))
    return r


def job_iid(job):
    G, g, rho, psi, c, n, seed, shrink = job
    spec = spec_cached(G, g, rho, psi, c, n, shrink)
    rng = np.random.default_rng(5000 * seed + n + 17 * G)
    Xr = bc.iid_design_raw(spec["Sigma"], n, rng)
    th = spec["theta"]
    yr = Xr @ th + rng.standard_normal(n)
    X = bc.standardize_X(Xr)
    y = bc.standardize_y(yr)
    key = ("lh_iid", G, g, rho, psi, c, n, shrink)
    r = ec.analyse(X, y, spec, key, sweep=6, rng=np.random.default_rng(seed))
    r.update(dict(design="iid", rho=rho, psi=psi, c=c, seed=seed, shrink=shrink, G=G, g=g))
    return r
