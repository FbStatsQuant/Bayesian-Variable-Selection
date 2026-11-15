"""Opus R1 scratch: independent checks of constants in Lemma W(ii), Lemma R, Claim C (all n >= 200), Claim B limit."""
import math, numpy as np
from scipy import integrate, special
import mpmath as mp

print("== Lemma W(ii): c_d sqrt(2pi) in [(d-1)/d, sqrt((d-1)/d)], and E W, E W^2 bounds")
worst = 0
for d in [3,4,5,10,50,199,1000,10**5]:
    cd = math.exp(special.gammaln(d/2) - special.gammaln((d-1)/2)) / math.sqrt(math.pi*d)
    v = cd*math.sqrt(2*math.pi)
    ok = (d-1)/d - 1e-15 <= v <= math.sqrt((d-1)/d) + 1e-15
    if not ok: print("  FAIL c_d", d, v)
    for tau in np.linspace(0.1, min(d/2, 600), 7):
        h = lambda t: cd*(1-t*t/d)**((d-3)/2)
        EW = integrate.quad(lambda t: math.exp(t*t/2)*h(t), -math.sqrt(tau), math.sqrt(tau), limit=200)[0]
        EW2 = integrate.quad(lambda t: math.exp(t*t)*h(t), -math.sqrt(tau), math.sqrt(tau), limit=200)[0]
        lo = math.sqrt(2*tau/math.pi)*(1-1/d)*math.exp(-tau**2/(2*d))
        hi = math.sqrt(2*tau/math.pi)*math.exp(tau/2)*math.exp(3*tau/(2*d))
        if EW < lo*(1-1e-9) or EW2 > hi*(1+1e-9): print("  FAIL", d, tau, EW, lo, EW2, hi)
        worst = max(worst, lo/EW, EW2/hi)
print("  max of (lower bound/EW, EW2/upper bound) =", worst, "(must be <= 1)")

print("== Lemma R: (1-e)e^{e/2} <= 1 - e/2 <= (1-e/4)^2 on (0,1)")
e = np.linspace(1e-6, 1-1e-6, 100001)
print("  max (1-e)e^{e/2} - (1-e/2):", float(((1-e)*np.exp(e/2) - (1-e/2)).max()),
      " max (1-e/2)-(1-e/4)^2:", float(((1-e/2)-(1-e/4)**2).max()))

print("== Claim C constants for every integer n in [200, 2e6] (exact k = ceil(12 log n))")
bad = []
for n in list(range(200, 20001)) + list(np.unique(np.logspace(np.log10(20001), np.log10(2e6), 4000).astype(int))):
    L = math.log(n); k = math.ceil(12*L); p = k+2; K = min(p, n//2)
    if not (p <= n//2 and k+1 <= n-1): bad.append(("F1", n))
    m = k//2
    # exact R^T_m n^2 (log domain)
    lq = [math.log(0.5) + math.lgamma(p+1)-math.lgamma(j+1)-math.lgamma(p-j+1) - (math.lgamma(2*p)-math.lgamma(j+1)-math.lgamma(2*p-j)) for j in range(p+1)]
    lw2 = -math.log(2) - (math.lgamma(2*p)-math.lgamma(3)-math.lgamma(2*p-2))
    tail = sum(math.exp(lq[j]) for j in range(m+1, K+1))
    R = tail/math.exp(lw2)
    if R*n*n > 1: bad.append(("R", n, R*n*n))
    # envelope used in the proof
    env = 3.78*(12*L+3)**2*n**-2.158
    if env > 1: bad.append(("env", n, env))
    # D_T bound
    eta = n**-2.0; c2 = 1/(1+eta*eta*k)
    trG = 2*(n-1); detG = (n-1)**2*(1-c2)
    DT = (1+(n+1)*trG+(n+1)**2*detG)/(1+trG+detG)
    if DT > 2*n: bad.append(("DT", n))
    if R*math.sqrt(DT)*math.sqrt(n) > n**-0.5: bad.append(("A", n))
    # log count bound: (3p-1) log 2 + (k/2) log n <= 12 L^2
    if (3*p-1)*math.log(2) + (k/2)*L > 12*L*L: bad.append(("count", n))
    # Delta constants: 4(k+1)/(1200 L^2) <= 0.0078 ;  (n-1)/(8n) >= 0.1243 ; 1/n <= 0.005
    if 4*(k+1)/(1200*L*L) > 0.0078: bad.append(("Delta1", n, 4*(k+1)/(1200*L*L)))
    if (n-1)/(8*n) < 0.1243 or 1/n > 0.005: bad.append(("Delta2", n))
print("  violations:", bad[:10], "count", len(bad))
print("  0.975/40 >= 1/42:", 0.975/40 >= 1/42, "; 1/42 - 1/100 >= 1/73:", 1/42-1/100 >= 1/73, (1/42-1/100), 1/73)
print("  log(1+x) >= 0.975x on [0,1/20]:", all(math.log1p(x) >= 0.975*x for x in np.linspace(0, 0.05, 10001)))

print("== Lemma P / reference cost at n=200, k=64 in mpmath (eta = n^-2): min over theta of B_T and the P bound")
mp.mp.dps = 50
n, k = 200, 64; eta = mp.mpf(n)**-2; c = 1/mp.sqrt(1+eta**2*k); b = mp.mpf(1)
# coordinates in the orthonormal basis (u1, u3..u_{k+2}) scaled: x1 = sqrt(n-1) e0, x_j = sqrt(n-1) e_j
s = mp.sqrt(n-1)
def vec_x(j):
    v = mp.zeros(k+1, 1)
    if j == 1: v[0] = s
    elif j == 2:
        v[0] = c*s
        for i in range(1, k+1): v[i] = -c*eta*s
    else: v[j-2] = s
    return v
mu = mp.zeros(k+1, 1)
for i in range(1, k+1): mu[i] = b/mp.sqrt(k)*s
def minB(S, full=True):
    XS = mp.matrix(k+1, len(S))
    for a, j in enumerate(S):
        v = vec_x(j)
        for i in range(k+1): XS[i, a] = v[i]
    G = XS.T*XS
    # B(t) = |mu - XS t|^2 + (|XS t|^2 + |t|^2)/n  (full) or |mu - XS t|^2 + |t|^2/n
    M = G + (G + mp.eye(len(S)))/n if full else G + mp.eye(len(S))/n
    rhs = XS.T*mu
    t = mp.lu_solve(M, rhs)
    r = mu - XS*t
    val = (r.T*r)[0] + ((((XS*t).T*(XS*t))[0] if full else 0) + (t.T*t)[0])/n
    return val
BT = minB([1, 2])
print("  min_theta B_T / (b^2 (n-1)) =", mp.nstr(BT/(b*b*(n-1)), 12), "(claimed in [1/2, 1])")
rng = np.random.default_rng(7)
worst = mp.inf
for trial in range(25):
    size = int(rng.integers(1, k//2+1))
    S = sorted(rng.choice(np.arange(1, k+3), size=size, replace=False).tolist())
    LS = minB(S, full=False)
    worst = min(worst, LS/((n-1)*b*b/4))
print("  min over 25 random S with |S| <= k/2 of L_S/((n-1)b^2/4) =", mp.nstr(worst, 8), "(must be >= 1)")

print("== Claim B critical scale: terms -> (lambda/2)^j/j!")
for lam in (1.0, 4.0):
    n = 10**8; s0 = int(lam*math.sqrt(n)); p = 10**12
    tot, lt = 0.0, 0.0
    for j in range(1, 200):
        i = j-1
        lt += math.log((s0+j)/j) - 0.5*math.log(n) + math.log((p-s0-i)/(2*p-1-s0-i))
        tot += math.exp(lt)
    print(f"  lambda={lam}: partial O_lb = {tot:.6f}, e^(lambda/2)-1 = {math.exp(lam/2)-1:.6f}")
