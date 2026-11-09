# R20: the uniform-in-n-frak bulk addition margin (X4.4 Remark) as an obstruction separate from the band term.
# At T_0 = [p] minus n-frak (n-frak = 15 largest positive null xi), exact production gain of re-adding l in n-frak,
# compared with the heuristic log p - 1/2 log n + 1/2 xi_l^2 - log p  (i.e. 1/2 xi_max^2 - 1/2 log n).
import sys, math, json, numpy as np
sys.path.insert(0, r"../../numerics")
import iid_core as ic
def run(n, p, rho, seed):
    rng = np.random.default_rng(seed)
    beta = np.zeros(p); S0 = [0]; beta[0] = 1.0
    P = ic.IidData(np.full(p, math.sqrt(rho)), beta, n, rng)
    xi = P.A[2:, 0]
    nulls = [j for j in range(1, p)]
    nn = sorted(nulls, key=lambda j: -xi[j])[:15]
    T = [j for j in range(p) if j not in nn]
    st = ic.PathState(P, T); Gd, Ga, Gs, psi = st.gains(with_swaps=False)
    return dict(n=n, p=p, logratio=round(math.log(p)/math.log(n), 3), max_add=round(float(Ga.max()), 3),
                best_del=round(float(Gd.max()), 3), half_xi2_minus_half_logn=round(0.5*max(xi[nn])**2 - 0.5*math.log(n), 3))
if __name__ == "__main__":
    for (n, p) in [(10**4, 50), (10**4, 300), (10**4, 1500), (10**5, 300), (10**5, 1500), (10**5, 3000)]:
        for seed in (1, 2):
            print(json.dumps(run(n, p, 0.5, seed))); sys.stdout.flush()
