r"""F-SHARE H2 / f2: simulation of the SMC-BVS v3 final run (exact small-p engine bvs_core.py) on the linked-hub
designs LH16 / LH20 (lh_design.py), testing the delivery-theorem claims:
  (C1) closure: no particle outside W := {x : Sref ⊆ x};
  (C2) most particles in W_0 := {Sref u A : A ⊆ M} or W_2 := W ∩ {<= 2 extras outside S0};
  (C3) S0 first scored at the predicted crossing stage t* = first t with grid[t] >= phi*,
       phi* = -g0 / (g1 - g0) at x = Sref (g_i = lg_i(Sref+b) - lg_i(Sref); max over masked hubs b);
  (C4) the hub-complete class H := {x : S0 ⊆ x} takes over shortly after t*, n_T(H) ≈ N;
  (C5) delivery to W_0 u H at the terminal boundary never fails.
Set counts are snapshots taken by bvs_core.island after each stage's move round (stage 0 = initial pi0 draw) plus
the final states after the L+4 terminal rounds; intermediate states inside a round (and the resampled population
before the round) are not counted separately (the resampled population is a sub-multiset of the previous snapshot).

Usage: python f2_sim_lh.py CONFIG n1,n2,... DATASETS ISLANDS_PER_DATASET [N]      (writes results/f2_sim_lh_CONFIG.*)
       python f2_sim_lh.py --merge                                                  (writes results/f2_sim_lh.{txt,json})
Seeds: dataset seed = 1000*n + 17*ds + cfg offset; island rng seeded from (20261102, n, ds, island).
"""
import sys, os, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bvs_core import BVS, suff_stats, popcount  # noqa: E402
from lh_design import lh_config  # noqa: E402

RES = os.path.join(os.path.dirname(HERE), "results")
os.makedirs(RES, exist_ok=True)


def crossing(m, Sref, M):
    x = sum(1 << j for j in Sref)
    out = []
    for b in M:
        xb = x | (1 << b)
        g1 = m.lg1[xb] - m.lg1[x]
        g0 = m.lg0[xb] - m.lg0[x]
        if g0 >= 0:
            ph = 0.0
        elif g1 <= g0 or g1 <= 0:
            ph = float("inf")
        else:
            ph = -g0 / (g1 - g0)
        out.append(dict(b=int(b), g0=float(g0), g1=float(g1), phi_star=float(ph)))
    return out


def tstar_of(grid, phi_star):
    if not np.isfinite(phi_star):
        return None
    for t in range(1, len(grid)):
        if grid[t] >= phi_star:
            return t
    return None


def run_config(cfg_name, ns, n_ds, n_isl, N0=1000):
    c = lh_config(cfg_name)
    p = c["p"]
    S0m = sum(1 << j for j in c["S0"]); Srefm = sum(1 << j for j in c["Sref"]); Mm = sum(1 << j for j in c["M"])
    allm = np.arange(1 << p, dtype=np.int64)
    W = (allm & Srefm) == Srefm
    W0 = (allm & ~Mm) == Srefm
    W2 = W & (popcount(allm & ~S0m) <= 2)
    H = (allm & S0m) == S0m
    sets = dict(W=W, W0=W0, W2=W2, H=H, W0H=W0 | H)
    lines, recs = [], []

    def pr(s=""):
        lines.append(s); print(s, flush=True)

    pr(f"######## {cfg_name}: p={p} S0={c['S0']} Sref={c['Sref']} M={c['M']} lambda_min(R)={c['lam_min']:.4f}")
    pr("(set counts = snapshots after each stage's move round, stage 0 = initial draw, plus final states after the "
       "terminal rounds; within-round states not counted)")
    off = 0 if cfg_name == "LH16" else 7
    for n in ns:
        N = N0
        pr(f"\n==== {cfg_name}  n={n}  N={N}  {n_ds} datasets x {n_isl} islands")
        printed_trace = False
        for ds in range(n_ds):
            t0 = time.time()
            z, yy = suff_stats(c["R"], c["theta"], 1.0, n, np.random.default_rng(1000 * n + 17 * ds + off))
            m = BVS(c["R"], z, yy, n, c["S0"])
            grid, pil, forced = m.method_grid()
            T = len(grid) - 1
            cr = crossing(m, c["Sref"], c["M"])
            phs = max(x["phi_star"] for x in cr)
            ts = tstar_of(grid, phs)
            pr(f"-- ds{ds}: build+grid {time.time()-t0:.0f}s; blocks={m.blocks}; T={T} (pilot {len(pil)-1}, forced {forced}); "
               f"L={m.L}; pi(S0)={m.post[m.S0]:.3f}; pi0(S0)={m.pi0[m.S0]:.2e}; start mode={m.fmt(m.start_mode)}; "
               f"pi0(W)={m.pi0[W].sum():.4f} pi0(W0)={m.pi0[W0].sum():.4f} pi(W0uH)={m.post[W0|H].sum():.3f}")
            pr("   crossing: " + "; ".join(f"b={x['b']}: g0={x['g0']:.2f} g1={x['g1']:.2f} phi*={x['phi_star']:.4f}" for x in cr)
               + f"  -> phi*={phs:.4f}, t*={ts} (grid[t*]={grid[ts] if ts is not None else float('nan'):.4f})")
            pr("   grid: " + " ".join(f"{g:.4f}" for g in grid))
            for isl in range(n_isl):
                rng = np.random.default_rng([20261102, n, ds, isl, off])
                ti = time.time()
                info = m.island(N, grid, rng, sets=sets)
                dt = time.time() - ti
                if dt > 90 and N > 500:
                    pr(f"   island took {dt:.0f}s > 90s at N={N}: reducing N to 500 for the remaining islands")
                    N = 500
                cnt = {k: info["counts"][k].tolist() + [info["final_counts"][k]] for k in sets}  # stages 0..T, final
                Nn = N if dt <= 90 or N == 500 else N
                Nn = len(info["final_states"])
                outW = sum(1 for v in cnt["W"] if v < Nn)
                fs = info["first_S0"]
                fs_stage = fs[0] if fs else None
                fs_mech = fs[1] if fs else "never"
                fs_phi = (float(grid[fs_stage]) if fs_stage < len(grid) else 1.0) if fs else None
                fW2 = np.array(cnt["W2"]) / Nn
                Hb = np.array(info["counts"]["H"]) / Nn
                t50 = next((t for t in range(T + 1) if Hb[t] >= 0.5), None)
                t99 = next((t for t in range(T + 1) if Hb[t] >= 0.99), None)
                minP = {k: float(np.min(np.cumsum(info["logr"][k]))) if len(info["logr"][k]) else 0.0 for k in ("W", "W0")}
                rec = dict(config=cfg_name, n=n, ds=ds, island=isl, N=Nn, T=T, grid=grid.tolist(), crossing=cr,
                           phi_star=phs, tstar=ts, first_S0_stage=fs_stage, first_S0_mech=fs_mech, first_S0_phi=fs_phi,
                           n_snap_outside_W=outW, counts=cnt, frac_outside_W2_max=float(1 - fW2.min()),
                           frac_outside_W2_median=float(np.median(1 - fW2)), H_t50=t50, H_t99=t99,
                           nT_bridge={k: info["counts"][k][-1] for k in sets}, final=info["final_counts"],
                           minlogP_W=minP["W"], minlogP_W0=minP["W0"], logZhat_over_Z=float(info["logZhat_over_Z"]),
                           pi_S0=float(m.post[m.S0]), seconds=dt)
                recs.append(rec)
                pr(f"   isl{isl}: {dt:.1f}s outW-snaps={outW} maxfrac!W2={rec['frac_outside_W2_max']:.3f} "
                   f"S0 first=({fs_stage},{fs_mech},phi={fs_phi if fs_phi is None else round(fs_phi,4)}) t*={ts} "
                   f"H>=50% t={t50} H>=99% t={t99}  n_T(bridge) W/W0/H={rec['nT_bridge']['W']}/{rec['nT_bridge']['W0']}/{rec['nT_bridge']['H']}"
                   f"  final W/W0/H/W0uH={cnt['W'][-1]}/{cnt['W0'][-1]}/{cnt['H'][-1]}/{cnt['W0H'][-1]}"
                   f"  minlogP W={minP['W']:.3f} W0={minP['W0']:.3f}  log(Zhat/Z)={rec['logZhat_over_Z']:.3f}")
                if not printed_trace:
                    printed_trace = True
                    pr("   trace (ds0 isl0): stage phi  fW  fW0  fW2  fH")
                    for t in range(T + 2):
                        ph = grid[t] if t <= T else 1.0
                        lab = str(t) if t <= T else "final"
                        pr(f"     {lab:>5} {ph:.4f} " + " ".join(f"{cnt[k][t]/Nn:.3f}" for k in ("W", "W0", "W2", "H")))
        summarize(pr, [r for r in recs if r["n"] == n], cfg_name, n)
        dump(cfg_name, lines, recs)
    return lines, recs


def summarize(pr, rs, cfg, n):
    if not rs:
        return
    k = len(rs)
    anyout = sum(r["n_snap_outside_W"] > 0 for r in rs)
    med = np.median([r["frac_outside_W2_median"] for r in rs]); mx = max(r["frac_outside_W2_max"] for r in rs)
    diff = [r["first_S0_stage"] - r["tstar"] for r in rs if r["first_S0_stage"] is not None and r["tstar"] is not None]
    mech = {}
    for r in rs:
        mech[r["first_S0_mech"]] = mech.get(r["first_S0_mech"], 0) + 1
    stages = sorted({(r["first_S0_stage"], r["tstar"]) for r in rs}, key=str)
    fullH_bridge = sum(r["nT_bridge"]["H"] == r["N"] for r in rs)
    fullH_final = sum(r["final"]["H"] == r["N"] for r in rs)
    fail = sum(r["final"]["W0H"] == 0 for r in rs)
    pr(f"## SUMMARY {cfg} n={n} ({k} islands): islands with any particle outside W: {anyout}; "
       f"frac outside W2 over stages: median {med:.3f}, max {mx:.3f}")
    pr(f"   S0 first-scored stage - t*: {sorted(diff)}  (pairs (first, t*): {stages}); mechanisms {mech}")
    pr(f"   n_T(H)=N at end of bridge: {fullH_bridge}/{k}; at final: {fullH_final}/{k}; "
       f"median H>=50% stage {np.median([r['H_t50'] if r['H_t50'] is not None else 99 for r in rs])}, "
       f"H>=99% {np.median([r['H_t99'] if r['H_t99'] is not None else 99 for r in rs])}; delivery failures (final W0uH = 0): {fail}")
    pr(f"   min log P_t: W {min(r['minlogP_W'] for r in rs):.3f}, W0 {min(r['minlogP_W0'] for r in rs):.3f}; "
       f"log(Zhat/Z) median {np.median([r['logZhat_over_Z'] for r in rs]):.3f}, range "
       f"[{min(r['logZhat_over_Z'] for r in rs):.3f}, {max(r['logZhat_over_Z'] for r in rs):.3f}]")


def dump(cfg, lines, recs):
    with open(os.path.join(RES, f"f2_sim_lh_{cfg}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(RES, f"f2_sim_lh_{cfg}.json"), "w", encoding="utf-8") as f:
        json.dump(recs, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))


def merge():
    txt, js = [], []
    for cfg in ("LH16", "LH20"):
        pt = os.path.join(RES, f"f2_sim_lh_{cfg}.txt")
        if os.path.exists(pt):
            txt.append(open(pt, encoding="utf-8").read())
            js += json.load(open(os.path.join(RES, f"f2_sim_lh_{cfg}.json"), encoding="utf-8"))
    open(os.path.join(RES, "f2_sim_lh.txt"), "w", encoding="utf-8").write("\n".join(txt))
    json.dump(js, open(os.path.join(RES, "f2_sim_lh.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "--merge":
        merge()
    else:
        cfg = sys.argv[1]; ns = [int(x) for x in sys.argv[2].split(",")]
        nds, nisl = int(sys.argv[3]), int(sys.argv[4])
        N0 = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
        run_config(cfg, ns, nds, nisl, N0)
