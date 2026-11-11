r"""rm_common.py -- shared helpers for the W3-RM sharpness probes (V1, L1, L2, N1).  FALSIFICATION / SHARPNESS PROBES:
observations only, never proofs; all theorems are asymptotic.  Imports (does NOT edit) the ported method objects in
Theory_work/Wave1C/C-GROW/numerics/bvs_core.py  (bc).

DEFINITIONS (used by every experiment)
  start mode S~      : bc.start_mode(prob, bc.partition(X)) (block DP; tie tolerance 1e-12, enumeration cap 20000;
                       `start_trunc` = info.truncated, `start_nopt` = info.n_optimal).
  extras             : S~ \ S0.   `extras_by_type` = JSON dict type -> count, type labels are experiment-specific.
  LS0 (complete scan): bc.local_search(prob, centre, cap) -- scores EVERY feasible add / delete / swap at every visited
                       centre.  Shipped cap = ell_cap(n,p) + |centre|; OLD cap = ell_cap(n,p) alone.  One run with the
                       shipped cap is made; the OLD-cap result is DERIVED exactly from the same (deterministic) path:
                       the old-cap path is path[:ell+1]  (final = path[min(moves, ell)], limit iff moves > ell).
  moves by type      : along the path, each move S -> S' classified relative to S0:
                       del_extra (delete a non-truth), add_truth, add_null, del_truth,
                       swap_total (any swap), swap_truth_removing (swap whose removed element is a truth),
                       swap_add_truth (swap removing a non-truth and adding a truth), [other swaps: null<->null].
                       truth-removing moves = del_truth + swap_truth_removing.
                       all_del_extra := (moves >= 0 and every move is del_extra).
  endpoint == S0     : final centre of the (capped) search equals S0 exactly.
  certified          : the complete scan at the final centre found no strict improvement (bc `certified`;
                       False iff the move cap was hit with an improving move still available).
  S0 scored          : S0 equals some visited centre or one of its add/delete/swap neighbours (size cap K ignored).
  S0 is reported-model proxy (`S0_is_max`) : S0 scored AND F(S0) >= F(M) for every M scored by that capped LS0
                       (scored = visited centres + all their complete-scan neighbours).
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
CGROW = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Wave1C", "C-GROW", "numerics"))
sys.path.insert(0, CGROW)
import bvs_core as bc          # noqa: E402  (imports numpy)
import numpy as np             # noqa: E402


def block_of(blocks, p):
    return bc.block_id_array(blocks, p)


def classify_move(Sa, Sb, S0set):
    a, b = set(Sa), set(Sb)
    if len(b) == len(a) + 1:
        j = next(iter(b - a))
        return "add_truth" if j in S0set else "add_null"
    if len(b) == len(a) - 1:
        j = next(iter(a - b))
        return "del_truth" if j in S0set else "del_extra"
    o = next(iter(a - b))
    i = next(iter(b - a))
    if o in S0set:
        return "swap_truth_removing"
    return "swap_add_truth" if i in S0set else "swap"


def is_nb_or_eq(C, S):
    Cs, Ss = set(C), set(S)
    if len(Cs) == len(Ss) + 1:
        return Ss <= Cs
    if len(Cs) == len(Ss) - 1:
        return Cs <= Ss
    if len(Cs) == len(Ss):
        return len(Cs - Ss) <= 1
    return False


def start_record(prob, blocks, S0, types, prefix="start_"):
    """Compute the start mode; return (mode, info, record dict).  types: array of per-column type labels."""
    info = bc.start_mode(prob, blocks)
    mode = tuple(info.mode)
    S0set = set(S0)
    extras = sorted(set(mode) - S0set)
    cnt = {}
    for e in extras:
        cnt[str(types[e])] = cnt.get(str(types[e]), 0) + 1
    r = {
        "start_size": len(mode), "S0_in_start": S0set <= set(mode), "n_extra": len(extras),
        "n_missing_truths": len(S0set - set(mode)),
        "extras_by_type": json.dumps(cnt, sort_keys=True), "start_eq_S0": mode == tuple(sorted(S0)),
        "start_trunc": bool(info.truncated), "start_nopt": int(info.n_optimal),
        "B": bc.block_size(prob.n, prob.p),
    }
    return mode, info, r


def ls_record(prob, centre, S0, prefix):
    """LS0 (complete scans) from `centre`, shipped cap ell+|centre| and OLD cap ell; returns record dict (keys prefixed)."""
    n, p = prob.n, prob.p
    S0t = tuple(sorted(S0))
    S0set = set(S0t)
    centre = tuple(sorted(centre))
    ell = bc.ell_cap(n, p)
    cap = ell + len(centre)
    res = bc.local_search(prob, centre, cap)
    path = res["path"]
    toks = [classify_move(path[i], path[i + 1], S0set) for i in range(len(path) - 1)]
    # per-state max F over {centre} + complete-scan neighbours (cached scores)
    Fmax_state = []
    for S in path:
        nb = bc.neighbours(S, p, prob.K)
        fv = prob.F_many(nb) if nb else np.array([-np.inf])
        Fmax_state.append(max(prob.F(S), float(np.max(fv))))
    FS0 = prob.F(S0t)
    out = {}
    for tag, c in (("", cap), ("old_", ell)):
        used = min(res["moves"], c) + 1                       # path[:used]
        moves = used - 1
        final = path[used - 1]
        if tag == "":
            limit = bool(res["local_limit"])
            certified = bool(res["certified"])
        else:
            limit = (res["moves"] > c) or (res["local_limit"] and c == cap)
            certified = not limit
        scored = any(is_nb_or_eq(path[i], S0t) for i in range(used))
        fmax = max(Fmax_state[:used])
        tk = toks[:moves]
        cn = {k: sum(1 for t in tk if t == k) for k in
              ("del_extra", "add_truth", "add_null", "del_truth", "swap", "swap_truth_removing", "swap_add_truth")}
        out.update({
            prefix + tag + "cap": c, prefix + tag + "moves": moves,
            prefix + tag + "final_eq_S0": final == S0t, prefix + tag + "certified": certified,
            prefix + tag + "S0_scored": scored,
            prefix + tag + "S0_is_max": bool(scored and FS0 >= fmax - 0.0),
            prefix + tag + "n_del_extra": cn["del_extra"], prefix + tag + "n_add_truth": cn["add_truth"],
            prefix + tag + "n_add_null": cn["add_null"], prefix + tag + "n_del_truth": cn["del_truth"],
            prefix + tag + "n_swap": cn["swap"] + cn["swap_truth_removing"] + cn["swap_add_truth"],
            prefix + tag + "n_swap_add_truth": cn["swap_add_truth"],
            prefix + tag + "n_swap_trem": cn["swap_truth_removing"],
            prefix + tag + "n_trem": cn["del_truth"] + cn["swap_truth_removing"],
            prefix + tag + "all_del_extra": moves == cn["del_extra"],
            prefix + tag + "final_size": len(final),
            prefix + tag + "S0_subset_final": S0set <= set(final),
        })
    out[prefix + "moveseq"] = " ".join(toks)
    return out, res


# --------------------------------------------------------------------------------------------------- summaries
def load_csv(path):
    import csv
    def conv(v):
        if v in ("True", "False"):
            return v == "True"
        try:
            f = float(v)
            return f
        except ValueError:
            return v
    with open(path, newline="") as f:
        return [{k: conv(v) for k, v in r.items()} for r in csv.DictReader(f)]


def write_csv(path, rows):
    import csv
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def cnt(rows, f):
    return "%d/%d" % (sum(1 for r in rows if f(r)), len(rows))
