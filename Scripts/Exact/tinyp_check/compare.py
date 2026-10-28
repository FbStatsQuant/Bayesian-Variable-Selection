"""Tiny-p check, part 3: apply the pre-declared rules of CRITERIA.md.

Usage: python -B compare.py FITS_DIR EXACT_DIR OUT_DIR    (writes RESULT.json and REPORT.md)
Indices: v3 PIPs are named by 1-based original columns; B's oracle uses 0-based columns.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

fits_dir, exact_dir, out_dir = (Path(a).resolve() for a in sys.argv[1:4])
out_dir.mkdir(parents=True, exist_ok=True)

ALPHA, R, N0 = 0.05, 4, 2500
ALPHA_LOGZ = ALPHA / 2 / 15      # 3 rules x 5 designs
ALPHA_PIP = ALPHA / 2 / 103      # 98 coordinates + 5 size tests
FLOOR = 1.0 / (N0 * R)           # resolution of the particle-frequency estimator (1e-4)

exact = {p.name.split(".")[0]: json.loads(p.read_text()) for p in exact_dir.glob("*.exact.json")}
fits = [json.loads(p.read_text()) for p in sorted(fits_dir.glob("D*_rep*_m*.json"))]
assert len(exact) == 10 and len(fits) == 40, (len(exact), len(fits))

hard_failures, rows = [], []
for f in fits:
    e = exact[f["id"]]
    if f["status"] != "completed" or f["branch_run"] != "smc":
        hard_failures.append("%s m%d: status %s branch %s" % (f["id"], f["m"], f["status"], f["branch_run"]))
        continue
    names = [int(j) for j in f["pip_r_rows"]]
    pip_r = np.array(f["pip_r"], dtype=float)               # p x R, rows in names order
    pip = np.array([f["pip_primary"][str(j)] for j in names])
    exact_pip = np.array([e["pips"][j - 1] for j in names])
    # Deterministic pooling checks: equal-weight mean, inside the island range.
    if f["pool_is_rowmeans"] is not True:          # checked in R with identical()
        hard_failures.append("%s m%d: pip_primary != rowMeans(pip_r)" % (f["id"], f["m"]))
    if np.any(pip < pip_r.min(axis=1)) or np.any(pip > pip_r.max(axis=1)):
        hard_failures.append("%s m%d: pooled PIP outside island range" % (f["id"], f["m"]))
    rows.append(dict(id=f["id"], design=f["id"].split("_")[0], m=f["m"], seed=f["seed"],
                     delta=f["log_Z_rel_m0"] - e["log_Z_bf"],
                     delta_full=f["log_Z"] - e["log_Z_full"],
                     log_m0_diff=f["log_m0"] - e["log_m_empty"],
                     L=f["log_Z_rel_m0"], s2=float(np.var(f["log_Z_r_rel_m0"], ddof=1)),
                     names=names, err=pip - exact_pip, pip_r=pip_r, exact_pip=exact_pip,
                     max_abs_pip_err=float(np.max(np.abs(pip - exact_pip))),
                     hpm=sorted(f["hpm"]), hpm_F=f["hpm_F"], flags=f["flags"], wall_s=f["wall_s"]))

fired, design_summary = [], {}
for D in ["D1", "D2", "D3", "D4", "D5"]:
    rs = [r for r in rows if r["design"] == D]
    if len(rs) != 8:
        hard_failures.append("%s: %d usable fits, expected 8" % (D, len(rs)))
        continue
    nD = len(rs)
    s2D = float(np.mean([r["s2"] for r in rs]))                 # 24 df
    by_ds = defaultdict(list)
    for r in rs:
        by_ds[r["id"]].append(r["L"])
    V = sum(float(np.sum((np.array(v) - np.mean(v)) ** 2)) for v in by_ds.values()) / (2 * (4 - 1))  # 6 df
    FA = V / (s2D / R)
    qA = stats.f.ppf(1 - ALPHA_LOGZ, 6, 24)
    A_fired = FA > qA
    var_pool, df = (V, 6) if A_fired else (s2D / R, 24)
    deltas = np.array([r["delta"] for r in rs])
    tB = float(deltas.mean() / np.sqrt(var_pool / nD))
    qB = stats.t.ppf(1 - ALPHA_LOGZ / 2, df)
    QC = float(np.sum(deltas ** 2) / (nD * var_pool))
    qC = stats.f.ppf(1 - ALPHA_LOGZ, nD, df)
    for name, stat, q, hit in (("A_island_independence", FA, qA, A_fired), ("B_shift", abs(tB), qB, abs(tB) > qB),
                               ("C_dispersion", QC, qC, QC > qC)):
        if hit:
            fired.append(dict(design=D, rule=name, stat=stat, threshold=q))
    # PIPs: per coordinate, island variance pooled over fits (24 df).
    qP = stats.t.ppf(1 - ALPHA_PIP / 2, 24)
    E = np.array([r["err"] for r in rs])                        # nD x p
    S2 = np.mean([np.var(r["pip_r"], axis=1, ddof=1) for r in rs], axis=0)
    mean_e = E.mean(axis=0)
    se = np.sqrt(S2 / (R * nD))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, mean_e / se, np.where(np.abs(mean_e) > 0, np.inf, 0.0))
    for j, name in enumerate(rs[0]["names"]):
        if abs(t[j]) > qP and abs(mean_e[j]) > FLOOR:
            fired.append(dict(design=D, rule="PIP", column=name, mean_err=float(mean_e[j]), t=float(t[j]), threshold=qP))
    size_err = np.array([r["err"].sum() for r in rs])
    size_s2 = float(np.mean([np.var(r["pip_r"].sum(axis=0), ddof=1) for r in rs]))
    size_t = float(size_err.mean() / np.sqrt(size_s2 / (R * nD))) if size_s2 > 0 else (np.inf if size_err.mean() else 0.0)
    if abs(size_t) > qP and abs(size_err.mean()) > FLOOR:
        fired.append(dict(design=D, rule="PIP_size", mean_err=float(size_err.mean()), t=size_t, threshold=qP))
    design_summary[D] = dict(s_D=float(np.sqrt(s2D)), F_A=FA, q_A=qA, t_B=tB, q_B=qB, QC=QC, q_C=qC,
                             mean_delta=float(deltas.mean()), max_abs_delta=float(np.max(np.abs(deltas))),
                             min_detectable_shift=float(qB * np.sqrt(var_pool / nD)),
                             max_abs_mean_pip_err=float(np.max(np.abs(mean_e))), max_abs_pip_t=float(np.max(np.abs(t))),
                             q_pip=qP, size_mean_err=float(size_err.mean()), size_t=size_t)

# HPM per dataset.
hpm_notes = []
for ident in sorted(exact):
    rs = [r for r in rows if r["id"] == ident]
    ex = sorted(j + 1 for j in exact[ident]["hpm"])
    sets = {tuple(r["hpm"]) for r in rs}
    for r in rs:
        if r["hpm"] == ex and abs(r["hpm_F"] - exact[ident]["hpm_score"]) > 1e-9:
            fired.append(dict(dataset=ident, rule="HPM_score", m=r["m"], diff=r["hpm_F"] - exact[ident]["hpm_score"]))
    if len(sets) == 1 and list(sets)[0] != tuple(ex):
        fired.append(dict(dataset=ident, rule="HPM_replicable_mismatch", v3=list(sets)[0], exact=ex))
    elif len(sets) > 1:
        hpm_notes.append(dict(dataset=ident, seeds_disagree=[list(s) for s in sets], exact=ex))

per_fit = [dict(id=r["id"], m=r["m"], seed=r["seed"], delta_logZ_bf=r["delta"], delta_logZ_full=r["delta_full"],
                s_f=float(np.sqrt(r["s2"])), max_abs_pip_err=r["max_abs_pip_err"], hpm=r["hpm"],
                hpm_exact=sorted(j + 1 for j in exact[r["id"]]["hpm"]), flags=r["flags"], wall_s=r["wall_s"])
           for r in rows]
result = dict(outcome="PASS" if not hard_failures and not fired else "INVESTIGATE",
              hard_failures=hard_failures, fired=fired, hpm_report_only=hpm_notes, designs=design_summary,
              scale_crosscheck=dict(max_abs_log_m0_diff=max(abs(r["log_m0_diff"]) for r in rows),
                                    max_abs_full_minus_bf=max(abs(r["delta_full"] - r["delta"]) for r in rows)),
              per_fit=per_fit, alpha=dict(total=ALPHA, logZ_test=ALPHA_LOGZ, pip_test=ALPHA_PIP, pip_floor=FLOOR),
              exact_enumerated={k: v["enumerated"] for k, v in exact.items()})
(out_dir / "RESULT.json").write_text(json.dumps(result, indent=1, default=float) + "\n")

lines = ["# Tiny-p SMC versus exact: result", "", "Outcome: **%s**" % result["outcome"], ""]
lines += ["| design | s_D | mean Δlog Z | max abs Δ | t_B (q) | F_A (q) | Q_C (q) | max abs mean PIP err | max abs PIP t (q) |",
          "|---|---|---|---|---|---|---|---|---|"]
for D, s in design_summary.items():
    lines.append("| %s | %.4f | %+.4f | %.4f | %.2f (%.2f) | %.2f (%.2f) | %.2f (%.2f) | %.2e | %.2f (%.2f) |" % (
        D, s["s_D"], s["mean_delta"], s["max_abs_delta"], s["t_B"], s["q_B"], s["F_A"], s["q_A"], s["QC"], s["q_C"],
        s["max_abs_mean_pip_err"], s["max_abs_pip_t"], s["q_pip"]))
lines += ["", "Fired rules: %d. Hard failures: %d. HPM seed disagreements (report only): %d." % (
    len(fired), len(hard_failures), len(hpm_notes)), ""]
lines += ["| fit | seed | Δlog Z (BF) | s_f | max abs PIP err | HPM v3 | HPM exact |", "|---|---|---|---|---|---|---|"]
for r in per_fit:
    lines.append("| %s m%d | %d | %+.4f | %.4f | %.2e | %s | %s |" % (r["id"], r["m"], r["seed"], r["delta_logZ_bf"],
                 r["s_f"], r["max_abs_pip_err"], r["hpm"], r["hpm_exact"]))
(out_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
print(result["outcome"], "fired", len(fired), "hard", len(hard_failures))
