"""W5-B2ENV s1: population margins on LH used by route (b2) (PROOF.md §4).  Exact, deterministic (no randomness
except the parameter sweep, seed 20261102).

Population residual Delta(V) = theta' Sigma theta - (Sigma theta)_V' Sigma_VV^{-1} (Sigma theta)_V  (exact Gram: in-sample
equals population).  For states S with S° ⊆ S ⊆ (signal units), any subset of the masked groups C_b, and any set of
neutral non-hubs (null groups carry no signal and are omitted: they change no Delta), compute
  STAB  m_del  = min_{S, t in S°}           Delta(S - t)     - Delta(S)
        m_swap = min_{S, t in S°, l notin S} Delta(S - t + l) - Delta(S)
  GAIN  m_gain = min_{S, i: j_b_i notin S}   Delta(S) - Delta(S + j_b_i)
  ZJL   max |<x_l, (I-P_S) mu>| over neutral l notin S   (must be 0)
  PZL   max |<x_k, (I-P_S) mu>| over proxies k notin S when all masked hubs are in S (must be 0)
Neutral extras are limited to at most kneu (all subsets of masked groups allowed).
"""
import itertools, sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lh_family import lh_sigma, lh_truth

out = []
pr = lambda s: (out.append(s), print(s, flush=True))


def margins(G, g, rho, links, visible, kneu=3, nullgroups=()):
    Sig, C = lh_sigma(G, g, rho, 0, links)
    th, S0, M, Sref = lh_truth(G, g, 0, links, visible)
    sig_units = sorted(set(sum([C[a] + C[b] for a, b, _ in links], [])) | set(sum([C[h] for h in visible if all(h != a for a, _, _ in links)], [])))
    bgroups = set(sum([C[b] for _, b, _ in links], []))
    neutral = [j for j in sig_units if j not in S0 and j not in bgroups]
    free = sorted(bgroups)
    v = Sig @ th; tot = th @ Sig @ th

    def Delta(V):
        V = sorted(V)
        if not V: return tot
        A = Sig[np.ix_(V, V)]
        return tot - v[V] @ np.linalg.solve(A, v[V])

    def resid_ip(V, l):
        V = sorted(V)
        if not V: return v[l]
        A = Sig[np.ix_(V, V)]
        coef = np.linalg.solve(A, v[V])          # projection coefficients of mu
        return v[l] - Sig[l, V] @ coef           # <x_l, (I-P_V) mu> / (n-1)

    md = ms = mg = np.inf; zjl = pzl = 0.0; nst = 0
    arg = {}
    for kn in range(kneu + 1):
        for Pn in itertools.combinations(neutral, kn):
            for r in range(len(free) + 1):
                for Pf in itertools.combinations(free, r):
                    S = set(Sref) | set(Pn) | set(Pf); nst += 1
                    dS = Delta(S)
                    outside = [l for l in sig_units if l not in S]
                    for t in Sref:
                        x = Delta(S - {t}) - dS
                        if x < md: md, arg["del"] = x, (sorted(S), t)
                        for l in outside:
                            x = Delta((S - {t}) | {l}) - dS
                            if x < ms: ms, arg["swap"] = x, (sorted(S), t, l)
                    for jb in M:
                        if jb not in S:
                            x = dS - Delta(S | {jb})
                            if x < mg: mg, arg["gain"] = x, (sorted(S), jb)
                    for l in outside:
                        if l in neutral:
                            zjl = max(zjl, abs(resid_ip(S, l)))
                    if all(jb in S for jb in M):
                        for l in outside:
                            if l in free:
                                pzl = max(pzl, abs(resid_ip(S, l)))
    return dict(states=nst, m_del=md, m_swap=ms, m_gain=mg, ZJL=zjl, PZL=pzl, arg=arg,
                R=[(visible[a] ** 2) * psi ** 2 * (1 - psi ** 2) for a, _, psi in links])


CONFIGS = {
    "A": dict(G=4, g=4, rho=0.7, links=[(0, 1, 0.5)], visible={0: 1.4, 2: 1.8}),
    "A85": dict(G=4, g=4, rho=0.85, links=[(0, 1, 0.5)], visible={0: 1.4, 2: 1.8}),
    "B": dict(G=5, g=4, rho=0.7, links=[(0, 1, 0.5), (2, 3, 0.5)], visible={0: 1.4, 2: 1.8}),
}
if __name__ == "__main__" and True:
    for name, cfg in CONFIGS.items():
        r = margins(**cfg)
        pr(f"config {name}: states {r['states']}  m_del={r['m_del']:.4f}  m_swap={r['m_swap']:.4f}  m_gain={r['m_gain']:.4f}  "
           f"ZJL={r['ZJL']:.1e}  PZL={r['PZL']:.1e}  R={np.round(r['R'],4)}")
        pr(f"   argmins: swap {r['arg'].get('swap')}  gain {r['arg'].get('gain')}")
    # sweep: c = 1, one visible group, g = 4, random parameters
    rng = np.random.default_rng(20261102)
    fails = []; nrun = 0
    for rep in range(300):
        rho = rng.uniform(0.2, 0.95); psi = rng.uniform(0.05, 0.95) * rho * rng.choice([-1, 1])
        ba = rng.uniform(0.2, 3) * rng.choice([-1, 1]); bh = rng.uniform(0.2, 3)
        cfg = dict(G=3, g=4, rho=rho, links=[(0, 1, psi)], visible={0: ba, 2: bh})
        r = margins(**cfg, kneu=2); nrun += 1
        if not (r["m_swap"] > 1e-9 and r["m_del"] > 1e-9 and r["m_gain"] > 1e-9):
            fails.append((round(rho, 3), round(psi, 3), round(ba, 3), round(bh, 3), round(r["m_swap"], 4), r["arg"].get("swap")))
    pr(f"sweep c=1, g=4, one visible group, kneu=2: {nrun} parameter draws, STAB/GAIN failures {len(fails)}")
    for f in fails[:12]:
        pr(f"   fail rho={f[0]} psi={f[1]} beta_a={f[2]} beta_h={f[3]} m_swap={f[4]} at {f[5]}")
    # sweep without visible group
    fails2 = 0
    for rep in range(200):
        rho = rng.uniform(0.2, 0.95); psi = rng.uniform(0.05, 0.95) * rho
        cfg = dict(G=2, g=4, rho=rho, links=[(0, 1, psi)], visible={0: 1.0})
        r = margins(**cfg, kneu=3)
        if not (r["m_swap"] > 1e-9 and r["m_del"] > 1e-9 and r["m_gain"] > 1e-9):
            fails2 += 1
    pr(f"sweep c=1, g=4, no visible group, kneu=3: 200 draws, STAB/GAIN failures {fails2}")
    open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")


# ---------------------------------------------------------------- type-based (exchangeability) version, any g
def margins_types(g, rho, links, visible, nvis_groups=None):
    """STAB(inf)/GAIN over ALL states S ⊇ S° inside the signal units (any number of neutral non-hubs), using
    exchangeability within groups: a state is determined by counts; representative sets are exact.
    Group layout: pair i uses groups (2i, 2i+1); visible-only groups follow."""
    G = 2 * len(links) + len([h for h in visible if all(h != a for a, _, _ in links)])
    Sig, C = lh_sigma(G, g, rho, 0, links)
    th, S0, M, Sref = lh_truth(G, g, 0, links, visible)
    v = Sig @ th; tot = th @ Sig @ th
    def Delta(V):
        V = sorted(V)
        if not V: return tot
        return tot - v[V] @ np.linalg.solve(Sig[np.ix_(V, V)], v[V])
    pairs = [(C[a], C[b]) for a, b, _ in links]
    vis = [C[h] for h in visible if all(h != a for a, _, _ in links)]
    # per pair: (has_jb, m_a in 0..g-1, m_b in 0..g-1); per visible: m_h in 0..g-1
    pair_types = [(hb, ma, mb) for hb in (0, 1) for ma in range(g) for mb in range(g)]
    md = ms = mg = np.inf; arg = {}
    for ptys in itertools.product(pair_types, repeat=len(pairs)):
        for vtys in itertools.product(range(g), repeat=len(vis)):
            S = set(Sref)
            for (Ca, Cb), (hb, ma, mb) in zip(pairs, ptys):
                S |= set(Ca[1:1 + ma]) | set(Cb[1:1 + mb]) | ({Cb[0]} if hb else set())
            for Ch, mh in zip(vis, vtys):
                S |= set(Ch[1:1 + mh])
            dS = Delta(S)
            # outside representatives: one per type
            outs = []
            for (Ca, Cb), (hb, ma, mb) in zip(pairs, ptys):
                if ma < g - 1: outs.append(Ca[1 + ma])
                if mb < g - 1: outs.append(Cb[1 + mb])
                if not hb: outs.append(Cb[0])
            for Ch, mh in zip(vis, vtys):
                if mh < g - 1: outs.append(Ch[1 + mh])
            for t in Sref:
                x = Delta(S - {t}) - dS
                if x < md: md, arg["del"] = x, (ptys, vtys, t)
                for l in outs:
                    x = Delta((S - {t}) | {l}) - dS
                    if x < ms: ms, arg["swap"] = x, (ptys, vtys, t, l)
            for jb in M:
                if jb not in S:
                    x = dS - Delta(S | {jb})
                    if x < mg: mg, arg["gain"] = x, (ptys, vtys, jb)
    return md, ms, mg, arg


if __name__ == "__main__" and True:
    out2 = []
    pr2 = lambda s: (out2.append(s), print(s, flush=True))
    pr2("type-based STAB(inf) (all neutral non-hubs allowed), m_del / m_swap / m_gain:")
    for name, cfg in CONFIGS.items():
        md, ms, mg, arg = margins_types(cfg["g"], cfg["rho"], cfg["links"], cfg["visible"])
        pr2(f"  config {name} (g={cfg['g']}): {md:.4f} / {ms:.4f} / {mg:.4f}   argmin swap {arg['swap']}")
    for g in (4, 9, 16):
        for rho in (0.4, 0.7, 0.85):
            for psi in (0.2, 0.5):
                if psi >= rho: continue
                for vis in ({0: 1.4}, {0: 1.4, 2: 1.8}):
                    md, ms, mg, arg = margins_types(g, rho, [(0, 1, psi)], vis)
                    ok = "OK  " if min(md, ms, mg) > 1e-9 else "FAIL"
                    pr2(f"  {ok} g={g:2d} rho={rho} psi={psi} visible={'yes' if len(vis)>1 else 'no '}: "
                        f"m_del={md:.4f} m_swap={ms:.4f} m_gain={mg:.4f}  worst swap {arg['swap']}")
    open(__file__.replace(".py", "_types.txt"), "w").write("\n".join(out2) + "\n")
