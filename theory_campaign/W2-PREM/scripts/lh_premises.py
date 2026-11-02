"""Theorem B premises on the linked-hub family LH (W1-EXP Thm 5), exact computation (W2-PREM §§4-7).

LH configuration B of W1-EXP: p = 20, five groups of g = 4 (equicorrelation rho = 0.7), hubs 0,4,8,12,16;
linked pairs (0,4) and (8,12) with psi = 0.5 (rank-one link through the hubs); theta_0 = 1.4, theta_4 = -0.7,
theta_8 = 1.8, theta_12 = -0.9; group 16..19 null; sigma = 1; exact Gram X'X = (n-1) Sigma.
Blocks = groups (W1-EXP Lemma 4.2: g <= B = 4 < 2g, |psi| < rho).  S0 = {0,4,8,12}; masked set M = {4,12};
reference S° = {0,8}; start x = S°.

Two repair families (both with V = |M(W)| + a in phase 1, |P(W)| in phase 2):
  W1 : [B]'s Z(x): U u P u Q, x n S0 <= U <= S0, P <= A_nb, Q <= J, |Q| <= c,   A_nb = U_{j in M(x)} N(j) \\ S0
       (N = the method's neighbour graph, threshold sqrt(2 log p / n), top-B, symmetric union).
  SH : Z#(x) of PROOF.md §5: U u E, x n S0 <= U <= S0, |E \\ A(M(W))| <= c + |A(M(x)) \\ A(M(W))|,
       with the useful-look-alike map A_LH(M') = U_{j_b in M'} (C_b \\ {j_b}).
Phase 2 family: S_a = {S0 u P : |P| <= a}, a = |A(M(x))| + c.

Per family and n (3 replicates each): exact per-label bad probabilities, Theorem B's constants
(eta1, eta2, eps_add, eps_pt, eps_del, H_a, c_*, bound with H' = L+5, v = V(x)), the independence-move bound
beta_I(W) <= (1 - pi0(S°)) + 1{S° bad at W} min(1, e^{d(S°)-d(W)}), and the W1-family counterexample state
W* = S° + {1} (1 is a group-mate of the *present* hub 0, hence useless).  Population (n-free) design checks:
TS, few-substitutes (FS), useful-look-alike retention (ULR), subset gain GS(S°).
Output: results/lh_premises.txt (+ .json).  Fixed seeds.
"""
import json
import sys
import numpy as np
from math import log, sqrt, comb
from itertools import combinations
from bvs_score import Data

p, g, rho, psi = 20, 4, 0.7, 0.5
B = 4
groups = [list(range(4 * h, 4 * h + 4)) for h in range(5)]
hubs = [0, 4, 8, 12, 16]
pairs = [(0, 4), (8, 12)]
S0 = frozenset([0, 4, 8, 12])
Sref = frozenset([0, 8])
Mx = frozenset([4, 12])
NULLS = [j for j in range(p) if j not in S0]


def lh_sigma():
    S = np.zeros((p, p))
    for G in groups:
        for a in G:
            for b in G:
                S[a, b] = 1.0 if a == b else rho
    for ha, hb in pairs:
        Ca, Cb = groups[ha // 4], groups[hb // 4]
        for k in Ca:
            for l in Cb:
                v = psi * (1.0 if k == ha else rho) * (1.0 if l == hb else rho)
                S[k, l] = S[l, k] = v
    return S


SIG = lh_sigma()
TH = np.zeros(p)
TH[[0, 4, 8, 12]] = [1.4, -0.7, 1.8, -0.9]


def neighbour_graph(n):
    R = SIG
    thr = sqrt(2 * log(p) / n)
    part = []
    for j in range(p):
        cand = [(-abs(R[j, l]), l) for l in range(p) if l != j]
        cand.sort()
        keep = [l for (v, l) in cand if -v > thr]
        if not keep:
            keep = [cand[0][1]]
        if cand[0][1] not in keep:
            keep = [cand[0][1]] + keep
        part.append(set(keep[:B]))
    N = [set() for _ in range(p)]
    for j in range(p):
        for l in part[j]:
            N[j].add(l)
            N[l].add(j)
    return N


def A_LH(Mset):
    out = set()
    for (ha, hb) in pairs:
        if hb in Mset:
            out |= set(groups[hb // 4]) - {hb}
    return frozenset(out)


class Fam:
    def __init__(self, kind, N, x):
        self.kind, self.N, self.x = kind, N, frozenset(x)
        self.xS = self.x & S0
        Mxx = S0 - self.x
        if kind == "W1":
            self.A = frozenset().union(*[N[j] for j in Mxx]) - S0
            self.c = len((self.x - S0) - self.A)
            self.a = len(self.A) + self.c
        else:
            self.Ax = A_LH(Mxx)
            self.c = len((self.x - S0) - self.Ax)
            self.a = len(self.Ax) + self.c

    def member(self, W):
        if not self.xS <= W:
            return False
        E = W - S0
        M = S0 - W
        if not M:
            return len(E) <= self.a
        if self.kind == "W1":
            return E - self.A <= E and len(E - self.A) <= self.c
        AW = A_LH(M)
        return len(E - AW) <= self.c + len(self.Ax - AW)

    def V(self, W):
        M = S0 - W
        return len(M) + self.a if M else len(W - S0)

    def states(self):
        out = []
        for r in range(0, len(NULLS) + 1):
            if r > self.a:
                break
            for E in combinations(NULLS, r):
                Ef = frozenset(E)
                for k in range(0, len(S0 - self.xS) + 1):
                    for T in combinations(sorted(S0 - self.xS), k):
                        W = self.xS | frozenset(T) | Ef
                        if W != S0 and self.member(W):
                            out.append(W)
        return out


class Scores:
    def __init__(self, D):
        self.D = D
        self.c = {}

    def F(self, W):
        v = self.c.get(W)
        if v is None:
            v = self.D.F(tuple(sorted(W)))
            self.c[W] = v
        return v


def block_logr(D):
    """log r_b(U) = log BF(U) for every U within a group (blocks = groups)."""
    T = []
    for G in groups:
        d = {}
        for r in range(0, len(G) + 1):
            for U in combinations(G, r):
                d[frozenset(U)] = D.logBF(tuple(U))
        T.append(d)
    return T


def pi0_and_d(D, tabs):
    # Zbar0 = sum_k w(k) * coef_k( prod_b e_b(z) ),  e_b(j) = sum_{|U|=j} r_b(U)
    prof = np.zeros(1)
    prof[0] = 1.0
    shift = 0.0
    for d in tabs:
        mx = max(d.values())
        e = np.zeros(5)
        for U, v in d.items():
            e[len(U)] += np.exp(v - mx)
        prof = np.convolve(prof, e)
        shift += mx
    w = np.exp(D.logw[: len(prof)] - D.logw.max())
    logZ0 = shift + D.logw.max() + np.log(np.sum(w * prof))

    def comp(W):
        return sum(t[frozenset(W & set(G))] for t, G in zip(tabs, groups))

    def logpi0(W):
        return D.logw[len(W)] + comp(W) - logZ0

    def dd(W):
        return D.logBF(tuple(sorted(W))) - comp(W)

    return logpi0, dd


def plog(x):
    return 1.0 / (1.0 + np.exp(-x)) if x > -700 else 0.0


def analyse(n, seed, kinds=("SH", "W1")):
    rng = np.random.default_rng(seed)
    D = Data(SIG, TH, n, rng)
    Sc = Scores(D)
    N = neighbour_graph(n)
    tabs = block_logr(D)
    logpi0, dd = pi0_and_d(D, tabs)
    pi0ref = np.exp(logpi0(Sref))
    d_ref = dd(Sref)
    out = {"n": n, "seed": seed, "pi0_ref": pi0ref, "pi0_S0": float(np.exp(logpi0(S0)))}
    for kind in kinds:
        fam = Fam(kind, N, Sref)
        st = fam.states()
        ph1 = [W for W in st if S0 - W]
        a = fam.a
        ph2 = [S0 | frozenset(E) for r in range(1, a + 1) for E in combinations(NULLS, r)]
        dcache = {}

        def dW(W):
            v = dcache.get(W)
            if v is None:
                v = dd(W)
                dcache[W] = v
            return v

        def in_F(W):
            M = S0 - W
            if not M:
                return len(W - S0) <= a
            return fam.member(W)

        def bad(W, W2):
            if not in_F(W2):
                return True
            if fam.V(W2) > fam.V(W):
                return True
            if not (W & S0) <= W2:
                return True
            return False

        def label_bad(W):
            """dict label -> P_W(bad step) for G_j (j), 'U', 'N' (one neighbour label), 'I' (upper bound)."""
            res = {}
            FW = Sc.F(W)
            k = len(W)
            for j in range(p):
                if j in W:
                    W2 = W - {j}
                    o = plog(FW - Sc.F(W2))
                    res[j] = (1 - o) if bad(W, W2) else 0.0
                else:
                    W2 = W | {j}
                    o = plog(Sc.F(W2) - FW)
                    res[j] = o if bad(W, W2) else 0.0
            out_ = [l for l in range(p) if l not in W]
            s = 0.0
            for j in W:
                for l in out_:
                    W2 = (W - {j}) | {l}
                    if bad(W, W2):
                        s += min(1.0, np.exp(Sc.F(W2) - FW))
            res["U"] = s / (k * (p - k))
            s = 0.0
            for j in W:
                cand = [l for l in N[j] if l not in W]
                if not cand:
                    continue
                for l in cand:
                    W2 = (W - {j}) | {l}
                    if bad(W, W2):
                        back = len([x for x in N[l] if x not in W2])
                        s += min(1.0, np.exp(Sc.F(W2) - FW) * len(cand) / back) / len(cand)
            res["N"] = s / k
            if bad(W, Sref):
                res["I"] = (1 - pi0ref) + min(1.0, np.exp(d_ref - dW(W)))
            else:
                res["I"] = (1 - pi0ref)
            return res

        def sup_sum(states):
            sup = {}
            arg = {}
            for W in states:
                r = label_bad(W)
                for key, v in r.items():
                    if v > sup.get(key, -1):
                        sup[key] = v
                        arg[key] = W
            eta = sum(v for key, v in sup.items() if key != "N") + B * sup.get("N", 0.0)
            gib_truth = sum(sup.get(j, 0) for j in S0)
            gib_null = sum(sup.get(j, 0) for j in NULLS)
            return eta, {"gibbs_truth": gib_truth, "gibbs_null": gib_null, "U": sup.get("U", 0), "B*N": B * sup.get("N", 0),
                         "I": sup.get("I", 0)}, {str(key): sorted(arg[key]) for key in ["U", "N", "I"] if key in arg}

        eta1, br1, arg1 = sup_sum(ph1)
        # phase-1 progress constants
        eps_pt = 0.0
        by_M = {}
        for W in ph1:
            M = S0 - W
            FW = Sc.F(W)
            os_ = {j: plog(Sc.F(W | {j}) - FW) for j in M}
            eps_pt = max(eps_pt, 1 - max(os_.values()))
            for j in M:
                by_M.setdefault((M, j), 0.0)
                by_M[(M, j)] = max(by_M[(M, j)], 1 - os_[j])
        Mfull = S0 - Sref
        eps_add = 0.0
        for r in range(1, len(Mfull) + 1):
            for Mp in combinations(sorted(Mfull), r):
                Mp = frozenset(Mp)
                vals = [by_M[(Mp, j)] for j in Mp if (Mp, j) in by_M]
                if vals:
                    eps_add = max(eps_add, min(vals))
        c1 = max(1 - eps_add, (1 - eps_pt) / len(Mfull))
        # phase 2
        eta2, br2, arg2 = sup_sum(ph2)
        eps_del = 0.0
        for W in ph2:
            FW = Sc.F(W)
            for l in W - S0:
                eps_del = max(eps_del, plog(FW - Sc.F(W - {l})))
        # slot hiding h(l) (U and N labels exactly; I bounded by 1 - pi0(S°)), H_a
        hU, hN = {}, {}
        for W in [S0] + ph2:
            FW = Sc.F(W)
            k = len(W)
            for l0 in W - S0:
                sU = 0.0
                for l in range(p):
                    if l in W:
                        continue
                    W2 = (W - {l0}) | {l}
                    if not bad(W, W2) and fam.V(W2) == fam.V(W):
                        sU += min(1.0, np.exp(Sc.F(W2) - FW))
                hU[l0] = max(hU.get(l0, 0), sU / (k * (p - k)))
                cand = [l for l in N[l0] if l not in W]
                sN = 0.0
                for l in cand:
                    W2 = (W - {l0}) | {l}
                    if not bad(W, W2) and fam.V(W2) == fam.V(W):
                        back = len([x for x in N[l] if x not in W2])
                        sN += min(1.0, np.exp(Sc.F(W2) - FW) * len(cand) / back) / len(cand)
                hN[l0] = max(hN.get(l0, 0), sN / k)
        h = {l: 0.5 * (hU.get(l, 0) + B * hN.get(l, 0) + (1 - pi0ref)) for l in NULLS}
        Ha = max(min(min(h[l] for l in W - S0), (B + 2) / (len(W - S0) + B + 2)) for W in ph2)
        c2 = 1 - eps_del - Ha
        cst = min(c1, c2)
        L = int(np.ceil(np.log2(n + 1)))
        Hp = L + 5
        v = fam.V(Sref)
        eta = eta1 + eta2
        from math import comb as C
        binom = sum(C(Hp, j) * cst ** j * (1 - cst) ** (Hp - j) for j in range(v)) if cst > 0 else 1.0
        rec = {"a": a, "v": v, "n_phase1_states": len(ph1), "eta1": eta1, "eta1_parts": br1, "eta1_argmax": arg1,
               "eta2": eta2, "eta2_parts": br2, "eps_add": eps_add, "eps_pt": eps_pt, "c1": c1, "eps_del": eps_del,
               "H_a": Ha, "c2": c2, "c_star": cst, "Hprime": Hp, "Binom_tail": binom, "Hprime_eta": Hp * eta,
               "bound": min(1.0, binom + Hp * eta)}
        if kind == "W1":
            rec["A_nb"] = sorted(fam.A)
            Ws = Sref | {1}
            rec["Wstar_in_family"] = fam.member(Ws)
            rec["Wstar_bad"] = label_bad(Ws) if fam.member(Ws) else None
        out[kind] = rec
    return out


def population_checks():
    """n-free design checks in exact Gram (rss_mu/(n-1) is a population quantity)."""
    n = 1000
    D = Data(SIG, TH, n, np.random.default_rng(0))
    N = neighbour_graph(n)
    fam = Fam("SH", N, Sref)
    ph1 = [W for W in fam.states() if S0 - W]
    r = lambda W: D.rss_mu(tuple(sorted(W))) / (n - 1)
    ts = min(r(W - {i}) - r(W) for W in ph1 for i in W & S0)
    fs_max, fs_nb_min = 0, 1e9
    for W in ph1:
        for i in W & S0:
            base = r(W)
            subs = [l for l in range(p) if l not in W and r((W - {i}) | {l}) - base <= 1e-9]
            fs_max = max(fs_max, len(subs))
            for l in N[i]:
                if l not in W:
                    fs_nb_min = min(fs_nb_min, r((W - {i}) | {l}) - base)
    ulr = 1e9
    for W in ph1:
        AW = A_LH(S0 - W)
        for k in (W - S0) & AW:
            for l in range(p):
                if l in W or l in S0 or l in AW:
                    continue
                ulr = min(ulr, r((W - {k}) | {l}) - r(W))
    gs = {str(sorted(T)): r(Sref) - r(Sref | set(T)) for k in (1, 2) for T in combinations(sorted(Mx), k)}
    # zero junk leakage: delta_{W,l} for current junk l at phase-1 states (exact Gram, population)
    G = SIG
    mu_cov = SIG @ TH
    maxdel = 0.0
    for W in ph1:
        AW = A_LH(S0 - W)
        idx = sorted(W)
        GW = G[np.ix_(idx, idx)]
        for l in NULLS:
            if l in W or l in AW:
                continue
            resid_cov = mu_cov[l] - G[l, idx] @ np.linalg.solve(GW, mu_cov[idx])   # x_l'(I-P_W)mu/(n-1)
            maxdel = max(maxdel, abs(resid_cov))
    return {"TS_min_loss": ts, "FS_max_substitutes": fs_max, "FS_min_loss_over_neighbours": fs_nb_min,
            "ULR_min_loss": ulr, "GS": gs, "max_junk_leakage_cov": maxdel, "n_phase1_states": len(ph1)}


if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1:]] or [400, 1600, 6400, 25600, 102400, 409600, 1638400]
    reps = 2
    pc = population_checks()
    print("population checks:", json.dumps(pc, indent=1), flush=True)
    allres = {"population": pc, "runs": []}
    lines = ["population (n-free) checks on the SH family, x = S°: " + json.dumps(pc)]
    hdr = ("kind | n | seed | pi0(S°) | eta1 [gibbs_truth, gibbs_null, U, B*N, I] | eta2 [gibbs_truth, gibbs_null, U, B*N, I]"
           " | eps_pt | eps_add | c1 | eps_del | H_a | c2 | c_* | v | H'=L+5 | Binom tail | H'eta")
    lines.append(hdr)
    for n in ns:
        for r in range(reps):
            kinds = ("SH", "W1") if (r == 0 and n in (1600, 102400)) else ("SH",)
            res = analyse(n, 1000 * r + n % 997, kinds)
            allres["runs"].append(res)
            for kind in [k_ for k_ in ("SH", "W1") if k_ in res]:
                q = res[kind]
                e1, e2 = q["eta1_parts"], q["eta2_parts"]
                f = lambda d: "[" + ", ".join(f"{d[k]:.2e}" for k in ["gibbs_truth", "gibbs_null", "U", "B*N", "I"]) + "]"
                lines.append(f"{kind} | {n} | {res['seed']} | {res['pi0_ref']:.4f} | {q['eta1']:.3e} {f(e1)} | {q['eta2']:.3e} {f(e2)}"
                             f" | {q['eps_pt']:.2e} | {q['eps_add']:.2e} | {q['c1']:.3f} | {q['eps_del']:.2e} | {q['H_a']:.3f} | {q['c2']:.3f}"
                             f" | {q['c_star']:.3f} | {q['v']} | {q['Hprime']} | {q['Binom_tail']:.3f} | {q['Hprime_eta']:.3e}")
                print(lines[-1], flush=True)
            if "W1" not in res:
                continue
            w1 = res["W1"]
            lines.append(f"   W1 family: A_nb = {w1['A_nb']}; W* = S°+{{1}} in family: {w1['Wstar_in_family']}; "
                         f"bad probs at W*: U = {w1['Wstar_bad']['U']:.3f}, B*N = {B * w1['Wstar_bad']['N']:.3f}" if w1["Wstar_bad"] else "")
            print(lines[-1], flush=True)
    tag = "_".join(str(v) for v in ns) if len(sys.argv) > 1 else "all"
    with open(__file__.replace("scripts/lh_premises.py", f"results/lh_premises_{tag}.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(__file__.replace("scripts/lh_premises.py", f"results/lh_premises_{tag}.json"), "w") as f:
        json.dump(allres, f, indent=1, default=str)
