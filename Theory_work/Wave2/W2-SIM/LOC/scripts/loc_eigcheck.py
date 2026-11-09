r"""loc_eigcheck.py -- positive definiteness / spectrum of the Toeplitz correlation matrices used by family LOC.
For each family (PT alpha: (1+h)^-alpha; AF d: ARFIMA(0,d,0) acf) and each p in the grid, lambda_min and lambda_max of
Sigma_p (scipy.linalg.eigvalsh, subset_by_index for the extremes) and the Cholesky success flag.
Also the spectral-density value at omega = pi, f(pi) = sum_h gamma(|h|) (-1)^h (truncated at p), a lower envelope check.
Usage: python3 loc_eigcheck.py OUT_JSONL p1 p2 ..."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loc_core as lc
from loc_core import np
from scipy.linalg import eigvalsh

FAMS = [("PT", a) for a in (0.5, 0.8, 1.5, 2.5, 4.0, 6.0, 8.5)] + [("AF", d) for d in (0.1, 0.25, 0.4)]
out = sys.argv[1]
for p in [int(v) for v in sys.argv[2:]]:
    for fam, par in FAMS:
        t = time.time()
        acf = lc.acf_poly(par, p) if fam == "PT" else lc.acf_arfima(par, p)
        S = lc.toeplitz(acf)
        lo = float(eigvalsh(S, subset_by_index=[0, 0])[0])
        hi = float(eigvalsh(S, subset_by_index=[p - 1, p - 1])[0])
        try:
            np.linalg.cholesky(S); chol = True
        except np.linalg.LinAlgError:
            chol = False
        sgn = (-1.0) ** np.arange(p)
        fpi = float(acf[0] + 2 * (acf[1:] * sgn[1:]).sum())
        rec = dict(fam=fam, par=par, p=p, lam_min=lo, lam_max=hi, chol_ok=chol, f_pi_trunc=fpi, secs=round(time.time() - t, 1))
        with open(out, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(rec, flush=True)
