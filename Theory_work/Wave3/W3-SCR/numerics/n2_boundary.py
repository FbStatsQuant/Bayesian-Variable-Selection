"""W3-SCR N2: boundary-violation numerics. Hunt locally optimal (LO) models of the coded neighbourhood with the coded
local search (own implementation, scr_lib.py; unlimited moves so every endpoint is LO) from many starts, in scenarios
that satisfy or violate each assumption of SCR-A / SCR-C.

Usage: py -3.13 n2_boundary.py SCENARIO [reps] > n2_out/SCENARIO.txt     (JSON lines + a summary line)
Scenarios (n = 100, p = 400 unless stated; sigma = 1; S0 = {2,26,53,75}, theta = bscale*(1.4,-1.0,1.8,-1.2)):
  iid_strong, cs_strong (rho .5), fac_strong (k = 3), ar_strong (rho .7)      -- assumptions hold
  iid_weak (bscale .35)                                                       -- visibility fails (weak signal)
  twin90, twin99, twin999   (each truth has a twin with that correlation)      -- identifiability margin fails
  masked (S0 = {2,26}, corr .9, theta = (2,-2))                               -- margin holds, visibility fails
  noisecs98 (noise columns equicorrelated .98, truths independent of them)    -- sparse floor fails, anchored floor holds
  dupnoise (cs .5, half of the noise columns are near-copies of the others)   -- sparse floor fails at size 2
  fac_p1000 (k = 3, p = 1000)                                                 -- strong factors, p = 10 n
  pairs_iid, pairs_cs20, pairs_cs50, pairs_cs80                               -- SCR-C boundary: LO supersets S0 + {j,l}
"""
import json, math, sys
import numpy as np
from scr_lib import Score, standardise

scen = sys.argv[1]; reps = int(sys.argv[2]) if len(sys.argv) > 2 else 20
# optional third argument "diag=R": only draw R; for every LO endpoint missing a truth print the noiseless visibility
# ratio  max_t sqrt(gamma(t|S)) / (sigma_S sqrt(T_n))  (< 1: the visibility hypothesis fails at that model even without noise)
diag = int(sys.argv[3].split("=")[1]) if len(sys.argv) > 3 else None
n, p = 100, 400
S0 = [2, 26, 53, 75]; coef = np.array([1.4, -1.0, 1.8, -1.2]); bscale = 1.0
if scen == "fac_p1000": p = 1000
if scen == "iid_weak": bscale = 0.35
if scen == "masked": S0 = [2, 26]; coef = np.array([2.0, -2.0])
seed0 = sum(ord(c) * (i + 1) for i, c in enumerate(scen)) + 20261109


def make(rng):
    if scen.startswith("iid") or scen == "pairs_iid":
        X = rng.standard_normal((n, p))
    elif scen in ("cs_strong", "pairs_cs50"):
        X = math.sqrt(.5) * rng.standard_normal((n, 1)) + math.sqrt(.5) * rng.standard_normal((n, p))
    elif scen == "pairs_cs20":
        X = math.sqrt(.2) * rng.standard_normal((n, 1)) + math.sqrt(.8) * rng.standard_normal((n, p))
    elif scen == "pairs_cs80":
        X = math.sqrt(.8) * rng.standard_normal((n, 1)) + math.sqrt(.2) * rng.standard_normal((n, p))
    elif scen in ("fac_strong", "fac_p1000"):
        k = 3; L = rng.uniform(.2, .9, (p, k)) / math.sqrt(k)
        X = rng.standard_normal((n, k)) @ L.T + rng.standard_normal((n, p)) * np.sqrt(1 - (L ** 2).sum(1))
    elif scen == "ar_strong":
        E = rng.standard_normal((n, p)); X = E.copy()
        for j in range(1, p): X[:, j] = .7 * X[:, j - 1] + math.sqrt(1 - .49) * E[:, j]
    elif scen.startswith("twin"):
        r = {"twin90": .9, "twin99": .99, "twin999": .999}[scen]
        X = rng.standard_normal((n, p))
        for t in S0: X[:, t + 1] = r * X[:, t] + math.sqrt(1 - r * r) * rng.standard_normal(n)
    elif scen == "masked":
        X = rng.standard_normal((n, p)); X[:, 26] = .9 * X[:, 2] + math.sqrt(1 - .81) * rng.standard_normal(n)
    elif scen == "noisecs98":
        X = math.sqrt(.98) * rng.standard_normal((n, 1)) + math.sqrt(.02) * rng.standard_normal((n, p))
        X[:, S0] = rng.standard_normal((n, len(S0)))
    elif scen == "dupnoise":
        X = math.sqrt(.5) * rng.standard_normal((n, 1)) + math.sqrt(.5) * rng.standard_normal((n, p))
        h = p // 2
        for j in range(h):
            if j not in S0 and (j + h) not in S0: X[:, j + h] = X[:, j] + 1e-3 * rng.standard_normal(n)
    else:
        raise SystemExit("unknown scenario")
    return X


def diagnostics(Xs, theta):
    """Design quantities at the truth: anchored quantities for a few random sparse S (not the exact minima)."""
    G = Xs.T @ Xs / (n - 1)
    off = np.abs(G - np.eye(p)); np.fill_diagonal(off, 0)
    return dict(max_abs_corr=float(off.max()), min_eig_S0=float(np.linalg.eigvalsh(G[np.ix_(S0, S0)]).min()))


summary = dict(scenario=scen, n=n, p=p, reps=reps, draws_with_LO_missing_q8=0, draws_with_LO_missing_q16=0,
               draws_with_LO_missing_any_size=0, draws_with_LO_strict_superset=0, draws_S0_is_LO=0,
               endpoint_sizes={}, n_endpoints=0, endpoints_missing=0, LO_pair_supersets=[])
for rep in (range(reps) if diag is None else [diag]):
    rng = np.random.default_rng(seed0 + 1000 * rep)
    X = make(rng); theta = np.zeros(p); theta[S0] = bscale * coef
    y = X @ theta + rng.standard_normal(n)
    Xs = standardise(X)
    sc = Score(Xs, standardise(y), standardised=True)
    K = sc.K; nonS0 = [j for j in range(p) if j not in S0]
    if scen.startswith("pairs"):
        # LO supersets of the form S0 + {j, l}: screen by the two deletions, then full LO check of the survivors
        F1 = sc.add_all(S0)[0]
        cands = []
        for j in nonS0:
            Fj = sc.add_all(sorted(S0 + [j]))[0]
            for l in np.where(Fj >= np.maximum(F1[j], F1) )[0]:
                l = int(l)
                if l > j and l not in S0: cands.append((j, l))
        lo_pairs = [pr for pr in cands if sc.is_certified(sorted(S0 + list(pr)))]
        lo_single = [int(j) for j in nonS0 if F1[j] >= sc.F(S0) and sc.is_certified(sorted(S0 + [j]))]
        rec = dict(rep=rep, S0_is_LO=sc.is_certified(S0), n_pair_candidates=len(cands), n_LO_pairs=len(lo_pairs),
                   n_LO_singles=len(lo_single), LO_pairs=lo_pairs[:5])
        summary["LO_pair_supersets"].append(len(lo_pairs)); summary["draws_S0_is_LO"] += rec["S0_is_LO"]
        summary["draws_with_LO_strict_superset"] += (len(lo_pairs) + len(lo_single) > 0)
        print(json.dumps(rec)); sys.stdout.flush(); continue
    starts = [("empty", []), ("truth", list(S0))]
    corr = np.abs(Xs.T @ Xs[:, S0]) / (n - 1); corr[S0, :] = 0
    starts.append(("proxies", sorted(set(int(corr[:, i].argmax()) for i in range(len(S0))))))
    for i in range(10): starts.append((f"rand5_{i}", sorted(rng.choice(nonS0, 5, replace=False).tolist())))
    for i in range(5): starts.append((f"rand15_{i}", sorted(rng.choice(nonS0, 15, replace=False).tolist())))
    for i in range(3): starts.append((f"rand30_{i}", sorted(rng.choice(nonS0, 30, replace=False).tolist())))
    for i in range(3): starts.append((f"randK-2_{i}", sorted(rng.choice(nonS0, K - 2, replace=False).tolist())))
    ends = {}
    for name, st in starts:
        r = sc.local_search(st)
        key = tuple(r["returned"])
        ends.setdefault(key, dict(from_=[], moves=r["moves"]))["from_"].append(name)
    recs = []
    for key, info in ends.items():
        S = list(key); miss = [t for t in S0 if t not in S]
        recs.append(dict(size=len(S), missing=len(miss), eq_S0=(sorted(S) == sorted(S0)), extra=len([j for j in S if j not in S0]),
                         F=round(sc.F(S), 4), n_starts=len(info["from_"]), starts=info["from_"][:4]))
    if diag is not None:
        mu_s = Xs @ (theta * np.sqrt((X - X.mean(0)).var(0, ddof=1)))        # mean in the standardised-column parametrisation
        lam0 = 1.0 / (n + 1); Tn = (1 + 1 / n) * (2 * math.log(2 * p - 1) + math.log(n + 1))
        for key in ends:
            S = list(key); T = [t for t in S0 if t not in S]
            if not T: continue
            XS = Xs[:, S]
            R = np.eye(n) - (XS @ np.linalg.solve(XS.T @ XS + lam0 * np.eye(len(S)), XS.T) if S else 0)
            gam = max(float(Xs[:, t] @ R @ mu_s) ** 2 / (float(Xs[:, t] @ R @ Xs[:, t]) + lam0) for t in T)
            sS2 = 1.0 + float(mu_s @ R @ mu_s) / (n - 1)
            print(f"DIAG rep {rep}: LO endpoint size {len(S)} missing {len(T)}: sqrt(gamma_max)={math.sqrt(gam):.2f}, sigma_S={math.sqrt(sS2):.2f}, "
                  f"sqrt(T_n)={math.sqrt(Tn):.2f}, visibility ratio={math.sqrt(gam / (sS2 * Tn)):.2f}, F(S0)-F(S)={sc.F(S0) - sc.F(S):.1f}")
    d = diagnostics(Xs, theta)
    rec = dict(rep=rep, F_S0=round(sc.F(S0), 4), endpoints=recs, **d)
    print(json.dumps(rec)); sys.stdout.flush()
    summary["n_endpoints"] += len(recs)
    summary["endpoints_missing"] += sum(e["missing"] > 0 for e in recs)
    summary["draws_with_LO_missing_q8"] += any(e["missing"] > 0 and e["size"] <= 8 for e in recs)
    summary["draws_with_LO_missing_q16"] += any(e["missing"] > 0 and e["size"] <= 16 for e in recs)
    summary["draws_with_LO_missing_any_size"] += any(e["missing"] > 0 for e in recs)
    summary["draws_with_LO_strict_superset"] += any(e["missing"] == 0 and e["extra"] > 0 for e in recs)
    summary["draws_S0_is_LO"] += any(e["eq_S0"] for e in recs)
    for e in recs:
        b = "0-8" if e["size"] <= 8 else "9-16" if e["size"] <= 16 else f"17-{K - 1}" if e["size"] < K else f"K={K}"
        summary["endpoint_sizes"][b] = summary["endpoint_sizes"].get(b, 0) + 1
print("SUMMARY " + json.dumps(summary))
