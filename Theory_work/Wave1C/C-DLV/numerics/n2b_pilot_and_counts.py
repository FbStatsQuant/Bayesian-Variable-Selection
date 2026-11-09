"""N2b: (a) Lemma 3.3 pilot cap: exact port of pilot_next_phi (float64, as coded) on random particle d-vectors,
   re-drawn each stage (adversarial: heavy spreads), count stages <= Te and last phi == 1.0;
   (b) Lemma 5.2' trial counts: two-model families with remainder controlled only on [0, 1+eta] (eta = 0.25)."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
mp.mp.dps = 60
def F(A, d, t): return mp.log(mp.fsum(mp.e ** (a + t * x) for a, x in zip(A, d)))
def rho(A, d, u, v): return mp.e ** (2 * F(A, d, v) - F(A, d, u) - F(A, d, 2 * v - u))
def q(A, d, t, i): return mp.e ** (A[i] + t * d[i] - F(A, d, t))
def build_grid(A, d, targets, Te):
    targets = sorted(targets); grid = [mp.mpf(0)]; u = mp.mpf(0); nb = 0
    while u < 1:
        b = next((t for t in targets if t > u), None)
        if b is None: return grid, "no_target", nb
        if rho(A, d, u, b) >= 0.9: v = b
        else:
            nb += 1; lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = (lo + hi) / 2
                if rho(A, d, u, mid) >= 0.9: lo, anyp = mid, True
                else: hi = mid
            if not anyp: return grid, "non_progress", nb
            v = lo
        if v >= 1 - mp.mpf(10) ** -12: v = mp.mpf(1)
        if not v > u: return grid, "non_progress", nb
        if not rho(A, d, u, v) >= 0.9: return grid, "validation_failed", nb
        grid.append(v)
        if len(grid) - 1 > Te: return grid, "too_many", nb
        u = v
    return grid, "ok", nb
def lse(x):
    m = max(x); return m + math.log(sum(math.exp(v - m) for v in x))
def ess(d, delta):
    x = [delta * v for v in d]; return math.exp(2 * lse(x) - lse([2 * v for v in x]))
def next_phi(d, phi, H, Te):
    thr = 0.9 * H
    if ess(d, 1.0 - phi) >= thr: return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess(d, mid - phi) >= thr: lo = mid
        else: hi = mid
    if lo - phi < 1.0 / Te:
        f = min(1.0, phi + 1.0 / Te)
        if f >= 1.0 - 1e-12: f = 1.0
        return f, True
    return lo, False
rng = random.Random(7); viol = 0; maxratio = 0; runs = 0
for trial in range(300):
    Te = rng.choice([7, 13, 50, 1000]); H = rng.choice([20, 64, 200])
    phi = 0.0; k = 0
    while phi != 1.0:
        scale = 10 ** rng.uniform(-1, 5)
        d = [rng.gauss(0, scale) for _ in range(H)]
        phi, _ = next_phi(d, phi, H, Te); k += 1
        if k > Te + 5: break
    runs += 1; maxratio = max(maxratio, k / Te)
    if k > Te or phi != 1.0: viol += 1
print(f"(a) pilot runs {runs}, violations of k<=Te & end at 1: {viol}, max k/Te {maxratio:.3f}")
# (b)
th = mp.mpf(0.9) / mp.mpf(0.99) ** 2; s0 = 2 * mp.atanh(mp.sqrt(1 - th)); lam = mp.log(th / (1 - th)); eta = mp.mpf("0.25")
tested = 0; v = 0; worst = 0
for trial in range(250):
    D = mp.mpf(10) ** rng.uniform(0, 3.5); x0 = -mp.mpf(10) ** rng.uniform(-1, 3)
    A = [mp.mpf(0), x0]; d = [mp.mpf(0), D]
    # a third model that overtakes beyond t = 1 + eta (controlled only on [0, 1+eta])
    tc = mp.mpf(rng.uniform(1.3, 1.9)); slope = D * mp.mpf(rng.uniform(1.5, 4))
    # line l3(t) = l2(t) + (t - tc)*(slope - D) - 5 ;  at t = tc it is 5 nats below M2
    A.append(x0 - tc * (slope - D) - 5); d.append(slope)
    rt = max(1 - q(A, d, t, 0) - q(A, d, t, 1) for t in [(1 + eta) * k / 300 for k in range(301)])
    if rt > 0.01: continue
    tested += 1
    pts = sorted(set(rng.random() for _ in range(rng.randint(0, 10))))
    tg = [mp.mpf(x) for x in pts] + [mp.mpf(1)]
    g, why, nb = build_grid(A, d, tg, 10 ** 6)
    bound = 1 + mp.ceil((2 * lam + 2 * s0) / (s0 / 2)) + mp.ceil(mp.log(max(1, (-x0 - lam) / (2 * s0))) / mp.log(mp.mpf(4) / 3)) + mp.ceil(mp.log((1 + eta) / eta) / mp.log(mp.mpf(4) / 3))
    worst = max(worst, nb / bound)
    if nb > bound or why != "ok": v += 1; print("viol", float(D), float(x0), float(tc), nb, float(bound), why)
print(f"(b) Lemma 5.2' families tested {tested}, violations {v}, worst N_b/bound {float(worst):.3f}")
