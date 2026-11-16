"""Item 1 (+ item 6b data): nested tails of Pi(n d^2 > t | D) per data set.  p=12, AR(0.5) Gaussian design, s=3 (1,-1,1), sigma*=1.
d^2 is EXACT given the draw (Gaussian design closed form); the only Monte Carlo is the posterior draw: NDRAW per data set.
usage: python3 -B item1_nested_tails.py NWORK R NDRAW   -> out/item1_n{n}.npz
DRAFT (by this seat, unchecked)"""
import sys, time
from multiprocessing import Pool
from fcommon import *
TGRID = np.arange(0.25, 40.001, 0.25)
P = 12
SIG = ar_sigma(P)
LC = np.linalg.cholesky(SIG)
BSTAR = np.zeros(P); BSTAR[:3] = [1, -1, 1]

def one(args):
    n, rep, ndraw = args
    rng = np.random.default_rng([20261116, 1, n, rep])
    Xr = rng.standard_normal((n, P)) @ LC.T
    yr = Xr @ BSTAR + rng.standard_normal(n)
    d = C.prep(Xr, yr); d.Xraw = Xr
    idx, lp, Q, sz = C.exact_family(d)
    pi = np.exp(lp - lp.max()); pi /= pi.sum()
    nd2 = []; chunk = 100000
    for s in range(0, ndraw, chunk):
        B, sig2, mid = C.sample_posterior(d, idx, lp, Q, min(chunk, ndraw - s), rng)
        nd2.append(n * gauss_d2(d, B, sig2, BSTAR, SIG))
    nd2 = np.sort(np.concatenate(nd2))
    tail = 1 - np.searchsorted(nd2, TGRID, side='right') / len(nd2)     # P(n d^2 > t)
    qs = np.quantile(nd2, [.5, .9, .99, .999])
    szlaw = np.array([pi[sz == k].sum() for k in range(P + 1)])          # exact pi(|S|=k)
    S0 = [0, 1, 2]
    logD0 = log_det_ratio(d, S0)                                        # Lemma S input (item 6b)
    mu2n, th2n = sample_quantities(d, BSTAR)
    is0 = (sz == 3) & (idx[:, 0] == 0) & (idx[:, 1] == 1) & (idx[:, 2] == 2)
    pi0 = pi[is0].sum()
    return dict(n=n, rep=rep, tail=tail, qs=qs, mean=nd2.mean(), szlaw=szlaw, logD0=logD0, mu2n=mu2n, th2n=th2n, pi0=pi0)

if __name__ == "__main__":
    nw, R, nd = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for n in (100, 400):
        t0 = time.time()
        with Pool(nw) as pool:
            res = pool.map(one, [(n, r, nd) for r in range(R)], chunksize=2)
        keys = ["tail", "qs", "mean", "szlaw", "logD0", "mu2n", "th2n", "pi0"]
        np.savez_compressed(f"out/item1_n{n}.npz", tgrid=TGRID, ndraw=nd, **{k: np.array([r[k] for r in res]) for k in keys})
        print(f"n={n}: R={R}, ndraw={nd}, {time.time()-t0:.0f}s", flush=True)
