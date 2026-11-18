#!/usr/bin/env python3
"""Figures and tables for the p = 10^6 pilot write-up.  Offline; needs numpy, pandas, matplotlib.

    python3 make_figures.py            # reads data/scaling.csv + data/stages_1e6.csv, writes next to this file

Outputs: fig_scaling.{pdf,png}, fig_stages_1e6.{pdf,png}, table_pilot.{md,tex}.
Replicates: append rows to data/scaling.csv (one per fit) and data/stages_1e6.csv (five per 10^6 fit), re-run.
A fit counts in the "replicate set" iff in_rep_set == 1 (the pilot is replicate 1) and status == completed.
Schema: see WRITEUP.md and data/build_seed_data.py (SCALING_COLS, STAGE_COLS).
"""
import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT_ID = "6-AR-n200-r01-V-s1"
P_BIG = 1_000_000
STAGES = ["setup", "calibrate", "islands", "merge", "eval"]
STAGE_LABEL = {"setup": "setup", "calibrate": "calibrate", "islands": "islands (16)", "merge": "merge", "eval": "eval + post"}

# Okabe-Ito colour-blind-safe palette
OI = dict(black="#000000", orange="#E69F00", sky="#56B4E9", green="#009E73", yellow="#F0E442",
          blue="#0072B2", verm="#D55E00", pink="#CC79A7", grey="#7f7f7f")
GROUPS = [  # engine key, legend label, colour, marker, hollow
    ("v2.2.1", "v2.2.1 core, PROD-H p ≫ n (n = 200)", OI["sky"], "o", False),
    ("v3.1", "v3.1 frozen core, PROD-H p ≫ n (n = 200)", OI["orange"], "s", False),
    ("v3 rev. D (stage run)", "v3 rev. D stage-level runs (S3-type; not full fits)", OI["green"], "^", True),
    ("v4 smcbvs4", "v4 smcbvs4, AR strong (n = 200)", OI["blue"], "D", False),
]
STAGE_COL = dict(zip(STAGES, [OI["sky"], OI["orange"], OI["blue"], OI["green"], OI["pink"]]))

SCALING_REQUIRED = ["run_id", "p", "engine", "status", "core_h", "wall_s", "peak_rss_gib", "in_rep_set"]
SCALING_NUM = ["p", "n", "replicate", "in_rep_set", "core_h", "wall_s", "wall_e2e_s", "peak_rss_gib", "peak_rss_sacct_gib",
               "hpm_eq_S0", "mpm_eq_S0", "logZ", "logZ_T", "pred_h2_hpm", "pred_h2_mpm", "pred_h2_T", "pred_h2_oracle",
               "kl_hpm", "kl_T", "test_mlpd_hpm", "test_mlpd_T"]
STAGE_REQUIRED = ["run_id", "p", "stage", "n_tasks", "cpus_per_task", "mem_req_gb", "wall_s", "core_h", "peak_mem_gib"]
STAGE_NUM = ["p", "n_tasks", "cpus_per_task", "mem_req_gb", "wall_s", "wall_mean_s", "wall_span_s", "core_h", "peak_mem_gib"]


# ----------------------------------------------------------------------------------------------- data
def read_csv(path, required, numeric):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    miss = [c for c in required if c not in df.columns]
    if miss:
        sys.exit(f"{path}: missing columns {miss}")
    for c in numeric:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].replace("", np.nan), errors="coerce")
    return df


def load(data_dir):
    sc = read_csv(os.path.join(data_dir, "scaling.csv"), SCALING_REQUIRED, SCALING_NUM)
    st = read_csv(os.path.join(data_dir, "stages_1e6.csv"), STAGE_REQUIRED, STAGE_NUM)
    dup = sc.run_id[sc.run_id.duplicated()].tolist()
    if dup:
        sys.exit(f"scaling.csv: duplicate run_id {dup[:5]}")
    if st.duplicated(["run_id", "stage"]).any():
        sys.exit("stages_1e6.csv: duplicate (run_id, stage)")
    unk = sorted(set(st.stage) - set(STAGES))
    if unk:
        sys.exit(f"stages_1e6.csv: unknown stage names {unk}")
    ok = sc[(sc.p == P_BIG) & (sc.status == "completed")].run_id
    nost = sorted(set(ok) - set(st.run_id))
    if nost:
        print(f"note: 10^6 fits without stage rows: {nost}")
    return sc, st


def rep_set(sc):
    return sc[(sc.p == P_BIG) & (sc.in_rep_set == 1) & (sc.status == "completed")]


# ------------------------------------------------------------------------------------------ summaries
def qsum(v):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) == 0:
        return None
    return dict(n=len(v), med=float(np.median(v)), q1=float(np.percentile(v, 25)), q3=float(np.percentile(v, 75)),
                lo=float(v.min()), hi=float(v.max()))


def fmt_summary(v, f):
    """Replicate-set cell: n < 2 -> dash; n = 2 -> range; n >= 3 -> median [Q1, Q3]."""
    s = qsum(v)
    if s is None or s["n"] < 2:
        return "—"
    if s["n"] == 2:
        return f"{f(s['lo'])} – {f(s['hi'])} (n = 2)"
    return f"{f(s['med'])} [{f(s['q1'])}, {f(s['q3'])}] (n = {s['n']})"


def pct(v, total):
    x = 100 * v / total
    return "<1%" if x < 1 else f"{x:.0f}%"


def hm(sec):
    sec = float(sec)
    h, m = int(sec // 3600), int(round((sec % 3600) / 60))
    if m == 60:
        h, m = h + 1, 0
    return f"{h} h {m:02d} min" if h else f"{m} min"


# ------------------------------------------------------------------------------------------ fig_scaling
def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5, "axes.labelsize": 9, "axes.titlesize": 9,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
        "xtick.direction": "out", "ytick.direction": "out", "xtick.major.size": 3.5, "ytick.major.size": 3.5,
        "xtick.minor.size": 2, "ytick.minor.size": 2, "legend.frameon": False, "legend.fontsize": 8,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300, "figure.dpi": 120,
        "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.6, "axes.axisbelow": True,
    })


def group_style(engine, k):
    for key, label, col, mk, hollow in GROUPS:
        if key == engine:
            return label, col, mk, hollow
    return engine, OI["grey"], "P", False  # engine added later: still plotted


def draw_group(ax, rows, ycol, scale, col, mk, hollow, rng, xoff):
    """Points for every fit; median + IQR bar for each p with >= 3 fits."""
    for p, g in rows.groupby("p"):
        y = g[ycol].to_numpy(float) / scale
        y = y[np.isfinite(y) & (y > 0)]
        if len(y) == 0:
            continue
        x = p * 10 ** (xoff + rng.uniform(-0.025, 0.025, len(y))) if len(y) > 1 else np.array([p * 10 ** xoff])
        fc = "none" if hollow else col
        many = len(y) >= 10
        ax.scatter(x, y, s=9 if many else 22, marker=mk, facecolors=fc, edgecolors=col, linewidths=0.8,
                   alpha=0.45 if many else 0.9, zorder=3)
        s = qsum(y)
        if s["n"] >= 3:
            xm = p * 10 ** xoff
            ax.errorbar([xm], [s["med"]], yerr=[[s["med"] - s["q1"]], [s["q3"] - s["med"]]], fmt=mk, ms=6.5,
                        mfc="white" if not hollow else "white", mec=col, ecolor=col, color=col, elinewidth=1.6, capsize=3,
                        capthick=1.6, mew=1.6, zorder=5)


def fig_scaling(sc, out_stem):
    style()
    ok = sc[sc.status == "completed"]
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.7), constrained_layout=False)
    panels = [("core_h", 1.0, "billed core-hours", "(a) compute cost"),
              ("wall_s", 3600.0, "wall time (h)", "(b) wall time"),
              ("peak_rss_gib", 1.0, "peak process memory (GiB)", "(c) memory")]
    engines = list(dict.fromkeys([g[0] for g in GROUPS] + sorted(set(ok.engine) - {g[0] for g in GROUPS})))
    offs = {"v2.2.1": -0.045, "v3.1": 0.045, "v4 smcbvs4": 0.07}   # v4 shifted right so the median/IQR is not hidden by the pilot star
    handles = []
    for ax, (col, scale, ylab, ttl) in zip(axes, panels):
        for e in engines:
            rows = ok[ok.engine == e]
            if rows.empty:
                continue
            label, c, mk, hollow = group_style(e, 0)
            draw_group(ax, rows, col, scale, c, mk, hollow, rng, offs.get(e, 0.0))
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(3e2, 4e6)
        ax.set_xlabel("number of variables $p$ (log scale)")
        ax.set_ylabel(ylab); ax.set_title(ttl, loc="left", fontweight="bold")
        ax.grid(True, which="major")
    for e in engines:
        if (ok.engine == e).any():
            label, c, mk, hollow = group_style(e, 0)
            handles.append(Line2D([], [], marker=mk, ls="", mfc="none" if hollow else c, mec=c, ms=6, label=label))

    # pilot highlight
    pr = sc[sc.run_id == PILOT_ID]
    if len(pr):
        r = pr.iloc[0]
        for ax, (col, scale, _, _) in zip(axes, panels):
            y = r[col] / scale
            if np.isfinite(y):
                ax.scatter([r.p], [y], s=190, marker="*", color=OI["verm"], edgecolor="black", linewidths=0.9, zorder=10)
        axes[0].annotate(f"pilot (6-AR-n200-r01)\n{r.core_h:.0f} core-h", (r.p, r.core_h), xytext=(-8, -42), textcoords="offset points",
                         ha="right", fontsize=8, color=OI["verm"], arrowprops=dict(arrowstyle="-", color=OI["verm"], lw=0.8))
        e2e = f"\n({hm(r.wall_e2e_s)} end-to-end)" if np.isfinite(r.wall_e2e_s) else ""
        axes[1].annotate(f"{hm(r.wall_s)}{e2e}", (r.p, r.wall_s / 3600), xytext=(-8, -42), textcoords="offset points", ha="right",
                         fontsize=8, color=OI["verm"], arrowprops=dict(arrowstyle="-", color=OI["verm"], lw=0.8))
        axes[2].annotate(f"{r.peak_rss_gib:.0f} GiB (calibration)", (r.p, r.peak_rss_gib), xytext=(-8, -24), textcoords="offset points",
                         ha="right", fontsize=8, color=OI["verm"], arrowprops=dict(arrowstyle="-", color=OI["verm"], lw=0.8))
        if np.isfinite(r.peak_rss_sacct_gib):
            axes[2].scatter([r.p], [r.peak_rss_sacct_gib], s=46, marker="D", facecolors="none", edgecolors=OI["verm"], linewidths=1.2, zorder=9)
            axes[2].annotate(f"{r.peak_rss_sacct_gib:.0f} GiB sacct\n(merge, incl. page cache)", (r.p, r.peak_rss_sacct_gib),
                             xytext=(-8, 8), textcoords="offset points", ha="right", fontsize=7.5, color=OI["verm"])
        handles.append(Line2D([], [], marker="*", ls="", mfc=OI["verm"], mec="black", ms=11, label="pilot fit at $p = 10^6$"))

    # v4 slope between 10^5 and 10^6 (medians when replicates exist)
    v4 = ok[ok.engine == "v4 smcbvs4"]
    a, b = v4[v4.p == 1e5].core_h, v4[v4.p == 1e6].core_h
    if len(a) and len(b):
        ratio = np.median(b) / np.median(a); alpha = np.log10(ratio)
        axes[0].text(0.03, 0.97, f"v4: ×{ratio:.1f} core-h for ×10 in $p$\n(log-log slope {alpha:.2f}; n = {len(a)} / {len(b)} fits)",
                     transform=axes[0].transAxes, va="top", fontsize=7.5, color=OI["blue"])
    nrep = len(rep_set(sc))
    fig.text(0.995, 0.005, f"open markers with bars: median and IQR where ≥ 3 fits per p (small points = single fits); 10⁶ replicate set n = {nrep}",
             ha="right", va="bottom", fontsize=7, color="#555555")
    fig.legend(handles=handles, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0), handlelength=1.2, columnspacing=1.6)
    fig.subplots_adjust(left=0.06, right=0.995, top=0.93, bottom=0.30, wspace=0.28)
    for ext in ("pdf", "png"):
        fig.savefig(f"{out_stem}.{ext}")
    plt.close(fig)


# ------------------------------------------------------------------------------------------ fig_stages
def fig_stages(sc, st, out_stem):
    style()
    pil = st[st.run_id == PILOT_ID].set_index("stage").reindex(STAGES)
    if pil.core_h.isna().all():
        sys.exit("no pilot rows in stages_1e6.csv")
    reps = st[st.run_id.isin(rep_set(sc).run_id)]
    nrun = reps.run_id.nunique()
    total = pil.core_h.sum()
    y = np.arange(len(STAGES))[::-1]
    def rep_hi(col, scale):
        """right edge of the median/IQR bar per stage (so value labels do not collide with it)"""
        out = []
        for s_ in STAGES:
            v = reps[reps.stage == s_][col].to_numpy(float) / scale
            v = v[np.isfinite(v)]
            out.append(np.percentile(v, 75) if (nrun >= 3 and len(v)) else -np.inf)   # only the IQR bar sits on the bar row
        return np.array(out)
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.3), sharey=True)
    ttl = ["(a) billed core-hours", "(b) wall time (min)", "(c) peak memory (GiB)"]
    for ax, t in zip(axes, ttl):
        ax.set_title(t, loc="left", fontweight="bold"); ax.grid(True, axis="x"); ax.grid(False, axis="y")
    def overlay(ax, col, scale):
        """replicate points (all rep-set runs) and median/IQR when >= 3 runs"""
        rng = np.random.default_rng(3)
        if nrun < 2:      # pilot only: the bars already show it
            return
        for i, s in enumerate(STAGES):
            v = (reps[reps.stage == s][col].to_numpy(float) / scale)
            v = v[np.isfinite(v)]
            if len(v) == 0:
                continue
            ax.scatter(v, y[i] - 0.40 + rng.uniform(-0.03, 0.03, len(v)), s=8, color="#333333", alpha=0.6, zorder=4, clip_on=False)
            q = qsum(v)
            if q["n"] >= 3:
                ax.errorbar([q["med"]], [y[i]], xerr=[[q["med"] - q["q1"]], [q["q3"] - q["med"]]], fmt="o", ms=5, mfc="white",
                            mec="black", ecolor="black", elinewidth=1.4, capsize=3, zorder=6)
    # (a) core-h
    ax = axes[0]
    ax.barh(y, pil.core_h, 0.6, color=[STAGE_COL[s] for s in STAGES], edgecolor="black", linewidth=0.6, zorder=3)
    for yi, v, h in zip(y, pil.core_h, rep_hi("core_h", 1.0)):
        ax.text(max(v, h) + total * 0.03, yi, f"{v:.1f} ({pct(v, total)})", va="center", fontsize=8)
    ax.set_xlim(0, total * 0.80); ax.set_xlabel("billed core-h (CPUs × elapsed)")
    ax.set_yticks(y); ax.set_yticklabels([STAGE_LABEL[s] for s in STAGES])
    ax.text(0.98, 0.04, f"total {total:.1f} core-h", transform=ax.transAxes, ha="right", fontsize=8.5, fontweight="bold")
    overlay(ax, "core_h", 1.0)
    # (b) wall
    ax = axes[1]; w = pil.wall_s / 60
    ax.barh(y, w, 0.6, color=[STAGE_COL[s] for s in STAGES], edgecolor="black", linewidth=0.6, zorder=3)
    for yi, v, h in zip(y, w, rep_hi("wall_s", 60.0)):
        ax.text(max(v, h) + w.max() * 0.03, yi, f"{v:.1f}", va="center", fontsize=8)
    isl = pil.loc["islands"]
    if np.isfinite(isl.get("wall_span_s", np.nan)):
        yi = y[STAGES.index("islands")]
        ax.plot([isl.wall_span_s / 60] * 2, [yi - 0.3, yi + 0.3], color="black", lw=1.6, zorder=5)
        ax.text(isl.wall_span_s / 60 + w.max() * 0.012, yi + 0.02, f"{isl.wall_span_s / 60:.0f} min: first start → last end", va="center", fontsize=7.5)
    ax.set_xlim(0, max(w.max(), isl.wall_span_s / 60 if np.isfinite(isl.wall_span_s) else 0) * 1.55)
    ax.set_xlabel("elapsed wall time (min); islands: slowest of 16 tasks")
    ws = pil.wall_s.sum()
    ax.text(0.98, 0.04, f"stage sum {hm(ws)}", transform=ax.transAxes, ha="right", fontsize=8.5, fontweight="bold")
    overlay(ax, "wall_s", 60.0)
    # (c) memory
    ax = axes[2]; m = pil.peak_mem_gib
    for yi, s, v, basis, h in zip(y, STAGES, m, pil.mem_basis, rep_hi("peak_mem_gib", 1.0)):
        if np.isfinite(v):
            sacct = str(basis).startswith("sacct")
            ax.barh([yi], [v], 0.6, color=STAGE_COL[s], edgecolor="black", linewidth=0.6, hatch="////" if sacct else None, zorder=3)
            ax.text(max(v, h) + np.nanmax(m) * 0.03, yi, f"{v:.1f}" + (" sacct*" if sacct else ""), va="center", fontsize=8)
        else:
            ax.text(np.nanmax(m) * 0.012, yi, "not recorded", va="center", fontsize=8, color="#555555")
    ax.set_xlim(0, np.nanmax(m) * 1.4); ax.set_xlabel("peak memory (GiB)")
    ax.text(0.98, 0.04, "* sacct MaxRSS incl. page cache;\n  process peak not measured", transform=ax.transAxes, ha="right", fontsize=7.5)
    overlay(ax, "peak_mem_gib", 1.0)
    note = f"bars: pilot (6-AR-n200-r01-V-s1)"
    if nrun >= 3:
        note += f"; dots: each replicate-set fit; ○ with bar: median and IQR (n = {nrun})"
    elif nrun > 1:
        note += f"; dots: replicate-set fits (n = {nrun}; median/IQR from n ≥ 3)"
    fig.text(0.995, 0.01, note, ha="right", va="bottom", fontsize=7, color="#555555")
    fig.subplots_adjust(left=0.10, right=0.995, top=0.90, bottom=0.17, wspace=0.12)
    for ext in ("pdf", "png"):
        fig.savefig(f"{out_stem}.{ext}")
    plt.close(fig)


# ------------------------------------------------------------------------------------------------ tables
def build_tables(sc, st):
    pil = sc[sc.run_id == PILOT_ID]
    if pil.empty:
        sys.exit("pilot row missing from scaling.csv")
    r = pil.iloc[0]
    R = rep_set(sc)
    k = len(R)
    head = f"Replicate set (n = {k}{'; pilot only' if k <= 1 else ''})"

    def cnt(col):
        v = R[col].dropna()
        return f"{int(v.sum())}/{len(v)}" if len(v) else "—"
    f6 = lambda x: f"{x:.6f}"
    f3 = lambda x: f"{x:.3f}".replace("-", "−")
    f1 = lambda x: f"{x:.1f}"
    fh = lambda x: f"{x / 3600:.2f}"
    rows = [  # label, pilot, replicate summary
        ("HPM $= S_0$", "yes (TP 5, FP 0, FN 0)" if r.hpm_eq_S0 == 1 else "no", cnt("hpm_eq_S0")),
        ("MPM $= S_0$", "yes (TP 5, FP 0, FN 0)" if r.mpm_eq_S0 == 1 else "no", cnt("mpm_eq_S0")),
        ("$\\log\\hat Z$", f3(r.logZ), fmt_summary(R.logZ, f3)),
        ("$\\log\\hat Z_T$ (deterministic lower bound)", f3(r.logZ_T), fmt_summary(R.logZ_T, f3)),
        ("predictive $h^2$, HPM (= MPM = oracle)", f6(r.pred_h2_hpm), fmt_summary(R.pred_h2_hpm, f6)),
        ("predictive $h^2$, law mixture $T$", f6(r.pred_h2_T), fmt_summary(R.pred_h2_T, f6)),
        ("wall time, stage sum (h)", f"{r.wall_s / 3600:.2f} ({hm(r.wall_s)})", fmt_summary(R.wall_s, fh)),
        ("wall time, end-to-end incl. queueing (h)", f"{r.wall_e2e_s / 3600:.2f} ({hm(r.wall_e2e_s)})" if np.isfinite(r.wall_e2e_s) else "—",
         fmt_summary(R.wall_e2e_s, fh)),
        ("billed core-h", f"{r.core_h:.1f}", fmt_summary(R.core_h, f1)),
        ("peak process memory, max stage (GiB)", f"{r.peak_rss_gib:.1f}", fmt_summary(R.peak_rss_gib, f1)),
        ("peak memory, merge sacct MaxRSS (GiB)", f"{r.peak_rss_sacct_gib:.1f}" if np.isfinite(r.peak_rss_sacct_gib) else "—",
         fmt_summary(R.peak_rss_sacct_gib, f1)),
    ]
    # stage table
    P = st[st.run_id == PILOT_ID].set_index("stage").reindex(STAGES)
    total = P.core_h.sum()
    Rst = st[st.run_id.isin(R.run_id)]
    srows = []
    for s in STAGES:
        x = P.loc[s]
        req = f"{int(x.n_tasks)} × {int(x.cpus_per_task)} CPUs, {int(x.mem_req_gb)} GB" if x.n_tasks > 1 else f"{int(x.cpus_per_task)} CPUs, {int(x.mem_req_gb)} GB"
        mem = f"{x.peak_mem_gib:.1f}" if np.isfinite(x.peak_mem_gib) else "n/r"
        if str(x.mem_basis).startswith("sacct"):
            mem += "*"
        wl = f"{x.wall_s / 60:.1f}"
        srows.append((STAGE_LABEL[s], req, wl, f"{x.core_h:.2f}", pct(x.core_h, total).replace("%", ""), mem,
                      fmt_summary(Rst[Rst.stage == s].core_h, lambda v: f"{v:.1f}")))
    srows.append(("total", "", f"{P.wall_s.sum() / 60:.1f}", f"{total:.2f}", "100", "", fmt_summary(R.core_h, lambda v: f"{v:.1f}")))
    return head, rows, srows


def tex_escape(s):
    s = s.replace("%", "\\%").replace("—", "---").replace("–", "--").replace("≥", "$\\geq$").replace("×", "$\\times$").replace("−", "$-$").replace("<1", "$<$1")
    return s.replace("[", "{[}").replace("]", "{]}") if False else s


def write_tables(sc, st, stem):
    head, rows, srows = build_tables(sc, st)
    k = len(rep_set(sc))
    # ---- markdown
    def md_math(s):
        return s.replace("$", "").replace("\\log\\hat Z_T", "log Ẑ_T").replace("\\log\\hat Z", "log Ẑ").replace("S_0", "S₀").replace("h^2", "h²")
    L = ["# Pilot fit and replicate summary (generated by make_figures.py; do not edit by hand)", "",
         "**Table 1.** Pilot `6-AR-n200-r01-V-s1` (AR strong, n = 200, p = 10⁶, V mode, N = 2,500, R′ = 16; engine v4 `smcbvs4` @ 2cfaa9e5; "
         "NOTS Sapphire Rapids). Right column: replicate set (pilot = replicate 1 + later rows with `in_rep_set = 1`); median [Q1, Q3] "
         "from n ≥ 3, range for n = 2, dash for n < 2. All values MEASURED except where `scaling.csv` says DERIVED.", "",
         f"| quantity | pilot | {head} |", "|---|---|---|"]
    L += [f"| {md_math(a)} | {b} | {c} |" for a, b, c in rows]
    L += ["", "**Table 2.** Stage breakdown of the pilot (sacct elapsed; billed core-h = allocated CPUs × elapsed). Islands: wall = slowest of 16 "
          "concurrent tasks (the first-start→last-end span was 38 min because of queueing). n/r = not recorded. "
          "\\* = sacct MaxRSS, which includes page cache; the merge process itself was estimated at 26–34 GiB (INFERENCE, `MERGE_MEM.md`).", "",
          f"| stage | request | wall (min) | core-h | % | peak mem (GiB) | rep. median [IQR] core-h (n = {k}) |",
          "|---|---|---:|---:|---:|---:|---|"]
    L += ["| " + " | ".join(x) + " |" for x in srows]
    with open(stem + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    # ---- LaTeX (booktabs); needs \usepackage{booktabs}
    T = ["% generated by make_figures.py; requires \\usepackage{booktabs}", "\\begin{table}[t]", "\\centering\\footnotesize\\setlength{\\tabcolsep}{3pt}",
         "\\caption{Pilot fit $p=10^6$ (AR strong, $n=200$, V mode, $N=2{,}500$, $R'=16$; engine v4, NOTS Sapphire Rapids) and the replicate set "
         "(pilot = replicate 1; median [Q1, Q3] from $n\\ge3$, range for $n=2$, dash for $n<2$).}", "\\label{tab:pilot}",
         "\\begin{tabular}{@{}p{0.34\\linewidth}p{0.25\\linewidth}p{0.36\\linewidth}@{}}", "\\toprule", f"quantity & pilot & {tex_escape(head)} \\\\", "\\midrule"]
    T += [f"{tex_escape(a)} & {tex_escape(b)} & {tex_escape(c)} \\\\" for a, b, c in rows]
    T += ["\\bottomrule", "\\end{tabular}", "\\end{table}", "",
          "\\begin{table}[t]", "\\centering\\footnotesize\\setlength{\\tabcolsep}{3pt}",
          "\\caption{Stage breakdown of the pilot (elapsed wall time; billed core-h $=$ allocated CPUs $\\times$ elapsed). Islands: slowest of 16 concurrent "
          "tasks. n/r: not recorded. $^*$sacct MaxRSS including page cache.}", "\\label{tab:stages}",
          "\\begin{tabular}{@{}p{0.17\\linewidth}rrrrrp{0.17\\linewidth}@{}}", "\\toprule",
          "stage & request & wall (min) & core-h & \\% & peak (GiB) & rep.\\ median [IQR] \\\\", "\\midrule"]
    for i, x in enumerate(srows):
        if x[0] == "total":
            T.append("\\midrule")
        c = [tex_escape(v).replace("*", "$^*$") for v in x]
        T.append(" & ".join(c) + " \\\\")
    T += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    with open(stem + ".tex", "w", encoding="utf-8") as f:
        f.write("\n".join(T) + "\n")


# --------------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=os.path.join(HERE, "data"))
    ap.add_argument("--out", default=HERE)
    a = ap.parse_args()
    sc, st = load(a.data)
    fig_scaling(sc, os.path.join(a.out, "fig_scaling"))
    fig_stages(sc, st, os.path.join(a.out, "fig_stages_1e6"))
    write_tables(sc, st, os.path.join(a.out, "table_pilot"))
    R = rep_set(sc)
    print(f"scaling rows {len(sc)} ({(sc.status == 'completed').sum()} completed); 10^6 replicate set n = {len(R)}; "
          f"stage rows {len(st)} ({st.run_id.nunique()} runs). Wrote fig_scaling, fig_stages_1e6, table_pilot to {a.out}")


if __name__ == "__main__":
    main()
