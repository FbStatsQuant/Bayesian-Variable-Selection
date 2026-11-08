"""N5: population lattice margins (PROOF s8.3, Lemma Lambda(c), (L) margin c5).  Exact population computations, no sampling noise."""
import itertools
import numpy as np
from lhcommon import *

out = Tee("n5_margins.txt")
out("N5 n5_margins.py -- population lattice margins c2, c5 and the closed forms of Lemma Lambda(c)")


class Setting:
    def __init__(self, c, v, g, rho, psi, beta, bvis):
        self.c, self.v, self.g, self.rho, self.psi, self.beta, self.bvis = c, v, g, rho, np.array(psi), np.array(beta), np.array(bvis)
        self.p = (2 * c + v) * g
        self.Sigma = build_sigma(self.p, g, c, rho, self.psi)
        self.theta = build_theta(self.p, g, c, v, self.psi, self.beta, self.bvis)
        self.w = self.Sigma @ self.theta
        self.tt = float(self.theta @ self.w)
        self.lam0 = np.linalg.eigvalsh(self.Sigma)[0]
        self.G = self.psi**2 * self.beta**2 * (1 - self.psi**2)
        self.eta = rho**2 * (1 - self.psi**2) / (1 - self.psi**2 * rho**2)
        self.ja = [2 * i * g for i in range(c)]
        self.jb = [(2 * i + 1) * g for i in range(c)]
        self.jv = [(2 * c + h) * g for h in range(v)]
        self.V = list(range(self.p))

    def lam(self, B):
        B = sorted(set(B))
        if not B:
            return self.tt
        Sb = self.Sigma[np.ix_(B, B)]
        wb = self.w[B]
        return self.tt - float(wb @ np.linalg.solve(Sb, wb))

    def lam_comp(self, i, B):
        """Var(mu_i | x_B), B subset of K_i (population)."""
        g = self.g
        K = list(range(2 * i * g, (2 * i + 2) * g))
        th = np.zeros(self.p)
        th[self.ja[i]] = self.beta[i]
        th[self.jb[i]] = -self.psi[i] * self.beta[i]
        S = self.Sigma
        tot = float(th @ S @ th)
        B = sorted(set(B))
        if not B:
            return tot
        wb = (S @ th)[B]
        return tot - float(wb @ np.linalg.solve(S[np.ix_(B, B)], wb))

    def var_vis(self, h, B):
        """Var(x_{j_h} | x_B) for B subset of V_h."""
        S = self.Sigma
        j = self.jv[h]
        B = sorted(set(B))
        if not B:
            return S[j, j]
        return float(S[j, j] - S[j, B] @ np.linalg.solve(S[np.ix_(B, B)], S[B, j]))

    def constants(self):
        c, v = self.c, self.v
        Gmin, etamax = self.G.min(), self.eta.max()
        b2 = self.beta**2
        omp = 1 - self.psi**2
        vis_min = (self.bvis**2).min() if v else np.inf
        c4 = min((b2 * omp**2).min(), (b2 * omp).min(), Gmin, vis_min)
        c2 = min(Gmin, Gmin * (1 - etamax), c4, (b2 * omp**2).min(), (self.lam0 * b2).min(),
                 (self.bvis**2 * (1 - self.rho**2)).min() if v else np.inf)
        c5 = min((b2 * omp).min(), Gmin, vis_min, Gmin * (1 - etamax), (self.lam0 * b2).min(),
                 (self.bvis**2 * (1 - self.rho**2)).min() if v else np.inf)
        return c2, c4, c5


def analyse(st):
    """Returns dict with min margins and closed-form deviations."""
    c, g = st.c, st.g
    res = dict(margin_min=np.inf, margin_arg=None, cat_min={}, claim_dev=0.0)
    Sdeg = st.ja + st.jv
    # lattice states
    for r in range(c):          # |M'| = r < c
        for Mp in itertools.combinations(range(c), r):
            S = Sdeg + [st.jb[i] for i in Mp]
            I = [i for i in range(c) if i not in Mp]
            istar = max(I, key=lambda i: st.G[i])
            Pstar = S + [st.jb[istar]]
            lP = st.lam(Pstar)
            lS = st.lam(S)
            # sanity: lambda(S) = sum_{i in I} G_i ; lambda(P*) = lambda(S) - G_i*
            res["claim_dev"] = max(res["claim_dev"], abs(lS - st.G[I].sum()), abs(lP - (lS - st.G[istar])))
            prog = set(st.jb[i] for i in I)

            def reg(cat, A, tag):
                m = st.lam(A) - lP
                if m < res["cat_min"].get(cat, (np.inf,))[0]:
                    res["cat_min"][cat] = (m, tag)
                if m < res["margin_min"]:
                    res["margin_min"], res["margin_arg"] = m, (cat, tag, S)
            reg("A=S", S, "stay")
            for l in st.V:
                if l in S:
                    continue
                if l in prog:
                    continue            # progress neighbour, excluded
                comp = l // g
                cat = "add-proxy(i in I)" if (comp % 2 == 1 and comp < 2 * c and (comp // 2) in I) else "add-other"
                reg(cat, S + [l], ("add", l))
                if cat == "add-proxy(i in I)":
                    i = comp // 2
                    res["claim_dev"] = max(res["claim_dev"], abs(st.lam(S + [l]) - (lS - st.G[i] * st.eta[i])))
            for k in S:
                A = [x for x in S if x != k]
                reg("delete", A, ("del", k))
                # claimed rises
                if k in st.ja:
                    i = st.ja.index(k)
                    claim = st.beta[i]**2 * (1 - st.psi[i]**2)**2 if i in I else st.beta[i]**2 * (1 - st.psi[i]**2)
                elif k in st.jb:
                    claim = st.G[st.jb.index(k)]
                else:
                    claim = st.bvis[st.jv.index(k)]**2
                res["claim_dev"] = max(res["claim_dev"], abs((st.lam(A) - lS) - claim))
                for l in st.V:
                    if l in S:
                        continue
                    same = (l // g) // 2 == (k // g) // 2 if (k // g < 2 * c and l // g < 2 * c) else ((l // g) == (k // g))
                    reg("swap-same-component" if same else "swap-diff-component", A + [l], ("swap", k, l))
    return res


def c5_check(st):
    """(L): min over deletions and swaps A of S0 of lambda(A)."""
    c, g = st.c, st.g
    S0 = st.ja + st.jb + st.jv
    best, arg = np.inf, None
    for k in S0:
        A = [x for x in S0 if x != k]
        m = st.lam(A)
        if m < best:
            best, arg = m, ("del", k)
        for l in st.V:
            if l in S0:
                continue
            m = st.lam(A + [l])
            if m < best:
                best, arg = m, ("swap", k, l)
    addmax = max(abs(st.lam(S0 + [l])) for l in st.V if l not in S0)
    return best, arg, addmax, abs(st.lam(S0))


def closed_forms(st):
    """Lemma Lambda(c), lines 312-314; returns max abs deviation of equalities and min slack of the inequality."""
    g = st.g
    dev, slack = 0.0, np.inf
    for i in range(st.c):
        ja, jb = st.ja[i], st.jb[i]
        Ca = [x for x in range(2 * i * g, (2 * i + 1) * g) if x != ja]
        Cb = [x for x in range((2 * i + 1) * g, (2 * i + 2) * g) if x != jb]
        b2, ps, G, eta = st.beta[i]**2, st.psi[i], st.G[i], st.eta[i]
        dev = max(dev, abs(st.lam_comp(i, []) - b2 * (1 - ps**2)), abs(st.lam_comp(i, [jb]) - b2 * (1 - ps**2)),
                  abs(st.lam_comp(i, [ja]) - G), abs(st.lam_comp(i, [ja, jb])))
        for l in Ca:
            dev = max(dev, abs(st.lam_comp(i, [ja, l]) - G))
        for l in Cb:
            dev = max(dev, abs(st.lam_comp(i, [ja, l]) - G * (1 - eta)))
        K = list(range(2 * i * g, (2 * i + 2) * g))
        for r in (0, 1, 2):
            for B in itertools.combinations(K, r):
                if ja in B:
                    continue
                lb = st.lam0 * b2 * (1 + ps**2 * (jb not in B))
                slack = min(slack, st.lam_comp(i, list(B)) - lb)
    for h in range(st.v):
        Vh = list(range(st.jv[h], st.jv[h] + g))
        dev = max(dev, abs(st.var_vis(h, []) - 1), abs(st.var_vis(h, [st.jv[h]])))
        for l in Vh[1:]:
            dev = max(dev, abs(st.var_vis(h, [l]) - (1 - st.rho**2)))
    # (b) additivity over components, random B
    rng = np.random.default_rng(1)
    for _ in range(20):
        B = sorted(rng.choice(st.p, size=int(rng.integers(0, 7)), replace=False).tolist())
        tot = 0.0
        for i in range(st.c):
            K = set(range(2 * i * g, (2 * i + 2) * g))
            tot += st.lam_comp(i, [x for x in B if x in K])
        for h in range(st.v):
            Vh = set(range(st.jv[h], st.jv[h] + g))
            tot += st.bvis[h]**2 * st.var_vis(h, [x for x in B if x in Vh])
        dev = max(dev, abs(tot - st.lam(B)))
    return dev, slack


def random_setting(rng, extreme=False):
    c = int(rng.choice([1, 2, 3])); v = int(rng.choice([0, 1, 2])); g = int(rng.choice([3, 4, 5]))
    rho = float(rng.uniform(0.3, 0.9))
    if extreme:
        rho = float(rng.choice([0.3, 0.5, 0.9]) + rng.uniform(-0.01, 0.01) * 0)
        psi_abs = rho * rng.uniform(0.9, 0.995, size=c)       # psi pushed to the boundary |psi| -> rho
        beta = rng.choice([-1, 1], size=c) * rng.choice([0.5, 2.0], size=c)
        bvis = rng.choice([-1, 1], size=v) * rng.choice([0.5, 2.0], size=v)
    else:
        psi_abs = rho * rng.uniform(0.02, 0.98, size=c)
        beta = rng.choice([-1, 1], size=c) * rng.uniform(0.5, 2.0, size=c)
        bvis = rng.choice([-1, 1], size=v) * rng.uniform(0.5, 2.0, size=v)
    psi = rng.choice([-1, 1], size=c) * psi_abs
    return Setting(c, v, g, rho, psi, beta, bvis)


for label, extreme in (("RANDOM (40 settings, seed 20260108)", False), ("EXTRA ADVERSARIAL (40 settings: |psi| in (0.9,0.995)*rho, rho in {.3,.5,.9}, |beta| in {.5,2})", True)):
    rng = np.random.default_rng(20260108 + int(extreme))
    out("\n" + "=" * 100)
    out(label)
    rows = []
    for s in range(40):
        st = random_setting(rng, extreme)
        c2, c4, c5 = st.constants()
        res = analyse(st)
        l5, arg5, addmax, lS0 = c5_check(st)
        dev, slack = closed_forms(st)
        f4 = st.lam0 - (1 - np.abs(st.psi).max()) * (1 - st.rho)
        rows.append(dict(s=s, c=st.c, v=st.v, g=st.g, rho=st.rho, psimax=np.abs(st.psi).max(), lam0=st.lam0, f4=f4,
                         c2=c2, c4=c4, c5=c5, mmin=res["margin_min"], arg=res["margin_arg"], cat=res["cat_min"],
                         l5=l5, arg5=arg5, addmax=addmax, lS0=lS0, dev=dev, slack=slack, cdev=res["claim_dev"]))
    out("%2s %2s %2s %2s %5s %6s %7s | %9s %9s %9s | %9s %7s | %9s %7s | %s" %
        ("#", "c", "v", "g", "rho", "psimax", "lam0", "c2", "minMargin", "min/c2", "c5", "L-min", "L-min/c5", "", "category of minimiser"))
    for r in rows:
        out("%2d %2d %2d %2d %5.2f %6.3f %7.4f | %9.5f %9.5f %9.3f | %9.5f %9.5f %7.3f | %s" %
            (r["s"], r["c"], r["v"], r["g"], r["rho"], r["psimax"], r["lam0"], r["c2"], r["mmin"], r["mmin"] / r["c2"], r["c5"], r["l5"],
             r["l5"] / r["c5"], r["arg"][0]))
    v2 = [r for r in rows if r["mmin"] < r["c2"] - 1e-10]
    v5 = [r for r in rows if r["l5"] < r["c5"] - 1e-10]
    out("\nSummary:")
    out("  min over settings of minMargin/c2 = %.4f (>=1 required);  #settings with min margin < c2: %d" % (min(r["mmin"] / r["c2"] for r in rows), len(v2)))
    out("  min over settings of (minMargin - c2) = %.3e ; of (L-min - c5) = %.3e   (negative would be a violation; ~0 means the bound is attained)" % (min(r["mmin"] - r["c2"] for r in rows), min(r["l5"] - r["c5"] for r in rows)))
    out("  #settings where the c2 bound is attained to within 1e-9 (tight): %d of 40;  c5 attained: %d of 40" % (sum(abs(r["mmin"] - r["c2"]) < 1e-9 for r in rows), sum(abs(r["l5"] - r["c5"]) < 1e-9 for r in rows)))
    out("  min over settings of L-min/c5      = %.4f (>=1 required);  #settings with min (L) lambda < c5: %d" % (min(r["l5"] / r["c5"] for r in rows), len(v5)))
    out("  c2 > 0 in all settings: %s; c5 > 0: %s; c4 > 0: %s" % (all(r["c2"] > 0 for r in rows), all(r["c5"] > 0 for r in rows), all(r["c4"] > 0 for r in rows)))
    out("  (F4) lambda_min(Sigma) >= (1-psibar)(1-rho): min slack = %.3e" % min(r["f4"] for r in rows))
    out("  Lemma Lambda(c)/(b) equalities: max abs deviation = %.3e ; inequality lambda_i(B) >= lam0 beta^2 (1+psi^2 1{jb notin B}) min slack = %.3e (>=0 required)" %
        (max(r["dev"] for r in rows), min(r["slack"] for r in rows)))
    out("  s8.3 case-list closed values (lambda(S)=sum G_i, lambda(P*), proxy drop G_i eta_i, deletion rises): max abs deviation = %.3e" % max(r["cdev"] for r in rows))
    out("  lambda(S0)= %.2e (max), lambda(S0 + l) max |.| = %.2e" % (max(r["lS0"] for r in rows), max(r["addmax"] for r in rows)))
    # per-category minimum of margin/c2 across settings
    cats = sorted(set(k for r in rows for k in r["cat"]))
    out("  per-category min of margin / c2 across settings:")
    for k in cats:
        vals = [(r["cat"][k][0] / r["c2"], r["s"], r["cat"][k][1]) for r in rows if k in r["cat"]]
        mn = min(vals)
        out("     %-22s min margin/c2 = %8.3f   (setting %d, move %s)" % (k, mn[0], mn[1], mn[2]))
    if v2:
        for r in v2:
            out("  VIOLATION c2: setting %d margin %.6g < c2 %.6g at %s" % (r["s"], r["mmin"], r["c2"], r["arg"]))
    if v5:
        for r in v5:
            out("  VIOLATION c5: setting %d min %.6g < c5 %.6g at %s" % (r["s"], r["l5"], r["c5"], r["arg5"]))
    out("  VIOLATIONS: " + ("none" if not (v2 or v5) else "see above"))

out("\nDONE")
out.close()
