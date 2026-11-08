"""N6: deterministic logic of Lemma LS and (C), exact enumeration, p=10 (g=2, c=2 linked pairs, 1 null group)."""
import math
import numpy as np
from lhcommon import Tee
from enumlib import *

out = Tee("n6_ls_and_C.txt")
out("N6 n6_ls_and_C.py -- Lemma LS and (C) on the p=10 miniature (g=2, c=2, rho=.7, psi=.5, beta=1, sigma=1); exact enumeration of 1024 models")
out("S0 = %s, masked hubs M = {%d,%d}, S-degree = %s, start = S-degree; ell = ceil(log2(n+p+1))" % (S0, JB[0], JB[1], SDEG))
NS = [50, 200, 1000]
NSEEDS = 20
c = CC
tot_viol = []
for n in NS:
    ell = math.ceil(math.log2(n + P + 1))
    rows = []
    for seed in range(NSEEDS):
        X, y = make_data(n, [20260108, 6, n, seed])
        F, K = enumerate_F(X, y)
        pi, lse = posterior(F)
        states = lattice_states()
        Dres = [check_DS(F, K, S, I) for (S, I) in states]
        D_all = all(h for h, _ in Dres)
        Dmargin = min(m for _, m in Dres)
        Lh, Lm = check_L(F, K)
        ls = local_search(F, K, SDEG, ell)
        scored_S0 = S0 in ls["scored"]
        certified = (ls["status"] == "local_certified" and ls["final"] == S0)
        best_scored = best_of(list(ls["scored"]), F)
        MAP = best_of(list(F.keys()), F)
        # lemma LS (i): path
        lat = set(S for S, _ in states) | {S0}
        # Lemma LS(i) concerns the FIRST c moves only: they must be additions of masked hubs inside Lat and end at S0.
        # (Further moves after S0 are possible iff (L) fails and are not constrained by (i).)
        pth = ls["path"]
        path_ok = (len(pth) >= c + 1 and pth[c] == S0 and all(s in lat for s in pth[:c + 1])
                   and all(set(pth[i + 1]) - set(pth[i]) <= set(JB) and len(pth[i + 1]) == len(pth[i]) + 1 for i in range(c)))
        rows.append(dict(seed=seed, D_all=D_all, Dm=Dmargin, L=Lh, Lm=Lm, scored=scored_S0, cert=certified, status=ls["status"],
                         final=ls["final"], moves=ls["moves"], scans=ls["scans"], path_ok=path_ok, piS0=pi[S0], MAP=MAP == S0,
                         best_scored_is_S0=(best_scored == S0), nscored=len(ls["scored"]), ell=ell, path=ls["path"]))
    out("\n" + "=" * 100)
    out("n = %d   (K = %d, ell = %d, #models = 1024, %d seeds)" % (n, min(P, n // 2), ell, NSEEDS))
    out("%4s | %5s %10s | %5s %10s | %6s %9s %15s %5s | %7s %5s %5s" % ("seed", "D_all", "minDmargin", "(L)", "L-margin", "scored", "certified", "status/final", "moves", "pi(S0)", "MAP", "bestS"))
    for r in rows:
        out("%4d | %5s %10.3f | %5s %10.3f | %6s %9s %15s %5d | %7.4f %5s %5s" %
            (r["seed"], r["D_all"], r["Dm"], r["L"], r["Lm"], r["scored"], r["cert"], r["status"][6:] + ("@S0" if r["final"] == S0 else "@" + str(r["final"])), r["moves"],
             r["piS0"], r["MAP"], r["best_scored_is_S0"]))
    nD = sum(r["D_all"] for r in rows); nL = sum(r["L"] for r in rows); nSc = sum(r["scored"] for r in rows); nCe = sum(r["cert"] for r in rows)
    # implications
    imp1_prem = [r for r in rows if r["D_all"] and r["ell"] >= c - 1]
    imp1_viol = [r for r in imp1_prem if not r["scored"]]
    imp0_viol = [r for r in rows if r["D_all"] and not r["path_ok"]]
    imp2_prem = [r for r in rows if r["D_all"] and r["L"] and r["ell"] >= c]
    imp2_viol = [r for r in imp2_prem if not (r["cert"] and r["status"] == "local_certified" and r["moves"] == c)]
    C_prem = [r for r in rows if r["scored"] and r["piS0"] > 0.5]
    C_viol = [r for r in C_prem if not r["best_scored_is_S0"]]
    C_all_prem = [r for r in rows if r["piS0"] > 0.5]
    out("Summary n=%d:" % n)
    out("  D_S holds on all lattice states: %d/%d;  (L) holds: %d/%d;  search scores S0: %d/%d;  search certifies S0: %d/%d" % (nD, NSEEDS, nL, NSEEDS, nSc, NSEEDS, nCe, NSEEDS))
    out("  pi(S0)>1/2: %d/%d; MAP = S0: %d/%d" % (sum(r["piS0"] > 0.5 for r in rows), NSEEDS, sum(r["MAP"] for r in rows), NSEEDS))
    out("  Lemma LS(i)  [D_all => first c moves each add a masked hub, states in Lat, c-th state = S0]: premise true %d, violations %d" % (nD, len(imp0_viol)))
    out("  Lemma LS(ii) [D_all and ell>=c-1 => S0 scored]:                                  premise true %d, violations %d" % (len(imp1_prem), len(imp1_viol)))
    out("  Lemma LS(iii)[D_all and (L) and ell>=c => certified at S0, no local_limit]:      premise true %d, violations %d" % (len(imp2_prem), len(imp2_viol)))
    out("  (C) [S0 scored and pi(S0)>1/2 => best scored model = S0]:                        premise true %d, violations %d" % (len(C_prem), len(C_viol)))
    out("  (C') [pi(S0)>1/2 => MAP = S0] premise true %d, violations %d" % (len(C_all_prem), sum(not r["MAP"] for r in C_all_prem)))
    conv = [r for r in rows if (not r["D_all"]) and r["scored"]]
    out("  info: seeds where D_all fails but S0 is still scored: %d; D_all fails and S0 not scored: %d; scored without certification: %d" %
        (len(conv), sum((not r["D_all"]) and (not r["scored"]) for r in rows), sum(r["scored"] and not r["cert"] for r in rows)))
    out("  info: (L) fails in %d seeds; of those pi(S0) values: %s" % (sum(not r["L"] for r in rows), ["%.3f" % r["piS0"] for r in rows if not r["L"]]))
    for r in imp0_viol + imp1_viol + imp2_viol + C_viol:
        tot_viol.append((n, r["seed"]))
        out("  VIOLATION at n=%d seed=%d path=%s status=%s" % (n, r["seed"], r["path"], r["status"]))
out("\nTOTAL implication violations over all n and seeds: %s" % ("none" if not tot_viol else tot_viol))
out("\nDONE")
out.close()
