"""run_t2.py -- Target 2 falsification: exact-Gram one-factor designs with r = 1, 2, 3 loading classes, uncapped LS0
path from the full set [p] (closed form, eg_core).  Per run: pure null deletion?  ends at S0?  max addition gain/log n,
min best-deletion gain/log n, max (best swap - best deletion) over null-out swaps, max truth-move gain, number of steps
with a per-class interval-hole violation, max centre ratio max_c l_c|X_T|/Hbar (whole path and end phase m <= 30),
the structure-free exponent A_S of Theorem T2-S, and the end-phase deletion sequence (class, sign).
Usage: py -3.13 run_t2.py out.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import eg_core as eg

DESIGNS = {
    "cs05":        ([math.sqrt(0.5)], [1.0]),
    "r2_02_095":   ([0.2, 0.95], [0.5, 0.5]),
    "r2_02_095_lo":([0.2, 0.95], [0.8, 0.2]),
    "r2_02_095_hi":([0.2, 0.95], [0.2, 0.8]),
    "r2_03_09":    ([0.3, 0.9], [0.5, 0.5]),
    "r2_05_095":   ([0.5, 0.95], [0.5, 0.5]),
    "r2_06_08":    ([0.6, 0.8], [0.5, 0.5]),
    "r3_02_06_095":([0.2, 0.6, 0.95], [1 / 3, 1 / 3, 1 / 3]),
    "r3_03_05_09": ([0.3, 0.5, 0.9], [1 / 3, 1 / 3, 1 / 3]),
    "r2_01_098":   ([0.1, 0.98], [0.5, 0.5]),
    "r2_02_095_vlo": ([0.2, 0.95], [0.9, 0.1]),
}
TRUTHS = {  # (truth class index rule, coefficients)
    "s1lo": ("lo", [1.2]),
    "s1hi": ("hi", [1.2]),
    "s3mix": ("mix", [1.3, -0.9, 1.6]),
}


def build(design, p, truth, rng):
    vals, props = DESIGNS[design]
    counts = np.floor(np.array(props) * p).astype(int); counts[-1] = p - counts[:-1].sum()
    lam = np.concatenate([np.full(c, v) for v, c in zip(vals, counts)])
    perm = rng.permutation(p); lam = lam[perm]
    rule, coefs = TRUTHS[truth]
    th = np.zeros(p)
    if rule == "lo":
        idx = [int(np.flatnonzero(lam == min(vals))[0])]
    elif rule == "hi":
        idx = [int(np.flatnonzero(lam == max(vals))[0])]
    else:
        idx = [int(np.flatnonzero(lam == vals[i % len(vals)])[i // len(vals)]) for i in range(len(coefs))]
    th[idx] = coefs
    return lam, th


def A_S(lam, th):
    ell = lam / np.sqrt(1 - lam ** 2)
    R = ell.max() / ell.min()
    kS = 1 + float((ell[th != 0] ** 2).sum())
    gbar = ell.max() ** 2 / kS
    return min(1 / (2 * max(1.0, gbar)), 1 / (2 * ((1 + R) ** 2 - 1))), R, gbar


def run(job):
    design, truth, n, p, seed = job
    rng = np.random.default_rng(7919 * seed + 31 * p + sum(map(ord, design + truth)) % 1000)
    lam, th = build(design, p, truth, rng)
    t0 = time.time()
    P = eg.EGData(lam, th, n, rng)
    out = eg.eg_path(P, range(p))
    mv = out["moves"]; info = out["info"]; st = out["steps"]
    types = {}
    for m in mv:
        types[m[0]] = types.get(m[0], 0) + 1
    ln = math.log(n)
    end = [s for s in st if s[1] <= 30]
    cr_end = max([s[3] for s in end] + [0.0])
    Jend = max([abs(s[5]) for s in end] + [0.0])
    vals = np.unique(lam)
    seq = []
    for m in mv[-30:]:
        if m[0] == "delN":
            seq.append("%d%s" % (m[4], "+" if P.xi[m[1]] > 0 else "-"))
        else:
            seq.append(m[0])
    As, R, gbar = A_S(lam, th)
    return dict(design=design, truth=truth, n=n, p=p, seed=seed, logp_logn=math.log(p) / ln, A_S=As, R=R, gbar=gbar,
                moves=len(mv), types=types, pure_deletion=all(m[0] == "delN" for m in mv),
                final_is_S0=out["final_is_S0"], max_add_over_logn=info["max_add"] / ln,
                min_best_del_over_logn=info["min_best_del"] / ln, max_swap_minus_del=info["max_swap_minus_del"],
                max_truth=info["max_truth"], interval_viol_steps=info["interval_viol"], ties=info["ties"],
                max_centre_ratio=info["max_centre_ratio"], centre_ratio_end=cr_end, maxJ_end=Jend,
                end_seq=" ".join(seq), bulk_delta_over_l=info.get("bulk_delta_over_l", 0.0),
                bulk_absX=info.get("bulk_absX", 0.0), bulk_onesided_steps=info.get("bulk_onesided_steps", 0),
                state_at_max_cr=list(max(st, key=lambda s: s[3])[:3]) + [max(st, key=lambda s: s[3])[5]] if st else None,
                t=round(time.time() - t0, 1))


if __name__ == "__main__":
    outf = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "main"
    J = []
    if mode == "main":
        for design in list(DESIGNS)[:9]:
            for truth in TRUTHS:
                for n in [10 ** 6, 10 ** 10]:
                    for p in [300, 1500]:
                        for seed in range(2):
                            J.append((design, truth, n, p, seed))
    else:  # stress: extreme loadings, small n (large log p / log n), large p
        for design in ["r2_01_098", "r2_02_095_vlo", "r2_02_095_lo", "r3_02_06_095", "cs05"]:
            for truth in ["s1lo", "s1hi", "s3mix"]:
                for n, p in [(10 ** 4, 1000), (10 ** 4, 3000), (10 ** 5, 3000), (10 ** 8, 4000), (10 ** 14, 4000)]:
                    for seed in range(2):
                        J.append((design, truth, n, p, seed))
    J.sort(key=lambda j: -j[3])
    print(len(J), "jobs", flush=True)
    with Pool(7) as pool:
        for r in pool.imap_unordered(run, J):
            with open(outf, "a") as f:
                f.write(json.dumps(r) + "\n")
            print("%-13s %-5s n=%-6g p=%-5d s%d %s %s add %.3f del %.3f sw-del %.2f viol %d cr %.2f cr_end %.2f t %.0f" % (
                r["design"], r["truth"], r["n"], r["p"], r["seed"], r["types"], "S0" if r["final_is_S0"] else "MISS",
                r["max_add_over_logn"], r["min_best_del_over_logn"], r["max_swap_minus_del"], r["interval_viol_steps"],
                r["max_centre_ratio"], r["centre_ratio_end"], r["t"]), flush=True)
    print("done", flush=True)
