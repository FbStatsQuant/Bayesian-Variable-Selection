"""Adversarial check of Lemma UD (uniform improving null deletion) on the two-tail family
U(nb,nt) = S0 + {nb lowest-xi nulls} + {nt highest-xi nulls}, which contains, for each centre x and radius,
the maximal 'all-far' configurations {|xi-x|>=r}. For each U the exact best null-deletion gain is computed
(nearest-to-centre null, exact F differences). Also the balance identity sum_U (xi-x_U) = x_U+eta+eps_U is checked.
Output: lemma_check_out.json."""
import math, json, sys
import numpy as np
from pathsim import Model

res = []
for n in [int(x) for x in sys.argv[1].split(',')]:
    for c in (0.6, 0.98):
        for s0 in (1, 2):
            for seed in (0, 1):
                m = Model(n, c, s0, seed); K = m.K; p = m.p
                order = np.argsort(m.xi[s0:]) + s0
                xs = m.xi[order]; ws = m.w[order]
                P1 = np.concatenate([[0], np.cumsum(ws)]); P2 = np.concatenate([[0], np.cumsum(ws ** 2)])
                tw1 = m.w[:s0].sum(); tw2 = (m.w[:s0] ** 2).sum(); txi = m.xi[:s0].sum()
                N = len(xs); logn = math.log(n)
                grid = sorted(set([0] + [int(round(v)) for v in np.geomspace(1, K - s0, 70)]))
                worst = {}; max_bal_err = 0.0; global_min = (1e9, None)
                kstar = None
                for nb in grid:
                    for nt in grid:
                        if nb + nt == 0 or nb + nt > K - s0: continue
                        k = s0 + nb + nt
                        W1 = tw1 + P1[nb] + (P1[N] - P1[N - nt]); W2 = tw2 + P2[nb] + (P2[N] - P2[N - nt])
                        x = m.centre_w(k, W1); Fc = m.F(k, W1, W2)
                        # balance identity
                        S = txi + xs[:nb].sum() + xs[N - nt:].sum()
                        bal = (S - k * x) - (x + m.eta); max_bal_err = max(max_bal_err, abs(bal))
                        pos = int(np.searchsorted(xs, x)); cand = {nb - 1, N - nt, pos - 1, pos, pos + 1}
                        best = -1e300
                        for i in cand:
                            if 0 <= i < N and (i < nb or i >= N - nt):
                                g = m.F(k - 1, W1 - ws[i], W2 - ws[i] ** 2) - Fc
                                best = max(best, g)
                        Delta = m.pen[k - 1] - m.pen[k]
                        b = int(math.log2(k))
                        rec = worst.get(b)
                        val = best / logn
                        if rec is None or val < rec[0]:
                            worst[b] = (val, k, nb, nt, (Delta - best) / logn, Delta / logn)
                        if val < global_min[0]: global_min = (val, dict(k=k, nb=nb, nt=nt))
                res.append(dict(n=n, c=c, s0=s0, seed=seed, logn=logn, global_min_bestdel_over_logn=global_min[0], at=global_min[1],
                                max_balance_identity_err=max_bal_err,
                                by_dyadic_k={str(2 ** b): dict(min_bestdel_over_logn=v[0], k=v[1], nb=v[2], nt=v[3], minloss_over_logn=v[4], Delta_over_logn=v[5]) for b, v in sorted(worst.items())}))
                print(n, c, s0, seed, 'min best-del/log n = %.3f' % global_min[0], global_min[1], 'bal err %.1e' % max_bal_err)
json.dump(res, open('lemma_check_out.json', 'w'), indent=1)
