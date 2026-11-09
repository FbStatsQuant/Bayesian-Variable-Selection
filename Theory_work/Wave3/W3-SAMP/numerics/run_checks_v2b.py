"""W3-SAMP v2b: a concentrated, regression-realisable case for Theorem C / LT# (appended to RESULTS_v2.txt)."""
import numpy as np, sys
from samp_sim import run_islands, exact_quantities
sys.argv = ["x"]
src = open("run_checks_v2.py", encoding="utf-8").read()
exec(src.split("def zs(")[0])  # imports, rng(seed 7), regression_model
rng = np.random.default_rng(11)
for n, beta in ((200, [0.5, 0.4]), (400, [0.5, 0.4])):
    M = regression_model(n=n, p=6, S0=[0, 3], beta=beta, rho=0.0, blocks=[[0, 1, 2], [3, 4, 5]], B=2, rng=rng)
    ex = exact_quantities(M)
    print(f"[reg-concentrated n={n}] delta={ex['delta']:.3e} o1={ex['o1']:.3e} o0={ex['o0']:.3e} pi0(S0)={M.pi0[M.S0]:.4f} kappa0={ex['kappa0']:.2e}")
    for T in (1, 5, 20):
        R = run_islands(M, list(np.linspace(0, 1, T + 1)), N=4, L=2, I=20000, rng=rng)
        W = R["W"]; err = np.abs(R["rb"] - ex["ind"]).max(1)
        x = 1 - R["Abr"]; U = x.sum(1)
        print(f"  T={T:2d} T*dbar={T*ex['dbar']:.3f}: E|W-1|={np.abs(W-1).mean():.4f} (bound {2*ex['o1']+8*(T+1)*ex['dbar']:.4f}); "
              f"E min(U,1)={np.minimum(U,1).mean():.4f} (bound {4*(T+1)*ex['dbar']:.4f}); P(W<.5)={(W<.5).mean():.4f}; "
              f"max RB err (95%)={np.quantile(err,.95):.2e}; P(MPM wrong)={(np.abs(np.where(R['rb']>0.5,1,0)-ex['ind']).max(1)>0).mean():.4f}; "
              f"P(S0 not drawn initially)={(R['Abr'][:,0]==0).mean():.4f}")
