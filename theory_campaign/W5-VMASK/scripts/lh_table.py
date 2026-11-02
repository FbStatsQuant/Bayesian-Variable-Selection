"""Independent reproduction of the W3-PXN LH-iid table (configs A, B) and adversarial variants.

Usage: python3 lh_table.py CONFIG [n p reps]...   writes ../results/lh_<CONFIG>.jsonl
Seed of a replicate: 7_000_000 + 10_000*cfg_index + 10*n_index + rep  (fixed).

Per replicate (own scorer, own partition port, own generator):
  actual v3 partition == groups?; margin condition of PXN Lemma P1 (min within |r| vs max cross |r|);
  SE-blk = min_b lambda_min(R_{C_b}); exact pi_0(S°), pi_0(S0) (convolution); Mstat; start mode; T22(i) q, e,
  bound <= pi_0(S°)?; LS0 = production local search from the start mode with the centre emitted
  (scored S0? certified at S0?); F(S0) - F(S°); max_l F(S0 + l) - F(S0) (the (L) addition margin);
  sample D_S margins at every lattice state of Lat(S°) \\ S0; Dep at x° = S° (c = 1).
"""
import json, math, sys, time
import numpy as np
from vm_core import *

CONFIGS = {
    "A": dict(g=10, rho=0.7, psis=[0.5], betas=[1.0], vis=[1.0]),
    "B": dict(g=10, rho=0.7, psis=[0.5, 0.5], betas=[1.0, -1.0], vis=[1.0]),
    # adversarial: |psi| close to rho (P1 margin (rho-psi)/3 = 0.017; (M2) margin unaffected)
    "ADV_PSI": dict(g=10, rho=0.7, psis=[0.65], betas=[1.0], vis=[1.0]),
    # adversarial: three null groups with within-group correlation 0.95 > rho = 0.7
    "ADV_NULL": dict(g=10, rho=0.7, psis=[0.5], betas=[1.0], vis=[1.0], rho_null=0.95, nullg=[5, 6, 7]),
    # outside the family: psi > rho (the cliff; expect hubs to pair up across groups)
    # near the cliff: psi = 0.69, rho = 0.7 (P1 margin (rho-psi)/3 = 0.0033)
    "EDGE_PSI": dict(g=10, rho=0.7, psis=[0.69], betas=[1.0], vis=[1.0]),
    "OUT_PSI": dict(g=10, rho=0.7, psis=[0.8], betas=[1.0], vis=[1.0]),
}
CIDX = {k: i for i, k in enumerate(CONFIGS)}


def neighbours(sc, C):
    """All flip and swap neighbours of C with their F: list of (F, frozenset)."""
    p, K = sc.p, sc.K
    out = []
    inC = np.zeros(p, bool)
    inC[C] = True
    if len(C) < K:
        a = sc.add_scan(C) + sc.logw[len(C) + 1]
        for l in np.flatnonzero(~inC):
            out.append((a[l], frozenset(C + [int(l)])))
    for j in C:
        T = [x for x in C if x != j]
        out.append((sc.F(T), frozenset(T)))
        a = sc.add_scan(T) + sc.logw[len(C)]
        for l in np.flatnonzero(~inC):
            out.append((a[l], frozenset(T + [int(l)])))
    return out


def lattice_DS(sc, Sref, M, S0):
    """min over S in Lat(S°)\\S0 of [max_progress F - max(F(S), max_nonprogress F)] and same restricted to
    Phi >= 2 (what LS-score needs)."""
    S0s = frozenset(S0)
    res_all, res_2 = np.inf, np.inf
    c = len(M)
    for mask in range(2 ** c - 1):
        S = sorted(Sref + [M[i] for i in range(c) if (mask >> i) & 1])
        phi = len(set(S) ^ S0s)
        FS = sc.F(S)
        best_prog, best_non = -np.inf, FS
        for Fv, T in neighbours(sc, S):
            if len(T ^ S0s) < phi:
                best_prog = max(best_prog, Fv)
            else:
                best_non = max(best_non, Fv)
        m = best_prog - best_non
        res_all = min(res_all, m)
        if phi >= 2:
            res_2 = min(res_2, m)
    return res_all, res_2


def dep_c1(sc, st, Sref, M, groups, g):
    """Dep = sum over l not in D u {j_b} of max(kappa_0, kappa_1) at x° = S° (W1-T38E D2), D = C_b minus j_b."""
    jb = M[0]
    hb = jb // g
    Dset = set(groups[hb]) - {jb}
    p = sc.p
    s = len(Sref)
    F0 = sc.F(Sref)
    a = sc.add_scan(Sref) + sc.logw[s + 1] - F0
    mk = st.masks_of(Sref)
    tot = 0.0
    inS = set(Sref)
    for l in range(p):
        if l in Dset or l == jb:
            continue
        b, t = st.where[l]
        if l in inS:
            T = [x for x in Sref if x != l]
            k1 = sc.F(T) - F0
            k0 = sc.logw[s - 1] - sc.logw[s] + st.logr[b][mk[b] & ~(1 << t)] - st.logr[b][mk[b]]
        else:
            k1 = a[l]
            k0 = sc.logw[s + 1] - sc.logw[s] + st.logr[b][mk[b] | (1 << t)] - st.logr[b][mk[b]]
        tot += math.exp(max(k0, k1))
    return tot


def run(cfgname, n, p, reps, nidx):
    cfg = CONFIGS[cfgname]
    g = cfg["g"]
    G = p // g
    p = G * g
    units, theta, S0, Sref, M, groups = lh_spec(G, g, cfg["rho"], cfg["psis"], cfg["betas"], cfg["vis"],
                                                rho_null=cfg.get("rho_null"), null_groups_rho=cfg.get("nullg"))
    c = len(M)
    ell = int(math.ceil(math.log2(n + p + 1)))
    out = []
    for rep in range(reps):
        t0 = time.time()
        seed = 7_000_000 + 10_000 * CIDX[cfgname] + 10 * nidx + rep
        rng = np.random.default_rng(seed)
        Xr, yr = gen_lh_iid(n, G, g, units, theta, rng)
        X, y = standardise(Xr, yr)
        bl, B = partition(X)
        beq = sorted(bl) == sorted(groups)
        minin, maxout = margin_partition_check(X, groups)
        seblk = min(np.linalg.eigvalsh(np.corrcoef(X[:, b].T)).min() if len(b) > 1 else 1.0 for b in bl)
        sc = Scorer(X, y)
        st = StartLaw(sc, bl)
        lp_ref = st.log_pi0(Sref)
        lp_S0 = st.log_pi0(S0)
        mode = st.mode()
        q, e, lb = st.t22(Sref)
        ls = local_search(sc, mode, ell, target=S0, emit_centre=True)
        cert = ls["certified"] and sorted(ls["returned"]) == S0
        FS0 = sc.F(S0)
        dF = FS0 - sc.F(Sref)
        a = sc.add_scan(S0) + sc.logw[len(S0) + 1] - FS0
        a[S0] = -np.inf
        Lmargin = -float(np.max(a))
        ds_all, ds_2 = lattice_DS(sc, Sref, M, S0)
        rec = dict(cfg=cfgname, n=n, p=p, rep=rep, seed=seed, B=B, blocks_eq_groups=beq, minin=minin, maxout=maxout,
                   seblk=seblk, log10_pi0_S0=lp_S0 / math.log(10), pi0_ref=math.exp(lp_ref),
                   mstat=lp_S0 + c * math.log(p) + 0.5 * c * math.log(n),
                   scaled_def=math.sqrt(n / math.log(n)) * (1 - math.exp(lp_ref)),
                   mode_eq_ref=(mode == Sref), mode=mode, q=q, e=e, t22_lb=lb, t22_ok=bool(lb <= math.exp(lp_ref) + 1e-12),
                   ls_scored=bool(ls["scored"]), ls_cert_S0=bool(cert), ls_moves=ls["moves"], ls_term=ls["term"],
                   ls_ties=ls["ties"], dF=dF, L_margin=Lmargin, DS_all=ds_all, DS_phi2=ds_2,
                   S0_best_seen=None, secs=time.time() - t0)
        if c == 1:
            rec["Dep"] = dep_c1(sc, st, Sref, M, groups, g)
        out.append(rec)
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rec.items() if k != "mode"}),
              flush=True)
    return out


if __name__ == "__main__":
    cfgname = sys.argv[1]
    args = [int(x) for x in sys.argv[2:]]
    grid = [tuple(args[i:i + 3]) for i in range(0, len(args), 3)]
    with open(f"../results/lh_{cfgname}.jsonl", "a") as f:
        for nidx, (n, p, reps) in enumerate(grid):
            nid = {200: 0, 400: 1, 800: 2, 1600: 3}.get(n, nidx)
            for rec in run(cfgname, n, p, reps, nid):
                f.write(json.dumps(rec) + "\n")
