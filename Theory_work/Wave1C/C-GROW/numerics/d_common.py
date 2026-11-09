"""d_common.py -- C-GROW diagnostics (D1 posterior concentration, D2/D3 LS0 with caps), one data set per call.
Library: bvs_core.py / study_common.py / exp_common.py copied (unchanged) from Theory_work/Wave1/W1-GEN/numerics.
job = (scen, p, c, n, seed, do_d1)   truths: s0 = 4, step 5 (study generator): 0-based indices 2, 26, 53, 75 (groups 0, 5, 10, 15) at every p."""
import math, time, json
import numpy as np
from scipy.special import logsumexp
import bvs_core as bc
import exp_common as ec
import study_common as sc

S0N, STEP = 4, 5
BIG = 10 ** 4


def ncat(S0, extras, blocks, p):
    """classify extras: same group (of 5) as a truth / same block (data partition) as a truth / elsewhere"""
    tg = {j // 5 for j in S0}
    bid = {}
    for b, blk in enumerate(blocks):
        for j in blk:
            bid[j] = b
    tb = {bid[j] for j in S0}
    out = dict(same_group=0, same_block=0, elsewhere=0)
    dists = []
    for e in extras:
        if e // 5 in tg:
            out["same_group"] += 1
        elif bid[e] in tb:
            out["same_block"] += 1
        else:
            out["elsewhere"] += 1
        dists.append(min(abs(e - t) for t in S0))
    return out, dists


def tok(Sa, Sb, S0):
    a, b = set(Sa), set(Sb)
    T = set(S0)
    if len(b) == len(a) + 1:
        j = next(iter(b - a))
        return "+T" if j in T else "+N"
    if len(b) == len(a) - 1:
        j = next(iter(a - b))
        return "-T" if j in T else "-N"
    o = next(iter(a - b))
    i = next(iter(b - a))
    return "sw" + ("T" if o in T else "N") + ">" + ("T" if i in T else "N")


def mc3(prob, start, steps, rng):
    """add/delete/swap Metropolis with Hastings correction; target pi(S) ~ exp(F(S)), |S| <= K.
    returns (trace of states as list of tuples (post-step), set of proposed models, accept rate)"""
    p, K = prob.p, prob.K
    S = tuple(sorted(start))
    FS = prob.F(S)
    states = []
    proposed = set()

    def nvalid(k):
        return (1 if (k < K and k < p) else 0) + (1 if k >= 1 else 0) + (1 if (k >= 1 and k < p) else 0)

    acc = 0
    for _ in range(steps):
        k = len(S)
        types = []
        if k < K and k < p:
            types.append("a")
        if k >= 1:
            types.append("d")
        if k >= 1 and k < p:
            types.append("s")
        t = types[int(rng.integers(len(types)))]
        Sset = set(S)
        if t == "a":
            while True:
                j = int(rng.integers(p))
                if j not in Sset:
                    break
            Sp = tuple(sorted(Sset | {j}))
            lq_fwd = -math.log(len(types)) - math.log(p - k)
            lq_rev = -math.log(nvalid(k + 1)) - math.log(k + 1)
        elif t == "d":
            i = S[int(rng.integers(k))]
            Sp = tuple(x for x in S if x != i)
            lq_fwd = -math.log(len(types)) - math.log(k)
            lq_rev = -math.log(nvalid(k - 1)) - math.log(p - (k - 1))
        else:
            i = S[int(rng.integers(k))]
            while True:
                j = int(rng.integers(p))
                if j not in Sset:
                    break
            Sp = tuple(sorted((Sset - {i}) | {j}))
            lq_fwd = -math.log(len(types)) - math.log(k) - math.log(p - k)
            lq_rev = lq_fwd
        proposed.add(Sp)
        Fp = prob.F(Sp)
        lr = Fp - FS + lq_rev - lq_fwd
        if lr >= 0 or math.log(rng.random()) < lr:
            S, FS = Sp, Fp
            acc += 1
        states.append(S)
    return states, proposed, acc / steps


def tr_unc_best(tr):
    return tr["scan_best"]


def best_of(prob, models):
    """argmax F (ties: smaller size, then lexicographic)"""
    best, bf = None, -np.inf
    for S in models:
        f = prob.F(S)
        if best is None or f > bf or (f == bf and (len(S), S) < (len(best), best)):
            best, bf = S, f
    return best, bf



def is_nb_or_eq(C, S):
    """True iff S == C or S is a one-flip / swap neighbour of C (add/delete/swap), ignoring the size cap K"""
    Cs, Ss = set(C), set(S)
    if len(Cs) == len(Ss) + 1:
        return Ss <= Cs
    if len(Cs) == len(Ss) - 1:
        return Cs <= Ss
    if len(Cs) == len(Ss):
        return len(Cs - Ss) <= 1
    return False


def F_nocache(prob, models):
    """F of a list of sorted tuples, grouped by size, WITHOUT storing in prob.cache (memory); identical arithmetic to prob.F_many"""
    out = np.empty(len(models))
    bysz = {}
    for i, S in enumerate(models):
        bysz.setdefault(len(S), []).append(i)
    for k, ids in bysz.items():
        v = prob.logm_idx(np.array([models[i] for i in ids], dtype=np.int64).reshape(len(ids), k)) if k > 0 else np.full(len(ids), prob.logm0)
        out[ids] = prob.logw[k] + v
    return out


def ls_trace(prob, centre, maxmoves=BIG):
    """same search as bc.local_search with cap maxmoves, but records per scan the best scanned model (F, model; ties: smaller size, lex).
    Capped searches (cap ell) are derived from the uncapped trace: path[:ell+1], local_limit iff the uncapped search has more than ell moves."""
    S = tuple(sorted(centre))
    prob.F(S)
    path = [S]
    scan_best = []
    moves = 0
    certified = False
    while True:
        nb = bc.neighbours(S, prob.p, prob.K)
        Fv = F_nocache(prob, nb) if nb else np.array([])
        FS = prob.F(S)
        mx = float(Fv.max()) if len(nb) else bc.NEG
        cands = [nb[i] for i in np.flatnonzero(Fv == mx)] if len(nb) else []
        bm = min(cands) if cands else None
        if bm is None or FS >= mx:
            scan_best.append((FS, S) if (bm is None or FS > mx or (len(S), S) < (len(bm), bm)) else (mx, bm))
        else:
            scan_best.append((mx, bm))
        if mx > FS:
            if moves >= maxmoves:
                break
            S = bm
            moves += 1
            path.append(S)
        else:
            certified = True
            break
    return dict(path=path, final=S, moves=moves, certified=certified, scan_best=scan_best)


def derive(tr, ell, S0):
    """result of the production search with cap ell, from an uncapped trace tr"""
    path, mv = tr["path"], tr["moves"]
    if mv <= ell:
        used = len(path)
        final, moves, limit, cert = tr["final"], mv, False, True
    else:
        used = ell + 1
        final, moves, limit, cert = path[ell], ell, True, False
    reach = S0 in path[:used]
    tau = path[:used].index(S0) if reach else -1
    scored = any(is_nb_or_eq(path[i], S0) for i in range(used))
    return dict(final=final, moves=moves, local_limit=limit, certified=cert, tau=tau, S0_scored=scored, used=used)


def run(job):
    scen, p, c, n, seed, do_d1 = job[:6]
    do_empty = job[6] if len(job) > 6 else True
    t00 = time.time()
    spec, X, y = sc.build_xy((scen, p, S0N, STEP, c, n, seed, "iid"))
    S0 = tuple(sorted(spec["S0"]))
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    t1 = time.time()
    info = bc.start_mode(prob, blocks)
    t_start = time.time() - t1
    mode = tuple(info.mode)
    ell_n = bc.ell_cap(n, p)
    extras = sorted(set(mode) - set(S0))
    missing = sorted(set(S0) - set(mode))
    cat, dists = ncat(S0, extras, blocks, p)
    r = dict(scen=scen, p=p, c=c, n=n, seed=seed, B=bc.block_size(n, p), K=prob.K, ell_n=ell_n,
             start=json.dumps(list(mode)), start_size=len(mode), n_extra=len(extras), n_missing=len(missing),
             start_contains_S0=(len(missing) == 0), start_eq_S0=(mode == S0), symdiff=len(extras) + len(missing),
             extra_same_group=cat["same_group"], extra_same_block=cat["same_block"], extra_elsewhere=cat["elsewhere"],
             extra_min_idx_dist=(min(dists) if dists else -1), extra_max_idx_dist=(max(dists) if dists else -1),
             extras=json.dumps(extras), start_truncated=info.truncated, n_optimal_start=info.n_optimal,
             t_start=round(t_start, 2))
    caps = {"ell_n": ell_n, "2ell_n": 2 * ell_n, "size+ell_n": len(mode) + ell_n, "unc": BIG}
    tr = ls_trace(prob, mode, BIG)
    ls_unc = tr
    for name, cap in caps.items():
        dv = derive(tr, cap, S0)
        r["%s_cap" % name] = cap
        r["%s_S0_scored" % name] = dv["S0_scored"]
        r["%s_final_eq_S0" % name] = (dv["final"] == S0)
        r["%s_local_limit" % name] = dv["local_limit"]
        r["%s_certified" % name] = dv["certified"]
        r["%s_moves" % name] = dv["moves"]
        r["%s_tau" % name] = dv["tau"]
        r["%s_final_size" % name] = len(dv["final"])
    # move types along the uncapped path
    path = ls_unc["path"]
    toks = [tok(path[i], path[i + 1], S0) for i in range(len(path) - 1)]
    tau = r["unc_tau"]
    r["unc_seq"] = " ".join(toks)
    seq_tau = toks[:tau] if tau >= 0 else None
    r["unc_seq_to_tau"] = (" ".join(seq_tau) if seq_tau is not None else "NA")
    if tau >= 0:
        r["tau_minus_symdiff"] = tau - r["symdiff"]
        only = all(t in ("+T", "-N") for t in seq_tau)
        adds_first = True
        seen_del = False
        for t in seq_tau:
            if t == "-N":
                seen_del = True
            if t == "+T" and seen_del:
                adds_first = False
        r["seq_only_addT_delN"] = only
        r["seq_adds_first"] = only and adds_first
        r["seq_n_addT"] = sum(t == "+T" for t in seq_tau)
        r["seq_n_addN"] = sum(t == "+N" for t in seq_tau)
        r["seq_n_delT"] = sum(t == "-T" for t in seq_tau)
        r["seq_n_delN"] = sum(t == "-N" for t in seq_tau)
        r["seq_n_swap"] = sum(t.startswith("sw") for t in seq_tau)
        r["seq_minimal"] = (tau == r["symdiff"])
    else:
        r["tau_minus_symdiff"] = None
    r["t_ls"] = round(time.time() - t00, 2)

    if do_d1:
        FS0 = prob.F(S0)
        # (b) neighbourhood of S0
        nb = bc.neighbours(S0, p, prob.K)
        dn = prob.F_many(nb) - FS0
        r["D1b_log_sum_nb"] = float(logsumexp(dn))
        r["D1b_max_nb_gap"] = float(dn.max())  # F(N)-F(S0), >0: a neighbour beats S0
        r["D1b_n_nb"] = len(nb)
        r["D1b_n_nb_better"] = int((dn > 0).sum())
        kind = [("add" if len(N) > len(S0) else "del" if len(N) < len(S0) else "swap") for N in nb]
        for kd in ("add", "del", "swap"):
            sel = np.array([k == kd for k in kind])
            r["D1b_log_sum_" + kd] = float(logsumexp(dn[sel])) if sel.any() else float("nan")
        # (a) all searches: uncapped LS from mode (done), from {}, from S0
        if do_empty:
            tr_e = ls_trace(prob, (), BIG)
        tr_s = ls_trace(prob, S0, BIG)
        cand = list(tr_unc_best(tr)) + list(tr_unc_best(tr_s)) + (list(tr_unc_best(tr_e)) if do_empty else [])
        bf_ls, b_ls = max(((f, m) for f, m in cand), key=lambda t: (t[0], -len(t[1]), tuple(-x for x in t[1])))
        r["D1a_LS_F_S0_minus_max"] = float(FS0 - bf_ls)
        r["D1a_LS_best_eq_S0"] = (b_ls == S0)
        r["D1a_LS_best"] = json.dumps(list(b_ls))
        r["D1a_LS_best_symdiff"] = len(set(b_ls) ^ set(S0))
        r["D1_LS_empty_done"] = bool(do_empty)
        if do_empty:
            r["D1_LS_empty_final_eq_S0"] = (tr_e["final"] == S0)
            r["D1_LS_empty_moves"] = tr_e["moves"]
        r["D1_LS_S0_final_eq_S0"] = (tr_s["final"] == S0)
        r["D1_LS_S0_final"] = json.dumps(list(tr_s["final"]))
        # (c) MC3
        steps = 20000
        rng = np.random.default_rng(777 + 13 * seed + n + 3 * scen + p)
        states, prop, accr = mc3(prob, mode, steps, rng)
        second = states[steps // 2:]
        r["D1c_frac_S0_second_half"] = sum(1 for s in second if s == S0) / len(second)
        r["D1c_frac_S0_all"] = sum(1 for s in states if s == S0) / len(states)
        r["D1c_frac_supset_S0_second_half"] = sum(1 for s in second if set(S0) <= set(s)) / len(second)
        r["D1c_mean_size_second_half"] = float(np.mean([len(s) for s in second]))
        r["D1c_accept"] = accr
        r["D1c_n_distinct_visited"] = len(set(states))
        r["D1c_first_hit_S0"] = next((i + 1 for i, s in enumerate(states) if s == S0), -1)
        vis_best, vf = best_of(prob, set(states))
        r["D1c_best_visited_F_minus_FS0"] = float(vf - FS0)
        r["D1c_best_visited_eq_S0"] = (vis_best == S0)
        r["D1c_best_visited"] = json.dumps(list(vis_best))
        b_ls_all, bf_all0 = best_of(prob, prop)
        bf_all, b_all = (bf_all0, b_ls_all) if (bf_all0 > bf_ls or (bf_all0 == bf_ls and (len(b_ls_all), b_ls_all) < (len(b_ls), b_ls))) else (bf_ls, b_ls)
        r["D1a_all_F_S0_minus_max"] = float(FS0 - bf_all)
        r["D1a_all_best_eq_S0"] = (b_all == S0)
        r["D1a_all_best"] = json.dumps(list(b_all))
        r["D1_n_proposed_mc3"] = len(prop)
        # simple lower bound on pi(S0): from the neighbourhood
        r["D1_logodds_lb"] = r["D1b_log_sum_nb"]
    r["t_total"] = round(time.time() - t00, 2)
    return r
