"""endgame.py -- the finite END-GAME of the LS0 path on a multi-class exchangeable design (population level).

State: per class c either L ("large": many retained nulls, |I_c|/u_c small) or (u_c, I_c) with 0 <= u_c <= USTAR retained
null extremes (at +-H in xi-units), I_c = n+ - n- (|I_c| <= u_c, I_c = u_c mod 2). Truth counts s_c are fixed.
Leading-order gains in units of h/2 (h = H^2 ~ 2 log p, r = log n / h -> 1/(2a)); P = (R^-1 + diag(utot_c/psi_c))^-1
with utot_c = s_c + u_c (L classes: utot = +inf, i.e. row/col of P -> 0):
   x_c/H = sum_e P_ce I_e / sqrt(psi_c psi_e)
   delete sign-s extreme of class c:    1 + r - D_del,  D_del = (s - x_c/H)^2 psi_c/(psi_c - P_cc)
   delete from an L class:              r
   add sign-s extreme to small class d: D_add - 1 - r,  D_add = (s - x_d/H)^2 psi_d/(psi_d + P_dd)   (L classes: -r)
   swap (delete j in class c, then add l in class d, computed at the post-deletion state): sum of the two gains;
   same-type swap (same class and sign) has leading gain 0 and loses at second order (the retained extreme is the
   largest of its sign) -> excluded.
Walk: best move (strict improvement at leading order); if the best move is an L deletion, branch over which L class
becomes small next, entering at (USTAR, I) for every |I| <= min(USTAR, IMAX) with the right parity.
(EM) holds iff from every start state (any mix of L and small classes with |I_c| <= min(u_c, IMAX)) every branch of the
walk ends at S0 (all u_c = 0, no L) and every step has a leading-order gain gap >= GAP (no leading-order ties).
Usage: python endgame.py -> table for the designs in DESIGNS; also importable: check_EM(R, s, a, ...)."""
import itertools, math, sys
import numpy as np

USTAR = 3
L = "L"


def P_matrix(R, psi, utot):
    """utot entries may be inf (L classes): those rows/cols of P are 0 (exact limit)."""
    k = len(psi)
    fin = [c for c in range(k) if np.isfinite(utot[c])]
    P = np.zeros((k, k))
    if fin:
        Rinv = np.linalg.inv(R)
        # Schur: for finite set F, P_FF = (Rinv_FF + diag(u/psi))^-1 ... careful: infinite N on the others kills them
        # (R^-1 + N)^-1 with N_dd -> inf for d not in F: the block for F is (Rinv_FF + diag(u_F/psi_F))^-1
        Q = Rinv[np.ix_(fin, fin)] + np.diag(np.array([utot[c] / psi[c] for c in fin]))
        P[np.ix_(fin, fin)] = np.linalg.inv(Q)
    return P


def gains(R, psi, s, state, r):
    """state: tuple per class: L or (u, I). Returns list of (gain, move, newstate)."""
    k = len(psi)
    utot = np.array([np.inf if st == L else s[c] + st[0] for c, st in enumerate(state)], float)
    I = np.array([0.0 if st == L else st[1] for st in state])
    P = P_matrix(R, psi, utot)
    x = np.array([sum(P[c, e] * I[e] / math.sqrt(psi[c] * psi[e]) for e in range(k)) for c in range(k)])
    moves = []
    # deletions
    for c, st in enumerate(state):
        if st == L:
            moves.append((r, ("delL", c), None))
            continue
        u, Ic = st
        for sg in (1, -1):
            cnt = (u + sg * Ic) / 2  # number of sign-sg extremes
            if cnt >= 1:
                D = (sg - x[c]) ** 2 * psi[c] / (psi[c] - P[c, c])
                ns = list(state); ns[c] = (u - 1, Ic - sg)
                moves.append((1 + r - D, ("del", c, sg), tuple(ns)))
    # additions (small classes only; L: gain -r, never best)
    for d, st in enumerate(state):
        if st == L:
            continue
        u, Id = st
        if u >= USTAR:
            continue  # bounded end space; additions beyond USTAR are not modelled (never best in the tested designs)
        for sg in (1, -1):
            D = (sg - x[d]) ** 2 * psi[d] / (psi[d] + P[d, d])
            ns = list(state); ns[d] = (u + 1, Id + sg)
            moves.append((D - 1 - r, ("add", d, sg), tuple(ns)))
    # swaps: delete (c, sg) then add (d, sg') at the post-deletion state
    for g1, mv, ns1 in list(moves):
        if mv[0] != "del":
            continue
        c, sg = mv[1], mv[2]
        utot1 = np.array([np.inf if st == L else s[e] + st[0] for e, st in enumerate(ns1)], float)
        I1 = np.array([0.0 if st == L else st[1] for st in ns1])
        P1 = P_matrix(R, psi, utot1)
        x1 = np.array([sum(P1[e, f] * I1[f] / math.sqrt(psi[e] * psi[f]) for f in range(k)) for e in range(k)])
        for d, st in enumerate(ns1):
            if st == L:
                continue
            u, Id = st
            if u >= USTAR:
                continue
            for sg2 in (1, -1):
                if d == c and sg2 == sg:
                    continue  # same-type swap: leading gain 0, loses at second order
                D2 = (sg2 - x1[d]) ** 2 * psi[d] / (psi[d] + P1[d, d])
                ns = list(ns1); ns[d] = (u + 1, Id + sg2)
                moves.append((g1 + D2 - 1 - r, ("swap", c, sg, d, sg2), tuple(ns)))
    return moves


def walk(R, psi, s, state, r, imax, gap, seen, log, depth=0):
    """returns (ok, reason). seen: set of states visited on the current branch (cycle detection)."""
    k = len(psi)
    if all(st != L and st[0] == 0 for st in state):
        return True, "S0"
    if state in seen:
        return False, f"cycle at {state}"
    seen = seen | {state}
    mv = gains(R, psi, s, state, r)
    mv.sort(key=lambda t: -t[0])
    best = mv[0]
    if best[0] <= 0:
        return False, f"TRAP at {state}: best gain {best[0]:.3f} ({best[1]})"
    def canon(st):
        if st is None: return None
        neg = tuple(x if x == L else (x[0], -x[1]) for x in st)
        return min(st, neg, key=repr)
    for alt in mv[1:]:
        if best[0] - alt[0] >= gap:
            break
        if best[1][0] == "delL" and alt[1][0] == "delL":
            continue
        if canon(best[2]) == canon(alt[2]):
            continue  # sign-mirror tie (I = 0 symmetric states): both choices lead to equivalent states
        return False, f"near-tie at {state}: {best[1]} {best[0]:.3f} vs {alt[1]} {alt[0]:.3f}"
    if best[1][0] == "delL":
        # branch: any L class may become small next, entering at (USTAR, I)
        for c, st in enumerate(state):
            if st != L:
                continue
            for I in range(-min(USTAR, imax), min(USTAR, imax) + 1):
                if (I - USTAR) % 2:
                    continue
                ns = list(state); ns[c] = (USTAR, I)
                ok, why = walk(R, psi, s, tuple(ns), r, imax, gap, seen, log, depth + 1)
                if not ok:
                    return False, why
        return True, "ok"
    if log is not None:
        log.append((state, best[1], round(best[0], 3)))
    return walk(R, psi, s, best[2], r, imax, gap, seen, log, depth + 1)


def check_EM(R, s, a, imax=3, gap=1e-6, verbose=False):
    R = np.asarray(R, float); psi = 1 - np.diag(R); s = np.asarray(s, float)
    k = len(psi); r = 1.0 / (2 * a)
    per_class = [L] + [(u, I) for u in range(USTAR + 1) for I in range(-min(u, imax), min(u, imax) + 1) if (u - I) % 2 == 0]
    bad = []
    n_states = 0
    for state in itertools.product(per_class, repeat=k):
        if all(st != L and st[0] == 0 for st in state):
            continue
        n_states += 1
        ok, why = walk(R, psi, s, state, r, imax, gap, frozenset(), None)
        if not ok:
            bad.append((state, why))
    if verbose:
        print(f"  a={a}: {n_states} start states, {len(bad)} failing")
        for st, why in bad[:6]:
            print("    ", st, "->", why)
    return bad, n_states


def kappa_eff(R, s):
    R = np.asarray(R, float); psi = 1 - np.diag(R); Rinv = np.linalg.inv(R)
    out = []
    for c in range(len(psi)):
        Q = Rinv + np.diag(np.asarray(s, float) / psi); Q[c, c] = Rinv[c, c]
        idx = [d for d in range(len(psi)) if d != c]
        out.append(psi[c] * (Q[c, c] - Q[c, idx] @ np.linalg.solve(Q[np.ix_(idx, idx)], Q[idx, c])) if idx else psi[c] * Q[c, c])
    return np.array(out)


DESIGNS = [
    ("indep .5/.7, truths (4,0)", [[0.5, 0], [0, 0.7]], [4, 0]),
    ("indep .5/.3, truths (4,0)", [[0.5, 0], [0, 0.3]], [4, 0]),
    ("r12=.3 .5/.7, truths (4,0)", [[0.5, 0.3], [0.3, 0.7]], [4, 0]),
    ("r12=.3 .5/.7, truths (3,1)", [[0.5, 0.3], [0.3, 0.7]], [3, 1]),
    ("r12=.6 .7/.7, truths (1,1)", [[0.7, 0.6], [0.6, 0.7]], [1, 1]),
    ("r12=.69 .7/.7, truths (1,1)", [[0.7, 0.69], [0.69, 0.7]], [1, 1]),
    ("r12=.69 .7/.7, truths (2,0)", [[0.7, 0.69], [0.69, 0.7]], [2, 0]),
    ("k3 G, truths (2,1,1)", [[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], [2, 1, 1]),
    ("k3 G, truths (4,0,0)", [[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], [4, 0, 0]),
    ("k3 .8/.5, truths (1,1,1)", [[0.8, 0.5, 0.5], [0.5, 0.8, 0.5], [0.5, 0.5, 0.8]], [1, 1, 1]),
    ("k3 .8/.5, truths (3,0,0)", [[0.8, 0.5, 0.5], [0.5, 0.8, 0.5], [0.5, 0.5, 0.8]], [3, 0, 0]),
    ("neg r12=-.4 .7/.7, truths (1,1)", [[0.7, -0.4], [-0.4, 0.7]], [1, 1]),
    ("neg r12=-.4 .7/.7, truths (2,0)", [[0.7, -0.4], [-0.4, 0.7]], [2, 0]),
    ("r12=.3 .9/.9, truths (1,1)", [[0.9, 0.3], [0.3, 0.9]], [1, 1]),
    ("r12=.85 .9/.9, truths (1,1)", [[0.9, 0.85], [0.85, 0.9]], [1, 1]),
    ("r12=.85 .9/.9, truths (2,0)", [[0.9, 0.85], [0.85, 0.9]], [2, 0]),
]

if __name__ == "__main__":
    out = open("endgame_out.txt", "w")
    def pr(*a):
        s = " ".join(str(x) for x in a); print(s); out.write(s + "\n"); out.flush()
    pr(f"END-GAME verification (USTAR={USTAR}); IMAX=3; a in {{0.5,0.75,0.9,1.0}}; (EM) passes iff 0 failing start states.")
    for lab, R, s in DESIGNS:
        ke = kappa_eff(R, s)
        pr(f"=== {lab}: kappa_eff@S0={np.round(ke,3).tolist()}  trap thresholds (1+k)/2 for truth-free classes: "
           f"{[round((1+ke[c])/2,3) for c in range(len(s)) if s[c]==0]}")
        for a in (0.5, 0.75, 0.9, 1.0):
            bad, n = check_EM(R, s, a)
            kinds = {}
            for st, why in bad:
                key = why.split(" at ")[0]
                kinds[key] = kinds.get(key, 0) + 1
            pr(f"   a={a}: {n} start states, {len(bad)} failing {kinds if bad else ''}")
            for st, why in bad[:3]:
                pr("       ", st, "->", why)
    # random designs with a truth in every class
    pr("\nRANDOM designs, k in {2,3}, truths >= 1 in every class, a = 1.0 (worst), IMAX = 3:")
    rng = np.random.default_rng(0)
    nfail = 0; ntot = 0
    for t in range(60):
        k = int(rng.integers(2, 4))
        while True:
            A = rng.uniform(-1, 1, (k, k)); R = A @ A.T
            d = np.sqrt(np.diag(R)); R = R / np.outer(d, d) * rng.uniform(0.3, 0.95)
            if np.all(np.linalg.eigvalsh(R) > 1e-3): break
        s = rng.integers(1, 3, k).tolist()
        bad, n = check_EM(R, s, 1.0)
        ntot += 1
        if bad:
            nfail += 1
            pr(f"   FAIL: R={np.round(R,3).tolist()} s={s}: {bad[0][1]}")
    pr(f"   random designs with truths in every class: {nfail}/{ntot} fail (EM) at a=1.0")
    pr("\nRANDOM designs, k=2, class 2 truth-free, a = 1.0: (EM) vs kappa_eff(2) > 1 (uncoupled-type criterion):")
    agree = 0; ntot = 0
    for t in range(60):
        while True:
            A = rng.uniform(-1, 1, (2, 2)); R = A @ A.T
            d = np.sqrt(np.diag(R)); R = R / np.outer(d, d) * rng.uniform(0.3, 0.95)
            if np.all(np.linalg.eigvalsh(R) > 1e-3): break
        s = [int(rng.integers(1, 3)), 0]
        bad, n = check_EM(R, s, 1.0)
        ke = kappa_eff(R, s)[1]
        pred_ok = ke > 1.0
        ntot += 1
        if pred_ok == (len(bad) == 0): agree += 1
        else: pr(f"   DISAGREE: R={np.round(R,3).tolist()} s={s} kappa_eff2={ke:.3f} EM={'ok' if not bad else bad[0][1]}")
    pr(f"   agreement of (EM) with 'kappa_eff(truth-free class) > 1' at a=1: {agree}/{ntot}")
    out.close()
