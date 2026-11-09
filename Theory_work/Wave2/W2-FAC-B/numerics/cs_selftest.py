"""cs_selftest: (a) cs_core.F == fac_core.ExactGram.F on random sets; (b) cs path == general-scanner path from [p]."""
import math, numpy as np
import fac_core as fc, cs_core as cc
class FakeRng:
    def __init__(self, seq): self.seq = list(seq)
    def standard_normal(self, k=None):
        v = self.seq.pop(0); return v
    def chisquare(self, df): return self.seq.pop(0)
worst_F, agree = 0.0, 0
for trial, (rho, n, p, c) in enumerate([(0.3, 400, 60, 1.0), (0.6, 2000, 80, 0.5), (0.9, 10**6, 50, 1.0), (0.3, 130, 64, 1.0)]):
    rng = np.random.default_rng(trial)
    th = np.zeros(p); th[[2, 26, 33]] = c * np.array([1.4, -1.0, 1.8])
    xi = rng.standard_normal(p); eta = float(rng.standard_normal()); chi = float(rng.chisquare(n - 1 - p))
    Pc = cc.CS(rho, th, n, xi=xi, eta=eta, chi=chi)
    Sigma, Lam, Psi = fc.factor_sigma(p, math.sqrt(rho) * np.ones(p), (1 - rho) * np.ones(p))
    Pg = fc.ExactGram(Sigma, th, n, FakeRng([np.array([eta]), xi, chi]), Lam=Lam, Psi=Psi)
    for _ in range(300):
        T = tuple(sorted(rng.choice(p, int(rng.integers(0, p + 1)), replace=False).tolist()))
        worst_F = max(worst_F, abs(Pc.F(T) - Pg.F(T)))
    pc = cc.ls0_path_cs(Pc)
    pg = fc.ls0_path(Pg, tuple(range(p)), Pc.S0)
    # reconstruct general path sets
    same = (pc["final"] == pg["final"]) and len(pc["moves"]) == pg["moves"]
    agree += same
    print(trial, "moves cs/gen", len(pc["moves"]), pg["moves"], "final equal", pc["final"] == pg["final"], "final=S0", pc["final_is_S0"])
print("max |F_cs - F_general| =", worst_F, " paths agree:", agree, "/4")
