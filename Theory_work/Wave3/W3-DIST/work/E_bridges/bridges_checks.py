"""W3-DIST stream E -- numerical sanity checks for B0, B1, B2-core, B2, B3 and the Example.
DRAFT (by this seat, unchecked). Run:  python3 bridges_checks.py  (< 1 min). Output: bridges_checks_out.txt
Each check prints PASS/FAIL; nothing here is a proof.
"""
import itertools, math, sys
import numpy as np

rng = np.random.default_rng(20261115)
out = []
def report(name, ok, detail=""):
    out.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

# ---------- N1: arithmetic of the constants ----------
# B1: exponents n*delta^2/(32K^4) (lower, delta=1/4), n*delta^2/(64K^4) (upper, delta=1/3), n/(8K^4) (mean)
lo, up, mean = (1/4)**2/32, (1/3)**2/64, 1/8
report("B1 exponents >= 1/576", min(lo, up, mean) >= 1/576 - 1e-15, f"lower={lo:.6g}, upper={up:.6g}, mean={mean:.6g}, 1/576={1/576:.6g}")
# B2-core net step: (sqrt(1-delta) - eps*sqrt(1+delta')/(1-eps))^2 >= 1/2 with delta=1/5, delta'=1, eps=1/10
val = (math.sqrt(4/5) - 0.1*math.sqrt(2)/0.9)**2
report("B2-core net inequality", val >= 0.5, f"value={val:.6f}")
# B2-core per-point exponents: lower delta^2/256 = 1/6400, upper 1/768
report("B2-core per-point exponent", abs(min((1/5)**2/256, 1/768) - 1/6400) < 1e-15, f"min={min((1/5)**2/256, 1/768):.6g}")
# union: log 2 * c2 + 2 log 21 * c2 + c2 <= 1/6400 ? (with L >= 1, log count <= 2 log21 L, log2 <= log2 L)
c2 = 1e-5
lhs = (math.log(2) + 2*math.log(21) + 2)*c2  # proof needs (log2 + 1 + 2log21)c2 + c2 <= 1/6400
report("B2-core union constant c2=1e-5", lhs <= 1/6400, f"(log2+2log21+2)c2={lhs:.4g} <= 1/6400={1/6400:.4g}")

# ---------- N2: window coverage m_n(M log n) + s <= ceil(C_q M log n) (and the bound used for m#_n) ----------
def m_n_uncapped(t, s0, p, n):
    return s0 + math.ceil((s0*math.log(2*p) + ((s0+2)/2)*math.log(n+1) + 3*t)/math.log(2))
worst = None; ok = True; cnt = 0
for s in range(0, 31):
    for A in [1, 1.25, 1.5, 2, 3, 5, 10]:
        Cq = 2*(s*(A+2)+4)/math.log(2)
        for logn in np.linspace(math.log(2), math.log(1e15), 80):
            n = math.exp(logn); n_int = max(2, int(round(n)))
            p = float(n_int)**A  # worst case p = n^A (m_n increases in p)
            for M in [1, 1.0001, 1.5, 2, 3, 7.3, 10, 100, 1e4]:
                lhs = m_n_uncapped(M*math.log(n_int), s, p, n_int) + s   # s0 = s is the worst case
                rhs = math.ceil(Cq*M*math.log(n_int))
                cnt += 1
                if lhs > rhs:
                    ok = False; worst = (s, A, n_int, M, lhs, rhs)
report("window coverage (grid)", ok, f"{cnt} cases; counterexample={worst}")
# B3: (2A+3)s+2 <= C_q log n for n>=3
ok = all((2*A+3)*s+2 <= 2*(s*(A+2)+4)/math.log(2)*math.log(3) for s in range(0, 200) for A in np.linspace(1, 50, 200))
report("B3: (2A+3)s+2 <= C_q log 3", ok)

# ---------- N3: one-column determinant ratio (interlacing) ----------
def Dval(G, n):
    lam = np.linalg.eigvalsh(G) if G.size else np.array([])
    return np.prod(((n+1)*lam + 1)/(lam + 1))
ok = True; minrat = np.inf
for trial in range(3000):
    n = int(rng.integers(3, 60)); k = int(rng.integers(0, 6))
    X = rng.standard_normal((n, k+1))
    if trial % 3 == 0:  # near-collinear last column
        X[:, -1] = X[:, :k].sum(axis=1) * (1 if k else 0) + 10**(-rng.uniform(0, 4))*rng.standard_normal(n)
    X = X - X.mean(axis=0); X = X/np.linalg.norm(X, axis=0)*math.sqrt(n-1)
    G1 = X.T @ X; G0 = G1[:k, :k]
    lam1 = np.linalg.eigvalsh(G1)[0]
    phi = ((n+1)*lam1 + 1)/(lam1 + 1)
    rat = Dval(G1, n)/Dval(G0, n)
    minrat = min(minrat, rat/phi)
    if rat < phi*(1 - 1e-9): ok = False
report("D_{S+j}/D_S >= phi(lambda_min(G_{S+j}))", ok, f"min ratio/phi = {minrat:.6f}")

# ---------- N4: Example: AR and equal-correlation principal blocks ----------
ok = True; worstgap = np.inf
for rho in [-0.95, -0.7, -0.3, 0.0, 0.3, 0.7, 0.95]:
    psi = (1-abs(rho))/(1+abs(rho))
    for trial in range(300):
        P = 200; k = int(rng.integers(1, 30))
        T = np.sort(rng.choice(P, size=k, replace=False))
        R = rho**np.abs(T[:, None]-T[None, :]).astype(float)
        lm = np.linalg.eigvalsh(R)[0]
        worstgap = min(worstgap, lm - psi)
        if lm < psi - 1e-12: ok = False
report("AR(rho) principal blocks: lambda_min >= (1-|rho|)/(1+|rho|)", ok, f"min(lambda_min - psi) = {worstgap:.3g}")
ok = True
for rho in [0, 0.2, 0.5, 0.9, 0.99]:
    for k in [1, 2, 5, 50]:
        R = (1-rho)*np.eye(k) + rho*np.ones((k, k))
        if np.linalg.eigvalsh(R)[0] < 1-rho-1e-12: ok = False
report("equal correlation: lambda_min >= 1 - rho", ok)

# ---------- N5: B2-core empirical (far from the proof constants; sanity only) ----------
def b2core_min(Z, q):
    """min over supports |T|=q of lambda_min( Gamma_T^{+1/2} What_T Gamma_T^{+1/2} ) on range(Gamma_T),
    with w = (1, z_T), Gamma_T = E w w^T computed from the known population correlation."""
    n, p = Z.shape
    best = np.inf
    for T in itertools.combinations(range(p), q):
        W = np.column_stack([np.ones(n), Z[:, T]])
        What = W.T @ W / n
        Gam = np.zeros((q+1, q+1)); Gam[0, 0] = 1; Gam[1:, 1:] = Corr[np.ix_(T, T)]
        ev, V = np.linalg.eigh(Gam); keep = ev > 1e-10
        Vr = V[:, keep]; isq = Vr @ np.diag(ev[keep]**-0.5) @ Vr.T
        B = Vr.T @ isq @ What @ isq @ Vr
        best = min(best, np.linalg.eigvalsh(B)[0])
    return best
n, p, q = 400, 14, 3
# (a) Gaussian AR(0.8)
Corr = 0.8**np.abs(np.subtract.outer(np.arange(p), np.arange(p))).astype(float)
L = np.linalg.cholesky(Corr)
Z = rng.standard_normal((n, p)) @ L.T
v = b2core_min(Z, q); report("B2-core empirical, Gaussian AR(0.8), n=400, p=14, q=3", v >= 0.5, f"min ratio = {v:.3f}")
# (b) independent Rademacher (K = 1)
Corr = np.eye(p); Z = rng.choice([-1.0, 1.0], size=(n, p))
v = b2core_min(Z, q); report("B2-core empirical, Rademacher, n=400, p=14, q=3", v >= 0.5, f"min ratio = {v:.3f}")
# (c) degenerate direction: z_1 = z_0 exactly (Corr singular), Gaussian
Corr = np.eye(p); Corr[0, 1] = Corr[1, 0] = 1.0
Z = rng.standard_normal((n, p)); Z[:, 1] = Z[:, 0]
v = b2core_min(Z, q); report("B2-core empirical, duplicated column (singular Corr)", v >= 0.5, f"min ratio on range = {v:.3f}")

# ---------- N6: B1 empirical ----------
n, p = 60, 2000
Z = rng.uniform(-math.sqrt(3), math.sqrt(3), size=(n, p))   # unit variance, sub-Gaussian
r = Z.var(axis=0, ddof=1)
report("B1 empirical, uniform, n=60, p=2000", (r.min() >= 0.5) and (r.max() <= 2), f"range of s_j^2/Var = [{r.min():.3f}, {r.max():.3f}]")

# ---------- N7: B0 pathwise equivariance on a small coded posterior ----------
def coded_posterior(xr, yr):
    n, p = xr.shape
    sd = xr.std(axis=0, ddof=1); X = (xr - xr.mean(axis=0))/sd
    U = np.linalg.qr(np.column_stack([np.ones(n), rng_fixed.standard_normal((n, n-1))]))[0][:, 1:]
    yc = U.T @ yr; Xc = U.T @ X; N = n-1
    sy2 = yc @ yc / N; b = 0.01*sy2; nu = 0.01 + n/2; K = min(p, n//2)
    res = {}
    for k in range(0, K+1):
        for S in itertools.combinations(range(p), k):
            S = list(S)
            if k:
                G = X[:, S].T @ X[:, S]; H = (n+1)*G + np.eye(k)
                D = np.linalg.det(H)/np.linalg.det(G + np.eye(k))
                mean = n*np.linalg.solve(H, Xc[:, S].T @ yc)
                Q = yc @ yc - yc @ Xc[:, S] @ mean
                cov_unit = n*np.linalg.inv(H)
            else:
                D = 1.0; mean = np.zeros(0); Q = yc @ yc; cov_unit = np.zeros((0, 0))
            w = 0.5/math.comb(2*p-1, k)
            logw = math.log(w) - 0.5*math.log(D) - nu*math.log(2*b + Q)
            res[tuple(S)] = dict(logw=logw, mean=mean, rate=b + Q/2, cov_unit=cov_unit, sd=sd[S], xbar=xr.mean(axis=0)[S], ybar=yr.mean())
    lw = np.array([r["logw"] for r in res.values()]); lw = np.exp(lw - lw.max()); lw /= lw.sum()
    for (S, r), pS in zip(res.items(), lw): r["pi"] = pS
    return res
rng_fixed = np.random.default_rng(1)
n, p = 12, 4
xr = rng.standard_normal((n, p)) @ np.diag([1, 3, 0.5, 2]) + 5
alpha, sigma = 2.7, 3.9
ytil = xr @ np.array([0.6, 0.0, -1.1, 0.0]) + rng.standard_normal(n)
yr = alpha + sigma*ytil
rng_fixed = np.random.default_rng(1); P1 = coded_posterior(xr, ytil)
rng_fixed = np.random.default_rng(1); P2 = coded_posterior(xr, yr)
ok = True; maxdev = 0.0
for S in P1:
    a, b_ = P1[S], P2[S]
    maxdev = max(maxdev, abs(a["pi"] - b_["pi"]), np.max(np.abs(sigma*a["mean"] - b_["mean"]), initial=0)/max(1, np.max(np.abs(b_["mean"]), initial=1)),
                 abs(sigma**2*a["rate"] - b_["rate"])/b_["rate"])
    # one draw: (theta, v) for ytil; mapped draw (sigma theta, sigma^2 v) for yr; plug-in intercepts and mean functions
    th = a["mean"] + 0.3; v = 0.8
    btil = th/a["sd"]; atil = a["ybar"] - a["xbar"] @ btil
    bR = sigma*th/b_["sd"]; aR = b_["ybar"] - b_["xbar"] @ bR
    maxdev = max(maxdev, abs(aR - (alpha + sigma*atil)), np.max(np.abs(bR - sigma*btil), initial=0))
ok = maxdev < 1e-8
report("B0: pi(S) invariant, posterior mean/rate equivariant, a_hat(y^r) = alpha* + sigma* a_hat(ytil)", ok, f"max deviation = {maxdev:.2e}")
# Hellinger invariance under y -> alpha + sigma y (closed form)
def H2(m1, v1, m2, v2):
    return 1 - math.sqrt(2*math.sqrt(v1*v2)/(v1+v2))*math.exp(-(m1-m2)**2/(4*(v1+v2)))
dev = 0.0
for _ in range(1000):
    m1, m2 = rng.standard_normal(2)*3; v1, v2 = rng.uniform(0.05, 5, 2)
    dev = max(dev, abs(H2(m1, v1, m2, v2) - H2(alpha + sigma*m1, sigma**2*v1, alpha + sigma*m2, sigma**2*v2)))
report("B0: H^2 invariant under the affine map", dev < 1e-12, f"max deviation = {dev:.1e}")
# Lemma H-style quadrature check of the closed form (one case)
m1, v1, m2, v2 = 0.4, 1.7, -0.2, 0.9
yy = np.linspace(-30, 30, 400001)
f = np.exp(-(yy-m1)**2/(2*v1))/math.sqrt(2*math.pi*v1); g = np.exp(-(yy-m2)**2/(2*v2))/math.sqrt(2*math.pi*v2)
quad = 1 - np.trapezoid(np.sqrt(f*g), yy)
report("closed-form H^2 vs quadrature", abs(quad - H2(m1, v1, m2, v2)) < 1e-8, f"{quad:.10f} vs {H2(m1, v1, m2, v2):.10f}")

text = "\n".join(out)
print(text)
with open(__file__.replace(".py", "_out.txt"), "w") as fh:
    fh.write(text + "\n")
