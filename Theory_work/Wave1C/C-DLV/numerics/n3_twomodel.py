import sys, os, json, math, glob, csv
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from psi_enum import build_grid   # exact replay function, imported unchanged

def rho(lg0, d, u, v):
    F = lambda t: logsumexp(lg0 + t * d)
    return math.exp(2 * F(v) - F(u) - F(2 * v - u))

def count_Nb(lg0, d, targets):
    """re-walk the same loop as build_grid; count steps with rho_V(u,b) < 0.90 (b = next target above u)."""
    targets = sorted(targets); u = 0.0; nb = 0; grid = [0.0]
    g, reason = build_grid(lg0, d, targets, 10**9)
    for v in g[1:]:
        b = next(t for t in targets if t > u)
        if not rho(lg0, d, u, b) >= 0.90: nb += 1
        u = v
    return nb

rows = []
T = np.linspace(0, 2, 4001)
for f in sorted(glob.glob(os.path.join(HERE, "n3", "*.json"))):
    J = json.load(open(f))
    for k, c in enumerate(J["cons"]):
        lg0 = np.array(c["log_gamma0"], float); d = np.array(c["d"], float)
        sched = [float(x) for x in np.atleast_1d(c["schedule"])]
        code_grid = np.atleast_1d(np.array(c["grid"], float))
        rg, rreason = build_grid(lg0, d, sched, int(c["T_e"]))
        rg = np.array(rg)
        same_len = len(rg) == len(code_grid)
        maxdiff = float(np.max(np.abs(rg - code_grid))) if same_len else float("nan")
        Nb = count_Nb(lg0, d, sched)
        i1 = int(np.argmax(lg0)); i2 = int(np.argmax(lg0 + d))
        x0 = float(lg0[i2] - lg0[i1]); D = float(d[i2] - d[i1])
        def rmax_on(hi):
            m = 0.0
            for t in np.linspace(0, hi, 4001):
                w = lg0 + t * d; lz = logsumexp(w)
                r = 1 - math.exp(w[i1] - lz) - (0.0 if i1 == i2 else math.exp(w[i2] - lz))
                m = max(m, r)
            return m
        rmax = rmax_on(2.0); r125 = rmax_on(1.25); r150 = rmax_on(1.5)
        def Bfun(eps):
            th = 0.9 / (1 - eps) ** 2; s0 = 2 * math.atanh(math.sqrt(1 - th)); lam = math.log(th / (1 - th))
            return 1 + math.ceil((2 * lam + 2 * s0) / (s0 / 2)) + math.ceil(math.log(max(1, (-x0 - lam) / (2 * s0))) / math.log(4 / 3))
        row = dict(file=os.path.basename(f), design=J["design"], n=J["n"], p=J["p"], seed=J["seed"], tier=c["tier"],
                   label=c["label"], T_e=c["T_e"], V_size=c["V_size"], code_ok=c["ok"], code_reason=c["reason"],
                   code_intervals=c["intervals"], replay_reason=rreason, replay_intervals=len(rg) - 1,
                   len_match=same_len, max_abs_diff=maxdiff, mismatch=(not same_len) or maxdiff > 1e-12,
                   N_b_replay=Nb, N_b_code_minus_Np=c["intervals"] - (len(sched) - 1), N_p=len(sched) - 1,
                   M1_eq_M2=(i1 == i2), M1=c["models"][i1], M2=c["models"][i2], x0=x0, D=D, r_max=rmax, r_max_125=r125, r_max_150=r150,
                   B=np.nan, Nb_le_B=None, B125=np.nan, Nb_le_B125=None)
        if rmax <= 0.02:
            row["B"] = Bfun(rmax); row["Nb_le_B"] = Nb <= row["B"]
        if r125 <= 0.02:
            row["B125"] = Bfun(r125) + math.ceil(math.log(2.25 / 0.25) / math.log(4 / 3)) + 1; row["Nb_le_B125"] = Nb <= row["B125"]
        rows.append(row)
keys = list(rows[0].keys())
with open(os.path.join(HERE, "N3_twomodel.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(rows)

R = np.array([r["r_max"] for r in rows]); N = len(rows)
out = ["# N3 two-model check (numbers only)", "",
       f"Constructions: {N} from {len(set(r['file'] for r in rows))} fits (designs M,F; (800,108),(1600,135); seeds 1-4).",
       f"Replay (psi_enum.build_grid, saved schedule as targets, saved T_e) vs code grid: length mismatches {sum(not r['len_match'] for r in rows)}, "
       f"mismatches (length or max abs diff > 1e-12) {sum(r['mismatch'] for r in rows)}, "
       f"max abs diff over same-length cases {np.nanmax([r['max_abs_diff'] for r in rows]):.3e}; replay reason != 'ok': {sum(r['replay_reason']!='ok' for r in rows)}.",
       f"N_b (replay, steps with rho<0.90): max {max(r['N_b_replay'] for r in rows)}; equals (code intervals - N_p) in {sum(r['N_b_replay']==r['N_b_code_minus_Np'] for r in rows)}/{N}.",
       f"M1 == M2: {sum(r['M1_eq_M2'] for r in rows)}/{N}.",
       f"r_max quantiles (0,10,25,50,75,90,100%): " + ", ".join(f"{q:.4g}" for q in np.quantile(R, [0, .1, .25, .5, .75, .9, 1])),
       f"fraction r_max <= 0.01: {np.mean(R<=0.01):.3f} ({int((R<=0.01).sum())}/{N}); <= 0.02: {np.mean(R<=0.02):.3f} ({int((R<=0.02).sum())}/{N}).", ""]
for key, nm in (("r_max", "[0,2]"), ("r_max_150", "[0,1.5]"), ("r_max_125", "[0,1.25]")):
    A = np.array([r[key] for r in rows])
    out.append(f"range {nm}: quantiles (0,50,90,100%) " + ", ".join(f"{q:.4g}" for q in np.quantile(A, [0, .5, .9, 1])) + f"; frac <=0.01: {np.mean(A<=0.01):.3f} ({int((A<=0.01).sum())}/{N}); frac <=0.02: {np.mean(A<=0.02):.3f} ({int((A<=0.02).sum())}/{N})")
ok125 = [r for r in rows if r["Nb_le_B125"] is not None]
if ok125:
    out.append(f"B125 (eps = r_max_125, plus ceil(log(9)/log(4/3))+1 = {math.ceil(math.log(9)/math.log(4/3))+1}) evaluated on {len(ok125)}: max N_b {max(r['N_b_replay'] for r in ok125)}, min/max B125 {min(r['B125'] for r in ok125)}/{max(r['B125'] for r in ok125)}, max N_b/B125 {max(r['N_b_replay']/r['B125'] for r in ok125):.4f}; N_b > B125: {sum(not r['Nb_le_B125'] for r in ok125)}")
    for r in ok125:
        if not r["Nb_le_B125"]: out.append(f"  VIOLATION125 {r['file']} tier {r['tier']} {r['label']}: N_b={r['N_b_replay']} B125={r['B125']}")
out.append("")
ok = [r for r in rows if r["Nb_le_B"] is not None]
if ok:
    ratios = [r["N_b_replay"] / r["B"] for r in ok]
    out += [f"Bound evaluated on {len(ok)} constructions (r_max <= 0.02): max N_b {max(r['N_b_replay'] for r in ok)}, min B {min(r['B'] for r in ok)}, max B {max(r['B'] for r in ok)}, max N_b/B {max(ratios):.4f}.",
            f"N_b > B: {sum(not r['Nb_le_B'] for r in ok)}"]
    for r in ok:
        if not r["Nb_le_B"]: out.append(f"  VIOLATION {r['file']} tier {r['tier']} {r['label']}: N_b={r['N_b_replay']} B={r['B']} r_max={r['r_max']:.4g}")
else: out.append("Bound not evaluated (no construction with r_max <= 0.02).")
out += ["", "Per (design, n): constructions, median r_max, max r_max, #r_max<=0.02, max N_b, M1==M2 count", "```"]
for dsg in "MF":
    for n in (800, 1600):
        s = [r for r in rows if r["design"] == dsg and r["n"] == n]
        if s: out.append(f"{dsg} n={n}: {len(s)}, {np.median([r['r_max'] for r in s]):.4g}, {max(r['r_max'] for r in s):.4g}, {sum(r['r_max']<=0.02 for r in s)}, {max(r['N_b_replay'] for r in s)}, {sum(r['M1_eq_M2'] for r in s)}")
out.append("```")
open(os.path.join(HERE, "N3_SUMMARY.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
