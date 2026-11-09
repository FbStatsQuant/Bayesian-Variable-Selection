"""pk_common.py -- W2-SIM family PK: shared helpers (seeds, truths, path statistics).

Ticket modules are imported UNCHANGED from the ticket snapshot ($TICKETS/Theory_work/Wave2/W2-FAC-PK/numerics,
sha256 in code/tickets_20261109T0943.SHA256SUMS on NOTS) or, for local pilots, from the repo copy (identical sha256).
"""
import os
import sys
import math
import json
import hashlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"     # one numerical thread per task (fac_core would otherwise default to 2)

_T = os.environ.get("TICKETS")
if _T is None:   # local pilot: repo root
    _T = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
TICKET_DIR = os.path.join(_T, "Theory_work", "Wave2", "W2-FAC-PK", "numerics")
sys.path.insert(0, TICKET_DIR)

import numpy as np  # noqa: E402

S0_IDX = (2, 26, 53, 75)          # 0-based, as pk_core / n1_scale / fac_core.study_layout
LAYOUTS = {"aligned": (1.4, 1.0, 1.8, 1.2), "mixed": (1.4, -1.0, 1.8, -1.2)}
FAMILY_TAG = 0x504B                # "PK"


def module_sha(names=("pk_core.py", "cs_core.py", "bvs_core.py", "fac_core.py")):
    out = {}
    for nm in names:
        with open(os.path.join(TICKET_DIR, nm), "rb") as f:
            out[nm] = hashlib.sha256(f.read()).hexdigest()
    return out


def cell_seed(*key):
    """deterministic 63-bit seed, distinct across (experiment, cell, replicate) keys."""
    ent = [FAMILY_TAG] + [int(round(k * 1000)) if isinstance(k, float) else
                          (int(hashlib.sha256(k.encode()).hexdigest()[:8], 16) if isinstance(k, str) else int(k))
                          for k in key]
    return int(np.random.SeedSequence(ent).generate_state(2, dtype=np.uint64)[0] >> np.uint64(1))


def theta_vec(p, layout):
    th = np.zeros(p)
    co = LAYOUTS[layout]
    th[list(S0_IDX[:len(co)])] = co
    return th


def ell_cap(n, p):
    return math.ceil(math.log2(n + p + 1))


def hit_index(sizes_extras_missing):
    """smallest scan index k with S0 in N(C_k) u {C_k} (flip/swap neighbourhood). LS0 with cap a scores S0 iff
    a >= k_hit (it scans the centres 0..min(a, m*))."""
    for k, (ex, mi) in enumerate(sizes_extras_missing):
        if ex + mi <= 1 or (ex == 1 and mi == 1):
            return k
    return None


def move_stats(tags):
    """tags: list of move tags, first char in {'s','-','+'} (swap, deletion, addition)."""
    from collections import Counter
    kinds = [t[0] for t in tags]
    first_del = next((i for i, m in enumerate(kinds) if m == "-"), None)
    lead = 0
    for m in kinds:
        if m == "s":
            lead += 1
        else:
            break
    return dict(tag_counts=dict(Counter(tags)), n_swaps=kinds.count("s"), n_dels=kinds.count("-"),
                n_adds=kinds.count("+"), lead_swaps=lead, first_del=first_del,
                swaps_after_first_del=(sum(1 for m in kinds[first_del:] if m == "s") if first_del is not None else 0),
                adds_after_first_del=(sum(1 for m in kinds[first_del:] if m == "+") if first_del is not None else 0))


def rle(tags):
    """run-length encoding of the move tag sequence, e.g. 'sN*19 -N*296'."""
    out = []
    for t in tags:
        if out and out[-1][0] == t:
            out[-1][1] += 1
        else:
            out.append([t, 1])
    return " ".join(f"{t}*{c}" for t, c in out)


def write_jsonl(path, rec):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ------------------------------------------------------------------------------------------------------------------
# general-scorer path tracer wrapper (R3, S5PK): fac_core.ls0_path + censoring, NaN guards, margins, direct spot checks
# ------------------------------------------------------------------------------------------------------------------
def _neighbour_set(T, O, kind, i, j=None):
    T = list(T)
    if kind == "add":
        return tuple(sorted(T + [int(O[i])]))
    if kind == "del":
        return tuple(t for t in T if t != T[i])
    return tuple(sorted([t for t in T if t != T[i]] + [int(O[j])]))


def _top_candidates(T, sc, m=5):
    """the m best neighbours (by scan F) as (F_scan, set)."""
    out = []
    O = sc["O"]
    add, dl, sw = sc["add"], sc["del"], sc["swap"]
    if add is not None and len(add):
        for i in np.argsort(-add)[:m]:
            if np.isfinite(add[i]):
                out.append((float(add[i]), ("add", int(i))))
    if len(dl):
        for i in np.argsort(-dl)[:m]:
            out.append((float(dl[i]), ("del", int(i))))
    if sw.size:
        flat = sw.ravel()
        idx = np.argpartition(-flat, min(m, flat.size - 1))[:m] if flat.size > m else np.arange(flat.size)
        for f in idx:
            i, j = divmod(int(f), sw.shape[1])
            out.append((float(sw[i, j]), ("swap", i, j)))
    out.sort(key=lambda t: -t[0])
    res = []
    for F, key in out[:m]:
        if key[0] == "swap":
            res.append((F, _neighbour_set(T, O, "swap", key[1], key[2])))
        else:
            res.append((F, _neighbour_set(T, O, key[0], key[1])))
    return res


def _r6(x):
    return None if (x is None or not np.isfinite(x)) else round(float(x), 6)


def trace_general(P, start, S0, max_moves=10 ** 6, check_every=250, n_check=5):
    """Uncapped LS0 path from `start` with fac_core.ls0_path (unchanged).  Adds: executed-move accounting (fac_core
    records the proposed move of the last scan before testing its move limit), censoring flag, NaN/inf guards on every
    scan, the winner margin (best minus second-best neighbour F) per scan, and direct (Cholesky, bvs_core.Problem.F) re-scoring
    of the n_check best neighbours + the centre at scans 0, 1, every `check_every`, the last scan, and the first 50 scans with
    margin < 1e-6."""
    import fac_core as fc
    S0 = tuple(S0)
    em, props, margins, checks, rows = [], [], [], [], []
    arrival = [None]
    ties = [0]
    state = {}

    def direct_check(T, sc, k, why):
        cands = _top_candidates(T, sc, n_check)
        FT_dir = P.F(tuple(int(t) for t in T))
        d = [abs(sc["FT"] - FT_dir)]
        dirF = []
        for Fs, S in cands:
            fdir = P.F(S)
            dirF.append(fdir)
            d.append(abs(Fs - fdir))
        order_ok = (int(np.argmax(dirF)) == 0) if dirF else True
        checks.append(dict(scan=k, why=why, size=len(T), max_absdiff=float(max(d)), n_cand=len(cands),
                           winner_order_ok=order_ok, top_gap_scan=(cands[0][0] - cands[1][0]) if len(cands) > 1 else None))

    def rec(P_, T, sc, inf):
        k = len(em)
        for nm in ("add", "del", "swap"):
            a = sc[nm]
            if a is not None and np.size(a) and np.isnan(a).any():
                raise FloatingPointError(f"NaN in scan {nm} at scan {k}")
            if a is not None and np.size(a) and np.isposinf(a).any():
                raise FloatingPointError(f"+inf in scan {nm} at scan {k}")
        if not np.isfinite(sc["FT"]):
            raise FloatingPointError(f"non-finite F(T) at scan {k}")
        em.append((inf["extras"], inf["missing"]))
        if arrival[0] is None and tuple(T) == S0:
            arrival[0] = k
        if inf.get("n_ties", 1) > 1:
            ties[0] += 1
        props.append(inf.get("move"))
        rows.append((k, len(T), inf["extras"], inf["missing"], inf.get("move"), _r6(inf["best_add"]), _r6(inf["best_del_N"]),
                     _r6(inf["best_del_T"]), _r6(inf["best_swap"]), _r6(inf["best_swap_T"])))
        vals = [np.ravel(a) for a in (sc["add"], sc["del"], sc["swap"]) if a is not None and np.size(a)]
        allv = np.concatenate(vals) if vals else np.array([])
        allv = allv[np.isfinite(allv)]
        if allv.size >= 2:
            top2 = np.partition(allv, allv.size - 2)[-2:]
            mg = float(top2[1] - top2[0])
        else:
            mg = None
        margins.append(mg)
        near = mg is not None and mg < 1e-6
        if near:
            state["n_near"] = state.get("n_near", 0) + 1
        if k in (0, 1) or (check_every and k % check_every == 0) or (near and state["n_near"] <= 50):
            direct_check(T, sc, k, "near-tie" if near else "schedule")
        state["last"] = (tuple(T), sc, inf, k)

    r = fc.ls0_path(P, start, S0, max_moves=max_moves, record=rec)
    T, sc, inf, k = state["last"]
    if not any(c["scan"] == k for c in checks):
        direct_check(T, sc, k, "last")
    limited = "move" in inf          # the last scan found a strictly better neighbour but the move limit stopped the path
    m = r["moves"]
    tags = [t.replace("sw", "s") for t in props[:m]]   # executed moves only
    assert len(em) == m + 1 and all(t is not None for t in tags)
    mv = [x for x in margins if x is not None]
    return dict(r=r, em=em, tags=tags, limited=limited, certified=not limited, arrival=arrival[0], scan_ties=ties[0],
                n_near_ties=state.get("n_near", 0), rows=rows,
                min_margin=(min(mv) if mv else None), min_margin_scan=(margins.index(min(mv)) if mv else None),
                direct_checks=checks, max_direct_absdiff=max(c["max_absdiff"] for c in checks),
                direct_order_ok=all(c["winner_order_ok"] for c in checks))


def path_record(P, start, S0, tr, n, p):
    """common per-run fields from trace_general output (general-scorer experiments)."""
    S0 = tuple(S0)
    r = tr["r"]
    K = P.K
    m_star = r["moves"]
    k_hit = hit_index(tr["em"])
    ell = ell_cap(n, p)
    s = len(start)
    st = move_stats(tr["tags"])
    final = tuple(int(t) for t in r["final"])
    out = dict(K=K, S0=list(S0), start_size=s, saturated=(s == K), start_has_S0=set(S0) <= set(start),
               start_truths=len(set(S0) & set(start)),
               limited=tr["limited"], certified=tr["certified"],
               m_star=m_star, m_star_over_K=m_star / K, final_is_S0=(final == S0), final_size=len(final),
               final_extras=len(set(final) - set(S0)), final_missing=len(set(S0) - set(final)),
               k_hit=k_hit, arrival=tr["arrival"], ell=ell, cap_MR1=ell + s, cap_2=ell + 2 * s,
               MR1_scores=(k_hit is not None and k_hit <= ell + s),
               cap2_scores=(k_hit is not None and k_hit <= ell + 2 * s),
               excess_over_MR1=(k_hit - ell - s) if k_hit is not None else None,
               W_minus_ell_s0=st["lead_swaps"] - ell - len(S0),
               scan_ties=tr["scan_ties"], n_near_ties=tr["n_near_ties"], min_margin=tr["min_margin"],
               min_margin_scan=tr["min_margin_scan"], max_direct_absdiff=tr["max_direct_absdiff"],
               direct_order_ok=tr["direct_order_ok"], direct_checks=tr["direct_checks"],
               moves_rle=rle(tr["tags"]), module_sha=module_sha(),
               scan_cols="scan,size,extras,missing,proposed_move,gain_add,gain_del_null,gain_del_truth,gain_swap_null_out,gain_swap_truth_out",
               first_scans=tr["rows"][:3],
               scan_at_first_del=(tr["rows"][st["first_del"]] if st["first_del"] is not None else None),
               last_scan=tr["rows"][-1], **st)
    if not out["final_is_S0"]:
        # independent check of the exceptional endpoint: direct scores of the endpoint and of S0
        out["F_final_direct"] = float(P.F(final))
        out["F_S0_direct"] = float(P.F(S0))
    return out
