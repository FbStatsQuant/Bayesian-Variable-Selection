"""CEX-2 (referee): W1 Lemma 0(b) says the search can deliver S0 only on E_LS = {F(S0) > F(S_c)} (correct), and then
'in particular on every posterior miss F(S0) <= F(S-hat) it cannot'. The 'in particular' treats a posterior miss
(measured AFTER the search, against the final HPM) as if it implied the complement of E_LS (measured BEFORE the
search, against the centre). It does not: here F(S_c) < F(S0) < F(S0 + l), the search climbs S_c -> S0 + l and
stops, the fit ends as a posterior miss, and yet E_LS held. So the remark 'the 0/541 repair count is forced by
monotonicity' needs the data fact F(S0) <= F(S_c) (or 'the final local search did not improve the HPM') for those
fits; the posterior-miss classification alone does not give it.

Deterministic construction: orthonormal centred columns scaled to sqrt(n-1); truths x1, x2 (theta = 0.5 each),
null x3 = e3, q further pure nulls; eps = sigma sqrt(n-1) (alpha e3 + sqrt(1-alpha^2) e_last), alpha = 0.45:
the noise leaks into the null x3, so S0 + {3} beats S0. Centre S_c = {x1, x3} = S0 - x2 + x3 (in R_1).
"""
import itertools, numpy as np
from vt_core import Model, standardise


def build(n=100, q=6, th=0.5, sigma=1.0, alpha=0.45, seed=3):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((n, q + 4)); Z -= Z.mean(0)
    E, _ = np.linalg.qr(Z); E *= np.sqrt(n - 1)
    X = E[:, :q + 3]
    y = th * (E[:, 0] + E[:, 1]) + sigma * (alpha * E[:, 2] + np.sqrt(1 - alpha ** 2) * E[:, q + 3])
    return standardise(X, y)


def main():
    X, y = build(); M = Model(X, y)
    S0 = (0, 1); Sc = (0, 2)
    print("F(Sc) - F(S0) = %.3f  (E_LS: F(S0) > F(Sc) is %s)" % (M.F(Sc) - M.F(S0), M.F(S0) > M.F(Sc)))
    print("F(S0+x3) - F(S0) = %.3f" % (M.F((0, 1, 2)) - M.F(S0)))
    out = M.local_search(Sc)
    print("local search from Sc:", out)
    Shat = out['returned']
    print("returned == S0:", Shat == S0, "; posterior miss F(S0) <= F(Shat):", M.F(S0) <= M.F(Shat))
    allS = [S for k in range(M.p + 1) for S in itertools.combinations(range(M.p), k)]
    F = M.Fset(allS)
    print("global HPM:", allS[int(np.argmax(F))])


if __name__ == "__main__":
    main()
