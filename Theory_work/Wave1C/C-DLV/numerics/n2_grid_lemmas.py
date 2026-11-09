"""C-DLV N2: falsification tests for L3 (Lemma 3.1 identity, Lemma 3.2 bound, Prop 3.5 dominance) and L5
(Lemma 5.1 closed form and bounds, Lemma 5.2 insertion bound), using an exact port of build_grid (psi_enum.py) in
high precision (mpmath, 60 digits) to stay close to EX-A. Random families; prints violation counts."""
import math, random, sys, os
import mpmath as mp
mp.mp.dps = 60
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

C0 = mp.log(mp.mpf(10) / 9)


def F(A, d, t):
    return mp.log(mp.fsum(mp.e ** (a + t * x) for a, x in zip(A, d)))


def rho(A, d, u, v):
    return mp.e ** (2 * F(A, d, v) - F(A, d, u) - F(A, d, 2 * v - u))


def q(A, d, t, i):
    return mp.e ** (A[i] + t * d[i] - F(A, d, t))


def build_grid(A, d, targets, Te):
    targets = sorted(targets); grid = [mp.mpf(0)]; u = mp.mpf(0); nb = 0
    while u < 1:
        b = next((t for t in targets if t > u), None)
        if b is None:
            return grid, "no_target", nb
        if rho(A, d, u, b) >= 0.9:
            v = b
        else:
            nb += 1; lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = (lo + hi) / 2
                if rho(A, d, u, mid) >= 0.9:
                    lo, anyp = mid, True
                else:
                    hi = mid
            if not anyp:
                return grid, "non_progress", nb
            v = lo
        if v >= 1 - mp.mpf(10) ** -12:
            v = mp.mpf(1)
        if not v > u:
            return grid, "non_progress", nb
        if not rho(A, d, u, v) >= 0.9:
            return grid, "validation_failed", nb
        grid.append(v)
        if len(grid) - 1 > Te:
            return grid, "too_many", nb
        u = v
    return grid, "ok", nb


def pilot_like(rng):
    k = rng.randint(1, 12)
    pts = sorted(set(rng.random() for _ in range(k - 1)))
    return [mp.mpf(x) for x in pts] + [mp.mpf(1)]


rng = random.Random(20261108)
viol = dict(identity=0, bound32=0, dominance=0, closed=0, b51=0, nb52=0, pilot=0)
# T1: identity & Lemma 3.2 bound on random families
for trial in range(300):
    m = rng.randint(2, 8)
    A = [mp.mpf(rng.gauss(0, 5)) for _ in range(m)]; d = [mp.mpf(rng.gauss(0, 30)) for _ in range(m)]
    u = mp.mpf(rng.random()); v = u + mp.mpf(rng.random()) * (1 - u)
    r = rho(A, d, u, v)
    for M in range(m):
        alt = q(A, d, u, M) * q(A, d, 2 * v - u, M) / q(A, d, v, M) ** 2
        if abs(alt - r) > mp.mpf(10) ** -40 * (1 + r):
            viol["identity"] += 1
    # sup variance on [u, 2v-u] by fine grid (lower estimate of sup) -> bound must hold with the true sup;
    ts = [u + (2 * v - 2 * u) * k / 400 for k in range(401)]
    sv = max((mp.fsum(q(A, d, t, i) * d[i] ** 2 for i in range(m)) - mp.fsum(q(A, d, t, i) * d[i] for i in range(m)) ** 2) for t in ts)
    Dl = -mp.log(r)
    if Dl > (v - u) ** 2 * sv * (1 + mp.mpf("1e-3")) + mp.mpf("1e-30"):
        viol["bound32"] += 1
# T2: dominance version of Prop 3.5(a)
for trial in range(200):
    m = rng.randint(2, 6)
    A = [mp.mpf(0)] + [mp.mpf(-rng.uniform(3, 12)) for _ in range(m - 1)]
    d = [mp.mpf(0)] + [mp.mpf(rng.uniform(-3, 3)) for _ in range(m - 1)]
    if q(A, d, 0, 0) >= mp.sqrt(0.9) and q(A, d, 2, 0) >= mp.sqrt(0.9):
        tg = pilot_like(rng)
        g, why, nb = build_grid(A, d, tg, 1000)
        if why != "ok" or nb != 0:
            viol["dominance"] += 1
# T3: Lemma 5.1 closed form and bounds
for trial in range(2000):
    x = mp.mpf(rng.uniform(-30, 30)); s = mp.mpf(rng.uniform(0, 20)); a = mp.e ** x; c = mp.e ** s
    sig = lambda z: mp.e ** z / (1 + mp.e ** z)
    r2 = sig(x) * sig(x + 2 * s) / sig(x + s) ** 2
    cf = 1 - a * (c - 1) ** 2 / ((1 + a) * (1 + a * c * c))
    if abs(r2 - cf) > mp.mpf(10) ** -40:
        viol["closed"] += 1
    one = 1 - cf
    if one > mp.tanh(s / 2) ** 2 + 1e-40 or one > 1 / (1 + a) + 1e-40 or one > a * c * c / (1 + a * c * c) + 1e-40:
        viol["b51"] += 1
# T4: Lemma 5.2 bound on two-model families with an eps-remainder
th = mp.mpf(0.9) / mp.mpf(0.99) ** 2; s0 = 2 * mp.atanh(mp.sqrt(1 - th)); lam = mp.log(th / (1 - th))
worst = 0
for trial in range(400):
    D = mp.mpf(10) ** rng.uniform(0, 4); x0 = mp.mpf(-10) ** 0 * -mp.mpf(10) ** rng.uniform(-1, 3)
    A = [mp.mpf(0), x0]; d = [mp.mpf(0), D]
    # remainder models: far below both lines on [0,2] so that r_t <= 0.01
    for _ in range(rng.randint(0, 4)):
        A.append(mp.mpf(-60) - mp.mpf(rng.uniform(0, 20))); d.append(mp.mpf(rng.uniform(-1, 1)) * D)
    rt = max(1 - q(A, d, t, 0) - q(A, d, t, 1) for t in [mp.mpf(k) / 200 for k in range(401)])
    if rt > 0.01:
        continue
    tg = pilot_like(rng)
    g, why, nb = build_grid(A, d, tg, 10 ** 6)
    bound = 1 + mp.ceil((2 * lam + 2 * s0) / (s0 / 2)) + mp.ceil(mp.log(max(1, (-x0 - lam) / (2 * s0))) / mp.log(mp.mpf(4) / 3))
    worst = max(worst, nb / bound)
    if nb > bound or why not in ("ok",):
        viol["nb52"] += 1
        print("viol 5.2", float(D), float(x0), nb, float(bound), why)
print("violations:", viol, " worst N_b/bound:", float(worst))
