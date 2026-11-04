"""W2_PC2: R2_C C8 'pilot extension' and §R3 stage-count row.
Claim: if every particle discrepancy lies in an interval of length <= D_* and 2^-60 <= h/2 (h = 2 c_rho / D_*),
the coded pilot (v3_calib.h pilot_next_phi: ESS 0.9 H, 60 halvings, floor 1/T_e) advances >= h/2 at every non-final
step, so P <= ceil(2/h)+1; with the checked grid count T <= P + ceil(2/h_V) + 1 this gives T <= 2 ceil(D_*/c_rho) + 2.
Test: adversarial populations re-drawn at every pilot step (two-point extremes, uniform, skewed), T_e in {2,10,1000},
D in [1e-3, 200]; then the coded build_grid on random finite (lg0, d) sets V with osc_V d <= D using those pilot targets.
Fixed seeds; < 1 min."""
import math
import numpy as np
c_rho = math.sqrt(math.log(10 / 9))


def lse(x):
    m = np.max(x); return m + math.log(np.exp(x - m).sum())


def ess_frac(dv, delta):
    x = delta * dv; return math.exp(2 * lse(x) - lse(2 * x)) / len(dv)


def pilot_next_phi(dv, phi, Te):
    if ess_frac(dv, 1.0 - phi) >= 0.90: return 1.0
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess_frac(dv, mid - phi) >= 0.90: lo = mid
        else: hi = mid
    if lo - phi < 1.0 / Te:
        f = min(1.0, phi + 1.0 / Te)
        return 1.0 if f >= 1.0 - 1e-12 else f
    return lo


def rhoV(lg0, d, u, v):
    return math.exp(2 * lse(lg0 + v * d) - lse(lg0 + u * d) - lse(lg0 + (2 * v - u) * d))


def build_grid(lg0, d, targets, Te):
    grid, u = [0.0], 0.0
    while u < 1.0:
        b = next((t for t in sorted(targets) if t > u), None)
        if b is None: return None
        if rhoV(lg0, d, u, b) >= .9: v = b
        else:
            lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = .5 * (lo + hi)
                if rhoV(lg0, d, u, mid) >= .9: lo, anyp = mid, True
                else: hi = mid
            if not anyp: return None
            v = lo
        if v >= 1 - 1e-12: v = 1.0
        if not v > u or not rhoV(lg0, d, u, v) >= .9: return None
        grid.append(v); u = v
        if len(grid) - 1 > Te: return None
    return grid


rng = np.random.default_rng(31)
bad_step = bad_P = bad_T = bad_T2 = 0; nruns = ngrids = 0; worst = 0.0
for it in range(600):
    D = float(np.exp(rng.uniform(math.log(1e-3), math.log(200))))
    Te = int(rng.choice([2, 10, 1000]))
    h = 2 * c_rho / D
    N = int(rng.choice([50, 300]))
    phi, targets = 0.0, []
    while phi < 1.0:
        kind = rng.integers(3)
        if kind == 0:
            dv = np.where(rng.random(N) < rng.uniform(.05, .95), D, 0.0)
        elif kind == 1:
            dv = rng.uniform(0, D, N)
        else:
            dv = D * rng.beta(.3, 3, N)
        dv = dv + rng.normal(0, 100)  # arbitrary location
        new = pilot_next_phi(dv, phi, Te)
        if new < 1.0 and new - phi < h / 2 - 1e-15: bad_step += 1
        worst = max(worst, (h / 2) / max(new - phi, 1e-300) if new < 1 else 0)
        targets.append(new); phi = new
    P = len(targets); nruns += 1
    if P > math.ceil(2 / h) + 1: bad_P += 1
    # grid on a random restricted set V with osc_V d <= D
    m = int(rng.integers(2, 40))
    dV = rng.uniform(0, D, m); dV[0], dV[1] = 0.0, rng.uniform(0, D)
    lg0V = rng.normal(0, 3, m)
    g = build_grid(lg0V, dV, targets, 10 ** 6)
    if g is not None:
        ngrids += 1; T = len(g) - 1; DV = dV.max() - dV.min()
        hV = 2 * c_rho / DV if DV > 0 else float('inf')
        if T > P + (math.ceil(2 / hV) if DV > 0 else 0) + 1: bad_T += 1
        if T > 2 * math.ceil(D / c_rho) + 2: bad_T2 += 1
print(f"pilot runs={nruns}; non-final steps advancing < h/2: {bad_step}; P > ceil(2/h)+1: {bad_P}; "
      f"max (h/2)/step = {worst:.3f}")
print(f"grids built={ngrids}; T > P+ceil(2/h_V)+1: {bad_T}; T > 2ceil(D/c_rho)+2: {bad_T2}")
