"""W5-FAVIID goal 4: simulate the v3 pilot (M §6.6) and one candidate-grid construction (M §6.7) on study designs,
to obtain the realised stage count T_n, and compute Delta_n = max(1 - pi0(S0), delta_1) (W2-T26 Lemma 1).

What is simulated faithfully (exact scores, EX-A):
  * H_e = ceil(512 N0/2500) particles, N0 = max(2500, n, p), iid exact pi0 draws (backward sampler);
  * pilot next-temperature rule = v3_calib.h::pilot_next_phi (ESS >= 0.90 H, 60 halvings, floor 1/T_e, T_e = T0);
  * multinomial resampling after every reweighting; one move round per stage at the new temperature:
    m = p + B + 2 labelled steps in a uniformly random order (p Gibbs flips with the cap K, one uniform swap,
    B neighbour swaps on the v3 neighbour graph, one independence proposal from pi0), as in M §6.5;
  * candidate grid = v3_calib.h::build_grid with the pilot temperatures as targets.
Approximation (stated in the report): V = top 20p by log gamma_0 and top 20p by log gamma_1 among the models scored in
the *pilot only* (initial draws, every Gibbs-flip neighbour of every visited state, every proposal), plus the empty
model; block-table sub-models and the diagnostic-island rebuild loop are omitted. The grid from a larger V can only
insert more points, so T_grid here is a lower bound for the method's realised T on these data.

delta_1 = 1 - pi(S0) is not computable exactly at p = 500; reported: u1 = sum over the one-move neighbourhood of S0
(additions, deletions, swaps) of pi(S)/pi(S0) (exact scores), the lower bound delta_1 >= u1/(1+u1), and the
product-form estimate 1 - exp(-u1).
Seeds: data as study_sweep.py; sampler seed = data seed + 777.
Usage: python3 pilot_sim.py OUT.jsonl scen p scale n rep [rep ...]
"""
import json, math, sys, time
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.special import logsumexp
import pxn_core as pc
import fav_core as fc

NS = [200, 400, 800, 1600, 3200]


def neighbour_graph(D, B):
    p = D.p
    R = np.abs(D.X.T @ D.X) / (D.n - 1)
    np.fill_diagonal(R, -1.0)
    rn = math.sqrt(2.0 * math.log(p) / D.n)
    chosen = []
    for j in range(p):
        order = np.lexsort((np.arange(p), -R[j]))  # |r| desc, ties by index
        above = int((R[j][order] > rn).sum())
        chosen.append(order[:min(B, max(1, above))])
    N = [set() for _ in range(p)]
    for j in range(p):
        for l in chosen[j]:
            N[j].add(int(l)); N[int(l)].add(j)
    return [np.array(sorted(s), int) for s in N]


class Model:
    def __init__(self, D, T, SL, G, rng):
        self.D, self.T, self.SL, self.G, self.rng = D, T, SL, G, rng
        self.n, self.p, self.nu, self.K = D.n, D.p, D.nu, D.K
        self.lw = pc.log_w(np.arange(self.p + 1), self.p)
        self.keys = rng.integers(1, 2 ** 63 - 1, size=self.p, dtype=np.int64)
        self.blk = np.empty(self.p, int)
        self.pos = np.empty(self.p, int)
        for b, C in enumerate(T.blocks):
            for t, j in enumerate(C):
                self.blk[j], self.pos[j] = b, t

    def logm(self, S):
        n, nu = self.n, self.nu
        if len(S) == 0:
            return -nu * math.log(0.02 + n - 1.0)
        S = np.asarray(S)
        GS = self.G[np.ix_(S, S)]
        zS = self.D.z[S]
        H = (n + 1.0) * GS + np.eye(len(S))
        M = GS + np.eye(len(S))
        cH, cM = cho_factor(H), cho_factor(M)
        ldH = 2 * np.log(np.diag(cH[0])).sum()
        ldM = 2 * np.log(np.diag(cM[0])).sum()
        c = zS @ cho_solve(cH, zS)
        return -0.5 * (ldH - ldM) - nu * math.log(0.02 + (n - 1.0) - n * c)

    def state(self, S):
        """Full cache for state S: logBF, lr0, flipBF (p), tabd (p), hash, masks."""
        n, nu, p = self.n, self.nu, self.p
        S = sorted(S)
        k = len(S)
        st = dict(S=S, k=k)
        z = self.D.z
        if k == 0:
            ldH = ldM = 0.0
            cS = 0.0
            sH = np.full(p, (n + 1.0) * (n - 1.0) + 1.0)
            sM = np.full(p, float(n))
            w = z.copy()
            lm = -nu * math.log(0.02 + n - 1.0)
        else:
            Sa = np.asarray(S)
            GS = self.G[np.ix_(Sa, Sa)]
            H = (n + 1.0) * GS + np.eye(k)
            M = GS + np.eye(k)
            cH, cM = cho_factor(H), cho_factor(M)
            ldH = 2 * np.log(np.diag(cH[0])).sum()
            ldM = 2 * np.log(np.diag(cM[0])).sum()
            Gs = self.G[Sa, :]
            HiG = cho_solve(cH, Gs)
            MiG = cho_solve(cM, Gs)
            sH = (n + 1.0) * (n - 1.0) + 1.0 - (n + 1.0) ** 2 * np.einsum("ij,ij->j", Gs, HiG)
            sM = float(n) - np.einsum("ij,ij->j", Gs, MiG)
            zS = z[Sa]
            HiZ = cho_solve(cH, zS)
            cS = zS @ HiZ
            w = z - (n + 1.0) * (Gs.T @ HiZ)
            lm = -0.5 * (ldH - ldM) - nu * math.log(0.02 + (n - 1.0) - n * cS)
        with np.errstate(divide="ignore", invalid="ignore"):
            Qa = 0.02 + (n - 1.0) - n * (cS + w * w / sH)
            la = -0.5 * (ldH + np.log(sH) - ldM - np.log(sM)) - nu * np.log(Qa)
        flip = la - lm
        if k > 0:
            Hinv = cho_solve(cH, np.eye(k))
            Minv = cho_solve(cM, np.eye(k))
            dH, dM = np.diag(Hinv), np.diag(Minv)
            Qd = 0.02 + (n - 1.0) - n * (cS - HiZ ** 2 / dH)
            ld = -0.5 * (ldH + np.log(dH) - ldM - np.log(dM)) - nu * np.log(Qd)
            flip[Sa] = ld - lm
        st["logBF"] = lm - (-nu * math.log(0.02 + n - 1.0))
        st["flipBF"] = flip
        inS = np.zeros(p, bool)
        inS[S] = True
        st["inS"] = inS
        masks = {}
        for j in S:
            masks[self.blk[j]] = masks.get(self.blk[j], 0) | (1 << int(self.pos[j]))
        st["masks"] = masks
        tabd = np.empty(p)
        lr0 = 0.0
        for b, C in enumerate(self.T.blocks):
            mb = masks.get(b, 0)
            lr = self.T.lr[b]
            lr0 += lr[mb]
            idx = mb ^ (1 << np.arange(len(C)))
            tabd[C] = lr[idx] - lr[mb]
        st["lr0"] = lr0
        st["tabd"] = tabd
        st["hash"] = int(np.bitwise_xor.reduce(self.keys[S])) if k else 0
        return st

    def lr0_of(self, S):
        return self.T.log_r(S)


class Pool:
    """Top-20p stores by log gamma_0 and log gamma_1 over everything scored (deduplicated by Zobrist hash)."""

    def __init__(self, cap):
        self.cap = cap
        self.h, self.l0, self.l1 = [], [], []

    def add(self, h, l0, l1):
        self.h.append(np.atleast_1d(h).astype(np.int64))
        self.l0.append(np.atleast_1d(l0).astype(float))
        self.l1.append(np.atleast_1d(l1).astype(float))
        if sum(len(x) for x in self.h) > 20 * self.cap:
            self.prune()

    def prune(self):
        h = np.concatenate(self.h); l0 = np.concatenate(self.l0); l1 = np.concatenate(self.l1)
        ok = np.isfinite(l0) & np.isfinite(l1)
        h, l0, l1 = h[ok], l0[ok], l1[ok]
        h, ui = np.unique(h, return_index=True)
        l0, l1 = l0[ui], l1[ui]
        keep = np.zeros(len(h), bool)
        if len(h) > self.cap:
            keep[np.argpartition(-l0, self.cap - 1)[:self.cap]] = True
            keep[np.argpartition(-l1, self.cap - 1)[:self.cap]] = True
        else:
            keep[:] = True
        self.h, self.l0, self.l1 = [h[keep]], [l0[keep]], [l1[keep]]

    def V(self):
        self.prune()
        return self.l0[0], self.l1[0] - self.l0[0]


def lse(x):
    m = np.max(x)
    return m + math.log(np.exp(x - m).sum()) if np.isfinite(m) else m


def pop_ess(d, delta):
    x = delta * d
    return math.exp(2 * lse(x) - lse(2 * x))


def pilot_next_phi(d, phi, H, Te):
    thr = 0.90 * H
    if pop_ess(d, 1.0 - phi) >= thr:
        return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if pop_ess(d, mid - phi) >= thr:
            lo = mid
        else:
            hi = mid
    if lo - phi < 1.0 / Te:
        f = min(1.0, phi + 1.0 / Te)
        if f >= 1 - 1e-12:
            f = 1.0
        return f, True
    return lo, False


def rho_V(l0, d, u, v):
    F = lambda t: lse(l0 + t * d)
    return math.exp(2 * F(v) - F(u) - F(2 * v - u))


def build_grid(l0, d, targets, Te):
    grid = [0.0]
    u = 0.0
    targets = sorted(targets)
    while u < 1.0:
        b = next(t for t in targets if t > u)
        if rho_V(l0, d, u, b) >= 0.90:
            v = b
        else:
            lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if rho_V(l0, d, u, mid) >= 0.90:
                    lo, anyp = mid, True
                else:
                    hi = mid
            if not anyp:
                return grid, "non_progress"
            v = lo
        if v >= 1 - 1e-12:
            v = 1.0
        if not v > u:
            return grid, "non_progress"
        grid.append(v)
        if len(grid) - 1 > Te:
            return grid, "too_many_intervals"
        u = v
    return grid, "ok"


def move_round(Mo, st, phi, NB, pool, rng, indep_draw):
    p, B = Mo.p, Mo.D.B
    m = p + B + 2
    order = rng.permutation(m)
    u = rng.random(m)
    lw = Mo.lw
    pos = 0

    def record(st):
        h = st["hash"] ^ Mo.keys
        l0 = np.where(st["inS"], lw[max(st["k"] - 1, 0)], lw[min(st["k"] + 1, p)]) + st["lr0"] + st["tabd"]
        l1 = np.where(st["inS"], lw[max(st["k"] - 1, 0)], lw[min(st["k"] + 1, p)]) + st["logBF"] + st["flipBF"]
        if st["k"] >= Mo.K:
            l0 = np.where(st["inS"], l0, -np.inf); l1 = np.where(st["inS"], l1, -np.inf)
        pool.add(h, l0, l1)

    def gam(S):  # log gamma_phi(S), lr0, logBF
        lr0 = Mo.lr0_of(S)
        lbf = Mo.logm(S) + Mo.nu * math.log(0.02 + Mo.n - 1.0)
        return lw[len(S)] + (1 - phi) * lr0 + phi * lbf, lr0, lbf

    record(st)
    while pos < m:
        k = st["k"]
        prior = np.where(st["inS"], lw[max(k - 1, 0)] - lw[k], (lw[min(k + 1, p)] - lw[k]) if k < Mo.K else -np.inf)
        Dl = prior + (1 - phi) * st["tabd"] + phi * st["flipBF"]
        pf = 1.0 / (1.0 + np.exp(-np.clip(Dl, -700, 700)))
        rest = order[pos:]
        gibbs = rest < p
        ev = ~gibbs.copy()
        ev[gibbs] = u[rest[gibbs]] < pf[rest[gibbs]]
        hit = np.flatnonzero(ev)
        if len(hit) == 0:
            break
        pos += int(hit[0])
        lab = int(order[pos])
        pos += 1
        S = st["S"]
        newS = None
        if lab < p:
            newS = sorted(set(S) ^ {lab})
        elif lab == p or lab <= p + B:  # uniform swap (lab == p) or neighbour swap
            if k == 0 or k == p:
                continue
            j = S[int(u[lab] * k)]
            if lab == p:
                outs = np.flatnonzero(~st["inS"])
                l = int(outs[int(rng.random() * len(outs))])
                corr = 0.0
            else:
                cand = [x for x in NB[j] if not st["inS"][x]]
                if not cand:
                    continue
                l = int(cand[int(rng.random() * len(cand))])
                S2 = set(S) - {j} | {l}
                nl = sum(1 for x in NB[l] if x not in S2)
                corr = math.log(len(cand)) - math.log(nl) if nl > 0 else -np.inf
            Sp = sorted(set(S) - {j} | {l})
            g1, lr1, lb1 = gam(Sp)
            g0 = lw[k] + (1 - phi) * st["lr0"] + phi * st["logBF"]
            pool.add(np.int64(st["hash"] ^ Mo.keys[j] ^ Mo.keys[l]), lw[k] + lr1, lw[k] + lb1)
            if math.log(rng.random() + 1e-300) < g1 - g0 + corr:
                newS = Sp
        else:  # independence proposal from pi0
            Sp = indep_draw()
            lr1 = Mo.lr0_of(Sp)
            lb1 = Mo.logm(Sp) + Mo.nu * math.log(0.02 + Mo.n - 1.0)
            hS = int(np.bitwise_xor.reduce(Mo.keys[Sp])) if Sp else 0
            pool.add(np.int64(hS), lw[len(Sp)] + lr1, lw[len(Sp)] + lb1)
            d1, d0 = lb1 - lr1, st["logBF"] - st["lr0"]
            if math.log(rng.random() + 1e-300) < phi * (d1 - d0):
                newS = Sp
        if newS is not None and newS != S:
            st = Mo.state(newS)
            record(st)
    return st


def delta1_neigh(D, S0):
    S0 = sorted(S0)
    p, s0 = D.p, len(S0)
    S0s = set(S0)
    nb = []
    for j in range(p):
        if j in S0s:
            nb.append([x for x in S0 if x != j])
        else:
            nb.append(sorted(S0 + [j]))
    for i in S0:
        rest = [x for x in S0 if x != i]
        for j in range(p):
            if j not in S0s:
                nb.append(sorted(rest + [j]))
    f = pc.log_F(D, nb)
    f0 = pc.log_F(D, [S0])[0]
    return float(np.exp(logsumexp(f - f0)))


def run(scen, p, scale, n, rep, out):
    nidx = NS.index(n)
    seed = 5000000 + 100000 * scen + 1000 * (p // 500) + 10 * nidx + rep
    rng = np.random.default_rng(seed)
    X = fc.gen_raw_X(scen, n, p, rng)
    eps = rng.standard_normal(n)
    active, beta, _ = fc.truth(p)
    Xs = X[:, active] - X[:, active].mean(0)
    Xs /= np.sqrt((Xs ** 2).sum(0) / (n - 1))
    S0 = sorted(active.tolist())
    D = pc.Data(X, scale * (Xs @ beta) + eps)
    blocks = pc.v3_blocks(D)
    T = fc.FastTables(D, blocks)
    SL = pc.StartLaw(T)
    one_m_pi0 = -math.expm1(SL.log_pi0(S0))
    t0 = time.time()
    u1 = delta1_neigh(D, S0)
    srng = np.random.default_rng(seed + 777)
    G = D.X.T @ D.X
    Mo = Model(D, T, SL, G, srng)
    NB = neighbour_graph(D, D.B)
    ell = math.ceil(math.log2(n + p + 1))
    T0 = max(1000, ell * ell)
    N0 = max(2500, n, p)
    H = math.ceil(512 * N0 / 2500)
    pool = Pool(20 * p)
    draws = SL.sample(H, srng)
    sts = [Mo.state(S) for S in draws]
    for st in sts:
        pool.add(np.int64(st["hash"]), Mo.lw[st["k"]] + st["lr0"], Mo.lw[st["k"]] + st["logBF"])
    phi, temps, forced = 0.0, [], 0
    buf = []

    def indep_draw():
        if not buf:
            buf.extend(SL.sample(256, srng))
        return buf.pop()

    ess_hist = []
    while phi < 1.0:
        d = np.array([st["logBF"] - st["lr0"] for st in sts])
        nphi, fz = pilot_next_phi(d, phi, H, T0)
        forced += fz
        lw_ = (nphi - phi) * d
        w = np.exp(lw_ - lw_.max())
        ess_hist.append(float(w.sum() ** 2 / (w * w).sum() / H))
        idx = srng.choice(H, size=H, p=w / w.sum())
        sts = [sts[i] for i in idx]
        phi = nphi
        temps.append(phi)
        sts = [move_round(Mo, st, phi, NB, pool, srng, indep_draw) for st in sts]
        if len(temps) > 400:
            break
    l0, dV = pool.V()
    l0 = np.append(l0, Mo.lw[0]); dV = np.append(dV, 0.0)  # the empty model
    grid, status = build_grid(l0, dV, temps, T0)
    frac_S0 = float(np.mean([st["S"] == S0 for st in sts]))
    delta1_lb = u1 / (1 + u1)
    delta1_est = -math.expm1(-u1)
    rec = dict(scen=scen, p=p, scale=scale, n=n, rep=rep, H=H, T_pilot=len(temps), forced=int(forced),
               temps=temps, T_grid=len(grid) - 1, grid_status=status, V_size=int(len(l0)),
               one_minus_pi0=one_m_pi0, u1=u1, delta1_lb=delta1_lb, delta1_est=delta1_est,
               Delta_lb=max(one_m_pi0, delta1_lb), Delta_est=max(one_m_pi0, delta1_est),
               P1_pilot=(len(temps) + 1) * max(one_m_pi0, delta1_est),
               P1_grid=(len(grid)) * max(one_m_pi0, delta1_est),
               frac_S0_end=frac_S0, ess_first=ess_hist[0], secs=time.time() - t0)
    with open(out, "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "temps"}), flush=True)


if __name__ == "__main__":
    out = sys.argv[1]
    scen, p, scale, n = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
    import os
    done = set()
    if os.path.exists(out):
        for l in open(out):
            if l.strip():
                r = json.loads(l)
                done.add((r["scen"], r["p"], r["scale"], r["n"], r["rep"]))
    for rep in sys.argv[6:]:
        if (scen, p, scale, n, int(rep)) in done:
            continue
        run(scen, p, scale, n, int(rep), out)
