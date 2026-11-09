r"""tv_cert_exact.py -- EXACT (rational) block-visibility certificates (R05 item 1, R04).

S5 population: Sigma = lam^2 11' + Psi, lam^2 = rho = 3/10, Psi = b H + d I (b = 2/5, d = 3/10), groups of 5,
one truth per truth group.  For truth j (coefficient theta_j) and conditioning set U (j not in U), with
U0 := U ∩ g(j) (nulls of j's group, u0 = |U0|), and for every group g with U_g := U ∩ g (u_g = |U_g|):
  s_g := lam^2 u_g/(d + u_g b),  t_g/lam := (d Th_{U_g} + u_g b Th_g)/(d + u_g b),
  (Th_g = theta of the truth of g or 0; Th_{U_g} = theta of that truth if it is in U, else 0),
  s := sum_g s_g, t/lam := sum_g t_g/lam (own group included, Th_{U0} = 0, Th_{g(j)} = theta_j),
  lt := d/(d + u0 b)  (so lambda-tilde = lam*lt),  psi := d(d + (u0+1)b)/(d + u0 b),  eta := theta_j * psi,
  Sigma_{j mu|U} = lam^2 * lt * (Theta - t/lam)/(1 + s) + eta,   Sigma_{jj|U} = psi + lam^2 lt^2/(1 + s),
  tau(U, j) = Sigma_{j mu|U}^2 / Sigma_{jj|U}   -- all rational.
(Derivation: lemmas/L5_random_instances.md, Lemma TVF; it is the closed form of the population partial covariance
for a one-factor + block-diagonal Sigma.)  Cross-check of the closed form against direct float linear algebra on
random configurations (selftest), then exact enumeration with fractions.Fraction over exactly the configurations of
tv_cert.py (blocks = g(j) plus up to two other groups: null groups or other truth groups; within groups by counts).
Also (GC-CS) for compound symmetry, exactly, with the R05 item 3 feasibility restriction u <= |V| + (p - s0)
(here p -> infinity, so u ranges over |V|..15).
-> TV_cert_exact_out.txt"""
import itertools
from fractions import Fraction as Fr
import numpy as np
import tv_cert as tc

RHO, B, D = Fr(3, 10), Fr(2, 5), Fr(3, 10)
PAT = [Fr(7, 5), Fr(-1), Fr(9, 5), Fr(-6, 5), Fr(4, 5), Fr(-8, 5)]


def tau_closed(theta_j, Theta, u0, groups_cfg, rho=RHO, b=B, d=D, F=Fr):
    """groups_cfg: list of (u_g, Th_g, Th_Ug) for groups other than g(j)."""
    s = rho * u0 / (d + u0 * b)
    t = (u0 * b * theta_j) / (d + u0 * b)
    for (ug, Thg, ThU) in groups_cfg:
        if ug == 0:
            continue
        s += rho * ug / (d + ug * b)
        t += (d * ThU + ug * b * Thg) / (d + ug * b)
    lt = d / (d + u0 * b)
    psi = d * (d + (u0 + 1) * b) / (d + u0 * b)
    eta = theta_j * psi
    num = rho * lt * (Theta - t) / (1 + s) + eta
    den = psi + rho * lt * lt / (1 + s)
    return num * num / den


def selftest(rng=np.random.default_rng(3)):
    # random S5 configurations: compare closed form (floats) to direct tau of tv_cert
    act, beta = tc.study_truth(14, 7)
    G = int(act.max() // 5) + 3; p = 5 * G
    Sig = tc.s5_sigma(p); th = np.zeros(p); th[act] = beta
    Theta = float(beta.sum())
    tg = {int(a // 5): (int(a), float(bb)) for a, bb in zip(act, beta)}
    err = 0.0
    for _ in range(3000):
        j = int(rng.choice(act)); gj = j // 5
        U = []
        u0 = int(rng.integers(0, 5)); U += [i for i in range(5 * gj, 5 * gj + 5) if i != j][:u0]
        cfg = []
        for g in rng.choice([g for g in range(G) if g != gj], size=int(rng.integers(0, 4)), replace=False):
            g = int(g); mem = list(range(5 * g, 5 * g + 5))
            if g in tg:
                ti, tb = tg[g]; tin = bool(rng.integers(0, 2)); nn = int(rng.integers(0, 5))
                Ug = ([ti] if tin else []) + [i for i in mem if i != ti][:nn]
                cfg.append((len(Ug), tb, tb if tin else 0.0))
            else:
                nn = int(rng.integers(0, 6)); Ug = mem[:nn]; cfg.append((nn, 0.0, 0.0))
            U += Ug
        t1 = tc.tau(Sig, th, j, U)
        t2 = tau_closed(float(th[j]), Theta, u0, cfg, 0.3, 0.4, 0.3, float)
        err = max(err, abs(t1 - t2))
    return err


def cert_s5_exact(s0, step):
    act, _ = tc.study_truth(s0, step)
    beta = [PAT[i % 6] for i in range(s0)]
    Theta = sum(beta)
    tgroups = [int(a // 5) for a in act]
    best = None; cnt = 0
    for jj in range(s0):
        thj = beta[jj]
        others = [i for i in range(s0) if i != jj]
        # other-group choices: () ; one truth group; null; two truth groups; truth+null; null+null
        choices = [()] + [(("T", i),) for i in others] + [(("N",),)] + [(("T", i), ("T", k)) for i, k in itertools.combinations(others, 2)] \
                  + [(("T", i), ("N",)) for i in others] + [(("N",), ("N",))]
        for ch in choices:
            per = []
            for gdesc in ch:
                if gdesc[0] == "T":
                    tb = beta[gdesc[1]]
                    per.append([(int(tin) + nn, tb, tb if tin else Fr(0)) for tin in (False, True) for nn in range(0, 5)])
                else:
                    per.append([(nn, Fr(0), Fr(0)) for nn in range(0, 6)])
            for u0 in range(0, 5):
                for combo in (itertools.product(*per) if per else [()]):
                    if u0 + sum(c[0] for c in combo) > 15:
                        continue
                    t = tau_closed(thj, Theta, u0, list(combo)); cnt += 1
                    if best is None or t < best[0]:
                        best = (t, jj, u0, combo)
    return best, cnt


def cert_cs_exact(a, s0):
    beta = [PAT[i % 6] for i in range(s0)]
    Th = sum(beta); worst = None
    for jj in range(s0):
        rest = [i for i in range(s0) if i != jj]
        for r in range(len(rest) + 1):
            for V in itertools.combinations(rest, r):
                ThV = sum(beta[i] for i in V)
                for u in range(r, 16):
                    v = abs(beta[jj] + a * (Th - ThV) / (1 - a + a * u))
                    if worst is None or v < worst:
                        worst = v
    return worst


if __name__ == "__main__":
    out = ["closed form vs direct float computation (3000 random S5 configurations): max |diff| = %.3e" % selftest()]
    for s0, step in ((4, 5), (14, 7), (14, 13)):
        (t, jj, u0, combo), cnt = cert_s5_exact(s0, step)
        out.append("S5 layout s0=%d step=%d: %d configurations; exact min tau = %s = %.8f (unit scale c=1; truth #%d, u0=%d, other groups %s)"
                   % (s0, step, cnt, t, float(t), jj, u0, [(c[0], str(c[1]), str(c[2])) for c in combo]))
    for a in (Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(7, 10), Fr(9, 10)):
        for s0 in (4, 14):
            w = cert_cs_exact(a, s0)
            out.append("CS a=%s s0=%d (study pattern): exact min |theta_j + a(Theta-Theta_V)/(1-a+au)| = %s = %.6f" % (a, s0, w, float(w)))
    txt = "\n".join(out); print(txt)
    open("TV_cert_exact_out.txt", "w").write(txt + "\n")
