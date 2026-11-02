"""First-order estimate of eps (probability that the double-precision final run takes a different discrete decision
than the long-double run on the same streams), from the threshold logs of make_log_cores.sh.
Under EX-S each uniform is U(0,1) and independent of the threshold it is compared with, so, given agreement so far,
  P(flip at a scalar comparison u < t)              = |t_fp - t_ld|
  P(flip at one resampling draw, boundaries W_k)    = sum_k |W_k^fp - W_k^ld|           (N draws per resampling)
  P(flip at one pi_0 categorical draw, cum array c) = sum_k |c_k^fp - c_k^ld|,  estimated without bias by
                                                      |c_k^fp - c_k^ld| / (c_k^fp - c_{k-1}^fp) at the drawn k
The union bound over the run gives eps_run <= sum of these (first order). Index draws floor(u m) are handled
analytically in AUDIT.md. Usage: python3 analyze_thr.py <fp.bin> <ld.bin> <fit_id>  (prints one CSV line)"""
import sys, numpy as np
dt = np.dtype([("tag", "<i4"), ("x", np.longdouble)], align=False)
assert np.dtype(np.longdouble).itemsize == 16
a = np.fromfile(sys.argv[1], dtype=dt); b = np.fromfile(sys.argv[2], dtype=dt); fid = sys.argv[3]
same_len = len(a) == len(b); same_tags = same_len and bool(np.array_equal(a["tag"], b["tag"]))
if not same_tags:
    print(f"{fid},PATH_MISMATCH,{len(a)},{len(b)}"); sys.exit(0)
tag = a["tag"]; d = np.abs(a["x"] - b["x"])
out = {}
for t, name in [(1, "gibbs"), (2, "uswap"), (3, "nswap"), (4, "indep")]:
    m = tag == t; out[name + "_n"] = int(m.sum()); out[name + "_sum"] = float(d[m].sum()); out[name + "_max"] = float(d[m].max()) if m.any() else 0.0
# resampling: blocks "8 N" then N entries of tag 5
idx8 = np.flatnonzero(tag == 8); rs = 0.0
for i in idx8:
    N = int(a["x"][i]); seg = d[i + 1:i + 1 + N]; assert np.all(tag[i + 1:i + 1 + N] == 5); rs += N * float(seg.sum())
out["resample_n"] = int(len(idx8)); out["resample_sum"] = rs
# pi_0 draws: pairs (6: c_k, 7: c_{k-1})
i6 = np.flatnonzero(tag == 6); assert np.all(tag[i6 + 1] == 7)
pk = (a["x"][i6] - a["x"][i6 + 1]).astype(np.longdouble)
est = d[i6] / pk
out["pi0_n"] = int(len(i6)); out["pi0_sum"] = float(est.sum()); out["pi0_max"] = float(est.max()) if len(i6) else 0.0
out["n_comparisons"] = int(sum(out[k] for k in ["gibbs_n", "uswap_n", "nswap_n", "indep_n", "pi0_n"])) + int(sum(a["x"][idx8].astype(int)))
tot = sum(out[k] for k in ["gibbs_sum", "uswap_sum", "nswap_sum", "indep_sum", "resample_sum", "pi0_sum"])
out["eps_first_order"] = tot
keys = list(out)
if fid == "1": print("id," + ",".join(keys))
print(fid + "," + ",".join(f"{out[k]:.6g}" for k in keys))
