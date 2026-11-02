"""W3-PGD core: population/sample greedy-dominance engine (batched, numpy only).

Objects (notation of 00_COMMON.md and W1-T37R/PROOF.md):
  Sig      : correlation (Gram/N) matrix on a candidate column set C (indices 0..c-1),
             population Sigma or the realised R = X'X/(n-1).
  theta    : length-c vector, nonzero exactly on the truth positions (theta* on the standardised scale).
  Delta_T  = theta' Schur_{S0|T} theta  (= ||(I-P_T) mu||^2/(n-1) for the realised design).
For a state S (sorted index tuple) the engine returns, for every feasible flip/swap of S, the
population residual reduction  red(S -> S') = Delta_S - Delta_S'  and classifies moves:
  progress     : add truth, delete extra, swap extra->truth
  non-progress : add null, delete truth, swap truth->anything, swap extra->null
R+(S) = max progress reduction, R0(S) = max non-progress reduction (W1-T37R Theorem C).
PGD(eta) on a region: R0 <= (1-eta) R+ for every state with m(S) >= 1.

Identities used (population regression algebra, Sig_{.|S} = residual covariance given S):
  W = Sig_{C,S} Sig_SS^{-1};  rc = Sig_{.|S} theta;  dg = diag Sig_{.|S}
  add x:     red = rc_x^2 / dg_x
  delete i:  red = -(W_{.,i}' theta)^2 / K_ii            (K = Sig_SS^{-1})
  Sig_{.|S-i} = Sig_{.|S} + W_{.,i} W_{.,i}' / K_ii       (rank-one 'un-conditioning')
  swap i->x: red = -(W_{.,i}'theta)^2/K_ii + (rc^{(i)}_x)^2 / dg^{(i)}_x.
Also returned: TRC ratio min_{u in U, j in M} a_u(S+j-u)/a_j(S), GERC = max_l ERC(S,l) (optional),
and the finite-n 'population score' margin with Fbar(T) = -nu log(sigma2 (N-|T|)/N + Delta_T) - pen(|T|).
"""
import itertools
import numpy as np
from math import lgamma, log, comb

NEG = -np.inf


def lchoose(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


def scenario_covariance(scenario, p):
    """Verbatim port of Scripts/Data_generators/gen_dev_data.R::scenario_covariance."""
    group = np.ceil(np.arange(1, p + 1) / 5).astype(int)
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if scenario == 1:
        return I
    if scenario == 2:
        idx = np.arange(p)
        return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if scenario == 3:
        return 0.7 * H + 0.3 * I
    if scenario == 4:
        return 0.85 * H + 0.15 * I
    if scenario == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scenario == 6:
        rho = 0.4 + 0.1 * ((group - 1) % 6)
        S = H * rho[:, None]
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError(scenario)


def truth(p):
    """Port of gen_dev_data.R::truth (0-based indices)."""
    s0, step = {30: (5, 1), 500: (14, 7), 1000: (14, 13)}[p]
    pos = [3, 2, 4, 1, 5, 3]
    pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0)
    block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k])
    beta = np.array([pattern[i % 6] for i in k])
    return active - 1, beta


def gen_design(p, scenario, n=200, seed=0, L=None):
    """Python re-implementation of gen_prod_data.R (same law, NOT the same bits: R's RNG is not reproduced).
    raw X ~ N(0, Sigma) rows, X = scale(raw X) (sd with n-1), signal = X beta, eps ~ N(0,1)."""
    rng = np.random.default_rng(seed)
    if L is None:
        L = np.linalg.cholesky(scenario_covariance(scenario, p))
    Xr = rng.standard_normal((n, p)) @ L.T
    X = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
    eps = rng.standard_normal(n)
    return X, eps


# ------------------------------------------------------------------ penalties
def penalties(n, p):
    """pen(k) = 1/2 k log(n+1) - log w(k)  (w = BB(1,p) per-model weight, up to the common W_K)."""
    K = min(p, n // 2)
    logw = np.array([-log(2) - lchoose(2.0 * p - 1, k) for k in range(K + 2)])
    return 0.5 * np.arange(K + 2) * log(n + 1) - logw


# ------------------------------------------------------------------ batched evaluation
class Engine:
    def __init__(self, Sig, theta, truth_pos, n=None, sigma2=1.0, p_prior=None, nu_extra=0.01):
        self.Sig = np.asarray(Sig, float)
        self.c = self.Sig.shape[0]
        self.theta = np.asarray(theta, float)
        self.tpos = np.asarray(truth_pos, int)
        self.is_truth = np.zeros(self.c, bool)
        self.is_truth[self.tpos] = True
        self.bvec = self.Sig @ self.theta
        self.tSt = float(self.theta @ self.bvec)
        self.diag = np.diag(self.Sig).copy()
        self.n = n
        if n is not None:
            self.N = n - 1
            self.nu = n / 2 + nu_extra
            self.sigma2 = sigma2
            self.pen = penalties(n, p_prior if p_prior is not None else self.c)

    def batch(self, idx, want_erc=False, want_fbar=False):
        """idx: (B, s) int array of sorted distinct candidate indices (s >= 0). Returns dict of arrays."""
        idx = np.asarray(idx, int)
        B, s = idx.shape
        c = self.c
        Sig, th = self.Sig, self.theta
        inS = np.zeros((B, c), bool)
        if s:
            np.put_along_axis(inS, idx, True, axis=1)
        tr_in = self.is_truth[None, :] & inS                       # truths in S
        tr_out = self.is_truth[None, :] & ~inS                     # missing truths M
        null_out = ~self.is_truth[None, :] & ~inS
        m = tr_out.sum(1)
        out = dict(m=m, e=(inS & ~self.is_truth[None, :]).sum(1), s=s)
        if s == 0:
            rc = np.broadcast_to(self.bvec, (B, c)).copy()
            dg = np.broadcast_to(self.diag, (B, c)).copy()
            Delta = np.full(B, self.tSt)
        else:
            SSS = Sig[idx[:, :, None], idx[:, None, :]]
            K = np.linalg.inv(SSS)
            SCS = np.transpose(Sig[:, idx], (1, 0, 2))               # (B, c, s)
            W = SCS @ K                                                # (B, c, s)
            bS = self.bvec[idx]                                        # (B, s)
            rc = self.bvec[None, :] - np.einsum('bcs,bs->bc', W, bS)
            dg = self.diag[None, :] - np.einsum('bcs,bcs->bc', W, SCS)
            Delta = self.tSt - np.einsum('bs,bs->b', bS, np.einsum('bst,bt->bs', K, bS))
        dg_safe = np.where(inS, 1.0, np.maximum(dg, 1e-300))
        add_red = np.where(inS, NEG, rc ** 2 / dg_safe)               # (B, c)
        out['Delta'] = Delta
        # ---- progress / non-progress maxima
        Rp = np.where(tr_out, add_red, NEG).max(1)
        R0 = np.where(null_out, add_red, NEG).max(1)
        R0_type = np.where(np.isfinite(R0), 1, 0)                     # 1 = add null
        if s:
            Kd = np.einsum('bss->bs', K)
            wth = np.einsum('bcs,c->bs', W, th)
            cost = wth ** 2 / Kd                                       # Delta_{S-i} - Delta_S
            sel_truth = self.is_truth[idx]                             # (B, s) item i is a truth
            del_red = -cost
            # deletes
            Rp = np.maximum(Rp, np.where(~sel_truth, del_red, NEG).max(1))
            dtr = np.where(sel_truth, del_red, NEG).max(1)
            R0_type = np.where(dtr > R0, 2, R0_type); R0 = np.maximum(R0, dtr)
            # swaps
            RC = rc[:, :, None] + W * (wth / Kd)[:, None, :]
            DG = dg[:, :, None] + W ** 2 / Kd[:, None, :]
            okx = ~inS[:, :, None]
            sw = np.where(okx, -cost[:, None, :] + RC ** 2 / np.maximum(DG, 1e-300), NEG)  # (B, c, s)
            xt = self.is_truth[None, :, None]
            it = sel_truth[:, None, :]
            prog_sw = np.where(~it & xt, sw, NEG).max((1, 2))         # extra -> truth
            Rp = np.maximum(Rp, prog_sw)
            t2t = np.where(it & xt, sw, NEG).max((1, 2))             # truth -> truth
            t2n = np.where(it & ~xt, sw, NEG).max((1, 2))            # truth -> null
            e2n = np.where(~it & ~xt, sw, NEG).max((1, 2))           # extra -> null
            for code, v in ((3, t2t), (4, t2n), (5, e2n)):
                R0_type = np.where(v > R0, code, R0_type); R0 = np.maximum(R0, v)
            # TRC: a_u(S+j-u)/a_j(S) for u truth in S, j missing truth
            num = cost[:, None, :] - RC ** 2 / np.maximum(DG, 1e-300) + add_red[:, :, None]
            den = add_red[:, :, None]
            mask = it & xt & okx
            ratio = np.where(mask & (den > 0), num / np.where(den > 0, den, 1.0), np.inf)
            out['TRC'] = ratio.min((1, 2))
        else:
            out['TRC'] = np.full(B, np.inf)
            sw = None
        out['Rp'] = Rp; out['R0'] = R0; out['R0_type'] = R0_type
        # ---- GERC (optional)
        if want_erc:
            T = self.tpos
            if s:
                SigTC = Sig[T, :]                                      # (t, c)
                RT = SigTC[None] - np.einsum('bts,bcs->btc', W[:, T, :], SCS)   # Sig_{T,C|S}
            else:
                RT = np.broadcast_to(Sig[T, :], (B, len(T), c)).copy()
            miss = tr_out[:, T]                                        # (B, t)
            RTT = RT[:, :, T]
            mm = miss[:, :, None] & miss[:, None, :]
            eye = np.eye(len(T))[None]
            A = np.where(mm, RTT, eye)
            rhs = np.where(miss[:, :, None], RT, 0.0)                  # (B, t, c)
            coef = np.linalg.solve(A, rhs)
            dj = np.sqrt(np.maximum(np.where(miss, np.einsum('btt->bt', RTT), 0.0), 0))
            erc = np.einsum('btc,bt->bc', np.abs(coef), dj) / np.sqrt(dg_safe)
            erc = np.where(null_out, erc, NEG)
            out['GERC'] = erc.max(1)
        # ---- finite-n population-score margin
        if want_fbar:
            N, nu, s2, pen = self.N, self.nu, self.sigma2, self.pen
            def Fb(D, k):
                return -nu * np.log(s2 * (N - k) / N + D) - pen[k]
            F_S = Fb(Delta, s)
            fa = np.where(inS, NEG, Fb(Delta[:, None] - np.where(inS, 0, add_red), s + 1))
            Pm = np.where(tr_out, fa, NEG).max(1)
            Om = np.maximum(F_S, np.where(null_out, fa, NEG).max(1))
            if s:
                fd = Fb(Delta[:, None] + cost, s - 1)
                Pm = np.maximum(Pm, np.where(~sel_truth, fd, NEG).max(1))
                Om = np.maximum(Om, np.where(sel_truth, fd, NEG).max(1))
                fs = np.where(okx, Fb(Delta[:, None, None] - np.where(okx, sw, 0), s), NEG)
                Pm = np.maximum(Pm, np.where(~it & xt, fs, NEG).max((1, 2)))
                Om = np.maximum(Om, np.where(it | ~xt, fs, NEG).max((1, 2)))
            out['Fbar_margin'] = Pm - Om
        return out


TYPE_NAMES = {0: 'none', 1: 'add_null', 2: 'del_truth', 3: 'swap_truth->truth', 4: 'swap_truth->null',
              5: 'swap_extra->null'}


def region_batches(truth_pos, extras, a, d, batch=4000, amin=0):
    """Yield (B, s) index batches enumerating R_{a,d}(extras) = {U u P : |S0\\U| <= a, P subset extras, |P|<=d},
    restricted to m(S) >= amin. Batches have constant size s."""
    T = list(truth_pos)
    s0 = len(T)
    for mm in range(amin, a + 1):
        for q in range(0, d + 1):
            s = s0 - mm + q
            buf = []
            for M in itertools.combinations(T, mm):
                U = [t for t in T if t not in M]
                for P in itertools.combinations(extras, q):
                    buf.append(sorted(U + list(P)))
                    if len(buf) == batch:
                        yield np.array(buf, int).reshape(len(buf), s)
                        buf = []
            if buf:
                yield np.array(buf, int).reshape(len(buf), s)


def region_size(s0, a, D, d, amin=0):
    return sum(comb(s0, mm) for mm in range(amin, a + 1)) * sum(comb(D, q) for q in range(d + 1))
