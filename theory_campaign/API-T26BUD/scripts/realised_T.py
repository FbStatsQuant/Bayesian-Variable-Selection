"""API-T26BUD: realised stage count T_n of the v3 calibration at exact p = 18, and the quantities of Theorem G / Lemma P.

For each design, n, seed:
  * Problem (exact enumeration of gamma_0, d, pi_0, pi) from W2-T26's bvs_exact.py (copied unchanged).
  * PILOT exactly as v3_calib.h::pilot_next_phi (population ESS of exp((phi'-phi) d_i) >= 0.90 H_e; phi'=1 if it passes;
    else 60 halvings; floor 1/T_e), with H_e = ceil(512*N0/2500), N0 = max(2500, n, p), T_e = T0 = max(1000, ell^2)
    (tier 0); multinomial resampling and one v3 move round per stage (W2-T26 smc_sim.Sim.round, copied unchanged);
    then L burn-in + 4 measured rounds at phi = 1 (local search omitted: it only adds scored models near the best).
  * SCORED set: every model whose score the round evaluates (particle states, both Gibbs alternatives, swap and
    independence proposals). V = top 20p scored by log gamma_0  U  top 20p scored by log gamma_1  U {empty}
    (one construction, no rebuild loop: a documented proxy for the final V).
  * GRID exactly as v3_calib.h::build_grid with targets = pilot temperatures, on V and on V = Omega (all feasible).
  * Theorem G quantities: R(t) = sum_{S != S0} (g0(S)/g0(S0)) e^{t (d(S)-d(S0))}; eps0 = 0.9^{-1/2} - 1;
    eta* = sup{eta in (0,1]: R(1+eta) <= eps0} (needs R(0) <= eps0); bound_G = N_pilot + ceil(log2(1/eta*)).
  * Lemma P quantities: per pilot stage the 2%-trimmed d-range D_k = max_i d_i - (2% quantile of d_i) and the advance;
    check advance >= min(1 - phi, a/D_k), a = 0.5125 (f = 0.02 constant of Lemma P).
Usage: python realised_T.py design n seed      (prints one JSON line)
Seeds: data rng as W2-T26 premise_scan (default_rng(1000*di + seed + 7919*n)); orth uses di = 3;
       pilot rng default_rng(5*10**6 + 1000*seed + n).
"""
import sys, os, json, math
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bvs_exact import Problem
from premise_scan import design, P
from smc_sim import Sim

EPS0 = 0.9 ** -0.5 - 1.0
A_F = 0.5125  # 2*arccosh(0.98/sqrt(0.9)) rounded down


def design_orth(n, rng):
    X = rng.standard_normal((n, P))
    X -= X.mean(0)
    Q, _ = np.linalg.qr(X)
    X = Q * math.sqrt(n - 1)
    beta = np.zeros(P); S0 = [0, 6, 12]; beta[S0] = 0.6
    y = X @ beta + rng.standard_normal(n)
    return X, y, S0


def ess_frac(d, delta):
    x = delta * d
    return math.exp(2 * logsumexp(x) - logsumexp(2 * x) - math.log(len(d)))


def pilot_next_phi(d, phi, Te):
    if ess_frac(d, 1.0 - phi) >= 0.9:
        return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess_frac(d, mid - phi) >= 0.9: lo = mid
        else: hi = mid
    if lo - phi < 1.0 / Te:
        f = min(1.0, phi + 1.0 / Te)
        return (1.0 if f >= 1 - 1e-12 else f), True
    return lo, False


class ScoredSim(Sim):
    """Sim.round with a record of every evaluated model (scored set)."""
    def __init__(self, pr):
        super().__init__(pr)
        self.scored = np.zeros(1 << pr.p, dtype=bool)
        self._lg = Sim.lg

    def lg(self, S, phi):
        self.scored[S] = True
        return Sim.lg(self, S, phi)


def FV(lg0, d, t):
    return logsumexp(lg0 + t * d)


def rhoV(lg0, d, u, v):
    return math.exp(2 * FV(lg0, d, v) - FV(lg0, d, u) - FV(lg0, d, 2 * v - u))


def build_grid(lg0, d, targets, Te):
    targets = sorted(targets)
    grid = [0.0]; u = 0.0; nbis = 0
    while u < 1.0:
        b = next((t for t in targets if t > u), None)
        if b is None: return None, 'no_target', nbis
        if rhoV(lg0, d, u, b) >= 0.9:
            v = b
        else:
            nbis += 1
            lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if rhoV(lg0, d, u, mid) >= 0.9: lo, anyp = mid, True
                else: hi = mid
            if not anyp: return None, 'non_progress', nbis
            v = lo
        if v >= 1 - 1e-12: v = 1.0
        if not v > u: return None, 'non_progress', nbis
        if not rhoV(lg0, d, u, v) >= 0.9: return None, 'validation_failed', nbis
        grid.append(v)
        if len(grid) - 1 > Te: return None, 'too_many_intervals', nbis
        u = v
    return grid, 'ok', nbis


def main():
    name, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    names = ['fav_iid', 'fav_cor', 'masked', 'orth']
    di = names.index(name)
    rng = np.random.default_rng(1000 * di + seed + 7919 * n)
    X, y, S0 = design_orth(n, rng) if name == 'orth' else design(name, n, rng)
    pr = Problem(X, y, S0)
    p = pr.p
    N0 = max(2500, n, p); H = math.ceil(512 * N0 / 2500); Te = pr.T0
    feas = pr.feas
    lg0 = np.where(feas, pr.lg0, -np.inf); d = pr.d
    s0 = pr.S0
    # ---- Theorem G quantities (full space, reference S0) ----
    mask = feas.copy(); mask[s0] = False
    lr = pr.lg0[mask] - pr.lg0[s0]; e = d[mask] - d[s0]
    logR = lambda t: logsumexp(lr + t * e)
    R0, R1 = math.exp(logR(0.0)), math.exp(logR(1.0))
    eta = None
    if R0 <= EPS0 and R1 <= EPS0:
        if logR(2.0) <= math.log(EPS0): eta = 1.0
        else:
            lo, hi = 0.0, 1.0
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if logR(1 + mid) <= math.log(EPS0): lo = mid
                else: hi = mid
            eta = lo
    Delta = max(1 - pr.pi0[s0], 1 - pr.pi[s0])
    # ---- pilot ----
    prng = np.random.default_rng(5 * 10 ** 6 + 1000 * seed + n)
    sim = ScoredSim(pr)
    S = sim.draw0(H, prng)
    sim.scored[S] = True
    phi, temps, forced, lemP_ok, Dks, advances = 0.0, [], 0, True, [], []
    while phi < 1.0:
        dS = d[S]
        q2 = np.quantile(dS, 0.02, method='inverted_cdf')
        Dk = float(dS.max() - q2)
        nphi, f = pilot_next_phi(dS, phi, Te)
        forced += int(f)
        adv = nphi - phi
        need = min(1 - phi, A_F / Dk) if Dk > 0 else 1 - phi
        if adv < need - 1e-12: lemP_ok = False
        Dks.append(Dk); advances.append(adv)
        lw = (nphi - phi) * dS
        prob = np.exp(lw - logsumexp(lw))
        S = S[np.searchsorted(np.cumsum(prob), prng.random(H) * prob.sum(), side='right').clip(0, H - 1)]
        S = sim.round(S, nphi, prng)
        phi = nphi; temps.append(phi)
        if len(temps) > 5000: break
    for _ in range(pr.L + 4):
        S = sim.round(S, 1.0, prng)
    sc = np.nonzero(sim.scored & feas)[0]
    k = 20 * p
    top0 = sc[np.argsort(-pr.lg0[sc], kind='stable')[:k]]
    top1 = sc[np.argsort(-pr.lg1[sc], kind='stable')[:k]]
    V = np.unique(np.concatenate([top0, top1, [0]]))
    gV, stV, nbV = build_grid(lg0[V], d[V], temps, Te)
    F = np.nonzero(feas)[0]
    gF, stF, nbF = build_grid(lg0[F], d[F], temps, Te)
    Npil = len(temps)
    TV = len(gV) - 1 if gV else None
    TF = len(gF) - 1 if gF else None
    Dbar = max(Dks)
    out = dict(design=name, n=n, seed=seed, p=p, B=pr.B, H=H, Te=Te,
               one_minus_pi0=float(1 - pr.pi0[s0]), delta1=float(1 - pr.pi[s0]), Delta=float(Delta),
               R0=R0, R1=R1, eta_star=eta,
               N_pilot=Npil, forced=forced, pilot_temps=[round(t, 6) for t in temps[:30]],
               T_V=TV, status_V=stV, bisect_V=nbV, T_full=TF, status_full=stF, bisect_full=nbF,
               S0_in_V=bool(np.any(V == s0)), V_size=int(V.size), n_scored=int(sc.size),
               bound_G=(Npil + (0 if eta == 1.0 else math.ceil(math.log2(1 / eta)))) if eta else None,
               Dbar=Dbar, D1=Dks[0], bound_P=1 + math.ceil(Dbar / A_F), lemmaP_ok=lemP_ok,
               P1_TV=((TV + 1) * Delta) if TV else None, P1_Te=(Te + 1) * Delta,
               S0_is_HPM=bool(np.argmax(pr.lg1) == s0))
    print(json.dumps(out), flush=True)


if __name__ == '__main__':
    main()
