import numpy as np, time
from common import *

MS = [1, 2, 4, 8, 16]

def run_rep(spec):
    t0 = time.time()
    n, p, kind = spec["n"], spec["p"], spec["kind"]
    seed = [20261115, spec["eid"], n, p, spec["rep"]]
    rng = np.random.default_rng(seed)
    rngf = np.random.default_rng(seed + [1])
    rngs = np.random.default_rng(seed + [2])
    tau2 = spec.get("tau2")
    bstar = beta_star(spec["beta"], n, p)
    Xr = gen_design(kind, n, p, rng, tau2)
    yr = Xr @ bstar + SIG_STAR * rng.standard_normal(n)
    d = prep(Xr, yr)
    d.Xraw = Xr
    nd = spec["ndraw"]
    if spec["family"] == "exact":
        idx, lp, Q, sz = exact_family(d); U = None
    else:
        idx, lp, Q, sz, U = restricted_family(d, set(np.where(bstar != 0)[0]), rngs)
    B, sig2, mid = sample_posterior(d, idx, lp, Q, nd, rngs)
    Xf = gen_design(kind, spec["mfresh"], p, rngf, tau2)
    r = distances(d, B, sig2, bstar, Xf, nd)
    d2, h2, tb, dm = r["d2"], r["h2in"], r["tbar"], r["dmean"]
    ln = np.log(n)
    rho = dm / (2 * tb + ln / n)
    out = dict(eid=spec["eid"], name=spec["name"], kind=kind, n=n, p=p, q=d.q, rep=spec["rep"], family=spec["family"],
               tau2=tau2 if tau2 is not None else np.nan, nmodels=len(lp))
    for nm, a in (("d2", d2), ("h2in", h2), ("dmean", dm)):
        out[nm + "_mean"] = a.mean()
        for qq in (0.5, 0.9, 0.99):
            out[f"{nm}_q{int(qq*100)}"] = np.quantile(a, qq)
    out["tbar_q50"] = np.quantile(tb, .5); out["tbar_q90"] = np.quantile(tb, .9)
    for M in MS:
        out[f"cnt_M{M}"] = int((d2 > M * ln / n).sum())
        out[f"cnth_M{M}"] = int((h2 > M * ln / n).sum())
    sizes = (B != 0).sum(1)
    hist = np.bincount(sizes, minlength=14)[:14]
    for k in range(14): out[f"size{k}"] = int(hist[k])
    out["esize"] = sizes.mean()
    ts = np.where(bstar != 0)[0]
    pos = {int(c): i for i, c in enumerate(d.keep)}
    for j in range(3):
        out[f"incl{j}"] = float((B[:, pos[j]] != 0).mean()) if j in pos else np.nan
    out["true_dropped"] = int(sum(1 for j in ts if j not in pos))
    out["rho_max"] = rho.max(); out["rho_q999"] = np.quantile(rho, .999); out["rho_med"] = np.median(rho)
    out["d2_if_dropped_med"] = np.median(d2) if out["true_dropped"] > 0 else np.nan
    out["sy"] = d.sy; out["time"] = time.time() - t0
    return out, d2.astype(np.float32), rho.astype(np.float32)
