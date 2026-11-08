"""study_common.py -- study generator (Scripts/Data_generators/gen_dev_data.R lines 18-42) at small and real scale."""
import math
import numpy as np
import bvs_core as bc
import exp_common as ec

POS = (3, 2, 4, 1, 5, 3)
PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)


def scenario_sigma(scen, p):
    """verbatim port of scenario_covariance() (groups of 5)"""
    idx = np.arange(1, p + 1)
    group = np.ceil(idx / 5).astype(int)
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if scen == 1:
        return I
    if scen == 2:
        return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if scen == 3:
        return 0.7 * H + 0.3 * I
    if scen == 4:
        return 0.85 * H + 0.15 * I
    if scen == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scen == 6:
        rho = 0.4 + 0.1 * ((group - 1) % 6)
        S = H * rho[:, None]  # H * matrix(rho,p,p): column-major recycling -> row index
        # R: H*matrix(rho,p,p) with matrix filled by column; rho has length p so entry [i,j] = rho[i]
        S = S.copy()
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError


def study_truth(s0, step):
    k = np.arange(s0)
    block = 1 + step * k  # 1-based group index
    pos = np.array([POS[i % 6] for i in k])
    active = 5 * (block - 1) + pos  # 1-based
    beta = np.array([PATTERN[i % 6] for i in k])
    return active - 1, beta, block - 1  # 0-based indices, coefficient, 0-based group index


def study_spec(scen, p, s0, step, c):
    Sigma = scenario_sigma(scen, p)
    act, beta, blk = study_truth(s0, step)
    th = np.zeros(p)
    th[act] = c * beta
    groups = [tuple(range(5 * h, 5 * h + 5)) for h in range(p // 5)]
    V = tuple(sorted(j for h in blk for j in groups[h]))
    return dict(Sigma=Sigma, theta=th, groups=groups, S0=tuple(int(a) for a in sorted(act)), V=V,
                ref_Sstar=None, sigma2=1.0, scen=scen, c=c)


_SPEC = {}


def spec_cached(scen, p, s0, step, c):
    key = (scen, p, s0, step, c)
    if key not in _SPEC:
        _SPEC[key] = study_spec(scen, p, s0, step, c)
    return _SPEC[key]


_XEX = {}


def build_xy(job):
    scen, p, s0, step, c, n, seed, design = job
    spec = spec_cached(scen, p, s0, step, c)
    rng = np.random.default_rng(9000 * seed + 31 * n + 7 * scen + (0 if design == "iid" else 5))
    if design == "iid":
        Xr = bc.iid_design_raw(spec["Sigma"], n, rng)
        X = bc.standardize_X(Xr)
    else:
        key = (scen, p, n)
        if key not in _XEX:
            _XEX[key] = bc.exact_gram_design(spec["Sigma"], n, np.random.default_rng(555 + n + scen))
        X = _XEX[key]
    y = bc.make_y_std(X, spec["theta"], 1.0, rng)  # R code: signal = X beta (X standardised); y = c*signal + eps
    return spec, X, y


def job_study(job):
    """job = (scen, p, s0, step, c, n, seed, design) ; design in {'iid','exact'}"""
    scen, p, s0, step, c, n, seed, design = job
    spec, X, y = build_xy(job)
    key = ("study", scen, p, s0, step, c, n, design)
    r = ec.analyse(X, y, spec, key, sweep=0, noise_ref=True)
    r.update(dict(scen=scen, c=c, seed=seed, design=design, s0=s0))
    return r


def population_unit(job):
    """SEP zeta and Lemma-3 decrement for c=1 at unit scale (n=2 => n-1=1); scale by c^2 (n-1) afterwards."""
    scen, p, s0, step = job
    spec = spec_cached(scen, p, s0, step, 1.0)
    pop = bc.Pop(spec["Sigma"], spec["theta"], 2)
    r = bc.sep_and_decrement(pop, spec["V"], S0=spec["S0"])
    r["scen"] = scen
    return r


def population_blocks(job):
    """VIS / NL / S* at actual (population-partition) blocks for (scen, p, s0, step, c, n)."""
    scen, p, s0, step, c, n = job
    spec = spec_cached(scen, p, s0, step, c)
    B = bc.block_size(n, p)
    blocks = bc.partition_from_corr(spec["Sigma"], B)
    pop = bc.Pop(spec["Sigma"], spec["theta"], n)
    Us = pop.block_minimisers(blocks)
    Sstar = tuple(sorted(j for U in Us for j in U))
    vis, va = pop.vis_margin(blocks, Us)
    nl, na = pop.nl_leak(blocks, Us)
    S0 = spec["S0"]
    # noise-level reading of 'minimiser': tolerance sigma^2 log n instead of 1e-7
    Us2 = pop.block_minimisers(blocks, tol=spec["sigma2"] * math.log(n))
    Sstar2 = tuple(sorted(j for U in Us2 for j in U))
    vis2, _ = pop.vis_margin(blocks, Us2)
    nl2, _ = pop.nl_leak(blocks, Us2)
    signal_groups_split = sum(1 for g in spec["groups"] if set(g) & set(S0) and not any(set(g) <= set(b) for b in blocks))
    shared = sum(1 for b in blocks if sum(1 for j in S0 if j in b) > 1)
    return dict(scen=scen, p=p, s0=s0, c=c, n=n, B=B, J=len(blocks), blocks_eq_groups=bc.same_partition(blocks, spec["groups"]),
                Sstar_size=len(Sstar), Sstar_eq_S0=(Sstar == S0), Sstar_missing=sorted(set(S0) - set(Sstar)),
                Sstar_extra=sorted(set(Sstar) - set(S0)), VIS=vis, VIS_arg=str(va), NL=nl,
                truths_split_over_blocks=signal_groups_split, blocks_with_2plus_truths=shared,
                Sstar_noise_size=len(Sstar2), Sstar_noise_eq_S0=(Sstar2 == S0), VIS_noise=vis2, NL_noise=nl2,
                K=min(p, n // 2))
