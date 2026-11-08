"""W1-N1 Monte Carlo companion on the PRODUCTION island (Engine::run_island, instrumented copy, see cpp/instr.diff).

For a design directory written by `n1_harness.exe export`, runs `n1_harness.exe mc` (production run_island on the
production grid, independent streams seed_stream(70000 + 100 id + N, 10 + r)), reads per-island log Zhat and the
4N measured endpoints, and reports for each h:
  mean of W_r H_r(h) vs pi(h) (z-score with the Monte Carlo SE), E[W] vs 1,
  Corollary E: mean of W_r |H_r(h) - h(S0)| vs delta1 (for h with values in [0,1]),
  adaptive-h control NC3: h_omega = 1{S = most frequent endpoint of the island} (chosen after the run). The N1-centred
  statistic is W H(h_omega) - pi(h_omega) (paired), whose mean would be 0 if N1 extended to this random h (the necessary
  consequence E[W H(h_omega)] = E[pi(h_omega)] of the conditional identity). Also reported, labelled separately: the
  weighted-centred statistic W (H(h_omega) - pi(h_omega)), a different selected-function identity.
Usage: py -3.13 n1_mc.py <dir> <N> <reps>
"""
import json
import math
import subprocess
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from n1_exact import h_list, load, lse  # noqa: E402

HARNESS = __file__.replace("n1_mc.py", "cpp/n1_harness_v2.exe")


def main(dirn, N, reps):
    meta, om, _ = load(dirn)
    did = int(meta["id"][0]); p = int(meta["p"][0]); M = int(meta["M"][0])
    grid = [float(x) for x in meta["grid"]]
    with open(f"{dirn}/grid_production.txt", "w") as f:
        f.write("\n".join(repr(x) for x in grid))
    tag = f"N{N}_R{reps}"
    cp = subprocess.run([HARNESS, "mc", str(did), dirn, str(N), str(reps), f"{dirn}/grid_production.txt", tag],
                        check=True, capture_output=True, text=True)
    hook_diff = float(cp.stdout.split()[-1])
    raw = np.fromfile(f"{dirn}/mc_{tag}.bin", dtype=np.uint8)
    rec = 8 + 2 * 4 * N
    raw = raw.reshape(reps, rec)
    logZhat = raw[:, :8].copy().view(np.float64).ravel()
    ends = raw[:, 8:].copy().view(np.uint16).reshape(reps, 4 * N).astype(np.int64)
    F = om["F"]; logZ = lse(F); pi = np.exp(F - logZ)
    W = np.exp(logZhat - logZ)
    H, s0mask = h_list(meta, om, p, M)
    masks = list(om["mask"].astype(int))
    s0idx = masks.index(s0mask) if s0mask in masks else None
    delta1 = 1 - (pi[s0idx] if s0idx is not None else 0.0)
    out = {"dir": dirn, "N": N, "reps": reps, "grid": grid, "EW": float(W.mean()), "EW_se": float(W.std(ddof=1) / math.sqrt(reps)),
           "delta1": float(delta1), "hook_vs_pip_plain_maxdiff": hook_diff, "h": {}}
    for hn, h in H.items():
        Hr = h[ends].mean(1)
        x = W * Hr
        se = x.std(ddof=1) / math.sqrt(reps)
        row = {"pi_h": float(pi @ h), "mean_WH": float(x.mean()), "se": float(se),
               "z": float((x.mean() - pi @ h) / se) if se > 0 else 0.0}
        if h.min() >= 0 and h.max() <= 1:
            hS0 = h[s0idx] if s0idx is not None else float("nan")
            y = W * np.abs(Hr - hS0)
            row.update({"corE_mean": float(y.mean()), "corE_se": float(y.std(ddof=1) / math.sqrt(reps)),
                        "corE_bound_delta1": float(delta1)})
        out["h"][hn] = row
    # adaptive h (chosen after seeing the island): indicator of the island's most frequent endpoint
    mode = np.array([np.bincount(e, minlength=M).argmax() for e in ends])
    Hm = (ends == mode[:, None]).mean(1)
    c1 = W * Hm - pi[mode]          # N1-centred
    c2 = W * (Hm - pi[mode])        # weighted-centred (different target)
    out["adaptive_mode_h"] = {"N1_centred_mean": float(c1.mean()), "N1_centred_se": float(c1.std(ddof=1) / math.sqrt(reps)),
                              "weighted_centred_mean": float(c2.mean()), "weighted_centred_se": float(c2.std(ddof=1) / math.sqrt(reps))}
    with open(f"{dirn}/mc_results_{tag}.json", "w") as f:
        json.dump(out, f, indent=1)
    zs = [r["z"] for r in out["h"].values()]
    print(f"== {dirn} N={N} reps={reps}: hook-vs-pip_plain {hook_diff:.1e}; E[W]={out['EW']:.4f}±{out['EW_se']:.4f}; max|z| over h = {max(abs(z) for z in zs):.2f}; "
          f"corE max mean/delta1 = {max(r.get('corE_mean', 0) for r in out['h'].values()) / max(delta1, 1e-300):.3f}; "
          f"NC3 N1-centred: {out['adaptive_mode_h']['N1_centred_mean']:+.4f} (se {out['adaptive_mode_h']['N1_centred_se']:.4f})")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
