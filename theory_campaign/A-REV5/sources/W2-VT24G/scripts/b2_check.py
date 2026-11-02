"""W2-VT24G: independent test of Prop. B2 at a = 1 (phase 2, superset family S_1 = {S0} u {S0+l}).
For a = 1 every bad step is an exit from S_1 (truth removal or null addition), so
  P_W(no exit during the round and S0 not scored) <= P_W(no bad, no progress) <= eps_del + H_1     (Prop. B2)
must hold at every W = S0+l.  We compute exactly (exact per-label laws):
  eps_del(1) = max_l o_l(S0+l)                                   (W1's definition)
  h(l) = 1/2 [P_U(neutral removal of l) + B P_N(neutral removal of l) + P_I(jump to S0+l', l' != l)]
  H_1 = max_l min{h(l), (B+2)/(B+3)}
  c2 = 1 - eps_del - H_1 (W1) and c2' = 1 - H_1 (W2 sharpening: eps_del is not needed when |P| = 1, because
  the G_l execution at S0+l scores S0 by SR whatever its draw)
  eta2(1) = sum over labels of max_l P_{S0+l}(label exits S_1)
and Monte Carlo (20000 rounds per state) of P_W(no exit and not scored). Data seed 1. RNG seed 4242."""
import sys, json, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import make_data, Model, mask_to_list
from exact_laws import gibbs_law, uswap_law, nswap_law, indep_accept


def main(out):
    rng = np.random.default_rng(4242)
    recs = []
    for scen in [1, 2, 3, 4, 5, 6]:
        for c in [1.0, 0.5]:
            X, y, S0 = make_data(scen, c, seed=1)
            M = Model(X, y, S0)
            ar = np.arange(1 << M.p, dtype=np.int64)
            ext = M.sizes[ar & ~np.int64(S0)]
            inS1 = ((ar & S0) == S0) & (ext <= 1)
            nul = [l for l in range(M.p) if not S0 >> l & 1]
            eps_del = 0.0; Hs = []; worst_mc = 0.0; worst_gap = 1.0; eta_lab = {}
            rows = []
            for l in nul:
                W = S0 | (1 << l)
                o = gibbs_law(M, W, l).get(W, 0.0)
                eps_del = max(eps_del, o)
                lu = uswap_law(M, W); ln = nswap_law(M, W); ai = indep_accept(M, W)
                neutral = lambda law: sum(pr for yy, pr in law.items() if yy != W and inS1[yy] and yy != S0)
                pi_ = float(ai[inS1 & (ar != S0) & (ar != W)].sum())
                h = 0.5 * (neutral(lu) + M.B * neutral(ln) + pi_)
                Hs.append(min(h, (M.B + 2) / (M.B + 3)))
                # exit probabilities per label (for eta2)
                for j in range(M.p):
                    e = sum(pr for yy, pr in gibbs_law(M, W, j).items() if not inS1[yy])
                    eta_lab['G%d' % j] = max(eta_lab.get('G%d' % j, 0), e)
                eta_lab['U'] = max(eta_lab.get('U', 0), sum(pr for yy, pr in lu.items() if not inS1[yy]))
                eta_lab['N'] = max(eta_lab.get('N', 0), sum(pr for yy, pr in ln.items() if not inS1[yy]))
                eta_lab['I'] = max(eta_lab.get('I', 0), float(ai[~inS1].sum()))
                _, sc, ex = M.round(np.full(20000, W, dtype=np.int64), rng, target=S0, region=inS1)
                mc = float((~sc & ~ex).mean())
                rows.append((l, mc, h))
            H1 = max(Hs)
            eta2 = sum(v for k, v in eta_lab.items() if k != 'N') + M.B * eta_lab['N']
            c2 = 1 - eps_del - H1; c2s = 1 - H1
            mcmax = max(r[1] for r in rows)
            rec = dict(scen=scen, c=c, B=M.B, eps_del=eps_del, H1=H1, c2_W1=c2, c2_sharpened=c2s,
                       floor=1 / (M.B + 3), eta2=eta2, mc_max_no_exit_not_scored=mcmax,
                       B2_bound_W1=eps_del + H1, B2_bound_sharp=H1,
                       consistent_W1=mcmax <= eps_del + H1 + 0.01, consistent_sharp=mcmax <= H1 + 0.01)
            recs.append(rec); print(json.dumps(rec), flush=True)
    json.dump(recs, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
