"""E4: adversarial designs within the class.
 (i)  combination look-alike: x3 = a(x1+x2)/sqrt(2(1+r12)) + sqrt(1-a^2) z, a=.85, truths x1,x2 (theta=1), 60 nulls (p=63)
 (ii) masked-suppressor cluster: two masked truths m1,m2 + two proxies q1,q2 in group B (g=6), linked to hub a of group A,
      Cov(x_B, mu)=0 exactly; p=60, rho=.7, psi=.4
 (iii) shrinking signals theta=n^-1/4 in the E2 design
"""
import itertools, json, math, time
import numpy as np
import bvs_core as bc, exp_common as ec, lh_common as lc

A_COEF = 0.85


def spec_i(r12):
    p = 63
    c = A_COEF * math.sqrt((1 + r12) / 2)
    Sigma = np.eye(p)
    Sigma[:3, :3] = np.array([[1, r12, c], [r12, 1, c], [c, c, 1.0]])
    th = np.zeros(p)
    th[0] = th[1] = 1.0
    return dict(Sigma=Sigma, theta=th, groups=None, S0=(0, 1), V=(0, 1, 2), ref_Sstar=(0, 1), sigma2=1.0)


def spec_ii(G=10, g=6, rho=0.7, psi=0.4):
    p = G * g
    Sg = (1 - rho) * np.eye(g) + rho * np.ones((g, g))
    Sigma = np.zeros((p, p))
    groups = [tuple(range(h * g, (h + 1) * g)) for h in range(G)]
    for h in range(G):
        Sigma[h * g:(h + 1) * g, h * g:(h + 1) * g] = Sg
    w = np.zeros(g)
    w[0] = w[1] = 1.0  # masked truths = first two members of group B (global idx g, g+1); proxies = members 2,3
    cAB = psi * (Sg @ w)  # Sigma[B, a]
    blk = np.outer(Sg[:, 0], cAB)  # Sigma[A, B] = Sigma[A,a] Sigma[a,B]
    Sigma[0:g, g:2 * g] = blk
    Sigma[g:2 * g, 0:g] = blk.T
    th = np.zeros(p)
    th[0] = 1.0
    th[g + 0] = -psi
    th[g + 1] = -psi
    V = tuple(range(0, 2 * g))
    return dict(Sigma=Sigma, theta=th, groups=groups, S0=(0, g, g + 1), V=V, ref_Sstar=(0,), sigma2=1.0)


_cache = {}


def get_spec(kind, par):
    key = (kind, par)
    if key not in _cache:
        _cache[key] = spec_i(par) if kind == "i" else spec_ii()
    return _cache[key]


_X = {}


def get_X(kind, par, n):
    key = (kind, par, n)
    if key not in _X:
        _X[key] = bc.exact_gram_design(get_spec(kind, par)["Sigma"], n, np.random.default_rng(31 + n))
    return _X[key]


def job(j):
    kind, par, n, seed = j
    spec = get_spec(kind, par)
    X = get_X(kind, par, n)
    y = bc.make_y_std(X, spec["theta"], 1.0, np.random.default_rng(100 * seed + n))
    key = ("e4" + kind, par, n)
    V = spec["V"]
    if kind == "i":
        allC = [tuple(c) for k in range(4) for c in itertools.combinations(V, k)]
        r = ec.analyse(X, y, spec, key, sweep=0, extra_centres=allC)
    else:
        r = ec.analyse(X, y, spec, key, sweep=40, rng=np.random.default_rng(seed))
    blocks = bc.partition(X)
    r["signal_block_ok"] = None
    if kind == "i":
        b0 = [b for b in blocks if 0 in b][0]
        r["signal_block_ok"] = (1 in b0 and 2 in b0)
        prob = bc.Problem(X, y)
        det = {}
        S0 = tuple(sorted(spec["S0"]))
        for C in allC:
            ls = bc.local_search(prob, C, r["ell"])
            fm = ls["first_move"]
            det[str(list(C))] = dict(first=(ec.move_kind(*fm) if fm else "none"),
                                     adds_x3=(fm is not None and 2 in fm[1] and 2 not in fm[0]),
                                     nonprog=(ec.nonprogress(fm[0], fm[1], S0) if fm else None),
                                     reach=S0 in ls["path"], inV=all(set(s) <= set(V) for s in ls["path"]),
                                     moves=ls["moves"], scored=S0 in ls["scored"],
                                     cert=ls["certified"] and ls["final"] == S0)
        r["centres"] = det
    r.update(dict(kind=kind, par=par, seed=seed))
    return r


if __name__ == "__main__":
    t0 = time.time()
    NS = [200, 800, 3200]
    # ---- (i)
    jobs = [("i", r12, n, s) for r12 in (0.0, 0.3) for n in NS for s in range(20)]
    rows_i = ec.pmap(job, jobs)
    ec.write_rows([{k: v for k, v in r.items() if k != "centres"} for r in rows_i], "E4i")
    summ_i = ec.agg(rows_i, ["par", "n"])
    for s in summ_i:
        s["r12"] = s.pop("par")
        rs = [r for r in rows_i if r["par"] == s["r12"] and r["n"] == s["n"]]
        s["x1x2x3 same block"] = ec.frac(rs, "signal_block_ok")
    cen_rows = []
    for r12 in (0.0, 0.3):
        for n in NS:
            rs = [r for r in rows_i if r["par"] == r12 and r["n"] == n]
            for C in rs[0]["centres"]:
                ds = [r["centres"][C] for r in rs]
                nm = sum(1 for d in ds if d["first"] != "none")
                cen_rows.append({"r12": r12, "n": n, "centre(0=x1,1=x2,2=x3)": C,
                                 "first move exists": f"{nm}/20",
                                 "first=add x3": f"{sum(d['adds_x3'] for d in ds)}/20",
                                 "first non-progress": f"{sum(1 for d in ds if d['nonprog'])}/{nm}",
                                 "path in V": f"{sum(d['inV'] for d in ds)}/20",
                                 "reaches S0": f"{sum(d['reach'] for d in ds)}/20",
                                 "S0 scored": f"{sum(d['scored'] for d in ds)}/20",
                                 "cert=S0": f"{sum(d['cert'] for d in ds)}/20",
                                 "max moves": max(d["moves"] for d in ds)})
    pop_i = []
    for r12 in (0.0, 0.3):
        for n in NS:
            spec = get_spec("i", r12)
            pop = bc.Pop(spec["Sigma"], spec["theta"], n)
            blocks = bc.partition_from_corr(spec["Sigma"], bc.block_size(n, 63))
            Us = pop.block_minimisers(blocks)
            vis, va = pop.vis_margin(blocks, Us)
            nl, na = pop.nl_leak(blocks, Us)
            sp = bc.sep_and_decrement(pop, spec["V"])
            pop_i.append(dict(r12=r12, n=n, Sstar=sorted(j for U in Us for j in U), VIS=round(vis, 3), NL=round(nl, 4),
                              zeta=sp["zeta"], dec=round(sp["dec"], 3), dec_over_logn=round(sp["dec"] / math.log(n), 3),
                              corr_x3_x1=round(float(spec["Sigma"][0, 2]), 3)))
    # ---- (ii)
    jobs = [("ii", 0, n, s) for n in NS for s in range(20)]
    rows_ii = ec.pmap(job, jobs)
    ec.write_rows(rows_ii, "E4ii")
    summ_ii = ec.agg(rows_ii, ["n"])
    spec = get_spec("ii", 0)
    pop_ii = []
    for n in NS:
        pop = bc.Pop(spec["Sigma"], spec["theta"], n)
        blocks = [list(g) for g in spec["groups"]]
        Us = pop.block_minimisers(blocks)
        vis, va = pop.vis_margin(blocks, Us)
        nl, na = pop.nl_leak(blocks, Us)
        sp = bc.sep_and_decrement(pop, spec["V"])
        covB = float(np.abs(spec["Sigma"][6:12] @ spec["theta"]).max())
        pop_ii.append(dict(n=n, Sstar=sorted(j for U in Us for j in U), VIS=round(vis, 3), NL=round(nl, 4), zeta=sp["zeta"],
                           dec=round(sp["dec"], 3), max_abs_cov_B_mu=covB,
                           lam_min_Sigma=round(float(np.linalg.eigvalsh(spec["Sigma"]).min()), 4)))
    # ---- (iii)
    CFG = [(0.4, 0.2), (0.7, 0.5)]
    jobs = [(12, 9, rho, psi, c, n, s, True) for (rho, psi) in CFG for c in (1, 2) for n in NS for s in range(20)]
    rows_iii = ec.pmap(lc.job_exact, jobs)
    ec.write_rows(rows_iii, "E4iii")
    summ_iii = ec.agg(rows_iii, ["rho", "psi", "c", "n"])
    pop_iii = []
    for (rho, psi) in CFG:
        for c in (1, 2):
            for n in NS:
                d = lc.population_checks(lc.spec_cached(12, 9, rho, psi, c, n, True), n)
                d.update(rho=rho, psi=psi, c=c)
                pop_iii.append(d)
    with open("E4_summary.md", "w") as f:
        f.write("## E4(i) combination look-alike (p=63, exact Gram, a=0.85, theta1=theta2=1, 60 nulls); 20 seeds\n\n")
        f.write("Route from the LS0 start mode:\n\n")
        f.write(ec.md_table(summ_i, ["r12", "n", "N", "x1x2x3 same block", "start=S*", "|start| (min-max)", "path in V", "moves (max)", "ell", "S0 scored", "certified", "HPM=S0", "max(1-pi0(S*))"]))
        f.write("\nPopulation:\n\n" + ec.md_table(pop_i))
        f.write("\nLocal search from every centre C subset V={x1,x2,x3} (per-centre counts over 20 seeds):\n\n" + ec.md_table(cen_rows))
        f.write("\n## E4(ii) masked-suppressor cluster (p=60, g=6, rho=.7, psi=.4); 20 seeds. a=idx0; masked truths m1,m2=idx 6,7; proxies idx 8,9\n\n")
        f.write(ec.md_table(summ_ii))
        f.write("\nPopulation:\n\n" + ec.md_table(pop_ii))
        f.write("\n## E4(iii) shrinking signals theta=n^-1/4 in the E2 design; 20 seeds\n\n")
        f.write(ec.md_table(summ_iii))
        f.write("\nPopulation (blocks = groups):\n\n")
        pp = [{k: (("%.3g" % v) if isinstance(v, float) else v) for k, v in d.items() if k != "Sstar_pop"} for d in pop_iii]
        f.write(ec.md_table(pp, ["rho", "psi", "c", "n", "Sstar_eq_ref", "VIS_margin", "NL_leak", "zeta", "dec", "dec_over_logn", "n_theta2", "logn"]))
    json.dump(dict(i=summ_i, pop_i=pop_i, ii=summ_ii, pop_ii=pop_ii, iii=summ_iii, pop_iii=pop_iii), open("E4_summary.json", "w"), indent=1, default=str)
    print(open("E4_summary.md").read())
    print("secs", time.time() - t0)
