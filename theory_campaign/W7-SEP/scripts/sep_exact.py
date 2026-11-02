"""W7-SEP main experiment (exact, p <= 20): start-only discovery vs search on LH.

Usage: python3 sep_exact.py CONFIG DESIGN REPS N1,N2,...   (seed = 20261102 + hash of args; fixed)
Per replicate (all exact, by enumeration of 2^p models):
  logpi0_S0, Mstat = log pi0(S0) + c log p + (c/2) log n, pi(S0), pi0(S°), mode_is_Sstar;
  iid start discovery: P(S0 among Q iid pi0 draws | data) = 1 - (1 - pi0(S0))^Q for
     Q_f = 4 N0 (L + 6) (the final run's minimal iid budget, 00_COMMON), and Q = n, n^2, n^3;
  one-shot importance correction: chi2(pi || pi0), KL(pi || pi0), per-draw relative variance of
     w(S)1{S = S0} (= 1/pi0(S0) - 1), ESS fraction 1/(1 + chi2);
  search: LS0 (production local search from the start mode S~0) scores S0?;
     pi0(basin) = sum of pi0(C) over centres C from which the search scores S0
        (= per-draw success probability of "iid pi0 draw + production local search");
     fraction of all centres in 2^R (R = non-null groups) / in 2^[p] from which the search scores S0;
     max moves used from centres in 2^R; number of local maxima of F other than S0.
Output: ../results/sep_<CONFIG>_<DESIGN>.jsonl
"""
import sys, json, math, zlib
import numpy as np
from scipy.special import logsumexp
from sep_core import *

cfgname, design, reps = sys.argv[1], sys.argv[2], int(sys.argv[3])
ns = [int(x) for x in sys.argv[4].split(",")]
seed = 20261102 + zlib.crc32(f"{cfgname}{design}".encode()) % 100000
rng = np.random.default_rng(seed)
cfg = make_config(cfgname)
out = open(f"../results/sep_{cfgname}_{design}.jsonl", "a")

def log1mexp_neg(x):  # log(1 - e^x), x < 0
    return math.log(-math.expm1(x)) if x > -0.693 else math.log1p(-math.exp(x))

for n in ns:
    for r in range(reps):
        d = build(cfg, n, rng, design)
        p = d["p"]; c = len(d["M"])
        sc = scores(d); F, lp0, lp, pc, K = sc["F"], sc["log_pi0"], sc["log_pi"], sc["pc"], sc["K"]
        S0m, Ssm = mask_of(d["S0"]), mask_of(d["Sstar"])
        l0 = lp0[S0m]
        mode = int(np.argmax(lp0))
        # iid start discovery
        N0 = max(2500, n, p); L = max(4, math.ceil(math.log2(n + 1)))
        budgets = {"Qf": 4 * N0 * (L + 6), "n": n, "n2": n ** 2, "n3": n ** 3}
        lmiss = log1mexp_neg(l0)
        hit = {k: -math.expm1(Q * lmiss) for k, Q in budgets.items()}
        # importance correction
        fin = np.isfinite(lp0)
        chi2p1 = float(np.exp(logsumexp(2 * lp[fin] - lp0[fin])))
        KL = float(np.sum(np.exp(lp[fin]) * (lp[fin] - lp0[fin])))
        # search
        ell = math.ceil(math.log2(n + p + 1))
        succ = successor(F, p, K, pc)
        near = near_mask(p, K, pc, S0m)
        hitls, endc, moves = ls_scores_S0(succ, near, ell)
        allm = np.arange(1 << p)
        Rm = mask_of(d["R"])
        inR = (allm & ~Rm) == 0
        feas = pc <= K
        locmax = (succ == allm) & feas
        nloc = int(locmax.sum()) - int(locmax[S0m])
        rec = dict(cfg=cfgname, design=design, n=n, p=p, c=c, rep=r,
                   logpi0_S0=float(l0), Mstat=float(l0 + c * math.log(p) + 0.5 * c * math.log(n)),
                   pi_S0=float(math.exp(lp[S0m])), pi0_Sstar=float(math.exp(lp0[Ssm])),
                   mode_is_Sstar=bool(mode == Ssm), mode=list(set_of(mode, p)),
                   Qstar=float(math.exp(-l0)), budgets=budgets, hit=hit,
                   chi2=chi2p1 - 1.0, log_chi2p1=math.log(chi2p1), KL=KL,
                   relvar_per_draw=float(math.expm1(-l0)), ess_frac=1.0 / chi2p1,
                   ls0_scores_S0=bool(hitls[mode]), ls0_moves=int(moves[mode]),
                   pi0_basin=float(np.exp(logsumexp(lp0[hitls & feas]))) if (hitls & feas).any() else 0.0,
                   frac_R_centres=float(hitls[inR & feas].mean()), n_R_fail=int((~hitls[inR & feas]).sum()),
                   frac_all_centres=float(hitls[feas].mean()), n_all_fail=int((~hitls[feas]).sum()),
                   max_moves_R=int(moves[inR & feas].max()), n_local_max_other=nloc,
                   ell=ell, K=K)
        # characterise failing centres (if any) in 2^R
        fails = np.flatnonzero(inR & feas & ~hitls)
        if len(fails):
            ends = np.unique(endc[fails])
            rec["fail_ends"] = [[list(set_of(int(e), p)), float(F[e] - F[S0m])] for e in ends[:5]]
        out.write(json.dumps(rec) + "\n"); out.flush()
        print(cfgname, design, n, r, f"log10pi0S0={l0/math.log(10):.2f} piS0={rec['pi_S0']:.3f} "
              f"LS0={rec['ls0_scores_S0']} basin={rec['pi0_basin']:.4f} fracR={rec['frac_R_centres']:.4f} "
              f"fracAll={rec['frac_all_centres']:.4f} hitQf={hit['Qf']:.3g}", flush=True)
