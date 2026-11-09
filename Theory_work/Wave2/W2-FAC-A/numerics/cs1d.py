"""cs1d.py -- exact one-dimensional reduction for exact-Gram compound symmetry (Lemma CS-1D, falsification + fast LS0).
X'X = (n-1)[(1-a)I + a 11'];  for |T| = k:  F(T) = log w(k) + D_k - nu*log(0.02 + y'y - (n/A)[P_T - b_k L_T^2]),
P_T = sum_T z_j^2, L_T = sum_T z_j, A = (n+1)(n-1)(1-a)+1, B = (n+1)(n-1)a, b_k = B/(A+kB),
D_k = -1/2[(k-1)log A + log(A+kB) - (k-1)log A' - log(A'+kB')], A' = (n-1)(1-a)+1, B' = (n-1)a (D_0 = 0).
selftest(): compares with fac_exact.ExactFast on random sets.  ls0_1d(): M 6.10 local search using the formula."""
import math, sys, json, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import bvs_core as bc
import fac_common as fc
import fac_exact as fe


class CS1D:
    def __init__(self, a, z, n, K=None):
        self.a, self.n, self.p = a, n, len(z)
        self.z = np.asarray(z, float)
        self.K = min(self.p, n // 2) if K is None else K
        n1 = n - 1.0
        self.A = (n + 1.0) * n1 * (1 - a) + 1.0
        self.B = (n + 1.0) * n1 * a
        self.A2 = n1 * (1 - a) + 1.0
        self.B2 = n1 * a
        k = np.arange(self.K + 2, dtype=float)
        self.b = self.B / (self.A + k * self.B)
        D = -0.5 * ((k - 1) * math.log(self.A) + np.log(self.A + k * self.B) - (k - 1) * math.log(self.A2) - np.log(self.A2 + k * self.B2))
        D[0] = 0.0
        self.D = D
        self.logw = bc.log_prior_w(self.p, self.K)
        self.nu = 0.01 + n / 2.0
        self.yty = n1

    def Fk(self, k, P, L):
        return self.logw[k] + self.D[k] - self.nu * np.log(0.02 + self.yty - (self.n / self.A) * (P - self.b[k] * L ** 2))

    def F(self, T):
        T = list(T)
        return float(self.Fk(len(T), float((self.z[T] ** 2).sum()), float(self.z[T].sum())))


def ls0_1d(m, start, cap, S0):
    p = m.p
    inT = np.zeros(p, bool); inT[list(start)] = True
    S0set = set(S0)
    moves, toks = 0, []
    limit = False
    while True:
        k = int(inT.sum())
        zi, zo = m.z[inT], m.z[~inT]
        idx_in, idx_out = np.flatnonzero(inT), np.flatnonzero(~inT)
        P, L = float((zi ** 2).sum()), float(zi.sum())
        FT = float(m.Fk(k, P, L))
        best, bestS = -np.inf, None
        cands = []
        if k >= 1:
            fd = m.Fk(k - 1, P - zi ** 2, L - zi)
            cands.append(("d", fd))
        if k < m.K and len(zo):
            fa = m.Fk(k + 1, P + zo ** 2, L + zo)
            cands.append(("a", fa))
        if k >= 1 and len(zo):
            fs = m.Fk(k, P - zi[:, None] ** 2 + zo[None, :] ** 2, L - zi[:, None] + zo[None, :])
            cands.append(("s", fs))
        mx = max(float(c[1].max()) for c in cands)
        if mx <= FT:
            break
        if moves >= cap:
            limit = True
            break
        # lexicographic tie-break among exact maxima
        sets = []
        cur = list(idx_in)
        for kind, arr in cands:
            for h in np.argwhere(arr == mx):
                if kind == "d":
                    S = tuple(sorted(set(cur) - {int(idx_in[h[0]])}))
                elif kind == "a":
                    S = tuple(sorted(set(cur) | {int(idx_out[h[0]])}))
                else:
                    S = tuple(sorted((set(cur) - {int(idx_in[h[0]])}) | {int(idx_out[h[1]])}))
                sets.append(S)
        nxt = min(sets)
        toks.append(fc.move_token(tuple(cur), nxt, S0))
        inT[:] = False; inT[list(nxt)] = True
        moves += 1
    final = tuple(int(v) for v in np.flatnonzero(inT))
    return dict(final=final, moves=moves, toks=toks, limit=limit)


def selftest():
    rng = np.random.default_rng(5)
    err = 0.0
    for a, p, n in [(0.3, 30, 200), (0.7, 50, 1000), (0.5, 40, 10 ** 6)]:
        Sigma = (1 - a) * np.eye(p) + a * np.ones((p, p))
        th = np.zeros(p); th[[2, 7, 11]] = [1.0, -0.5, 0.8]
        z, g = fe.draw_z(Sigma, th, n, 1.0, rng)
        f1, f2 = CS1D(a, z, n), fe.ExactFast(Sigma, z, n)
        for _ in range(30):
            k = int(rng.integers(0, min(p, n // 2) + 1))
            T = tuple(sorted(rng.choice(p, size=k, replace=False)))
            err = max(err, abs(f1.F(T) - f2.F_of(T)))
        # LS equivalence from full model
        st = tuple(range(min(p, n // 2)))
        r1 = ls0_1d(f1, st, 10 ** 6, (2, 7, 11))
        r2 = fc.ls0(f2, st, 10 ** 6, (2, 7, 11), diag=False)
        assert r1["final"] == r2["final"] and r1["moves"] == r2["moves"], (r1["final"], r2["final"])
    return err


def run(job):
    a, s0, p, n, seed = job
    rng = np.random.default_rng(777 + 31 * seed + p + 7 * s0 + int(100 * a) + n % 9973)
    Sigma = None
    # theta: s0 truths at positions 0..s0-1 (exchangeable design: positions irrelevant), coefficients alternating
    pat = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
    th = np.zeros(p); th[:s0] = pat[np.arange(s0) % 6]
    S0 = tuple(range(s0))
    # draw z directly: X'eps/(sigma sqrt(n-1)) = sqrt(1-a) h + sqrt(a) h0 1
    n1 = n - 1.0
    h = rng.standard_normal(p); h0 = rng.standard_normal()
    Sth = (1 - a) * th + a * th.sum()
    noise = math.sqrt(1 - a) * h + math.sqrt(a) * h0
    thSth = float(th @ Sth)
    # |P_X eps|^2/sigma^2 = noise' Sigma^{-1} noise ; mu'eps = sqrt(n1) theta' noise
    Sinv_noise = (noise - (a / (1 - a + p * a)) * noise.sum()) / (1 - a)
    pe = float(noise @ Sinv_noise)
    chi = rng.chisquare(n - 1 - p)
    Y2 = n1 * thSth + 2 * math.sqrt(n1) * float(th @ noise) + pe + chi
    z = (n1 * Sth + math.sqrt(n1) * noise) * math.sqrt(n1) / math.sqrt(Y2)
    m = CS1D(a, z, n)
    start = tuple(range(min(p, m.K)))  # start mode = [p] (p <= K) asymptotically; see lemma
    r = ls0_1d(m, start, 10 ** 7, S0)
    toks = r["toks"]
    ell = bc.ell_cap(n, p)
    return dict(a=a, s0=s0, p=p, n=n, seed=seed, moves=r["moves"], final_eq=(r["final"] == S0),
                n_delN=sum(t == "-N" for t in toks), n_swap=sum(t.startswith("sw") for t in toks),
                n_add=sum(t.startswith("+") for t in toks), n_delT=sum(t == "-T" for t in toks),
                within_MR1=(r["final"] == S0 and r["moves"] <= ell + len(start)),
                swap_positions=json.dumps([i for i, t in enumerate(toks) if not t == "-N"][:20]))


if __name__ == "__main__":
    if sys.argv[1] == "test":
        print("max |F_1d - F_exact| =", selftest())
    else:
        tag = sys.argv[1]
        As = [float(v) for v in sys.argv[2].split(",")]
        s0s = [int(v) for v in sys.argv[3].split(",")]
        ps = [int(v) for v in sys.argv[4].split(",")]
        ns = [int(float(v)) for v in sys.argv[5].split(",")]
        seeds = int(sys.argv[6])
        jobs = [(a, s0, p, n, s) for a in As for s0 in s0s for p in ps for n in ns for s in range(seeds) if p <= n // 2]
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=7) as ex:
            rows = list(ex.map(run, jobs, chunksize=4))
        with open("D3_%s_raw.jsonl" % tag, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print("rows", len(rows), "secs", round(time.time() - t0, 1))
