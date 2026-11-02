"""C2N (referee): test the noise-variance inequality used in W1's sketch of Theorem C(C2):
   (I)  ||(P_{S'} - P_{S''}) mu||^2 <= C (n-1) (|Delta_{S'} - Delta_S| + |Delta_{S''} - Delta_S|)   for neighbours S', S'' of S
   (II) ... <= C (n-1) R+(S).
and the repaired bound proposed in the referee report:
   (III) ||(P_A - P_B) mu||^2 <= 2 (n-1) [(Delta_A - Delta_{AuB}) + (Delta_B - Delta_{AuB})]   (always true)
   (IV)  with A = pi(S) (best progress neighbour) and B any neighbour:
         ||(P_A - P_B) mu||^2 <= (n-1) [ c1 R+(S) + 2 (Delta_B - Delta_S)_+ ],  c1 = 2 + 2 s0^2/phi^4 ... we report the
         empirical max of ||(P_A-P_B)mu||^2/(n-1) - 2 (Delta_B - Delta_S)_+ over R+(S), and of the ratio in (I) and (II).
Population computation in R^p (columns = Cholesky factor, Gram = (n-1) * Rcorr with n - 1 := 1).
Random designs: p = 7, S0 = {0,1,2}, equicorrelated blocks / random correlation, theta random; seed 777.
"""
import itertools, numpy as np


def proj(Xc, T):
    if not T: return np.zeros((Xc.shape[0], Xc.shape[0]))
    A = Xc[:, list(T)]; return A @ np.linalg.pinv(A)


def nbrs(S, p):
    S = tuple(sorted(S)); out = []
    for j in range(p):
        out.append(tuple(x for x in S if x != j) if j in S else tuple(sorted(S + (j,))))
    for i in S:
        for l in range(p):
            if l not in S: out.append(tuple(sorted(tuple(x for x in S if x != i) + (l,))))
    return out


def main():
    rng = np.random.default_rng(777)
    p, S0 = 7, (0, 1, 2)
    worst = dict(I=0, II=0, III=0, IV=0, IV_phi=None)
    exI = None
    for trial in range(400):
        A = rng.standard_normal((p, p)) * rng.uniform(0.2, 1.5)
        C = A @ A.T + np.diag(rng.uniform(0.05, 1, p)); d = np.sqrt(np.diag(C)); Rc = C / np.outer(d, d)
        Xc = np.linalg.cholesky(Rc).T          # columns x_j, ||x_j|| = 1
        th = np.zeros(p); th[list(S0)] = rng.choice([-1, 1], 3) * rng.uniform(0.05, 2, 3)
        mu = Xc @ th
        Dl = lambda T: float(mu @ (np.eye(p) - proj(Xc, T)) @ mu)
        phi = lambda T: len(set(S0) ^ set(T))
        lam = np.linalg.eigvalsh(Rc[np.ix_(range(p), range(p))]).min()
        for k in range(0, 4):
            for S in itertools.combinations(range(p), k):
                if set(S0) <= set(S): continue
                nb = nbrs(S, p); DS = Dl(S)
                prog = [T for T in nb if phi(T) < phi(S)]
                Api = min(prog, key=Dl); Rp = DS - Dl(Api)
                if Rp <= 1e-9: continue
                for B in nb:
                    for Ap in (Api,):
                        v = mu @ (proj(Xc, Ap) - proj(Xc, B)); v = float(v @ v)
                        den = abs(Dl(Ap) - DS) + abs(Dl(B) - DS)
                        if den > 1e-12 and v / den > worst['I']:
                            worst['I'] = v / den
                        worst['II'] = max(worst['II'], v / Rp)
                        U = tuple(sorted(set(Ap) | set(B)))
                        r3 = v / max(1e-15, 2 * (Dl(Ap) - Dl(U) + Dl(B) - Dl(U)))
                        worst['III'] = max(worst['III'], r3)
                        r4 = (v - 2 * max(0.0, Dl(B) - DS)) / Rp
                        if r4 > worst['IV']:
                            worst['IV'] = r4; worst['IV_phi'] = (round(lam, 4), S, Api, B)
                # the explicit pair of the report: S' = add a missing truth, S'' = truth->truth swap
    print("max ratio in (I) with S' = pi(S):", round(worst['I'], 3))
    print("max ratio in (II) ||(P_pi - P_B)mu||^2 / R+(S):", round(worst['II'], 3), "(unbounded => (II) false)")
    print("max ratio in (III) (must be <= 1):", round(worst['III'], 6))
    print("max of [||(P_pi-P_B)mu||^2 - 2(Delta_B-Delta_S)_+] / R+:", round(worst['IV'], 3), " at (lambda_min(R), S, pi, B) =", worst['IV_phi'])
    # explicit orthogonal example for (I) with a general pair
    p = 4; Xc = np.eye(p); th = np.array([1.0, 1.0, 0.1, 0]); mu = Xc @ th
    Dl = lambda T: float(mu @ (np.eye(p) - proj(Xc, T)) @ mu)
    S, Sp, Spp = (0,), (0, 2), (1,)
    v = mu @ (proj(Xc, Sp) - proj(Xc, Spp)); v = float(v @ v)
    print("orthogonal example S={x1}, S'=S+x3, S''=swap x1->x2, theta=(1,1,0.1): ||(P_S'-P_S'')mu||^2 = %.3f,"
          " |dDelta'|+|dDelta''| = %.3f  (ratio %.0f)" % (v, abs(Dl(Sp) - Dl(S)) + abs(Dl(Spp) - Dl(S)), v / (abs(Dl(Sp) - Dl(S)) + abs(Dl(Spp) - Dl(S)))))
    S, Spp = (0,), ()
    th2 = np.array([3.0, 0.2, 0.0, 0.0]); mu = Xc @ th2
    Dl = lambda T: float(mu @ (np.eye(p) - proj(Xc, T)) @ mu)
    print("(II) example S0={x1,x2}, theta=(3,0.2), S={x1}: R+ = %.3f, |Delta_{S-x1} - Delta_S| = %.3f" % (Dl(S) - Dl((0, 1)), abs(Dl(()) - Dl(S))))


if __name__ == "__main__":
    main()
