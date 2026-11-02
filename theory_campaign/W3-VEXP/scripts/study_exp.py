"""Study-scale (n = 200, p = 500) EXP' remainders and start-mass anatomy. Seed 20261102 + 10*sc + rep.

For scenario sc in {1,3,4,5,6}, signal scale c in {1, 0.5} (Y = c*signal + eps, as gen_dev_data.R), REPS designs:
  * the v3 partition (port), all block tables;
  * exact EXP' remainders R over EVERY within-block addition: max|R| over all, and over additions of a
    non-true variable (l not in S0);
  * Thm 1's explicit kappa_EXP (with M = ||mu||^2/n, sigma^2 = 1, phi0^2 = min_b lambda_min(R_{C_b}));
  * the data-computable Lemma 1.3 certificate  (1+phi^-2)/(2 phi^2 (n-1)) + nu (1.02 + 1/(n phi^2)) / min_b RSS^y_{C_b}
    (min over U subset C_b of RSS^y_U is attained at U = C_b);
  * log10 pi0(S0) (exact: capped convolution normaliser), the start mode (max-plus convolution over block sizes),
    the missing truths of the mode (with |theta_j| and the truth's block-level visibility), extras of the mode.
"""
import itertools, math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V
from scen import scenario_cov, truth

N = 200
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
SCS = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 3, 4, 5, 6]
p = 500
act, beta = truth(p)
th = np.zeros(p); th[act] = beta
S0 = set(int(a) for a in act)


def table_and_rss(sf, C):
    m = len(C)
    t = np.zeros(1 << m); rss = np.zeros(1 << m); rss[0] = sf.yty
    l0 = sf.logm_rel(())
    for k in range(1, m + 1):
        combs = np.array(list(itertools.combinations(range(m), k)))
        idx = np.array(C)[combs]
        codes = (1 << combs).sum(1)
        for st in range(0, len(idx), 4000):
            sl = slice(st, st + 4000)
            t[codes[sl]] = sf.logm_batch(idx[sl]) - l0
            Gs = sf.G[idx[sl][:, :, None], idx[sl][:, None, :]]
            zs = sf.z[idx[sl]]
            rss[codes[sl]] = sf.yty - np.einsum('ij,ij->i', zs, np.linalg.solve(Gs, zs[:, :, None])[:, :, 0])
    return t, rss


out = []
for sc in SCS:
    Sig = scenario_cov(sc, p); Lc = np.linalg.cholesky(Sig)
    for cs in (1.0, 0.5):
        for r in range(REPS):
            rng = np.random.default_rng(20261102 + 10 * sc + r)
            Z = rng.standard_normal((N, p)) @ Lc.T
            X = Z - Z.mean(0); X /= X.std(0, ddof=1)
            eps = rng.standard_normal(N)
            Y = cs * (X @ th) + eps
            Yc = Y - Y.mean(); y = Yc / Yc.std(ddof=1)
            G = X.T @ X
            sf = V.Suff(G, X.T @ y, y @ y, N)
            R = G / (N - 1)
            blocks = V.make_blocks(R, V.B_rule(N, p))
            mu = cs * (X @ th); mu -= mu.mean()
            M = mu @ mu / N
            phi2 = min(np.linalg.eigvalsh(R[np.ix_(C, C)]).min() for C in blocks)
            nu = sf.nu
            cst = 1 / (8 * (M + 2))
            kap = (1 + 1 / phi2) / (2 * phi2 * (N - 1)) + nu * (1.02 + 1 / (N * phi2)) / (cst * N)
            maxR = 0.0; maxR_null = 0.0; minrss = np.inf
            tabs = []
            for C in blocks:
                t, rss = table_and_rss(sf, C)
                tabs.append(t)
                minrss = min(minrss, rss[-1])
                m = len(C); codes = np.arange(1 << m)
                for i in range(m):
                    base = codes[(codes >> i & 1) == 0]
                    x = (rss[base] - rss[base | (1 << i)]) / rss[base]
                    Rm = t[base | (1 << i)] - t[base] + 0.5 * math.log(N + 1) + nu * np.log1p(-x)
                    a = np.abs(Rm).max(); maxR = max(maxR, a)
                    if C[i] not in S0: maxR_null = max(maxR_null, a)
            cert = (1 + 1 / phi2) / (2 * phi2 * (N - 1)) + nu * (1.02 + 1 / (N * phi2)) / minrss
            # start: profiles, normaliser, log pi0(S0), mode via max-plus convolution
            K = sf.K
            prof, mprof, marg = [], [], []
            for C, t in zip(blocks, tabs):
                m = len(C); kk = V.popcount(np.arange(1 << m))
                prof.append(np.array([np.logaddexp.reduce(t[kk == j]) for j in range(m + 1)]))
                mprof.append(np.array([t[kk == j].max() for j in range(m + 1)]))
                marg.append([int(np.arange(1 << m)[kk == j][np.argmax(t[kk == j])]) for j in range(m + 1)])
            F = np.array([0.0]); Fm = np.array([0.0]); back = []
            for pr, mp in zip(prof, mprof):
                nF = np.full(min(len(F) + len(pr) - 1, K + 1), -np.inf); nFm = nF.copy(); bk = np.zeros(len(nF), int)
                for j, q in enumerate(pr):
                    L = min(len(F), len(nF) - j)
                    if L <= 0: continue
                    nF[j:j + L] = np.logaddexp(nF[j:j + L], F[:L] + q)
                    cand = Fm[:L] + mp[j]
                    upd = cand > nFm[j:j + L]
                    nFm[j:j + L][upd] = cand[upd]; bk[j:j + L][upd] = j
                F, Fm = nF, nFm; back.append(bk)
            lw = np.array([V.logw(p, k) for k in range(len(F))])
            logZ = np.logaddexp.reduce(F + lw)
            k0 = int(np.argmax(Fm + lw))
            mode = []; kk = k0
            for b in range(len(blocks) - 1, -1, -1):
                j = back[b][kk]; code = marg[b][j]
                mode += [blocks[b][i] for i in range(len(blocks[b])) if code >> i & 1]
                kk -= j
            mode = set(mode)
            blk = {j: b for b, C in enumerate(blocks) for j in C}
            pos = {j: blocks[blk[j]].index(j) for j in range(p)}
            lg0 = V.logw(p, len(S0))
            for b, C in enumerate(blocks):
                code = sum(1 << pos[j] for j in S0 if blk[j] == b)
                lg0 += tabs[b][code]
            # exact pi0(R_d), d = 0,1,2: bivariate profiles e_b(k, j) (k = block size of U, j = #extras <= 2)
            F2 = np.full((1, 3), -np.inf); F2[0, 0] = 0.0
            for b, (C, t) in enumerate(zip(blocks, tabs)):
                m = len(C); codes = np.arange(1 << m); kk2 = V.popcount(codes)
                nullbits = sum(1 << i for i, j in enumerate(C) if j not in S0)
                ex = V.popcount(codes & nullbits)
                e2 = np.full((m + 1, 3), -np.inf)
                for k_ in range(m + 1):
                    for j_ in range(3):
                        sel = (kk2 == k_) & (ex == j_)
                        if sel.any(): e2[k_, j_] = np.logaddexp.reduce(t[sel])
                nF2 = np.full((min(F2.shape[0] + m, K + 1), 3), -np.inf)
                for k_ in range(m + 1):
                    for j_ in range(3):
                        if not np.isfinite(e2[k_, j_]): continue
                        Lk = min(F2.shape[0], nF2.shape[0] - k_)
                        if Lk <= 0: continue
                        for jj in range(3 - j_):
                            nF2[k_:k_ + Lk, jj + j_] = np.logaddexp(nF2[k_:k_ + Lk, jj + j_], F2[:Lk, jj] + e2[k_, j_])
                F2 = nF2
            lw2 = np.array([V.logw(p, k) for k in range(F2.shape[0])])
            Rd = [float(np.exp(np.logaddexp.reduce((F2[:, :d + 1] + lw2[:, None]).ravel()) - logZ)) for d in range(3)]
            # exact iid pi0 draws (backward sampler) -> distribution of |S n S0| and |S \ S0|
            pref = [np.array([0.0])]
            for pr in prof:
                Fp = pref[-1]; nF = np.full(min(len(Fp) + len(pr) - 1, K + 1), -np.inf)
                for j, q in enumerate(pr):
                    Lk = min(len(Fp), len(nF) - j)
                    if Lk > 0: nF[j:j + Lk] = np.logaddexp(nF[j:j + Lk], Fp[:Lk] + q)
                pref.append(nF)
            ntrue, nextra = [], []
            for dr in range(1000):
                lpk = pref[-1] + np.array([V.logw(p, k) for k in range(len(pref[-1]))])
                pk = np.exp(lpk - lpk.max()); kk_ = rng.choice(len(pk), p=pk / pk.sum())
                Sd = []
                for b in range(len(blocks) - 1, -1, -1):
                    m = len(blocks[b]); js = np.arange(min(m, kk_) + 1)
                    lpj = prof[b][js] + pref[b][np.minimum(kk_ - js, len(pref[b]) - 1)]
                    lpj[kk_ - js >= len(pref[b])] = -np.inf
                    pj = np.exp(lpj - lpj.max()); j = rng.choice(js, p=pj / pj.sum())
                    codes = np.arange(1 << m); sel = codes[V.popcount(codes) == j]
                    lt = tabs[b][sel]; pc = np.exp(lt - lt.max()); code = rng.choice(sel, p=pc / pc.sum())
                    Sd += [blocks[b][i] for i in range(m) if code >> i & 1]
                    kk_ -= j
                Sd = set(Sd); ntrue.append(len(Sd & S0)); nextra.append(len(Sd - S0))
            row = dict(S=sc, c=cs, rep=r, M=round(M, 2), phi0sq=round(float(phi2), 3), maxR=round(float(maxR), 3),
                       pi0_R0=round(Rd[0], 4), pi0_R1=round(Rd[1], 4), pi0_R2=round(Rd[2], 4),
                       draws_true_q10_50_90=[int(x) for x in np.quantile(ntrue, [.1, .5, .9])],
                       draws_extra_mean=round(float(np.mean(nextra)), 2),
                       maxR_null=round(float(maxR_null), 3), kappa_EXP=round(float(kap), 1), lemma13_cert=round(float(cert), 3),
                       log10_pi0S0=round(float((lg0 - logZ) / math.log(10)), 2),
                       mode_missing=sorted((int(j), float(th[j])) for j in S0 - mode), mode_extras=len(mode - S0),
                       mode_size=len(mode))
            print(json.dumps(row), flush=True); out.append(row)
json.dump(out, open(__file__.rsplit('/', 2)[0] + '/results/study_exp_%s.json' % '_'.join(map(str, SCS)), 'w'), indent=0)
