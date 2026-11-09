"""endstate_map.py -- asymptotic end-state map for multi-class designs (population-level, no data).
End state sigma: per class c, (n+_c, n-_c) retained null extremes at +H / -H (plus the s_c truths of the class, whose
xi are O(L_n) = o(H) and are ignored). With P = (R^-1 + diag(u_c/psi_c))^-1, u_c = s_c + n+_c + n-_c:
   x_c/H = sum_e P_ce I_e / sqrt(psi_c psi_e),   I_e = n+_e - n-_e,
   deletion of a retained extreme of sign s in class c:  D_del = (s - x_c/H)^2 * psi_c/(psi_c - P_cc)
   addition of an outside extreme of sign s in class d:  D_add = (s - x_d/H)^2 * psi_d/(psi_d + P_dd)
Asymptotically (h = H^2 ~ 2 log p, r := log n / h -> 1/(2a), a = lim log p/log n <= 1):
   deletion gain ~ (h/2)(1 + r - D_del),  addition gain ~ (h/2)(D_add - 1 - r)   [+ o(h)].
A state is a local maximum iff min D_del >= 1 + r and max D_add <= 1 + r (swaps: gain ~ (h/2)(D_add' - D_del) over
the deleted-set centre; dominated when both conditions hold with margin -- checked separately in the lemma).
Usage: python endstate_map.py -> prints trapped states for several designs and a in {0.5, 0.75, 0.9, 1.0}.
"""
import itertools, math, numpy as np


def P_of(R, psi, u):
    return np.linalg.inv(np.linalg.inv(R) + np.diag(u / psi))


def analyse(R, psi, s, umax=2, a_list=(0.5, 0.75, 0.9, 1.0), verbose=True, label=""):
    k = len(psi)
    R = np.asarray(R, float); psi = np.asarray(psi, float); s = np.asarray(s, float)
    states = []
    rng_c = [(np_, nm) for np_ in range(umax + 1) for nm in range(umax + 1 - np_)]
    for combo in itertools.product(rng_c, repeat=k):
        nplus = np.array([c[0] for c in combo], float); nminus = np.array([c[1] for c in combo], float)
        if nplus.sum() + nminus.sum() == 0:
            continue
        u = s + nplus + nminus
        P = P_of(R, psi, u)
        I = nplus - nminus
        x = np.array([sum(P[c, e] * I[e] / math.sqrt(psi[c] * psi[e]) for e in range(k)) for c in range(k)])
        Ddel = []
        for c in range(k):
            for sgn, cnt in ((1, nplus[c]), (-1, nminus[c])):
                if cnt > 0:
                    Ddel.append(((sgn - x[c]) ** 2 * psi[c] / (psi[c] - P[c, c]), c, sgn))
        Dadd = []
        for d in range(k):
            for sgn in (1, -1):
                Dadd.append(((sgn - x[d]) ** 2 * psi[d] / (psi[d] + P[d, d]), d, sgn))
        states.append(dict(nplus=nplus.astype(int).tolist(), nminus=nminus.astype(int).tolist(),
                           minDdel=min(Ddel)[0], maxDadd=max(Dadd)[0], x=x))
    out = {}
    for a in a_list:
        r = 1.0 / (2 * a)
        trapped = [st for st in states if st["minDdel"] >= 1 + r and st["maxDadd"] <= 1 + r]
        adds = [st for st in states if st["maxDadd"] > 1 + r]
        out[a] = (trapped, adds)
        if verbose:
            print(f"[{label}] a=log p/log n={a}: r={r:.3f}; {len(trapped)} trapped end-states of {len(states)}; "
                  f"{len(adds)} states with a profitable extreme addition")
            for st in trapped[:8]:
                print(f"     TRAP n+={st['nplus']} n-={st['nminus']} minDdel={st['minDdel']:.3f} maxDadd={st['maxDadd']:.3f} x/H={np.round(st['x'],3).tolist()}")
            for st in adds[:4]:
                print(f"     ADD  n+={st['nplus']} n-={st['nminus']} minDdel={st['minDdel']:.3f} maxDadd={st['maxDadd']:.3f}")
    return states, out


if __name__ == "__main__":
    print("kappa_marg = psi/rho_cc; kappa_eff(c) at S0 = psi_c * Schur(R^-1 + diag(s/psi))_cc\n")
    designs = [
        ("indep, r11=.5 r22=.7, truths (4,0)", [[0.5, 0], [0, 0.7]], [4, 0]),
        ("indep, r11=.5 r22=.3, truths (4,0)", [[0.5, 0], [0, 0.3]], [4, 0]),
        ("r12=.3, r11=.5 r22=.7, truths (4,0)", [[0.5, 0.3], [0.3, 0.7]], [4, 0]),
        ("r12=.3, r11=.5 r22=.7, truths (3,1)", [[0.5, 0.3], [0.3, 0.7]], [3, 1]),
        ("r12=.6, r11=.7 r22=.7, truths (1,1)", [[0.7, 0.6], [0.6, 0.7]], [1, 1]),
        ("r12=.69, r11=.7 r22=.7, truths (1,1) near-singular", [[0.7, 0.69], [0.69, 0.7]], [1, 1]),
        ("r12=.69, r11=.7 r22=.7, truths (2,0) near-singular", [[0.7, 0.69], [0.69, 0.7]], [2, 0]),
        ("k=3 G-design truths (2,1,1)", [[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], [2, 1, 1]),
        ("k=3 G-design truths (4,0,0)", [[0.5, 0.2, 0.1], [0.2, 0.6, 0.3], [0.1, 0.3, 0.4]], [4, 0, 0]),
        ("k=3 strong r=.8 within, .5 between, truths (1,1,1)", [[0.8, 0.5, 0.5], [0.5, 0.8, 0.5], [0.5, 0.5, 0.8]], [1, 1, 1]),
        ("k=3 strong r=.8 within, .5 between, truths (3,0,0)", [[0.8, 0.5, 0.5], [0.5, 0.8, 0.5], [0.5, 0.5, 0.8]], [3, 0, 0]),
        ("negative coupling r12=-.4, r=.7, truths (1,1)", [[0.7, -0.4], [-0.4, 0.7]], [1, 1]),
        ("negative coupling r12=-.4, r=.7, truths (2,0)", [[0.7, -0.4], [-0.4, 0.7]], [2, 0]),
    ]
    for lab, R, s in designs:
        R = np.array(R, float); psi = 1 - np.diag(R)
        Rinv = np.linalg.inv(R)
        keff = []
        for c in range(len(psi)):
            Q = Rinv + np.diag(np.array(s) / psi); Q[c, c] = Rinv[c, c]
            idx = [d for d in range(len(psi)) if d != c]
            keff.append(psi[c] * (Q[c, c] - Q[c, idx] @ np.linalg.solve(Q[np.ix_(idx, idx)], Q[idx, c])))
        print(f"=== {lab}: kappa_marg={np.round(psi/np.diag(R),3).tolist()} kappa_eff@S0={np.round(keff,3).tolist()}")
        analyse(R, psi, s, label=lab)
        print()
