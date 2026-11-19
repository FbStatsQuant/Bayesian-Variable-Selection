#!/usr/bin/env python3
"""reproj_w1.py -- independent (Opus) re-projection of the 10^4 overlap rung after W1.

Model (NOT the Sonnet w1_projection.py structure):
  * Tier-0 calibration of a T fit is a two-regime process (observed: K0 = 1 or K0 in 11..14+, nothing in between):
      fast  (prob pi_d):  grid identical at rebuild 1;
      slow  (1 - pi_d):   K = ceil(exp(Z)), Z ~ N(mu_d, sig^2); converges at K if K <= 14, else hits the cap ell = 14
                          -> grid_unconverged -> escalation (calib.h:243, 270-273).
    Plus eps = P(a non-cap trigger (E1/E2/E3/local_limit) fires on a converged fit) -> escalation without the cap.
    Hierarchy: mu_d = mu0 + tau * z_d + shift_d over the designs AR, ARweak, ADJ, IND.
  * Tier-1 rebuild count K1: mixture. With prob phi the tier-1 grid behaves like the tier-0 slow regime of that design
    (K1 = ceil(exp(Z))), else K1 ~ Geometric(p). Capped at ell = 14 (tier 1 is final: calib.h:271).
  * Posterior by importance weighting of prior draws with the likelihood of the 8 observed T fits (W0 counted + W1);
    W0 evidence repeats are the same seeds (deterministic: ADJ 12 = 12, AR 14 = 14) and are not new observations.
  * Cost from wall seconds (calibrate 48 CPU, wall/75 = core-h): o0 + K0*g0 + esc*(0.8*g0 + K1*3.46*g0); per-rebuild
    seconds g0 from cost-file mtimes (rebuild_times.py); islands at N_final; dataset factor (new datasets) and node factor.
  * Calibrate wall > 10,800 s (3:00) -> TIMEOUT: 144 core-h billed, stage fails, and (engine deterministic) the fit
    must be re-run with a raised limit: cost = 144 + full fit. Counted in the rung total.
Reproducible: python3 -I reproj_w1.py  (seed fixed). Read-only; writes nothing.
"""
import numpy as np
from math import log
from scipy.stats import norm

SEED = 20261118
NPRIOR = 1_500_000
NPOST = 300_000
SPENT = 254.74 + 277.90          # W0 incl. 91.50 evidence + W1 (sacct)
SPENT_COUNTED = 163.24 + 277.90
CAP = 14
CAL_LIMIT_S = 10_800.0
CORE_PER_S = 48.0 / 3600.0       # calibrate runs on 48 CPUs (89.56 core-h / 6,717 s)
D = ["AR", "ARweak", "ADJ", "IND"]
# measured design constants (seconds / core-h)
G0 = {"AR": 230.0, "ARweak": 144.0, "ADJ": 206.0}          # tier-0 rebuild wall s (AR 213/246, ADJ 193/219, ARweak 144)
O0 = {"AR": 60.0, "ARweak": 37.0, "ADJ": 60.0}             # start-up + tier-0 pilot (IND s1 60, ADJ 58, ARweak s2 37)
ISL10 = {"AR": 49.21 / 4.0, "ARweak": 7.14, "ADJ": 12.57}   # islands at N 1e4 (ADJ: 12.29 / 12.85)
ISL40 = {"AR": 49.21, "ARweak": 24.99, "ADJ": 12.57 * 4.08}  # islands at N 4e4 (IND 4.16x, ARweak 3.50x)
VCOST = {"AR": (2.42, 0.25), "ARweak": (1.69, 0.12), "ADJ": (2.38, 0.25)}
FIXED = 0.033 + 0.06             # setup + merge + eval
G1_RATIO = 3.46                  # tier-1 rebuild / tier-0 rebuild wall (AR 3.39, IND 3.56, ARweak 3.44)
PIL1 = 0.8                       # tier-1 pilot / g0 (AR ~0.8, IND 0.76, ARweak 0.89)
# remaining T fits: (design, dataset, wave); dataset r01 of AR and ADJ was measured (factor 1)
REM = [("ARweak", "ARweak-r02", "W2"), ("ARweak", "ARweak-r02", "W2"),
       ("ADJ", "ADJ-r01", "W2"), ("ADJ", "ADJ-r02", "W2"), ("ADJ", "ADJ-r02", "W2"),
       ("AR", "AR-r01", "W2")] + [("AR", f"AR-r0{r}", "W3") for r in (2, 3, 4) for _ in (1, 2)]
FIT_NAMES = ["ARweak r02 s1", "ARweak r02 s2", "ADJ r01 s2", "ADJ r02 s1", "ADJ r02 s2", "AR r01 s2"] + \
            [f"AR r0{r} s{s}" for r in (2, 3, 4) for s in (1, 2)]
V_FITS = {"W2": ["ARweak", "ARweak", "ADJ", "ADJ", "ADJ", "AR"], "W3": ["AR"] * 6}

# observations (W0 counted + W1 T fits)
REGIME = {"AR": (0, 1), "ARweak": (1, 1), "ADJ": (0, 1), "IND": (0, 2)}      # (fast, slow)
SLOW_K = {"AR": [None], "ARweak": [None], "ADJ": [12], "IND": [11, None]}     # None = censored > 14
N_CONVERGED = 5                                                              # no non-cap trigger on 5 converged fits
TIER1 = [("AR", 1), ("ARweak", 1), ("IND", 3)]


def draw_prior(rng, n, cfg):
    P = {"mu0": rng.normal(log(cfg["mu0_center"]), 0.5, n),
         "tau": np.abs(rng.normal(0, 0.25, n)),
         "sig": np.abs(rng.normal(0, 0.30, n)) + 0.05,
         "eps": rng.beta(*cfg["eps_prior"], n),
         "phi": rng.beta(*cfg["phi_prior"], n),
         "p": rng.beta(*cfg["p_prior"], n)}
    for d in D:
        P["mu_" + d] = P["mu0"] + P["tau"] * rng.normal(0, 1, n) + cfg["shift"].get(d, 0.0)
        P["pi_" + d] = rng.beta(*cfg["pi_prior"][d], n)
    return P


def pK_eq(k, mu, sig):           # P(ceil(exp Z) = k)
    return norm.cdf((log(k) - mu) / sig) - (norm.cdf((log(k - 1) - mu) / sig) if k > 1 else 0.0)


def pK_gt(k, mu, sig):           # P(exp Z > k)
    return norm.sf((log(k) - mu) / sig)


def loglik(P, extra=None):
    ll = np.zeros_like(P["mu0"])
    obs_reg = {d: list(v) for d, v in REGIME.items()}
    obs_k = {d: list(v) for d, v in SLOW_K.items()}
    nconv = N_CONVERGED
    t1 = list(TIER1)
    if extra:                    # scenario observations: list of (design, regime 'fast'/'slow', K0 or None, K1 or None)
        for d, reg, k0, k1 in extra:
            f, s = obs_reg[d]
            obs_reg[d] = [f + (reg == "fast"), s + (reg == "slow")]
            if reg == "slow":
                obs_k[d].append(k0)
            if k0 is not None or reg == "fast":
                nconv += 1
            if k1 is not None:
                t1.append((d, k1))
    for d in D:
        f, s = obs_reg[d]
        ll += f * np.log(P["pi_" + d]) + s * np.log1p(-P["pi_" + d])
        for k in obs_k[d]:
            ll += np.log(np.maximum(pK_eq(k, P["mu_" + d], P["sig"]) if k else pK_gt(CAP, P["mu_" + d], P["sig"]), 1e-300))
    ll += nconv * np.log1p(-P["eps"])
    for d, k in t1:
        geo = P["p"] * (1 - P["p"]) ** (k - 1)
        slow = pK_eq(k, P["mu_" + d], P["sig"]) if k < CAP else pK_gt(CAP - 1, P["mu_" + d], P["sig"])
        ll += np.log((1 - P["phi"]) * geo + P["phi"] * slow)
    return ll


def posterior(rng, cfg, extra=None):
    P = draw_prior(rng, NPRIOR, cfg)
    ll = loglik(P, extra)
    w = np.exp(ll - ll.max()); w /= w.sum()
    ess = 1.0 / np.sum(w ** 2)
    idx = rng.choice(NPRIOR, NPOST, p=w)
    return {k: v[idx] for k, v in P.items()}, ess


def simulate(rng, Q, cfg, fits=None):
    """simulate remaining T fits (and V) for each posterior draw. Returns dict of arrays."""
    n = len(Q["mu0"])
    fits = list(range(len(REM))) if fits is None else fits
    dsf = {}
    for d, ds, w in REM:
        if ds not in dsf:
            sd = 0.0 if ds in ("AR-r01", "ADJ-r01") else cfg["ds_sd"]
            dsf[ds] = np.exp(rng.normal(0, sd, n))
    out = {"cost": np.zeros((n, len(REM))), "esc": np.zeros((n, len(REM)), bool), "to": np.zeros((n, len(REM)), bool),
           "k1": np.zeros((n, len(REM)), int)}
    eta = {}
    for j in fits:
        d, ds, w = REM[j]
        if cfg.get("eta_sd", 0) > 0:
            if ds not in eta:
                eta[ds] = rng.normal(0, cfg["eta_sd"], n)
            mu = Q["mu_" + d] + eta[ds]
        else:
            mu = Q["mu_" + d]
        sig = Q["sig"]
        fast = rng.random(n) < Q["pi_" + d]
        K = np.ceil(np.exp(rng.normal(mu, sig)))
        K0 = np.where(fast, 1, np.minimum(K, CAP))
        esc_cap = (~fast) & (K > CAP)
        esc = esc_cap | (rng.random(n) < Q["eps"])
        slow1 = rng.random(n) < Q["phi"]
        K1s = np.ceil(np.exp(rng.normal(mu, sig)))
        K1g = rng.geometric(Q["p"])
        K1 = np.minimum(np.where(slow1, K1s, K1g), CAP).astype(int)
        g0 = G0[d] * dsf[ds] * np.exp(rng.normal(0, cfg["node_sd"], n))
        wall = O0[d] + K0 * g0 + esc * (PIL1 * g0 + K1 * G1_RATIO * g0)
        isl = np.where(esc, ISL40[d], ISL10[d]) * dsf[ds] * np.exp(rng.normal(0, 0.04, n))
        full = FIXED + wall * CORE_PER_S + isl
        lim = cfg.get("cal_limit_W3", cfg["cal_limit"]) if w == "W3" else cfg["cal_limit"]
        to = wall > lim
        cost = np.where(to, 0.033 + lim * CORE_PER_S + full, full)
        out["cost"][:, j] = cost; out["esc"][:, j] = esc; out["to"][:, j] = to; out["k1"][:, j] = np.where(esc, K1, 0)
        out.setdefault("full", np.zeros((n, len(REM))))[:, j] = full
    V = {w: sum(rng.normal(*VCOST[d], n) for d in V_FITS[w]) for w in V_FITS}
    wave = {w: V[w] + out["cost"][:, [j for j in fits if REM[j][2] == w]].sum(1) for w in V_FITS}
    out["W2"], out["W3"] = wave["W2"], wave["W3"]
    out["total"] = SPENT + wave["W2"] + wave["W3"]
    return out


def fit_cost_det(d, reg, k0, k1):
    """cost of a W2 T fit at the mean speeds for a scenario (TIMEOUT -> 144 + re-run)"""
    K0 = 1 if reg == "fast" else (CAP if k0 is None else k0)
    esc = k1 is not None
    wall = O0[d] + K0 * G0[d] + esc * (PIL1 * G0[d] + (k1 or 0) * G1_RATIO * G0[d])
    full = FIXED + wall * CORE_PER_S + (ISL40[d] if esc else ISL10[d])
    return full + (0.033 + CAL_LIMIT_S * CORE_PER_S if wall > CAL_LIMIT_S else 0.0)


BASE = {"mu0_center": 10.0, "shift": {"AR": 0.15}, "eps_prior": (0.5, 0.5), "phi_prior": (0.25, 4.75),
        "p_prior": (1, 1), "pi_prior": {"AR": (0.5, 3.5), "ARweak": (1, 3), "ADJ": (1, 3), "IND": (1, 3)},
        "ds_sd": 0.08, "node_sd": 0.06, "cal_limit": CAL_LIMIT_S, "eta_sd": 0.0}


def q(x, ps=(10, 50, 90)):
    return [float(np.percentile(x, v)) for v in ps]


def report(label, cfg, rng, extra=None, full=False, w3_quote=None):
    Q, ess = posterior(rng, cfg, extra)
    o = simulate(rng, Q, cfg)
    t = o["total"]
    over172 = (o["cost"] > 172.5) | o["to"]
    line = (f"{label:<58s} ESS {ess:8.0f} | W2 {o['W2'].mean():5.0f} [{q(o['W2'])[0]:4.0f},{q(o['W2'])[2]:4.0f}] "
            f"W3 {o['W3'].mean():5.0f} [{q(o['W3'])[0]:4.0f},{q(o['W3'])[2]:4.0f}] | rung {t.mean():5.0f} "
            f"P10/50/90 {q(t)[0]:4.0f}/{q(t)[1]:4.0f}/{q(t)[2]:4.0f} | P>1.6k {np.mean(t>1600):.2f} P>2.1k {np.mean(t>2100):.3f} "
            f"P>2.5k {np.mean(t>2500):.4f} | P(any>172) {over172.any(1).mean():.3f} P(TO) {o['to'].any(1).mean():.3f}")
    pes = []
    for d in ("AR", "ADJ", "ARweak"):
        pe = (1 - Q["pi_" + d]) * norm.sf((log(CAP) - Q["mu_" + d]) / Q["sig"]); pe = pe + (1 - pe) * Q["eps"]
        pes.append(f"{pe.mean():.2f}")
    print(line + " | P(esc) AR/ADJ/ARw " + "/".join(pes) + f" | E#>172 {over172.sum(1).mean():.2f}")
    if full:
        print("  posterior means: " + ", ".join(f"{k} {Q[k].mean():.3f}" for k in
              ["mu0", "tau", "sig", "eps", "phi", "p"] + [f"mu_{d}" for d in D] + [f"pi_{d}" for d in D]))
        for d in ("AR", "ARweak", "ADJ"):
            pe = (1 - Q["pi_" + d]) * norm.sf((log(CAP) - Q["mu_" + d]) / Q["sig"])
            pe = pe + (1 - pe) * Q["eps"]
            print(f"  P(esc) {d}: mean {pe.mean():.3f}  P10-P90 {np.percentile(pe,10):.2f}-{np.percentile(pe,90):.2f}")
        print("  per fit: name, P(esc), E cost, P90 cost, P(>172 completed), P(TIMEOUT), E k1|esc")
        for j, nm in enumerate(FIT_NAMES):
            e = o["esc"][:, j]
            print(f"   {nm:<14s} {e.mean():.3f} {o['cost'][:,j].mean():7.1f} {np.percentile(o['cost'][:,j],90):7.1f} "
                  f"{np.mean((o['cost'][:,j]>172.5)&~o['to'][:,j]):.4f} {o['to'][:,j].mean():.4f} {o['k1'][e,j].mean():.2f}")
        nesc = o["esc"].sum(1)
        print(f"  escalations in 12 remaining T: E {nesc.mean():.2f} P10-P90 {q(nesc,(10,90))}")
        cum2 = SPENT + o["W2"]
        print(f"  cum after W2: E {cum2.mean():.0f} P90 {np.percentile(cum2,90):.0f}; P(W2>960) {np.mean(o['W2']>960):.4f}; "
              f"P(W2>480) {np.mean(o['W2']>480):.3f}")
        print(f"  W2 P(any>172 or TO) {over172[:, :6].any(1).mean():.3f} (TO {o['to'][:, :6].any(1).mean():.3f}); W3 {over172[:, 6:].any(1).mean():.3f} (TO {o['to'][:, 6:].any(1).mean():.3f})")
        anyto = o["to"].any(1)
        print(f"  P(>2.1k & TO) {np.mean((t>2100)&anyto):.4f}  P(>2.1k & no TO) {np.mean((t>2100)&~anyto):.4f}; "
              f"P(>1.6k & no TO) {np.mean((t>1600)&~anyto):.3f}; E rung | no TO {t[~anyto].mean():.0f}, | TO {t[anyto].mean():.0f}")
        print(f"  max single-fit cost P99.9 {np.percentile(o['cost'].max(1), 99.9):.0f}; full (no-TO) fit cost max over draws {o['full'].max():.0f}")
        for nm, mask in (("ADJ", [2, 3, 4]), ("AR", list(range(5, 12)))):
            print(f"  P(any {nm} fit >172 or TO) {over172[:, mask].any(1).mean():.3f}")
        for qq in (600, 650, 700, 720, 750):
            print(f"  W3 quote {qq}: P(W3 > quote) {np.mean(o['W3']>qq):.3f}  P(W3 > 2x) {np.mean(o['W3']>2*qq):.4f}")
        # stop-rule-adjusted: cumulative 1.6k / 2.1k trip during W3
        print(f"  P(cum after W2 > 1.6k) {np.mean(cum2>1600):.4f};  P(total > 2.0k) {np.mean(t>2000):.3f}")
        # no-TIMEOUT-rerun accounting (TIMEOUT fit counted at 144 + rerun) vs without rerun
        t_norerun = t - (o["cost"] - np.where(o["to"], 0.033 + cfg["cal_limit"] * CORE_PER_S, o["cost"])).sum(1)
        print(f"  rung if TIMEOUT fits were NOT re-run: E {t_norerun.mean():.0f} P90 {np.percentile(t_norerun,90):.0f}")
    return Q, o


if __name__ == "__main__":
    import sys
    rng = np.random.default_rng(SEED)
    print("=== BASE (full) ===")
    Q, o = report("BASE", BASE, rng, full=True)
    print("\n=== SENSITIVITY ===")
    def cfgw(**kw):
        c = {k: (dict(v) if isinstance(v, dict) else v) for k, v in BASE.items()}
        for k, v in kw.items():
            c[k] = v
        return c
    rows = [
        ("tier-1 tail: phi = 0 (pure geometric, p~Beta(1,1))", cfgw(phi_prior=(1e-6, 1e6))),
        ("tier-1 tail: phi ~ Beta(0.5,3.5) prior (post. mean .07)", cfgw(phi_prior=(0.5, 3.5))),
        ("tier-1 tail: phi ~ Beta(1,3) prior (post. mean .14)", cfgw(phi_prior=(1, 3))),
        ("tier-1 geometric optimistic p~Beta(3,1) prior", cfgw(p_prior=(3, 1))),
        ("AR esc low: no AR shift, pi_AR~Beta(1,3)", cfgw(shift={}, pi_prior={**BASE["pi_prior"], "AR": (1, 3)})),
        ("AR esc high: shift +0.35, pi_AR~Beta(0.2,4)", cfgw(shift={"AR": 0.35}, pi_prior={**BASE["pi_prior"], "AR": (0.2, 4)})),
        ("slow-K centre prior 7 (easier)", cfgw(mu0_center=7.0)),
        ("slow-K centre prior 14 (harder)", cfgw(mu0_center=14.0)),
        ("eps ~ 0 (only the cap escalates)", cfgw(eps_prior=(1e-6, 1e6))),
        ("dataset latent eta sd 0.15 (seeds of a dataset correlated)", cfgw(eta_sd=0.15)),
        ("calibrate limit raised to 4:00 now (14,400 s)", cfgw(cal_limit=14_400.0)),
        ("dataset cost factor sd 0.15", cfgw(ds_sd=0.15)),
        ("AR esc ~0.9 (F16 'certain'): shift +0.6, pi_AR~Beta(0.1,5)", cfgw(shift={"AR": 0.6}, pi_prior={**BASE["pi_prior"], "AR": (0.1, 5)})),
        ("calibrate limit 5:00 (18,000 s): no TIMEOUT possible", cfgw(cal_limit=18_000.0)),
        ("5:00 limit + phi ~ Beta(1,3) prior", cfgw(cal_limit=18_000.0, phi_prior=(1, 3))),
    ]
    for lab, c in rows:
        report(lab, c, rng)
    if "--scen" in sys.argv:
        print("\n=== W2 READ-BACK SCENARIOS (BASE; W2 outcome added as observations, W3 re-projected) ===")
        # (design, regime, K0 (None = cap), K1) for the 6 W2 T fits
        scen = {
            "S1 benign: AR esc k1=1; ADJ 1/3 esc k1=1 (others K0 12,13); ARweak 1 fast,1 esc k1=1":
                [("AR", "slow", None, 1), ("ADJ", "slow", None, 1), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                 ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
            "S2 typical-bad: AR esc k1=3; ADJ 2/3 esc k1=1,2; ARweak 2/2 esc k1=1":
                [("AR", "slow", None, 3), ("ADJ", "slow", None, 1), ("ADJ", "slow", None, 2), ("ADJ", "slow", 13, None),
                 ("ARweak", "slow", None, 1), ("ARweak", "slow", None, 1)],
            "S3 AR per-fit stop: AR esc k1=7 (>172); ADJ 1/3 esc k1=1":
                [("AR", "slow", None, 7), ("ADJ", "slow", None, 1), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                 ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
            "S4 tier-1 slow: AR esc k1=14 (TIMEOUT); ADJ 2/3 esc k1=1,4":
                [("AR", "slow", None, 14), ("ADJ", "slow", None, 1), ("ADJ", "slow", None, 4), ("ADJ", "slow", 13, None),
                 ("ARweak", "slow", None, 1), ("ARweak", "slow", None, 1)],
            "S3b AR k1=9 (completes ~192 at mean speed); ADJ 1/3 esc k1=1":
                [("AR", "slow", None, 9), ("ADJ", "slow", None, 1), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                 ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
            "S4b ADJ TIMEOUT: ADJ esc k1=14; AR esc k1=1; ARweak 1/2 esc":
                [("AR", "slow", None, 1), ("ADJ", "slow", None, 14), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                 ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
            "S5 good: AR fast (no esc); ADJ 0/3 esc; ARweak 1 fast":
                [("AR", "fast", None, None), ("ADJ", "slow", 11, None), ("ADJ", "slow", 12, None), ("ADJ", "fast", None, None),
                 ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
        }
        NPRIOR = 3_000_000
        for lab, ex in scen.items():
            Qs, ess = posterior(rng, BASE, ex)
            os_ = simulate(rng, Qs, BASE, fits=list(range(6, 12)))
            w3 = os_["W3"]
            w2a = 13.0 + sum(fit_cost_det(*x) for x in ex)
            tot = SPENT + w2a + w3
            over = ((os_["cost"][:, 6:] > 172.5) | os_["to"][:, 6:]).any(1)
            print(f"{lab}\n   ESS {ess:.0f}; W3 E {w3.mean():.0f} P10/50/90 {[round(v) for v in q(w3)]}; "
                  f"P(any W3 AR fit >172 or TO) {over.mean():.3f}; P(TO) {os_['to'][:,6:].any(1).mean():.3f}; "
                  f"E esc AR {Qs['pi_AR'].mean():.2f}(pi)\n   W2 actual (mean speeds) {w2a:.0f}; rung at W2 read-back E {tot.mean():.0f} "
                  f"P10/50/90 {[round(v) for v in q(tot)]}; P>1.6k {np.mean(tot>1600):.2f} P>2.1k {np.mean(tot>2100):.3f} P>2.5k {np.mean(tot>2500):.4f}")
