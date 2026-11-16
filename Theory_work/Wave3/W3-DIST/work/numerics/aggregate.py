import numpy as np, os, csv
class Frame:
    def __init__(self, cols): self._c = cols
    def __len__(self): return len(next(iter(self._c.values())))
    def __getattr__(self, k):
        if k == "_c": raise AttributeError
        return self._c[k]
    def __getitem__(self, k):
        if isinstance(k, str): return self._c[k]
        k = np.asarray(k); return Frame({a: v[k] for a, v in self._c.items()})
def read(fn):
    rows = list(csv.DictReader(open(fn)))
    cols = {}
    for k in rows[0]:
        v = [r[k] for r in rows]
        try: cols[k] = np.array([float(x) for x in v])
        except ValueError: cols[k] = np.array(v, dtype=object)
    return Frame(cols)
ND = 4000; MS = [1, 2, 4, 8, 16]
df = read("raw_reps.csv")
out = []
def P(s=""): out.append(s)
def fmt(x, f="{:.3f}"):
    return "nan" if (x is None or (isinstance(x, float) and np.isnan(x))) else f.format(x)

def tail_stats(g, n):
    ln = np.log(n); R = len(g)
    res = {}
    cnt = np.array([g[f"cnt_M{M}"].sum() for M in MS])
    floor = 0.5 / ND
    lp = np.array([np.mean(np.log(np.maximum(g[f"cnt_M{M}"] / ND, floor))) for M in MS])
    fl = np.array([np.mean(g[f"cnt_M{M}"] == 0) for M in MS])
    pooled = cnt / (R * ND)
    ok = cnt >= 5
    c = np.nan
    if ok.sum() >= 2:
        sl = np.polyfit(np.array(MS)[ok], np.log(pooled[ok]), 1)[0]; c = -sl / ln
    return lp, fl, pooled, c, ok.sum()

summary = {}
def table_main(name, title, extra=None):
    g0 = df[df.name == name]
    if len(g0) == 0: return
    P(f"### {title}"); P()
    P("(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)"); P()
    hdr = "| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | " + " | ".join(f"meanlogΠ M={M}" for M in MS) + " | frac reps floored (M=8,16) | ĉ=−slope/log n |"
    P(hdr); P("|" + "---|" * (hdr.count("|") - 1))
    rows = []
    for n in [int(x) for x in np.unique(g0.n)]:
        g = g0[g0.n == n]; ln = np.log(n)
        lp, fl, pooled, c, nok = tail_stats(g, n)
        r = dict(n=n, R=len(g), m50=n * g.d2_q50.mean(), m90=n * g.d2_q90.mean(), m99=n * g.d2_q99.mean(), mm=n * g.d2_mean.mean(),
                 h50=n * g.h2in_q50.mean(), c=c)
        rows.append(r)
        P(f"| {n} | {len(g)} | {r['m50']:.2f} | {r['m90']:.2f} | {r['m99']:.2f} | {r['m50']/ln:.3f} | {r['m90']/ln:.3f} | {r['m99']/ln:.3f} | {r['mm']:.2f} | {r['h50']:.2f} | "
          + " | ".join(f"{x:.2f}" for x in lp) + f" | {fl[3]:.2f},{fl[4]:.2f} | {fmt(c, '{:.2f}')} |")
    P()
    d = Frame({k: np.array([r[k] for r in rows], dtype=float) for k in rows[0]})
    ln = np.log(d.n)
    s_q99 = np.polyfit(ln, np.log(d.m99), 1)[0]; s_q99l = np.polyfit(ln, np.log(d.m99 / ln), 1)[0]
    s_med = np.polyfit(ln, np.log(d.m50), 1)[0]
    summary[name] = dict(title=title, slope_nd2_q99=s_q99, slope_nd2_med=s_med, slope_nd2log_q99=s_q99l,
                         m99_first=d.m99[0], m99_last=d.m99[-1], m50_last=d.m50[-1], c_last=d.c[-1],
                         c_all=np.nanmedian(d.c))
    P(f"log–log slope of n·d² vs n: median {s_med:.2f}, q99 {s_q99:.2f}; of n·d²/log n (q99): {s_q99l:.2f}"); P()


def supp_tail(name, title):
    g0 = df[df.name == name]
    if len(g0) == 0: return
    P(f"### {title} — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)"); P()
    P("P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.")
    P(); P("| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |"); P("|---|---|---|---|---|---|---|---|---|---|")
    ct = {}
    for n in [int(x) for x in np.unique(g0.n)]:
        f = f"arrays/{name}_n{n}.npz"
        if not os.path.exists(f): continue
        a = np.load(f)["d2"].astype(float).ravel() * n; N = a.size
        pr = lambda t: (a > t).mean()
        ts = np.arange(1, 15); cn = np.array([(a > t).sum() for t in ts]); ok = cn >= 5
        c = np.nan
        if ok.sum() >= 3: c = -np.polyfit(ts[ok], np.log(cn[ok] / N), 1)[0]
        ct[n] = c
        ln = np.log(n)
        P(f"| {n} | {pr(2):.2e} | {pr(4):.2e} | {pr(6):.2e} | {pr(8):.2e} | {pr(12):.2e} | {pr(.5*ln):.2e} | {pr(ln):.2e} | {pr(2*ln):.2e} | {fmt(c,'{:.2f}')} ({ok.sum()}) |")
    P()
    summary[name]["ct"] = ct

def table_extra(name, title):
    g0 = df[df.name == name]
    if len(g0) == 0: return
    P(f"### {title} — selection / size / dropped columns"); P()
    P("| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |"); P("|---|---|---|---|---|---|---|---|---|")
    for n in [int(x) for x in np.unique(g0.n)]:
        g = g0[g0.n == n]
        H = np.array([g[f"size{k}"].sum() for k in range(14)], float); H /= H.sum()
        hs = f"{H[:2].sum():.3f}, {H[2]:.3f}, {H[3]:.3f}, {H[4]:.3f}, {H[5]:.3f}, {H[6:].sum():.3f}"
        dr = g[g.true_dropped > 0]; nd = g[g.true_dropped == 0]
        P(f"| {n} | {g.esize.mean():.2f} | {hs} | {np.nanmean(g.incl0):.2f} | {np.nanmean(g.incl1):.2f} | {np.nanmean(g.incl2):.2f} | {len(dr)}/{len(g)} | {fmt(n*np.median(dr.d2_q50) if len(dr) else np.nan,'{:.1f}')} | {fmt(n*np.median(nd.d2_q50) if len(nd) else np.nan,'{:.2f}')} |")
    P()

P("# W3-DIST numerics — auto-generated tables (aggregate.py; raw per-replication rows in raw_reps.csv)"); P()
P(f"Posterior draws per replication: {ND}; fresh rows per replication: 20000 (40000 for spike). log Π floored at 0.5/{ND} (log = {np.log(0.5/ND):.2f}) when no draw exceeds the threshold; "
  "'frac reps floored' = share of replications at the floor. ĉ = −slope/log n from the regression of log(pooled exceedance fraction) on M over the M with ≥5 exceeding draws pooled over replications."); P()
table_main("N1", "N1 — sub-Gaussian AR(0.5), p=12, s0=3, β*=(1,−1,1)"); table_extra("N1", "N1"); supp_tail("N1", "N1")
table_main("N2a_t25", "N2a — iid t_2.5 coordinates"); supp_tail("N2a_t25", "N2a_t25"); table_extra("N2a_t25", "N2a")
table_main("N2b_pareto", "N2b — symmetric Pareto, tail index 2.1"); supp_tail("N2b_pareto", "N2b_pareto"); table_extra("N2b_pareto", "N2b")
table_main("N2c_spike", "N2c — spike columns"); supp_tail("N2c_spike", "N2c_spike"); table_extra("N2c_spike", "N2c")
table_main("N3", "N3 — no beta-min, β*=(1, c√(log n/n), c√(log n/n)), c=0.7"); supp_tail("N3", "N3"); table_extra("N3", "N3")
for lab in ["n-2", "n-1", "logn_n", "1"]:
    nm = "N4_tau2=" + lab
    table_main(nm, f"N4 — collinear nulls, τ² = {lab}"); supp_tail(nm, f"N4 τ²={lab}"); table_extra(nm, f"N4 τ²={lab}")
table_main("N5", "N5 — approximate sparsity β*_j = c j⁻², Var(xᵀβ*)=3"); supp_tail("N5", "N5"); table_extra("N5", "N5")
for nm, t in [("N7_ar_p4n", "N7 — restricted family, AR(0.5), p=4n"), ("N7_ar_p15", "N7 — restricted family, AR(0.5), p=min(n^1.5,600)"),
              ("N7_t25_p4n", "N7 — restricted family, iid t_2.5, p=4n"), ("N7_t25_p15", "N7 — restricted family, iid t_2.5, p=min(n^1.5,600)")]:
    table_main(nm, t + " (RESTRICTED FAMILY)"); supp_tail(nm, t); table_extra(nm, t)

# N6
P("### N6 — transfer ratio ρ = d²_mean / (2 t̄ + log n / n) over all posterior draws"); P()
P("| design | n | draws | max ρ | pooled 0.999 q | pooled median | max over reps of per-rep 0.999 q |"); P("|---|---|---|---|---|---|---|")
n6 = {}
for name in ["N1", "N2a_t25", "N2b_pareto", "N2c_spike", "N3", "N4_tau2=n-2", "N4_tau2=n-1", "N4_tau2=logn_n", "N4_tau2=1", "N5",
             "N7_ar_p4n", "N7_ar_p15", "N7_t25_p4n", "N7_t25_p15"]:
    allr = []
    for n in [int(x) for x in np.unique(df[df.name == name].n)]:
        f = f"arrays/{name}_n{n}.npz"
        if not os.path.exists(f): continue
        r = np.load(f)["rho"].astype(float).ravel(); allr.append(r)
        g = df[(df.name == name) & (df.n == n)]
        P(f"| {name} | {n} | {r.size} | {r.max():.3f} | {np.quantile(r, .999):.3f} | {np.median(r):.3f} | {g.rho_q999.max():.3f} |")
    if allr:
        a = np.concatenate(allr); n6[name] = (a.max(), np.quantile(a, .999))
P(); P("Overall per design (all n pooled): " + "; ".join(f"{k}: max {v[0]:.3f}, q.999 {v[1]:.3f}" for k, v in n6.items())); P()

# final
P("## Final table"); P()
P("Rule: 'bounded' = log–log slope of the statistic against n is below 0.15 (growth slower than n^0.15; log n alone would give about 0.3–0.4 over n=50…800), "
  "'unclear' 0.15–0.30, 'no' above 0.30. 'n·d² bounded' is read on the median and q99. Tail slope: ĉ at the largest n (and median over n).  "); P()
P("| design | n·d²/log n bounded? (q99 slope) | n·d² bounded? (med slope / q99 slope) | n·d² med at largest n | n·d² q99 at smallest→largest n | tail rate c_t (log P(n d²>t) ≈ −c_t t), per n |"); P("|---|---|---|---|---|---|")
def yn(s): return "yes" if s < .15 else ("unclear" if s < .30 else "no")
for k, s in summary.items():
    cts = ', '.join(f'{n}:{fmt(c,"{:.2f}")}' for n, c in s.get('ct', {}).items())
    P(f"| {k} | {yn(s['slope_nd2log_q99'])} ({s['slope_nd2log_q99']:.2f}) | {yn(max(s['slope_nd2_med'], s['slope_nd2_q99']))} ({s['slope_nd2_med']:.2f} / {s['slope_nd2_q99']:.2f}) | {s['m50_last']:.2f} | {s['m99_first']:.2f} → {s['m99_last']:.2f} | c_t by n: {cts} |")
open("RESULTS_tables.md", "w").write("\n".join(out))
print("\n".join(out[-30:]))
