"""Prop. O check on ORTH at large p (no enumeration). Closed forms with X^T X = (n-1) I (g = n, as bvs_exact.all_log_m):
log BF(S) = -(|S|/2) log n - nu [log(2b0 + yy - sum_{j in S} z_j^2/n) - log(2b0 + yy)], nu = a0 + n/2; BB(1,p) prior as bvs_exact.
Blocks: contiguous blocks of size B = min(floor(sqrt n), floor(sqrt p), 16) (all correlations are 0 on ORTH, so the
method's clustering is a tie; contiguous is one valid tie-break). S0 = {0, B, 2B} (one signal in each of 3 blocks), theta = 0.6.
R_C(t) = sum over the class C = {S0 u E : 1 <= |E| <= 2} u {S0 \\ {k} u E : |E| <= 1} of r_S e^{t e_S}: a LOWER bound on R(t),
expected to carry its leading term. Reports log10 R_C(t) at t = 0, 1, 1.5, 2, and eta_C = sup{eta: R_C(1+eta) <= eps0}.
Usage: python orth_R.py A seeds  -> p = min(n-1, round(n^A)); seeds: default_rng(4242 + 100*seed + n)
"""
import sys, math, json
import numpy as np
from scipy.special import logsumexp, gammaln
A0 = B0 = 0.01
EPS0 = 0.9 ** -0.5 - 1


def run(n, p, seed):
    rng = np.random.default_rng(4242 + 100 * seed + n)
    X = rng.standard_normal((n, p)); X -= X.mean(0)
    Q, _ = np.linalg.qr(X); X = Q * math.sqrt(n - 1)
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    S0 = [0, B, 2 * B]
    y = X[:, S0] @ np.full(3, 0.6) + rng.standard_normal(n)
    y = (y - y.mean()) / y.std(ddof=1)
    z2 = (X.T @ y) ** 2 / n; yy = float(y @ y); nu = A0 + n / 2
    blk = np.arange(p) // B
    lw = lambda k: math.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    def lbf(sumz, k):  # log BF for a model with |S| = k and sum z^2/n = sumz
        return -0.5 * k * math.log(n) - nu * (np.log(2 * B0 + yy - sumz) - math.log(2 * B0 + yy))
    s0set = set(S0); nulls = np.array([j for j in range(p) if j not in s0set])
    # per-block signal sums
    bs = {}
    for j in S0: bs[blk[j]] = bs.get(blk[j], 0.0) + z2[j]
    Stot = sum(z2[S0])
    def odds(E, M):
        """vectors over candidate configurations: E = list of arrays of null indices (same length), M = removed signal or None"""
        k = 3 + len(E) - (0 if M is None else 1)
        sumz = Stot + sum(z2[e] for e in E) - (0 if M is None else z2[M])
        l1 = lw(k) - lw(3) + lbf(sumz, k) - lbf(Stot, 3)
        # block tables: changed blocks only
        l0 = lw(k) - lw(3)
        delta = {}
        contrib = np.zeros_like(np.asarray(sumz, dtype=float))
        # compute per-element block deltas
        blocks_E = [blk[e] for e in E]
        # start ratio = prod over changed blocks of r_b(new)/r_b(old)
        def lr_b(bsum_new, knew, bsum_old, kold):
            return lbf(bsum_new, knew) - lbf(bsum_old, kold)
        if len(E) == 0:
            b = blk[M]; base = bs[b]; kb = sum(1 for j in S0 if blk[j] == b)
            contrib = lr_b(base - z2[M], kb - 1, base, kb)
        else:
            # accumulate per-block modifications (handles same-block pairs)
            nE = len(E[0]); cnt = {}
            add_sum = [np.zeros(nE)]; 
            # generic: loop over unique block combos via arrays
            bsig = np.array([bs.get(b, 0.0) for b in range(blk.max() + 1)])
            ksig = np.bincount(blk[S0], minlength=blk.max() + 1)
            newsum = {}; 
            B1 = blocks_E[0]; s1 = z2[E[0]]
            if M is not None:
                bm = blk[M]
            if len(E) == 1:
                bsum_old = bsig[B1]; k_old = ksig[B1]
                bsum_new = bsum_old + s1; k_new = k_old + 1
                if M is not None:
                    same = B1 == bm
                    c = np.where(same, lr_b(bsum_new - z2[M], k_new - 1, bsum_old, k_old), lr_b(bsum_new, k_new, bsum_old, k_old))
                    c = c + np.where(same, 0.0, lr_b(bsig[bm] - z2[M], ksig[bm] - 1, bsig[bm], ksig[bm]))
                    contrib = c
                else:
                    contrib = lr_b(bsum_new, k_new, bsum_old, k_old)
            else:
                B2 = blocks_E[1]; s2 = z2[E[1]]; same = B1 == B2
                c_same = lr_b(bsig[B1] + s1 + s2, ksig[B1] + 2, bsig[B1], ksig[B1])
                c_diff = lr_b(bsig[B1] + s1, ksig[B1] + 1, bsig[B1], ksig[B1]) + lr_b(bsig[B2] + s2, ksig[B2] + 1, bsig[B2], ksig[B2])
                contrib = np.where(same, c_same, c_diff)
        return l0 + contrib, l1   # log r_S, log pi-odds
    logs = []
    logs.append(odds([nulls], None))
    for M in S0:
        logs.append(odds([], M)); logs.append(odds([nulls], M))
    iu, ju = np.triu_indices(len(nulls), 1)
    logs.append(odds([nulls[iu], nulls[ju]], None))
    lr = np.concatenate([np.atleast_1d(a) for a, _ in logs]); l1 = np.concatenate([np.atleast_1d(b) for _, b in logs])
    e = l1 - lr
    logR = lambda t: float(logsumexp(lr + t * e))
    out = dict(n=n, p=p, B=B, seed=seed, **{f'log10R_{t}': logR(t) / math.log(10) for t in (0, 1, 1.5, 2)})
    if max(logR(0), logR(1)) <= math.log(EPS0):
        if logR(2) <= math.log(EPS0): eta = 1.0
        else:
            lo, hi = 0.0, 1.0
            for _ in range(40):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if logR(1 + mid) <= math.log(EPS0) else (lo, mid)
            eta = lo
    else: eta = None
    out['eta_C'] = eta
    out['R2_single_extras'] = float(np.exp(logsumexp(logs[0][0] + 2 * (logs[0][1] - logs[0][0]))))
    return out


if __name__ == '__main__':
    A = float(sys.argv[1]); seeds = int(sys.argv[2])
    for n in [400, 1600, 6400, 25600]:
        p = min(n - 1, int(round(n ** A)))
        if p * p > 4e7: continue
        for s in range(seeds):
            print(json.dumps(run(n, p, s)), flush=True)
