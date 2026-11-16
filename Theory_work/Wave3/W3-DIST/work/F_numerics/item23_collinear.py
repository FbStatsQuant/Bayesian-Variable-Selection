"""Item 2 (dangerous collinearity scale, experiment N4 with tau^2 in {log n/n^2, 4 log n/n^2, n^-1.5}) and
Item 3 ((A5) violated: two true columns with correlation 1-1/n, coefficients +B,-B).  p=12, exact enumeration, EXACT d^2 given the draw
(Gaussian design, closed form), NDRAW posterior draws per data set.   usage: python3 -B item23_collinear.py {2|3} NWORK R NDRAW
DRAFT (by this seat, unchecked)"""
import sys, time, math
from multiprocessing import Pool
from fcommon import *
TGRID = np.array([0.5, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128, 256, 512, 1024.0])
MS = [1, 2, 4, 8, 16]
P = 12

def design2(n, tau2, rng):
    Xr = C.gen_design("collin", n, P, rng, tau2)
    S6 = ar_sigma(6)
    Sig = np.zeros((P, P)); Sig[:6, :6] = S6
    Sig[6:, :6] = S6[0][None, :]; Sig[:6, 6:] = S6[0][:, None]
    Sig[6:, 6:] = 1.0 + tau2 * np.eye(6)
    np.fill_diagonal(Sig[:6, :6], 1.0)
    b = np.zeros(P); b[:3] = [1, -1, 1]
    return Xr, Sig, b, [0, 6, 7, 8, 9, 10, 11]          # group of near-duplicates of x1

def design3(n, B, rng):
    rho = 1 - 1.0 / n
    Sc = ar_sigma(11)
    Z = rng.standard_normal((n, 11)) @ np.linalg.cholesky(Sc).T
    xi = rng.standard_normal(n)
    x2 = rho * Z[:, 0] + math.sqrt(1 - rho * rho) * xi
    Xr = np.column_stack([Z[:, 0], x2, Z[:, 1:]])
    Sig = np.zeros((P, P))
    Sig[0, 0] = 1; Sig[1, 1] = 1; Sig[0, 1] = Sig[1, 0] = rho
    Sig[2:, 2:] = Sc[1:, 1:]
    Sig[0, 2:] = Sig[2:, 0] = Sc[0, 1:]
    Sig[1, 2:] = Sig[2:, 1] = rho * Sc[0, 1:]
    b = np.zeros(P); b[0] = B; b[1] = -B
    return Xr, Sig, b, [0, 1]

def one(args):
    mode, n, par, rep, ndraw = args
    rng = np.random.default_rng([20261116, mode, n, int(round(par * 1e6)) % 2**31, rep])
    if mode == 2:
        Xr, Sig, b, grp = design2(n, par, rng)
    else:
        Xr, Sig, b, grp = design3(n, par, rng)
    yr = Xr @ b + rng.standard_normal(n)
    d = C.prep(Xr, yr); d.Xraw = Xr
    idx, lp, Q, sz = C.exact_family(d)
    pi = np.exp(lp - lp.max()); pi /= pi.sum()
    nd2 = []; chunk = 100000
    for s in range(0, ndraw, chunk):
        Bd, sig2, mid = C.sample_posterior(d, idx, lp, Q, min(chunk, ndraw - s), rng)
        nd2.append(n * gauss_d2(d, Bd, sig2, b, Sig))
    nd2 = np.sort(np.concatenate(nd2)); N = len(nd2)
    tail = 1 - np.searchsorted(nd2, TGRID, side='right') / N
    ln = math.log(n)
    tailM = np.array([1 - np.searchsorted(nd2, M * ln, side='right') / N for M in MS])
    A = np.zeros((len(idx), P + 1), bool)
    A[np.arange(len(idx))[:, None], np.where(idx >= 0, idx, P)] = True
    A = A[:, :P]
    incl = pi @ A
    ngrp = pi @ A[:, grp].sum(1)
    szlaw = np.array([pi[sz == k].sum() for k in range(P + 1)])
    mu2n, th2n = sample_quantities(d, b)
    return dict(qs=np.quantile(nd2, [.5, .9, .99, .999]), mean=nd2.mean(), tail=tail, tailM=tailM, szlaw=szlaw, incl=incl,
                ngrp=ngrp, mu2n=mu2n, th2n=th2n, nd2max=nd2.max(), N=N)

if __name__ == "__main__":
    mode, nw, R, nd = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    cells = []
    if mode == 2:
        for n in (100, 400, 1600):
            ln = math.log(n)
            for name, t2 in (("logn/n^2", ln / n**2), ("4logn/n^2", 4 * ln / n**2), ("n^-1.5", n**-1.5)):
                cells.append((n, t2, name))
    else:
        for n in (100, 400):
            for name, Bv in (("1", 1.0), ("sqrt(n)", math.sqrt(n)), ("n", float(n))):
                cells.append((n, Bv, name))
    out = {}
    t0 = time.time()
    with Pool(nw) as pool:
        for (n, par, name) in cells:
            res = pool.map(one, [(mode, n, par, r, nd) for r in range(R)], chunksize=2)
            keys = res[0].keys()
            out[f"{n}|{name}"] = {k: np.array([r[k] for r in res]) for k in keys}
            out[f"{n}|{name}"]["par"] = par
            print(f"mode {mode} n={n} {name} done {time.time()-t0:.0f}s", flush=True)
    import pickle
    pickle.dump(dict(out=out, tgrid=TGRID, ms=MS, ndraw=nd, R=R), open(f"out/item{mode}.pkl", "wb"))
