"""
COUNTEREXAMPLE to the uniform one-round exit input of H24 (T21 route (e) / T24(i)) in correlated designs.

For each design, search R_d (d = 1, 2; U subset S0 arbitrary) for the state Y maximising the exact
first-change exit probability (Lemma P with 'success' := exit from R_d), then estimate the actual one-round
exit probability P_Y(first exit from R_d during one round) by simulating the actual round (exact scores).
Prints (L+4) * max_Y P_Y(exit) which H24 requires to tend to 0.
Fixed seeds: design seed 1, simulation seed 7.
"""
import math, sys, json
import numpy as np
from bvs_engine import *
from round_analysis import label_laws, GL_T, GL_W
from simulate import simulate


def exit_pstar(M, x, inR):
    """exact P(first state change in the round is an exit from R) at x (lower bound for P_x(exit))."""
    laws = label_laws(M, x)
    s, q = [], []
    for typ, j, law in laws:
        se = sum(pr for dst, pr in law if dst != x and not inR[dst])
        qe = sum(pr for dst, pr in law if dst != x)
        s.append(se); q.append(qe)
    a = M.ind_accept_vector(x); a[x] = 0
    s.append(a[~inR].sum()); q.append(a.sum())
    s = np.array(s); q = np.clip(np.array(q), 0, 1)
    tot = 0.0
    for e in np.nonzero(s > 1e-12)[0]:
        qq = np.delete(q, e)
        tot += s[e] * (GL_W @ np.prod(1 - GL_T[:, None] * qq[None, :], axis=1))
    return tot


def main():
    out = []
    rng = np.random.default_rng(7)
    for scen in [1, 2, 3, 4, 5, 6]:
        for c in [1.0, 0.5]:
            X, y, S0, b = gen_design(scen, p=20, n=200, c=c, seed=1)
            M = Model(X, y, S0)
            for d in [1, 2]:
                inR, V, miss, extra = region_arrays(M, d, M.p)
                # candidates: boundary states with |P| = d and >= 1 missing truth (fast screen by Gibbs only)
                cand = np.nonzero(inR & (extra == d) & (miss >= 1))[0]
                best, bx = -1, None
                # screen: max over null Gibbs labels of addition probability
                scr = []
                for x in cand:
                    x = int(x)
                    mx = 0.0
                    for l in range(M.p):
                        if not (S0 >> l & 1) and not (x >> l & 1):
                            law = M.gibbs_law(x, l)
                            mx = max(mx, law[0][1])
                    scr.append(mx)
                scr = np.array(scr)
                top = cand[np.argsort(-scr)[:40]]
                for x in top:
                    v = exit_pstar(M, int(x), inR)
                    if v > best:
                        best, bx = v, int(x)
                r = simulate(M, np.full(20000, bx, dtype=np.int64), 1, 20000, rng, inR, V)
                pexit = float(r['exit'][0].mean())
                L = max(4, math.ceil(math.log2(M.n + 1)))
                rec = dict(scen=scen, c=c, d=d, Y=[j for j in range(M.p) if bx >> j & 1],
                           S0=[j for j in range(M.p) if S0 >> j & 1], exit_pstar=best, exit_sim=pexit,
                           se=math.sqrt(pexit * (1 - pexit) / 20000), Lplus4_times=(L + 4) * pexit)
                out.append(rec)
                print(rec, flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1)


if __name__ == '__main__':
    main()
