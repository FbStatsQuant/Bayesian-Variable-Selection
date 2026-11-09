"""n0_common.py -- shared design builders / runners for W2-APP numerics (n1_, n2_, n3_).
Imports (does NOT edit) the ported method objects from Theory_work/Wave1C/C-GROW/numerics/bvs_core.py.
All designs: raw rows iid N(0, Sigma), Sigma unit diagonal; y = X theta + eps on standardised X (sigma = 1), via bc.make_y_std.
"""
import os, sys, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
BVS = "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-GROW/numerics"
if BVS not in sys.path:
    sys.path.insert(0, BVS)
import numpy as np
import bvs_core as bc

BASE_SEED = 20261109          # all rngs: default_rng(SeedSequence([BASE_SEED, tag, did, n, p, seed]))
DID = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "V1": 5, "V2": 6, "V3a": 7, "V3b": 8}
THETA3 = np.array([1.0, -0.8, 1.2])
THETA3_ZERO = np.array([1.0, -0.5, -0.5])


def rng_for(tag, did, n, p, seed):
    return np.random.default_rng(np.random.SeedSequence([BASE_SEED, tag, DID[did], n, p, seed]))


# ---------------------------------------------------------------- covariance builders
def toeplitz_from_acf(acf, p):
    acf = np.asarray(acf, float)
    i = np.arange(p)
    return acf[np.abs(i[:, None] - i[None, :])]


def acf_ma2(p):
    th = np.array([1.0, 0.8, -0.5])
    g0 = (th ** 2).sum()
    g1 = th[0] * th[1] + th[1] * th[2]
    g2 = th[0] * th[2]
    a = np.zeros(p)
    a[0], a[1], a[2] = 1.0, g1 / g0, g2 / g0
    return a


def acf_ar2(p, phi=(0.5, 0.3)):
    f1, f2 = phi
    a = np.zeros(p)
    a[0] = 1.0
    a[1] = f1 / (1.0 - f2)
    for k in range(2, p):
        a[k] = f1 * a[k - 1] + f2 * a[k - 2]
    return a


def equicorr_blocks(sizes, rho):
    p = int(sum(sizes))
    S = np.eye(p)
    s = 0
    for g in sizes:
        S[s:s + g, s:s + g] = (1 - rho) * np.eye(g) + rho * np.ones((g, g))
        s += g
    return S


def block_sizes(p, g):
    full, rem = divmod(p, g)
    return [g] * full + ([rem] if rem else [])


def sigma_of(did, n, p):
    """population correlation matrix; also returns info dict (groups, visible nulls...)"""
    info = {}
    if did == "L1":
        S = toeplitz_from_acf(acf_ma2(p), p)
    elif did == "L2":
        S = toeplitz_from_acf(acf_ar2(p), p)
    elif did == "L3":
        S = equicorr_blocks(block_sizes(p, 20), 0.6)
        info["g"] = 20
    elif did == "L4":
        S = toeplitz_from_acf(0.5 ** np.arange(p), p)
    elif did == "V1":
        m = int(round(n ** (1.0 / 3.0)))
        assert p >= m + 20
        S = np.eye(p)
        a = 1.0 / (2.0 * math.sqrt(m))
        S[0, 1:m + 1] = a
        S[1:m + 1, 0] = a
        info["m"] = m
        info["leaves"] = tuple(range(1, m + 1))
    elif did == "V2":
        g = min(int(round(math.sqrt(n))), p)
        S = equicorr_blocks(block_sizes(p, g), 0.5)
        info["g"] = g
    elif did in ("V3a", "V3b"):
        S = equicorr_blocks([p], 0.3)
    else:
        raise ValueError(did)
    return S, info


def truths_of(did, n, p, s0=3):
    """truth indices and theta values."""
    if did == "V1":
        return (0,), np.array([1.0])
    if did == "V2":
        info = sigma_of(did, n, p)[1]
        g = info["g"]
        nfull = p // g
        sizes = block_sizes(p, g)
        if s0 <= nfull:
            blocks = sorted(set(int(round(x)) for x in np.linspace(0, nfull - 1, s0))) if s0 > 1 else [0]
            if len(blocks) < s0:
                blocks = list(range(s0))
        else:  # not enough full blocks: use all blocks (last may be partial)
            blocks = list(range(min(s0, len(sizes))))
        starts = np.cumsum([0] + sizes)
        idx = tuple(int(starts[b] + sizes[b] // 2) for b in blocks)
        th = THETA3[:len(idx)]
        return idx, th.copy()
    if did == "V3b":
        th = THETA3_ZERO
    else:
        th = THETA3
    idx = tuple(int(round(p * f)) for f in (0.15, 0.5, 0.85))
    return idx, th.copy()


def build_data(did, n, p, seed, s0=3, tag=1):
    """returns dict(X standardised, y, theta, S0, Sigma, info)"""
    S, info = sigma_of(did, n, p)
    idx, th = truths_of(did, n, p, s0)
    theta = np.zeros(p)
    theta[list(idx)] = th
    rng = rng_for(tag, did, n, p, seed)
    Wr = bc.iid_design_raw(S, n, rng)
    X = bc.standardize_X(Wr)
    y = bc.make_y_std(X, theta, 1.0, rng)
    return dict(X=X, y=y, theta=theta, S0=tuple(sorted(idx)), Sigma=S, info=info, Wraw=Wr)


# ---------------------------------------------------------------- timed local search (identical logic to bc.local_search + deadline)
def ls_timed(prob, centre, ell, tmax=600.0):
    t0 = time.time()
    S = tuple(sorted(centre))
    prob.F(S)
    scored = {S}
    path = [S]
    moves = 0
    certified = False
    local_limit = False
    timed_out = False
    while True:
        nb = bc.neighbours(S, prob.p, prob.K)
        Fv = prob.F_many(nb) if nb else np.array([])
        scored.update(nb)
        FS = prob.F(S)
        mx = float(Fv.max()) if len(nb) else bc.NEG
        if mx > FS:
            if moves >= ell:
                local_limit = True
                break
            if time.time() - t0 > tmax:
                timed_out = True
                break
            cands = [nb[i] for i in np.flatnonzero(Fv == mx)]
            S = min(cands)
            moves += 1
            path.append(S)
        else:
            certified = True
            break
    return dict(path=path, final=S, scored=scored, moves=moves, certified=certified,
                local_limit=local_limit, timed_out=timed_out)


def start_and_ls(D, tmax=600.0):
    """partition, start mode, LS0 with cap ell_cap(n,p)+|S~0|.  D from build_data."""
    X, y, S0 = D["X"], D["y"], D["S0"]
    n, p = X.shape
    t0 = time.time()
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    t1 = time.time()
    info = bc.start_mode(prob, blocks)
    t2 = time.time()
    mode = tuple(info.mode)
    ell = bc.ell_cap(n, p) + len(mode)
    res = ls_timed(prob, mode, ell, tmax)
    t3 = time.time()
    extras = sorted(set(mode) - set(S0))
    missing = sorted(set(S0) - set(mode))
    dists = [min(abs(e - t) for t in S0) for e in extras]
    bsz = np.array([len(b) for b in blocks])
    bid = bc.block_id_array(blocks, p)
    out = dict(n=n, p=p, B=bc.block_size(n, p), K=prob.K, nblocks=len(blocks), blk_min=int(bsz.min()),
               blk_max=int(bsz.max()), blk_mean=float(bsz.mean()),
               blk_hist=" ".join("%d:%d" % (k, c) for k, c in zip(*np.unique(bsz, return_counts=True))),
               truths_in_distinct_blocks=len({int(bid[j]) for j in S0}) == len(S0),
               mode=mode, mode_size=len(mode), S0_in_mode=(len(missing) == 0), n_missing=len(missing),
               n_extra=len(extras), extras=extras,
               maxdist_extra=(max(dists) if dists else -1), start_truncated=bool(info.truncated),
               n_optimal_start=int(info.n_optimal),
               ell=ell, ls_moves=res["moves"], ls_certified=res["certified"], ls_limit=res["local_limit"],
               ls_timed_out=res["timed_out"], ls_S0_scored=(S0 in res["scored"]),
               ls_S0_on_path=(S0 in res["path"]), ls_final_eq_S0=(res["final"] == S0),
               ls_final_size=len(res["final"]), ls_final_symdiff=len(set(res["final"]) ^ set(S0)),
               t_part=round(t1 - t0, 1), t_start=round(t2 - t1, 1), t_ls=round(t3 - t2, 1))
    return out, mode, blocks, prob


if __name__ == "__main__":
    # sanity: Sigma PD and unit diagonal, truth placement; ls_timed == bc.local_search
    for did in DID:
        for n, p in [(800, 200), (12800, 400)]:
            S, info = sigma_of(did, n, p)
            ev = np.linalg.eigvalsh(S)
            idx, th = truths_of(did, n, p)
            print(did, n, p, "diag", np.allclose(np.diag(S), 1), "mineig %.3f" % ev.min(), "truths", idx, th, info.get("g", info.get("m", "")))
    D = build_data("L4", 800, 100, 1)
    prob = bc.Problem(D["X"], D["y"])
    blocks = bc.partition(D["X"])
    info = bc.start_mode(prob, blocks)
    r1 = bc.local_search(prob, info.mode, 10)
    r2 = ls_timed(prob, info.mode, 10)
    print("ls match:", r1["path"] == r2["path"], r1["moves"], r2["moves"], r1["certified"] == r2["certified"], r1["scored"] == r2["scored"])
