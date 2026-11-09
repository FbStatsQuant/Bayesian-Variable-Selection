"""R02 reviewer falsification checks for XA L1 (a,b,c). Local, small. Python 3.13 + numpy/scipy."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import itertools, json, sys
import numpy as np
from scipy.optimize import minimize

def root(M):
    w, v = np.linalg.eigh(M); return (v * np.sqrt(np.clip(w, 0, None))) @ v.T
def iroot(M):
    w, v = np.linalg.eigh(M); return (v / np.sqrt(w)) @ v.T
def direction(M, T, j):
    v = M[:, j].copy()
    if T:
        Q = np.linalg.qr(M[:, list(T)], mode='reduced')[0]; v -= Q @ (Q.T @ v)
    return v / np.linalg.norm(v)
def cs(p, rho): return (1 - rho) * np.eye(p) + rho * np.ones((p, p))
def onef(p, lo=.4, hi=.85):
    lam = np.linspace(lo, hi, p); return np.diag(1 - lam**2) + np.outer(lam, lam)
def sample_R(Sig, n, rng):
    X = rng.standard_normal((n, Sig.shape[0])) @ root(Sig)
    Xc = X - X.mean(0); S = Xc.T @ Xc / (n - 1)
    d = np.sqrt(np.diag(S)); return S / np.outer(d, d), S, Xc
out = {}

# ---------- L1a: rates of absolute op, Frobenius, relative norms ----------
rng = np.random.default_rng(20261109)
rows = []
for name, mk in (('CS0.5', lambda p: cs(p, .5)), ('1F', onef)):
    for n in (500, 2000, 8000):
        for p in (4, 16, 64, 128):
            if p > n / 4: continue
            Sig = mk(p); Si = iroot(Sig); c = np.linalg.eigvalsh(Sig)[0]
            ab, fr, rel = [], [], []
            for r in range(10):
                R, S, _ = sample_R(Sig, n, rng); M = R - Sig
                ab.append(np.linalg.norm(M, 2)); fr.append(np.linalg.norm(M, 'fro'))
                rel.append(np.linalg.norm(Si @ M @ Si, 2))
            d = n - 1
            rows.append(dict(design=name, n=n, p=p, c=c,
                abs_over_p_sqrtd=np.mean(ab) / (p / np.sqrt(d)),
                fro2_times_d_over_p2=np.mean(np.square(fr)) * d / p**2,
                rel_over_p_sqrtd=np.mean(rel) / (p / np.sqrt(d)),
                rel_over_sqrt_p_d=np.mean(rel) / np.sqrt(p / d),
                rel_le_abs_over_c=bool(all(x <= y / c + 1e-12 for x, y in zip(rel, ab)))))
out['L1a'] = rows

# ---------- L1b: adversarial E, worst constant in ||qB-qA|| <= K e/sqrt(c) ----------
def worst_ratio(Sig, e, W):
    W = (W + W.T) / 2; nW = np.linalg.norm(W, 2)
    if nW == 0: return 0.
    E = e * W / nW; A = root(Sig); B = root(np.eye(len(Sig)) + E) @ A
    c = np.linalg.eigvalsh(Sig)[0]; p = len(Sig); m = 0.
    for k in range(p):
        for T in itertools.combinations(range(p), k):
            for j in set(range(p)) - set(T):
                m = max(m, np.linalg.norm(direction(B, T, j) - direction(A, T, j)))
    return m / (e / np.sqrt(c))
adv = []
rng = np.random.default_rng(7)
for name, Sig in (('CS0.5_p4', cs(4, .5)), ('CS0.9_p4', cs(4, .9)), ('CS0.99_p3', cs(3, .99)),
                  ('1F_p4', onef(4)), ('1F_.1-.995_p4', onef(4, .1, .995)),
                  ('pair0.999_p3', np.array([[1, .999, 0], [.999, 1, 0], [0, 0, 1.]]))):
    p = len(Sig)
    for e in (1e-3, .25):
        best = 0.
        for start in range(6):
            w0 = rng.standard_normal(p * p)
            f = lambda w: -worst_ratio(Sig, e, w.reshape(p, p))
            res = minimize(f, w0, method='Nelder-Mead', options=dict(maxiter=1500, xatol=1e-6, fatol=1e-9))
            best = max(best, -res.fun)
        adv.append(dict(Sigma=name, e=e, c=float(np.linalg.eigvalsh(Sig)[0]), worst_K=best, proved_K=8.0))
out['L1b_adversarial'] = adv

# ---------- L1c: coupling realized on actual data + scaling ----------
def l1c_case(Sig, n, rng, maxk):
    p = len(Sig); d = n - 1
    R, S, Xc = sample_R(Sig, n, rng)
    Xt = Xc / np.sqrt(np.diag(S))           # columns: mean 0, sum sq = d
    A = root(Sig); Si = iroot(Sig); E = Si @ (R - Sig) @ Si; e = np.linalg.norm(E, 2)
    B = root(np.eye(p) + E) @ A
    O = Xt @ np.linalg.inv(B) / np.sqrt(d)
    orth_err = np.abs(O.T @ O - np.eye(p)).max()
    eps = rng.standard_normal(n); Ceps = eps - eps.mean()
    z = O.T @ Ceps; r = Ceps @ Ceps - z @ z
    c = np.linalg.eigvalsh(Sig)[0]
    ident = 0.; supdiff = 0.
    for k in range(maxk + 1):
        for T in itertools.combinations(range(p), k):
            js = [j for j in range(p) if j not in T]
            for j in js:
                v = Xt[:, j].copy()
                if T:
                    Q = np.linalg.qr(Xt[:, list(T)], mode='reduced')[0]; v -= Q @ (Q.T @ v)
                Zact = v @ eps / np.linalg.norm(v)
                qB = direction(B, T, j); qA = direction(A, T, j)
                ident = max(ident, abs(Zact - qB @ z))
                supdiff = max(supdiff, abs((qB - qA) @ z))
    return dict(n=n, p=p, maxk=maxk, e=e, orth_err=orth_err, identity_err=ident, sup_ZB_ZA=supdiff,
                bound=10 * e * np.linalg.norm(z) / np.sqrt(c), resid_chi2=r,
                sup_over_p32_sqrtn=supdiff / (p**1.5 / np.sqrt(n)), sup_over_p_sqrtn=supdiff / (p / np.sqrt(n)))
rng = np.random.default_rng(11)
cpl = []
for name, mk in (('CS0.5', lambda p: cs(p, .5)), ('1F', onef)):
    for n, p, mk_ in ((400, 8, 7), (4000, 8, 7), (40000, 8, 7), (2000, 32, 2), (8000, 32, 2), (32000, 32, 2)):
        rec = l1c_case(mk(p), n, rng, mk_); rec['design'] = name; cpl.append(rec)
out['L1c'] = cpl

json.dump(out, open(os.path.join(os.path.dirname(__file__), 'r02_checks_out.json'), 'w'), indent=1, default=float)
for k, v in out.items():
    print('==', k)
    for row in v: print({a: (round(b, 4) if isinstance(b, float) else b) for a, b in row.items()})
