r"""tv_cert.py -- population block-visibility certificates (TV-pop / TV) for the instances of STATEMENT (I).
S5 (block CS 0.3/0.7, groups of 5): blocks are unions of <= 3 whole groups (lemmas/L5_random_instances.md, Lemma P5);
for every truth j, every block C = g(j) ∪ (up to two other groups: null groups or other truth groups) and every
U ⊆ C \ {j}, compute tau(U,j) := (Sigma_{j mu|U})^2 / Sigma_{j j|U} at unit signal scale (c = 1; tau scales with c^2).
Symmetry reduction (exact): within a null group only |U ∩ g| matters; within truth group i only (i ∈ U?, #nulls of g_i in U);
within g(j) only #nulls.  Layouts: diagnostic (s0=4, step 5) and the study high-p layouts (s0=14, step 7 and 13),
truth positions/coefficients as Theory_work/Wave1/W1-GEN/numerics/study_common.py study_truth().
CS: (GC-CS) minimum over V ⊆ S0\{j}, u in {|V|..15} of |theta_j + a(Theta - Theta_V)/(1-a+a u)| (diagnostic layout and
cycled patterns).  -> TV_cert_out.txt"""
import itertools, math
import numpy as np

POS = (3, 2, 4, 1, 5, 3)
PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)


def study_truth(s0, step):
    k = np.arange(s0)
    block = 1 + step * k
    pos = np.array([POS[i % 6] for i in k])
    return (5 * (block - 1) + pos - 1).astype(int), np.array([PATTERN[i % 6] for i in k])


def s5_sigma(p):
    idx = np.arange(p); grp = idx // 5
    H = (grp[:, None] == grp[None, :]).astype(float)
    return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * np.eye(p)


def tau(Sig, theta, j, U):
    smu = Sig @ theta
    if not U:
        return smu[j] ** 2 / Sig[j, j]
    U = list(U)
    c = np.linalg.solve(Sig[np.ix_(U, U)], Sig[U, j])
    pc = smu[j] - c @ smu[U]
    pv = Sig[j, j] - Sig[j, U] @ c
    return pc ** 2 / pv


def cert_s5(s0, step):
    act, beta = study_truth(s0, step)
    G = int(act.max() // 5) + 3          # include one null group beyond the last truth group
    p = 5 * G
    Sig = s5_sigma(p)
    th = np.zeros(p); th[act] = beta
    tgroups = sorted({int(a // 5) for a in act})
    ngroups = [g for g in range(G) if g not in tgroups]
    nullg = ngroups[0]; nullg2 = ngroups[1]
    worst = (np.inf, None); count = 0
    for j in act:
        gj = int(j // 5)
        others_t = [g for g in tgroups if g != gj]
        choices = [()] + [(g,) for g in others_t + [nullg]] + [tuple(c) for c in itertools.combinations(others_t, 2)] \
                  + [(g, nullg) for g in others_t] + [(nullg, nullg2)]
        mates = [i for i in range(5 * gj, 5 * gj + 5) if i != j]
        for ch in choices:
            # per-group configurations
            grp_cfgs = []
            for g in ch:
                members = list(range(5 * g, 5 * g + 5))
                tr = [i for i in members if th[i] != 0]
                nl = [i for i in members if th[i] == 0]
                cfgs = []
                for ti in ([[]] + ([[tr[0]]] if tr else [])):
                    for m in range(0, len(nl) + 1):
                        cfgs.append(ti + nl[:m])
                grp_cfgs.append(cfgs)
            for m0 in range(0, 5):
                base = mates[:m0]
                for combo in itertools.product(*grp_cfgs) if grp_cfgs else [()]:
                    U = base + [i for part in combo for i in part]
                    if len(U) > 15: continue
                    t = tau(Sig, th, int(j), U); count += 1
                    if t < worst[0]: worst = (t, (int(j), tuple(U)))
    return worst, count


def cert_cs(a, theta_S0):
    s0 = len(theta_S0); Th = float(sum(theta_S0)); worst = np.inf
    for jj in range(s0):
        rest = [i for i in range(s0) if i != jj]
        for r in range(len(rest) + 1):
            for V in itertools.combinations(rest, r):
                ThV = float(sum(theta_S0[i] for i in V))
                for u in range(r, 16):
                    worst = min(worst, abs(theta_S0[jj] + a * (Th - ThV) / (1 - a + a * u)))
    return worst


if __name__ == "__main__":
    out = []
    for s0, step in ((4, 5), (14, 7), (14, 13)):
        (w, arg), cnt = cert_s5(s0, step)
        out.append("S5 layout s0=%d step=%d: configurations %d, min tau(U,j) = %.6f (c=1; scales with c^2) at j=%d, |U|=%d"
                   % (s0, step, cnt, w, arg[0], len(arg[1])))
    for a in (0.1, 0.3, 0.5, 0.7, 0.9):
        for s0, step in ((4, 5), (14, 7)):
            _, beta = study_truth(s0, step)
            out.append("CS a=%.1f layout s0=%d: min |theta_j + a(Theta-Theta_V)/(1-a+au)| = %.6f" % (a, s0, cert_cs(a, list(beta))))
    txt = "\n".join(out); print(txt)
    open("TV_cert_out.txt", "w").write(txt + "\n")
