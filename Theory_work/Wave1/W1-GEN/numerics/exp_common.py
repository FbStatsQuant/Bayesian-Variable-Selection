"""exp_common.py -- shared route-statistics code, parallel map, aggregation, markdown tables."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import csv, json, math, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import bvs_core as bc

_USTAR_MEMO = {}


def pmap(fn, jobs, workers=7):
    if workers <= 1:
        return [fn(j) for j in jobs]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, jobs, chunksize=1))


def ustar_for_blocks(spec_key, spec, blocks, n, noise_tol=False):
    key = (spec_key, n, tuple(tuple(b) for b in blocks), noise_tol)
    if key not in _USTAR_MEMO:
        pop = bc.Pop(spec["Sigma"], spec["theta"], n, spec.get("sigma2", 1.0))
        Us = pop.block_minimisers(blocks, tol=(spec.get("sigma2", 1.0) * math.log(n) if noise_tol else 1e-7))
        _USTAR_MEMO[key] = Us
    return _USTAR_MEMO[key]


def symdiff(A, B):
    return len(set(A) ^ set(B))


def move_kind(a, b):
    a, b = set(a), set(b)
    if len(b) == len(a) + 1:
        return "add"
    if len(b) == len(a) - 1:
        return "delete"
    return "swap"


def nonprogress(Sfrom, Sto, S0):
    """first move is a non-progress move if it does not decrease |S symmetric-difference S0|"""
    return symdiff(Sto, S0) >= symdiff(Sfrom, S0)


def make_centres(V, S0, Sstar, K, rng, n_random=10, max_single=30):
    V = sorted(V)
    S0 = tuple(sorted(S0))
    out = {(): "empty"}
    sing = V if len(V) <= max_single else sorted(rng.choice(V, max_single, replace=False).tolist())
    for j in sing:
        out[(j,)] = "single"
    out[tuple(sorted(Sstar))] = "Sstar"
    out[S0] = "S0"
    for j in S0:
        out[tuple(x for x in S0 if x != j)] = "S0-1"
    rest = [j for j in V if j not in set(S0)]
    for j in (rng.choice(rest, min(5, len(rest)), replace=False).tolist() if rest else []):
        out[tuple(sorted(S0 + (j,)))] = "S0+1"
    for _ in range(n_random):
        k = int(rng.integers(2, min(len(V), 8, K) + 1))
        out[tuple(sorted(rng.choice(V, k, replace=False).tolist()))] = "random"
    return out


def centre_sweep(prob, centres, V, S0, ell):
    Vset = set(V)
    S0 = tuple(sorted(S0))
    st = dict(sw_n=0, sw_inV=0, sw_reach=0, sw_scored=0, sw_cert_S0=0, sw_maxmoves=0, sw_maxtau=0,
              sw_first_nonprog=0, sw_first_moves=0, sw_limit=0)
    fails = []
    for C in centres:
        ls = bc.local_search(prob, C, ell)
        inV = all(set(s) <= Vset for s in ls["path"])
        reach = S0 in ls["path"]
        tau = ls["path"].index(S0) if reach else -1
        st["sw_n"] += 1
        st["sw_inV"] += inV
        st["sw_reach"] += reach
        st["sw_scored"] += (S0 in ls["scored"])
        st["sw_cert_S0"] += (ls["certified"] and ls["final"] == S0)
        st["sw_maxmoves"] = max(st["sw_maxmoves"], ls["moves"])
        st["sw_maxtau"] = max(st["sw_maxtau"], tau)
        st["sw_limit"] += ls["local_limit"]
        if ls["first_move"] is not None:
            st["sw_first_moves"] += 1
            st["sw_first_nonprog"] += nonprogress(ls["first_move"][0], ls["first_move"][1], S0)
        if not (inV and reach and (S0 in ls["scored"]) and ls["certified"]):
            fails.append(dict(centre=list(C), path_len=len(ls["path"]), inV=inV, reach=reach,
                              certified=ls["certified"], limit=ls["local_limit"]))
    st["sw_fail_examples"] = fails[:3]
    return st


def analyse(X, y, spec, spec_key, ell=None, sweep=0, rng=None, extra_centres=None, noise_ref=False):
    """Route statistics for one data set.
    spec: dict(Sigma, theta, groups (or None), S0, V, sigma2, ref_Sstar (optional))"""
    n, p = X.shape
    t0 = time.time()
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    ell = bc.ell_cap(n, p) if ell is None else ell
    S0 = tuple(sorted(spec["S0"]))
    V = tuple(sorted(spec["V"]))
    Vset = set(V)
    Us = ustar_for_blocks(spec_key, spec, blocks, n)
    Sstar = tuple(sorted(j for U in Us for j in U))
    mode = info.mode
    ls = bc.local_search(prob, mode, ell)
    hpm = bc.hpm_of(prob, ls["scored"])
    row = dict(
        n=n, p=p, B=bc.block_size(n, p), J=len(blocks), ell=ell,
        blocks_eq_groups=(bc.same_partition(blocks, spec["groups"]) if spec.get("groups") else None),
        Sstar=list(Sstar), Sstar_size=len(Sstar),
        Sstar_eq_ref=(Sstar == tuple(sorted(spec["ref_Sstar"])) if spec.get("ref_Sstar") is not None else None),
        start=list(mode), start_size=len(mode), start_eq_Sstar=(mode == Sstar),
        start_extra_vs_S0=len(set(mode) - set(S0)), start_missing_vs_S0=len(set(S0) - set(mode)),
        start_extra_vs_Sstar=len(set(mode) - set(Sstar)), start_missing_vs_Sstar=len(set(Sstar) - set(mode)),
        one_minus_pi0_Sstar=float(-np.expm1(bc.log_pi0(prob, info, Sstar))) if len(Sstar) <= prob.K else float("nan"),
        start_truncated=info.truncated,
        path_in_V=all(set(s) <= Vset for s in ls["path"]),
        moves=ls["moves"], tau=(ls["path"].index(S0) if S0 in ls["path"] else -1),
        S0_scored=(S0 in ls["scored"]), certified=ls["certified"], local_limit=ls["local_limit"],
        final_eq_S0=(ls["final"] == S0), hpm_eq_S0=(hpm == S0), n_scored=len(ls["scored"]),
        path=[list(s) for s in ls["path"]],
    )
    if noise_ref:
        Us2 = ustar_for_blocks(spec_key, spec, blocks, n, noise_tol=True)
        Sstar2 = tuple(sorted(j for U in Us2 for j in U))
        row["Sstar_noise_size"] = len(Sstar2)
        row["start_eq_Sstar_noise"] = (mode == Sstar2)
        row["Sstar_noise_eq_S0"] = (Sstar2 == S0)
    if ls["first_move"] is not None:
        row["first_move"] = move_kind(*ls["first_move"])
        row["first_nonprogress"] = nonprogress(ls["first_move"][0], ls["first_move"][1], S0)
    else:
        row["first_move"] = "none"
        row["first_nonprogress"] = None
    if sweep or extra_centres:
        rng = np.random.default_rng(0) if rng is None else rng
        cs = list(make_centres(V, S0, Sstar, prob.K, rng, n_random=sweep).keys()) if sweep else []
        if extra_centres:
            cs += [tuple(sorted(c)) for c in extra_centres]
        row.update(centre_sweep(prob, cs, V, S0, ell))
    row["secs"] = round(time.time() - t0, 2)
    return row


# ------------------------------------------------------------------------------------------------
def write_rows(rows, stem):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(stem + "_raw.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()})


def frac(rows, key, val=True):
    vals = [r[key] for r in rows if r.get(key) is not None]
    return f"{sum(1 for v in vals if v == val)}/{len(vals)}"


def agg(rows, group_keys):
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r[k] for k in group_keys), []).append(r)
    out = []
    for gk, rs in groups.items():
        d = dict(zip(group_keys, gk))
        d["N"] = len(rs)
        d["blocks=groups"] = frac(rs, "blocks_eq_groups")
        d["start=S*"] = frac(rs, "start_eq_Sstar")
        d["|start| (min-max)"] = f"{min(r['start_size'] for r in rs)}-{max(r['start_size'] for r in rs)}"
        d["|S*|"] = f"{min(r['Sstar_size'] for r in rs)}-{max(r['Sstar_size'] for r in rs)}"
        d["path in V"] = frac(rs, "path_in_V")
        d["moves (max)"] = max(r["moves"] for r in rs)
        d["ell"] = rs[0]["ell"]
        d["S0 scored"] = frac(rs, "S0_scored")
        d["certified"] = frac(rs, "certified")
        d["HPM=S0"] = frac(rs, "hpm_eq_S0")
        d["max(1-pi0(S*))"] = "%.2e" % max(r["one_minus_pi0_Sstar"] for r in rs)
        if "start_eq_Sstar_noise" in rs[0]:
            d["start=S*noise"] = frac(rs, "start_eq_Sstar_noise")
            d["|S*noise|"] = f"{min(r['Sstar_noise_size'] for r in rs)}-{max(r['Sstar_noise_size'] for r in rs)}"
        if "sw_n" in rs[0]:
            d["sweep: inV"] = f"{sum(r['sw_inV'] for r in rs)}/{sum(r['sw_n'] for r in rs)}"
            d["sweep: S0 reached"] = f"{sum(r['sw_reach'] for r in rs)}/{sum(r['sw_n'] for r in rs)}"
            d["sweep: S0 scored"] = f"{sum(r['sw_scored'] for r in rs)}/{sum(r['sw_n'] for r in rs)}"
            d["sweep: cert=S0"] = f"{sum(r['sw_cert_S0'] for r in rs)}/{sum(r['sw_n'] for r in rs)}"
            d["sweep: max tau"] = max(r["sw_maxtau"] for r in rs)
        out.append(d)
    return out


def md_table(rows, cols=None):
    if not rows:
        return "(no rows)\n"
    cols = cols or list(rows[0].keys())
    s = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(r.get(c, "")) for c in cols) + " |\n"
    return s
