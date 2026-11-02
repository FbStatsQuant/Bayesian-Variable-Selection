"""PHIR (referee): W1's 'What is weakest' paragraph claims that among statements that keep the move count <= Phi,
TD'_P is necessary and sufficient. A4 proves necessity only for 'every greedy move decreases Phi'. Here we test
the stronger claim empirically: PHI-REACH(R) := every uncapped greedy path from every S in R ends at S0 within
Phi(S) moves. Does PHI-REACH(R_{3,2}) ever hold while TD'_P(R_{3,2}) fails?
Same designs/seeds as exhaust_theoremA.py (n in {40, 80}, c in {0.25, 0.5, 1}, S1-S6), reps given on the command line.
"""
import sys
from vt_core import Model, region, phi
from conditions import TDP
from exhaust_theoremA import data


def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    tot = both = phir_only = tdp_only = 0; examples = []
    for s in range(1, 7):
        for n in (40, 80):
            for c in (0.25, 0.5, 1.0):
                for rep in range(reps):
                    seed = 31_000_000 + 100000 * s + 1000 * n + 100 * int(4 * c) + rep
                    X, y, S0 = data(s, n, c, seed); M = Model(X, y)
                    R = region(S0, [j for j in range(M.p) if j not in S0], 3, 2)
                    ok = True; bad = None
                    for S in R:
                        P = M.greedy_uncapped(S)
                        if P[-1] != S0 or len(P) - 1 > phi(S, S0):
                            ok = False; break
                        if any(phi(P[i + 1], S0) >= phi(P[i], S0) for i in range(len(P) - 1)) and bad is None:
                            bad = (S, P)
                    t = not TDP(M, S0, R)
                    tot += 1; both += ok and t; phir_only += ok and not t; tdp_only += t and not ok
                    if ok and not t and len(examples) < 3: examples.append((s, n, c, rep, bad))
    print('datasets', tot, ' PHI-REACH & TDP', both, ' PHI-REACH only', phir_only, ' TDP only', tdp_only)
    print('examples (scen, n, c, rep, (S, path with a non-progress move)):', examples)


if __name__ == '__main__':
    main()
