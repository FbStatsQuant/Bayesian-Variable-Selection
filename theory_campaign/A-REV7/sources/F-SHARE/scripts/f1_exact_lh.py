r"""F-SHARE / H1: exact checks on the basin W = {x : S° ⊆ x} for the linked-hub (LH) designs.

For LH16 and LH20, n in {400, 1600, 6400, 25600}, independent noise replicates (fresh suff_stats each), exact
enumeration (bvs_core.BVS) of F = lg1 (log posterior up to a constant) and lg0 (log start law up to a constant),
d = lg1 - lg0.  Computes over ALL feasible x in W (size <= K, lg0 and lg1 finite):
  Q1 keep margins   m1 = min_{x in W, j in S°} F(x) - F(x-j),  m0 = same with lg0
  Q2 hub crossing   g1 = F(x+b) - F(x), g0 = lg0(x+b) - lg0(x) for masked hubs b not in x; phi* = -g0/(g1-g0)
  Q3 extras         a1 = max F(x+l)-F(x), a0 = max lg0(x+l)-lg0(x), dmax/dmin of d(x+l)-d(x), l not in S0 ∪ x;
                    tot1 = max_x sum_l exp(F(x+l)-F(x)), tot0 likewise; also restricted to x with <= 2 extras
  Q4 masses         pi0(W^c), pi(W^c), |W|, pi0(W0), pi(W0), min_phi q_phi(W), min_phi q_phi(W0)
  Q5 exit bound     eta(x) = sum_{j in S°} max(kappa0, kappa1)(x, j); max over W
  Q6 fixed-Gaussian spread of F(x+l)-F(x) across x in W (<= 2 extras) with equal x ∩ group(l), l null
"Extras" of x := x \ S0 (elements outside the full true support S0 = S° ∪ M).

Scores: BVS is subclassed only to vectorise the index extraction and cache the data-free log-det terms per (R, n)
(identical formula; checked to agree with the original class to ~1e-9 on LH16 at the start of the run).

Usage: python f1_exact_lh.py [reps16=20] [reps20=5]
Writes ../results/f1_exact_lh.txt (printed table) and ../results/f1_exact_lh.json (raw numbers).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import sys, json, time
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from bvs_core import BVS, suff_stats, popcount, lse
from lh_design import lh_config

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
NS = [400, 1600, 6400, 25600]
SEED = 20261102


class BVSfast(BVS):
    """Same scores as BVS._logm_rel; index extraction vectorised and data-free log-dets cached per (R, n)."""
    _cache = {}

    def _logm_rel(self, masks):
        n, a0, b0 = self.n, 0.01, 0.01
        nu = a0 + n / 2
        out = np.empty(len(masks))
        sizes = popcount(masks)
        base = -nu * np.log(2 * b0 + self.yy)
        key = (self.R.tobytes(), n, masks.tobytes())
        cache = BVSfast._cache.get(key)
        if cache is None:
            cache = {}
            for k in np.unique(sizes):
                sel = np.where(sizes == k)[0]
                if k == 0:
                    cache[k] = (sel, None, None); continue
                bits = ((masks[sel][:, None] >> np.arange(self.p)) & 1).astype(bool)
                idx = np.nonzero(bits)[1].reshape(len(sel), k)
                Gs = (n - 1) * self.R[idx[:, :, None], idx[:, None, :]]
                I = np.eye(k)
                H = (n + 1) * Gs + I
                ldH = np.linalg.slogdet(H)[1]; ldG = np.linalg.slogdet(Gs + I)[1]
                cache[k] = (sel, idx.astype(np.int16), -0.5 * (ldH - ldG))
                del Gs, H
            BVSfast._cache = {key: cache}   # keep only the current (R, n)
        for k, (sel, idx, ld) in cache.items():
            if k == 0:
                out[sel] = base; continue
            H = (n + 1) * (n - 1) * self.R[idx[:, :, None], idx[:, None, :]] + np.eye(k)
            zs = self.z[idx]
            sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
            Q = self.yy - n * np.sum(zs * sol, axis=1)
            out[sel] = ld - nu * np.log(2 * b0 + Q)
        return out - base


def bm(S):
    return sum(1 << j for j in S)


def analyse(b, cfg):
    p, n = b.p, b.n
    masks = np.arange(b.nstates, dtype=np.int64)
    F, G0, d = b.lg1, b.lg0, b.d
    feas = np.isfinite(F) & np.isfinite(G0)
    Sref, M, S0 = bm(cfg["Sref"]), bm(cfg["M"]), bm(cfg["S0"])
    W = feas & ((masks & Sref) == Sref)
    ext = popcount(masks & ~S0)
    W2 = W & (ext <= 2)
    W0 = np.zeros(b.nstates, bool)
    for sub in range(1 << len(cfg["M"])):
        A = sum(1 << cfg["M"][i] for i in range(len(cfg["M"])) if (sub >> i) & 1)
        W0[Sref | A] = True
    W0 &= feas
    out = {"n": n, "K": b.K, "absW": int(W.sum()), "absW0": int(W0.sum())}

    # ---------------- Q1 keep margins
    m1, m0 = np.inf, np.inf; am1 = am0 = None
    for j in cfg["Sref"]:
        x = masks[W]; y = x & ~(1 << j)
        ok = feas[y]; x, y = x[ok], y[ok]
        v1 = F[x] - F[y]; v0 = G0[x] - G0[y]
        i1, i0 = np.argmin(v1), np.argmin(v0)
        if v1[i1] < m1: m1, am1 = v1[i1], (int(x[i1]), j)
        if v0[i0] < m0: m0, am0 = v0[i0], (int(x[i0]), j)
    out.update(m1=float(m1), m0=float(m0), m1_n=float(m1 / n), m0_n=float(m0 / n),
               m1_arg=b.fmt(am1[0]) + " -" + str(am1[1]), m0_arg=b.fmt(am0[0]) + " -" + str(am0[1]),
               m1_arg_ext=int(popcount(am1[0] & ~S0)), m0_arg_ext=int(popcount(am0[0] & ~S0)))
    # keep margins at S° itself (and at S0 for the masked hub)
    out["m1_at_Sref"] = float(min(F[Sref] - F[Sref & ~(1 << j)] for j in cfg["Sref"]))
    out["m0_at_Sref"] = float(min(G0[Sref] - G0[Sref & ~(1 << j)] for j in cfg["Sref"]))

    # ---------------- Q2 hub crossing
    g1min, g0max, phimax, nneg, ng0pos, npairs = np.inf, -np.inf, -np.inf, 0, 0, 0
    g1min_arg = g0max_arg = phimax_arg = None
    phi_at_Sref = []; g1_at_Sref = []; g0_at_Sref = []
    for bb in cfg["M"]:
        sel = W & ((masks >> bb) & 1 == 0)
        x = masks[sel]; y = x | (1 << bb)
        ok = feas[y]; x, y = x[ok], y[ok]
        g1 = F[y] - F[x]; g0 = G0[y] - G0[x]
        npairs += len(x)
        nneg += int(np.sum(g1 <= 0)); ng0pos += int(np.sum(g0 >= 0))
        i = np.argmin(g1)
        if g1[i] < g1min: g1min, g1min_arg = g1[i], (int(x[i]), bb)
        i = np.argmax(g0)
        if g0[i] > g0max: g0max, g0max_arg = g0[i], (int(x[i]), bb)
        cr = (g0 < 0) & (g1 > 0)
        ph = np.full(len(x), np.nan); ph[cr] = -g0[cr] / (g1[cr] - g0[cr])
        if cr.any():
            i = np.nanargmax(ph)
            if ph[i] > phimax: phimax, phimax_arg = ph[i], (int(x[i]), bb)
        g1s = F[Sref | (1 << bb)] - F[Sref]; g0s = G0[Sref | (1 << bb)] - G0[Sref]
        g1_at_Sref.append(float(g1s)); g0_at_Sref.append(float(g0s))
        phi_at_Sref.append(float(-g0s / (g1s - g0s)) if (g0s < 0 < g1s) else float("nan"))
    ref_g0 = -np.log(2 * p) - 0.5 * np.log(n + 1)
    out.update(g1min=float(g1min), g1min_n=float(g1min / n), g1min_arg=b.fmt(g1min_arg[0]) + " +" + str(g1min_arg[1]),
               g0max=float(g0max), g0max_minus_ref=float(g0max - ref_g0), g0max_arg=b.fmt(g0max_arg[0]) + " +" + str(g0max_arg[1]),
               phimax=float(phimax), phimax_arg=b.fmt(phimax_arg[0]) + " +" + str(phimax_arg[1]),
               phi_at_Sref=max(phi_at_Sref), g1_at_Sref_n=float(min(g1_at_Sref) / n), g0_at_Sref=float(max(g0_at_Sref)),
               n_g1_le0=nneg, n_g0_ge0=ng0pos, n_hubpairs=npairs, ref_g0=float(ref_g0))

    # ---------------- Q3 extras
    g = cfg["g"]
    proxy_of = [sum(1 << bb for bb in cfg["M"] if (l - l % g) == (bb - bb % g)) for l in range(p)]

    def q3(Wset, nonproxy=False):
        """nonproxy: drop pairs (x, l) with l in the group of a masked hub b not in x (l is then a proxy of b)."""
        a1 = a0 = dmax = -np.inf; dmin = np.inf
        a1_arg = None
        ltot1 = np.full(b.nstates, -np.inf); ltot0 = np.full(b.nstates, -np.inf)
        npos1 = 0
        for l in range(p):
            if (S0 >> l) & 1: continue
            sel = Wset & ((masks >> l) & 1 == 0)
            x = masks[sel]; y = x | (1 << l)
            ok = feas[y]
            if nonproxy:
                ok &= (proxy_of[l] & ~x) == 0
            x, y = x[ok], y[ok]
            if len(x) == 0: continue
            v1 = F[y] - F[x]; v0 = G0[y] - G0[x]; vd = d[y] - d[x]
            npos1 += int(np.sum(v1 > 0))
            i = np.argmax(v1)
            if v1[i] > a1: a1, a1_arg = v1[i], (int(x[i]), l)
            a0 = max(a0, v0.max()); dmax = max(dmax, vd.max()); dmin = min(dmin, vd.min())
            ltot1[x] = np.logaddexp(ltot1[x], v1); ltot0[x] = np.logaddexp(ltot0[x], v0)
        if a1_arg is None:
            return None
        lt1 = ltot1[Wset]; lt0 = ltot0[Wset]
        i1 = np.argmax(lt1)
        return dict(a1=float(a1), a0=float(a0), dmax=float(dmax), dmin=float(dmin),
                    a1_arg=b.fmt(a1_arg[0]) + " +" + str(a1_arg[1]), n_a1_pos=npos1,
                    log_tot1=float(lt1.max()), log_tot0=float(lt0.max()),
                    log_tot1_arg=b.fmt(int(masks[Wset][i1])))
    Wf = W & ((masks & M) == M)   # x ⊇ S0
    out["Q3"] = q3(W); out["Q3_le2"] = q3(W2)
    out["Q3_full"] = q3(Wf); out["Q3_full_le2"] = q3(Wf & (ext <= 2))
    out["Q3_np"] = q3(W, True); out["Q3_np_le2"] = q3(W2, True)
    out["Q3_proxyonly_count"] = out["Q3"]["n_a1_pos"] - out["Q3_np"]["n_a1_pos"]

    # ---------------- Q4 masses (log scale)
    lZ0, lZ1 = lse(G0[feas]), lse(F[feas])
    Wc = feas & ~W
    out.update(log_pi0_Wc=float(lse(G0[Wc]) - lZ0), log_pi_Wc=float(lse(F[Wc]) - lZ1),
               pi0_W0=float(np.exp(lse(G0[W0]) - lZ0)), pi_W0=float(np.exp(lse(F[W0]) - lZ1)),
               pi0_W=float(np.exp(lse(G0[W]) - lZ0)), pi_W=float(np.exp(lse(F[W]) - lZ1)))
    qW, qW0 = [], []
    for phi in np.linspace(0, 1, 101):
        lg = G0[feas] + phi * d[feas]
        L = lse(lg)
        qW.append(lse(lg[W[feas]]) - L); qW0.append(lse(lg[W0[feas]]) - L)
    qW, qW0 = np.exp(qW), np.exp(qW0)
    out.update(min_qW=float(qW.min()), argmin_qW=float(np.argmin(qW) / 100), min_qW0=float(qW0.min()),
               argmin_qW0=float(np.argmin(qW0) / 100))

    # ---------------- Q5 exit bound
    leta = np.full(b.nstates, -np.inf)
    for j in cfg["Sref"]:
        x = masks[W]; y = x & ~(1 << j)
        k = np.maximum(G0[y] - G0[x], F[y] - F[x])
        leta[x] = np.logaddexp(leta[x], k)
    le = leta[W]; i = np.argmax(le)
    out.update(log_eta_max=float(le.max()), eta_max_arg=b.fmt(int(masks[W][i])),
               log_eta_le2=float(leta[W2].max()))

    # ---------------- Q6 fixed-Gaussian spread
    nullgroup = list(range(12, 16)) if cfg["name"] == "LH16" else list(range(16, 20))
    gm = bm(nullgroup)
    spread, sp_arg = 0.0, None
    for l in nullgroup:
        if (S0 >> l) & 1: continue
        sel = W2 & ((masks >> l) & 1 == 0)
        x = masks[sel]; y = x | (1 << l)
        ok = feas[y]; x, y = x[ok], y[ok]
        v = F[y] - F[x]; key = x & gm
        for kk in np.unique(key):
            vv = v[key == kk]
            s = vv.max() - vv.min()
            if s > spread: spread, sp_arg = s, (l, b.fmt(int(kk)))
    out.update(Q6_spread=float(spread), Q6_spread_n=float(spread / n), Q6_arg="l=%d, x∩g=%s" % sp_arg if sp_arg else "",
               Q6_group=nullgroup)
    return out


def check_fast():
    cfg = lh_config("LH16"); rng = np.random.default_rng(1)
    z, yy = suff_stats(cfg["R"], cfg["theta"], 1.0, 400, rng)
    a = BVS(cfg["R"], z, yy, 400, cfg["S0"]); f = BVSfast(cfg["R"], z, yy, 400, cfg["S0"])
    fin = np.isfinite(a.lg1)
    return float(max(np.max(np.abs(a.lg1[fin] - f.lg1[fin])), np.max(np.abs(a.lg0[fin] - f.lg0[fin]))))


# keys summarised in the table: (label, getter, worst = 'min' or 'max', fmt)
ROWS = [
    ("m1/n  (post keep margin)", lambda r: r["m1_n"], "min", "%.4f"),
    ("m0/n  (start keep margin)", lambda r: r["m0_n"], "min", "%.4f"),
    ("m1/n at x=S°", lambda r: r["m1_at_Sref"] / r["n"], "min", "%.4f"),
    ("#extras at argmin m1", lambda r: r["m1_arg_ext"], "max", "%d"),
    ("min g1/n (hub gain, post)", lambda r: r["g1min_n"], "min", "%.4f"),
    ("g1/n at x=S°", lambda r: r["g1_at_Sref_n"], "min", "%.4f"),
    ("max g0 (hub gain, start)", lambda r: r["g0max"], "max", "%.3f"),
    ("  ref -log2p-.5log(n+1)", lambda r: r["ref_g0"], "max", "%.3f"),
    ("g0 at x=S°", lambda r: r["g0_at_Sref"], "max", "%.3f"),
    ("max phi* over (x,b)", lambda r: r["phimax"], "max", "%.5f"),
    ("phi* at x=S°", lambda r: r["phi_at_Sref"], "max", "%.5f"),
    ("#(x,b) with g1<=0", lambda r: r["n_g1_le0"], "max", "%d"),
    ("#(x,b) with g0>=0", lambda r: r["n_g0_ge0"], "max", "%d"),
    ("[W] a1", lambda r: r["Q3"]["a1"], "max", "%.3f"),
    ("[W] #F-gain>0", lambda r: r["Q3"]["n_a1_pos"], "max", "%d"),
    ("[W] a0", lambda r: r["Q3"]["a0"], "max", "%.3f"),
    ("[W] dmax", lambda r: r["Q3"]["dmax"], "max", "%.4f"),
    ("[W] dmin", lambda r: r["Q3"]["dmin"], "min", "%.4f"),
    ("[W] log tot1", lambda r: r["Q3"]["log_tot1"], "max", "%.3f"),
    ("[W] log tot0", lambda r: r["Q3"]["log_tot0"], "max", "%.3f"),
    ("[W,<=2ext] a1", lambda r: r["Q3_le2"]["a1"], "max", "%.3f"),
    ("[W,<=2ext] #F-gain>0", lambda r: r["Q3_le2"]["n_a1_pos"], "max", "%d"),
    ("[W,<=2ext] a0", lambda r: r["Q3_le2"]["a0"], "max", "%.3f"),
    ("[W,<=2ext] dmax", lambda r: r["Q3_le2"]["dmax"], "max", "%.4f"),
    ("[W,<=2ext] dmin", lambda r: r["Q3_le2"]["dmin"], "min", "%.4f"),
    ("[W,<=2ext] log tot1", lambda r: r["Q3_le2"]["log_tot1"], "max", "%.3f"),
    ("[W,<=2ext] log tot0", lambda r: r["Q3_le2"]["log_tot0"], "max", "%.3f"),
    ("[W∩{M⊆x}] a1", lambda r: r["Q3_full"]["a1"], "max", "%.3f"),
    ("[W∩{M⊆x}] #F-gain>0", lambda r: r["Q3_full"]["n_a1_pos"], "max", "%d"),
    ("[W∩{M⊆x}] a0", lambda r: r["Q3_full"]["a0"], "max", "%.3f"),
    ("[W∩{M⊆x}] dmax", lambda r: r["Q3_full"]["dmax"], "max", "%.4f"),
    ("[W∩{M⊆x}] dmin", lambda r: r["Q3_full"]["dmin"], "min", "%.4f"),
    ("[W∩{M⊆x}] log tot1", lambda r: r["Q3_full"]["log_tot1"], "max", "%.3f"),
    ("[W∩{M⊆x}] log tot0", lambda r: r["Q3_full"]["log_tot0"], "max", "%.3f"),
    ("[W∩{M⊆x},<=2e] a1", lambda r: r["Q3_full_le2"]["a1"], "max", "%.3f"),
    ("[W∩{M⊆x},<=2e] #F-gain>0", lambda r: r["Q3_full_le2"]["n_a1_pos"], "max", "%d"),
    ("[W∩{M⊆x},<=2e] a0", lambda r: r["Q3_full_le2"]["a0"], "max", "%.3f"),
    ("[W∩{M⊆x},<=2e] dmax", lambda r: r["Q3_full_le2"]["dmax"], "max", "%.4f"),
    ("[W∩{M⊆x},<=2e] dmin", lambda r: r["Q3_full_le2"]["dmin"], "min", "%.4f"),
    ("[W∩{M⊆x},<=2e] log tot1", lambda r: r["Q3_full_le2"]["log_tot1"], "max", "%.3f"),
    ("[W∩{M⊆x},<=2e] log tot0", lambda r: r["Q3_full_le2"]["log_tot0"], "max", "%.3f"),
    ("[W,non-proxy l] a1", lambda r: r["Q3_np"]["a1"], "max", "%.3f"),
    ("[W,non-proxy l] #F-gain>0", lambda r: r["Q3_np"]["n_a1_pos"], "max", "%d"),
    ("[W,non-proxy l] a0", lambda r: r["Q3_np"]["a0"], "max", "%.3f"),
    ("[W,non-proxy l] dmax", lambda r: r["Q3_np"]["dmax"], "max", "%.4f"),
    ("[W,non-proxy l] dmin", lambda r: r["Q3_np"]["dmin"], "min", "%.4f"),
    ("[W,non-proxy l] log tot1", lambda r: r["Q3_np"]["log_tot1"], "max", "%.3f"),
    ("[W,non-proxy l] log tot0", lambda r: r["Q3_np"]["log_tot0"], "max", "%.3f"),
    ("[W,np,<=2ext] a1", lambda r: r["Q3_np_le2"]["a1"], "max", "%.3f"),
    ("[W,np,<=2ext] #F-gain>0", lambda r: r["Q3_np_le2"]["n_a1_pos"], "max", "%d"),
    ("[W,np,<=2ext] a0", lambda r: r["Q3_np_le2"]["a0"], "max", "%.3f"),
    ("[W,np,<=2ext] dmax", lambda r: r["Q3_np_le2"]["dmax"], "max", "%.4f"),
    ("[W,np,<=2ext] dmin", lambda r: r["Q3_np_le2"]["dmin"], "min", "%.4f"),
    ("[W,np,<=2ext] log tot1", lambda r: r["Q3_np_le2"]["log_tot1"], "max", "%.3f"),
    ("[W,np,<=2ext] log tot0", lambda r: r["Q3_np_le2"]["log_tot0"], "max", "%.3f"),
    ("|W|", lambda r: r["absW"], "max", "%d"),
    ("log10 pi0(W^c)", lambda r: r["log_pi0_Wc"] / np.log(10), "max", "%.2f"),
    ("log10 pi(W^c)", lambda r: r["log_pi_Wc"] / np.log(10), "max", "%.2f"),
    ("pi0(W0)", lambda r: r["pi0_W0"], "min", "%.4f"),
    ("pi(W0)", lambda r: r["pi_W0"], "min", "%.4f"),
    ("min_phi q_phi(W)", lambda r: r["min_qW"], "min", "%.6f"),
    ("min_phi q_phi(W0)", lambda r: r["min_qW0"], "min", "%.4f"),
    ("  argmin phi for q(W0)", lambda r: r["argmin_qW0"], "max", "%.2f"),
    ("log10 max eta", lambda r: r["log_eta_max"] / np.log(10), "max", "%.2f"),
    ("log10 max eta [<=2 ext]", lambda r: r["log_eta_le2"] / np.log(10), "max", "%.2f"),
    ("Q6 spread", lambda r: r["Q6_spread"], "max", "%.3f"),
    ("Q6 spread/n", lambda r: r["Q6_spread_n"], "max", "%.2e"),
]


def main():
    reps = {"LH16": int(sys.argv[1]) if len(sys.argv) > 1 else 20, "LH20": int(sys.argv[2]) if len(sys.argv) > 2 else 5}
    t0 = time.time()
    lines = []
    def P(s=""):
        print(s, flush=True); lines.append(s)
    diff = check_fast()
    P("F-SHARE/H1 f1_exact_lh.py — exact checks on W = {x : S° ⊆ x} (seed %d); BVSfast vs BVS max |diff| = %.2e" % (SEED, diff))
    allres = {"seed": SEED, "fast_check_maxdiff": diff, "configs": {}}
    for ci, nm in enumerate(["LH16", "LH20"]):
        cfg = lh_config(nm)
        P(); P("=" * 100)
        P("%s: p=%d, S0=%s, S°=%s, M=%s, reps=%d, sigma=1" % (nm, cfg["p"], cfg["S0"], cfg["Sref"], cfg["M"], reps[nm]))
        res = {}
        for n in NS:
            rr = []
            for r in range(reps[nm]):
                rng = np.random.default_rng([SEED, ci, n, r])
                z, yy = suff_stats(cfg["R"], cfg["theta"], 1.0, n, rng)
                b = BVSfast(cfg["R"], z, yy, n, cfg["S0"])
                assert [sorted(x) for x in b.blocks] == [list(range(c, c + 4)) for c in range(0, cfg["p"], 4)]
                rr.append(analyse(b, cfg))
            res[n] = rr
            print("  %s n=%d done (%.0fs)" % (nm, n, time.time() - t0), flush=True)
        allres["configs"][nm] = {"cfg": {k: cfg[k] for k in ("p", "S0", "Sref", "M", "pairs", "vis")},
                                 "results": {str(n): res[n] for n in NS}}
        P("%-28s " % "quantity [median | worst]" + " ".join("%22s" % ("n=%d" % n) for n in NS))
        for lab, g, w, f in ROWS:
            cells = []
            for n in NS:
                v = np.array([g(r) for r in res[n]], float)
                med = np.nanmedian(v) if np.any(np.isfinite(v)) else np.nan
                wv = (np.nanmin(v) if w == "min" else np.nanmax(v)) if np.any(np.isfinite(v)) else np.nan
                cells.append("%10s|%-11s" % (f % med if f != "%d" else "%d" % round(med), f % wv if f != "%d" else "%d" % wv))
            P("%-28s " % lab + " ".join(cells))
        P("argmin / argmax states (worst replicate):")
        for n in NS:
            rr = res[n]
            i1 = int(np.argmin([r["m1_n"] for r in rr])); i0 = int(np.argmin([r["m0_n"] for r in rr]))
            ig = int(np.argmin([r["g1min_n"] for r in rr])); ip = int(np.argmax([r["phimax"] for r in rr]))
            ia = int(np.argmax([r["Q3"]["a1"] for r in rr])); ie = int(np.argmax([r["log_eta_max"] for r in rr]))
            iaf = int(np.argmax([r["Q3_full"]["a1"] for r in rr])); ian = int(np.argmax([r["Q3_np"]["a1"] for r in rr]))
            P("  n=%-6d m1:%s  m0:%s  g1min:%s  g0max:%s  phi*max:%s  eta:%s  Q6:%s" % (
                n, rr[i1]["m1_arg"], rr[i0]["m0_arg"], rr[ig]["g1min_arg"], rr[ig]["g0max_arg"], rr[ip]["phimax_arg"],
                rr[ie]["eta_max_arg"], rr[0]["Q6_arg"]))
            P("           a1[W]:%s  a1[W∩{M⊆x}]:%s  a1[W,non-proxy]:%s" % (
                rr[ia]["Q3"]["a1_arg"], rr[iaf]["Q3_full"]["a1_arg"], rr[ian]["Q3_np"]["a1_arg"]))
    P(); P("total runtime %.0fs" % (time.time() - t0))
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "f1_exact_lh.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(RES, "f1_exact_lh.json"), "w", encoding="utf-8") as fh:
        json.dump(allres, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))


if __name__ == "__main__":
    main()
