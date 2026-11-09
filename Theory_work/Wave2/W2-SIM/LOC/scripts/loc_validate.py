r"""loc_validate.py -- validation of loc_core's fast re-implementations against W2-FAC-B bvs_core (unchanged). v2 (R01-1/2/3).
Exit status 1 if any check fails.
(A) Partition: lc.fast_partition(X) (scipy linkage + reference-tie certificate, fallback = bc.partition) == bc.partition(X)
    on every design family used, several n/p/seeds; plus constructed cases: the R01 near-tie counterexample
    (r01 = .5, r12 = .5 + 5e-11, r02 = .1, B = 2) and an exact duplicate column.
(B) LS0: lc.ls_loc(prob, c, cap) vs bc.local_search(prob, c, cap): identical path (tuple sequence), final, certified and
    local-limit flags, for centres: start mode; empty set (forces additions); start mode minus one truth (missing truth);
    start mode + 3 random nulls; caps 0 and 2 (move-limit stops; ls_loc's returned_prod is also checked against the best
    neighbour of the last centre computed EXHAUSTIVELY with bc scores); K boundary (Problem with K = |centre|: no adds);
    exact ties (data set with a duplicated null column); large correlated start modes (AF d = .4, n = 2000, p = 500).
(C) All-neighbour scores: for several centres (incl. |centre| > 100) the fast score of EVERY neighbour vs the exact
    bc score (prob.F_many): max |fast - exact|, compared with the screening window 1e-3.
"""
import sys, os, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loc_core as lc
from loc_core import bc, np
import loc_run

FAIL = []


def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + extra if extra else ""), flush=True)
    if not ok:
        FAIL.append(name)


def exhaustive_best(prob, S):
    nb = bc.neighbours(S, prob.p, prob.K)
    Fv = prob.F_many(nb)
    mx = Fv.max()
    return min(nb[i] for i in np.flatnonzero(Fv == mx)), float(mx), nb, Fv


def ls_compare(tag, prob, c, cap):
    t = time.time(); r1 = bc.local_search(prob, c, cap); t1 = time.time() - t
    t = time.time(); r2 = lc.ls_loc(prob, c, cap); t2 = time.time() - t
    ok = (r1["path"] == r2["path"] and r1["final"] == r2["final"] and r1["certified"] == r2["certified"]
          and r1["local_limit"] == r2["local_limit"])
    types = "".join((s.get("move") or "")[:1] for s in r2["steps"])
    extra = f"|c|={len(c)} cap={cap} moves={r1['moves']} types={types[:60]} cert={r1['certified']} lim={r1['local_limit']} t_bc={t1:.1f}s t_fast={t2:.1f}s"
    if r1["local_limit"]:
        best, bF, _, _ = exhaustive_best(prob, r1["final"])
        ok_ret = tuple(r2["returned_prod"]) == best and bF > prob.F(r1["final"])
        extra += f" returned_prod==exhaustive_best:{ok_ret}"
        ok = ok and ok_ret
    check("LS " + tag, ok, extra)
    return r1


def all_neighbour(tag, prob, S):
    S = tuple(sorted(S))
    fs = lc.fast_neighbour_F(prob, S)
    J = fs["J"]
    models, fast = [], []
    if fs["add"] is not None:
        for i, j in enumerate(J):
            models.append(tuple(sorted(S + (int(j),)))); fast.append(fs["add"][i])
    for a in range(len(S)):
        models.append(S[:a] + S[a + 1:]); fast.append(fs["dele"][a])
    if fs["swap"] is not None:
        for a in range(len(S)):
            for jj, j in enumerate(J):
                models.append(tuple(sorted(S[:a] + S[a + 1:] + (int(j),)))); fast.append(fs["swap"][a, jj])
    t = time.time()
    ex = prob.F_many(models)
    err = float(np.max(np.abs(ex - np.array(fast))))
    check("ALLNB " + tag, np.all(np.isfinite(fast)) and err < 1e-6,
          f"|S|={len(S)} neighbours={len(models)} max|fast-exact|={err:.2e} (window 1e-3) t={time.time()-t:.0f}s")


def exact_gram(R, n, seed):
    rng = np.random.default_rng(seed)
    Zm = rng.standard_normal((n, R.shape[0])); Zm -= Zm.mean(0)
    Q, _ = np.linalg.qr(Zm)
    return np.sqrt(n - 1) * Q @ np.linalg.cholesky(R).T


# ---------------- (A) partition ----------------
print("== (A) partition", flush=True)
for (fam, par, place, n, pr) in [("PT", 1.5, "adj", 400, "q"), ("PT", 0.5, "spread", 800, "q"), ("PT", 10.0, "spread", 600, "q"),
                                 ("AF", 0.4, "adj", 1000, "q"), ("AF", 0.25, "spread", 2000, "s"), ("PT", 4.0, "adj", 2000, "q"),
                                 ("CSG", (0.5, 0.8), "two", 2000, "q"), ("CSG", (0.35, 0.5), "one4", 1600, "q"),
                                 ("CSG", (0.2, 0.8), "twoM", 800, "q"), ("PT", 0.8, "adj", 4000, "q")]:
    for seed in (1, 2):
        X, y, S0, theta, spec, p = loc_run.run(fam, par, place, n, pr, 900 + seed, return_data=True)
        b1 = bc.partition(X)
        b2, inf = lc.fast_partition(X, return_info=True)
        check(f"PART {fam} {par} {place} n={n} {pr} s={seed} p={p}", b1 == b2, str(inf))
R = np.array([[1, .5, .1], [.5, 1, .50000000005], [.1, .50000000005, 1]])
X = exact_gram(R, 50, 1)
b2, inf = lc.fast_partition(X, 2, return_info=True)
check("PART R01 near-tie counterexample", bc.partition(X, 2) == b2 and inf["fallback"], f"{b2} {inf}")
X, y, *_ = loc_run.run("PT", 1.5, "adj", 400, "q", 7, return_data=True)
X = X.copy(); X[:, 10] = X[:, 11]
b2, inf = lc.fast_partition(X, return_info=True)
check("PART duplicate column", bc.partition(X) == b2, str(inf))

# ---------------- (B) LS paths ----------------
print("== (B) local search paths", flush=True)
cases = [("PT", 1.5, "adj", 400, "q"), ("PT", 0.5, "spread", 800, "q"), ("AF", 0.4, "adj", 1000, "q"),
         ("CSG", (0.5, 0.8), "twoM", 1200, "q"), ("CSG", (0.5, 0.8), "two", 1200, "q"), ("PT", 10.0, "adj", 600, "q"),
         ("AF", 0.25, "spread", 2000, "s")]
for (fam, par, place, n, pr) in cases:
    seed = 3
    X, y, S0, theta, spec, p = loc_run.run(fam, par, place, n, pr, 900 + seed, return_data=True)
    prob = bc.Problem(X, y)
    info = bc.start_mode(prob, lc.fast_partition(X))
    mode = tuple(info.mode)
    ell = bc.ell_cap(n, p)
    tag = f"{fam} {par} {place} n={n} p={p}"
    ls_compare(tag + " start", prob, mode, ell + len(mode))
    ls_compare(tag + " empty", prob, (), ell)
    miss = tuple(sorted(set(mode) - {S0[1]}))
    ls_compare(tag + " start-minus-truth", prob, miss, ell + len(miss))
    rng = np.random.default_rng(seed)
    nulls = [j for j in range(p) if j not in mode]
    pert = tuple(sorted(set(mode) | set(int(v) for v in rng.choice(nulls, 3, replace=False))))
    ls_compare(tag + " start+3nulls", prob, pert, ell + len(pert))
    ls_compare(tag + " cap0", prob, pert, 0)
    ls_compare(tag + " cap2", prob, pert, 2)
    probK = bc.Problem(X, y, K=len(pert))
    ls_compare(tag + " K=|centre|", probK, pert, ell + len(pert))
# exact ties: duplicated null column next to a truth
X, y, S0, theta, spec, p = loc_run.run("PT", 1.5, "adj", 800, "q", 905, return_data=True)
X = X.copy(); j1 = S0[2] + 1; j2 = S0[2] + 5; X[:, j2] = X[:, j1]
prob = bc.Problem(X, y)
info = bc.start_mode(prob, bc.partition(X))
mode = tuple(info.mode)
for c in [mode, tuple(sorted(set(mode) | {j1})), tuple(sorted(set(mode) | {j2})), ()]:
    ls_compare(f"exact-tie dup({j1},{j2}) centre={c[:8]}", prob, c, bc.ell_cap(800, p) + len(c))
# exact ties forcing the tie rule: duplicate of a TRUTH column (models with the truth or its copy score identically)
X2 = X.copy(); jt = S0[2]; jd = S0[2] + 7; X2[:, jd] = X2[:, jt]
prob2 = bc.Problem(X2, y)
mode2 = tuple(bc.start_mode(prob2, bc.partition(X2)).mode)
for c in [(), mode2, tuple(sorted(set(mode2) | {jt, jd})), tuple(sorted((set(mode2) - {jt}) | {jd}))]:
    ls_compare(f"exact-tie truth-dup({jt},{jd}) centre={c[:8]}", prob2, c, bc.ell_cap(800, p) + len(c))
# large correlated start mode
X, y, S0, theta, spec, p = loc_run.run("AF", 0.4, "adj", 2000, "q", 911, return_data=True)
prob = bc.Problem(X, y)
mode = tuple(bc.start_mode(prob, lc.fast_partition(X)).mode)
ls_compare(f"LARGE AF 0.4 adj n=2000 p={p}", prob, mode, bc.ell_cap(2000, p) + len(mode))

# ---------------- (C) all-neighbour scores ----------------
print("== (C) all-neighbour fast vs exact scores", flush=True)
all_neighbour(f"AF 0.4 adj n=2000 start mode", prob, mode)
all_neighbour(f"AF 0.4 adj n=2000 S0", prob, S0)
for (fam, par, place, n, pr, s) in [("CSG", (0.5, 0.8), "twoM", 4000, "q", 1), ("PT", 0.5, "adj", 4000, "q", 1),
                                    ("CSG", (0.5, 0.8), "one", 8000, "q", 1)]:
    X, y, S0, theta, spec, p = loc_run.run(fam, par, place, n, pr, s, return_data=True)
    prob = bc.Problem(X, y)
    mode = tuple(bc.start_mode(prob, lc.fast_partition(X)).mode)
    all_neighbour(f"{fam} {par} {place} n={n} p={p} start mode", prob, mode)
print("FAILURES:", FAIL)
print("ALL_PASS", not FAIL)
sys.exit(1 if FAIL else 0)
