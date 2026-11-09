"""S3: centre condition CC_n(c) along the actual path (which is Pi when pure deletion):
max over visited T and T' in {T} u {T minus j: j retained null} of kappa0|e_T'| / H_q, H_q = sqrt(2 log(2^q p)+2 loglog n).
Also checks the gain approximation: exact deletion gain vs Delta_k - (1/2) tau^2 (in units of log n).
usage: py -3.13 s3_cc.py p n seed [q rb rw]"""
import sys, math, json, numpy as np
import bcs_core as B
p, n, seed = int(sys.argv[1]), int(float(sys.argv[2])), int(sys.argv[3])
q = int(sys.argv[4]) if len(sys.argv) > 4 else 5
rb = float(sys.argv[5]) if len(sys.argv) > 5 else .3
rw = float(sys.argv[6]) if len(sys.argv) > 6 else .7
rng = np.random.default_rng(10007 * seed + p)
P = B.BCS(n, np.arange(p) // q, rb, rw, B.layout(p, q, s0=4), rng)
isnull = np.ones(p, bool); isnull[P.S0] = False
path = B.Path(P, np.ones(p, bool))
k0 = 1 / math.sqrt(1 - rb); Hq = math.sqrt(2 * math.log(2 ** q * p) + 2 * math.log(math.log(n)))
logn = math.log(n)
marg = 1e9; marg_at = None; cc_max = 0.0; cc_bulk = 0.0; gain_err = 0.0; pure = True; steps = 0; at = None
while True:
    G = path.gains(swaps=False)
    nt = path.noise_tau()
    Tidx = G["Tidx"]; retN = Tidx[isnull[Tidx]]
    vals = [abs(nt["e_T"])] + ([float(np.max(np.abs(nt["eR"][retN])))] if len(retN) else [])
    cc = k0 * max(vals) / Hq
    if cc > cc_max: cc_max, at = cc, len(retN)
    kk = path.k
    mg = (math.log(n) + 2 * math.log((2 * p - kk) / (kk + 1)) - (Hq + k0 * max(vals)) ** 2) / logn
    if mg < marg: marg, marg_at = mg, len(retN)
    if len(retN) >= 30: cc_bulk = max(cc_bulk, cc)
    if len(retN):
        k = path.k
        Dk = math.log((2 * p - k) / k) + 0.5 * math.log(n + 1)
        approx = Dk - 0.5 * nt["tau"][retN] ** 2
        exact = G["gdel"][isnull[Tidx]]
        gain_err = max(gain_err, float(np.max(np.abs(exact - approx))) / logn)
        j = int(Tidx[G["gdel"] == G["gdel"].max()].max())  # lex-smallest resulting set on exact ties
        if not isnull[j] or G["gdel"].max() <= 0: pure = False; break
        path.apply("del", j=j); steps += 1
    else:
        break
print(json.dumps(dict(p=p, n=n, seed=seed, alpha=math.log(p) / logn, steps=steps, reached_S0=pure,
                      cc_max=cc_max, cc_max_at_m=at, cc_bulk_m30=cc_bulk, gain_approx_err_over_logn=gain_err,
                      CCdelta_margin_over_logn=marg, margin_at_m=marg_at, c_needed_for_alpha=1 / math.sqrt(2 * math.log(p) / logn) - 1)))
